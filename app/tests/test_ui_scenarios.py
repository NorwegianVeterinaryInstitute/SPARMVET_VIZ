# app/tests/test_ui_scenarios.py
import unittest
from app.src.bootloader import BootLoader
from app.modules.orchestrator import DataOrchestrator
from app.modules.exporter import SubmissionExporter
from pathlib import Path
import polars as pl
import yaml


class TestUIScenarios(unittest.TestCase):
    def setUp(self):
        self.bootloader = BootLoader(persona="test_full_pipeline")
        self.orchestrator = DataOrchestrator(
            manifests_dir=self.bootloader.get_location("manifests"),
            raw_data_dir=self.bootloader.get_location("raw_data")
        )
        self.exporter = SubmissionExporter("tmp/test_exports")

    def test_global_export_workflow(self):
        """Simulates a full export cycle."""
        print("Testing Global Export Workflow...")
        # 1. Mock Data
        df = pl.DataFrame({"sample_id": ["S1"], "species": ["E. coli"]})
        tiers = {"tier1_anchor": df.to_pandas(), "tier3_leaf": df.to_pandas()}

        # 2. Bundle
        zip_path = self.exporter.bundle_global_export(
            project_id="TEST_PROJECT",
            plot_path="tmp/test_plot.png",
            tiers=tiers,
            manifest={"info": {"name": "Test"}},
            audit_trail=["test action: verified"]
        )
        self.assertTrue(Path(zip_path).exists())
        print(f"  [SUCCESS] Export materialized at {zip_path}")

    def test_persona_gating_logic(self):
        """Verifies feature toggles align with persona ADR-026."""
        print("Testing Persona Gating...")
        self.assertTrue(self.bootloader.is_enabled("developer_mode_enabled"))

        # Test restricted persona
        limited = BootLoader(persona="ui_persona")
        self.assertFalse(limited.is_enabled("developer_mode_enabled"))
        print("  [SUCCESS] Persona isolation enforced.")


if __name__ == "__main__":
    # Ensure mock plot exists
    Path("tmp/test_plot.png").write_text("dummy")
    unittest.main()
