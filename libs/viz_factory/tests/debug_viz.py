import polars as pl
import argparse
from viz_factory import VizFactory
import os


def main():
    parser = argparse.ArgumentParser(
        description="Artist Pillar Debugging Tool.")
    parser.add_argument(
        "--output", type=str, default="tmp/USER_debug_plot.png", help="Path to output plot.")
    args = parser.parse_args()

    # 1. Generate Dummy Data (ST22-like)
    data = {
        "Sample": ["S1", "S2", "S3", "S4", "S5", "S6"],
        "ST": ["ST22", "ST22", "ST22", "ST11", "ST11", "ST11"],
        "Identity": [98.5, 99.2, 97.8, 95.1, 96.4, 95.8],
        "Gene": ["geneA", "geneA", "geneA", "geneA", "geneA", "geneA"]
    }
    df = pl.DataFrame(data).lazy()

    # 2. Draft Test Manifest
    # Follows the vision: Dictionary-for-Names, List-for-Layers
    manifest = {
        "plots": {
            "test_boxplot": {
                "mapping": {"x": "ST", "y": "Identity", "fill": "ST"},
                "layers": [
                    {"name": "geom_boxplot", "params": {}},
                    {"name": "theme_minimal", "params": {}}
                ]
            }
        }
    }

    # 3. Call VizFactory
    # Logic: accept (dataframe, manifest_dict, plot_id)
    factory = VizFactory()
    p = factory.render(df, manifest, "test_boxplot")

    # 4. Materialization (Evidence Generation - Follow rules_behavior.md)
    os.makedirs(os.path.dirname(args.output), exist_ok=True)
    p.save(args.output, width=10, height=6, dpi=100)

    print(
        f"Plot is ready in `{args.output}`. Please open the image to verify. Waiting for @verify.")
    print("DataFrame Glimpse:")
    df.collect().glimpse()


if __name__ == "__main__":
    main()
