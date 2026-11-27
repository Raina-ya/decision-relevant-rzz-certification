"""Prespecified analysis for the exploratory hardware pilot HW-P2.

Input: results/hw_p2/<label>/<block>.json written by hardware/run_hw_p2.py.
Output: per (pair, angle) finite-sample M0 boxes, diagnostics, and decision
verdicts; plus direct decision-circuit gaps. Every number this produces is
[hardware-locked, exploratory pilot HW-P2] when the input is hardware data,
or [sim] when the input comes from analysis/hardware/simulate_hw_p2.py.

Prespecified choices (fixed before any data):
- alpha = 0.05 per (pair, angle) box, Bonferroni over all phase intervals in
  that box (probe, delay and k=0 circuits).
- SPAM/reference offset: subtract the k=0 phase of the same role and control;
  delay circuits subtract the k=0 phase of control 0.
- Unwrapping: src/estimate.unwrap_phase_intervals with prior (-pi, pi) on the
  per-gate slope; ambiguity or inconsistency is reported, never resolved.
- Z conservation: control flip rate at the largest k, threshold = upper
  Hoeffding bound of the readout flip rate of that qubit plus 0.02.
- Decisions: gamma interval from src/certify.gamma_interval_per_candidate
  with the instance margin from the development family.
"""

from __future__ import annotations

from collections import defaultdict
import json
from math import pi, sqrt, log
from pathlib import Path

from analysis.tolerance.instances import GeneratedDecision
from src.certify import certify, gamma_interval_per_candidate
from src.decision import EdgeError, signed_gap_per_candidate
from src.diagnostics import z_conservation_diagnostic
from src.estimate import (
    BinomialCount,
    CircularInterval,
    LinearInterval,
    UnwrapStatus,
    four_phase_confidence,
    recover_m0_intervals,
    unwrap_phase_intervals,
)
from src.probes import ANALYSIS_PHASES

ALPHA = 0.05
REPO = Path(__file__).resolve().parents[2]
FAMILY = REPO / "analysis" / "tolerance" / "instances_development.json"


def _wrap(angle: float) -> float:
    return (angle + pi) % (2 * pi) - pi


def _bits(counts: dict[str, int]) -> tuple[dict[int, int], int]:
    """Return per-bit zero counts (bit 0 = rightmost) and total shots."""
    total = sum(counts.values())
    zeros: dict[int, int] = defaultdict(int)
    for key, value in counts.items():
        key = key.replace(" ", "")
        for position, char in enumerate(reversed(key)):
            if char == "0":
                zeros[position] += value
    return zeros, total


def load_blocks(paths: list[Path]) -> list[dict]:
    return [json.loads(path.read_text(encoding="utf-8")) for path in paths]


def readout_flip_rates(records: list[dict]) -> dict[int, tuple[float, int]]:
    """Per local bit: worst-case assignment flip rate over prepared states."""
    worst: dict[int, tuple[float, int]] = {}
    for record in records:
        meta = record["meta"]
        if meta["type"] != "readout":
            continue
        zeros, total = _bits(record["counts"])
        for bit in range(meta["qubits"]):
            prepared_one = (meta["prepared"] >> bit) & 1
            wrong = zeros[bit] if prepared_one else total - zeros[bit]
            rate = wrong / total
            if bit not in worst or rate > worst[bit][0]:
                worst[bit] = (rate, total)
    return worst


