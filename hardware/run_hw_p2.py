"""Runner for the exploratory hardware pilot HW-P2.

Dry run (default): no network. Uses a fake Heron target with a bounded
fractional RZZ, transpiles and verifies every circuit, and writes receipts to
hardware/dry_run/.

Submission (--submit): run by the owner on the owner's own machine with a
saved IBM Quantum account (QiskitRuntimeService(name=...)). This module never
reads, prints or stores a token. Submission requires the approval record in
docs/decisions/HW-P2-approval.json to name an ancestor commit and this exact
script hash; see hardware/approval.py.

Usage (PowerShell, from the repository root):
  python -m hardware.run_hw_p2 --label A                       # dry run
  python -m hardware.run_hw_p2 --label A --submit --account <saved-name> \
      --backend ibm_marrakesh --max-qpu-seconds 420
  python -m hardware.run_hw_p2 --label B --submit --account <saved-name-2> \
      --backend ibm_marrakesh --max-qpu-seconds 420     # reads A's chain
"""

from __future__ import annotations

import argparse
from dataclasses import asdict
from datetime import datetime, timezone
from hashlib import sha256
import io
import json
from math import pi
from pathlib import Path
import random
import sys
import time

from analysis.tolerance.instances import GeneratedDecision
from hardware.approval import ApprovalError, verify_pilot_approval
from hardware.hw_p2_design import PLANS, SEED, Block
from src.qiskit_adapter import (
    build_probe_circuit,
    fractional_target,
    rzz_duration_seconds,
    to_isa,
    verify_isa_probe,
)

REPO = Path(__file__).resolve().parents[1]
MAX_PUBS_PER_JOB = 290  # backend configuration reports max_experiments = 300
APPROVAL = REPO / "docs" / "decisions" / "HW-P2-approval.json"
FAMILY = REPO / "analysis" / "tolerance" / "instances_development.json"


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def select_chain(target) -> tuple[int, int, int]:
    """Deterministic chain rule: minimise summed 2q error plus readout error."""
    rzz = target["rzz"]
    edges = {tuple(sorted(q)) for q in rzz.keys()}
    measure = target["measure"]

    def err(props):
        return float("inf") if props is None or props.error is None else float(props.error)

    def readout(q):
        return err(measure.get((q,)))

    def edge_error(a, b):
        return min(err(rzz.get((a, b))), err(rzz.get((b, a))))

    neighbours: dict[int, set[int]] = {}
    for a, b in edges:
        neighbours.setdefault(a, set()).add(b)
        neighbours.setdefault(b, set()).add(a)
    best = None
    for middle, adjacent in neighbours.items():
        for left in adjacent:
            for right in adjacent:
                if left >= right:
                    continue
                score = (
                    edge_error(left, middle)
                    + edge_error(middle, right)
                    + readout(left)
                    + readout(middle)
                    + readout(right)
                )
                candidate = (score, (left, middle, right))
                if best is None or candidate < best:
                    best = candidate
    if best is None or best[0] == float("inf"):
        raise RuntimeError("no 3-qubit chain with reported rzz and readout errors")
    return best[1]


def readout_circuits(qubits: int):
    from qiskit import QuantumCircuit

    circuits = []
    for state in range(2**qubits):
        circuit = QuantumCircuit(qubits, qubits, name=f"readout_{state:0{qubits}b}")
        for bit in range(qubits):
            if (state >> bit) & 1:
                circuit.x(bit)
        circuit.measure(range(qubits), range(qubits))
        circuits.append(({"type": "readout", "prepared": state, "qubits": qubits}, circuit))
    return circuits


def qaoa_circuit(record: dict, which: str, native: bool):
    from qiskit import QuantumCircuit

    values = dict(record)
    values["edges"] = tuple(tuple(edge) for edge in values["edges"])
    decision = GeneratedDecision(**values)
    instance, first, second = decision.objects()
    candidate = first if which == "first" else second
    n = instance.qubits
    circuit = QuantumCircuit(n, n, name=f"qaoa_{decision.instance_id}_{which}_{'native' if native else 'cz'}")
    circuit.h(range(n))
    for (left, right), theta in zip(instance.edges, candidate.rzz_angles):
        if native:
            circuit.rzz(theta, left, right)
        else:
            circuit.cx(left, right)
            circuit.rz(theta, right)
            circuit.cx(left, right)
    circuit.rx(2.0 * candidate.beta, range(n))
    circuit.measure(range(n), range(n))
    meta = {
        "type": "decision",
        "instance_id": decision.instance_id,
        "candidate": which,
        "implementation": "native-rzz" if native else "cz-decomposed",
        "beta": candidate.beta,
        "theta": candidate.rzz_angles[0],
        "margin": decision.margin,
        "ideal_gap": decision.ideal_gap,
    }
    return meta, circuit


