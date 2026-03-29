from typing import Dict, Any
from plotnine import (
    theme, theme_gray, theme_bw, theme_linedraw, theme_light,
    theme_minimal, theme_classic, theme_void, theme_dark,
    ggplot, element_text, element_line, element_rect, element_blank
)
from viz_factory.registry import register_plot_component


def _apply_theme_safely(base_theme_func, spec: Dict[str, Any]) -> Any:
    """
    Helper to apply a base theme while allowing additional theme() parameters
    to be passed in the same spec (e.g. legend_position).
    """
    base_keys = ["base_size", "base_family"]
    base_params = {k: spec.pop(k) for k in base_keys if k in spec}

    # 1. Start with base theme
    p_theme = base_theme_func(**base_params)

    # 2. Add extra parameters via theme()
    if spec:
        p_theme += theme(**spec)

    return p_theme


@register_plot_component("theme_gray")
def handle_theme_gray(p: ggplot, spec: Dict[str, Any]) -> ggplot:
    return p + _apply_theme_safely(theme_gray, spec)


@register_plot_component("theme_bw")
def handle_theme_bw(p: ggplot, spec: Dict[str, Any]) -> ggplot:
    return p + _apply_theme_safely(theme_bw, spec)


@register_plot_component("theme_linedraw")
def handle_theme_linedraw(p: ggplot, spec: Dict[str, Any]) -> ggplot:
    return p + _apply_theme_safely(theme_linedraw, spec)


@register_plot_component("theme_light")
def handle_theme_light(p: ggplot, spec: Dict[str, Any]) -> ggplot:
    return p + _apply_theme_safely(theme_light, spec)


@register_plot_component("theme_minimal")
def handle_theme_minimal(p: ggplot, spec: Dict[str, Any]) -> ggplot:
    return p + _apply_theme_safely(theme_minimal, spec)


@register_plot_component("theme_classic")
def handle_theme_classic(p: ggplot, spec: Dict[str, Any]) -> ggplot:
    return p + _apply_theme_safely(theme_classic, spec)


@register_plot_component("theme_void")
def handle_theme_void(p: ggplot, spec: Dict[str, Any]) -> ggplot:
    return p + _apply_theme_safely(theme_void, spec)


@register_plot_component("theme_dark")
def handle_theme_dark(p: ggplot, spec: Dict[str, Any]) -> ggplot:
    return p + _apply_theme_safely(theme_dark, spec)


@register_plot_component("theme_dashboard")
def handle_theme_dashboard(p: ggplot, spec: Dict[str, Any]) -> ggplot:
    spec.setdefault("base_size", 14)
    return p + _apply_theme_safely(theme_bw, spec)


@register_plot_component("theme_publication")
def handle_theme_publication(p: ggplot, spec: Dict[str, Any]) -> ggplot:
    spec.setdefault("base_size", 11)
    return p + _apply_theme_safely(theme_classic, spec)


@register_plot_component("theme_legend_position")
def handle_theme_legend_position(p: ggplot, spec: Dict[str, Any]) -> ggplot:
    pos = spec.get("position", "right")
    return p + theme(legend_position=pos)


@register_plot_component("theme_custom")
def handle_theme_custom(p: ggplot, spec: Dict[str, Any]) -> ggplot:
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
