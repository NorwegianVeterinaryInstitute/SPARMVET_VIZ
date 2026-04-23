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
locates materialized data (written by debug_assembler.py), and renders PNG files.

Data lookup priority:
  1. tmp/EVE_assembly_{target_dataset}.parquet  — debug_assembler.py output (default)
  2. --data_root override                        — explicit path prefix
"""


def resolve_data_path(target_dataset: str, data_root: Path) -> Path | None:
    """Locate materialized parquet for a target dataset."""
    # Primary: debug assembler output (parquet)
    candidate = data_root / f"EVE_assembly_{target_dataset}.parquet"
    if candidate.exists():
        return candidate
    # Legacy fallback: TSV (kept for backward compat with old debug output)
    candidate_tsv = data_root / f"EVE_assembly_{target_dataset}.tsv"
    if candidate_tsv.exists():
        return candidate_tsv
    return None


def main():
    parser = argparse.ArgumentParser(
        description="Materialize all plots from a manifest into PNGs (headless art audit).")
    parser.add_argument("--manifest", type=str, required=True,
                        help="Path to the master manifest (.yaml)")
    parser.add_argument("--output_root", type=str,
                        default="tmp/materialized_gallery", help="Directory to save PNGs")
    parser.add_argument("--data_root", type=str, default="tmp",
                        help="Root directory containing EVE_assembly_*.parquet files (default: tmp/)")
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
    data_root = Path(args.data_root)

    # Iterate through Analysis Groups
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

            data_path = resolve_data_path(target_dataset, data_root)

            if not data_path:
                print(
                    f"  └── ❌ [FAIL] {plot_id}: No materialized data for '{target_dataset}' in {data_root}. "
                    f"Run debug_assembler.py first.")
                continue

            print(f"  └── 🖌️ [RENDER] {plot_id} via {data_path.name}...")

            try:
                if data_path.suffix == ".parquet":
                    lf = pl.scan_parquet(data_path)
                else:
                    lf = pl.scan_csv(data_path, separator="\t",
                                     null_values=["-", "n/a", "NA", "null"])
                p = factory.render(lf, {"plots": {plot_id: spec}}, plot_id)

                output_path = group_dir / f"{plot_id}.png"
                p.save(output_path, width=10, height=6, dpi=150, verbose=False)
                print(f"      ✅ [DONE] Saved to {output_path}")
            except Exception as e:
                print(f"      ❌ [ERROR] {plot_id}: {e}")

    print(f"\n🏁 [COMPLETE] Gallery materialized in: {args.output_root}")


if __name__ == "__main__":
    main()