def analyze_probe_records(records: list[dict], alpha: float = ALPHA) -> list[dict]:
    probes = [r for r in records if r["meta"]["type"] == "probe"]
    readout = readout_flip_rates(records)
    by_pair: dict[tuple, list[dict]] = defaultdict(list)
    for record in probes:
        by_pair[tuple(record["meta"]["pair"])].append(record)
    outputs = []
    for pair, items in by_pair.items():
        table: dict[tuple, list] = defaultdict(lambda: [None] * 4)
        flips: dict[tuple, list[int]] = defaultdict(lambda: [0, 0])
        for record in items:
            m = record["meta"]
            zeros, total = _bits(record["counts"])
            index = ANALYSIS_PHASES.index(m["analysis_phase"])
            kind = m["circuit_kind"]
            theta = None if kind == "k_zero" else m["theta"]
            key = (kind, theta, m["k"], m["control"], m["role"])
            if kind == "anchor":
                continue  # anchors are a drift time series, summarized separately
            table[key][index] = BinomialCount(zeros[0], total)
            if kind == "probe":
                control_zeros = zeros[1]
                wrong = control_zeros if m["control"] == 1 else total - control_zeros
                flips[(theta, m["k"], m["control"], m["role"])][0] += wrong
                flips[(theta, m["k"], m["control"], m["role"])][1] += total
        thetas = sorted({key[1] for key in table if key[0] == "probe"})
        ks_all = sorted({key[2] for key in table if key[0] == "probe"})
        zero_keys = [key for key in table if key[0] == "k_zero" and None not in table[key]]
        for theta in thetas:
            interval_count = 0
            for role in (1, 2):
                interval_count += sum(1 for c in (0, 1) for k in ks_all if None not in table[("probe", theta, k, c, role)])
                interval_count += sum(1 for k in ks_all if None not in table[("delay", theta, k, 0, role)])
            interval_count += len(zero_keys)
            alpha_each = alpha / max(1, interval_count)
            zero_phase = {
                (key[3], key[4]): four_phase_confidence(tuple(table[key]), alpha_each).confidence_interval
                for key in zero_keys
            }
            slopes = {}
            statuses = {}
            point = {}
            for role in (1, 2):
                for label, kind, control in (("c0", "probe", 0), ("c1", "probe", 1), ("delay", "delay", 0)):
                    reference = zero_phase.get((control, role))
                    observations = []
                    centers = []
                    for k in ks_all:
                        cells = table.get((kind, theta, k, control, role))
                        if cells is None or None in cells or reference is None:
                            continue
                        estimate = four_phase_confidence(tuple(cells), alpha_each)
                        center = _wrap(estimate.confidence_interval.center - reference.center)
                        radius = min(pi, estimate.confidence_interval.radius + reference.radius)
                        observations.append((k, CircularInterval(center, radius, 1 - alpha)))
                        centers.append((k, center))
                    result = unwrap_phase_intervals(tuple(observations), LinearInterval(-pi, pi))
                    slopes[(role, label)] = result.interval
                    statuses[(role, label)] = result.status.value
                    # point estimate: slope implied at the largest unwrapped k
                    point[(role, label)] = 0.5 * (result.interval.lower + result.interval.upper)
            entry = {"pair": list(pair), "theta": theta, "alpha": alpha, "intervals_in_union_bound": interval_count,
                     "unwrap_status": {f"r{r}-{l}": s for (r, l), s in statuses.items()}}
            identified = all(s == UnwrapStatus.IDENTIFIED.value for s in statuses.values())
            if identified:
                try:
                    box = recover_m0_intervals(
                        slopes[(1, "c0")], slopes[(1, "c1")], slopes[(1, "delay")],
                        slopes[(2, "c0")], slopes[(2, "c1")], slopes[(2, "delay")],
                    )
                except ValueError as error:
                    identified = False
                    entry["inconsistency"] = str(error)
            if identified:
                entry["epsilon"] = [box.epsilon.lower, box.epsilon.upper]
                entry["a"] = [box.a.lower, box.a.upper]
                entry["b"] = [box.b.lower, box.b.upper]
            if not identified:
                entry["epsilon"] = entry["a"] = entry["b"] = None
            # Z conservation at the largest k
            kmax = max(ks_all)
            diags = []
            for (t, k, c, r), (wrong, total) in flips.items():
                if t != theta or k != kmax:
                    continue
                control_bit = 1
                base_rate, base_total = readout.get(control_bit, (0.0, 1))
                threshold = min(1.0, base_rate + sqrt(log(2 / alpha) / (2 * base_total)) + 0.02)
                result = z_conservation_diagnostic(wrong, total, threshold, alpha)
                diags.append({"k": k, "control": c, "role": r, "flip_rate": wrong / total,
                              "threshold": threshold, "status": result.status.value})
            entry["z_conservation"] = diags
            outputs.append(entry)
    return outputs


def _box(entry: dict) -> tuple[EdgeError, EdgeError] | None:
    if entry is None or entry["epsilon"] is None:
        return None
    mid = lambda iv: 0.5 * (iv[0] + iv[1])  # noqa: E731
    rad = lambda iv: 0.5 * (iv[1] - iv[0])  # noqa: E731
    return (EdgeError(mid(entry["epsilon"]), mid(entry["a"]), mid(entry["b"])),
            EdgeError(rad(entry["epsilon"]), rad(entry["a"]), rad(entry["b"])))


