#!/usr/bin/env python3
"""
debug_apply_manifest_standards.py
==================================
Enforces ADR-013 structure on VizFactory YAML manifests:
  - Adds the required header blocks (id, description, input_fields,
    wrangling, output_fields) if missing.

Usage:
    ./.venv/bin/python assets/scripts/debug_apply_manifest_standards.py
    ./.venv/bin/python assets/scripts/debug_apply_manifest_standards.py \\
        --test-dir libs/viz_factory/tests/test_data \\
        --dry-run
"""

import argparse
import glob
import os
from pathlib import Path


def parse_args():
    parser = argparse.ArgumentParser(
        description=(
            "SPARMVET_VIZ Manifest Standards Enforcer. "
            "Applies ADR-013 header structure to VizFactory YAML test manifests "
            "that are missing required blocks (id, description, input_fields, "
            "wrangling, output_fields)."
        )
    )
    parser.add_argument(
        "--test-dir",
        default="libs/viz_factory/tests/test_data",
        help="Directory with YAML manifests (default: libs/viz_factory/tests/test_data)",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print what would be changed without writing files.",
    )
    return parser.parse_args()


def main():
    args = parse_args()
    yamls = glob.glob(os.path.join(args.test_dir, "*.yaml"))

    patched = 0
    for y in yamls:
        with open(y, "r") as f:
            content = f.read()

        if "input_fields:" not in content:
            stem = Path(y).stem  # e.g. "geom_point_test"
            header = (
                f'id: "{stem}"\n'
                f'description: "Test manifest for {stem}"\n'
                f"input_fields: []\n"
                f"wrangling: []\n"
                f"output_fields: []\n"
            )
            new_content = header + content
            if args.dry_run:
                print(f"[DRY RUN] Would patch: {y}")
            else:
                with open(y, "w") as f:
                    f.write(new_content)
                print(f"[PATCHED] {y}")
            patched += 1

    print(f"\nApplied ADR-013 to {patched}/{len(yamls)} YAML manifests.")
    if args.dry_run:
        print("(Dry run — no files written.)")


if __name__ == "__main__":
    main()
