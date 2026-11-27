"""Canonical semantic circuit manifests.

This module deliberately does not claim to produce Qiskit ISA circuits. It
defines the immutable intent that a future SDK adapter must preserve exactly.
"""

from dataclasses import asdict, dataclass
from hashlib import sha256
import json
from math import pi

from .probes import validate_probe
from .types import CircuitKind, ProbeKey


@dataclass(frozen=True, slots=True)
class Operation:
    name: str
    qubits: tuple[int, ...]
    angle: float | None = None


def semantic_operations(key: ProbeKey) -> tuple[Operation, ...]:
    validate_probe(key)
    target = 0 if key.role == 1 else 1
    control = 1 - target
    operations: list[Operation] = []
    if key.control == 1:
        operations.append(Operation("x", (control,)))
    operations.extend((Operation("sx", (target,)), Operation("rz", (target,), pi / 2)))

    if key.circuit_kind is CircuitKind.PROBE or key.circuit_kind is CircuitKind.ANCHOR:
        for _ in range(key.k):
            operations.extend(
                (Operation("rzz", (0, 1), key.theta), Operation("barrier", (0, 1)))
            )
        reference = -(1 if key.control == 0 else -1) * key.k * key.theta
        operations.append(Operation("rz", (target,), reference))
    elif key.circuit_kind is CircuitKind.DELAY:
        operations.append(Operation("delay_like_rzz", (0, 1), key.k * key.theta))

    operations.extend(
        (
            Operation("rz", (target,), -key.analysis_phase),
            Operation("sx", (target,)),
            Operation("measure", (target, control)),
        )
    )
    return tuple(operations)


def circuit_hash(key: ProbeKey) -> str:
    payload = {
        "schema": "rzz-probe-semantic-v1",
        "key": {**asdict(key), "circuit_kind": key.circuit_kind.value},
        "operations": [asdict(operation) for operation in semantic_operations(key)],
    }
    encoded = json.dumps(payload, sort_keys=True, separators=(",", ":"), allow_nan=False)
    return sha256(encoded.encode("utf-8")).hexdigest()

