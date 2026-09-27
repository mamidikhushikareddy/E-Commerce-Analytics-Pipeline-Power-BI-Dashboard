from pathlib import Path

import pytest

import pandas as pd

from src.quality.dq_engine import (
    evaluate_not_null,
    evaluate_unique,
    load_rules,
    evaluate_range,
)


PROJECT_ROOT = Path(__file__).resolve().parents[2]
RULES_PATH = PROJECT_ROOT / "configs" / "dq_rules.yaml"


def test_load_rules_returns_all_governed_rules():
    rules = load_rules(RULES_PATH)

    assert len(rules) == 33


def test_rule_ids_are_unique():
    rules = load_rules(RULES_PATH)
    rule_ids = [rule["rule_id"] for rule in rules]

    assert len(rule_ids) == len(set(rule_ids))


def test_all_rules_have_required_fields():
    rules = load_rules(RULES_PATH)
    required_fields = {
        "rule_id",
        "domain",
        "name",
        "severity",
        "description",
    }

    for rule in rules:
        assert required_fields.issubset(rule)


def test_missing_rule_registry_raises_error(tmp_path):
    missing_path = tmp_path / "missing.yaml"

    with pytest.raises(FileNotFoundError):
        load_rules(missing_path)

def test_evaluate_not_null_passes_complete_column():
    df = pd.DataFrame({"value": [1, 2, 3]})

    result = evaluate_not_null(
        df,
        rule_id="TEST-001",
        column="value",
    )

    assert result["status"] == "PASS"
    assert result["affected_records"] == 0
    assert result["affected_pct"] == 0.0


def test_evaluate_not_null_fails_incomplete_column():
    df = pd.DataFrame({"value": [1, None, 3]})

    result = evaluate_not_null(
        df,
        rule_id="TEST-002",
        column="value",
    )

    assert result["status"] == "FAIL"
    assert result["affected_records"] == 1
    assert result["affected_pct"] > 0

def test_evaluate_not_null_raises_for_missing_column():
    df = pd.DataFrame({"value": [1, 2, 3]})

    with pytest.raises(KeyError):
        evaluate_not_null(
            df,
            rule_id="TEST-003",
            column="missing_column",
        )

def test_evaluate_unique_passes_unique_column():
    df = pd.DataFrame({"id": [1, 2, 3]})

    result = evaluate_unique(
        df,
        rule_id="TEST-004",
        columns=["id"],
    )

    assert result["status"] == "PASS"
    assert result["affected_records"] == 0


def test_evaluate_unique_fails_duplicate_column():
    df = pd.DataFrame({"id": [1, 2, 2, 3]})

    result = evaluate_unique(
        df,
        rule_id="TEST-005",
        columns=["id"],
    )

    assert result["status"] == "FAIL"
    assert result["affected_records"] == 2
    assert result["affected_pct"] == 50.0


def test_evaluate_unique_supports_composite_key():
    df = pd.DataFrame(
        {
            "order_id": ["A", "A", "B"],
            "item_id": [1, 2, 1],
        }
    )

    result = evaluate_unique(
        df,
        rule_id="TEST-006",
        columns=["order_id", "item_id"],
    )

    assert result["status"] == "PASS"
def test_evaluate_unique_passes_unique_column():
    df = pd.DataFrame({"id": [1, 2, 3]})

    result = evaluate_unique(
        df,
        rule_id="TEST-004",
        columns=["id"],
    )

    assert result["status"] == "PASS"
    assert result["affected_records"] == 0


def test_evaluate_unique_fails_duplicate_column():
    df = pd.DataFrame({"id": [1, 2, 2, 3]})

    result = evaluate_unique(
        df,
        rule_id="TEST-005",
        columns=["id"],
    )

    assert result["status"] == "FAIL"
    assert result["affected_records"] == 2
    assert result["affected_pct"] == 50.0


def test_evaluate_unique_supports_composite_key():
    df = pd.DataFrame(
        {
            "order_id": ["A", "A", "B"],
            "item_id": [1, 2, 1],
        }
    )

    result = evaluate_unique(
        df,
        rule_id="TEST-006",
        columns=["order_id", "item_id"],
    )

    assert result["status"] == "PASS"


def test_evaluate_unique_raises_for_missing_column():
    df = pd.DataFrame({"id": [1, 2, 3]})

    with pytest.raises(KeyError):
        evaluate_unique(
            df,
            rule_id="TEST-007",
            columns=["missing_column"],
        )
def test_evaluate_range_passes_valid_values():
    df = pd.DataFrame({"score": [1, 3, 5]})

    result = evaluate_range(
        df,
        rule_id="TEST-008",
        column="score",
        minimum=1,
        maximum=5,
    )

    assert result["status"] == "PASS"
    assert result["affected_records"] == 0


def test_evaluate_range_fails_out_of_range_values():
    df = pd.DataFrame({"score": [1, 3, 5, 0, 6]})

    result = evaluate_range(
        df,
        rule_id="TEST-009",
        column="score",
        minimum=1,
        maximum=5,
    )

    assert result["status"] == "FAIL"
    assert result["affected_records"] == 2


def test_evaluate_range_ignores_null_values():
    df = pd.DataFrame({"score": [1, None, 5]})

    result = evaluate_range(
        df,
        rule_id="TEST-010",
        column="score",
        minimum=1,
        maximum=5,
    )

    assert result["status"] == "PASS"
    assert result["affected_records"] == 0


def test_evaluate_range_raises_for_missing_column():
    df = pd.DataFrame({"score": [1, 2, 3]})

    with pytest.raises(KeyError):
        evaluate_range(
            df,
            rule_id="TEST-011",
            column="missing_column",
            minimum=1,
            maximum=5,
        )