"""Qiskit adapter for the semantic probe manifests (optional dependency).

Everything here is SDK glue: it must reproduce `src/circuits.py` exactly.
`verify_isa_probe` is the check that the transpiler did not merge, fold or
reroute any RZZ. Importing this module does not contact any service.
"""

from __future__ import annotations

from copy import deepcopy
from dataclasses import dataclass
from math import isclose, pi

from .circuits import semantic_operations
from .types import CircuitKind, ProbeKey


def _qiskit():
    try:
        import qiskit  # noqa: F401
    except ImportError as error:  # pragma: no cover - environment dependent
        raise RuntimeError("qiskit>=2.1 is required for the hardware adapter") from error
    from qiskit import QuantumCircuit, transpile
    from qiskit.circuit import Parameter
    from qiskit.circuit.library import RZZGate
    from qiskit.transpiler import InstructionProperties

    return QuantumCircuit, transpile, Parameter, RZZGate, InstructionProperties


RZZ_BOUNDS = (0.0, pi / 2)


def fractional_target(base_target, error_source: str = "cz"):
    """Copy a target and add a bounded parametric RZZ on every `error_source` edge.

    Used only for fake-backend dry runs. Durations and errors are copied from
    the CZ entries and are placeholders, not measured RZZ properties
    [fake-backend].
    """
    _, _, Parameter, RZZGate, InstructionProperties = _qiskit()
    target = deepcopy(base_target)
    if "rzz" in target.operation_names:
        return target
    properties = {}
    for qargs, props in base_target[error_source].items():
        properties[qargs] = InstructionProperties(
            duration=None if props is None else props.duration,
            error=None if props is None else props.error,
        )
    target.add_instruction(RZZGate(Parameter("theta")), properties, angle_bounds=[RZZ_BOUNDS])
    return target


def rzz_duration_seconds(target, pair: tuple[int, int]) -> float:
    for qargs in (pair, pair[::-1]):
        props = target["rzz"].get(qargs)
        if props is not None and props.duration is not None:
            return float(props.duration)
    raise ValueError(f"target reports no rzz duration on pair {pair}")


def build_probe_circuit(key: ProbeKey, rzz_seconds: float):
    """Logical 2-qubit circuit for one probe; clbit 0 = target, clbit 1 = control."""
    QuantumCircuit, *_ = _qiskit()
    circuit = QuantumCircuit(2, 2, name=f"probe_{key.circuit_kind.value}")
    for op in semantic_operations(key):
        if op.name == "x":
            circuit.x(op.qubits[0])
        elif op.name == "sx":
            circuit.sx(op.qubits[0])
        elif op.name == "rz":
            circuit.rz(op.angle, op.qubits[0])
        elif op.name == "rzz":
            circuit.rzz(op.angle, *op.qubits)
        elif op.name == "barrier":
            circuit.barrier(*op.qubits)
        elif op.name == "delay_like_rzz":
            duration = key.k * rzz_seconds
            if duration > 0:
                circuit.delay(duration, 0, unit="s")
                circuit.delay(duration, 1, unit="s")
        elif op.name == "measure":
            target_qubit, control_qubit = op.qubits
            circuit.measure(target_qubit, 0)
            circuit.measure(control_qubit, 1)
        else:  # pragma: no cover - manifest and adapter must stay in sync
            raise ValueError(f"unknown semantic operation {op.name}")
    return circuit


@dataclass(frozen=True, slots=True)
class IsaReport:
    ok: bool
    rzz_count: int
    rzz_angles_ok: bool
    physical_qubits: tuple[int, ...]
    forbidden_ops: tuple[str, ...]
    detail: str


ALLOWED_ISA_OPS = {"rz", "sx", "x", "rzz", "barrier", "measure", "delay"}


def verify_isa_probe(isa_circuit, key: ProbeKey, pair: tuple[int, int]) -> IsaReport:
    used = set()
    rzz_count = 0
    angles_ok = True
    forbidden = []
    for instruction in isa_circuit.data:
        name = instruction.operation.name
        qubits = tuple(isa_circuit.find_bit(q).index for q in instruction.qubits)
        used.update(qubits)
        if name not in ALLOWED_ISA_OPS:
            forbidden.append(name)
        if name == "rzz":
            rzz_count += 1
            angle = float(instruction.operation.params[0])
            if not isclose(angle, key.theta, rel_tol=0.0, abs_tol=1e-12):
                angles_ok = False
            if set(qubits) != set(pair):
                forbidden.append("rzz-off-pair")
    expected = key.k if key.circuit_kind in (CircuitKind.PROBE, CircuitKind.ANCHOR) else 0
    ok = (
        rzz_count == expected
        and angles_ok
        and not forbidden
        and used <= set(pair)
    )
    detail = f"rzz={rzz_count}/{expected}, angles_ok={angles_ok}, used={sorted(used)}, forbidden={forbidden}"
    return IsaReport(ok, rzz_count, angles_ok, tuple(sorted(used)), tuple(forbidden), detail)


def to_isa(circuit, target, physical: tuple[int, ...], seed: int = 20261127):
    _, transpile, *_ = _qiskit()
    return transpile(
        circuit,
        target=target,
        initial_layout=list(physical),
        optimization_level=0,
        seed_transpiler=seed,
    )
