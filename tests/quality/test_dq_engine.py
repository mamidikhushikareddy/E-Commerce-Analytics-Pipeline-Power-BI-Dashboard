from pathlib import Path

import pytest

from src.quality.dq_engine import load_rules, evaluate_not_null

import pandas as pd


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