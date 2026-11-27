"""Analysis for HW-P3 parallel blocks: split per pair, then reuse the HW-P2 analysis.

Same prespecified choices as analyze_hw_p2 (alpha = 0.05 per pair-angle box,
k=0 subtraction, interval unwrapping). Also compares pair (53, 54) in parallel
context with its isolated HW-P2 boxes at the same angle.
"""

from __future__ import annotations

import json
from pathlib import Path
import sys

from analysis.hardware.analyze_hw_p2 import analyze_probe_records


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


if __name__ == "__main__":
    files = [Path(p) for p in sys.argv[1:]] or sorted(Path("results/hw_p3").glob("*/P3*.json"))
    report = {}
    for path in files:
        block = json.loads(path.read_text(encoding="utf-8"))
        entries = analyze_block(block)
        report[block["block"]] = {"summary": summarize(entries), "entries": entries}
    print(json.dumps(report, indent=1))
