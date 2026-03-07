from pathlib import Path
import yaml
from typing import Dict, Any, Optional
import logging

logger = logging.getLogger(__name__)


class ConfigRegistry:
    """
    A registry that recursively loads all YAML configuration files from a given base directory.
    Configurations are indexed by their mandatory `type` and `id` headers.
    """

    def __init__(self, base_config_dir: str | Path):
        self.base_dir = Path(base_config_dir)
        # Indexed by type -> id -> config_dict
        # e.g., self.registry['species']['ecoli_v1']
        self.registry: Dict[str, Dict[str, Any]] = {
            "species": {},
            "audit": {},
            "plot_template": {},
            "connector_config": {},
            "pipeline_run": {},
            "user_preference": {}
        }
        self.loaded_files = []
        self._load_all()

    def _load_all(self):
        """Recursively search for and load all .yaml files in the config directory."""
        if not self.base_dir.exists():
            logger.warning(f"Config directory {self.base_dir} does not exist.")
            return

        for yaml_path in self.base_dir.rglob("*.yaml"):
            try:
                with open(yaml_path, 'r', encoding='utf-8') as f:
                    config = yaml.safe_load(f)

                # Validation: must be a dictionary
                if not isinstance(config, dict):
                    logger.warning(
                        f"Skipping {yaml_path}: content is not a dictionary.")
                    continue

                # Parsing Headers
                config_id = config.get("id")
                config_type = config.get("type")

                if not config_id or not config_type:
                    logger.warning(
                        f"Skipping {yaml_path}: missing required 'id' or 'type' header.")
                    continue

                # Initialize type category if it doesn't exist yet
                if config_type not in self.registry:
                    self.registry[config_type] = {}

                self.registry[config_type][config_id] = config
                self.loaded_files.append(str(yaml_path))

            except yaml.YAMLError as exc:
                logger.error(f"Error parsing YAML file {yaml_path}: {exc}")
            except Exception as e:
                logger.error(f"Failed to read {yaml_path}: {e}")

    def get_config(self, config_type: str, config_id: str) -> Optional[Dict[str, Any]]:
        """Retrieve a specific configuration by its type and id."""
        return self.registry.get(config_type, {}).get(config_id)

    @staticmethod
    def deep_merge(base: Dict[str, Any], override: Dict[str, Any]) -> Dict[str, Any]:
        """
        Recursively merge two dictionaries.
        The `override` dictionary takes precedence over the `base` dictionary.
        This does not mutate the original dictionaries.
        """
        import copy
        merged = copy.deepcopy(base)

        for key, val in override.items():
            if isinstance(val, dict) and key in merged and isinstance(merged[key], dict):
                merged[key] = ConfigRegistry.deep_merge(merged[key], val)
            else:
                merged[key] = copy.deepcopy(val)

        return merged

    def resolve_plot_config(self, plot_request: Dict[str, Any], user_prefs: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Resolves the final plot configuration using the 3-tier deep merge strategy:
        1. Plot Archetype (base)
        2. Manifest Specifics (override 1)
        3. User Preferences (override 2)
        """
        # 1. Fetch Archetype (Base)
        template_id = plot_request.get('factory_id')
        archetype = self.get_config(
            "plot_template", template_id) if template_id else {}

        # 2. Merge with Manifest request
        resolved = self.deep_merge(archetype, plot_request)

        # 3. Apply User Preferences if provided
        if user_prefs:
            # Assume user_prefs is structured to override specific plot IDs or globally
            # For this example, we merge directly if the prefs apply to this specific plot
            resolved = self.deep_merge(resolved, user_prefs)

        return resolved
