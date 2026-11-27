"""Offline-only preflight and receipt generation."""

from dataclasses import asdict, dataclass
from datetime import datetime, timezone
import importlib.util
import json
from pathlib import Path
import platform
import subprocess

from src.circuits import circuit_hash, semantic_operations
from src.types import ProbeKey


@dataclass(frozen=True, slots=True)
class CapabilityReceipt:
    schema: str
    created_utc: str
    git_commit: str | None
    python_version: str
    qiskit_available: bool
    qiskit_ibm_runtime_available: bool
    network_queried: bool
    hardware_job_submitted: bool


@dataclass(frozen=True, slots=True)
class CircuitReceipt:
    circuit_hash: str
    theta: float
    k: int
    control: int
    role: int
    analysis_phase: float
    circuit_kind: str
    rzz_count: int
    operation_count: int


def current_commit(repo: Path) -> str | None:
    completed = subprocess.run(
        ["git", "rev-parse", "HEAD"],
        cwd=repo,
        check=False,
        capture_output=True,
        text=True,
    )
    return completed.stdout.strip() if completed.returncode == 0 else None


def offline_capability_receipt(repo: Path) -> CapabilityReceipt:
    """Inspect only the local environment; never instantiate an IBM service."""
    return CapabilityReceipt(
        schema="rzz-capability-receipt-v1",
        created_utc=datetime.now(timezone.utc).isoformat(),
        git_commit=current_commit(repo),
        python_version=platform.python_version(),
        qiskit_available=importlib.util.find_spec("qiskit") is not None,
        qiskit_ibm_runtime_available=importlib.util.find_spec("qiskit_ibm_runtime") is not None,
        network_queried=False,
        hardware_job_submitted=False,
    )


def circuit_receipt(key: ProbeKey) -> CircuitReceipt:
    operations = semantic_operations(key)
    return CircuitReceipt(
        circuit_hash=circuit_hash(key),
        theta=key.theta,
        k=key.k,
        control=key.control,
        role=key.role,
        analysis_phase=key.analysis_phase,
        circuit_kind=key.circuit_kind.value,
        rzz_count=sum(operation.name == "rzz" for operation in operations),
        operation_count=len(operations),
    )


def write_dry_run_receipt(path: Path, repo: Path, keys: tuple[ProbeKey, ...]) -> None:
    payload = {
        "capability": asdict(offline_capability_receipt(repo)),
        "circuits": [asdict(circuit_receipt(key)) for key in keys],
    }
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")

