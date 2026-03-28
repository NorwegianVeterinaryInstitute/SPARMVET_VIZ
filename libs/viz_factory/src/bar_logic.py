from typing import Dict, Any
import polars as pl
from plotnine import ggplot, aes, geom_bar, theme_minimal, labs
try:
    from registry import register_plot
except ImportError:
    from viz_factory.registry import register_plot


@register_plot("bar_logic")
def draw_bar(df: pl.DataFrame, config: Dict[str, Any]):
    """
    Standard bar chart factory using Plotnine. 
    Expects 'target_col' in config.
    """
    # Convert Polars to Pandas for Plotnine
    pdf = df.to_pandas()
    target_col = config.get('target_col')
    title = config.get('title', f"Bar chart of {target_col}")

    if not target_col or target_col not in pdf.columns:
        raise ValueError(f"target_col '{target_col}' not found in dataframe")

    fig = (
        ggplot(pdf, aes(x=target_col))
        + geom_bar(fill="#2c3e50")
        + theme_minimal()
        + labs(title=title)
    )
    return fig


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(
        description="Manual execution hook for testing.")
    parser.add_argument("--test", action="store_true", help="Run in test mode")
    args = parser.parse_args()
    if args.test:
        print(f"Executing {__file__} in test mode.")
