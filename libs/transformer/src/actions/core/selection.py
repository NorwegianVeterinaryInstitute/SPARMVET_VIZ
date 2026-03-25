import polars as pl
from typing import List, Dict, Any
from ..base import action


@action(name="keep_columns", category="core")
def action_keep_columns(lf: pl.LazyFrame, columns: List[str], rule: Dict[str, Any]) -> pl.LazyFrame:
    """
    Selects only the specified columns, ensuring that primary keys defined in the schema
    are always preserved to prevent join breakage.
    """
    # 1. Verification: Ensure all requested columns exist
    existing_cols = lf.columns
    missing = [c for c in columns if c not in existing_cols]
    if missing:
        raise ValueError(
            f"Action 'keep_columns' failed: The following columns were not found in the dataset: {missing}. "
            f"Ensure you are using the sanitized column names (snake_case)."
        )

    # 2. Safety: Resolve primary keys from rule metadata
    pks = rule.get("__metadata__", {}).get("primary_keys", [])

    # Merge requested columns with primary keys, preserving order of request
    final_selection = list(dict.fromkeys(columns + pks))

    return lf.select(final_selection)
