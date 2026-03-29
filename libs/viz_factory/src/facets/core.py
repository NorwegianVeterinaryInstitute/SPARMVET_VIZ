from typing import Dict, Any
from plotnine import facet_wrap, facet_grid, ggplot
from viz_factory.registry import register_plot_component


@register_plot_component("facet_wrap")
def handle_facet_wrap(p: ggplot, spec: Dict[str, Any]) -> ggplot:
    """Standard individual panel wrapping."""
    # Ensure facets is a list or string
    facets = spec.pop("facets", None)
    return p + facet_wrap(facets=facets, **spec)


@register_plot_component("facet_grid")
def handle_facet_grid(p: ggplot, spec: Dict[str, Any]) -> ggplot:
    """Standard 2D grid of panels."""
    facets = spec.pop("facets", None)
    if facets and "~" in facets:
        rows, cols = facets.split("~")
        rows = rows.strip()
        cols = cols.strip()
        spec["rows"] = rows if rows != "." else None
        spec["cols"] = cols if cols != "." else None
    return p + facet_grid(**spec)


@register_plot_component("facet_rows")
def handle_facet_rows(p: ggplot, spec: Dict[str, Any]) -> ggplot:
    """Shortcut for vertical-only stacking in a grid."""
    facets = spec.pop("facets", None)
    return p + facet_grid(rows=facets, **spec)


@register_plot_component("facet_cols")
def handle_facet_cols(p: ggplot, spec: Dict[str, Any]) -> ggplot:
    """Shortcut for horizontal-only stacking in a grid."""
    facets = spec.pop("facets", None)
    return p + facet_grid(cols=facets, **spec)
