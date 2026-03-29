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

    def render(self, df: Any, manifest: Dict[str, Any], plot_id: str):
        """
        Main entry point for rendering a single plot by ID from a manifest.
        Supports both Polars LazyFrame and DataFrame.

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
        # Ensure it's a LazyFrame for consistent ADR-010 handling
        if isinstance(df, pl.DataFrame):
            df = df.lazy()
        plot_config = manifest.get('plots', {}).get(plot_id)
        if not plot_config:
            raise KeyError(f"Plot ID '{plot_id}' not found in manifest.")

        # 1. Initialize mapping (Agnostic Mapping)
        mapping_spec = plot_config.get('mapping', {})
        mapping = aes(**mapping_spec)

        # 2. Instantiate the ggplot object & ADR-010: Hand-off to Pandas strictly at init.
        p = ggplot(df.collect().to_pandas(), mapping)

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
