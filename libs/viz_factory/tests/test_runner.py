from viz_factory import VizFactory
import polars as pl
import yaml
import argparse
import os
import matplotlib
matplotlib.use('Agg')


def main():
    print("TEST_RUNNER_START")
    parser = argparse.ArgumentParser(
        description="Unified Artist Pillar Test Runner.")
    parser.add_argument("manifest_path", type=str,
                        help="Path to the test manifest (.yaml).")
    parser.add_argument("--plot_id", type=str, default=None,
                        help="Optional Plot ID to render. Defaults to first found.")
    args = parser.parse_args()

    # 1. Load Manifest
    if not os.path.exists(args.manifest_path):
        raise FileNotFoundError(f"Manifest not found: {args.manifest_path}")

    with open(args.manifest_path, "r") as f:
        manifest = yaml.safe_load(f)

    # 2. Extract Metadata & Data Path (Data-Manifest Coupling)
    data_path = manifest.get("data_path")
    if not data_path:
        raise ValueError("Manifest MUST include a 'data_path' key.")

    # Resolve relative data_path based on manifest location
    manifest_dir = os.path.dirname(os.path.abspath(args.manifest_path))
    abs_data_path = os.path.abspath(os.path.join(manifest_dir, data_path))

    # 3. Load Data (Lazy for ADR-010)
    # We assume TSV as per the 'Artist Law' triplet definition.
    df = pl.scan_csv(abs_data_path, separator="\t")

    # 4. Resolve Plot ID
    if not args.plot_id:
        # Default to the first plot key in 'plots'
        plots = manifest.get("plots", {})
        if not plots:
            raise ValueError("Manifest must contain a 'plots' entry.")
        args.plot_id = list(plots.keys())[0]

    # 5. Render via VizFactory
    factory = VizFactory()
    p = factory.render(df, manifest, args.plot_id)

    # 6. Materialize Artifact (tmp/USER_debug_{component}.png)
    component_name = os.path.basename(
        args.manifest_path).replace("_test.yaml", "")
    output_path = f"tmp/USER_debug_{component_name}.png"
    os.makedirs("tmp", exist_ok=True)

    p.save(output_path, width=8, height=6, dpi=100)

    print(f"Artifact ready in: {output_path}")
    print(f"Applied Manifest: {args.manifest_path}")


if __name__ == "__main__":
    main()
