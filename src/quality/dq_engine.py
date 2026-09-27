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
def evaluate_not_null(
    df,
    rule_id: str,
    column: str,
) -> dict:
    """Evaluate whether a column contains null values."""
    if column not in df.columns:
        raise KeyError(f"Column not found: {column}")

    missing_count = int(df[column].isna().sum())
    total_count = len(df)

    return {
        "rule_id": rule_id,
        "status": "PASS" if missing_count == 0 else "FAIL",
        "total_records": total_count,
        "affected_records": missing_count,
        "affected_pct": (
            (missing_count / total_count) * 100
            if total_count
            else 0.0
        ),
    }

def evaluate_unique(
    df,
    rule_id: str,
    columns: list[str],
) -> dict:
    """Evaluate whether a column or composite key is unique."""
    missing_columns = [
        column for column in columns if column not in df.columns
    ]

    if missing_columns:
        raise KeyError(
            f"Columns not found: {missing_columns}"
        )

    duplicate_mask = df.duplicated(
        subset=columns,
        keep=False,
    )

    affected_records = int(duplicate_mask.sum())
    total_records = len(df)

    return {
        "rule_id": rule_id,
        "status": "PASS" if affected_records == 0 else "FAIL",
        "total_records": total_records,
        "affected_records": affected_records,
        "affected_pct": (
            (affected_records / total_records) * 100
            if total_records
            else 0.0
        ),
    }

def evaluate_range(
    df,
    rule_id: str,
    column: str,
    minimum: float,
    maximum: float,
) -> dict:
    """Evaluate whether values fall within an inclusive numeric range."""
    if column not in df.columns:
        raise KeyError(f"Column not found: {column}")

    invalid_mask = (
        df[column].notna()
        & (
            (df[column] < minimum)
            | (df[column] > maximum)
        )
    )

    affected_records = int(invalid_mask.sum())
    total_records = len(df)

    return {
        "rule_id": rule_id,
        "status": "PASS" if affected_records == 0 else "FAIL",
        "total_records": total_records,
        "affected_records": affected_records,
        "affected_pct": (
            (affected_records / total_records) * 100
            if total_records
            else 0.0
        ),
    }
def evaluate_minimum(
    df,
    rule_id: str,
    column: str,
    minimum: float,
) -> dict:
    """Evaluate whether non-null values meet a minimum threshold."""
    if column not in df.columns:
        raise KeyError(f"Column not found: {column}")

    invalid_mask = (
        df[column].notna()
        & (df[column] < minimum)
    )

    affected_records = int(invalid_mask.sum())
    total_records = len(df)

    return {
        "rule_id": rule_id,
        "status": "PASS" if affected_records == 0 else "FAIL",
        "total_records": total_records,
        "affected_records": affected_records,
        "affected_pct": (
            (affected_records / total_records) * 100
            if total_records
            else 0.0
        ),
    }
def evaluate_reference_integrity(
    child_df,
    parent_df,
    rule_id: str,
    child_column: str,
    parent_column: str,
) -> dict:
    """Evaluate whether child foreign-key values exist in the parent dataset."""
    if child_column not in child_df.columns:
        raise KeyError(f"Child column not found: {child_column}")

    if parent_column not in parent_df.columns:
        raise KeyError(f"Parent column not found: {parent_column}")

    parent_keys = set(parent_df[parent_column].dropna())

    invalid_mask = (
        child_df[child_column].notna()
        & ~child_df[child_column].isin(parent_keys)
    )

    affected_records = int(invalid_mask.sum())
    total_records = len(child_df)

    return {
        "rule_id": rule_id,
        "status": "PASS" if affected_records == 0 else "FAIL",
        "total_records": total_records,
        "affected_records": affected_records,
        "affected_pct": (
            (affected_records / total_records) * 100
            if total_records
            else 0.0
        ),
    }
def evaluate_reference_integrity(
    child_df,
    parent_df,
    rule_id: str,
    child_column: str,
    parent_column: str,
) -> dict:
    """Evaluate whether child foreign-key values exist in the parent dataset."""
    if child_column not in child_df.columns:
        raise KeyError(f"Child column not found: {child_column}")

    if parent_column not in parent_df.columns:
        raise KeyError(f"Parent column not found: {parent_column}")

    parent_keys = set(parent_df[parent_column].dropna())

    invalid_mask = (
        child_df[child_column].notna()
        & ~child_df[child_column].isin(parent_keys)
    )

    affected_records = int(invalid_mask.sum())
    total_records = len(child_df)

    return {
        "rule_id": rule_id,
        "status": "PASS" if affected_records == 0 else "FAIL",
        "total_records": total_records,
        "affected_records": affected_records,
        "affected_pct": (
            (affected_records / total_records) * 100
            if total_records
            else 0.0
        ),
    }
def evaluate_allowed_values(
    df,
    rule_id: str,
    column: str,
    allowed_values: set,
) -> dict:
    """Evaluate whether non-null values belong to an allowed domain."""
    if column not in df.columns:
        raise KeyError(f"Column not found: {column}")

    invalid_mask = (
        df[column].notna()
        & ~df[column].isin(allowed_values)
    )

    affected_records = int(invalid_mask.sum())
    total_records = len(df)

    return {
        "rule_id": rule_id,
        "status": "PASS" if affected_records == 0 else "FAIL",
        "total_records": total_records,
        "affected_records": affected_records,
        "affected_pct": (
            (affected_records / total_records) * 100
            if total_records
            else 0.0
        ),
    }