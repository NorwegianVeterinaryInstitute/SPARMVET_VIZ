from libs.utils.src.config_loader import ConfigManager
import sys
import argparse
from pathlib import Path

# Automatically resolve the root directory relative to this script's location
# libs/utils/tests/test_config_loader.py -> parents[3] is the project root
root_dir = Path(__file__).resolve().parents[3]
# STRICT BAN: sys.path.append / sys.path.insert are explicitly forbidden. Rely on pip install -e.


def test_config_loader(yaml_path):
    print("Testing ConfigManager with !include support...")
    test_yaml_path = Path(yaml_path)

    try:
        manager = ConfigManager(test_yaml_path)
        print(f"\nSuccessfully loaded master file: {test_yaml_path.name}\n")

        # Test 1: Can we get the full stitched data_schemas?
        schemas = manager.get_data_schemas()
        print(f"Loaded {len(schemas)} data schemas:")
        for name, config in schemas.items():
            input_fields = config.get(
                "input_fields") or config.get("fields") or {}
            output_fields = config.get("output_fields") or {}
            wrangling = config.get("wrangling") or []
            print(f"  - {name}:")
            print(f"    └── {len(input_fields)} input fields defined")
            print(f"    └── {len(output_fields)} output fields defined")
            print(f"    └── {len(wrangling)} wrangling actions defined")

        # Test 2: Can we get the stitched metadata_schema?
        meta = manager.get_metadata_rules()
        meta_input_fields = meta.get(
            "input_fields") or meta.get("fields") or {}
        meta_output_fields = meta.get("output_fields") or {}
        meta_wrangling = meta.get("wrangling") or []
        print(f"\nLoaded metadata schema:")
        print(f"  └── {len(meta_input_fields)} input fields defined")
        print(f"  └── {len(meta_output_fields)} output fields defined")
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

    test_config_loader(args.yaml)
