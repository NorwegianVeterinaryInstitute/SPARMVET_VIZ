from libs.utils.src.loader2 import ConfigManager
import sys
import argparse
from pathlib import Path

# Automatically resolve the root directory relative to this script's location
# libs/utils/tests/test_loader.py -> parents[3] is the project root
root_dir = Path(__file__).resolve().parents[3]
sys.path.append(str(root_dir))


def test_loader(yaml_path):
    print("Testing ConfigManager with !include support...")
    test_yaml_path = Path(yaml_path)

    try:
        manager = ConfigManager(test_yaml_path)
        print(f"\nSuccessfully loaded master file: {test_yaml_path.name}\n")

        # Test 1: Can we get the full stitched data_schemas?
        schemas = manager.get_data_schemas()
        print(f"Loaded {len(schemas)} data schemas:")
        for name, config in schemas.items():
            fields = config.get("fields", {})
            wrangling = config.get("wrangling", [])
            print(f"  - {name}:")
            print(f"    └── {len(fields)} fields schemas defined")
            print(f"    └── {len(wrangling)} wrangling actions defined")

        # Test 2: Can we get the stitched metadata_schema?
        meta = manager.get_metadata_rules()
        meta_fields = meta.get("fields", {})
        meta_wrangling = meta.get("wrangling", [])
        print(f"\nLoaded metadata schema:")
        print(f"  └── {len(meta_fields)} fields schemas defined")
        print(f"  └── {len(meta_wrangling)} wrangling actions defined")

        # Test 3: Can we get a plot config?
        plot_cfg = manager.get_plot_config("Example_Group", "demo_bar")
        print("\nLoaded Plot Config (merged with defaults):")
        for k, v in plot_cfg.items():
            print(f"  - {k}: {v}")

        print("\nAll tests passed successfully! The !include logic works beautifully.")

    except Exception as e:
        print(f"\nERROR loading configuration: {e}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Test the YAML ConfigManager loading visually.")
    parser.add_argument("--yaml", required=True,
                        help="Path to the master YAML configuration file to test.")
    args = parser.parse_args()

    test_loader(args.yaml)
