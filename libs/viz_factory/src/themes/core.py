from typing import Dict, Any
from plotnine import theme_minimal, theme_bw, ggplot
from viz_factory.registry import register_plot_component


@register_plot_component("theme_minimal")
def apply_theme_minimal(p: ggplot, spec: Dict[str, Any]) -> ggplot:
    return p + theme_minimal(**spec)


@register_plot_component("theme_bw")
def apply_theme_bw(p: ggplot, spec: Dict[str, Any]) -> ggplot:
    return p + theme_bw(**spec)
