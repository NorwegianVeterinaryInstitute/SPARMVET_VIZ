#!/usr/bin/env python3
"""
materialize_manifest_plots.py — DEPRECATED SHIM

The canonical headless art audit tool is now:
  libs/viz_factory/tests/debug_gallery.py

This script is a thin forwarding shim kept for backward compatibility
with any documented commands. It delegates all work to debug_gallery.py.

Usage (preferred):
  .venv/bin/python libs/viz_factory/tests/debug_gallery.py --manifest <path>

Usage (legacy, via this shim):
  .venv/bin/python assets/scripts/materialize_manifest_plots.py --manifest <path>
"""
import sys
import subprocess
from pathlib import Path

project_root = Path(__file__).resolve().parent.parent.parent
gallery_script = project_root / "libs/viz_factory/tests/debug_gallery.py"

if not gallery_script.exists():
    print(f"❌ Cannot find debug_gallery.py at {gallery_script}")
    sys.exit(1)

print(f"⚠️  This script is a shim. Delegating to: {gallery_script}")
result = subprocess.run([sys.executable, str(gallery_script)] + sys.argv[1:])
sys.exit(result.returncode)
