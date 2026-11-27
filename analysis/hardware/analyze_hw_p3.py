"""Analysis for HW-P3 parallel blocks: split per pair, then reuse the HW-P2 analysis.

Same prespecified choices as analyze_hw_p2 (alpha = 0.05 per pair-angle box,
k=0 subtraction, interval unwrapping). Also compares pair (53, 54) in parallel
context with its isolated HW-P2 boxes at the same angle.
"""

from __future__ import annotations

import json
from collections import defaultdict
from math import log, sqrt
from pathlib import Path
import sys

from analysis.hardware.analyze_hw_p2 import _bits, analyze_probe_records


def split_by_pair(block: dict) -> dict[tuple, list[dict]]:
    out: dict[tuple, list[dict]] = {}
    for index, pair in enumerate(block["pairs"]):
        pair = tuple(pair)
        out[pair] = [{"meta": {**r["meta"], "pair": list(pair)}, "counts": r["pair_counts"][index]}
                     for r in block["records"]]
    return out


def analyze_block(block: dict) -> list[dict]:
    entries = []
    for pair, records in split_by_pair(block).items():
        for entry in analyze_probe_records(records):
            entry["block"] = block["block"]
            entries.append(entry)
    return entries


def summarize(entries: list[dict]) -> dict:
    identified = [e for e in entries if e["epsilon"] is not None]
    excludes_zero = [e for e in identified if e["epsilon"][0] > 0 or e["epsilon"][1] < 0]
    return {"boxes": len(entries), "identified": len(identified),
            "epsilon_excludes_zero": [(e["pair"], e["theta"], e["epsilon"]) for e in excludes_zero]}


def t1_excess_analysis(probe_blocks: list[dict], reference_block: dict, alpha: float = 0.05) -> dict:
    """Angle-matched control-|1> flip excess over the delay-only amendment."""
    if not 0.0 < alpha < 1.0:
        raise ValueError("alpha must lie in (0, 1)")
    sums: dict[tuple, list[int]] = defaultdict(lambda: [0, 0])

    def add(block: dict, kind: str) -> None:
        for pair, records in split_by_pair(block).items():
            for record in records:
                meta = record["meta"]
                if meta.get("type") != "probe" or meta.get("control") != 1:
                    continue
                zeros, total = _bits(record["counts"])
                key = (pair, meta["theta"], meta["k"], meta["role"], kind)
                sums[key][0] += zeros[1]
                sums[key][1] += total

    for block in probe_blocks:
        add(block, "probe")
    add(reference_block, "delay")
    matched = []
    for key, (probe_flips, probe_total) in sorted(sums.items()):
        pair, theta, k, role, kind = key
        if kind != "probe":
            continue
        delay = sums.get((pair, theta, k, role, "delay"))
        if delay and probe_total and delay[1]:
            matched.append((pair, theta, k, role, probe_flips, probe_total, delay[0], delay[1]))
    if not matched:
        return {"alpha_family": alpha, "rows": [], "triggered_pairs": []}

    alpha_row = alpha / len(matched)
    rows = []
    triggered_pairs = set()
    for pair, theta, k, role, probe_flips, probe_total, delay_flips, delay_total in matched:
        probe_rate = probe_flips / probe_total
        delay_rate = delay_flips / delay_total
        radius = sqrt(log(2.0 / alpha_row) / (2.0 * probe_total)) + sqrt(
            log(2.0 / alpha_row) / (2.0 * delay_total)
        )
        excess = probe_rate - delay_rate
        triggered = excess - radius > 0.02
        if triggered:
            triggered_pairs.add(pair)
        rows.append({
            "pair": list(pair), "theta": theta, "k": k, "role": role,
            "probe_rate": probe_rate, "delay_rate": delay_rate,
            "excess": excess, "excess_radius": radius, "threshold": 0.02,
            "triggered": triggered,
        })
    return {
        "evidence": "[hardware-locked, exploratory pilot HW-P3; result-informed amendment]",
        "alpha_family": alpha,
        "alpha_per_row": alpha_row,
        "matched_rows": len(rows),
        "rows": rows,
        "triggered_pairs": [list(pair) for pair in sorted(triggered_pairs)],
    }


if __name__ == "__main__":
    files = [Path(p) for p in sys.argv[1:]] or sorted(Path("results/hw_p3").glob("*/P3*.json"))
    blocks = [json.loads(path.read_text(encoding="utf-8")) for path in files]
    references = [block for block in blocks if "t1-reference" in block["block"]]
    probes = [block for block in blocks if "t1-reference" not in block["block"]]
    report = {}
    for block in probes:
        entries = analyze_block(block)
        report[block["block"]] = {"summary": summarize(entries), "entries": entries}
    if references:
        report["P3B3-t1-excess"] = t1_excess_analysis(probes, references[-1])
    print(json.dumps(report, indent=1))
