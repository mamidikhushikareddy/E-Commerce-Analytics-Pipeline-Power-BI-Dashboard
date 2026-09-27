import pandas as pd
import pytest

from src.quality.dq_results import (
    RESULT_COLUMNS,
    save_results,
    validate_results,
)


def valid_results():
    return pd.DataFrame(
        {
            "rule_id": ["R1", "R2"],
            "status": ["PASS", "FAIL"],
            "total_records": [100, 100],
            "affected_records": [0, 2],
            "affected_pct": [0.0, 2.0],
            "evaluator": ["not_null", "unique"],
            "dataset": ["orders", "orders"],
        }
    )


def test_validate_results_accepts_valid_results():
    results = valid_results()

    validate_results(results)


def test_validate_results_rejects_missing_columns():
    results = valid_results().drop(columns=["status"])

    with pytest.raises(ValueError, match="Missing DQ result columns"):
        validate_results(results)


def test_validate_results_rejects_duplicate_rule_ids():
    results = valid_results()
    results.loc[1, "rule_id"] = "R1"

    with pytest.raises(ValueError, match="rule_id values must be unique"):
        validate_results(results)


def test_validate_results_rejects_invalid_status():
    results = valid_results()
    results.loc[0, "status"] = "UNKNOWN"

    with pytest.raises(ValueError, match="Invalid DQ statuses"):
        validate_results(results)


def test_validate_results_rejects_negative_counts():
    results = valid_results()
    results.loc[0, "affected_records"] = -1

    with pytest.raises(ValueError, match="affected_records"):
        validate_results(results)


def test_save_results(tmp_path):
    results = valid_results()
    output_path = tmp_path / "dq_results.csv"

    returned_path = save_results(
        results,
        output_path,
    )

    assert returned_path == output_path
    assert output_path.exists()

    saved = pd.read_csv(output_path)

    assert list(saved.columns) == RESULT_COLUMNS
    assert len(saved) == 2