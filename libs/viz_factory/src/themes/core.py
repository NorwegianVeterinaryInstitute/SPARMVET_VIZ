from typing import Dict, Any
from plotnine import (
    theme_gray, theme_bw, theme_linedraw, theme_light,
    theme_minimal, theme_classic, theme_void, theme_dark,
    ggplot
)
from viz_factory.registry import register_plot_component


@register_plot_component("theme_gray")
def handle_theme_gray(p: ggplot, spec: Dict[str, Any]) -> ggplot:
    """Default Plotnine theme."""
    return p + theme_gray(**spec)


@register_plot_component("theme_bw")
def handle_theme_bw(p: ggplot, spec: Dict[str, Any]) -> ggplot:
    """Black and white theme."""
    return p + theme_bw(**spec)


@register_plot_component("theme_linedraw")
def handle_theme_linedraw(p: ggplot, spec: Dict[str, Any]) -> ggplot:
    """Linedraw theme."""
    return p + theme_linedraw(**spec)


@register_plot_component("theme_light")
def handle_theme_light(p: ggplot, spec: Dict[str, Any]) -> ggplot:
    """Light theme."""
    return p + theme_light(**spec)


@register_plot_component("theme_minimal")
def handle_theme_minimal(p: ggplot, spec: Dict[str, Any]) -> ggplot:
    """Minimal theme."""
    return p + theme_minimal(**spec)


@register_plot_component("theme_classic")
def handle_theme_classic(p: ggplot, spec: Dict[str, Any]) -> ggplot:
    """Classic theme (axis lines, no grid)."""
    return p + theme_classic(**spec)


@register_plot_component("theme_void")
def handle_theme_void(p: ggplot, spec: Dict[str, Any]) -> ggplot:
    """Empty theme."""
    return p + theme_void(**spec)


@register_plot_component("theme_dark")
def handle_theme_dark(p: ggplot, spec: Dict[str, Any]) -> ggplot:
    """Dark background theme."""
    return p + theme_dark(**spec)


@register_plot_component("theme_dashboard")
def handle_theme_dashboard(p: ggplot, spec: Dict[str, Any]) -> ggplot:
    """
    Optimized for Shiny integration.
    High contrast (theme_bw) with larger base font for legibility on small screens.
    """
    base_size = spec.pop("base_size", 14)  # Default to larger font
    return p + theme_bw(base_size=base_size, **spec)


@register_plot_component("theme_publication")
def handle_theme_publication(p: ggplot, spec: Dict[str, Any]) -> ggplot:
    """
    Journal-ready theme.
    Clean (theme_classic) with standard publication font size.
    """
    base_size = spec.pop("base_size", 11)
    return p + theme_classic(base_size=base_size, **spec)


@register_plot_component("theme_legend_position")
def handle_theme_legend_position(p: ggplot, spec: Dict[str, Any]) -> ggplot:
    """
    Registered component to toggle legend placement.
    Params: position (top, bottom, left, right, none).
    """
    from plotnine import theme
    pos = spec.get("position", "right")
    return p + theme(legend_position=pos)


@register_plot_component("theme_custom")
def handle_theme_custom(p: ggplot, spec: Dict[str, Any]) -> ggplot:
    """
    Highly granular theme modification.
    Supports nested element_text, element_line, and element_rect definitions.
    """
    from plotnine import theme, element_text, element_line, element_rect, element_blank

    theme_kwargs = {}
    for key, val in spec.items():
        if isinstance(val, dict) and "name" in val:
            elem_name = val["name"]
            elem_params = val.get("params", {})
            if elem_name == "element_text":
                theme_kwargs[key] = element_text(**elem_params)
            elif elem_name == "element_line":
                theme_kwargs[key] = element_line(**elem_params)
            elif elem_name == "element_rect":
                theme_kwargs[key] = element_rect(**elem_params)
            elif elem_name == "element_blank":
                theme_kwargs[key] = element_blank()
        else:
            theme_kwargs[key] = val

    return p + theme(**theme_kwargs)
