"""The Data Import test files (assets/test_uploads/) behave as their README says.

Uses the same column check the Data Import panel runs (MetadataValidator against the
manifest's input_fields), and checks that the files are exactly what the generating script
produces, so the set cannot drift away from the data.

Run: PYTHONPATH=. ./.venv/bin/python -m pytest app/tests/test_import_test_files.py -q
"""
import importlib.util
from pathlib import Path

import polars as pl
import pytest

from ingestion.ingestor import DataIngestor
from transformer.metadata_validator import MetadataValidator
from utils.config_loader import ConfigManager

ROOT = Path(__file__).resolve().parents[2]
UPLOADS = ROOT / "assets" / "test_uploads"
MANIFEST = ROOT / "config" / "manifests" / "pipelines" / "1_test_data_ST22_dummy.yaml"

ACCEPTED = [
    ("FastP", "FastP_valid_changed.tsv"),
    ("Bracken", "Bracken_valid_changed.tsv"),
    ("FastP", "FastP_ok_extra_column.tsv"),
    ("FastP", "FastP_gap_text_in_numeric_column.tsv"),   # known gap: the column check passes
]
REJECTED = [
    "FastP_error_missing_column.tsv",
    "FastP_error_misspelled_header.tsv",
    "FastP_error_wrong_delimiter.tsv",
    "FastP_error_no_header.tsv",
]


@pytest.fixture(scope="module")
def schemas():
    return ConfigManager(str(MANIFEST)).raw_config["data_schemas"]


def _column_check_accepts(path: Path, schema: dict) -> bool:
    try:
        MetadataValidator().validate(pl.scan_csv(path, separator="\t"), schema["input_fields"], context="[test]")
        return True
    except Exception:
        return False


@pytest.mark.parametrize("dataset,name", ACCEPTED)
def test_these_files_pass_the_column_check(schemas, dataset, name):
    assert _column_check_accepts(UPLOADS / name, schemas[dataset])


@pytest.mark.parametrize("name", REJECTED)
def test_these_files_fail_the_column_check(schemas, name):
    assert not _column_check_accepts(UPLOADS / name, schemas["FastP"])


def test_the_valid_files_keep_the_sample_ids_and_change_only_the_named_column():
    original = pl.read_csv(ROOT / "assets/test_data/1_test_data_ST22_dummy/test_data_FastP_20260307_105756.tsv", separator="\t")
    changed = pl.read_csv(UPLOADS / "FastP_valid_changed.tsv", separator="\t")
    assert changed["sample_id"].to_list() == original["sample_id"].to_list()
    differing = [c for c in original.columns if original[c].to_list() != changed[c].to_list()]
    assert differing == ["total_reads"]


def test_the_files_are_exactly_what_the_script_generates(tmp_path):
    spec = importlib.util.spec_from_file_location("make_files", ROOT / "assets/scripts/create_import_test_files.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    written = module.build(ROOT / "assets/test_data/1_test_data_ST22_dummy", tmp_path)
    assert sorted(p.name for p in written) == sorted(p.name for p in UPLOADS.glob("*.tsv"))
    for path in written:
        assert path.read_bytes() == (UPLOADS / path.name).read_bytes(), f"{path.name} differs from the committed file"


@pytest.mark.xfail(strict=True, reason="Known gap: Data Import checks column names only, so text in a numeric "
                                       "column is accepted and written, then breaks the data. When fixed, this "
                                       "test starts to pass: remove the marker.")
def test_text_in_a_numeric_column_does_not_break_the_data_after_import(schemas, tmp_path):
    path = UPLOADS / "FastP_gap_text_in_numeric_column.tsv"
    if not _column_check_accepts(path, schemas["FastP"]):
        return  # rejected at import: fine
    schema = {**schemas["FastP"], "source": {"type": "local_tsv", "path": str(path)}}
    lf, _ = DataIngestor(data_dir=str(tmp_path)).ingest("FastP", schema)
    lf.collect()  # raises when the accepted file cannot be read: the gap
