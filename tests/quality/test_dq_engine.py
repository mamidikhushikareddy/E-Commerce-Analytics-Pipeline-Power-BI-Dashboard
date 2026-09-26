from pathlib import Path

import pytest

from src.quality.dq_engine import load_rules


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