#!/usr/bin/env python3
import argparse
import yaml
from pathlib import Path
import sys


def main():
    parser = argparse.ArgumentParser(
        description="Create a test deployment configuration file.")
    parser.add_argument("--data_file", required=True,
                        help="Path to the synthetic data TSV.")
    parser.add_argument("--metadata_file", required=False,
                        help="Path to the synthetic metadata TSV.")
    parser.add_argument("--deployment_file", required=True,
                        help="Filename for the desired deployment (e.g., local_test.yaml).")
    parser.add_argument("--manifest_id", required=True,
                        help="The ID of the specific species manifest to lock this deployment to (e.g., test_species).")
    parser.add_argument("--description", required=True,
                        help="A brief description of this test deployment deployment.")
    args = parser.parse_args()

    # Define output path
    out_dir = Path("config/deployments/test_deployments")
    out_dir.mkdir(parents=True, exist_ok=True)

    # Clean up the output filename if user provided a bare name
    out_name = args.deployment_file
    if not out_name.endswith(('.yaml', '.yml')):
        out_name += '.yaml'

    out_path = out_dir / out_name

    # Build the Deployment configuration
    deployment = {
        "id": out_path.stem.replace(" ", "_").lower(),
        "type": "pipeline_run",
        "target_connector": "local/file_upload",
        "info": {
            "display_name": "Local Automated Test Run",
            "description": args.description,
            "version": "1.0",
            "tags": ["test", "local", "auto-generated"]
        },
        "connector_params": {
            "data_file": args.data_file
        },
        "allowed_manifests": [f"species/{args.manifest_id}"]
    }

    if args.metadata_file:
        deployment["connector_params"]["metadata_file"] = args.metadata_file

    with open(out_path, 'w') as f:
        yaml.dump(deployment, f, sort_keys=False, default_flow_style=False)

    print(f"Successfully generated Test Deployment context: {out_path}")
    print(
        f"When the dashboard launches, it will read this config, load {args.data_file}, and apply the {args.manifest_id} rules.")


if __name__ == "__main__":
    main()
