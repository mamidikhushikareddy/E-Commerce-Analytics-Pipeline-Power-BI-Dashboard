from pathlib import Path

from src.quality.dq_results import save_results
from src.quality.dq_runner import run_dq


PROJECT_ROOT = Path(__file__).resolve().parents[1]

RAW_DIR = PROJECT_ROOT / "data" / "raw"
EXECUTION_CONFIG = PROJECT_ROOT / "configs" / "dq_execution.yaml"
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

    save_results(
        results,
        OUTPUT_PATH,
    )

    print(f"Rules executed: {len(results)}")
    print(f"PASS: {(results['status'] == 'PASS').sum()}")
    print(f"FAIL: {(results['status'] == 'FAIL').sum()}")
    print(f"Results written to: {OUTPUT_PATH}")


if __name__ == "__main__":
    main()