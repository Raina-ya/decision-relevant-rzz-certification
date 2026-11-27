"""Run the fixed development-only ADEMP scenario."""

from pathlib import Path

from analysis.simulation.ademp import AdempScenario, run_ademp, write_summary
from src.decision import Candidate, MaxCutInstance


def main() -> None:
    scenario = AdempScenario(
        epsilon=0.02,
        a=-0.01,
        b=0.015,
        detuning_1=0.005,
        detuning_2=-0.004,
        visibility=0.9,
        readout_scale=0.94,
        readout_offset=-0.03,
        shots_per_phase=500,
        alpha_total=0.05,
        margin=0.05,
    )
    summary = run_ademp(
        scenario,
        MaxCutInstance(2, ((0, 1),)),
        Candidate(0.3, (0.4,)),
        Candidate(-0.2, (0.7,)),
        trials=2000,
        seed=20261127,
    )
    output = Path(__file__).with_name("development_result.json")
    write_summary(output, summary)


if __name__ == "__main__":
    main()
