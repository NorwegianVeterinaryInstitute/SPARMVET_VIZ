"""app/handlers/single_graph_export_handlers.py
Single Graph Export panel — exports the active plot as a .zip bundle.

New in Phase 25-H (ADR-052). Reuses helpers from home_theater.define_server()
(passed in as closures) so the export sees the same plot spec, T3 stack and
filter pipeline that the on-screen render sees.

Bundle contents
---------------
- plot.<png|svg|pdf>          — rendered figure for the active plot
- data.tsv                    — T1 + applied filters + T3 stack data slice
- manifest_fragment.yaml      — the active plot's spec section
- t3_recipe.json              — committed T3 RecipeNodes for this plot
- README.txt                  — bundle metadata

Two-Category Law (ADR-045): this module contains @render.* / @reactive.*
decorators only. It MUST NOT be imported by non-Shiny contexts.
"""

from __future__ import annotations

# @deps
# provides: function:define_single_graph_export_server, output:single_graph_export_ui, output:export_single_graph
# consumes: app/src/bootloader.py, libs/viz_factory/src/viz_factory/viz_factory.py, polars, shiny
# consumed_by: app/handlers/home_theater.py
# doc: .antigravity/knowledge/architecture_decisions.md#ADR-045, .antigravity/knowledge/architecture_decisions.md#ADR-052
# @end_deps

import copy
from pathlib import Path

from shiny import render, ui

from app.src.bootloader import bootloader


def define_single_graph_export_server(input, output, session, *,
                                      viz_factory, active_cfg, active_home_subtab,
                                      applied_filters, home_state, safe_input,
                                      _resolve_active_spec, _resolve_active_lf,
                                      _t3_filter_rows, _t3_drop_columns,
                                      _active_plot_t3_nodes):
    """Register the Single Graph Export panel + download handler.

    All reactive helpers are passed as closures from home_theater.define_server
    so this module sees the same view of the active plot's spec, data, and T3
    stack that the on-screen render uses.
    """

    @output
    @render.ui
    def single_graph_export_ui():
        if not bootloader.is_enabled("export_graph_enabled"):
            return ui.div()

        subtab = active_home_subtab.get()
        active_label = subtab.removeprefix("subtab_") if subtab else "(none)"

        return ui.div(
            ui.tags.small(
                f"Active plot: {active_label}",
                class_="text-muted d-block mb-1",
                style="font-size:0.7em;",
            ),
            ui.input_radio_buttons(
                "export_graph_format",
                label="Format",
                choices={"png": "PNG", "svg": "SVG", "pdf": "PDF"},
                selected="png",
                inline=True,
            ),
            ui.download_button(
                "export_single_graph",
                "🖼 Export Active Graph",
                class_="btn-outline-success btn-sm w-100 mt-1",
            ),
            class_="mb-2 px-2",
            style="font-size:0.8em;",
        )

    @render.download(filename=lambda: _single_graph_filename())
    async def export_single_graph():
        """Stream a .zip containing: plot, data slice, manifest fragment, T3 stack."""
        import datetime
        import io
        import json
        import tempfile
        import zipfile
        import yaml

        if not bootloader.is_enabled("export_graph_enabled"):
            yield b""
            return

        subtab = active_home_subtab.get()
        p_id = subtab.removeprefix("subtab_") if subtab else None
        if not p_id:
            ui.notification_show(
                "No active plot subtab — open a plot before exporting.",
                type="warning", duration=5,
            )
            yield b""
            return

        spec = _resolve_active_spec(p_id)
        if spec is None:
            ui.notification_show(
                f"No spec found for plot '{p_id}'.", type="error", duration=5
            )
            yield b""
            return

        fmt = safe_input(input, "export_graph_format", "png")
        now = datetime.datetime.now()

        # Build the same plot_spec the dynamic_tabs renderer would build —
        # filters injected, eq/ne→in/not_in promotion when value is a list.
        plot_spec = copy.deepcopy(spec)
        filter_rows = list(applied_filters.get()) + _t3_filter_rows(subtab)
        if filter_rows:
            vf_filters = [
                {k: v for k, v in f.items() if k != "dtype"}
                for f in filter_rows
            ]
            for vf in vf_filters:
                if isinstance(vf.get("value"), list):
                    if vf["op"] in ("eq", "in"):
                        vf["op"] = "in"
                    elif vf["op"] in ("ne", "not_in"):
                        vf["op"] = "not_in"
            plot_spec["filters"] = vf_filters

        cfg = active_cfg()
        synthetic_manifest = {
            "plots": {p_id: plot_spec},
            "plot_defaults": cfg.raw_config.get("plot_defaults", {}),
        }

        try:
            lf = _resolve_active_lf(spec)
            drops = [c for c in _t3_drop_columns(subtab) if c in lf.collect_schema().names()]
            if drops:
                lf = lf.drop(drops)
        except Exception as e:
            ui.notification_show(f"❌ Data error: {e}", type="error", duration=8)
            yield b""
            return

        buf = io.BytesIO()
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp = Path(tmpdir)
            with zipfile.ZipFile(buf, "w", zipfile.ZIP_DEFLATED) as zf:
                # 1. Plot
                try:
                    fig = viz_factory.render(lf, synthetic_manifest, p_id)
                    plot_path = tmp / f"plot.{fmt}"
                    if fmt == "png":
                        fig.save(str(plot_path), dpi=300, verbose=False)
                    else:
                        fig.save(str(plot_path), format=fmt, verbose=False)
                    zf.write(plot_path, arcname=plot_path.name)
                except Exception as e:
                    zf.writestr("plot_ERROR.txt", f"Plot render failed:\n{e}")

                # 2. Data slice (T1 + filters + T3 drops)
                try:
                    df = lf.collect()
                    data_path = tmp / "data.tsv"
                    df.write_csv(str(data_path), separator="\t")
                    zf.write(data_path, arcname="data.tsv")
                except Exception as e:
                    zf.writestr("data_ERROR.txt", f"Data export failed:\n{e}")

                # 3. Manifest fragment — the active plot's spec only
                zf.writestr(
                    "manifest_fragment.yaml",
                    yaml.safe_dump({"plots": {p_id: spec}}, sort_keys=False),
                )

                # 4. T3 nodes committed for this plot
                t3_nodes = _active_plot_t3_nodes(subtab) if home_state is not None else []
                zf.writestr("t3_recipe.json", json.dumps(t3_nodes, indent=2))

                # 5. README
                proj_id = safe_input(input, "project_id", "")
                readme = [
                    "SPARMVET-VIZ Single Graph Export",
                    "=" * 40,
                    f"Generated : {now.isoformat()}",
                    f"Project   : {proj_id}",
                    f"Plot      : {p_id}",
                    f"Format    : {fmt}",
                    f"Filters   : {len(filter_rows)} applied",
                    f"T3 nodes  : {len(t3_nodes)} committed",
                ]
                zf.writestr("README.txt", "\n".join(readme))

        yield buf.getvalue()

    def _single_graph_filename() -> str:
        import datetime, re
        ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        subtab = active_home_subtab.get() or ""
        p_id = subtab.removeprefix("subtab_") or "plot"
        safe_pid = re.sub(r"[^A-Za-z0-9_-]", "_", p_id)[:40]
        return f"{ts}_{safe_pid}_graph.zip"
