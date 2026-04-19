# libs/viz_gallery/src/viz_gallery/gallery_manager.py
import yaml
import shutil
from pathlib import Path
from datetime import datetime
import polars as pl


class GalleryManager:
    """
    GalleryManager (gallery_manager.py) – part of the viz_gallery library.
    Handles persistence of a recipe, data sample, and metadata to the
    assets/gallery_data directory.
    """

    def __init__(self, gallery_dir: str = "assets/gallery_data"):
        self.gallery_dir = Path(gallery_dir)
        self.gallery_dir.mkdir(parents=True, exist_ok=True)

    def submit_recipe(self, name: str, recipe: list, data: pl.DataFrame,
                      meta_markdown: str, plot_config: dict = None,
                      plot_source_path: str = None) -> str:
        """Create a standardized gallery bundle.
        Returns the absolute path to the created bundle directory.
        """
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        safe_name = name.lower().replace(" ", "_")
        folder_name = f"{ts}_{safe_name}"
        target_dir = self.gallery_dir / folder_name
        target_dir.mkdir(parents=True, exist_ok=True)

        # 1. Save recipe manifest (YAML)
        manifest_bundle = {
            "info": {
                "name": name,
                "submission_date": datetime.now().strftime("%Y-%m-%d"),
            },
            "data_path": "example_data.tsv",
            "plots": {
                safe_name: plot_config or {}
            },
            "wrangling": {
                "tier1": [],
                "tier2": [],
                "tier3": recipe
            }
        }
        with open(target_dir / "recipe_manifest.yaml", "w") as f:
            yaml.dump(manifest_bundle, f, sort_keys=False)

        # 2. Save data sample (TSV) – limit to 100 rows for preview
        data.head(100).write_csv(
            target_dir / "example_data.tsv", separator="\t")

        # 3. Save metadata markdown
        with open(target_dir / "recipe_meta.md", "w") as f:
            f.write(meta_markdown)

        # 4. Optional plot preview
        if plot_source_path and Path(plot_source_path).exists():
            shutil.copy(plot_source_path, target_dir / "preview_plot.png")

        return str(target_dir)

    def list_submissions(self):
        """Return a list of existing gallery bundle folder names."""
        return [d.name for d in self.gallery_dir.iterdir() if d.is_dir()]
