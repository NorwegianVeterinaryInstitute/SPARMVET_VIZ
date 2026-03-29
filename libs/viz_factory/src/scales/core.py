from typing import Dict, Any
from plotnine import (
    scale_color_gradient, scale_fill_gradient,
    scale_color_gradient2, scale_fill_gradient2,
    scale_color_gradientn, scale_fill_gradientn,
    scale_color_distiller, scale_fill_distiller,
    scale_color_cmap, scale_fill_cmap,
    scale_color_cmap_d, scale_fill_cmap_d,
    scale_color_discrete, scale_fill_discrete,
    scale_color_brewer, scale_fill_brewer,
    scale_color_manual, scale_fill_manual,
    scale_x_continuous, scale_y_continuous,
    scale_x_discrete, scale_y_discrete,
    scale_x_log10, scale_y_log10,
    scale_x_reverse, scale_y_reverse,
    scale_x_datetime, scale_y_datetime,
    ggplot
)
from viz_factory.registry import register_plot_component


@register_plot_component("scale_color_gradient")
def handle_color_gradient(p: ggplot, spec: Dict[str, Any]) -> ggplot:
    """Standard Color Gradient component wrapper."""
    return p + scale_color_gradient(**spec)


@register_plot_component("scale_fill_gradient")
def handle_fill_gradient(p: ggplot, spec: Dict[str, Any]) -> ggplot:
    """Standard Fill Gradient component wrapper."""
    return p + scale_fill_gradient(**spec)


@register_plot_component("scale_color_gradient2")
def handle_color_gradient2(p: ggplot, spec: Dict[str, Any]) -> ggplot:
    """Standard Color Gradient 2 component wrapper."""
    return p + scale_color_gradient2(**spec)


@register_plot_component("scale_fill_gradient2")
def handle_fill_gradient2(p: ggplot, spec: Dict[str, Any]) -> ggplot:
    """Standard Fill Gradient 2 component wrapper."""
    return p + scale_fill_gradient2(**spec)


@register_plot_component("scale_color_gradientn")
def handle_color_gradientn(p: ggplot, spec: Dict[str, Any]) -> ggplot:
    """Standard Color Gradient n component wrapper."""
    return p + scale_color_gradientn(**spec)


@register_plot_component("scale_fill_gradientn")
def handle_fill_gradientn(p: ggplot, spec: Dict[str, Any]) -> ggplot:
    """Standard Fill Gradient n component wrapper."""
    return p + scale_fill_gradientn(**spec)


@register_plot_component("scale_color_distiller")
def handle_color_distiller(p: ggplot, spec: Dict[str, Any]) -> ggplot:
    """Standard Color Distiller component wrapper."""
    return p + scale_color_distiller(**spec)


@register_plot_component("scale_fill_distiller")
def handle_fill_distiller(p: ggplot, spec: Dict[str, Any]) -> ggplot:
    """Standard Fill Distiller component wrapper."""
    return p + scale_fill_distiller(**spec)


@register_plot_component("scale_color_cmap")
def handle_color_cmap(p: ggplot, spec: Dict[str, Any]) -> ggplot:
    """Standard Color Matplotlib Cmap component wrapper."""
    return p + scale_color_cmap(**spec)


@register_plot_component("scale_fill_cmap")
def handle_fill_cmap(p: ggplot, spec: Dict[str, Any]) -> ggplot:
    """Standard Fill Matplotlib Cmap component wrapper."""
    return p + scale_fill_cmap(**spec)


@register_plot_component("scale_color_viridis_d")
def handle_color_viridis_d(p: ggplot, spec: Dict[str, Any]) -> ggplot:
    """Standard Color Viridis (Discrete) via cmap mapping."""
    if "cmap_name" not in spec:
        # Map Viridis 'option' (magma, inferno, etc.) to matplotlib cmap_name
        spec["cmap_name"] = spec.pop("option", "viridis")
    return p + scale_color_cmap_d(**spec)


@register_plot_component("scale_fill_viridis_d")
def handle_fill_viridis_d(p: ggplot, spec: Dict[str, Any]) -> ggplot:
    """Standard Fill Viridis (Discrete) via cmap mapping."""
    if "cmap_name" not in spec:
        spec["cmap_name"] = spec.pop("option", "viridis")
    return p + scale_fill_cmap_d(**spec)


@register_plot_component("scale_color_viridis_c")
def handle_color_viridis_c(p: ggplot, spec: Dict[str, Any]) -> ggplot:
    """Standard Color Viridis (Continuous) via cmap mapping."""
    if "cmap_name" not in spec:
        spec["cmap_name"] = spec.pop("option", "viridis")
    return p + scale_color_cmap(**spec)


