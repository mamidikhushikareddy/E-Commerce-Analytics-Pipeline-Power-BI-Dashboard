from __future__ import annotations

from pathlib import Path

import pandas as pd
import yaml

from src.quality.dq_engine import (
    evaluate_allowed_values,
    evaluate_minimum,
    evaluate_not_null,
    evaluate_range,
    evaluate_reconciliation,
    evaluate_reference_integrity,
    evaluate_temporal_order,
    evaluate_unique,
)
from src.quality.dq_preparation import (
    build_order_item_temporal_frame,
    build_order_reconciliation_frame,
)


SUPPORTED_EVALUATORS = {
    "allowed_values",
    "minimum",
    "not_null",
    "range",
    "reconciliation",
    "reference_integrity",
    "temporal_order",
    "unique",
}


def load_execution_config(config_path: Path) -> dict:
    """Load and validate the DQ execution configuration."""
    if not config_path.exists():
        raise FileNotFoundError(
            f"Execution configuration not found: {config_path}"
        )

    if config_path.suffix.lower() not in {".yaml", ".yml"}:
        raise ValueError(
            f"Expected a YAML configuration file: {config_path}"
        )

    with config_path.open("r", encoding="utf-8") as file:
        config = yaml.safe_load(file)

    if not isinstance(config, dict):
        raise ValueError("Execution configuration must be a mapping.")

    required_sections = {"version", "datasets", "rules"}

    missing_sections = required_sections - set(config)
    if missing_sections:
        raise ValueError(
            f"Missing configuration sections: {sorted(missing_sections)}"
        )

    if not isinstance(config["datasets"], dict):
        raise ValueError("'datasets' must be a mapping.")

    if not isinstance(config["rules"], dict):
        raise ValueError("'rules' must be a mapping.")

    for rule_id, rule in config["rules"].items():
        if not isinstance(rule, dict):
            raise ValueError(
                f"Execution definition for {rule_id} must be a mapping."
            )

        if "evaluator" not in rule:
            raise ValueError(
                f"Execution definition for {rule_id} "
                "is missing 'evaluator'."
            )

        evaluator = rule["evaluator"]

        if evaluator not in SUPPORTED_EVALUATORS:
            raise ValueError(
                f"Unsupported evaluator '{evaluator}' "
                f"for rule {rule_id}."
            )

    return config


def load_datasets(
    raw_dir: Path,
    dataset_config: dict,
) -> dict[str, pd.DataFrame]:
    """Load all source datasets declared by the execution configuration."""
    datasets: dict[str, pd.DataFrame] = {}

    for dataset_name, dataset_definition in dataset_config.items():
        if not isinstance(dataset_definition, dict):
            raise ValueError(
                f"Dataset definition for {dataset_name} must be a mapping."
            )

        if "file" not in dataset_definition:
            raise ValueError(
                f"Dataset definition for {dataset_name} "
                "is missing 'file'."
            )

        file_path = raw_dir / dataset_definition["file"]

        if not file_path.exists():
            raise FileNotFoundError(
                f"Raw dataset not found: {file_path}"
            )

        datasets[dataset_name] = pd.read_csv(file_path)

    return datasets


def prepare_derived_datasets(
    datasets: dict[str, pd.DataFrame],
) -> dict[str, pd.DataFrame]:
    """Build explicitly declared derived datasets required by DQ rules."""
    derived = {}

    derived["order_item_temporal"] = build_order_item_temporal_frame(
        datasets["orders"],
        datasets["order_items"],
    )

    derived["order_reconciliation"] = build_order_reconciliation_frame(
        datasets["order_items"],
        datasets["payments"],
    )

    return derived


def execute_rule(
    rule_id: str,
    rule: dict,
    datasets: dict[str, pd.DataFrame],
) -> dict:
    """Execute one configured DQ rule."""
    evaluator = rule["evaluator"]

    if evaluator == "not_null":
        return evaluate_not_null(
            datasets[rule["dataset"]],
            rule_id,
            rule["column"],
        )

    if evaluator == "unique":
        return evaluate_unique(
            datasets[rule["dataset"]],
            rule_id,
            rule["columns"],
        )

    if evaluator == "range":
        return evaluate_range(
            datasets[rule["dataset"]],
            rule_id,
            rule["column"],
            rule["minimum"],
            rule["maximum"],
        )

    if evaluator == "minimum":
        return evaluate_minimum(
            datasets[rule["dataset"]],
            rule_id,
            rule["column"],
            rule["minimum"],
        )

    if evaluator == "reference_integrity":
        return evaluate_reference_integrity(
            datasets[rule["child_dataset"]],
            datasets[rule["parent_dataset"]],
            rule_id,
            rule["child_column"],
            rule["parent_column"],
        )

    if evaluator == "temporal_order":
        return evaluate_temporal_order(
            datasets[rule["dataset"]],
            rule_id,
            rule["earlier_column"],
            rule["later_column"],
        )

    if evaluator == "reconciliation":
        return evaluate_reconciliation(
            datasets[rule["dataset"]],
            rule_id,
            rule["expected_column"],
            rule["actual_column"],
            rule["tolerance"],
        )

    if evaluator == "allowed_values":
        return evaluate_allowed_values(
            datasets[rule["dataset"]],
            rule_id,
            rule["column"],
            set(rule["allowed_values"]),
        )

    raise ValueError(
        f"Unsupported evaluator '{evaluator}' for rule {rule_id}."
    )


def run_dq(
    raw_dir: Path,
    execution_config_path: Path,
) -> pd.DataFrame:
    """Execute the governed DQ rule set and return structured results."""
    config = load_execution_config(execution_config_path)

    datasets = load_datasets(
        raw_dir,
        config["datasets"],
    )

    derived_datasets = prepare_derived_datasets(datasets)

    all_datasets = {
        **datasets,
        **derived_datasets,
    }

    results = []

    for rule_id, rule in config["rules"].items():
        result = execute_rule(
            rule_id,
            rule,
            all_datasets,
        )

        result["evaluator"] = rule["evaluator"]
        result["dataset"] = rule.get(
            "dataset",
            rule.get("child_dataset", ""),
        )

        results.append(result)

    return pd.DataFrame(results)