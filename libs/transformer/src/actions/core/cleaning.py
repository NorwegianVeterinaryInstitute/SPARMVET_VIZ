import polars as pl
from typing import Dict, Any, List, Union
from libs.transformer.src.actions.base import register_action


@register_action("strip_whitespace")
def action_strip_whitespace(lf: pl.LazyFrame, spec: Dict[str, Any]) -> pl.LazyFrame:
    """
    Strips leading and trailing whitespace from string columns.
    If 'columns' is not provided in spec, targets all pl.String columns.
    """
    columns = spec.get("columns", [])

    if not columns:
        # Smart Selection: auto-target String columns
        schema = lf.collect_schema()
        process_cols = [name for name,
                        dtype in schema.items() if dtype == pl.String]
    else:
        process_cols = columns if isinstance(columns, list) else [columns]

    if not process_cols:
        return lf

    return lf.with_columns(pl.col(process_cols).str.strip_chars())


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(
        description="Manual execution hook for testing.")
    parser.add_argument("--test", action="store_true", help="Run in test mode")
    args = parser.parse_args()
    if args.test:
        print(f"Executing {__file__} in test mode.")
