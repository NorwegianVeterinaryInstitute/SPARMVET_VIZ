import polars as pl
from typing import Dict, Any
from libs.transformer.src.actions.base import register_action


@register_action("split_column")
def action_split_column(lf: pl.LazyFrame, spec: Dict[str, Any]) -> pl.LazyFrame:
    """
    Split a string column into multiple new columns based on a delimiter.

    Usage in YAML:
      - action: "split_column"
        source: "some_col"
        new_columns: ["col_1", "col_2"]
        delimiter: ": "
        drop_source: true
    """
    source = spec.get("source", spec.get("target_column"))
    new_columns = spec.get("new_columns", [])
    delimiter = spec.get("delimiter", spec.get("separator", " "))
    drop_source = spec.get("drop_source", False)

    if not source or not new_columns or source not in lf.columns:
        return lf

    # Implementation: Use split_exact to generate a struct, rename the fields, alias it, and unnest
    # n=len(new_columns)-1 ensures we split into exactly the number of columns requested
    lf = lf.with_columns(
        pl.col(source).str.split_exact(delimiter, n=len(new_columns)-1)
        .struct.rename_fields(new_columns)
        .alias("_split_struct")
    ).unnest("_split_struct")

    if drop_source:
        lf = lf.drop(source)

    return lf


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(
        description="Manual execution hook for testing.")
    parser.add_argument("--test", action="store_true", help="Run in test mode")
    args = parser.parse_args()
    if args.test:
        print(f"Executing {__file__} in test mode.")
