"""app/handlers/export_handlers.py
Export pipeline: results bundle (.zip) + audit report (HTML/DOCX) +
system tools sidebar UI.

Extracted from home_theater.py in Phase 24-C (ADR-051).

Two-Category Law (ADR-045): this module contains @render.* / @reactive.*
decorators only. It MUST NOT be imported by non-Shiny contexts.
"""

from __future__ import annotations

# @deps
# provides: function:define_export_server, output:system_tools_ui, output:export_bundle_download, output:export_audit_report_ui, output:export_audit_report_download
# consumes: app/modules/exporter.py, app/modules/session_manager.py, libs/viz_factory/src/viz_factory/viz_factory.py, polars, shiny
# consumed_by: app/handlers/home_theater.py
# doc: .antigravity/knowledge/architecture_decisions.md#ADR-045, .antigravity/knowledge/architecture_decisions.md#ADR-051
# @end_deps

from pathlib import Path

import polars as pl
from shiny import reactive, render, ui

from app.modules.t3_recipe_engine import _op_label


def define_export_server(input, output, session, *,
                         bootloader, orchestrator, viz_factory,
                         current_persona, active_cfg,
                         tier1_anchor, tier_reference, tier3_leaf,
                         tier_toggle, applied_filters,
                         home_state, safe_input):
    """Register export-bundle + audit-report + system-tools handlers.

    Reactive deps (kwargs):
      bootloader      : Path Authority (ADR-031)
      orchestrator    : tier1/tier2 materialiser
      viz_factory     : plot renderer
      current_persona : reactive.Value[str]
      active_cfg      : reactive.Calc[ConfigManager]
      tier1_anchor    : reactive.Calc[LazyFrame]
      tier_reference  : reactive.Calc[LazyFrame | None]
      tier3_leaf      : reactive.Calc[DataFrame | None]
      tier_toggle     : reactive.Value[str]   ("T1"|"T2"|"T3")
      applied_filters : reactive.Value[list]
      home_state      : reactive.Value[dict] | None
      safe_input      : helper (input, key, default) → value
    """

    @output
    @render.ui
    def system_tools_ui():
        if not bootloader.is_enabled("export_bundle_enabled"):
            return ui.div()
        n_active = len(applied_filters.get())
        filter_warning = ui.div()
        if n_active:
            filter_warning = ui.tags.small(
                f"⚠ {n_active} active filter(s) — a note will be embedded in the bundle.",
                class_="text-warning d-block mb-1",
                style="font-size:0.7em;"
            )
        return ui.div(
            # ── Export Results Bundle ─────────────────────────────────────
            ui.div(
                ui.input_text(
                    "export_user_name", label="Bundle label / name",
                    placeholder="label (no spaces, no special characters)…",
                    value="",
                ),
                ui.input_radio_buttons(
                    "export_preset",
                    label="Quality",
                    choices={"web": "Web / Presentation", "publication": "Publication (≥600 DPI)"},
                    selected="web",
                    inline=False,
                ),
                ui.input_radio_buttons(
                    "export_plot_format",
                    label="Plot format",
                    choices={"png": "PNG", "svg": "SVG", "pdf": "PDF"},
                    selected="png",
                    inline=True,
                ),
                filter_warning,
                ui.download_button(
                    "export_bundle_download",
                    "📦 Export Bundle",
                    class_="btn-success btn-sm w-100 mt-1",
                ),
                class_="mb-2 px-2",
                style="font-size:0.8em;"
            ),
            # ── Export Audit Report (22-E) ────────────────────────────────
            ui.output_ui("export_audit_report_ui"),
        )

    @render.download(filename=lambda: _export_bundle_filename())
    async def export_bundle_download():
        """
        Phase 21-I: Export Results Bundle.

        Produces a zip file containing:
        - plots/          SVG (web preset) or high-DPI PNG (publication preset) per plot
        - data/           T1 TSV for each dataset referenced by active plots
        - recipes/        YAML wrangling recipe(s) for the active project
        - FILTERS.txt     If any applied_filters exist ("No Trace No Export" compliance note)
        - report.qmd      Quarto source report embedding all plots and datasets
        - README.txt      Bundle manifest (timestamp, project, persona, preset)
        """
        import io
        import zipfile
        import tempfile
        import datetime
        import shutil
        import csv
        import copy

        now = datetime.datetime.now()
        ts = now.strftime("%Y%m%d_%H%M%S")
        raw_name = safe_input(input, "export_user_name", "user").strip() or "user"
        # Sanitize: replace spaces/special chars with underscore, lowercase
        import re
        safe_name = re.sub(r"[^A-Za-z0-9_-]", "_", raw_name)[:40]
        preset = safe_input(input, "export_preset", "web")
        persona = current_persona.get()
        dpi = 300 if preset == "web" else 600

        cfg = active_cfg()
        proj_id = safe_input(input, "project_id", bootloader.get_default_project())
        groups = cfg.raw_config.get("analysis_groups", {})
        top_plots = cfg.raw_config.get("plots", {})
        active_filters = applied_filters.get()

        # Collect all (plot_id, spec) pairs for this export
        all_plots: list[tuple[str, dict]] = []
        for _gid, gspec in groups.items():
            for p_id, pentry in gspec.get("plots", {}).items():
                spec = pentry.get("spec")
                if spec:
                    all_plots.append((p_id, spec))
        if not all_plots:
            for p_id, spec in top_plots.items():
                all_plots.append((p_id, spec))

        buf = io.BytesIO()
        with zipfile.ZipFile(buf, mode="w", compression=zipfile.ZIP_DEFLATED) as zf:
            bundle_dir = f"{ts}_{safe_name}"

            # ── FILTERS.txt (No Trace No Export) ─────────────────────────
            if active_filters:
                lines = [
                    "FILTER TRACE — embedded per 'No Trace No Export' protocol.",
                    f"Exported at: {now.isoformat()}",
                    f"Project: {proj_id}",
                    "",
                    "Applied filters at time of export:",
                ]
                for i, f in enumerate(active_filters, 1):
                    col = f.get("column", "?")
                    op = _op_label(f.get("op", "eq"))
                    val = f.get("value", "")
                    val_str = ", ".join(str(v) for v in val) if isinstance(val, list) else str(val)
                    lines.append(f"  {i}. {col} {op} {val_str}")
                zf.writestr(f"{bundle_dir}/FILTERS.txt", "\n".join(lines))

            # ── Render and save plots ─────────────────────────────────────
            rendered_plots = {}  # p_id → figure object
            with tempfile.TemporaryDirectory() as tmpdir:
                tmpdir_path = Path(tmpdir)

                for p_id, spec in all_plots:
                    try:
                        # Build synthetic manifest with applied filters
                        plot_spec = copy.deepcopy(spec)
                        if active_filters:
                            vf_filters = [
                                {k: v for k, v in f.items() if k != "dtype"}
                                for f in active_filters
                            ]
                            for vf in vf_filters:
                                if isinstance(vf.get("value"), list):
                                    vf["op"] = "in" if vf["op"] in ("eq", "in") else "not_in"
                            plot_spec["filters"] = vf_filters

                        synthetic_manifest = {
                            "plots": {p_id: plot_spec},
                            "plot_defaults": cfg.raw_config.get("plot_defaults", {}),
                        }

                        # Resolve dataset
                        target_ds = spec.get("target_dataset")
                        if target_ds:
                            anchor_dir = bootloader.get_location("user_sessions") / "anchors"
                            out_path = anchor_dir / f"{target_ds}.parquet"
                            if out_path.exists():
                                lf = pl.scan_parquet(out_path)
                            else:
                                lf = orchestrator.materialize_tier1(
                                    project_id=proj_id,
                                    collection_id=target_ds,
                                    output_path=out_path
                                )
                        else:
                            lf = tier1_anchor()

                        fig = viz_factory.render(lf, synthetic_manifest, p_id)
                        rendered_plots[p_id] = fig

                        # Save to temp file then read bytes into zip
                        if preset == "web":
                            plot_path = tmpdir_path / f"{p_id}.svg"
                            fig.save(str(plot_path), format="svg", verbose=False)
                        else:
                            plot_path = tmpdir_path / f"{p_id}.png"
                            fig.save(str(plot_path), dpi=dpi, verbose=False)

                        with open(plot_path, "rb") as f:
                            zf.writestr(
                                f"{bundle_dir}/plots/{plot_path.name}",
                                f.read()
                            )
                    except Exception as e:
                        # Write error stub so bundle is still complete
                        zf.writestr(
                            f"{bundle_dir}/plots/{p_id}_ERROR.txt",
                            f"Plot render failed:\n{e}"
                        )

                # ── Export data by tier ───────────────────────────────────
                # T1: always exported.
                # T2: always exported when materialize_tier2 is available (tier_reference).
                # T3: only for advanced+ personas, and only when tier_toggle == "T3".
                #     T3 is the user-adjusted DataFrame (tier3_leaf); deferred if no active T3.
                # EXPORT-BUG-1 (2026-04-30): persona IDs use HYPHENS per project
                # convention. Underscore variants silently fail every gate, so
                # T3 data was being skipped from every export regardless of
                # persona. Same bug family as the earlier sidebar_nav fix.
                is_advanced = persona in (
                    "pipeline-exploration-advanced", "project-independent",
                    "developer", "qa",
                )
                active_tier = tier_toggle.get()  # "T1", "T2", "T3"
                export_t3 = is_advanced and active_tier == "T3"

                exported_datasets: set[str] = set()
                for p_id, spec in all_plots:
                    target_ds = spec.get("target_dataset")
                    ds_key = target_ds or "__tier1_anchor__"
                    if ds_key in exported_datasets:
                        continue
                    exported_datasets.add(ds_key)

                    # ── T1 ────────────────────────────────────────────────
                    try:
                        if target_ds:
                            anchor_dir = bootloader.get_location("user_sessions") / "anchors"
                            out_path = anchor_dir / f"{target_ds}.parquet"
                            if out_path.exists():
                                lf_t1 = pl.scan_parquet(out_path)
                            else:
                                lf_t1 = orchestrator.materialize_tier1(
                                    project_id=proj_id,
                                    collection_id=target_ds,
                                    output_path=out_path
                                )
                        else:
                            lf_t1 = tier1_anchor()
                        df_t1 = lf_t1.collect()
                        safe_ds = ds_key.replace("/", "_")
                        tsv_path = tmpdir_path / f"{safe_ds}_T1.tsv"
                        df_t1.write_csv(str(tsv_path), separator="\t")
                        with open(tsv_path, "rb") as f:
                            zf.writestr(f"{bundle_dir}/data/{safe_ds}_T1.tsv", f.read())
                    except Exception as e:
                        zf.writestr(
                            f"{bundle_dir}/data/{ds_key}_T1_ERROR.txt",
                            f"T1 data export failed:\n{e}"
                        )

                    # ── T2 ────────────────────────────────────────────────
                    try:
                        lf_t2 = tier_reference()
                        if lf_t2 is not None:
                            df_t2 = lf_t2.collect() if hasattr(lf_t2, "collect") else lf_t2
                            safe_ds = ds_key.replace("/", "_")
                            tsv_path = tmpdir_path / f"{safe_ds}_T2.tsv"
                            df_t2.write_csv(str(tsv_path), separator="\t")
                            with open(tsv_path, "rb") as f:
                                zf.writestr(f"{bundle_dir}/data/{safe_ds}_T2.tsv", f.read())
                    except Exception as e:
                        zf.writestr(
                            f"{bundle_dir}/data/{ds_key}_T2_ERROR.txt",
                            f"T2 data export failed:\n{e}"
                        )

                    # ── T3 (advanced persona + T3 active only) ────────────
                    if export_t3:
                        try:
                            df_t3 = tier3_leaf()
                            if df_t3 is not None:
                                if hasattr(df_t3, "lazy"):
                                    df_t3 = df_t3  # already DataFrame
                                safe_ds = ds_key.replace("/", "_")
                                tsv_path = tmpdir_path / f"{safe_ds}_T3.tsv"
                                df_t3.write_csv(str(tsv_path), separator="\t")
                                with open(tsv_path, "rb") as f:
                                    zf.writestr(
                                        f"{bundle_dir}/data/{safe_ds}_T3.tsv", f.read()
                                    )
                        except Exception as e:
                            zf.writestr(
                                f"{bundle_dir}/data/{ds_key}_T3_ERROR.txt",
                                f"T3 data export failed:\n{e}"
                            )

                # ── Copy YAML recipes (active project ONLY) ──────────────
                # EXPORT-BUG-2 (2026-04-30): the previous code did
                # proj_dir.rglob("*.yaml") on the parent directory, which
                # scooped up EVERY other project's manifest + their include
                # fragments into the bundle (cross-project leak). Now we copy:
                #   1. The active project's manifest itself
                #   2. Its `!include` subdirectory if one exists (named
                #      `{proj_id}/`) — that's where fragment files live per
                #      the basename-mirroring convention.
                try:
                    proj_manifest_path = bootloader.available_projects.get(proj_id)
                    if proj_manifest_path:
                        manifest_p = Path(str(proj_manifest_path))
                        proj_dir = manifest_p.parent
                        # 1. The active manifest itself
                        with open(manifest_p, "rb") as f:
                            zf.writestr(
                                f"{bundle_dir}/recipes/{manifest_p.name}",
                                f.read()
                            )
                        # 2. Includes subdirectory (if it exists for this project)
                        includes_dir = proj_dir / proj_id
                        if includes_dir.is_dir():
                            for yaml_file in includes_dir.rglob("*.yaml"):
                                rel = yaml_file.relative_to(proj_dir)
                                with open(yaml_file, "rb") as f:
                                    zf.writestr(
                                        f"{bundle_dir}/recipes/{rel}",
                                        f.read()
                                    )
                except Exception as e:
                    zf.writestr(f"{bundle_dir}/recipes/ERROR.txt", str(e))

            # ── Generate Quarto .qmd report ───────────────────────────────
            plot_ext = "svg" if preset == "web" else "png"
            qmd_lines = [
                "---",
                f'title: "Results Report — {proj_id}"',
                f'date: "{now.strftime("%Y-%m-%d")}"',
                f'author: "{safe_name}"',
                'format:',
                '  html:',
                '    self-contained: true',
                '  pdf:',
                '    documentclass: article',
                "---",
                "",
                "## Overview",
                "",
                f"Project: **{proj_id}**  ",
                f"Persona: **{persona}**  ",
                f"Export preset: **{preset}**  ",
                f"Generated: {now.strftime('%Y-%m-%d %H:%M:%S')}  ",
                "",
            ]
            if active_filters:
                qmd_lines += [
                    "## Active Filters at Export",
                    "",
                    "| Column | Op | Value |",
                    "|--------|-----|-------|",
                ]
                for f in active_filters:
                    col = f.get("column", "?")
                    op = _op_label(f.get("op", "eq"))
                    val = f.get("value", "")
                    val_str = ", ".join(str(v) for v in val) if isinstance(val, list) else str(val)
                    qmd_lines.append(f"| {col} | {op} | {val_str} |")
                qmd_lines.append("")

            qmd_lines += ["## Plots", ""]
            for p_id, spec in all_plots:
                label = spec.get("title") or p_id.replace("_", " ").title()
                qmd_lines += [
                    f"### {label}",
                    "",
                    f"![{label}](plots/{p_id}.{plot_ext}){{width=100%}}",
                    "",
                ]

            qmd_lines += ["## Data", ""]
            tiers_exported = ["T1", "T2"] + (["T3"] if export_t3 else [])
            qmd_lines.append(
                f"Tiers exported: **{', '.join(tiers_exported)}**"
                + ("  *(T3 = user-adjusted)*" if export_t3 else "")
            )
            qmd_lines.append("")
            for ds_key in exported_datasets:
                safe_ds = ds_key.replace("/", "_")
                qmd_lines += [f"### {ds_key}", ""]
                for tier in tiers_exported:
                    qmd_lines.append(f"- {tier}: `data/{safe_ds}_{tier}.tsv`")
                qmd_lines.append("")

            qmd_lines += [
                "---",
                "",
                "> Report generated by SPARMVET-VIZ.",
                "> Recipes are in the `recipes/` folder.",
                "> To render: `quarto render report.qmd`",
            ]
            zf.writestr(f"{bundle_dir}/report.qmd", "\n".join(qmd_lines))

            # ── README.txt ────────────────────────────────────────────────
            readme_lines = [
                "SPARMVET-VIZ Export Bundle",
                "=" * 40,
                f"Timestamp  : {now.isoformat()}",
                f"Project    : {proj_id}",
                f"User       : {safe_name}",
                f"Persona    : {persona}",
                f"Preset     : {preset} (DPI={dpi})",
                f"Plots      : {len(all_plots)}",
                f"Tiers      : {', '.join(tiers_exported)}",
                f"Filters    : {len(active_filters)} active",
                "",
                "Contents:",
                "  plots/      — rendered figures",
                "  data/       — datasets as TSV: <dataset>_T1.tsv, <dataset>_T2.tsv"
                + (", <dataset>_T3.tsv" if export_t3 else ""),
                "  recipes/    — YAML wrangling recipes (T3 updated recipe if applicable)",
                "  report.qmd  — Quarto source report (run: quarto render report.qmd)",
                "  FILTERS.txt — filter trace (if filters were active)",
                "  README.txt  — this file",
            ]
            zf.writestr(f"{bundle_dir}/README.txt", "\n".join(readme_lines))

        buf.seek(0)
        yield buf.read()

    # ── 22-E: Export Audit Report ─────────────────────────────────────────────

    @output
    @render.ui
    def export_audit_report_ui():
        """Audit Report export — single format selector + one download button.

        Phase 25-G: consolidated radio (HTML/PDF/DOCX) + single download button.
        The download handler dispatches on `export_audit_format` and renders all
        three formats via Quarto natively (ADR-052-FOLLOWUP-1 closed: no Pandoc
        fallback).

        Phase 25-K (FOLLOWUP-2): persona visibility now gated by
        `audit_report_enabled` rather than a hardcoded persona-name set, so
        templates control this independently of code changes.
        """
        if not bootloader.is_enabled("audit_report_enabled"):
            return ui.div()

        discarded_warning = ui.div()
        if home_state is not None:
            state = home_state.get()
            all_committed = [
                n for nodes in (state.get("t3_recipe_by_plot", {}) or {}).values()
                for n in nodes
            ]
            n_discarded = sum(1 for n in all_committed if not n.get("active", True))
            if n_discarded:
                discarded_warning = ui.tags.small(
                    f"⚠️ {n_discarded} deactivated node(s) — they will NOT appear in the report.",
                    class_="text-warning d-block mb-1",
                    style="font-size:0.7em;",
                )

        return ui.div(
            ui.p("Export Audit Report", class_="ultra-small fw-bold mb-1"),
            discarded_warning,
            ui.input_radio_buttons(
                "export_audit_format",
                label="Format",
                choices={"html": "HTML", "pdf": "PDF", "docx": "DOCX"},
                selected="html",
                inline=True,
            ),
            ui.download_button(
                "export_audit_report_download",
                "📋 Export Audit Report",
                class_="btn-info btn-sm w-100",
            ),
            class_="mb-3 px-2",
            style="font-size:0.8em;",
        )

    @render.download(filename=lambda: _audit_report_filename(
        safe_input(input, "export_audit_format", "html")
    ))
    async def export_audit_report_download():
        """Render the audit report in the selected format and stream the bytes.

        Phase 25-K (ADR-052-FOLLOWUP-1 closed): Quarto renders HTML/PDF/DOCX
        natively via `quarto render --to <fmt>`. No Pandoc fallback. If the
        render fails, the user is notified and the .qmd source is streamed so
        the failure is visible rather than silent.
        """
        import tempfile
        from app.modules.exporter import render_audit_report

        if home_state is None:
            yield b""
            return

        state = home_state.get()
        proj_id = safe_input(input, "project_id", "")
        fmt = safe_input(input, "export_audit_format", "html")

        msig = state.get("manifest_sha256") or ""
        dbh = state.get("data_batch_hash") or ""
        session_key = ""
        if msig and dbh:
            from app.modules.session_manager import SessionManager
            session_key = SessionManager.compute_session_key(msig, dbh)

        with tempfile.TemporaryDirectory() as tmpdir:
            out_path = render_audit_report(
                home_state=state,
                session_key=session_key,
                output_dir=tmpdir,
                manifest_id=proj_id,
                fmt=fmt,
            )
            if Path(out_path).suffix.lstrip(".") != fmt:
                ui.notification_show(
                    f"⚠️ Quarto could not render {fmt.upper()} — streaming the .qmd source.",
                    type="warning", duration=8,
                )
            yield Path(out_path).read_bytes()

    def _audit_report_filename(fmt: str) -> str:
        import datetime, re
        ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        proj_id = safe_input(input, "project_id", "report")
        safe_id = re.sub(r"[^A-Za-z0-9_-]", "_", proj_id)[:30]
        return f"{ts}_{safe_id}_audit_report.{fmt}"

    def _export_bundle_filename() -> str:
        """Generate timestamped zip filename for the export bundle."""
        import datetime, re
        now = datetime.datetime.now()
        ts = now.strftime("%Y%m%d_%H%M%S")
        raw_name = safe_input(input, "export_user_name", "user").strip() or "user"
        safe_name = re.sub(r"[^A-Za-z0-9_-]", "_", raw_name)[:40]
        return f"{ts}_{safe_name}_results.zip"
