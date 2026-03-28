import polars as pl
from plotnine import ggplot, aes
from typing import Dict, Any, List
# Explicit imports to ensure registration occurs
from viz_factory.registry import get_component


class VizFactory:
    """
    Electronic Artist Pillar (VizFactory).
    Takes standardized Polars dataframes and applies declarative Plotnine layers.
    """

    def render_plot(self, df: pl.LazyFrame, manifest_dict: Dict[str, Any], plot_id: str):
        """
        Main entry point for rendering a single plot by ID from a manifest.

        manifest_dict follows the structure:
        {
           "plots": {
              "[plot_id]": {
                 "mapping": {"x": "column_a", "fill": "column_b"},
                 "layers": [
                    {"name": "geom_boxplot", "params": {"outlier_shape": "NA"}},
                    {"name": "theme_minimal", "params": {}}
                 ]
              }
           }
        }
        """
        plot_config = manifest_dict.get('plots', {}).get(plot_id)
        if not plot_config:
            raise KeyError(f"Plot ID '{plot_id}' not found in manifest.")

        # ADR-010: Hand-off to Pandas ONLY at the last moment of plotting.
        # Plotnine does not natively support Polars yet.
        pdf = df.collect().to_pandas()

        # 1. Initialize mapping (Agnostic Mapping)
        mapping_spec = plot_config.get('mapping', {})
        # Translate string based mapping into plotnine aes object
        mapping = aes(**mapping_spec)

        # 2. Instantiate the ggplot object
        p = ggplot(pdf, mapping)

        # 3. Apply Layers sequentially
        layers = plot_config.get('layers', [])
        for layer_spec in layers:
            layer_name = layer_spec.get('name')
            layer_params = layer_spec.get('params', {})

            # Fetch the registered component
            component_func = get_component(layer_name)

            # Pipe the plot object through the component
            p = component_func(p, layer_params)

            print(f"Applied layer: {layer_name}")

        return p