def build_block(block: Block, target, chain: tuple[int, int, int]):
    """Return [(metadata, isa_circuit)] in prespecified randomized order."""
    family = {r["instance_id"]: r for r in json.loads(FAMILY.read_text(encoding="utf-8"))["instances"]}
    items = []
    if block.kind == "probe":
        pair = (chain[0], chain[1]) if block.pair == "A" else (chain[1], chain[2])
        seconds = rzz_duration_seconds(target, pair)
        for key in block.keys:
            isa = to_isa(build_probe_circuit(key, seconds), target, pair)
            report = verify_isa_probe(isa, key, pair)
            if not report.ok:
                raise RuntimeError(f"ISA verification failed for {key}: {report.detail}")
            meta = {"type": "probe", "pair": list(pair), **{**asdict(key), "circuit_kind": key.circuit_kind.value}}
            items.append((meta, isa))
        for meta, circuit in readout_circuits(2):
            items.append(({**meta, "pair": list(pair)}, to_isa(circuit, target, pair)))
    else:
        record = family[block.pair]
        physical = chain[: record["qubits"]]
        for which in ("first", "second"):
            for native in (True, False):
                meta, circuit = qaoa_circuit(record, which, native)
                isa = to_isa(circuit, target, physical)
                names = {inst.operation.name for inst in isa.data}
                if native and "rzz" not in names:
                    raise RuntimeError("native decision circuit lost its rzz gates")
                if not native and "rzz" in names:
                    raise RuntimeError("cz-decomposed decision circuit contains rzz")
                items.append(({**meta, "qubits": list(physical)}, isa))
    order = list(range(len(items)))
    random.Random(SEED + sum(map(ord, block.name))).shuffle(order)
    return [items[i] for i in order]


def circuit_digest(circuit) -> str:
    from qiskit import qpy

    buffer = io.BytesIO()
    qpy.dump(circuit, buffer)
    return sha256(buffer.getvalue()).hexdigest()


def dry_run(label: str) -> Path:
    from qiskit_ibm_runtime.fake_provider import FakeMarrakesh

    target = fractional_target(FakeMarrakesh().target)
    chain = select_chain(target)
    out_dir = REPO / "hardware" / "dry_run" / label
    out_dir.mkdir(parents=True, exist_ok=True)
    summary = {"label": label, "backend": "fake_marrakesh+fractional[fake-backend]", "chain": chain,
               "created_utc": utc_now(), "blocks": []}
    for block in PLANS[label]:
        items = build_block(block, target, chain)
        summary["blocks"].append({
            "block": block.name, "circuits": len(items), "shots": block.shots,
            "digests_sha256": sha256("".join(circuit_digest(c) for _, c in items).encode()).hexdigest(),
        })
    path = out_dir / "dry_run_summary.json"
    path.write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8", newline="\n")
    return path


def usage_seconds(job) -> float | None:
    for getter in (lambda: job.usage(), lambda: job.metrics()["usage"]["quantum_seconds"]):
        try:
            value = getter()
            if value is not None:
                return float(value)
        except Exception:  # noqa: BLE001 - runtime versions differ
            continue
    return None


