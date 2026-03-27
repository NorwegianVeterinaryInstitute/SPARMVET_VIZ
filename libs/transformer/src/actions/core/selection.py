import polars as pl
from typing import List, Dict, Any
from transformer.actions.base import register_action
from typing import List, Dict, Any, Union


@register_action("keep_columns")
def action_keep_columns(lf: pl.LazyFrame, spec: Dict[str, Any]) -> pl.LazyFrame:
    """
    Selects only the specified columns, ensuring that primary keys defined in the schema
    are always preserved to prevent join breakage.
    """
    columns = spec.get("columns", [])
    # 1. Verification: Use Lazy execution pattern for schema checks
    schema = lf.collect_schema()
    existing_cols = schema.names()
    missing = [c for c in columns if c not in existing_cols]
    if missing:
        raise ValueError(
            f"Action 'keep_columns' failed: The following columns were not found in the dataset: {missing}. "
            f"Ensure you are using the sanitized column names (snake_case)."
        )

    # 2. Safety: Resolve primary keys from rule metadata
    pks = spec.get("__metadata__", {}).get("primary_keys", [])

    # Merge requested columns with primary keys, ensuring PKs come first
    final_selection = list(dict.fromkeys(pks + columns))

    return lf.select(final_selection)


@register_action("drop_columns")
def action_drop_columns(lf: pl.LazyFrame, spec: Dict[str, Any]) -> pl.LazyFrame:
    """
    Drops the specified columns, but prevents dropping primary keys.
    """
    requested_drops = spec.get("columns", [])
    if isinstance(requested_drops, str):
        requested_drops = [requested_drops]

    # Safety: Fetch PKs
    pks = spec.get("__metadata__", {}).get("primary_keys", [])

    # Filter out PKs from dropping
    safe_drops = [c for c in requested_drops if c not in pks]

    if len(safe_drops) < len(requested_drops):
        print(
            f"Warning: Primary keys {set(requested_drops) & set(pks)} were protected from dropping.")

    # Only drop if they exist
    existing_cols = lf.collect_schema().names()
    final_drops = [c for c in safe_drops if c in existing_cols]

    if not final_drops:
        return lf

    return lf.drop(final_drops)
