import argparse
import polars as pl
import os
import yaml
from viz_factory.viz_factory import VizFactory


def main():
    parser = argparse.ArgumentParser(description="VizFactory Debug Runner")
    parser.add_argument(
        "--data", default="tmp/viz/test_data.tsv", help="Path to test TSV")
    parser.add_argument("--plot_id", default="species_box",
                        help="ID of plot in manifest")
    parser.add_argument(
        "--output", default="tmp/viz/test_plot.png", help="Output PNG path")
    args = parser.parse_args()

    # Define a sample manifest purely for this test
    manifest = {
        "plots": {
            "species_box": {
                "mapping": {"x": "Species", "y": "Value", "fill": "Species"},
                "layers": [
                    {"name": "geom_boxplot", "params": {
                        "outlier_shape": "NA", "alpha": 0.5}},
                    {"name": "theme_minimal", "params": {}}
                ]
            },
            "resistance_histogram": {
                "mapping": {"x": "Value", "fill": "Resistance"},
                "layers": [
                    {"name": "geom_histogram", "params": {
                        "bins": 10, "alpha": 0.7}},
                    {"name": "theme_bw", "params": {}}
                ]
            }
        }
    }

    print(f"Loading data from: {args.data}")
    # Load data as LazyFrame as requested
    lf = pl.scan_csv(args.data, separator="\t")

    print(f"Initializing VizFactory...")
    factory = VizFactory()

    print(f"Rendering plot: {args.plot_id}")
    plot = factory.render_plot(lf, manifest, args.plot_id)

    # Save to tmp/viz
    print(f"Saving plot to: {args.output}")
    os.makedirs(os.path.dirname(args.output), exist_ok=True)
    plot.save(args.output, width=8, height=6, dpi=100)
    print("Done!")


if __name__ == "__main__":
    main()
