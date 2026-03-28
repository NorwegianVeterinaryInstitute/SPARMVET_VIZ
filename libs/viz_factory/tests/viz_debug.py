import polars as pl
import argparse
from pathlib import Path
import sys
import matplotlib.pyplot as plt

# Ensure viz_factory is in the path if not installed
project_root = Path(__file__).resolve().parent.parent.parent.parent
sys.path.append(str(project_root / "libs/viz_factory/src"))

try:
    from registry import get_plot_function
    import bar_logic  # Trigger registration
except ImportError:
    # If using absolute package imports
    try:
        from viz_factory.registry import get_plot_function
        from viz_factory import bar_logic
    except ImportError as e:
        print(f"❌ Error: Could not import viz_factory. {e}")
        sys.exit(1)


def main():
    parser = argparse.ArgumentParser(
        description="Debug script for Viz Factory logic verification.")
    parser.add_argument("--data", required=True, help="Path to assembly TSV.")
    parser.add_argument("--factory", default="bar_logic",
                        help="Plot factory ID.")
    parser.add_argument("--target_col", required=True, help="Column to plot.")
    parser.add_argument("--output", default="tmp/viz_demo.png",
                        help="Path to save plot PNG.")

    args = parser.parse_args()

    # 1. Load Data
    df = pl.read_csv(args.data, separator='\t')
    print(f"[1] LOADED DATA: {args.data} ({df.height} rows)")

    # 2. Get Plot Function
    try:
        plot_func = get_plot_function(args.factory)
    except Exception as e:
        print(f"❌ Error: {e}")
        return

    # 3. Generate Plot
    config = {
        "target_col": args.target_col,
        "title": f"Demo: {args.target_col} Distribution (High Integrity Data)"
    }

    print(f"[2] GENERATING PLOT: {args.factory} on {args.target_col}...")
    plot_obj = plot_func(df, config)

    # 4. Save
    print(f"[3] SAVING PLOT to {args.output}...")
    # Plotnine objects have a .save() method
    plot_obj.save(args.output, width=8, height=6,
                  dpi=100)  # Lower DPI for quick demo
    print(f"✅ SUCCESS: Plot materialized to {args.output}")


if __name__ == "__main__":
    main()
