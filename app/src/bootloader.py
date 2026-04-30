# app/src/bootloader.py
import yaml
from pathlib import Path
from typing import Dict, Any


class Bootloader:
    """
    System Bootloader (ADR-031, ADR-026).
    Handles path authority and UI Persona feature toggling.
    """
    # ADR-031: Static Cache Layer
    _persona_cache: Dict[str, Dict[str, Any]] = {}
    _connector_cache: Dict[str, Dict[str, Any]] = {}

    # Hierarchical Asset Cache: project_id -> dataset_id -> plot_id -> asset_type -> asset
    _asset_cache: Dict[str, Dict[str, Dict[str, Dict[str, Any]]]] = {}

    def get_cached_asset(self, project_id: str, dataset_id: str, plot_id: str, asset_type: str) -> Any:
        try:
            return self._asset_cache[project_id][dataset_id][plot_id][asset_type]
        except KeyError:
            return None

    def set_cached_asset(self, project_id: str, dataset_id: str, plot_id: str, asset_type: str, asset: Any):
        if project_id not in self._asset_cache:
            self._asset_cache[project_id] = {}
        if dataset_id not in self._asset_cache[project_id]:
            self._asset_cache[project_id][dataset_id] = {}
        if plot_id not in self._asset_cache[project_id][dataset_id]:
            self._asset_cache[project_id][dataset_id][plot_id] = {}
        self._asset_cache[project_id][dataset_id][plot_id][asset_type] = asset

    def __init__(self, persona: str | None = None, connector: str | None = None):
        import os
        self.persona = persona or os.environ.get(
            "SPARMVET_PERSONA", "ui_persona")
        self.connector = connector or os.environ.get(
            "SPARMVET_CONNECTOR", "local")

        # 1. Path Authority (Location Management)
        self.connector_path = Path(
            f"config/connectors/{self.connector}/{self.connector}_connector.yaml")

        # Optimized Load (Connector is usually static per session)
        if self.connector not in self._connector_cache:
            self._connector_cache[self.connector] = self._load_connector_config(
            )
        self.connector_config = self._connector_cache[self.connector]
        self.locations = self.connector_config.get("locations", {})

        # 2. Persona Logic (Feature Toggling)
        self.set_persona(self.persona)

        # 3. Project Authority (Agnostic Discovery)
        self.project_dir = self.get_location("manifests")
        self.available_projects = self._discover_projects()

    def set_persona(self, persona: str):
        """Updates the persona context with caching (Zero-Latency)."""
        self.persona = persona
        self.persona_path = Path(
            f"config/ui/templates/{self.persona}_template.yaml")

        if self.persona not in self._persona_cache:
            self._persona_cache[self.persona] = self._load_persona_config()

        self.config = self._persona_cache[self.persona]
        self.features = self.config.get("features", {})
        self.automation = self.config.get("automation", {})

    def _discover_projects(self) -> Dict[str, str]:
        """Scans the project directory for YAML manifests."""
        mf_files = list(self.project_dir.glob("*.yaml"))
        return {f.stem: str(f) for f in mf_files}

    def get_default_project(self) -> str:
        """Returns the first available project ID found."""
        if not self.available_projects:
            raise FileNotFoundError("No projects found in Location 2.")
        return list(self.available_projects.keys())[0]

    def _load_connector_config(self) -> Dict[str, Any]:
        """Loads the entire connector configuration (locations, scripts, runtime)."""
        if not self.connector_path.exists():
            raise FileNotFoundError(
                f"Connector config not found: {self.connector_path}")

        try:
            with open(self.connector_path, "r") as f:
                return yaml.safe_load(f) or {}
        except Exception:
            return {}

    def _load_persona_config(self) -> Dict[str, Any]:
        """Loads UI feature toggles from the persona template."""
        path = self.persona_path
        if not path.exists():
            # Fallback to local file if template not found in templates dir
            path = Path(f"config/ui/{self.persona}.yaml")
            if not path.exists():
                return {}

        try:
            with open(path, "r") as f:
                return yaml.safe_load(f) or {}
        except Exception:
            return {}

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

    def get_script_path(self, key: str) -> Path:
        """Resolves system script paths from connector config (ADR-032)."""
        mapping = self.connector_config.get("scripts", {})
        path_str = mapping.get(key)
        if not path_str:
            raise KeyError(
                f"Script key '{key}' not found in connector 'scripts' block.")
        return Path(path_str)

    def get_python_path(self) -> str:
        """Retrieves the configured Python interpreter path (ADR-031)."""
        runtime = self.connector_config.get("runtime", {})
        path = runtime.get("python_interpreter")
        if not path:
            raise KeyError(
                "Connector config missing 'runtime.python_interpreter' definition.")
        return str(path)


# Global Instance for UI/Server discovery
bootloader = Bootloader()
