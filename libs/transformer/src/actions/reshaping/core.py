import polars as pl
from typing import Dict, Any, List, Union
from transformer.actions.base import register_action


@register_action("unpivot")
def action_unpivot(lf: pl.LazyFrame, spec: Dict[str, Any]) -> pl.LazyFrame:
    """
    Unpivots (melts) a LazyFrame from wide to long format.
    Spec: { index: ["col1"], on: ["val1", "val2"], variable_name: "var", value_name: "val" }
    """
    index = spec.get("index", [])
    on = spec.get("on", [])
    variable_name = spec.get("variable_name", "variable")
    value_name = spec.get("value_name", "value")

    return lf.unpivot(on=on, index=index, variable_name=variable_name, value_name=value_name)


@register_action("explode")
def action_explode(lf: pl.LazyFrame, spec: Dict[str, Any]) -> pl.LazyFrame:
    """
    Explodes list-like columns into multiple rows.
    Spec: { columns: ["col1"] }
    """
    columns = spec.get("columns", [])
    if not columns:
        return lf
    return lf.explode(columns)


@register_action("unnest")
def action_unnest(lf: pl.LazyFrame, spec: Dict[str, Any]) -> pl.LazyFrame:
    """
    Unnests struct columns into multiple columns.
    Spec: { columns: ["col1"] }
    """
    columns = spec.get("columns", [])
    if not columns:
        return lf
    return lf.unnest(columns)


@register_action("split_to_list")
def action_split_to_list(lf: pl.LazyFrame, spec: Dict[str, Any]) -> pl.LazyFrame:
    """
    Splits a string column into a List column.
    Spec: { columns: ["col1"], separator: "," }
    """
    columns = spec.get("columns", [])
    separator = spec.get("separator", ",")
    if not columns:
        return lf
    return lf.with_columns(pl.col(columns).str.split(separator))


@register_action("to_struct")
def action_to_struct(lf: pl.LazyFrame, spec: Dict[str, Any]) -> pl.LazyFrame:
    """
    Combines multiple columns into a struct.
    Spec: { columns: ["col1", "col2"], target_column: "my_struct" }
    """
    columns = spec.get("columns", [])
    target = spec.get("target_column")
    if not columns or not target:
        return lf
    return lf.with_columns(pl.struct(columns).alias(target)).drop(columns)


@register_action("pivot")
def action_pivot(lf: pl.LazyFrame, spec: Dict[str, Any]) -> pl.LazyFrame:
    """
    Pivots a LazyFrame from long to wide format (Materializes!).
    Spec: { index: ["col1"], on: "variable", values: "value", aggregate_function: "first" }
    NOTE: Pivot is NOT lazy in Polars. This will call .collect().
    """
    index = spec.get("index")
    on = spec.get("on")
    values = spec.get("values")
    aggregate_function = spec.get("aggregate_function", "first")

    # Pivot is not lazy, so we must collect.
    # To keep it semi-consistent with the pipeline, we return a new LazyFrame from the result.
    df = lf.collect().pivot(
        values=values,
        index=index,
        on=on,
        aggregate_function=aggregate_function
    )
    return df.lazy()
