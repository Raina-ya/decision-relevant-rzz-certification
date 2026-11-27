"""Runner for HW-P3 chip-wide parallel probes (owner runs; no token handling).

  python -m hardware.run_hw_p3 --label A                      # dry run, no network
  python -m hardware.run_hw_p3 --label A --submit --account acctA --backend ibm_marrakesh --max-qpu-seconds 110

Stores per-pair 2-bit marginal counts (bit 0 = target, bit 1 = control), not
full bitstrings. Requires docs/decisions/HW-P3-approval.json.
"""

from __future__ import annotations

import argparse
from dataclasses import asdict
import json
from pathlib import Path
import random
import sys
import time

from hardware.approval import ApprovalError, verify_pilot_approval
from hardware.hw_p3_design import PLANS_P3, SEED, select_matching
from hardware.run_hw_p2 import circuit_digest, usage_seconds, utc_now
from src.circuits import semantic_operations
from src.qiskit_adapter import fractional_target, rzz_duration_seconds, to_isa
from src.types import ProbeKey

REPO = Path(__file__).resolve().parents[1]
APPROVAL = REPO / "docs" / "decisions" / "HW-P3-approval.json"
MAX_PUBS_PER_JOB = 290


def parallel_circuit(key: ProbeKey, pairs, seconds: float):
    """Logical circuit: pair p uses logical qubits (2p target-or-control...) mapped by semantic indices."""
    from qiskit import QuantumCircuit

    n = 2 * len(pairs)
    circuit = QuantumCircuit(n, n, name=f"par_{key.circuit_kind.value}")
    for op in semantic_operations(key):
        for p in range(len(pairs)):
            q = [2 * p + i for i in op.qubits]
            if op.name == "x":
                circuit.x(q[0])
            elif op.name == "sx":
                circuit.sx(q[0])
            elif op.name == "rz":
                circuit.rz(op.angle, q[0])
            elif op.name == "rzz":
                circuit.rzz(op.angle, q[0], q[1])
            elif op.name == "barrier":
                pass
            elif op.name == "delay_like_rzz":
                if key.k > 0:
                    circuit.delay(key.k * seconds, q[0], unit="s")
                    circuit.delay(key.k * seconds, q[1], unit="s")
            elif op.name == "measure":
                target, control = q
                circuit.measure(target, 2 * p)
                circuit.measure(control, 2 * p + 1)
        if op.name == "barrier":
            circuit.barrier()
    return circuit


def readout_parallel(pairs):
    from qiskit import QuantumCircuit

    out = []
    for state in range(4):
        n = 2 * len(pairs)
        circuit = QuantumCircuit(n, n, name=f"par_readout_{state:02b}")
        for p in range(len(pairs)):
            for bit in range(2):
                if (state >> bit) & 1:
                    circuit.x(2 * p + bit)
        circuit.measure(range(n), range(n))
        out.append(({"type": "readout", "prepared": state, "qubits": 2}, circuit))
    return out


def verify_parallel(isa, key: ProbeKey, pairs) -> None:
    per_pair = {tuple(sorted(p)): 0 for p in pairs}
    for inst in isa.data:
        if inst.operation.name == "rzz":
            qs = tuple(sorted(isa.find_bit(q).index for q in inst.qubits))
            if qs not in per_pair:
                raise RuntimeError(f"rzz on unexpected pair {qs}")
            if abs(float(inst.operation.params[0]) - key.theta) > 1e-12:
                raise RuntimeError("rzz angle changed by the transpiler")
            per_pair[qs] += 1
        elif inst.operation.name not in {"rz", "sx", "x", "rzz", "barrier", "measure", "delay"}:
            raise RuntimeError(f"unexpected ISA operation {inst.operation.name}")
    expected = key.k if key.circuit_kind.value in ("probe", "anchor") else 0
    if any(count != expected for count in per_pair.values()):
        raise RuntimeError(f"rzz count per pair != {expected}")


def build(block, target, pairs):
    layout = [q for pair in pairs for q in pair]
    seconds = max(rzz_duration_seconds(target, p) for p in pairs)
    items = []
    for key in block.keys:
        isa = to_isa(parallel_circuit(key, pairs, seconds), target, tuple(layout))
        verify_parallel(isa, key, pairs)
        items.append(({"type": "probe", **{**asdict(key), "circuit_kind": key.circuit_kind.value}}, isa))
    for meta, circuit in readout_parallel(pairs):
        items.append((meta, to_isa(circuit, target, tuple(layout))))
    order = list(range(len(items)))
    random.Random(SEED + sum(map(ord, block.name))).shuffle(order)
    return [items[i] for i in order]


def marginals(bitarray, npairs: int) -> list[dict[str, int]]:
    return [bitarray.slice_bits([2 * p, 2 * p + 1]).get_counts() for p in range(npairs)]


