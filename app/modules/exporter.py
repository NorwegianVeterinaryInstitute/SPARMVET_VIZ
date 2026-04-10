# app/modules/exporter.py
import zipfile
import pandas as pd
import yaml
import subprocess
from pathlib import Path
from datetime import datetime


class SubmissionExporter:
    """Handles the creation of the SPARMVET Submission Package (.zip)."""

    def __init__(self, export_dir: str = "tmp/exports"):
        self.export_dir = Path(export_dir)
        self.export_dir.mkdir(parents=True, exist_ok=True)

    def create_audit_log(self, narrative: list, project_id: str = "ABROMICS_DEMO") -> str:
        """Converts the narrative log into a human-readable audit trace via Pandoc."""
        ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        md_path = self.export_dir / "audit_log.md"
        txt_path = self.export_dir / "audit_log.txt"

        # 1. Draft the Markdown trace
        with open(md_path, "w") as f:
            f.write(f"# SPARMVET AUDIT LOG: {project_id}\n")
            f.write(f"Generated: {ts}\n\n")
            f.write("## 📜 Narrative Trace (ADR-026)\n")
            for entry in narrative:
                f.write(f"- {entry}\n")

        # 2. Convert to Text/Docx via Pandoc
        try:
            subprocess.run(["pandoc", str(md_path), "-o",
                           str(txt_path)], check=True)
            return str(txt_path)
        except Exception:
            return str(md_path)  # Fallback to markdown if pandoc fails

    def bundle_package(self, plot_path: str, data_df: pd.DataFrame, manifest: dict, audit_trail: list) -> str:
        """Creates the final .zip Submission Package."""
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        zip_path = self.export_dir / f"submission_{ts}.zip"

        # 1. Prep individual files
        audit_path = self.create_audit_log(audit_trail)
        data_path = self.export_dir / "data_subset.csv"
        data_df.to_csv(data_path, index=False)

        manifest_path = self.export_dir / "active_recipe.yaml"
        with open(manifest_path, "w") as f:
            yaml.dump(manifest, f)

        # 2. Build the Zip
        with zipfile.ZipFile(zip_path, 'w') as zipf:
            zipf.write(audit_path, arcname="audit_log.txt")
            zipf.write(data_path, arcname="data_subset.csv")
            zipf.write(manifest_path, arcname="active_recipe.yaml")
            if plot_path and Path(plot_path).exists():
                zipf.write(plot_path, arcname="high_dpi_plot.png")

        return str(zip_path)

    def bundle_global_export(self, project_id: str, plot_path: str, tiers: dict, manifest: dict, audit_trail: list) -> str:
        """
        Bundles the full session state (Phase 14-C).
        Format: SPARMVET_EXPORT_{ISO_DATE}_{PROJECT_ID}.zip
        """
        iso_date = datetime.now().strftime("%Y-%m-%d")
        zip_name = f"SPARMVET_EXPORT_{iso_date}_{project_id}.zip"
        zip_path = self.export_dir / zip_name

        # 1. Prep individual files
        audit_path = self.create_audit_log(audit_trail, project_id)

        with zipfile.ZipFile(zip_path, 'w') as zipf:
            zipf.write(audit_path, arcname="audit_log.txt")

            # YAML Manifest
            manifest_path = self.export_dir / "session_manifest.yaml"
            with open(manifest_path, "w") as f:
                yaml.dump(manifest, f)
            zipf.write(manifest_path, arcname="session_manifest.yaml")

            # Tiers 1-3 Data
            for tier_name, df in tiers.items():
                if df is not None:
                    t_path = self.export_dir / f"{tier_name}.csv"
                    df.to_csv(t_path, index=False)
                    zipf.write(t_path, arcname=f"data/{tier_name}.csv")

            # Plot
            if plot_path and Path(plot_path).exists():
                zipf.write(plot_path, arcname="preview_plot.png")

            # Educational Metadata Template (ADR-033/Phase 14-C)
            meta_template = f"""# Recipe Metadata: {project_id}
## Suitability
- [Describe when this visualization is most useful]

## Data Schema (Tier 1)
- [List required columns and types]

## Transformation Logic (Tier 2)
- [Describe essential reshapes]

## Interpretations
- [Assumptions, limitations, and comments]
"""
            meta_path = self.export_dir / "recipe_meta.md"
            with open(meta_path, "w") as f:
                f.write(meta_template)
            zipf.write(meta_path, arcname="recipe_meta.md")

        return str(zip_path)
