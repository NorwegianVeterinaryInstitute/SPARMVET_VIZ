import polars as pl
from pathlib import Path
from typing import Dict, Any, Tuple, Optional


class DataIngestor:
    """
    The official Ingestion Engine for the Dashboard.
    Responsible for mapping conceptual datasets defined in the YAML manifest
    to physical files on disk, executing Polars lazy loading, and optionally 
    validating the raw columns against the schema structure.
    """

    def __init__(self, data_dir: str):
        self.data_dir = Path(data_dir)
        if not self.data_dir.exists():
            raise FileNotFoundError(
                f"Data directory not found: {self.data_dir}")

    def find_file(self, dataset_name: str) -> Optional[Path]:
        """
        Attempts to locate the physical TSV file for a given dataset name.
        Uses exact match first, then falls back to prefix/substring globbing.
        """
        exact_match = self.data_dir / f"{dataset_name}.tsv"
        if exact_match.exists():
            return exact_match

        # Fallback to fuzzy mapping
        potential_files = list(self.data_dir.glob(f"*{dataset_name}*.tsv"))
        if potential_files:
            return potential_files[0]

        return None

    def ingest(self, dataset_name: str, dataset_schema: Dict[str, Any]) -> Tuple[pl.LazyFrame, Path]:
        """
        Locates the dataset file and returns a standard Polars LazyFrame.

        Raises:
            FileNotFoundError: If the TSV file cannot be located.
            ValueError: If the file exists but Polars fails to parse it.
        """
        tsv_path = self.find_file(dataset_name)
        if not tsv_path:
            raise FileNotFoundError(
                f"Could not locate a physical .tsv file for dataset '{dataset_name}' in {self.data_dir}")

        try:
            # We enforce TSV format globally
            lf = pl.scan_csv(tsv_path, separator="\t")

            # Standardize Column Names based on the Schema
            # ADR-013: Use 'input_fields' for raw ingestion mapping
            fields_data = dataset_schema.get(
                "input_fields") or dataset_schema.get("fields") or {}
            rename_mapping = {}
            for key, props in fields_data.items():
                original_name = props.get("original_name")
                if original_name and original_name != key:
                    rename_mapping[original_name] = key

            if rename_mapping:
                # We only rename if the column actually exists in the scan
                # This prevents crashes if the TSV is missing a column (handled by validation later)
                available_cols = lf.collect_schema().names()
                safe_mapping = {
                    old: new for old, new in rename_mapping.items() if old in available_cols
                }
                if safe_mapping:
                    lf = lf.rename(safe_mapping)

            return lf, tsv_path
        except Exception as e:
            raise ValueError(
                f"Polars failed to parse or rename {tsv_path.name}. Error: {e}")

    def validate_schema(self, lf: pl.LazyFrame, dataset_schema: Dict[str, Any]) -> bool:
        """
        Validates that the physical loaded LazyFrame contains all the mandatory 
        columns defined in the formal _fields.yaml dictionary.
        ADR-013: Uses 'input_fields' for raw validation.
        """
        fields_data = dataset_schema.get(
            "input_fields") or dataset_schema.get("fields") or {}
        if not fields_data:
            return True  # Nothing to validate against

        # For now, simply confirming we can read the raw columns
        # Strict validation of names/types will occur here.
        raw_columns = lf.columns
        return len(raw_columns) > 0


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(
        description="Manual execution hook for testing.")
    parser.add_argument("--test", action="store_true", help="Run in test mode")
    args = parser.parse_args()
    if args.test:
        print(f"Executing {__file__} in test mode.")
