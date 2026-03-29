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
    """
    Standard 2D grid of panels.
    Supports both formula-style 'facets' (rows ~ cols) or explicit 'rows'/'cols'.
    """
    facets = spec.pop("facets", None)
    if facets and "~" in facets:
        items = [i.strip() for i in facets.split("~")]
        if len(items) == 2:
            spec["rows"] = items[0] if items[0] != "." else None
            spec["cols"] = items[1] if items[1] != "." else None

    # Remove 'facets' if still present for some reason (to avoid signature error)
    spec.pop("facets", None)
    return p + facet_grid(**spec)


@register_plot_component("facet_rows")
def handle_facet_rows(p: ggplot, spec: Dict[str, Any]) -> ggplot:
    """Shortcut for vertical-only stacking in a grid."""
    row_var = spec.pop("facets", None)
    return p + facet_grid(rows=row_var, **spec)


@register_plot_component("facet_cols")
def handle_facet_cols(p: ggplot, spec: Dict[str, Any]) -> ggplot:
    """Shortcut for horizontal-only stacking in a grid."""
    col_var = spec.pop("facets", None)
    return p + facet_grid(cols=col_var, **spec)


@register_plot_component("facet_null")
def handle_facet_null(p: ggplot, spec: Dict[str, Any]) -> ggplot:
    """
    Default single-panel display. 
    This is useful for explicitly disabling multi-panel layouts.
    """
    from plotnine import facet_null
    return p + facet_null(**spec)
