"""Development-only Monte Carlo calibration for the G2.5 diagnostics."""

from dataclasses import asdict, dataclass
import json
from math import exp, sqrt
from pathlib import Path
import random

from analysis.simulation.ademp import wilson_interval
from src.diagnostics import (
    DiagnosticStatus,
    allocate_diagnostic_alpha,
    combine_diagnostics,
    log_linear_visibility_diagnostic,
    phase_linearity_diagnostic,
    z_conservation_diagnostic,
)
from src.estimate import BinomialCount, LinearInterval, four_phase_joint_confidence
from src.model import phase_cycle_signals


@dataclass(frozen=True, slots=True)
class DiagnosticScenario:
    name: str
    flip_rate: float
    phase_slope: float
    phase_curvature: float
    visibility_decay: float
    visibility_curvature: float


@dataclass(frozen=True, slots=True)
class CalibrationDesign:
    # Development values selected by a prespecified grid search. They are not
    # a hardware budget or a G3 recommendation.
    shots_per_phase: int = 16000
    z_shots: int = 32000
    alpha_diag: float = 0.05
    allowed_flip_rate: float = 0.02
    readout_scale: float = 0.94
    readout_offset: float = -0.03
    ks: tuple[int, ...] = (1, 2, 4, 8)


@dataclass(frozen=True, slots=True)
class CalibrationSummary:
    scenario: dict[str, object]
    trials: int
    seed: int
    any_trigger_rate: float
    any_trigger_wilson95: tuple[float, float]
    inconclusive_rate: float
    z_trigger_rate: float
    phase_trigger_rate: float
    visibility_trigger_rate: float


def _draw_binomial(generator: random.Random, shots: int, probability: float) -> int:
    if hasattr(generator, "binomialvariate"):
        return generator.binomialvariate(shots, probability)
    return sum(generator.random() < probability for _ in range(shots))


def _phase_counts(
    generator: random.Random,
    design: CalibrationDesign,
    phase: float,
    amplitude_visibility: float,
) -> tuple[BinomialCount, BinomialCount, BinomialCount, BinomialCount]:
    signals = phase_cycle_signals(
        phase,
        visibility=amplitude_visibility,
        readout_scale=design.readout_scale,
        readout_offset=design.readout_offset,
    )
    return tuple(
        BinomialCount(
            _draw_binomial(generator, design.shots_per_phase, (signal + 1.0) / 2.0),
            design.shots_per_phase,
        )
        for signal in signals
    )  # type: ignore[return-value]


def run_calibration(
    scenario: DiagnosticScenario,
    design: CalibrationDesign,
    trials: int,
    seed: int,
) -> CalibrationSummary:
    if trials <= 0:
        raise ValueError("trials must be positive")
    if design.shots_per_phase <= 0 or design.z_shots <= 0:
        raise ValueError("shot counts must be positive")
    if not design.ks or any(k <= 0 for k in design.ks) or len(set(design.ks)) != len(design.ks):
        raise ValueError("ks must be unique positive integers")
    if not 0.0 <= scenario.flip_rate <= 1.0:
        raise ValueError("flip_rate must lie in [0, 1]")

    allocation = allocate_diagnostic_alpha(design.alpha_diag)
    # The joint phase/amplitude set for every k is valid on the same event.
    alpha_cycle = min(allocation.phase_linearity, allocation.visibility_linearity) / len(
        design.ks
    )
    generator = random.Random(seed)
    any_trigger = inconclusive = z_trigger = phase_trigger = visibility_trigger = 0

    for _ in range(trials):
        flips = _draw_binomial(generator, design.z_shots, scenario.flip_rate)
        z_result = z_conservation_diagnostic(
            flips, design.z_shots, design.allowed_flip_rate, allocation.z_conservation
        )
        phase_observations = []
        visibility_observations = []
        for k in design.ks:
            phase = k * scenario.phase_slope + scenario.phase_curvature * k * k
            visibility = exp(
                -scenario.visibility_decay * k - scenario.visibility_curvature * k * k
            )
            estimate = four_phase_joint_confidence(
                _phase_counts(generator, design, phase, visibility), alpha_cycle
            )
            phase_observations.append((k, estimate.phase.confidence_interval))
            visibility_observations.append((k, estimate.amplitude_interval))

        phase_result = phase_linearity_diagnostic(
            tuple(phase_observations), LinearInterval(-3.141592653589793, 3.141592653589793)
        )
        visibility_result = log_linear_visibility_diagnostic(tuple(visibility_observations))
        results = (z_result, phase_result, visibility_result)
        model_status = combine_diagnostics(results)
        triggered = model_status.value == "model-inadequate"
        any_trigger += triggered
        inconclusive += model_status.value == "diagnostic-inconclusive"
        z_trigger += z_result.status is DiagnosticStatus.TRIGGERED
        phase_trigger += phase_result.status is DiagnosticStatus.TRIGGERED
        visibility_trigger += visibility_result.status is DiagnosticStatus.TRIGGERED

    return CalibrationSummary(
        scenario=asdict(scenario),
        trials=trials,
        seed=seed,
        any_trigger_rate=any_trigger / trials,
        any_trigger_wilson95=wilson_interval(any_trigger, trials),
        inconclusive_rate=inconclusive / trials,
        z_trigger_rate=z_trigger / trials,
        phase_trigger_rate=phase_trigger / trials,
        visibility_trigger_rate=visibility_trigger / trials,
    )


def development_scenarios() -> tuple[DiagnosticScenario, ...]:
    return (
        DiagnosticScenario("m0-null", 0.01, 0.12, 0.0, 0.015, 0.0),
        DiagnosticScenario("z-boundary-null", 0.02, 0.12, 0.0, 0.015, 0.0),
        DiagnosticScenario("z-alternative-0.03", 0.03, 0.12, 0.0, 0.015, 0.0),
        DiagnosticScenario("z-alternative-0.05", 0.05, 0.12, 0.0, 0.015, 0.0),
        DiagnosticScenario("z-alternative", 0.08, 0.12, 0.0, 0.015, 0.0),
        DiagnosticScenario("phase-curvature-0.005", 0.01, 0.12, 0.005, 0.015, 0.0),
        DiagnosticScenario("phase-curvature-0.015", 0.01, 0.12, 0.015, 0.015, 0.0),
        DiagnosticScenario("phase-curvature", 0.01, 0.12, 0.03, 0.015, 0.0),
        DiagnosticScenario("visibility-curvature-0.005", 0.01, 0.12, 0.0, 0.015, 0.005),
        DiagnosticScenario("visibility-curvature-0.010", 0.01, 0.12, 0.0, 0.015, 0.01),
        DiagnosticScenario("visibility-curvature", 0.01, 0.12, 0.0, 0.015, 0.02),
    )


def write_calibration(
    path: Path,
    design: CalibrationDesign,
    summaries: tuple[CalibrationSummary, ...],
) -> None:
    payload = {
        "label": "development simulation; not a G2.5 gate",
        "design": asdict(design),
        "summaries": [asdict(x) for x in summaries],
    }
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def main() -> None:
    design = CalibrationDesign()
    summaries = tuple(
        run_calibration(scenario, design, trials=2000, seed=2026112700 + index)
        for index, scenario in enumerate(development_scenarios())
    )
    write_calibration(Path(__file__).with_name("development_calibration.json"), design, summaries)


if __name__ == "__main__":
    main()
