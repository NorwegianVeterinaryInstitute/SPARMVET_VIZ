#!/usr/bin/env python
"""
normalize_manifest_fields.py (app/assets/)
------------------------------------------
Utility to convert legacy {column: type} dict-format `input_fields` /
`output_fields` entries in a SPARMVET YAML manifest to the standard list format:

  Standard format: [{name: col, dtype: type, description: ""}]

Importable API (used by Blueprint Architect UI):
    from app.assets.normalize_manifest_fields import normalize_file
    changes, success, message = normalize_file(Path("path/to/file.yaml"), write=True)

CLI Usage:
    ./.venv/bin/python app/assets/normalize_manifest_fields.py \
        --manifest path/to/file.yaml [--write] [--no-backup]
"""
import argparse
import shutil
import sys
from pathlib import Path

import yaml


# ── Core Logic (importable) ───────────────────────────────────────────────────

def _normalize_fields(fields):
    """
    Converts a fields value to the standard list-of-dicts format.
    Accepts:
      - dict  {col: type}              → [{name, dtype, description}]
      - list  [str, ...]               → [{name, dtype="?", description}]
      - list  [{name, dtype, ...}, ...] → unchanged (already standard)
    Returns (normalized_list, was_changed: bool).
    """
    if isinstance(fields, dict):
        normalized = [
            {"name": k, "dtype": str(v), "description": ""}
            for k, v in fields.items()
        ]
        return normalized, True

    if isinstance(fields, list):
        changed = False
        out = []
        for item in fields:
            if isinstance(item, dict):
                entry = {
                    "name": item.get("name", item.get("field", "?")),
                    "dtype": item.get("dtype", item.get("type", "?")),
                    "description": item.get("description", ""),
                }
                if entry != item:
                    changed = True
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
    Recursively walks a parsed YAML structure and normalises any
    input_fields / output_fields entries.
    Returns (obj, changes: list[str]).
    """
    changes = []

    if isinstance(obj, dict):
        for key, val in obj.items():
            if key in ("input_fields", "output_fields"):
                normalized, changed = _normalize_fields(val)
                if changed:
                    changes.append(
                        f"  [{path}.{key}]: converted to standard list format")
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


def normalize_file(manifest_path: Path, write: bool = False,
                   backup: bool = True) -> tuple:
    """
    Programmatic API entry point.

    Parameters
    ----------
    manifest_path : Path
        Absolute path to the YAML file to inspect (and optionally update).
    write : bool
        If True, write the normalized content back to disk.
    backup : bool
        If True (and write=True), save a .bak copy before overwriting.

    Returns
    -------
    (changes: list[str], success: bool, message: str)
    """
    if not manifest_path.exists():
        return [], False, f"File not found: {manifest_path}"

    try:
        raw = manifest_path.read_text(encoding="utf-8")
        data = yaml.safe_load(raw)
    except Exception as e:
        return [], False, f"YAML parse error: {e}"

    normalized_data, changes = _walk_and_normalize(data)

    if not changes:
        return [], True, "Already in standard format — no changes needed."

    if not write:
        summary = f"Dry-run: {len(changes)} field block(s) would be converted."
        return changes, True, summary

    # Write with optional backup
    if backup:
        bak = manifest_path.with_suffix(".yaml.bak")
        shutil.copy2(manifest_path, bak)

    out_yaml = yaml.dump(normalized_data, default_flow_style=False,
                         sort_keys=False, allow_unicode=True)
    manifest_path.write_text(out_yaml, encoding="utf-8")
    msg = (f"Normalized {len(changes)} field block(s) and saved to "
           f"'{manifest_path.name}'.")
    if backup:
        msg += " (.bak backup created)"
    return changes, True, msg


# ── CLI ───────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("--manifest", required=True,
                        help="Path to the YAML file to inspect / normalize.")
    parser.add_argument("--write", action="store_true", default=False,
                        help="Write normalized content back to disk (default: dry-run).")
    parser.add_argument("--no-backup", action="store_true", default=False,
                        help="Skip creating a .bak backup before writing.")
    args = parser.parse_args()

    path = Path(args.manifest)
    changes, success, message = normalize_file(
        path, write=args.write, backup=not args.no_backup)

    if not success:
        print(f"ERROR: {message}", file=sys.stderr)
        sys.exit(1)

    if changes:
        print(
            f"🔍 Found {len(changes)} field block(s) requiring normalization:")
        for c in changes:
            print(c)
        print()
    print(message)


if __name__ == "__main__":
    main()
