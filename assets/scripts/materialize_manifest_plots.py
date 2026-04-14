import polars as pl
from viz_factory.viz_factory import VizFactory
from utils.config_loader import ConfigManager
import os
import sys
import argparse
from pathlib import Path
import matplotlib
matplotlib.use('Agg')

"""
materialize_manifest_plots.py
----------------------------
Official tool for 'Headless Art Audit'. 
Reads a master manifest, resolves all plot definitions across all analysis groups,
locates materialized data in tmp/ or layer1/, and renders PNG files.
"""


def main():
    parser = argparse.ArgumentParser(
        description="Materialize all plots from a manifest into Layer 3 PNGs.")
    parser.add_argument("--manifest", type=str, required=True,
                        help="Path to the master manifest (.yaml)")
    parser.add_argument("--output_root", type=str,
                        default="tmp/materialized_gallery", help="Directory to save PNGs")
    args = parser.parse_args()

    print(f"🚀 [GALLERY] Starting materialization for: {args.manifest}")

    try:
        config_loader = ConfigManager(args.manifest)
        config = config_loader.raw_config
        manifest_id = config.get("id", "unknown_manifest")
    except Exception as e:
        print(f"❌ [FATAL] Failed to load manifest: {e}")
        sys.exit(1)

    factory = VizFactory()

    # 1. Prepare Data Registry
    layer1_root = Path(f"tmp/TEST_MANIFEST/{manifest_id}/layer1")

    # 2. Iterate through Analysis Groups
    analysis_groups = config.get("analysis_groups", {})
    for group_id, group_config in analysis_groups.items():
        print(f"\n📂 [GROUP] {group_id}")
        plots = group_config.get("plots", {})

        group_dir = Path(args.output_root) / manifest_id / group_id
        group_dir.mkdir(parents=True, exist_ok=True)

        for plot_id, plot_entry in plots.items():
            spec = plot_entry.get("spec", {})
            target_dataset = spec.get("target_dataset")

            if not target_dataset:
                continue

            # Resolve Data Location
            data_path = None

            # 1. Check for materialized assembly in root tmp/
            potential_assembly = Path(f"tmp/EVE_assembly_{target_dataset}.tsv")
            if potential_assembly.exists():
                data_path = potential_assembly
            else:
                # 2. Check for Layer 1 debug view in various potential folders
                search_roots = [
                    Path(f"tmp/TEST_MANIFEST/{manifest_id}/layer1"),
                    # Filename fallback
                    Path(f"tmp/TEST_MANIFEST/1_test_data_ST22_dummy/layer1"),
                    Path("tmp/materialized_gallery") / manifest_id / "layer1"
                ]
                for root in search_roots:
                    potential_l1 = root / f"{target_dataset}_debug.tsv"
                    if potential_l1.exists():
                        data_path = potential_l1
                        break

            if not data_path:
                print(
                    f"  └── ❌ [FAIL] {plot_id}: Target data '{target_dataset}' not found.")
                continue

            print(
                f"  └── 🖌️ [RENDER] Rendering {plot_id} via {data_path.name}...")

            try:
                # Load and Render (Lazy with robust null handling)
                df = pl.scan_csv(data_path, separator="\t",
                                 null_values=["-", "n/a", "NA", "null"])
                p = factory.render(df, {"plots": {plot_id: spec}}, plot_id)

                output_path = group_dir / f"{plot_id}.png"
                p.save(output_path, width=10, height=6, dpi=150, verbose=False)
                print(f"      ✅ [DONE] Saved to {output_path}")
            except Exception as e:
                print(f"      ❌ [ERROR] {plot_id}: {e}")

    print(f"\n🏁 [COMPLETE] Gallery materialized in: {args.output_root}")


if __name__ == "__main__":
    main()
