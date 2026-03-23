from typing import Dict, Any
import polars as pl
import plotly.express as px
from libs.viz_factory.src.registry import register_plot


@register_plot("bar_logic")
def draw_bar(df: pl.DataFrame, config: Dict[str, Any]):
    """
    Standard bar chart factory. 
    Expects 'target_col' and 'height' in config.
    """
    # Convert Polars to Pandas for Plotly Express
    pdf = df.to_pandas()
    # Apply standard plotly params
    fig = px.bar(pdf, x=config.get('target_col'),
                 height=config.get('height', 450))
    return fig