def submit(label: str, account: str, backend_name: str, max_seconds: float, only: set[str] | None) -> None:
    try:
        approval = verify_pilot_approval(REPO, APPROVAL, Path(__file__))
    except ApprovalError as error:
        raise SystemExit(f"refusing to submit: {error}")
    if backend_name not in approval["backends"]:
        raise SystemExit(f"backend {backend_name} is not named in the approval")

    from qiskit_ibm_runtime import QiskitRuntimeService, SamplerV2

    service = QiskitRuntimeService(name=account)
    backend = service.backend(backend_name, use_fractional_gates=True)
    target = backend.target
    if "rzz" not in target.operation_names:
        raise SystemExit("G0 FAIL: backend target has no rzz with use_fractional_gates=True")

    results = REPO / "results" / "hw_p2" / label
    private = REPO / "hardware" / "private"
    results.mkdir(parents=True, exist_ok=True)
    private.mkdir(parents=True, exist_ok=True)
    selection_path = REPO / "results" / "hw_p2" / "A" / "selection.json"
    if label == "A" and not selection_path.exists():
        chain = select_chain(target)
        selection = {"backend": backend.name, "chain": chain, "selected_utc": utc_now(),
                     "rule": "min sum of rzz error on both edges + readout error on 3 qubits",
                     "edge_errors": {f"{a}-{b}": target["rzz"].get((a, b)).error if target["rzz"].get((a, b)) else None
                                     for a, b in ((chain[0], chain[1]), (chain[1], chain[0]), (chain[1], chain[2]), (chain[2], chain[1]))},
                     "readout_errors": {str(q): target["measure"][(q,)].error for q in chain},
                     "rzz_duration_s": {"A": rzz_duration_seconds(target, (chain[0], chain[1])),
                                        "B": rzz_duration_seconds(target, (chain[1], chain[2]))}}
        selection_path.write_text(json.dumps(selection, indent=2) + "\n", encoding="utf-8", newline="\n")
    if not selection_path.exists():
        raise SystemExit("account B needs results/hw_p2/A/selection.json from account A first")
    chain = tuple(json.loads(selection_path.read_text(encoding="utf-8"))["chain"])

    used = 0.0
    seconds_per_shot = None
    jobs_log = private / f"{label}_jobs.json"
    log = json.loads(jobs_log.read_text(encoding="utf-8")) if jobs_log.exists() else []
    for block in PLANS[label]:
        if only and block.name not in only:
            continue
        out = results / f"{block.name}.json"
        if out.exists():
            print(f"skip {block.name}: already recorded")
            continue
        items = build_block(block, target, chain)
        shots_total = len(items) * block.shots
        if seconds_per_shot is not None and used + seconds_per_shot * shots_total > max_seconds:
            print(f"stop before {block.name}: estimated {seconds_per_shot * shots_total:.0f}s exceeds remaining cap")
            break
        sampler = SamplerV2(mode=backend)
        sampler.options.dynamical_decoupling.enable = False
        sampler.options.twirling.enable_gates = False
        sampler.options.twirling.enable_measure = False
        submitted = utc_now()
        records = []
        seconds_total = 0.0
        seconds_known = True
        job_ids = []
        for start in range(0, len(items), MAX_PUBS_PER_JOB):
            chunk = items[start:start + MAX_PUBS_PER_JOB]
            job = sampler.run([(circuit,) for _, circuit in chunk], shots=block.shots)
            job_ids.append(job.job_id())
            print(f"submitted {block.name} chunk {start // MAX_PUBS_PER_JOB}: {len(chunk)} circuits x {block.shots} shots")
            result = job.result()
            for (meta, circuit), pub in zip(chunk, result):
                counts = getattr(pub.data, circuit.cregs[0].name).get_counts()
                records.append({"meta": meta, "counts": counts, "isa_sha256": circuit_digest(circuit)})
            chunk_seconds = usage_seconds(job)
            if chunk_seconds is None:
                seconds_known = False
            else:
                seconds_total += chunk_seconds
        finished = utc_now()
        seconds = seconds_total if seconds_known else None
        if seconds is not None:
            used += seconds
            seconds_per_shot = seconds / shots_total
        payload = {"schema": "hw-p2-block-v1", "evidence": "[hardware-locked, exploratory pilot HW-P2]",
                   "label": label, "block": block.name, "purpose": block.purpose, "backend": backend.name,
                   "chain": chain, "shots": block.shots, "submitted_utc": submitted, "finished_utc": finished,
                   "quantum_seconds": seconds, "approval_commit": approval["commit"], "records": records}
        out.write_text(json.dumps(payload, indent=1) + "\n", encoding="utf-8", newline="\n")
        log.append({"block": block.name, "job_ids": job_ids, "quantum_seconds": seconds, "finished_utc": finished})
        jobs_log.write_text(json.dumps(log, indent=2) + "\n", encoding="utf-8", newline="\n")
        print(f"finished {block.name}: {seconds} s; cumulative {used:.1f} s of {max_seconds:.0f} s")
        time.sleep(1)


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--label", choices=sorted(PLANS), required=True)
    parser.add_argument("--submit", action="store_true")
    parser.add_argument("--account", help="name of a saved QiskitRuntimeService account")
    parser.add_argument("--backend", default="ibm_marrakesh")
    parser.add_argument("--max-qpu-seconds", type=float, default=420.0)
    parser.add_argument("--only", nargs="*", help="run only these block names")
    args = parser.parse_args(argv)
    if not args.submit:
        print(dry_run(args.label))
        return
    if not args.account:
        raise SystemExit("--account is required with --submit")
    submit(args.label, args.account, args.backend, args.max_qpu_seconds, set(args.only) if args.only else None)


if __name__ == "__main__":
    main(sys.argv[1:])
