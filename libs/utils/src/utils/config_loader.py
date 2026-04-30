import yaml
import os
from pathlib import Path

# @deps
# provides: class:ConfigManager
# consumed_by: app/modules/orchestrator.py, app/handlers/home_theater.py, app/handlers/blueprint_handlers.py
# @end_deps


class ConfigManager:
    def __init__(self, yaml_path):
        # Define a custom constructor for !include tags
        def include_constructor(loader, node):
            # Resolve the path relative to the current file
            included_file = loader.construct_scalar(node)
            filename = os.path.join(os.path.dirname(yaml_path), included_file)

            with open(filename, 'r') as f:
                content = yaml.load(f, Loader=yaml.SafeLoader)

            # Defensive Unnesting (ADR-014 Resilience):
            # Fragment files may be authored with a top-level wrapper key so they
            # are valid standalone YAML (e.g. input_fields: {...}).  When !include
            # pulls such a fragment into a position that already provides the key
            # name, the wrapper would become a redundant double-nesting.
            # Example: data_schemas.amr_data.input_fields: !include amr_data.yaml
            #   where amr_data.yaml starts with  input_fields: {...}
            #   Without unnesting → data_schemas.amr_data.input_fields.input_fields: {...}  ← wrong
            #   With unnesting    → data_schemas.amr_data.input_fields: {...}               ← correct
            # This is WHY manifests work even when fragment files have wrapper keys.
            # The ingestor, MetadataValidator, and DataWrangler all rely on this
            # behaviour — do NOT remove it without updating those layers.
            redundant_keys = {"input_fields", "output_fields",
                              "wrangling", "source", "recipe", "spec"}
            if isinstance(content, dict) and len(content) == 1:
                key = list(content.keys())[0]
                if key in redundant_keys:
                    print(
                        f"  [ConfigManager] Auto-unnesting redundant key '{key}' from {included_file}")
                    return content[key]
            return content

        yaml.SafeLoader.add_constructor('!include', include_constructor)

        with open(yaml_path, 'r') as f:
            self.raw_config = yaml.load(f, Loader=yaml.SafeLoader)

        # ADR-003/029b: Flatten analysis_groups into top-level 'plots' for VizFactory
        self.raw_config['plots'] = self.raw_config.get('plots', {})
        groups = self.raw_config.get('analysis_groups', {})
        for g_id, g_spec in groups.items():
            g_plots = g_spec.get('plots', {})
            for p_id, p_spec in g_plots.items():
                # Unnest 'spec' if found (Phase 11-D convention)
                if isinstance(p_spec, dict) and "spec" in p_spec:
                    p_body = p_spec["spec"].copy()
                    if "info" in p_spec:
                        p_body["info"] = p_spec["info"]
                else:
                    p_body = p_spec

                self.raw_config['plots'][p_id] = p_body

        self.defaults = self.raw_config.get('plot_defaults', {})

    def get_plot_config(self, group_name, plot_id):
        """
        Retrieves a plot config and merges it with defaults.
        Specific plot values 'shout louder' (overwrite) defaults.
        """
        # 1. Grab specific plot rules
        group = self.raw_config.get('analysis_groups', {}).get(group_name, {})
        plot_entry = group.get('plots', {}).get(plot_id, {})

        if not plot_entry:
            return None

        # 2. Handle nested spec (Phase 14-D refinement)
        # If 'spec' is present, we treat it as the base and merge 'info' into it
        if "spec" in plot_entry:
            plot_spec = plot_entry["spec"].copy()
            if "info" in plot_entry:
                plot_spec["info"] = plot_entry["info"]
        else:
            plot_spec = plot_entry

        # 3. Merge logic: start with defaults, update with specific specs
        final_config = self.defaults.copy()
        final_config.update(plot_spec)

        return final_config

    def get_metadata_rules(self):
        """Returns the 'Doorman' rules for the Ingestion Layer."""
        return self.raw_config.get('metadata_schema', {})

    def get_data_schemas(self):
        """Returns the dictionary of datasets to ingest for this pipeline."""
        return self.raw_config.get('data_schemas', {})


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(
        description="Manual execution hook for testing.")
    parser.add_argument("--test", action="store_true", help="Run in test mode")
    args = parser.parse_args()
    if args.test:
        print(f"Executing {__file__} in test mode.")
