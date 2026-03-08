from libs.utils.src.loader2 import ConfigManager
import sys
from pathlib import Path

# Add the libs to the python path
root_dir = Path(
    "/home/evezeyl/Documents/Insync/gdrive/OBSWORK/20_GITS/SPARMVET_VIZ")
sys.path.append(str(root_dir))


def test_loader():
    print("Testing ConfigManager with !include support...")
    test_yaml_path = root_dir / "assets/template_manifests/1_test_data_ST22_dummy.yaml"

    try:
        manager = ConfigManager(test_yaml_path)
        print(f"\nSuccessfully loaded master file: {test_yaml_path.name}\n")

        # Test 1: Can we get the full stitched data_schemas?
        schemas = manager.get_data_schemas()
        print(f"Loaded {len(schemas)} data schemas:")
        for name, fields in schemas.items():
            print(f"  - {name} ({len(fields)} fields)")

        # Test 2: Can we get the stitched metadata_schema?
        meta = manager.get_metadata_rules()
        print(f"\nLoaded metadata schema with {len(meta)} fields:")
        for name in meta.keys():
            print(f"  - {name}")

        # Test 3: Can we get a plot config?
        plot_cfg = manager.get_plot_config("Example_Group", "demo_bar")
        print("\nLoaded Plot Config (merged with defaults):")
        for k, v in plot_cfg.items():
            print(f"  - {k}: {v}")

        print("\nAll tests passed successfully! The !include logic works beautifully.")

    except Exception as e:
        print(f"\nERROR loading configuration: {e}")


if __name__ == "__main__":
    test_loader()
