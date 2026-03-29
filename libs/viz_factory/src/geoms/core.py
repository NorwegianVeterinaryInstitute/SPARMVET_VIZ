from typing import Dict, Any
from plotnine import geom_point, geom_line, geom_bar, geom_col, geom_boxplot, geom_violin, geom_histogram, ggplot
from viz_factory.registry import register_plot_component


@register_plot_component("geom_boxplot")
def handle_boxplot(p: ggplot, spec: Dict[str, Any]) -> ggplot:
    """Standard Boxplot component wrapper."""
    return p + geom_boxplot(**spec)


@register_plot_component("geom_violin")
def handle_violin(p: ggplot, spec: Dict[str, Any]) -> ggplot:
    """Standard Violin (Density) component wrapper."""
    return p + geom_violin(**spec)


@register_plot_component("geom_point")
def handle_point(p: ggplot, spec: Dict[str, Any]) -> ggplot:
    """Standard Point (Scatter) component wrapper."""
    return p + geom_point(**spec)


@register_plot_component("geom_line")
def handle_line(p: ggplot, spec: Dict[str, Any]) -> ggplot:
    """Standard Line (Connected points) component wrapper."""
    return p + geom_line(**spec)


@register_plot_component("geom_bar")
def handle_bar(p: ggplot, spec: Dict[str, Any]) -> ggplot:
    """Standard Bar (count) component wrapper."""
    return p + geom_bar(**spec)


@register_plot_component("geom_col")
def handle_col(p: ggplot, spec: Dict[str, Any]) -> ggplot:
    """Standard Column (identity) component wrapper."""
    return p + geom_col(**spec)


@register_plot_component("geom_histogram")
def handle_histogram(p: ggplot, spec: Dict[str, Any]) -> ggplot:
    """Standard Histogram component wrapper."""
    return p + geom_histogram(**spec)
