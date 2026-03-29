from typing import Dict, Any
from plotnine import geom_point, geom_line, geom_boxplot, geom_histogram, ggplot
from viz_factory.registry import register_plot_component


@register_plot_component("geom_boxplot")
def handle_boxplot(p: ggplot, spec: Dict[str, Any]) -> ggplot:
    """Standard Boxplot component wrapper."""
    # Plotnine doesn't allow 'pipe' like Polars,
    # but we can return plot_object + component.
    return p + geom_boxplot(**spec)


@register_plot_component("geom_point")
def handle_point(p: ggplot, spec: Dict[str, Any]) -> ggplot:
    """Standard Point (Scatter) component wrapper."""
    return p + geom_point(**spec)


@register_plot_component("geom_line")
def handle_line(p: ggplot, spec: Dict[str, Any]) -> ggplot:
    """Standard Line (Connected points) component wrapper."""
    return p + geom_line(**spec)


@register_plot_component("geom_histogram")
def handle_histogram(p: ggplot, spec: Dict[str, Any]) -> ggplot:
    """Standard Histogram component wrapper."""
    return p + geom_histogram(**spec)
