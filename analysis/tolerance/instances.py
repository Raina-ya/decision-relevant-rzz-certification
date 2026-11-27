"""Prespecified development generator for tier-A decision instances."""

from dataclasses import asdict, dataclass
import json
from math import pi
from pathlib import Path
import random

from src.decision import Candidate, MaxCutInstance, decision_gap


@dataclass(frozen=True, slots=True)
class GeneratedDecision:
    instance_id: str
    qubits: int
    edges: tuple[tuple[int, int], ...]
    first_beta: float
    first_theta: float
    second_beta: float
    second_theta: float
    ideal_gap: float
    margin: float
    attempts: int
    evidence: str = "[exact]"

    def objects(self) -> tuple[MaxCutInstance, Candidate, Candidate]:
        instance = MaxCutInstance(self.qubits, self.edges)
        first = Candidate(self.first_beta, (self.first_theta,) * len(self.edges))
        second = Candidate(self.second_beta, (self.second_theta,) * len(self.edges))
        return instance, first, second


def _path_instance(qubits: int) -> MaxCutInstance:
    return MaxCutInstance(qubits, tuple((index, index + 1) for index in range(qubits - 1)))


def generate_decision_family(
    seed: int,
    min_ideal_gap: float = 0.15,
    margin_fraction: float = 0.5,
    max_attempts: int = 10_000,
) -> tuple[GeneratedDecision, ...]:
    """Generate 2-4 qubit path instances with exactly two decision angles."""
    if min_ideal_gap <= 0.0:
        raise ValueError("min_ideal_gap must be positive")
    if not 0.0 < margin_fraction < 1.0:
        raise ValueError("margin_fraction must lie in (0, 1)")
    generator = random.Random(seed)
    decisions = []
    for qubits in (2, 3, 4):
        instance = _path_instance(qubits)
        for attempt in range(1, max_attempts + 1):
            first_beta = generator.uniform(-pi / 4, pi / 4)
            second_beta = generator.uniform(-pi / 4, pi / 4)
            first_theta = generator.uniform(pi / 16, pi / 2)
            second_theta = generator.uniform(pi / 16, pi / 2)
            first = Candidate(first_beta, (first_theta,) * len(instance.edges))
            second = Candidate(second_beta, (second_theta,) * len(instance.edges))
            gap = decision_gap(instance, first, second)
            if abs(gap) < min_ideal_gap:
                continue
            decisions.append(
                GeneratedDecision(
                    instance_id=f"path-{qubits}q",
                    qubits=qubits,
                    edges=instance.edges,
                    first_beta=first_beta,
                    first_theta=first_theta,
                    second_beta=second_beta,
                    second_theta=second_theta,
                    ideal_gap=gap,
                    margin=margin_fraction * abs(gap),
                    attempts=attempt,
                )
            )
            break
        else:
            raise RuntimeError(f"no qualifying {qubits}-qubit instance within max_attempts")
    return tuple(decisions)


def write_family(path: Path, family: tuple[GeneratedDecision, ...], seed: int) -> None:
    payload = {
        "schema": "rzz-decision-family-development-v1",
        "status": "unlocked-development",
        "seed": seed,
        "instances": [asdict(decision) for decision in family],
    }
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")

