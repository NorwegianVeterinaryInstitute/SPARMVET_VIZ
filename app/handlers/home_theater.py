"""app/handlers/home_theater.py
Home Theater Shiny wiring (ADR-043 / ADR-044 / ADR-045).

Entry point:
    define_server(input, output, session, *,
                  bootloader, wrangle_studio, dev_studio,
                  orchestrator, viz_factory, gallery_viewer,
                  current_persona, anchor_path, tier1_anchor,
                  tier_reference, tier3_leaf, active_cfg,
                  active_collection_id, safe_input, active_home_subtab)

Concern: dynamic_tabs, sidebar_nav_ui, sidebar_tools_ui, right_sidebar_content_ui,
         sidebar_filters, system_tools_ui, plot_reference, table_reference,
         plot_leaf, table_leaf, handle_plot_brush, comparison_mode_toggle_ui.
Two-Category Law (ADR-045): This file contains @render.* and @reactive.*
decorators only. It MUST NOT be imported by non-Shiny contexts.
"""

from __future__ import annotations

# @deps
# provides: function:define_server (home_theater)
# consumes: app/modules/orchestrator.py, app/modules/wrangle_studio.py, app/modules/dev_studio.py, libs/viz_factory/src/viz_factory/viz_factory.py, utils/config_loader.py
# consumed_by: app/src/server.py
# doc: .antigravity/knowledge/architecture_decisions.md#ADR-043, .antigravity/knowledge/architecture_decisions.md#ADR-044, .antigravity/knowledge/architecture_decisions.md#ADR-045
# @end_deps

from pathlib import Path

import polars as pl
from transformer.lookup import lookup_anchor_rows
from shiny import reactive, render, ui
from utils.config_loader import ConfigManager


def _collect_all_group_plot_ids(bootloader) -> list[tuple[str, dict]]:
    """Enumerate all (plot_id, spec_dict) pairs from analysis_groups across all projects.

    Called once at server init to register dynamic @render.plot handlers.
    Returns list of (p_id, spec) tuples (spec may be None for unresolved entries).
    """
    seen = set()
    results = []
    for proj_id, manifest_path in bootloader.available_projects.items():
        try:
            cfg = ConfigManager(str(manifest_path))
            groups = cfg.raw_config.get("analysis_groups", {})
            for _gid, gspec in groups.items():
                for p_id, plot_entry in gspec.get("plots", {}).items():
                    if p_id not in seen:
                        seen.add(p_id)
                        results.append((p_id, plot_entry.get("spec")))
        except Exception:
            pass
    return results


