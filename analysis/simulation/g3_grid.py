"""Prospective two-angle development grid for the sign-sensitive instance."""

from dataclasses import asdict, dataclass, replace
import json
from pathlib import Path
import random

from analysis.simulation.ademp import AdempScenario, estimate_m0_box, wilson_interval
from src.certify import Verdict, certify, gamma_interval_per_candidate
from src.decision import Candidate, EdgeError, MaxCutInstance, signed_gap_per_candidate


@dataclass(frozen=True, slots=True)
class TwoAngleSummary:
    epsilon: float
    shots_per_phase: int
    trials: int
    seed: int
    true_gamma: float
    true_class: str
    joint_coverage_rate: float
    joint_coverage_wilson95: tuple[float, float]
    interval_available_rate: float
    harmless_rate: float
    harmless_wilson95: tuple[float, float]
    harmful_rate: float
    harmful_wilson95: tuple[float, float]
    inconclusive_rate: float
    inconclusive_wilson95: tuple[float, float]
    false_harmless_rate: float
    false_harmless_wilson95: tuple[float, float]
    false_harmful_rate: float
    false_harmful_wilson95: tuple[float, float]
    total_probe_circuits: int
    total_probe_shots: int
    qpu_seconds_linear_estimate: float


def _center_radius(box):
    center = EdgeError(
        0.5 * (box.epsilon.lower + box.epsilon.upper),
        0.5 * (box.a.lower + box.a.upper),
        0.5 * (box.b.lower + box.b.upper),
    )
    radius = EdgeError(
        0.5 * (box.epsilon.upper - box.epsilon.lower),
        0.5 * (box.a.upper - box.a.lower),
        0.5 * (box.b.upper - box.b.lower),
    )
    return center, radius


def run_two_angle_grid_point(
    scenario: AdempScenario,
    instance: MaxCutInstance,
    first: Candidate,
    second: Candidate,
    trials: int,
    seed: int,
    seconds_per_shot: float = 0.00028,
) -> TwoAngleSummary:
    """Estimate each candidate angle separately under a joint alpha budget."""
    if len(instance.edges) != 1:
        raise ValueError("this development grid is restricted to one edge")
    if trials <= 0:
        raise ValueError("trials must be positive")
    if seconds_per_shot <= 0.0:
        raise ValueError("seconds_per_shot must be positive")
    per_angle = replace(scenario, alpha_total=scenario.alpha_total / 2.0)
    generator = random.Random(seed)
    truth = (EdgeError(scenario.epsilon, scenario.a, scenario.b),)
    true_gamma = signed_gap_per_candidate(instance, first, second, truth, truth)
    if true_gamma >= scenario.margin:
        true_class = Verdict.HARMLESS.value
    elif true_gamma < 0.0:
        true_class = Verdict.HARMFUL.value
    else:
        true_class = Verdict.INCONCLUSIVE.value

    covered = available = harmless = harmful = inconclusive = 0
    for _ in range(trials):
        first_box = estimate_m0_box(generator, per_angle)
        second_box = estimate_m0_box(generator, per_angle)
        if first_box is None or second_box is None:
            inconclusive += 1
            continue
        available += 1
        first_covered = (
            first_box.epsilon.contains(scenario.epsilon)
            and first_box.a.contains(scenario.a)
            and first_box.b.contains(scenario.b)
        )
        second_covered = (
            second_box.epsilon.contains(scenario.epsilon)
            and second_box.a.contains(scenario.a)
            and second_box.b.contains(scenario.b)
        )
        covered += first_covered and second_covered
        first_center, first_radius = _center_radius(first_box)
        second_center, second_radius = _center_radius(second_box)
        interval = gamma_interval_per_candidate(
            instance,
            first,
            second,
            (first_center,),
            (first_radius,),
            (second_center,),
            (second_radius,),
            1.0 - scenario.alpha_total,
        )
        verdict = certify(interval, scenario.margin)
        harmless += verdict is Verdict.HARMLESS
        harmful += verdict is Verdict.HARMFUL
        inconclusive += verdict is Verdict.INCONCLUSIVE

    circuits = 2 * 6 * len(scenario.ks) * 4
    total_shots = circuits * scenario.shots_per_phase
    false_harmless = harmless if true_gamma < scenario.margin else 0
    false_harmful = harmful if true_gamma >= 0.0 else 0
    return TwoAngleSummary(
        epsilon=scenario.epsilon,
        shots_per_phase=scenario.shots_per_phase,
        trials=trials,
        seed=seed,
        true_gamma=true_gamma,
        true_class=true_class,
        joint_coverage_rate=covered / trials,
        joint_coverage_wilson95=wilson_interval(covered, trials),
        interval_available_rate=available / trials,
        harmless_rate=harmless / trials,
        harmless_wilson95=wilson_interval(harmless, trials),
        harmful_rate=harmful / trials,
        harmful_wilson95=wilson_interval(harmful, trials),
        inconclusive_rate=inconclusive / trials,
        inconclusive_wilson95=wilson_interval(inconclusive, trials),
        false_harmless_rate=false_harmless / trials,
        false_harmless_wilson95=wilson_interval(false_harmless, trials),
        false_harmful_rate=false_harmful / trials,
        false_harmful_wilson95=wilson_interval(false_harmful, trials),
        total_probe_circuits=circuits,
        total_probe_shots=total_shots,
        qpu_seconds_linear_estimate=total_shots * seconds_per_shot,
    )


def _load_instance(path: Path):
    record = json.loads(path.read_text(encoding="utf-8"))["instances"][0]
    instance = MaxCutInstance(record["qubits"], tuple(map(tuple, record["edges"])))
    first = Candidate(record["first_beta"], (record["first_theta"],))
    second = Candidate(record["second_beta"], (record["second_theta"],))
    return record, instance, first, second


def main() -> None:
    root = Path(__file__).resolve().parents[2]
    record, instance, first, second = _load_instance(
        root / "analysis" / "tolerance" / "instances_sign_sensitive.json"
    )
    summaries = []
    index = 0
    for epsilon in (-0.4, -0.2, 0.0, 0.1):
        for shots in (500, 1000, 2000, 4000):
            scenario = AdempScenario(
                epsilon=epsilon,
                a=0.0,
                b=0.0,
                detuning_1=0.0,
                detuning_2=0.0,
                visibility=0.85,
                readout_scale=0.94,
                readout_offset=-0.03,
                shots_per_phase=shots,
                alpha_total=0.05,
                margin=record["margin"],
            )
            summaries.append(
                run_two_angle_grid_point(
                    scenario, instance, first, second, trials=1000, seed=2026112800 + index
                )
            )
            index += 1
    payload = {
        "label": "prospective development simulation; not a G3 gate",
        "instance_id": record["instance_id"],
        "assumptions": {
            "shared_truth_across_angles": True,
            "separate_confidence_boxes_per_angle": True,
            "seconds_per_shot": 0.00028,
            "diagnostic_cost_included": False,
        },
        "summaries": [asdict(summary) for summary in summaries],
    }
    output = Path(__file__).with_name("g3_development_grid.json")
    output.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