def dry_run(label: str) -> Path:
    from qiskit_ibm_runtime.fake_provider import FakeMarrakesh

    target = fractional_target(FakeMarrakesh().target)
    pairs = select_matching(target)
    out = REPO / "hardware" / "dry_run" / f"P3{label}"
    out.mkdir(parents=True, exist_ok=True)
    summary = {"label": label, "backend": "fake_marrakesh+fractional[fake-backend]", "pairs": pairs,
               "qubits_used": 2 * len(pairs), "blocks": []}
    for block in PLANS_P3[label]:
        items = build(block, target, pairs)
        summary["blocks"].append({"block": block.name, "circuits": len(items), "shots": block.shots})
    path = out / "dry_run_summary.json"
    path.write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8", newline="\n")
    return path


def submit(label, account, backend_name, max_seconds, only):
    try:
        approval = verify_pilot_approval(REPO, APPROVAL, Path(__file__))
    except ApprovalError as error:
        raise SystemExit(f"refusing to submit: {error}")
    if backend_name not in approval["backends"]:
        raise SystemExit(f"backend {backend_name} is not named in the approval")
    from qiskit_ibm_runtime import QiskitRuntimeService, SamplerV2

    backend = QiskitRuntimeService(name=account).backend(backend_name, use_fractional_gates=True)
    target = backend.target
    if "rzz" not in target.operation_names:
        raise SystemExit("backend has no rzz with use_fractional_gates=True")
    results = REPO / "results" / "hw_p3" / label
    private = REPO / "hardware" / "private"
    results.mkdir(parents=True, exist_ok=True)
    private.mkdir(parents=True, exist_ok=True)
    sel = REPO / "results" / "hw_p3" / "matching.json"
    if not sel.exists():
        pairs = select_matching(target)
        sel.write_text(json.dumps({"backend": backend.name, "pairs": pairs, "selected_utc": utc_now(),
                                   "rule": "greedy disjoint rzz pairs by reported error; (53,54) forced; readout <= 0.05",
                                   "rzz_errors": {f"{a}-{b}": (target["rzz"].get((a, b)) or target["rzz"].get((b, a))).error for a, b in pairs}},
                                  indent=2) + "\n", encoding="utf-8", newline="\n")
    pairs = [tuple(p) for p in json.loads(sel.read_text(encoding="utf-8"))["pairs"]]
    used, rate = 0.0, None
    log_path = private / f"P3{label}_jobs.json"
    log = json.loads(log_path.read_text(encoding="utf-8")) if log_path.exists() else []
    for block in PLANS_P3[label]:
        if only and block.name not in only:
            continue
        out = results / f"{block.name}.json"
        if out.exists():
            print(f"skip {block.name}: already recorded")
            continue
        items = build(block, target, pairs)
        shots_total = len(items) * block.shots
        estimate = (rate or 2.8e-4) * shots_total
        if used + estimate > max_seconds:
            print(f"stop before {block.name}: estimated {estimate:.0f}s exceeds remaining cap")
            break
        sampler = SamplerV2(mode=backend)
        sampler.options.dynamical_decoupling.enable = False
        sampler.options.twirling.enable_gates = False
        sampler.options.twirling.enable_measure = False
        records, seconds, ids = [], 0.0, []
        submitted = utc_now()
        for start in range(0, len(items), MAX_PUBS_PER_JOB):
            chunk = items[start:start + MAX_PUBS_PER_JOB]
            job = sampler.run([(c,) for _, c in chunk], shots=block.shots)
            ids.append(job.job_id())
            print(f"submitted {block.name}: {len(chunk)} circuits on {2 * len(pairs)} qubits x {block.shots} shots")
            result = job.result()
            for (meta, circuit), pub in zip(chunk, result):
                bits = getattr(pub.data, circuit.cregs[0].name)
                records.append({"meta": meta, "pair_counts": marginals(bits, len(pairs)),
                                "isa_sha256": circuit_digest(circuit)})
            seconds += usage_seconds(job) or 0.0
        used += seconds
        rate = seconds / shots_total if seconds else rate
        payload = {"schema": "hw-p3-block-v1", "evidence": "[hardware-locked, exploratory pilot HW-P3]",
                   "label": label, "block": block.name, "purpose": block.purpose, "backend": backend.name,
                   "pairs": pairs, "shots": block.shots, "submitted_utc": submitted, "finished_utc": utc_now(),
                   "quantum_seconds": seconds, "approval_commit": approval["commit"], "records": records}
        out.write_text(json.dumps(payload) + "\n", encoding="utf-8", newline="\n")
        log.append({"block": block.name, "job_ids": ids, "quantum_seconds": seconds})
        log_path.write_text(json.dumps(log, indent=2) + "\n", encoding="utf-8", newline="\n")
        print(f"finished {block.name}: {seconds} s; cumulative {used:.1f} of {max_seconds:.0f} s")
        time.sleep(1)


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--label", choices=sorted(PLANS_P3), required=True)
    parser.add_argument("--submit", action="store_true")
    parser.add_argument("--account")
    parser.add_argument("--backend", default="ibm_marrakesh")
    parser.add_argument("--max-qpu-seconds", type=float, default=110.0)
    parser.add_argument("--only", nargs="*")
    args = parser.parse_args(argv)
    if not args.submit:
        print(dry_run(args.label))
        return
    if not args.account:
        raise SystemExit("--account is required with --submit")
    submit(args.label, args.account, args.backend, args.max_qpu_seconds, set(args.only) if args.only else None)


if __name__ == "__main__":
    main(sys.argv[1:])
