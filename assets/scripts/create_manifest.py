#!/usr/bin/env python3
import argparse
import polars as pl
import yaml
from pathlib import Path
from datetime import datetime
import sys
from typing import Any


def map_dtype_to_schema(dtype):
    """Maps a Polars dtype to the dashboard schema definitions."""
    if dtype in [pl.Int8, pl.Int16, pl.Int32, pl.Int64,
                 pl.Float32, pl.Float64, pl.UInt8, pl.UInt16, pl.UInt32, pl.UInt64]:
        return "numeric"
    elif dtype in [pl.Date, pl.Datetime, pl.Time]:
        return "date"
    elif dtype in [pl.Boolean]:
        return "boolean"
    else:
        # For String/Utf8, Categorical, Object, etc.
        return "categorical"


def scaffold_schema(df, primary_key=None, is_metadata=False):
    """Generates the schema dictionary from a dataframe."""
    schema = {}

    # If it's the metadata section, the top level might be required_id_column or similar,
    # but the instructions say they are listed under metadata_schema.
    # However, based on the implementation plan, metadata_schema looks like:
    # metadata_schema:
    #   isolate_id: { type: "character", label: "Isolate ID", is_primary_key: true }
    #   ...

    for col in df.columns:
        col_type = map_dtype_to_schema(df[col].dtype)

        # Build field dict
        field_dict: dict[str, Any] = {
            "type": col_type,
            "label": str(col).replace('_', ' ').title()
        }

        if col == primary_key:
            field_dict["is_primary_key"] = True

        if col_type == "date":
            field_dict["format"] = "%Y-%m-%d"  # Default guess

        if is_metadata and col != primary_key:
            # Just an example of marking something optional
            field_dict["mandatory"] = False

        schema[col] = field_dict

    return schema


def main():
    parser = argparse.ArgumentParser(
        description="Scaffold a deployment manifest from a dataset.")
    parser.add_argument("--data_file", required=True,
                        help="Path to main data file.")
    parser.add_argument("--metadata_file", required=False,
                        help="Path to metadata file.")
    parser.add_argument("--primary_key_data", required=True,
                        help="Primary key column for main data.")
    parser.add_argument("--primary_key_metadata", required=False,
                        help="Primary key column for metadata.")
    args = parser.parse_args()

    # Define output directory
    out_dir = Path("assets/template_manifests")
    out_dir.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    out_file = out_dir / f"template_{timestamp}.yaml"

    try:
        df_data = pl.read_csv(
            args.data_file, separator='\t' if args.data_file.endswith('.tsv') else ',')
    except Exception as e:
        print(f"Error reading main data: {e}")
        sys.exit(1)

    # 1. Base Headers
    manifest: dict[str, Any] = {
        "id": "example_species_template",
        "type": "species",
        "info": {
            "display_name": "Example Species",
            "category": "Auto-generated",
            "tags": ["template", "draft"],
            "description": f"Template manifest generated from {Path(args.data_file).name}.",
            "version": "1.0"
        }
    }

    # 2. Main Data Schema (Nested under data_schemas)
    if args.primary_key_data not in df_data.columns:
        print(
            f"Warning: Primary key '{args.primary_key_data}' not found in data columns!")

    manifest["data_schemas"] = {
        "dataset_1": scaffold_schema(
            df_data, primary_key=args.primary_key_data, is_metadata=False)
    }

    # 3. Metadata Schema (optional)
    if args.metadata_file and args.primary_key_metadata:
        try:
            df_meta = pl.read_csv(
                args.metadata_file, separator='\t' if args.metadata_file.endswith('.tsv') else ',')
            if args.primary_key_metadata not in df_meta.columns:
                print(
                    f"Warning: Primary key '{args.primary_key_metadata}' not found in metadata columns!")
            manifest["metadata_schema"] = scaffold_schema(
                df_meta, primary_key=args.primary_key_metadata, is_metadata=True)
        except Exception as e:
            print(f"Error reading metadata: {e}")

    # 4. Standard Plot Archetypes Placeholder
    manifest["plot_defaults"] = {
        "height": 450,
        "theme": "theme_minimal",
        "show_legend": True
    }

    manifest["analysis_groups"] = {
        "Example_Group": {
            "description": "Auto-scaffolded plotting group",
            "plots": {
                "demo_bar": {
                    "factory_id": "bar_logic",
                    "target_dataset": "dataset_1",  # Explicit dataset target
                    "target_col": "Replace_Me",
                    "title": "Replace Me Title"
                }
            }
        }
    }

    # Write to file
    with open(out_file, 'w') as f:
        yaml.dump(manifest, f, sort_keys=False, default_flow_style=False)

    print(f"Successfully generated scaffold manifest: {out_file}")
    print("Please review and manually align plotting logic keys before moving to config/manifests/species/")


if __name__ == "__main__":
    main()
