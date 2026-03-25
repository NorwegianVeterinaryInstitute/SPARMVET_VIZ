import polars as pl
from typing import Any
from ...utils.naming import clean_column_header
from libs.transformer.src.actions.base import register_action
from typing import Any, List, Union, Dict


@register_action("sanitize_column_names")
def action_sanitize_column_names(lf: pl.LazyFrame, spec: Dict[str, Any] = None) -> pl.LazyFrame:
    """
    Sanitizes column names into safe snake_case using the project-standard utility.
    Useful for ingesting raw data from external sources that don't match the manifest keys.
    """
    columns = spec.get("columns", [])
    if not columns or columns == "all":
        cols_to_fix = lf.columns
    else:
        cols_to_fix = columns if isinstance(columns, list) else [columns]

    rename_map = {col: clean_column_header(col) for col in cols_to_fix}
    return lf.rename(rename_map)
