import polars as pl
from typing import Dict, Any, List
from viz_factory.registry import get_plot_function


def render_group_plots(group_config: Dict[str, Any], dataframe: pl.DataFrame) -> List[Any]:
    """
    Takes a 'group' from the YAML (e.g., Example_Group) 
    and returns a list of figures by calling registered factory functions.
    """
    figures = []

    # Get the 'plots' dictionary from the group config
    plots_config = group_config.get('plots', {})

    for plot_name, plot_meta in plots_config.items():
        # Get factory_id, which identifies the @register_plot function
        fid = plot_meta.get('factory_id')
        if not fid:
            print(f"Plot '{plot_name}' is missing a 'factory_id'. Skipping.")
            continue

        try:
            # 1. Fetch the correct function from the Python Registry
            plot_func = get_plot_function(fid)

            # 2. Apply it to get the figure (Plotnine or other)
            fig = plot_func(dataframe, plot_meta)
            figures.append(fig)
        except Exception as e:
            # For prototype, we log but don't break the entire dashboard
            print(
                f"Error rendering plot '{plot_name}' with factory '{fid}': {e}")
            import traceback
            traceback.print_exc()

    return figures


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(
        description="Manual execution hook for testing.")
    parser.add_argument("--test", action="store_true", help="Run in test mode")
    args = parser.parse_args()
    if args.test:
        print(f"Executing {__file__} in test mode.")
