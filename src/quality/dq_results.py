from __future__ import annotations

from pathlib import Path

import pandas as pd


RESULT_COLUMNS = [
    "rule_id",
    "status",
    "total_records",
    "affected_records",
    "affected_pct",
    "evaluator",
    "dataset",
]


def validate_results(results: pd.DataFrame) -> None:
    """Validate the structure of a governed DQ result set."""
    missing_columns = [
        column
        for column in RESULT_COLUMNS
        if column not in results.columns
    ]

    if missing_columns:
        raise ValueError(
            f"Missing DQ result columns: {missing_columns}"
        )

    if results["rule_id"].duplicated().any():
        raise ValueError("DQ result rule_id values must be unique.")

    invalid_statuses = set(results["status"]) - {"PASS", "FAIL"}

    if invalid_statuses:
        raise ValueError(
            f"Invalid DQ statuses: {sorted(invalid_statuses)}"
        )

    if results["affected_records"].lt(0).any():
        raise ValueError(
            "affected_records cannot contain negative values."
        )

    if results["total_records"].lt(0).any():
        raise ValueError(
            "total_records cannot contain negative values."
        )


def save_results(
    results: pd.DataFrame,
    output_path: Path,
) -> Path:
    """Validate and persist governed DQ results as CSV."""
    validate_results(results)

    output_path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    results[RESULT_COLUMNS].to_csv(
        output_path,
        index=False,
    )

    return output_path