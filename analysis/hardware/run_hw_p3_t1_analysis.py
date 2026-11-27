"""Write the deterministic, result-informed HW-P3 T1 excess analysis."""

import json
from pathlib import Path

from analysis.hardware.analyze_hw_p3 import t1_excess_analysis


def main() -> None:
    root = Path(__file__).resolve().parents[2]
    paths = sorted((root / "results" / "hw_p3").glob("[AB]/P3*.json"))
    blocks = [json.loads(path.read_text(encoding="utf-8")) for path in paths]
    references = [block for block in blocks if "t1-reference" in block["block"]]
    probes = [block for block in blocks if "t1-reference" not in block["block"]]
    if len(references) != 1:
        raise RuntimeError("expected exactly one HW-P3 T1 reference block")
    result = t1_excess_analysis(probes, references[0])
    result["source_blocks"] = [block["block"] for block in probes]
    result["reference_block"] = references[0]["block"]
    output = root / "results" / "hw_p3" / "t1_excess_analysis.json"
    output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
