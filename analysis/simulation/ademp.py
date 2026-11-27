"""End-to-end development simulation for the finite-sample certification chain."""

from dataclasses import asdict, dataclass
import json
from math import sqrt
from pathlib import Path
import random

from src.certify import Verdict, certify, gamma_interval_from_error_box
from src.decision import Candidate, EdgeError, MaxCutInstance, signed_gap
from src.estimate import (
    BinomialCount,
    LinearInterval,
    UnwrapStatus,
    four_phase_confidence,
    recover_m0_intervals,
    unwrap_phase_intervals,
)
from src.model import phase_cycle_signals


@dataclass(frozen=True, slots=True)
class AdempScenario:
    epsilon: float
    a: float
    b: float
    detuning_1: float
    detuning_2: float
    visibility: float
    readout_scale: float
    readout_offset: float
    shots_per_phase: int
    alpha_total: float
    margin: float
    ks: tuple[int, ...] = (1, 2, 4, 8, 16)


@dataclass(frozen=True, slots=True)
class TrialResult:
    m0_covered: bool
    verdict: str
    true_gamma: float
    interval_available: bool


@dataclass(frozen=True, slots=True)
class AdempSummary:
    seed: int
    trials: int
    scenario: dict[str, object]
    true_class: str
    m0_coverage: float
    m0_coverage_mcse: float
    m0_coverage_wilson95: tuple[float, float]
    interval_available_rate: float
    harmless_rate: float
    harmful_rate: float
    inconclusive_rate: float
    false_harmless_rate: float
    false_harmless_wilson95: tuple[float, float]
    false_harmful_rate: float
    false_harmful_wilson95: tuple[float, float]


def _draw_binomial(generator: random.Random, shots: int, probability: float) -> int:
    if hasattr(generator, "binomialvariate"):
        return generator.binomialvariate(shots, probability)
    return sum(generator.random() < probability for _ in range(shots))


def wilson_interval(successes: int, trials: int, z: float = 1.959963984540054) -> tuple[float, float]:
    """Wilson score interval for a binomial proportion."""
    if trials <= 0 or not 0 <= successes <= trials:
        raise ValueError("invalid binomial summary")
    proportion = successes / trials
    denominator = 1.0 + z**2 / trials
    center = (proportion + z**2 / (2.0 * trials)) / denominator
    radius = (
        z
        * sqrt(proportion * (1.0 - proportion) / trials + z**2 / (4.0 * trials**2))
        / denominator
    )
    lower = 0.0 if successes == 0 else max(0.0, center - radius)
    upper = 1.0 if successes == trials else min(1.0, center + radius)
    return lower, upper


def _slope_interval(
    generator: random.Random,
    slope: float,
    scenario: AdempScenario,
    alpha_cycle: float,
) -> LinearInterval | None:
    observations = []
    for k in scenario.ks:
        signals = phase_cycle_signals(
            k * slope,
            visibility=scenario.visibility,
            readout_scale=scenario.readout_scale,
            readout_offset=scenario.readout_offset,
        )
        counts = tuple(
            BinomialCount(
                _draw_binomial(generator, scenario.shots_per_phase, (signal + 1.0) / 2.0),
                scenario.shots_per_phase,
            )
            for signal in signals
        )
        estimate = four_phase_confidence(counts, alpha_cycle)
        observations.append((k, estimate.confidence_interval))
    result = unwrap_phase_intervals(tuple(observations))
    return result.interval if result.status is UnwrapStatus.IDENTIFIED else None


