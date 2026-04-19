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
    scale_x_date, scale_y_date,
    scale_x_sqrt, scale_y_sqrt,
    scale_x_symlog, scale_y_symlog,
    scale_x_timedelta, scale_y_timedelta,
    scale_size_continuous, scale_size_discrete,
    scale_shape_discrete,
    scale_alpha_continuous, scale_alpha_discrete,
    scale_linetype_discrete,
    scale_color_identity, scale_fill_identity,
    scale_size_identity, scale_shape_identity,
    scale_alpha_identity, scale_linetype_identity,
    scale_stroke_continuous,
    scale_stroke_identity,
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


@register_plot_component("scale_x_date")
def handle_x_date(p: ggplot, spec: Dict[str, Any]) -> ggplot:
    """Standard X Date scale wrapper."""
    return p + scale_x_date(**spec)


@register_plot_component("scale_y_date")
def handle_y_date(p: ggplot, spec: Dict[str, Any]) -> ggplot:
    """Standard Y Date scale wrapper."""
    return p + scale_y_date(**spec)


@register_plot_component("scale_x_sqrt")
def handle_x_sqrt(p: ggplot, spec: Dict[str, Any]) -> ggplot:
    """Standard X Sqrt scale wrapper."""
    return p + scale_x_sqrt(**spec)


@register_plot_component("scale_y_sqrt")
def handle_y_sqrt(p: ggplot, spec: Dict[str, Any]) -> ggplot:
    """Standard Y Sqrt scale wrapper."""
    return p + scale_y_sqrt(**spec)


@register_plot_component("scale_x_symlog")
def handle_x_symlog(p: ggplot, spec: Dict[str, Any]) -> ggplot:
    """Standard X Symlog scale wrapper."""
    return p + scale_x_symlog(**spec)


@register_plot_component("scale_y_symlog")
def handle_y_symlog(p: ggplot, spec: Dict[str, Any]) -> ggplot:
    """Standard Y Symlog scale wrapper."""
    return p + scale_y_symlog(**spec)


# @register_plot_component("scale_x_timedelta")
# def handle_x_timedelta(p: ggplot, spec: Dict[str, Any]) -> ggplot:
#     """Standard X Timedelta scale wrapper."""
#     return p + scale_x_timedelta(**spec)


# @register_plot_component("scale_y_timedelta")
# def handle_y_timedelta(p: ggplot, spec: Dict[str, Any]) -> ggplot:
#     """Standard Y Timedelta scale wrapper."""
#     return p + scale_y_timedelta(**spec)


# --- Size, Shape, Alpha ---
@register_plot_component("scale_size_continuous")
def handle_size_continuous(p: ggplot, spec: Dict[str, Any]) -> ggplot:
    """Standard Size Continuous scale wrapper."""
    return p + scale_size_continuous(**spec)


@register_plot_component("scale_size_discrete")
def handle_size_discrete(p: ggplot, spec: Dict[str, Any]) -> ggplot:
    """Standard Size Discrete scale wrapper."""
    return p + scale_size_discrete(**spec)


@register_plot_component("scale_shape_discrete")
def handle_shape_discrete(p: ggplot, spec: Dict[str, Any]) -> ggplot:
    """Standard Shape Discrete scale wrapper."""
    return p + scale_shape_discrete(**spec)


@register_plot_component("scale_alpha_continuous")
def handle_alpha_continuous(p: ggplot, spec: Dict[str, Any]) -> ggplot:
    """Standard Alpha Continuous scale wrapper."""
    return p + scale_alpha_continuous(**spec)


@register_plot_component("scale_alpha_discrete")
def handle_alpha_discrete(p: ggplot, spec: Dict[str, Any]) -> ggplot:
    """Standard Alpha Discrete scale wrapper."""
    return p + scale_alpha_discrete(**spec)


# --- Linetype ---
@register_plot_component("scale_linetype_discrete")
def handle_linetype_discrete(p: ggplot, spec: Dict[str, Any]) -> ggplot:
    """Standard Linetype Discrete scale wrapper."""
    return p + scale_linetype_discrete(**spec)


# --- Stroke ---
@register_plot_component("scale_stroke_continuous")
def handle_stroke_continuous(p: ggplot, spec: Dict[str, Any]) -> ggplot:
    """Standard Stroke Continuous scale wrapper."""
    return p + scale_stroke_continuous(**spec)


# --- Identity ---
@register_plot_component("scale_color_identity")
def handle_color_identity(p: ggplot, spec: Dict[str, Any]) -> ggplot:
    """Standard Color Identity scale wrapper."""
    return p + scale_color_identity(**spec)


@register_plot_component("scale_fill_identity")
def handle_fill_identity(p: ggplot, spec: Dict[str, Any]) -> ggplot:
    """Standard Fill Identity scale wrapper."""
    return p + scale_fill_identity(**spec)


@register_plot_component("scale_size_identity")
def handle_size_identity(p: ggplot, spec: Dict[str, Any]) -> ggplot:
    """Standard Size Identity scale wrapper."""
    return p + scale_size_identity(**spec)


@register_plot_component("scale_shape_identity")
def handle_shape_identity(p: ggplot, spec: Dict[str, Any]) -> ggplot:
    """Standard Shape Identity scale wrapper."""
    return p + scale_shape_identity(**spec)


@register_plot_component("scale_alpha_identity")
def handle_alpha_identity(p: ggplot, spec: Dict[str, Any]) -> ggplot:
    """Standard Alpha Identity scale wrapper."""
    return p + scale_alpha_identity(**spec)


@register_plot_component("scale_linetype_identity")
def handle_linetype_identity(p: ggplot, spec: Dict[str, Any]) -> ggplot:
    """Standard Linetype Identity scale wrapper."""
    return p + scale_linetype_identity(**spec)


@register_plot_component("scale_stroke_identity")
def handle_stroke_identity(p: ggplot, spec: Dict[str, Any]) -> ggplot:
    """Standard Stroke Identity scale wrapper."""
    return p + scale_stroke_identity(**spec)