def certify_instance(instance_id: str, residuals: list[dict], chain: list[int]) -> dict:
    family = {r["instance_id"]: r for r in json.loads(FAMILY.read_text(encoding="utf-8"))["instances"]}
    record = dict(family[instance_id])
    record["edges"] = tuple(tuple(edge) for edge in record["edges"])
    decision = GeneratedDecision(**record)
    instance, first, second = decision.objects()
    pairs = [[chain[i], chain[i + 1]] for i in range(instance.qubits - 1)]

    def lookup(pair, theta):
        for entry in residuals:
            if entry["pair"] == pair and abs(entry["theta"] - theta) < 1e-12:
                return _box(entry)
        return None

    boxes = {}
    for which, candidate in (("first", first), ("second", second)):
        centers, radii = [], []
        for pair, theta in zip(pairs, candidate.rzz_angles):
            box = lookup(pair, theta)
            if box is None:
                return {"instance_id": instance_id, "verdict": "not evaluable",
                        "reason": f"no identified residual box for pair {pair} at theta {theta}"}
            centers.append(box[0]); radii.append(box[1])
        boxes[which] = (tuple(centers), tuple(radii))
    confidence = 1 - 2 * ALPHA * len(pairs)  # union over candidate-angle boxes
    interval = gamma_interval_per_candidate(instance, first, second, *boxes["first"], *boxes["second"], confidence)
    point = signed_gap_per_candidate(instance, first, second, boxes["first"][0], boxes["second"][0])
    return {"instance_id": instance_id, "margin": decision.margin, "gamma_point": point,
            "gamma_interval": [interval.lower, interval.upper], "confidence": confidence,
            "verdict": certify(interval, decision.margin).value}


def analyze_decision_records(records: list[dict]) -> list[dict]:
    cuts: dict[tuple, dict] = {}
    for record in records:
        meta = record["meta"]
        if meta["type"] != "decision":
            continue
        family = {r["instance_id"]: r for r in json.loads(FAMILY.read_text(encoding="utf-8"))["instances"]}
        edges = family[meta["instance_id"]]["edges"]
        total = sum(record["counts"].values())
        value = 0.0
        for key, count in record["counts"].items():
            bits = key.replace(" ", "")[::-1]
            value += count * sum(bits[a] != bits[b] for a, b in edges)
        mean = value / total
        radius = len(edges) * sqrt(log(2 * 4 / ALPHA) / (2 * total))
        cuts[(meta["instance_id"], meta["implementation"], meta["candidate"])] = {
            "mean_cut": mean, "radius": radius, "ideal_gap": meta["ideal_gap"]}
    out = []
    for (iid, impl, _), _value in list(cuts.items()):
        if (iid, impl, "first") not in cuts or (iid, impl, "second") not in cuts:
            continue
        if any(o["instance_id"] == iid and o["implementation"] == impl for o in out):
            continue
        f, s = cuts[(iid, impl, "first")], cuts[(iid, impl, "second")]
        sign = 1.0 if f["ideal_gap"] > 0 else -1.0
        gap = sign * (f["mean_cut"] - s["mean_cut"])
        radius = f["radius"] + s["radius"]
        out.append({"instance_id": iid, "implementation": impl, "signed_gap": gap,
                    "interval": [gap - radius, gap + radius],
                    "ideal_decision_preserved": "yes" if gap - radius > 0 else ("no" if gap + radius < 0 else "undetermined")})
    return out


def analyze(paths: list[Path]) -> dict:
    blocks = load_blocks(paths)
    chain = blocks[0]["chain"] if blocks else None
    residuals, decisions = [], []
    for block in blocks:
        residuals.extend({**entry, "block": block["block"], "label": block["label"]}
                         for entry in analyze_probe_records(block["records"]))
        decisions.extend({**entry, "block": block["block"]} for entry in analyze_decision_records(block["records"]))
    certificates = []
    for instance_id in ("path-2q", "path-3q"):
        certificates.append(certify_instance(instance_id, residuals, list(chain)) if chain else None)
    evidence = blocks[0].get("evidence", "[sim]") if blocks else "[sim]"
    return {"evidence": evidence, "residuals": residuals, "certificates": certificates, "direct_decisions": decisions}


if __name__ == "__main__":
    import sys

    files = [Path(p) for p in sys.argv[1:]] or sorted((REPO / "results" / "hw_p2").glob("*/*.json"))
    files = [f for f in files if f.name != "selection.json"]
    print(json.dumps(analyze(files), indent=1))
