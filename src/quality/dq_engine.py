from pathlib import Path

import yaml


REQUIRED_RULE_FIELDS = {
    "rule_id",
    "domain",
    "name",
    "severity",
    "description",
}

ALLOWED_SEVERITIES = {
    "critical",
    "warning",
    "info",
}


def load_rules(rules_path: Path) -> list[dict]:
    """Load and structurally validate the governed DQ rule registry."""
    if not rules_path.exists():
        raise FileNotFoundError(f"DQ rule registry not found: {rules_path}")

    if rules_path.suffix.lower() not in {".yaml", ".yml"}:
        raise ValueError(f"Expected a YAML rule registry: {rules_path}")

    with rules_path.open("r", encoding="utf-8") as file:
        config = yaml.safe_load(file)

    if not isinstance(config, dict):
        raise ValueError("DQ rule registry must contain a YAML mapping.")

    rules = config.get("rules")

    if not isinstance(rules, list):
        raise ValueError("DQ rule registry must contain a 'rules' list.")

    rule_ids = set()

    for rule in rules:
        if not isinstance(rule, dict):
            raise ValueError("Every DQ rule must be a mapping.")

        missing_fields = REQUIRED_RULE_FIELDS - rule.keys()

        if missing_fields:
            raise ValueError(
                f"Rule is missing required fields: {sorted(missing_fields)}"
            )

        rule_id = rule["rule_id"]

        if rule_id in rule_ids:
            raise ValueError(f"Duplicate rule_id found: {rule_id}")

        rule_ids.add(rule_id)

        if rule["severity"] not in ALLOWED_SEVERITIES:
            raise ValueError(
                f"Invalid severity for {rule_id}: {rule['severity']}"
            )

    return rules