def run_trial(
    generator: random.Random,
    scenario: AdempScenario,
    instance: MaxCutInstance,
    first: Candidate,
    second: Candidate,
) -> TrialResult:
    if scenario.shots_per_phase <= 0:
        raise ValueError("shots_per_phase must be positive")
    if not 0.0 < scenario.alpha_total < 1.0:
        raise ValueError("alpha_total must lie in (0, 1)")
    if not 0.0 < scenario.visibility <= 1.0:
        raise ValueError("visibility must lie in (0, 1]")
    # Six slopes per theta: c=0, c=1, and delay for each Ramsey role.
    alpha_cycle = scenario.alpha_total / (6 * len(scenario.ks))
    slopes = (
        scenario.epsilon + scenario.a + scenario.detuning_1,
        -scenario.epsilon + scenario.a + scenario.detuning_1,
        scenario.detuning_1,
        scenario.epsilon + scenario.b + scenario.detuning_2,
        -scenario.epsilon + scenario.b + scenario.detuning_2,
        scenario.detuning_2,
    )
    intervals = tuple(
        _slope_interval(generator, slope, scenario, alpha_cycle) for slope in slopes
    )
    truth = (EdgeError(scenario.epsilon, scenario.a, scenario.b),)
    true_gamma = signed_gap(instance, first, second, truth)
    if any(interval is None for interval in intervals):
        return TrialResult(False, Verdict.INCONCLUSIVE.value, true_gamma, False)
    try:
        box = recover_m0_intervals(*intervals)  # type: ignore[arg-type]
    except ValueError:
        return TrialResult(False, Verdict.INCONCLUSIVE.value, true_gamma, False)
    covered = (
        box.epsilon.contains(scenario.epsilon)
        and box.a.contains(scenario.a)
        and box.b.contains(scenario.b)
    )
    centers = (
        EdgeError(
            0.5 * (box.epsilon.lower + box.epsilon.upper),
            0.5 * (box.a.lower + box.a.upper),
            0.5 * (box.b.lower + box.b.upper),
        ),
    )
    radii = (
        EdgeError(
            0.5 * (box.epsilon.upper - box.epsilon.lower),
            0.5 * (box.a.upper - box.a.lower),
            0.5 * (box.b.upper - box.b.lower),
        ),
    )
    gamma_interval = gamma_interval_from_error_box(
        instance, first, second, centers, radii, 1.0 - scenario.alpha_total
    )
    verdict = certify(gamma_interval, scenario.margin)
    return TrialResult(covered, verdict.value, true_gamma, True)


def run_ademp(
    scenario: AdempScenario,
    instance: MaxCutInstance,
    first: Candidate,
    second: Candidate,
    trials: int,
    seed: int,
) -> AdempSummary:
    if trials <= 0:
        raise ValueError("trials must be positive")
    generator = random.Random(seed)
    outcomes = [run_trial(generator, scenario, instance, first, second) for _ in range(trials)]
    true_gamma = outcomes[0].true_gamma
    if true_gamma >= scenario.margin:
        true_class = Verdict.HARMLESS.value
    elif true_gamma < 0.0:
        true_class = Verdict.HARMFUL.value
    else:
        true_class = Verdict.INCONCLUSIVE.value

    def count(predicate) -> int:
        return sum(predicate(outcome) for outcome in outcomes)

    coverage_count = count(lambda outcome: outcome.m0_covered)
    available_count = count(lambda outcome: outcome.interval_available)
    harmless_count = count(lambda outcome: outcome.verdict == Verdict.HARMLESS.value)
    harmful_count = count(lambda outcome: outcome.verdict == Verdict.HARMFUL.value)
    inconclusive_count = count(lambda outcome: outcome.verdict == Verdict.INCONCLUSIVE.value)
    coverage = coverage_count / trials
    harmless = harmless_count / trials
    harmful = harmful_count / trials
    inconclusive = inconclusive_count / trials
    false_harmless_count = harmless_count if true_gamma < scenario.margin else 0
    false_harmful_count = harmful_count if true_gamma >= 0.0 else 0
    return AdempSummary(
        seed=seed,
        trials=trials,
        scenario=asdict(scenario),
        true_class=true_class,
        m0_coverage=coverage,
        m0_coverage_mcse=sqrt(coverage * (1.0 - coverage) / trials),
        m0_coverage_wilson95=wilson_interval(coverage_count, trials),
        interval_available_rate=available_count / trials,
        harmless_rate=harmless,
        harmful_rate=harmful,
        inconclusive_rate=inconclusive,
        false_harmless_rate=false_harmless_count / trials,
        false_harmless_wilson95=wilson_interval(false_harmless_count, trials),
        false_harmful_rate=false_harmful_count / trials,
        false_harmful_wilson95=wilson_interval(false_harmful_count, trials),
    )


def write_summary(path: Path, summary: AdempSummary) -> None:
    path.write_text(json.dumps(asdict(summary), indent=2, sort_keys=True) + "\n", encoding="utf-8")
