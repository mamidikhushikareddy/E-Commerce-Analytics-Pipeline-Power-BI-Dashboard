from pathlib import Path
import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[2]
RAW_DIR = PROJECT_ROOT / "data" / "raw"
MANIFEST_PATH = PROJECT_ROOT / "outputs" / "raw_data_manifest.csv"


def test_raw_dataset_has_expected_file_count():
    files = list(RAW_DIR.glob("*.csv"))
    assert len(files) == 9


def test_raw_manifest_exists():
    assert MANIFEST_PATH.exists()


def test_raw_manifest_has_unique_files():
    df = pd.read_csv(MANIFEST_PATH)
    assert df["file_name"].is_unique
    assert df["file_name"].notna().all()


def test_raw_manifest_has_no_missing_values():
    df = pd.read_csv(MANIFEST_PATH)
    assert df.notna().all().all()
