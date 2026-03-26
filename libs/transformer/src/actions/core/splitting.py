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
    # ADR-013 / ADR-001: Prioritize the resolved 'columns' list from DataWrangler
    columns = spec.get("columns", [])
    source = columns[0] if columns else spec.get(
        "source", spec.get("target_column"))

    new_columns = spec.get("new_columns", [])
    delimiter = spec.get("delimiter", spec.get("separator", " "))
    drop_source = spec.get("drop_source", False)

    if not source or not new_columns or source not in lf.columns:
        return lf

    # Implementation: Use split to get a list, then extract columns.
    # The last column gets the 'remainder' (all remaining parts joined back)
    # to match typical 'split(sep, n)' behavior and satisfy the test case.

    n = len(new_columns)
    lf = lf.with_columns(
        pl.col(source).str.split(delimiter).alias("_split_list")
    )

    new_cols_exprs = []
    for i in range(n):
        col_name = new_columns[i]
        if i < n - 1:
            # Standard parts
            expr = pl.col("_split_list").list.get(i).alias(col_name)
        else:
            # Remainder part: slice from i to the end and join back
            # We only join if there's actually a remainder; otherwise null if list was too short
            expr = (
                pl.when(pl.col("_split_list").list.len() > i)
                .then(pl.col("_split_list").list.slice(i).list.join(delimiter))
                .otherwise(None)
                .alias(col_name)
            )
        new_cols_exprs.append(expr)

    lf = lf.with_columns(new_cols_exprs).drop("_split_list")

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
