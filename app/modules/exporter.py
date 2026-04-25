# app/modules/exporter.py
# @deps
# provides: class:SubmissionExporter, function:generate_methods_text, function:render_audit_report
# consumed_by: app/handlers/gallery_handlers.py, app/src/server.py, app/handlers/home_theater.py
# doc: .antigravity/knowledge/architecture_decisions.md#ADR-033, .agents/rules/ui_implementation_contract.md#12f
# @end_deps
import zipfile
import pandas as pd
import yaml
import subprocess
from pathlib import Path
from datetime import datetime


class SubmissionExporter:
    """Handles the creation of the SPARMVET Submission Package (.zip)."""

    def __init__(self, export_dir: str = "tmp/exports"):
        self.export_dir = Path(export_dir)
        self.export_dir.mkdir(parents=True, exist_ok=True)

    def create_audit_log(self, narrative: list, project_id: str = "ABROMICS_DEMO") -> str:
        """Converts the narrative log into a human-readable audit trace via Pandoc."""
        ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        md_path = self.export_dir / "audit_log.md"
        txt_path = self.export_dir / "audit_log.txt"

        # 1. Draft the Markdown trace
        with open(md_path, "w") as f:
            f.write(f"# SPARMVET AUDIT LOG: {project_id}\n")
            f.write(f"Generated: {ts}\n\n")
            f.write("## 📜 Narrative Trace (ADR-026)\n")
            for entry in narrative:
                f.write(f"- {entry}\n")

        # 2. Convert to Text/Docx via Pandoc
        try:
            subprocess.run(["pandoc", str(md_path), "-o",
                           str(txt_path)], check=True)
            return str(txt_path)
        except Exception:
            return str(md_path)  # Fallback to markdown if pandoc fails

    def bundle_package(self, plot_path: str, data_df: pd.DataFrame, manifest: dict, audit_trail: list) -> str:
        """Creates the final .zip Submission Package."""
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        zip_path = self.export_dir / f"submission_{ts}.zip"

        # 1. Prep individual files
        audit_path = self.create_audit_log(audit_trail)
        data_path = self.export_dir / "data_subset.csv"
        data_df.to_csv(data_path, index=False)

        manifest_path = self.export_dir / "active_recipe.yaml"
        with open(manifest_path, "w") as f:
            yaml.dump(manifest, f)

        # 2. Build the Zip
        with zipfile.ZipFile(zip_path, 'w') as zipf:
            zipf.write(audit_path, arcname="audit_log.txt")
            zipf.write(data_path, arcname="data_subset.csv")
            zipf.write(manifest_path, arcname="active_recipe.yaml")
            if plot_path and Path(plot_path).exists():
                zipf.write(plot_path, arcname="high_dpi_plot.png")

        return str(zip_path)

    def bundle_global_export(self, project_id: str, plot_path: str, tiers: dict, manifest: dict, audit_trail: list) -> str:
        """
        Bundles the full session state (Phase 14-C).
        Format: SPARMVET_EXPORT_{ISO_DATE}_{PROJECT_ID}.zip
        """
        iso_date = datetime.now().strftime("%Y-%m-%d")
        zip_name = f"SPARMVET_EXPORT_{iso_date}_{project_id}.zip"
        zip_path = self.export_dir / zip_name

        # 1. Prep individual files
        audit_path = self.create_audit_log(audit_trail, project_id)

        with zipfile.ZipFile(zip_path, 'w') as zipf:
            zipf.write(audit_path, arcname="audit_log.txt")

            # YAML Manifest
            manifest_path = self.export_dir / "session_manifest.yaml"
            with open(manifest_path, "w") as f:
                yaml.dump(manifest, f)
            zipf.write(manifest_path, arcname="session_manifest.yaml")

            # Tiers 1-3 Data
            for tier_name, df in tiers.items():
                if df is not None:
                    t_path = self.export_dir / f"{tier_name}.csv"
                    df.to_csv(t_path, index=False)
                    zipf.write(t_path, arcname=f"data/{tier_name}.csv")

            # Plot
            if plot_path and Path(plot_path).exists():
                zipf.write(plot_path, arcname="preview_plot.png")

            # Educational Metadata Template (ADR-033/Phase 14-C)
            meta_template = f"""# Recipe Metadata: {project_id}
## Family (Purpose): [Distribution | Correlation | Comparison | Ranking]
## Data Pattern: [1 Numeric | 2 Numeric | 1 Numeric, 1 Categorical]
## Difficulty: [Simple | Intermediate | Advanced]

## Suitability
- [Describe when this visualization is most useful]

## Data Schema (Tier 1)
- [List required columns and types]

## Transformation Logic (Tier 2)
- [Describe essential reshapes]

## Interpretations
- [Assumptions, limitations, and comments]

## Inspiration & Resources
- [Link to community resource or R Graph Gallery](https://r-graph-gallery.com/)
"""
            meta_path = self.export_dir / "recipe_meta.md"
            with open(meta_path, "w") as f:
                f.write(meta_template)
            zipf.write(meta_path, arcname="recipe_meta.md")

        return str(zip_path)


# ---------------------------------------------------------------------------
# Phase 22-E: Audit Report generation (§12f)
# ---------------------------------------------------------------------------