def define_server(input, output, session, *,
                  bootloader, wrangle_studio, dev_studio,
                  orchestrator, viz_factory, gallery_viewer,
                  current_persona, anchor_path, tier1_anchor,
                  tier_reference, tier3_leaf, active_cfg,
                  active_collection_id, safe_input,
                  active_home_subtab):
    """Register all Home Theater reactive handlers.

    Parameters
    ----------
    bootloader : Bootloader
        Path Authority (ADR-031).
    wrangle_studio : WrangleStudio
        Shared WrangleStudio state (for render_ui routing).
    dev_studio : DevStudio
        Shared DevStudio state.
    orchestrator : DataOrchestrator
        Used for Tier 1 materialization in dynamic_tabs.
    viz_factory : VizFactory
        Plotting engine.
    gallery_viewer : GalleryViewer
        Gallery explorer module.
    current_persona : reactive.Value[str]
        Active persona (ADR-030).
    anchor_path : reactive.Value[str | None]
        Path to active Parquet anchor.
    tier1_anchor : reactive.Calc
        Tier 1 LazyFrame.
    tier_reference : reactive.Calc
        Tier 2 reference LazyFrame.
    tier3_leaf : reactive.Calc
        Tier 3 user-modified DataFrame.
    active_cfg : reactive.Calc
        Active ConfigManager.
    active_collection_id : reactive.Calc
        Active collection ID string.
    safe_input : callable
        Shared utility: safe_input(input_obj, key, default) → value.
    active_home_subtab : reactive.Value[str]
        Phase 21-B: tracks the active plot sub-tab id across groups.
    """

    # ── Phase 21-B: Dynamic plot handlers for analysis_groups ─────────────────
    # Enumerate all plot IDs at server init time so Shiny can register each
    # @render.plot slot. Handlers read active_cfg() at render time, not init time.
    _all_group_plot_ids = _collect_all_group_plot_ids(bootloader)

    def _make_group_plot_handler(p_id: str):
        """Factory: returns a @render.plot fn that renders plot_group_{p_id}."""
        @output(id=f"plot_group_{p_id}")
        @render.plot(alt=f"Plot: {p_id}")
        def _group_plot_handler():
            cfg = active_cfg()
            groups = cfg.raw_config.get("analysis_groups", {})
            # Find the spec for this p_id across all groups
            spec = None
            for _gid, gspec in groups.items():
                plot_entry = gspec.get("plots", {}).get(p_id)
                if plot_entry is not None:
                    spec = plot_entry.get("spec")
                    break
            if spec is None:
                return None

            # Build synthetic manifest so viz_factory.render can be used
            synthetic_manifest = {
                "plots": {p_id: spec},
                "plot_defaults": cfg.raw_config.get("plot_defaults", {}),
            }

            # Resolve data: use target_dataset or fall back to tier1_anchor
            target_ds = spec.get("target_dataset")
            if target_ds:
                proj_id = safe_input(input, "project_id", bootloader.get_default_project())
                coll_id = target_ds
                anchor_dir = bootloader.get_location("user_sessions") / "anchors"
                anchor_dir.mkdir(parents=True, exist_ok=True)
                out_path = anchor_dir / f"{coll_id}.parquet"
                try:
                    if out_path.exists():
                        lf = pl.scan_parquet(out_path)
                    else:
                        lf = orchestrator.materialize_tier1(
                            project_id=proj_id,
                            collection_id=coll_id,
                            output_path=out_path
                        )
                except Exception as e:
                    import matplotlib.pyplot as plt
                    fig, ax = plt.subplots()
                    ax.text(0.5, 0.5, f"Data error: {e}", ha="center", va="center",
                            transform=ax.transAxes, color="red", fontsize=9)
                    ax.axis("off")
                    return fig
            else:
                lf = tier1_anchor()

            try:
                return viz_factory.render(lf, synthetic_manifest, p_id)
            except Exception as e:
                import matplotlib.pyplot as plt
                fig, ax = plt.subplots()
                ax.text(0.5, 0.5, f"Render error:\n{e}", ha="center", va="center",
                        transform=ax.transAxes, color="red", fontsize=9,
                        wrap=True)
                ax.axis("off")
                return fig

        return _group_plot_handler

    # Register one handler per discovered plot ID
    for _p_id, _spec in _all_group_plot_ids:
        _make_group_plot_handler(_p_id)

    # 3. Reactive Tab Components (Discovery Architecture)
    @render.ui
    def dynamic_tabs():
        """
        Routes to WrangleStudio, DevStudio, Gallery, or the Unified Home Theater.
        ADR-043 / Phase 21-A: 'Analysis Theater / Viz' nav mode eliminated.
        Home renders exclusively from manifest analysis_groups.
        """
        active_sidebar = safe_input(input, "sidebar_nav", "Home")
        p = current_persona.get()

        # 1. Module Routing (ADR-031 Compliance)
        if active_sidebar == "Wrangle Studio":
            return ui.div(wrangle_studio.render_ui(), class_="theater-container-main")
        if active_sidebar == "Dev Studio":
            return ui.div(dev_studio.render_ui(), class_="theater-container-main")
        if active_sidebar == "Gallery":
            return ui.div(gallery_viewer.render_explorer_ui(), class_="theater-container-main")

        # 2. Results Theater (Home) Logic — ADR-043 Unified Home Theater
        try:
            proj_id = safe_input(input, "project_id", bootloader.get_default_project())
            coll_id = active_collection_id()
            # ADR-024: Materialize to persistent session location
            anchor_dir = bootloader.get_location("user_sessions") / "anchors"
            if not anchor_dir.exists():
                anchor_dir.mkdir(parents=True, exist_ok=True)
            out_path = anchor_dir / f"{coll_id}.parquet"

            lf_full = orchestrator.materialize_tier1(
                project_id=proj_id,
                collection_id=coll_id,
                output_path=out_path
            )
            if out_path.exists():
                anchor_path.set(str(out_path))
        except Exception as e:
            return ui.div(ui.markdown(f"**Data Assembly Failed**: {e}"), class_="alert alert-danger")

        # Discover columns (retained for future filter scoping in Phase 21-F)
        all_cols = lf_full.columns  # noqa: F841

        # --- Sub-Header: Branding & Persona Status (ADR-043) ---
        theater_header = ui.div(
            ui.div(
                ui.h4("SPARMVET Home", class_="mb-0"),
                ui.tags.small(
                    f"Manifest: {input.project_id()} | Persona: {p.replace('_', ' ').title()}",
                    class_="text-muted"
                ),
                class_="d-flex flex-column"
            ),
            class_="theater-header-branding mb-2",
            style="padding: 10px 15px; background: white; border-bottom: 1px solid #dee2e6;"
        )

        # --- Build manifest-driven tabs (ADR-043 / Phase 21-B) ---
        # analysis_groups only — no hardcoded tabs. Each group becomes a
        # ui.accordion_panel (collapsible, default expanded) containing a
        # navset_underline of plot sub-tabs.
        cfg = active_cfg()
        groups = cfg.raw_config.get("analysis_groups", {})
        accordion_panels = []

        for group_id, group_spec in groups.items():
            plot_ids = list(group_spec.get("plots", {}).keys())
            # ADR-036 ID sanitation
            safe_sub_id = (
                group_id.replace(' ', '_').replace('📊', 'QC')
                        .replace('💊', 'AMR').lower()
            )

            plot_subtabs = []
            for p_id in plot_ids:
                label = (
                    group_spec["plots"][p_id].get("label")
                    or p_id.replace("_", " ").title()
                )
                plot_subtabs.append(
                    ui.nav_panel(
                        label,
                        ui.card(
                            ui.output_plot(f"plot_group_{p_id}"),
                            class_="shadow-none border-0 mt-0",
                            style="min-height: 520px;"
                        ),
                        value=f"subtab_{p_id}"
                    )
                )

            if not plot_subtabs:
                panel_content = ui.p(
                    "No plots defined for this group.", class_="text-muted p-4"
                )
            else:
                panel_content = ui.navset_underline(
                    *plot_subtabs,
                    id=f"subtabs_{safe_sub_id}"
                )

            group_label = group_spec.get("label") or group_spec.get("description", group_id)
            accordion_panels.append(
                ui.accordion_panel(
                    group_label,
                    panel_content,
                    value=f"group_{safe_sub_id}",
                )
            )

        if not accordion_panels:
            home_body = ui.p(
                "Define analysis_groups in your manifest to populate this view.",
                class_="text-muted p-4"
            )
        else:
            home_body = ui.accordion(
                *accordion_panels,
                id="home_groups_accordion",
                multiple=True,
                open=[p._data_value for p in accordion_panels],  # all expanded by default
            )

        return ui.div(
            theater_header,
            home_body,
            class_="theater-container-main"
        )

    # Phase 21-B: Track active sub-tab across all analysis_groups navsets.
    # Polls all subtabs_{group_id} inputs; first non-None value wins.
    @reactive.Effect
    def _track_active_home_subtab():
        cfg = active_cfg()
        groups = cfg.raw_config.get("analysis_groups", {})
        for group_id in groups:
            safe_sub_id = (
                group_id.replace(' ', '_').replace('📊', 'QC')
                        .replace('💊', 'AMR').lower()
            )
            val = safe_input(input, f"subtabs_{safe_sub_id}", None)
            if val:
                active_home_subtab.set(val)
                return

    @render.ui
    def sidebar_nav_ui():
        perm = current_persona.get()
        print(f"DEBUG: Rendering sidebar_nav_ui for Persona: {perm}")

        nav_items = [ui.nav_panel("Home", value="Home")]

        if perm in ["pipeline_exploration_advanced", "project_independent", "developer"]:
            nav_items.append(ui.nav_panel("Blueprint Architect", value="Wrangle Studio"))

        if perm in ["developer"]:
            nav_items.append(ui.nav_panel("Dev Studio", value="Dev Studio"))

        nav_items.append(ui.nav_panel("Gallery", value="Gallery"))

        return ui.navset_pill(
            *nav_items,
            id="sidebar_nav",
            header=ui.h6(f"Active: {perm.replace('_', ' ').title()}",
                         class_="text-muted px-2 py-1 mb-1 border-bottom", style="font-size: 0.7em;")
        )

    # 4. Sidebar Tools (Contextual Manifest Workbench)
    @output(id="sidebar_tools_ui")
    @render.ui
    def sidebar_tools_ui():
        """
        Relocated Sidebar Management (ADR-038).
        Enforces dedicated Persona-based control clusters.
        """
        active_sidebar = safe_input(input, "sidebar_nav", "Home")

        # 🟢 Discovery Mode (Gallery)
        if active_sidebar == "Gallery":
            return ui.div(
                ui.p("Discovery Mode Active", class_="text-muted p-4 italic"),
                ui.p("Choose a visual recipe to begin.", class_="text-muted px-4 small")
            )

        # 🔵 Manifest Workbench (Wrangle Studio)
        if active_sidebar == "Wrangle Studio":
            return ui.div(
                ui.accordion(
                    ui.accordion_panel(
                        "🗂️ Master Manifest",
                        ui.input_select("stored_manifest_selector", None,
                                        choices=["Scanning config/..."]),
                        ui.tags.small(
                            "Select a project manifest. Click any node in the TubeMap to navigate.",
                            class_="text-muted d-block mt-1"),
                        icon=ui.tags.i(class_="bi bi-diagram-3")
                    ),
                    ui.accordion_panel(
                        "📤 External Exchange",
                        ui.input_file("manifest_uploader", "Select YAML...",
                                      accept=[".yaml"], multiple=False),
                        ui.input_action_button("btn_upload_replace", "📥 Upload (Replace)",
                                               class_="btn-info btn-sm w-100 mb-1"),
                        ui.input_action_button("btn_upload_append", "➕ Upload & Append",
                                               class_="btn-outline-primary btn-sm w-100"),
                        ui.hr(),
                        ui.download_button("btn_download_manifest", "💾 Download/Export",
                                           class_="btn-outline-primary w-100"),
                        icon=ui.tags.i(class_="bi bi-cloud-arrow-up")
                    ),
                    id="wrangle_sidebar_accordion"
                ),
                # Hidden controls — kept in DOM so Shiny bridge can programmatically
                # update the selection and fire the import trigger via js_eval.
                ui.div(
                    ui.input_select("dataset_pipeline_selector", None,
                                    choices=["Select a Master first"]),
                    ui.input_action_button("btn_import_manifest", "Import",
                                           class_="btn-info btn-sm"),
                    ui.input_action_button("btn_save_internal", "Save",
                                           class_="btn-success btn-sm"),
                    style="display:none;",
                    id="blueprint_hidden_controls"
                )
            )

        # 🏠 Standard Operation Sidebar (Home — ADR-043)
        try:
            proj_choices = list(bootloader.available_projects.keys())
            def_proj = bootloader.get_default_project()
        except Exception:
            proj_choices = []
            def_proj = None

        return ui.accordion(
            ui.accordion_panel(
                "Project Navigator",
                ui.div(
                    ui.input_select("project_id", "Project Selection",
                                    choices=proj_choices,
                                    selected=def_proj),
                    class_="d-flex flex-column gap-1"
                ),
                icon=ui.tags.i(class_="bi bi-folder-fill")
            ),
            ui.accordion_panel(
                "Filters",
                ui.div(
                    ui.output_ui("sidebar_filters"),
                    class_="d-flex flex-column gap-0"
                ),
                icon=ui.tags.i(class_="bi bi-filter-circle-fill")
            ),
            ui.accordion_panel(
                "System Tools",
                ui.div(
                    ui.output_ui("system_tools_ui"),
                    class_="d-flex flex-column gap-1"
                ),
                icon=ui.tags.i(class_="bi bi-cpu-fill")
            ),
            id="nav_accordion",
            multiple=True,
            open=["Project Navigator", "Filters"]
        )

    # --- 📐 Right Sidebar Context Matrix (ADR-039 / ADR-044) ---
    @output
    @render.ui
    def right_sidebar_content_ui():
        """
        Context-sensitive right sidebar (ADR-039).
        Switches content based on the active module.
        """
        active_sidebar = safe_input(input, "sidebar_nav", "Home")

        # --- 🏗️ Blueprint Architect (Wrangle Studio) ---
        if active_sidebar == "Wrangle Studio":
            selected_node = safe_input(input, "blueprint_node_clicked", None)
            stack = wrangle_studio.logic_stack.get()
            step_count = len(stack)

            node_info = ui.div(
                ui.p("No node selected. Click a TubeMap node to begin surgical focus.",
                     class_="text-muted small italic"),
                class_="p-2"
            )
            if selected_node:
                node_info = ui.div(
                    ui.div(
                        ui.span("🔬 ", class_="me-1"),
                        ui.span(f"Focused: {selected_node}", class_="fw-bold"),
                        class_="mb-1"
                    ),
                    ui.div(f"Logic stack: {step_count} step(s)", class_="text-muted small"),
                    class_="p-2 bg-white border rounded shadow-sm mb-2"
                )

            return ui.div(
                ui.card(
                    ui.card_header(
                        ui.div(ui.h5("Blueprint Surgeon", class_="mb-0"),
                               class_="d-flex justify-content-center w-100")
                    ),
                    ui.div(
                        node_info,
                        ui.hr(),
                        ui.h6("Active Logic Stack", class_="text-muted px-2"),
                        ui.output_ui("audit_nodes_tier3"),
                        class_="p-2"
                    ),
                    class_="mb-2 shadow-sm border-0"
                ),
                class_="sidebar-content p-0 d-flex flex-column h-100"
            )

        # --- 🏠 Home Theater (ADR-043 / ADR-044) ---
        if active_sidebar in ("Home", None, ""):
            return ui.div(
                ui.card(
                    ui.card_header(
                        ui.div(ui.h5("Pipeline Audit", class_="mb-0"),
                               class_="d-flex justify-content-center w-100")
                    ),
                    ui.div(
                        ui.h6("Tier 2 (Inherited)", class_="text-muted"),
                        ui.output_ui("audit_nodes_tier2"),
                        ui.hr(),
                        ui.h6("Tier 3 (User)", class_="text-muted"),
                        ui.output_ui("audit_nodes_tier3"),
                        class_="p-2"
                    ),
                    class_="mb-2 shadow-sm border-0"
                ),
                ui.div(
                    ui.output_ui("audit_stack_tools_ui"),
                    class_="mt-auto p-2"
                ),
                class_="sidebar-content p-0 d-flex flex-column h-100"
            )

        # --- 🖼️ Gallery ---
        if active_sidebar == "Gallery":
            return ui.div(
                ui.card(
                    ui.card_header(ui.h5("Gallery Explorer", class_="mb-0 text-center")),
                    ui.div(
                        ui.p("📚 Browse visual recipes.", class_="text-muted small p-2"),
                        ui.p("Select a recipe to copy its YAML into the Architect sandbox.",
                             class_="text-muted small px-2"),
                        class_="p-1"
                    ),
                    class_="mb-2 shadow-sm border-0"
                ),
                class_="sidebar-content p-0"
            )

        # --- 🛠️ Dev Studio ---
        if active_sidebar == "Dev Studio":
            return ui.div(
                ui.card(
                    ui.card_header(ui.h5("Dev Inspector", class_="mb-0 text-center")),
                    ui.div(
                        ui.p("🔧 Developer diagnostic tools.", class_="text-muted small p-2"),
                        class_="p-1"
                    ),
                    class_="mb-2 shadow-sm border-0"
                ),
                class_="sidebar-content p-0"
            )

        # --- Default fallback ---
        return ui.div(
            ui.p("—", class_="text-muted p-3 text-center"),
            class_="sidebar-content p-0"
        )

    @render.ui
    def system_tools_ui():
        return ui.div(
            ui.div(
                ui.p("Session Management", class_="ultra-small fw-bold mb-1"),
                ui.div(
                    ui.input_action_button(
                        "restore_session", "Restore Last Session", class_="btn-sm w-100 mb-1"),
                    ui.input_action_button(
                        "export_global", "Export Full Dataset", class_="btn-sm w-100"),
                ),
                class_="mb-3 px-2"
            ),
            ui.div(
                ui.p("Data Ingestion (ADR-031)", class_="ultra-small fw-bold mb-1"),
                ui.div(
                    ui.input_file("file_ingest", None, multiple=True, accept=[".yaml"]),
                    class_="upload-row mb-1"
                ),
                ui.input_action_button("btn_ingest", "🚀 Ingest Manifests", class_="w-100"),
                class_="px-2"
            )
        )

    @output
    @render.ui
    def sidebar_filters():
        try:
            lf = tier1_anchor()
            cols = lf.columns[:6]
            filters = []
            for col in cols:
                clean_id = col.replace(" ", "_").replace("(", "").replace(")", "")
                choices = ["All"] + \
                    sorted(lf.select(pl.col(col)).unique().collect()[col].to_list())
                filters.append(ui.card(
                    ui.input_select(f"filter_{clean_id}", f"Filter: {col}",
                                    choices=choices, selected="All"),
                    class_="mb-2 border-0 shadow-none bg-transparent"
                ))
            return ui.div(*filters)
        except Exception:
            return ui.div(ui.markdown("*Filters unavailable.*"))

    @output
    @render.plot
    def plot_reference():
        cfg = active_cfg()
        plot_ids = list(cfg.raw_config.get("plots", {}).keys())
        if not plot_ids:
            return None
        plot_id = plot_ids[0]

        proj = cfg.raw_config.get("id", input.project_id())
        coll = active_collection_id()
        cached_plot = bootloader.get_cached_asset(proj, coll, plot_id, "ref_plot")
        if cached_plot is not None:
            return cached_plot

        plt = viz_factory.render(tier_reference(), cfg.raw_config, plot_id)
        bootloader.set_cached_asset(proj, coll, plot_id, "ref_plot", plt)
        return plt

    @output
    @render.table
    def table_reference():
        return tier_reference().head(100).collect()

    @output
    @render.plot
    def plot_leaf():
        cfg = active_cfg()
        plot_ids = list(cfg.raw_config.get("plots", {}).keys())
        if not plot_ids:
            return None
        return viz_factory.render(tier3_leaf().lazy(), cfg.raw_config, plot_ids[0])

    @output
    @render.table
    def table_leaf():
        return tier3_leaf().head(5)

    @reactive.Effect
    @reactive.event(input.plot_leaf_brush)
    def handle_plot_brush():
        brush = input.plot_leaf_brush()
        if not brush:
            return
        cfg = active_cfg()
        plot_ids = list(cfg.raw_config.get("plots", {}).keys())
        if not plot_ids:
            return
        plot_id = plot_ids[0]
        mapping = cfg.raw_config["plots"][plot_id].get("mapping", {})
        x_col = mapping.get("x")
        y_col = mapping.get("y")

        outliers = lookup_anchor_rows(
            brush, anchor_path.get(), x_col=x_col, y_col=y_col)
        if outliers.is_empty():
            return

        m = ui.modal(
            ui.h4(f"Outlier Quick-View ({outliers.height} rows)"),
            ui.output_table("brush_results_table"),
            ui.modal_button("Close"),
            size="xl", easy_close=True
        )
        ui.modal_show(m)

        @output
        @render.table
        def brush_results_table():
            return outliers.head(20)

    @render.ui
    def comparison_mode_toggle_ui():
        """ADR-043: Comparison Mode toggle (persona-gated, deferred full impl to Phase 21-E)."""
        p = current_persona.get()
        if p in ["pipeline_exploration_advanced", "project_independent", "developer"]:
            return ui.div(
                ui.input_switch("comparison_mode", "Comparison Mode", value=False),
                class_="d-flex align-items-center me-3",
                style="height: 36px; padding-top: 4px;"
            )
        return ui.div()
