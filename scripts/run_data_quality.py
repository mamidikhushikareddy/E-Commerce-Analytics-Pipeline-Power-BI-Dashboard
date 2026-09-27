from pathlib import Path

from src.quality.dq_results import (
    enrich_results_with_rule_metadata,
    save_results,
)
from src.quality.dq_runner import run_dq


PROJECT_ROOT = Path(__file__).resolve().parents[1]

RAW_DIR = PROJECT_ROOT / "data" / "raw"
EXECUTION_CONFIG = PROJECT_ROOT / "configs" / "dq_execution.yaml"
RULES_CONFIG = PROJECT_ROOT / "configs" / "dq_rules.yaml"
OUTPUT_PATH = (
    PROJECT_ROOT
    / "outputs"
    / "data_quality"
    / "dq_results.csv"
)


def main() -> None:
    results = run_dq(
        raw_dir=RAW_DIR,
        execution_config_path=EXECUTION_CONFIG,
    )

    governed_results = enrich_results_with_rule_metadata(
        results,
        RULES_CONFIG,
    )

    save_results(
        governed_results,
        OUTPUT_PATH,
    )

    print(f"Rules executed: {len(governed_results)}")
    print(
        f"PASS: {(governed_results['status'] == 'PASS').sum()}"
    )
    print(
        f"FAIL: {(governed_results['status'] == 'FAIL').sum()}"
    )
    print(
        "Critical failures: "
        f"{((governed_results['status'] == 'FAIL') & (governed_results['severity'] == 'critical')).sum()}"
    )
    print(f"Results written to: {OUTPUT_PATH}")


if __name__ == "__main__":
    main()