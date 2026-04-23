# app/modules/persona_manager.py
# @deps
# provides: class:PersonaManager
# consumed_by: app/src/server.py, app/handlers/home_theater.py
# doc: .antigravity/knowledge/architecture_decisions.md#ADR-026
# @end_deps
import yaml
from pathlib import Path
from typing import Dict, Any, List

class PersonaManager:
    """Manages the UI Persona and feature visibility based on ADR-026."""
    
    def __init__(self, mode: str = "pipeline"):
        self.mode = mode
        self.config_path = Path(f"config/ui/{mode}.yaml")
        self.config = self._load_config()
        self.persona = self.config.get("persona", "pipeline")
        self.features = self.config.get("features", {})
        
    def _load_config(self) -> Dict[str, Any]:
        """Loads the bootloader configuration."""
        if not self.config_path.exists():
            return {"persona": "pipeline", "features": {}}
        try:
            with open(self.config_path, "r") as f:
                return yaml.safe_load(f)
        except Exception:
            return {"persona": "pipeline", "features": {}}

    def can_feature(self, feature_name: str) -> bool:
        """Checks if a feature is enabled for the current persona."""
        return self.features.get(feature_name, False)

    def get_filters(self) -> List[Dict[str, str]]:
        """Returns the dynamic filter definitions."""
        return self.config.get("demo_filters", [])

    def is_pipeline_mode(self) -> bool:
        """Returns True if the persona is 'pipeline'."""
        return self.persona == "pipeline"
