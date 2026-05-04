"""debug_output.py — output directory routing for debug runner scripts.

Debug scripts write to tmpAI/YYYY-MM-DD/[label]/ rather than flat tmp/ so
artifacts are date-organised and easy to clean by date.

Usage in a debug script:
    from utils.debug_output import get_debug_out_dir
    out_dir = get_debug_out_dir("assembler")
    # → <project_root>/tmpAI/2026-05-03/assembler/
"""
from datetime import date
from pathlib import Path

# Resolve project root: libs/utils/src/utils/ → up 4 levels
_PROJECT_ROOT = Path(__file__).resolve().parents[4]


def get_debug_out_dir(label: str = "", root: Path | None = None) -> Path:
    """Return a date-stamped scratch directory for debug runner output.

    Creates: <project_root>/tmpAI/YYYY-MM-DD/[label]/

    Args:
        label: subdirectory name within the date dir (e.g. "assembler", "gallery").
               If empty, returns the bare date directory.
        root:  override project root (useful in tests).

    Returns:
        Path that exists on disk.
    """
    base = (root if root is not None else _PROJECT_ROOT) / "tmpAI" / date.today().isoformat()
    out = base / label if label else base
    out.mkdir(parents=True, exist_ok=True)
    return out
