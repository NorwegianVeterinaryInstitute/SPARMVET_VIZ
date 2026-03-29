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
    df = pl.scan_csv(abs_data_path, separator="\t", try_parse_dates=True)

    # 4. Resolve Plot ID
    if not args.plot_id:
        # Default to the first plot key in 'plots'
        plots = manifest.get("plots", {})
        if not plots:
            raise ValueError("Manifest must contain a 'plots' entry.")
        args.plot_id = list(plots.keys())[0]

    # 5. Render via VizFactory
    factory = VizFactory()
    plot_config = manifest.get("plots", {}).get(args.plot_id)
    os.makedirs("tmp", exist_ok=True)
    component_name = os.path.basename(
        args.manifest_path).replace("_test.yaml", "")
    output_path = f"tmp/USER_debug_{component_name}.png"

    if plot_config.get("comparison"):
        from PIL import Image
        import copy
        from plotnine import labs

        # 1. Render DEFAULT (Force baseline position for comparison baseline)
        print(f"DEBUG: Plot config: {plot_config}")
        default_manifest = copy.deepcopy(manifest)
        layers_spec = default_manifest["plots"][args.plot_id].get("layers", [])

        # User can specify 'comparison_baseline' in the plot spec, defaults to 'identity'
        baseline_pos = plot_config.get("comparison_baseline", "identity")

        default_layers = []
        for l in layers_spec:
            if not l["name"].startswith("position_"):
                l_copy = copy.deepcopy(l)
                # Only force baseline for GEOM layers
                if l["name"].startswith("geom_"):
                    if "params" not in l_copy:
                        l_copy["params"] = {}
                    l_copy["params"]["position"] = baseline_pos
                default_layers.append(l_copy)

        default_manifest["plots"][args.plot_id]["layers"] = default_layers

        # Render and save default
        p_default = factory.render(df, default_manifest, args.plot_id)
        p_default = p_default + \
            labs(title=f"[DEFAULT: {baseline_pos.upper()} POSITION]")
        default_tmp = output_path.replace(".png", "_default_tmp.png")
        p_default.save(default_tmp, width=8, height=6, dpi=100)

        # 2. Render APPLIED
        p_applied = factory.render(df, manifest, args.plot_id)
        # Identify applied position for the title
        applied_pos = [l["name"]
                       for l in layers_spec if l["name"].startswith("position_")]
        pos_title = applied_pos[0] if applied_pos else "APPLIED"
        p_applied = p_applied + labs(title=f"[APPLIED: {pos_title}]")
        applied_tmp = output_path.replace(".png", "_applied_tmp.png")
        p_applied.save(applied_tmp, width=8, height=6, dpi=100)

        # 3. Concatenate using PIL
        img_def = Image.open(default_tmp)
        img_app = Image.open(applied_tmp)
        combined = Image.new(
            'RGB', (img_def.width + img_app.width, img_def.height), "white")
        combined.paste(img_def, (0, 0))
        combined.paste(img_app, (img_def.width, 0))
        combined.save(output_path)

        # Cleanup
        os.remove(default_tmp)
        os.remove(applied_tmp)
    else:
        # Standard Single Render
        p = factory.render(df, manifest, args.plot_id)
        p.save(output_path, width=8, height=6, dpi=100)

    print(f"Artifact ready in: {output_path}")
    print(f"Applied Manifest: {args.manifest_path}")


if __name__ == "__main__":
    main()
