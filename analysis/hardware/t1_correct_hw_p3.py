"""HW-P3 Amendment 1: gate-induced control flips over the chip-wide T1 reference.

For every pair, probe angle, k and role, the control-|1> flip rate of the RZZ
probe circuits (blocks P3A1-P3B2) is compared with the delay-only reference
(block P3B3) at equal elapsed time. Hoeffding two-sided intervals at
ALPHA per rate; `excess_lower > 0` marks a gate-induced flip excess. The
re-stated OD11 verdict uses this excess test instead of the absolute flip
threshold. [post-hoc analysis, HW-P3 Amendment 1; both columns are kept]

Readout error enters probe and delay rates alike and cancels in the excess.
The reference was taken about 20 minutes after the probe blocks.
"""

from __future__ import annotations

from collections import defaultdict
import glob
import json
from math import log, sqrt
from pathlib import Path

ALPHA = 0.05
THRESHOLD = 0.07294694083467376  # the allowed flip rate of the HW-P2/HW-P3 Z-conservation diagnostic
REPO = Path(__file__).resolve().parents[2]
P3 = REPO / "results" / "hw_p3"


def _flips(records, index):
    """(theta_or_None, kind, k, role) -> [control flips, shots] for control = 1."""
    out = defaultdict(lambda: [0, 0])
    for r in records:
        m = r["meta"]
        if m["type"] != "probe" or m["control"] != 1 or m["circuit_kind"] not in ("probe", "delay"):
            continue
        counts = r["pair_counts"][index]
        flips = sum(v for key, v in counts.items() if key[0] == "0")  # bit 1 (control) is the left character
        theta = round(m["theta"], 4) if m["circuit_kind"] == "probe" else None
        cell = out[(theta, m["circuit_kind"], m["k"], m["role"])]
        cell[0] += flips
        cell[1] += sum(counts.values())
    return out


def excess_table():
    blocks = [json.loads(Path(f).read_text()) for f in sorted(glob.glob(str(P3 / "*" / "P3*.json")))]
    ref = next(b for b in blocks if b["block"].startswith("P3B3"))
    probes = [b for b in blocks if not b["block"].startswith("P3B3")]
    rows = []
    for index, pair in enumerate(ref["pairs"]):
        delay = _flips(ref["records"], index)
        for block in probes:
            assert block["pairs"] == ref["pairs"]
            for (theta, kind, k, role), (f, n) in sorted(_flips(block["records"], index).items()):
                if kind != "probe":
                    continue
                df, dn = delay[(None, "delay", k, role)]
                rp, rd = sqrt(log(2 / ALPHA) / (2 * n)), sqrt(log(2 / ALPHA) / (2 * dn))
                ex = f / n - df / dn
                rows.append({"pair": pair, "theta": theta, "k": k, "role": role, "probe_rate": f / n,
                             "delay_rate": df / dn, "excess": ex, "excess_lower": ex - rp - rd,
                             "excess_upper": ex + rp + rd})
    return rows


def main():
    rows = excess_table()
    gate = [r for r in rows if r["excess_lower"] > 0]
    over = [r for r in rows if r["excess_lower"] > THRESHOLD]
    flagged_any = {(tuple(r["pair"]), r["theta"]) for r in gate}
    flagged_thr = {(tuple(r["pair"]), r["theta"]) for r in over}
    cert = json.loads((P3 / "certificate_map.json").read_text())
    from analysis.hardware.analyze_hw_p2 import load_family
    from analysis.tolerance.instances import GeneratedDecision
    fam = load_family()
    counts = defaultdict(lambda: defaultdict(int))
    for c in cert:
        rec = dict(fam[c["instance"]]); rec["edges"] = tuple(tuple(x) for x in rec["edges"])
        _, c1, c2 = GeneratedDecision(**rec).objects()
        angles = {round(c1.rzz_angles[0], 4), round(c2.rzz_angles[0], 4)}
        v = c["raw_verdict"]
        for col, flagged in (("od11_excess_any", flagged_any), ("od11_excess_over_threshold", flagged_thr)):
            trig = any((tuple(c["pair"]), a) in flagged for a in angles)
            c[col] = "inconclusive (model-inadequate)" if trig and v != "not evaluable" else v
            counts[c["instance"] + " " + col][c[col]] += 1
        c.pop("od11_t1_corrected", None)
    (P3 / "t1_excess.json").write_text(json.dumps(rows) + "\n")
    (P3 / "certificate_map.json").write_text(json.dumps(cert, indent=1) + "\n")
    summary = {"cells": len(rows), "gate_excess_cells": len(gate), "excess_over_threshold_cells": len(over),
               "pairs_with_gate_excess": sorted({tuple(r["pair"]) for r in gate}),
               "by_theta": {str(t): sum(1 for r in gate if r["theta"] == t) for t in sorted({r["theta"] for r in rows})},
               "median_delay_rate_k32": sorted(r["delay_rate"] for r in rows if r["k"] == 32)[len([r for r in rows if r["k"] == 32]) // 2],
               "od11": {k: dict(v) for k, v in counts.items()}}
    print(json.dumps(summary, indent=1))
    return summary


if __name__ == "__main__":
    main()
