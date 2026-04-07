from typing import Dict, Any, Union
import polars as pl
import os
from transformer.actions.base import register_action

@register_action("sink_parquet")
def action_sink_parquet(lf: pl.LazyFrame, spec: Dict[str, Any]) -> pl.LazyFrame:
    """
    Tier 1 Persistence Action (ADR-024).
    Sinks the query to disk as a Parquet file for long-term session anchoring.
    Returns a new LazyFrame scanning the written file to enable optimized 
    downstream Tier 2 (View) processing.
    """
    path = spec.get("path")
    if not path:
        raise ValueError("Action 'sink_parquet' requires a 'path' parameter.")

    # Ensure parent directory exists
    os.makedirs(os.path.dirname(os.path.abspath(path)), exist_ok=True)

    # ADR-010: Polars sink_parquet returns None. 
    # We execute it here to materialize the "Anchor".
    print(f"      └── 💾 Materializing Anchor (Tier 1) to: {path}")
    lf.sink_parquet(path)

    # Return a new LazyFrame scanning the materialized file.
    # This allows downstream actions (Tier 2) to benefit from 
    # Predicate Pushdown on the already calculated results.
    return pl.scan_parquet(path)

@register_action("scan_parquet")
def action_scan_parquet(lf: Union[None, pl.LazyFrame], spec: Dict[str, Any]) -> pl.LazyFrame:
    """
    Scanner for existing Parquet anchors. 
    Can be used as a starting action if 'lf' is None.
    """
    path = spec.get("path")
    if not path:
        raise ValueError("Action 'scan_parquet' requires a 'path' parameter.")
    
    if not os.path.exists(path):
        raise FileNotFoundError(f"Parquet anchor not found: {path}")
        
    return pl.scan_parquet(path)
