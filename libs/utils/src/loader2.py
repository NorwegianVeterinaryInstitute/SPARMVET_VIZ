import yaml
import os
from pathlib import Path


class ConfigManager:
    def __init__(self, yaml_path):
        # Define a custom constructor for !include tags
        def include_constructor(loader, node):
            # Resolve the path relative to the current file
            filename = os.path.join(os.path.dirname(
                yaml_path), loader.construct_scalar(node))
            with open(filename, 'r') as f:
                return yaml.load(f, Loader=yaml.SafeLoader)

        yaml.SafeLoader.add_constructor('!include', include_constructor)

        with open(yaml_path, 'r') as f:
            self.raw_config = yaml.load(f, Loader=yaml.SafeLoader)

        self.defaults = self.raw_config.get('plot_defaults', {})

    def get_plot_config(self, group_name, plot_id):
        """
        Retrieves a plot config and merges it with defaults.
        Specific plot values 'shout louder' (overwrite) defaults.
        """
        # 1. Grab specific plot rules
        group = self.raw_config.get('analysis_groups', {}).get(group_name, {})
        plot_spec = group.get('plots', {}).get(plot_id, {})

        if not plot_spec:
            return None

        # 2. Merge logic: start with defaults, update with specific specs
        # This is the "Cascade Pattern" in Python
        final_config = self.defaults.copy()
        final_config.update(plot_spec)

        return final_config

    def get_metadata_rules(self):
        """Returns the 'Doorman' rules for the Ingestion Layer."""
        return self.raw_config.get('metadata_schema', {})

    def get_data_schemas(self):
        """Returns the dictionary of datasets to ingest for this pipeline."""
        return self.raw_config.get('data_schemas', {})
