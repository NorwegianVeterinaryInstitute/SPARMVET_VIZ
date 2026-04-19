#!/usr/bin/env python
"""
normalize_manifest_fields.py
----------------------------
Utility script to convert legacy {column: type} dict-format `input_fields` /
`output_fields` entries in a SPARMVET YAML manifest to the standard list format:

  Standard format: [{name: col, dtype: type, description: ""}]

Usage:
  ./.venv/bin/python assets/scripts/normalize_manifest_fields.py --manifest path/to/manifest.yaml
  ./.venv/bin/python assets/scripts/normalize_manifest_fields.py --manifest path/to/manifest.yaml --write

Options:
  --manifest   Path to the YAML manifest to inspect (required).
  --write      Write the normalized manifest back to disk (default: dry-run only).
  --backup     Keep a .bak copy of the original before writing (default: True).
  --no-backup  Skip creating a backup.
"""
import argparse
import sys
import shutil
from pathlib import Path

import yaml


# ── Helpers ───────────────────────────────────────────────────────────────────

def _normalize_fields(fields):
    """
    Converts a fields value to the standard list-of-dicts format.
    Accepts:
      - dict  {col: type}  → [{name, dtype, description}]
      - list  [{name, ...}] → unchanged (already standard)
    Returns (normalized_list, was_changed: bool).
    """
    if isinstance(fields, dict):
        normalized = [
            {"name": k, "dtype": str(v), "description": ""}
            for k, v in fields.items()
        ]
        return normalized, True

    if isinstance(fields, list):
        # Already list — ensure each item has the standard keys
        changed = False
        out = []
        for item in fields:
            if isinstance(item, dict):
                entry = {
                    "name": item.get("name", item.get("field", "?")),
                    "dtype": item.get("dtype", item.get("type", "?")),
                    "description": item.get("description", ""),
                }
                changed = changed or entry != item
                out.append(entry)
            else:
                # Scalar residual — wrap
                out.append(
                    {"name": str(item), "dtype": "?", "description": ""})
                changed = True
        return out, changed

    return fields, False


def _walk_and_normalize(obj, path="root"):
    """
    Recursively walks a parsed YAML dict and normalises any input_fields /
    output_fields entries. Returns (obj, changes: list[str]).
    """
    changes = []

    if isinstance(obj, dict):
        for key, val in obj.items():
            if key in ("input_fields", "output_fields"):
                normalized, changed = _normalize_fields(val)
                if changed:
                    changes.append(
                        f"  [{path}.{key}]: converted from dict/legacy to standard list")
                    obj[key] = normalized
            else:
                sub_obj, sub_changes = _walk_and_normalize(
                    val, path=f"{path}.{key}")
                obj[key] = sub_obj
                changes.extend(sub_changes)

    elif isinstance(obj, list):
        for i, item in enumerate(obj):
            sub_obj, sub_changes = _walk_and_normalize(
                item, path=f"{path}[{i}]")
            obj[i] = sub_obj
            changes.extend(sub_changes)

    return obj, changes


# ── CLI ───────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("--manifest", required=True,
                        help="Path to the YAML manifest to inspect / normalize.")
    parser.add_argument("--write", action="store_true", default=False,
                        help="Write the normalized manifest back to disk. (Default: dry-run)")
    parser.add_argument("--no-backup", action="store_true", default=False,
                        help="Skip creating a .bak backup before writing.")
    args = parser.parse_args()

    manifest_path = Path(args.manifest)
    if not manifest_path.exists():
        print(f"ERROR: Manifest not found: {manifest_path}", file=sys.stderr)
        sys.exit(1)

    raw = manifest_path.read_text(encoding="utf-8")
    try:
        data = yaml.safe_load(raw)
    except yaml.YAMLError as e:
        print(f"ERROR: Cannot parse YAML: {e}", file=sys.stderr)
        sys.exit(1)

    normalized_data, changes = _walk_and_normalize(data)

    if not changes:
        print(f"✅ No changes needed. All fields already in standard format.")
        print(f"   Manifest: {manifest_path}")
        sys.exit(0)

    print(f"🔍 Found {len(changes)} field(s) requiring normalization:")
    for c in changes:
        print(c)
    print()

    if not args.write:
        print("⚠️  Dry-run mode. No files were modified.")
        print("   Re-run with --write to apply changes.")
        sys.exit(0)

    # Backup
    if not args.no_backup:
        backup_path = manifest_path.with_suffix(".yaml.bak")
        shutil.copy2(manifest_path, backup_path)
        print(f"📦 Backup saved: {backup_path}")

    # Write
    out_yaml = yaml.dump(normalized_data, default_flow_style=False,
                         sort_keys=False, allow_unicode=True)
    manifest_path.write_text(out_yaml, encoding="utf-8")
    print(f"✅ Manifest normalized and saved: {manifest_path}")


if __name__ == "__main__":
    main()
