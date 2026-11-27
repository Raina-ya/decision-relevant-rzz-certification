"""Generate the fixed development decision-family manifest."""

from pathlib import Path

from analysis.tolerance.instances import generate_decision_family, write_family


def main() -> None:
    seed = 20261127
    output = Path(__file__).with_name("instances_development.json")
    write_family(output, generate_decision_family(seed), seed)


if __name__ == "__main__":
    main()