def generate_methods_text(t3_recipe: list) -> tuple:
    """Convert active T3 RecipeNodes into plain-English Methods lines.

    Returns:
        (methods_lines, discarded_nodes)
        methods_lines  — list of strings for active nodes only
        discarded_nodes — list of node dicts with active=False
    """
    methods: list = []
    discarded: list = []

    for node in t3_recipe:
        p = node.get("params", {})
        nt = node.get("node_type", "")
        reason = node.get("reason", "—")
        scope = node.get("plot_scope", "__all__")
        scope_str = f" (plot: {scope})" if scope != "__all__" else ""

        if not node.get("active", True):
            discarded.append(node)
            continue

        if nt == "filter_row":
            col = p.get("column", "?")
            op = p.get("op", "?")
            val = p.get("value", "?")
            methods.append(
                f"Rows were filtered to include only `{col}` {op} `{val}`{scope_str}. "
                f"Reason: {reason}."
            )
        elif nt == "exclusion_row":
            col = p.get("column", "?")
            val = p.get("value", "?")
            methods.append(
                f"The following `{col}` values were explicitly excluded: `{val}`{scope_str}. "
                f"Reason: {reason}."
            )
        elif nt == "drop_column":
            col = p.get("column", "?")
            methods.append(
                f"Column `{col}` was permanently removed from the exported dataset{scope_str}. "
                f"Reason: {reason}."
            )
        elif nt == "aesthetic_override":
            keys = [k for k in ("fill", "colour", "alpha", "shape") if k in p]
            methods.append(
                f"Plot aesthetics were adjusted for {scope}: {', '.join(keys) or 'overrides'}."
            )
        elif nt == "developer_raw_yaml":
            methods.append(
                f"A custom manifest fragment was applied{scope_str}. "
                f"Reason: {reason}."
            )

    return methods, discarded


def render_audit_report(
    home_state: dict,
    session_key: str,
    output_dir,
    manifest_id: str = "",
    deployment_profile: str = "local",
    figure_paths=None,
    dataset_summaries=None,
):
    """Render the Quarto HTML audit report into output_dir.

    Returns path to the rendered HTML file, or the .qmd if Quarto is unavailable.

    figure_paths: list of {plot_id, title, path}
    dataset_summaries: list of {id, path, n_rows}
    """
    import json
    import hashlib
    from datetime import datetime, timezone

    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    t3_recipe = home_state.get("t3_recipe", [])
    manifest_sha256 = home_state.get("manifest_sha256") or ""
    tier_toggle = home_state.get("tier_toggle", "T2")

    active_recipe = [n for n in t3_recipe if n.get("active", True)]
    t3_recipe_sha256 = hashlib.sha256(
        json.dumps(active_recipe, sort_keys=True).encode()
    ).hexdigest()

    methods_lines, discarded_nodes = generate_methods_text(t3_recipe)
    now = datetime.now(timezone.utc)
    export_ts = now.strftime("%Y-%m-%dT%H:%M:%S")
    date_str = now.strftime("%Y-%m-%d")

    report_data = {
        "manifest_id": manifest_id,
        "manifest_sha256": manifest_sha256,
        "t3_recipe_sha256": t3_recipe_sha256,
        "session_key": session_key,
        "tier_toggle": tier_toggle,
        "methods_text": methods_lines,
        "discarded_nodes": discarded_nodes,
        "active_recipe": active_recipe,
        "figures": figure_paths or [],
        "datasets": dataset_summaries or [],
    }
    (output_dir / "report_data.json").write_text(json.dumps(report_data, indent=2))

    template_path = Path(__file__).parent.parent / "assets" / "report_template.qmd"
    if not template_path.exists():
        template_path = Path("app/assets/report_template.qmd")

    template = template_path.read_text() if template_path.exists() else _FALLBACK_TEMPLATE
    filled = template
    for key, val in {
        "{{date}}": date_str,
        "{{manifest_id}}": manifest_id or "—",
        "{{manifest_sha256}}": (manifest_sha256[:16] + "…") if manifest_sha256 else "—",
        "{{t3_recipe_sha256}}": t3_recipe_sha256[:16] + "…",
        "{{deployment_profile}}": deployment_profile,
        "{{export_timestamp}}": export_ts,
    }.items():
        filled = filled.replace(key, val)

    qmd_path = output_dir / "report.qmd"
    qmd_path.write_text(filled)

    html_path = output_dir / "report.html"
    try:
        result = subprocess.run(
            ["quarto", "render", str(qmd_path), "--output", str(html_path)],
            capture_output=True, text=True, timeout=120,
        )
        if result.returncode == 0 and html_path.exists():
            return html_path
    except Exception:
        pass

    return qmd_path


def pandoc_convert(html_path, fmt: str = "docx"):
    """Convert a rendered HTML report to DOCX or PDF via Pandoc.

    Returns output path, or None if Pandoc is unavailable.
    fmt: "docx" | "pdf"
    """
    import shutil as _shutil
    html_path = Path(html_path)
    if _shutil.which("pandoc") is None:
        return None
    out_path = html_path.with_suffix(f".{fmt}")
    try:
        result = subprocess.run(
            ["pandoc", str(html_path), "-o", str(out_path)],
            capture_output=True, text=True, timeout=120,
        )
        if result.returncode == 0 and out_path.exists():
            return out_path
    except Exception:
        pass
    return None


def pandoc_available() -> bool:
    import shutil as _shutil
    return _shutil.which("pandoc") is not None


_FALLBACK_TEMPLATE = """---
title: "SPARMVET Audit Report"
date: "{{date}}"
---

## Study Context

Manifest: {{manifest_id}} | SHA256: {{manifest_sha256}}
Exported: {{export_timestamp}}

## Methods

*(Quarto template not found — see report_data.json for full detail)*
"""
