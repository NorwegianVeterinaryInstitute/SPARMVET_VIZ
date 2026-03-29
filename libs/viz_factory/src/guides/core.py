from typing import Dict, Any
from plotnine import (
    guides, guide_legend, guide_colorbar,
    ggplot
)
from viz_factory.registry import register_plot_component


@register_plot_component("guides")
def handle_guides_group(p: ggplot, spec: Dict[str, Any]) -> ggplot:
    """
    Main guides container. Allows setting multiple guides at once.
    Example:
      params:
        color: "none"
        fill: "legend"
    """
    guide_specs = {}
    for mapping, guide_type in spec.items():
        if guide_type == "none" or guide_type is False:
            guide_specs[mapping] = False
        elif guide_type == "legend":
            guide_specs[mapping] = guide_legend()
        elif guide_type == "colorbar":
            guide_specs[mapping] = guide_colorbar()
        else:
            guide_specs[mapping] = guide_type

    return p + guides(**guide_specs)


@register_plot_component("guide_legend")
def handle_guide_legend(p: ggplot, spec: Dict[str, Any]) -> ggplot:
    """
    Apply a legend guide to a specific mapping.
    MANDATORY key: 'mapping' (e.g., 'color', 'fill', 'shape')
    """
    mapping = spec.pop("mapping", None)
    if not mapping:
        print("Warning: guide_legend requires a 'mapping' parameter.")
        return p
    return p + guides(**{mapping: guide_legend(**spec)})


@register_plot_component("guide_colorbar")
def handle_guide_colorbar(p: ggplot, spec: Dict[str, Any]) -> ggplot:
    """
    Apply a colorbar guide to a specific mapping (usually color or fill).
    MANDATORY key: 'mapping'
    """
    mapping = spec.pop("mapping", None)
    if not mapping:
        print("Warning: guide_colorbar requires a 'mapping' parameter.")
        return p
    return p + guides(**{mapping: guide_colorbar(**spec)})


@register_plot_component("guide_colourbar")
def handle_guide_colourbar(p: ggplot, spec: Dict[str, Any]) -> ggplot:
    """Alias for guide_colorbar."""
    return handle_guide_colorbar(p, spec)


@register_plot_component("guide_none")
def handle_guide_none(p: ggplot, spec: Dict[str, Any]) -> ggplot:
    """
    Remove the guide for a specific mapping.
    MANDATORY key: 'mapping'
    """
    mapping = spec.pop("mapping", None)
    if not mapping:
        print("Warning: guide_none requires a 'mapping' parameter.")
        return p
    return p + guides(**{mapping: False})
