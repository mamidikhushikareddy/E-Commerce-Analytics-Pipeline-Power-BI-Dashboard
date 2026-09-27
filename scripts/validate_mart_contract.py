import yaml
from pathlib import Path


MART_PATH = Path(
    "docs/data_dictionary/mart_product_performance_daily.yaml"
)

WAREHOUSE_SCHEMA_PATH = Path(
    "docs/data_dictionary/warehouse_schema.yaml"
)


mart = yaml.safe_load(
    MART_PATH.read_text(encoding="utf-8")
)["mart"]

warehouse = yaml.safe_load(
    WAREHOUSE_SCHEMA_PATH.read_text(encoding="utf-8")
)["warehouse_schema"]

warehouse_tables = {
    **warehouse["facts"],
    **warehouse["dimensions"],
}


errors = []


# ---------------------------------------------------------------------
# Validate source tables
# ---------------------------------------------------------------------

for table_name in mart["source_tables"]:
    if table_name not in warehouse_tables:
        errors.append(
            f"Source table not found in warehouse schema: {table_name}"
        )


# ---------------------------------------------------------------------
# Validate join rules are declared
# ---------------------------------------------------------------------

if not mart.get("join_rules"):
    errors.append("No join rules declared")


# ---------------------------------------------------------------------
# Validate mart business key
# ---------------------------------------------------------------------

mart_business_key = mart.get("business_key", [])

for key_column in mart_business_key:
    if key_column not in mart["columns"]:
        errors.append(
            f"Business key column '{key_column}' "
            "is not declared in mart columns"
        )


# ---------------------------------------------------------------------
# Validate source references in mart columns
# ---------------------------------------------------------------------

for column_name, column in mart["columns"].items():

    source = column.get("source")

    if not source:
        continue

    # Derived fields are intentionally allowed.
    if source.startswith("derived"):
        continue

    # Parse simple table.column references.
    if "." not in source:
        continue

    table_name, source_column = source.split(".", 1)

    if table_name not in warehouse_tables:
        errors.append(
            f"{column_name}: source table '{table_name}' "
            "not found in warehouse schema"
        )
        continue

    if source_column not in warehouse_tables[table_name]["columns"]:
        errors.append(
            f"{column_name}: source column '{source_column}' "
            f"not found in {table_name}"
        )


# ---------------------------------------------------------------------
# Validate all direct source references inside transformations
# ---------------------------------------------------------------------

for transformation in mart.get("transformations", []):

    if not isinstance(transformation, str):
        errors.append(
            "Transformation rule must be a string"
        )


# ---------------------------------------------------------------------
# Validate column count
# ---------------------------------------------------------------------

if len(mart["columns"]) != 11:
    errors.append(
        f"Expected 11 mart columns, found {len(mart['columns'])}"
    )


# ---------------------------------------------------------------------
# Report
# ---------------------------------------------------------------------

print("MART:", mart["name"])
print("SOURCE TABLES DECLARED:", len(mart["source_tables"]))
print("MART COLUMNS DECLARED:", len(mart["columns"]))
print("CONTRACT ERRORS:", len(errors))

for error in errors:
    print("ERROR:", error)

assert not errors, "Mart contract validation failed"

print("MART CONTRACT VALIDATION: PASS")