@register_plot_component("scale_fill_viridis_c")
def handle_fill_viridis_c(p: ggplot, spec: Dict[str, Any]) -> ggplot:
    """Standard Fill Viridis (Continuous) via cmap mapping."""
    if "cmap_name" not in spec:
        spec["cmap_name"] = spec.pop("option", "viridis")
    return p + scale_fill_cmap(**spec)


@register_plot_component("scale_color_cmap_d")
def handle_color_cmap_d(p: ggplot, spec: Dict[str, Any]) -> ggplot:
    """Standard Discrete Color Cmap component wrapper."""
    return p + scale_color_cmap_d(**spec)


@register_plot_component("scale_fill_cmap_d")
def handle_fill_cmap_d(p: ggplot, spec: Dict[str, Any]) -> ggplot:
    """Standard Discrete Fill Cmap component wrapper."""
    return p + scale_fill_cmap_d(**spec)


@register_plot_component("scale_color_discrete")
def handle_color_discrete(p: ggplot, spec: Dict[str, Any]) -> ggplot:
    """Standard Color Discrete component wrapper."""
    return p + scale_color_discrete(**spec)


@register_plot_component("scale_fill_discrete")
def handle_fill_discrete(p: ggplot, spec: Dict[str, Any]) -> ggplot:
    """Standard Fill Discrete component wrapper."""
    return p + scale_fill_discrete(**spec)


@register_plot_component("scale_color_brewer")
def handle_color_brewer(p: ggplot, spec: Dict[str, Any]) -> ggplot:
    """Standard Color Brewer (Discrete) component wrapper."""
    return p + scale_color_brewer(**spec)


@register_plot_component("scale_fill_brewer")
def handle_fill_brewer(p: ggplot, spec: Dict[str, Any]) -> ggplot:
    """Standard Fill Brewer (Discrete) component wrapper."""
    return p + scale_fill_brewer(**spec)


@register_plot_component("scale_color_manual")
def handle_color_manual(p: ggplot, spec: Dict[str, Any]) -> ggplot:
    """Standard Color Manual component wrapper."""
    return p + scale_color_manual(**spec)


@register_plot_component("scale_fill_manual")
def handle_fill_manual(p: ggplot, spec: Dict[str, Any]) -> ggplot:
    """Standard Fill Manual component wrapper."""
    return p + scale_fill_manual(**spec)


@register_plot_component("scale_x_continuous")
def handle_x_continuous(p: ggplot, spec: Dict[str, Any]) -> ggplot:
    """Standard X Continuous scale wrapper."""
    return p + scale_x_continuous(**spec)


@register_plot_component("scale_y_continuous")
def handle_y_continuous(p: ggplot, spec: Dict[str, Any]) -> ggplot:
    """Standard Y Continuous scale wrapper."""
    return p + scale_y_continuous(**spec)


@register_plot_component("scale_x_discrete")
def handle_x_discrete(p: ggplot, spec: Dict[str, Any]) -> ggplot:
    """Standard X Discrete scale wrapper."""
    return p + scale_x_discrete(**spec)


@register_plot_component("scale_y_discrete")
def handle_y_discrete(p: ggplot, spec: Dict[str, Any]) -> ggplot:
    """Standard Y Discrete scale wrapper."""
    return p + scale_y_discrete(**spec)


@register_plot_component("scale_x_log10")
def handle_x_log10(p: ggplot, spec: Dict[str, Any]) -> ggplot:
    """Standard X Log10 scale wrapper."""
    return p + scale_x_log10(**spec)


@register_plot_component("scale_y_log10")
def handle_y_log10(p: ggplot, spec: Dict[str, Any]) -> ggplot:
    """Standard Y Log10 scale wrapper."""
    return p + scale_y_log10(**spec)


@register_plot_component("scale_x_reverse")
def handle_x_reverse(p: ggplot, spec: Dict[str, Any]) -> ggplot:
    """Standard X Inverted scale wrapper."""
    return p + scale_x_reverse(**spec)


@register_plot_component("scale_y_reverse")
def handle_y_reverse(p: ggplot, spec: Dict[str, Any]) -> ggplot:
    """Standard Y Inverted scale wrapper."""
    return p + scale_y_reverse(**spec)


@register_plot_component("scale_x_datetime")
def handle_x_datetime(p: ggplot, spec: Dict[str, Any]) -> ggplot:
    """Standard X Date/Time scale wrapper."""
    return p + scale_x_datetime(**spec)


@register_plot_component("scale_y_datetime")
def handle_y_datetime(p: ggplot, spec: Dict[str, Any]) -> ggplot:
    """Standard Y Date/Time scale wrapper."""
    return p + scale_y_datetime(**spec)
