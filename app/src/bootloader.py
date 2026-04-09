# app/src/bootloader.py
import yaml
from pathlib import Path
from typing import Dict, Any


class Bootloader:
    """
    System Bootloader (ADR-031, ADR-026).
    Handles path authority and UI Persona feature toggling.
    """

    def __init__(self, persona: str = "template_persona", connector: str = "local"):
        self.persona = persona
        self.connector = connector

        # 1. Path Authority (Location Management)
        self.connector_path = Path(
            f"config/connectors/{connector}/{connector}_connector.yaml")
        self.locations = self._load_locations()

        # 2. Persona Logic (Feature Toggling)
        self.persona_path = Path(
            f"config/ui/templates/{persona}_template.yaml")
        self.config = self._load_persona_config()
        self.features = self.config.get("features", {})
        self.automation = self.config.get("automation", {})

        # 3. Pipeline Authority (Agnostic Discovery)
        self.manifest_dir = self.get_location("manifests")
        self.available_manifests = self._discover_manifests()

    def _discover_manifests(self) -> Dict[str, str]:
        """Scans the manifest directory for YAML files."""
        mf_files = list(self.manifest_dir.glob("*.yaml"))
        return {f.stem: str(f) for f in mf_files}

    def get_default_pipeline(self) -> str:
        """Returns the first available manifest ID found."""
        if not self.available_manifests:
            raise FileNotFoundError("No manifests found in Location 2.")
        return list(self.available_manifests.keys())[0]

    def _load_locations(self) -> Dict[str, str]:
        """Loads system paths from the connector configuration."""
        if not self.connector_path.exists():
            raise FileNotFoundError(
                f"Connector config not found: {self.connector_path}")

        with open(self.connector_path, "r") as f:
            cfg = yaml.safe_load(f)
            return cfg.get("locations", {})

    def _load_persona_config(self) -> Dict[str, Any]:
        """Loads UI feature toggles from the persona template."""
        if not self.persona_path.exists():
            # Fallback to local file if template not found in templates dir
            fallback = Path(f"config/ui/{self.persona}.yaml")
            if fallback.exists():
                with open(fallback, "r") as f:
                    return yaml.safe_load(f)
            return {}

        with open(self.persona_path, "r") as f:
            return yaml.safe_load(f)

    def get_location(self, key: str) -> Path:
        """Returns the resolved path for a specific location key."""
        path_str = self.locations.get(key)
        if not path_str:
            raise KeyError(f"Location key '{key}' not defined in connector.")
        return Path(path_str)

    def is_enabled(self, feature: str) -> bool:
        """Checks if a UI feature is enabled."""
        return self.features.get(feature, False)

    def get_automation_setting(self, key: str, subkey: str) -> Any:
        """Returns automation settings (e.g., ghost_save frequency)."""
        return self.automation.get(key, {}).get(subkey)


# Global Instance for UI/Server discovery
bootloader = Bootloader()
