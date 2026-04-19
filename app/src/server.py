# app/src/server.py
from shiny import render, reactive, ui
import polars as pl
from pathlib import Path
from datetime import datetime
import pandas as pd
import shutil
import yaml
import os
import json
import base64

# Authority: Library Sovereignty (ADR-003)
from app.src.bootloader import bootloader
from app.modules.orchestrator import DataOrchestrator
from utils.config_loader import ConfigManager
from viz_factory.viz_factory import VizFactory
from app.modules.wrangle_studio import WrangleStudio
from app.modules.dev_studio import DevStudio
from app.modules.gallery_viewer import gallery_viewer
from transformer.data_wrangler import DataWrangler
from transformer.lookup import lookup_anchor_rows
from app.modules.exporter import SubmissionExporter
from utils.errors import SPARMVET_Error
from viz_gallery.gallery_manager import GalleryManager
import zipfile


def server(input, output, session):

    # 1. Reactive Manifest Authority (Universal Architecture)
    @reactive.Calc
    def active_cfg():
        project_id = input.project_id()
        cached = bootloader.get_cached_asset(
            project_id, "manifest", "raw", "cfg")
        if cached is not None:
            return cached

        path = bootloader.get_location("manifests") / f"{project_id}.yaml"
        cfg = ConfigManager(str(path))
        bootloader.set_cached_asset(project_id, "manifest", "raw", "cfg", cfg)
        return cfg

    @reactive.Calc
    def active_collection_id():
        """Agnostic Discovery: fetches the first collection in the manifest."""
        cfg = active_cfg()
        collections = list(cfg.raw_config.get("assembly_manifests", {}).keys())
        if not collections:
            return "Untitled_Collection"
        return collections[0]

    orchestrator = DataOrchestrator(
        manifests_dir=bootloader.get_location("manifests"),
        raw_data_dir=bootloader.get_location("raw_data")
    )
    viz_factory = VizFactory()

    # 2. State Management
    anchor_path = reactive.Value(None)
    theater_state = reactive.Value("split")  # split, plot, table
    # True when recipe has unsaved changes
    recipe_pending = reactive.Value(False)
    snapshot_recipe = reactive.Value([])     # Committed recipe after Apply

    # 2b. Module Orchestration (Phase 11-F)
    wrangle_studio = WrangleStudio(session.id)
    # Pass a lambda to reactively fetch Tier 1 columns
    wrangle_studio.define_server(
        input, output, session, lambda: tier1_anchor().columns)

    dev_studio = DevStudio()
    dev_studio.define_server(input, output, session)

    # Gallery Refresh Trigger (Phase 14-B)
    gallery_refresh_trigger = reactive.Value(0)

    # --- Global Helpers & State ─────────────────────────────────────────────
    current_persona = reactive.Value(bootloader.persona()) if callable(
        bootloader.persona) else reactive.Value(bootloader.persona)

    def show_sparmvet_error(err):
        """Unified SPARMVET Error Display."""
        if isinstance(err, SPARMVET_Error):
            title = f"❗ {err.context} Error"
            tip = err.tip
        else:
            title = "❗ Unexpected Error"
            tip = "Check system logs for architectural trace."

        ui.modal_show(
            ui.modal(
                ui.div(
                    ui.h3(title, class_="text-danger"),
                    ui.p(str(err), style="font-size: 1.1em; text-align: left;"),
                    ui.hr(),
                    ui.div(
                        ui.h5("💡 Debugging Tip", class_="fw-bold"),
                        ui.p(tip),
                        class_="p-3 rounded border",
                        style="background-color: #fff9c4; border-color: #f9eeb1; color: #5f5a3a;"
                    ),
                    class_="soft-note-modal"
                ),
                title="System Alert",
                easy_close=True,
                footer=ui.modal_button("Close")
            )
        )

    def _safe_input(input_obj, key, default):
        try:
            val = getattr(input_obj, key)()
            return val if val is not None else default
        except Exception:
            return default

    def _apply_tier2_transforms(lf, cfg):
        """Reusable wrapper for Tier 2 viz-factory baseline transforms."""
        # Introspect for first plot definition
        plot_ids = list(cfg.raw_config.get("plots", {}).keys())
        if not plot_ids:
            return lf

        plot_id = plot_ids[0]
        spec = cfg.raw_config["plots"][plot_id]

        # Apply viz-factory data-wrangling baseline
        lf = viz_factory.prepare_data(lf, spec)
        return lf

    def primary_keys():
        """Returns the list of primary keys from the active manifest."""
        cfg = active_cfg()
        return cfg.raw_config.get("primary_keys", [])

    # 3. Reactive Tab Components (Discovery Architecture)
    @render.ui
    def dynamic_tabs():
        """
        Routes to WrangleStudio, DevStudio, Gallery, or the Analysis Theater.
        ADR-029a / Phase 11-F Routing Hierarchy.
        """
        active_sidebar = _safe_input(input, "sidebar_nav", "Home")
        p = current_persona.get()
        state = theater_state.get()
        is_comparison = _safe_input(input, "comparison_mode", False)

        # 1. Module Routing (ADR-031 Compliance)
        if active_sidebar == "Wrangle Studio":
            return ui.div(wrangle_studio.render_ui(), class_="theater-container-main")
        if active_sidebar == "Dev Studio":
            return ui.div(dev_studio.render_ui(), class_="theater-container-main")
        if active_sidebar == "Gallery":
            return ui.div(gallery_viewer.render_explorer_ui(), class_="theater-container-main")

        # 'Viz' follows the same layout as the Theater but can have different headers
        # if active_sidebar == "Viz":
        #    ... (rest of the theater logic handles Home and Viz)

        # 2. Results Theater (Home) Logic
        # Developer persona 'Clean Slate' only applies to the Theater logic below if needed.
        # But we allow access to the Theater structure.

        # Force state for restricted personas (ADR-030)
        if p == "pipeline_static":
            state = "split"
        elif p == "pipeline_exploration_simple":
            if state == "split":
                state = "plot"

        # Dynamically fetch active collection Data
        try:
            proj_id = _safe_input(input, "project_id",
                                  bootloader.get_default_project())
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
            # Commit to reactive trigger for anchor discovery
            if out_path.exists():
                anchor_path.set(str(out_path))
        except Exception as e:
            return ui.div(ui.markdown(f"**Data Assembly Failed**: {e}"), class_="alert alert-danger")

        # Discover columns for filter generation
        all_cols = lf_full.columns

        # Metrics overview (Top ribbon)
        metrics = []
        try:
            count = lf_full.select(pl.len()).collect().item()
            metrics.append(ui.div(f"Rows: {count:,}",
                                  class_="metric-pill",
                                  style="margin-right: 12px;"))
            metrics.append(ui.div(f"Cols: {len(all_cols)}",
                                  class_="metric-pill",
                                  style="margin-right: 12px;"))
        except Exception:
            pass

        metrics_ui = ui.div(*metrics,
                            class_="d-flex align-items-center me-auto",
                            style="margin-left: 10px;") if metrics else None

        # --- Sub-Header: Branding & Persona Status ---
        theater_header = ui.div(
            ui.div(
                ui.div(
                    ui.h4(f"SPARMVET Dashboard ({active_sidebar})",
                          class_="mb-0"),
                    ui.tags.small(f"Manifest: {input.project_id()} | Persona: {p.replace('_', ' ').title()}",
                                  class_="text-muted"),
                    class_="flex-grow-1"
                ),
                class_="d-flex align-items-center"
            ),
            class_="theater-header-branding mb-2",
            style="padding: 10px 15px; background: white; border-bottom: 1px solid #dee2e6;"
        )

        # Shared Header Controls (Aggressive Alighment ADR-029a)
        header_controls = ui.div(
            ui.div(
                # Left Side: Metrics + Control Buttons
                ui.div(
                    ui.div(metrics_ui if metrics_ui else ui.div(),
                           style="display: flex; align-items: center;"),
                    ui.div(
                        ui.input_action_button("btn_max_plot", ui.tags.i(class_="bi bi-graph-up"),
                                               class_=f"control-btn {'active-view-btn' if state == 'plot' else ''}",
                                               title="Maximize Plot View"),
                        ui.input_action_button("btn_max_table", ui.tags.i(class_="bi bi-table"),
                                               class_=f"control-btn {'active-view-btn' if state == 'table' else ''}",
                                               title="Maximize Table View"),
                        ui.input_action_button("btn_reset_theater", ui.tags.i(class_="bi bi-grid-1x2"),
                                               class_=f"control-btn {'active-view-btn' if state == 'split' else ''}",
                                               title="Grid Quadrant View"),
                        class_="btn-group d-flex align-items-center ms-2",
                        style="height: 28px;"
                    ),
                    class_="d-flex align-items-center",
                    style="height: 36px;"
                ),
                # Right Side: Toggles
                ui.div(
                    ui.div(ui.input_switch("view_toggle", "Wide ↔ Long", value=False),
                           class_="d-flex align-items-center me-3", style="height: 36px; padding-top: 4px;"),
                    ui.output_ui("comparison_mode_toggle_ui"),
                    class_="d-flex align-items-center",
                    style="height: 36px;"
                ),
                class_="d-flex justify-content-between align-items-center w-100 bg-light border p-1 rounded",
                style="height: 38px;"
            ),
            class_="d-flex align-items-center w-100 p-0",
            style="margin-top: -2px; padding: 0 10px !important; height: 40px;"
        )

        # --- Theater Layout (2x2 Quadrant Philosophy - ADR-029a) ---

        # 🟢 Quadrant A: Reference Plot
        ref_plot_quad = ui.card(
            ui.card_header(ui.tags.span(
                "Plot Reference (T1/T2)", class_="reference-label")),
            ui.output_plot("plot_reference"),
            class_="shadow-sm flex-grow-1"
        )

        # 🟢 Quadrant B: Reference Table
        ref_table_quad = ui.card(
            ui.card_header(ui.tags.span(
                "Table Reference", class_="reference-label")),
            ui.div(ui.input_switch("ref_tier_switch",
                                   "T1 ↔ T2", value=False), class_="small"),
            ui.output_table("table_reference"),
            class_="shadow-sm flex-grow-1"
        )

        # 🔵 Quadrant C: Active Plot (T3)
        active_plot_quad = ui.card(
            ui.card_header(ui.h6("Active Visualization (Tier 3)"),
                           class_="d-flex justify-content-between"),
            ui.output_plot("plot_leaf", brush=ui.brush_opts(
                fill="#2196f3", opacity=0.3)),
            class_="shadow-sm flex-grow-1"
        )

        # 🔵 Quadrant D: Active Data Sandbox (Drawing #3 - Wider Column Picker)
        pkeys = primary_keys()
        data_cols = [c for c in all_cols if c not in pkeys]
        active_table_quad = ui.card(
            ui.card_header(ui.h6("Active Data Sandbox")),
            ui.div(
                ui.input_selectize("column_visibility_picker", None,
                                   choices=data_cols, selected=data_cols, multiple=True,
                                   options={"plugins": ["remove_button"]}),
                class_="px-2 pt-1 pb-1 w-100 column-picker-container"
            ),
            ui.output_table("table_leaf"),
            class_="shadow-sm flex-grow-1"
        )

        # Apply button with pending badge (ADR-029a Synchronization)
        apply_controls = ui.div(
            ui.div(ui.output_ui("recipe_pending_badge_ui"),
                   style="height: 31px; display: flex; align-items: center;"),
            ui.input_action_button(
                "btn_apply", "▶ Apply", class_="btn btn-success btn-sm", style="height: 31px;"),
            class_="apply-btn-container d-flex align-items-center justify-content-end mb-2 gap-2"
        )

        # Implementation logic for Grid States (ADR-030)
        if state == "plot":
            # Maximized Plot View
            active_col = ui.div(
                apply_controls, active_plot_quad, class_="active-pane h-100")
            reference_col = ui.div(
                ref_plot_quad, class_="reference-pane h-100")
        elif state == "table":
            # Maximized Table View
            active_col = ui.div(
                apply_controls, active_table_quad, class_="active-pane h-100")
            reference_col = ui.div(
                ref_table_quad, class_="reference-pane h-100")
        else:
            # Standard Quadrant Stack
            active_col = ui.div(
                apply_controls,
                ui.layout_columns(active_plot_quad,
                                  active_table_quad, col_widths=12),
                class_="active-pane h-100"
            )
            reference_col = ui.div(
                ui.layout_columns(
                    ref_plot_quad, ref_table_quad, col_widths=12),
                class_="reference-pane h-100"
            )

        is_triple = _safe_input(input, "triple_tier_mode", False)

        # Final Assembly (Comparison VS Single)
        if is_triple:
            theater_layout = ui.layout_columns(
                ui.div(ui.h6("T1: Raw"), ui.output_table(
                    "table_anchor"), class_="p-1 border rounded small"),
                ui.div(ui.h6("T2: Ref"), ui.output_table(
                    "table_reference"), class_="p-1 border rounded small"),
                ui.div(ui.h6("T3: Leaf"), ui.output_table(
                    "table_leaf"), class_="p-1 border rounded small"),
                col_widths=[4, 4, 4]
            )
        elif is_comparison:
            theater_layout = ui.layout_columns(
                reference_col, active_col, col_widths=[5, 7])
        else:
            theater_layout = active_col

        # Build manifest-driven tabs
        cfg = active_cfg()
        groups = cfg.raw_config.get("analysis_groups", {})
        extra_tabs = []

        for group_id, group_spec in groups.items():
            plot_ids = list(group_spec.get("plots", {}).keys())

            # --- 2. Sub-Tabs for individual plots ---
            plot_subtabs = []
            for p_id in plot_ids:
                plot_subtabs.append(
                    ui.nav_panel(
                        p_id.replace("_", " ").title(),
                        ui.card(
                            ui.output_plot(f"plot_group_{p_id}"),
                            class_="shadow-none border-0 mt-0",
                            style="min-height: 550px;"
                        )
                    )
                )

            if not plot_subtabs:
                group_content = ui.div(
                    ui.hr(class_="my-1"),
                    ui.p("No plots defined for this group.",
                         class_="text-muted p-4")
                )
            else:
                group_content = ui.div(
                    ui.div(
                        ui.navset_underline(
                            *plot_subtabs, id=f"subtabs_{group_id.replace(' ', '_')}"),
                        class_="px-3 pb-3"
                    )
                )

            # --- ID Sanitation Audit ---
            safe_id = group_id.replace(' ', '_').replace(
                '📊', 'QC').replace('💊', 'AMR').lower()
            extra_tabs.append(ui.nav_panel(
                group_spec.get("description", group_id),
                group_content,
                value=f"tab_{safe_id}"
            ))

        tabs = [
            ui.nav_panel("Theater", theater_layout),
            ui.nav_panel("Inspector", ui.output_table("full_data_table"))
        ] + extra_tabs

        return ui.div(
            theater_header,
            ui.navset_card_tab(
                *tabs,
                id="central_theater_tabs",
                header=header_controls
            ),
            class_="theater-container-main"
        )

    @render.ui
    def sidebar_nav_ui():
        perm = current_persona.get()

        # Persona-based sidebar masking (ADR-030)
        nav_items = [
            ui.nav_panel("Home", value="Home")
        ]

        if perm in ["pipeline_exploration_advanced", "project_independent", "developer"]:
            nav_items.append(ui.nav_panel(
                "Blueprint Architect", value="Wrangle Studio"))
            nav_items.append(ui.nav_panel("Analysis Theater", value="Viz"))

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
        active_sidebar = _safe_input(input, "sidebar_nav", "Home")

        # 🟢 Discovery Mode (Gallery)
        if active_sidebar == "Gallery":
            return ui.div(
                ui.p("Discovery Mode Active", class_="text-muted p-4 italic"),
                ui.p("Choose a visual recipe to begin.",
                     class_="text-muted px-4 small")
            )

        # 🔵 Manifest Workbench (Wrangle Studio)
        if active_sidebar == "Wrangle Studio":
            return ui.accordion(
                ui.accordion_panel(
                    "Blueprint Discovery",
                    ui.input_select("stored_manifest_selector", "1. Master Manifest:",
                                    choices=["Scanning config/..."]),
                    ui.input_select("dataset_pipeline_selector", "2. Target Blueprint Component:",
                                    choices=["Select a Master first"]),
                    ui.div(
                        ui.tags.small(
                            "Info: This selects a specific processing track (e.g. a dataset or assembly) from the Master Manifest to load into your workbench.", class_="text-muted"),
                        class_="mb-2"
                    ),
                    ui.input_action_button("btn_import_manifest", "📥 Import (Replace)",
                                           class_="btn-info btn-sm w-100 mt-2"),
                    ui.input_action_button("btn_save_internal", "💾 Save to Project",
                                           class_="btn-success btn-sm w-100 mt-1"),
                    icon=ui.tags.i(class_="bi bi-search")
                ),
                ui.accordion_panel(
                    "External Exchange",
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
            )

        # 🏠 Standard Operation Sidebar (Home/Viz)
        try:
            proj_choices = list(bootloader.available_projects.keys())
            def_proj = bootloader.get_default_project()
        except:
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

    # 5. Reactive Tiers (ADR-024 / ADR-031)

    @reactive.Calc
    def tier1_anchor():
        """Scans the physical Parquet anchor (Predicate Pushdown ready)."""
        project_id = _safe_input(input, "project_id", "default")
        coll_id = active_collection_id()

        cached_lf = bootloader.get_cached_asset(
            project_id, coll_id, "anchor", "lf")
        if cached_lf is not None:
            return cached_lf

        path = anchor_path.get()
        if not path:
            return pl.DataFrame().lazy()

        lf = pl.scan_parquet(path)
        bootloader.set_cached_asset(project_id, coll_id, "anchor", "lf", lf)
        return lf

    @reactive.Calc
    def tier_reference():
        lf = tier1_anchor()
        show_tier2 = _safe_input(input, "ref_tier_switch", False)
        if show_tier2:
            cfg = active_cfg()
            lf = _apply_tier2_transforms(lf, cfg)
        return lf

    @reactive.Calc
    @reactive.event(input.btn_apply)
    def tier3_leaf():
        lf = tier1_anchor()
        cfg = active_cfg()
        recipe = snapshot_recipe.get()
        show_long = _safe_input(input, "view_toggle", False)

        # Stage 1: Pre-transform filters
        pre_steps = [s for s in recipe if s.get("stage") == "pre_transform"]
        for step in pre_steps:
            action = step.get("action", "")
            col = step.get("column")
            val = step.get("value")
            if action == "filter_eq" and col and val is not None:
                try:
                    lf = lf.filter(pl.col(col) == val)
                except Exception:
                    pass

        # Global Sidebar Filters
        for col in lf.columns[:10]:
            clean_col = col.replace(" ", "_").replace("(", "").replace(")", "")
            try:
                val = getattr(input, f"filter_{clean_col}")()
                if val and val != "All":
                    lf = lf.filter(pl.col(col) == val)
            except Exception:
                pass

        # Stage 2: Inherited Tier 2 viz transforms
        if show_long:
            lf = _apply_tier2_transforms(lf, cfg)

        # Stage 3: Post-transform user steps
        post_steps = [s for s in recipe if s.get("stage") == "post_transform"]
        for step in post_steps:
            action = step.get("action", "")
            if action == "select_columns":
                cols_select = step.get("columns")
                if cols_select:
                    try:
                        lf = lf.select(cols_select)
                    except Exception:
                        pass

        # Column visibility
        try:
            visible_cols = input.column_visibility_picker()
            if visible_cols:
                pkeys = primary_keys()
                final_cols = list(set(visible_cols) | set(pkeys))
                ordered_cols = [c for c in lf.columns if c in final_cols]
                lf = lf.select(ordered_cols)
        except Exception:
            pass

        # Apply WrangleStudio recipe
        lf = wrangle_studio.apply_logic(lf)

        result = lf.collect()
        if result.height == 0:
            ui.notification_show(
                "⚠️ No data. Adjust filters.", type="warning", duration=10)

        recipe_pending.set(False)
        return result

    @reactive.Effect
    @reactive.event(input.btn_apply)
    def handle_apply():
        current_recipe = wrangle_studio.logic_stack.get()
        snapshot_recipe.set(current_recipe)

    @reactive.Effect
    def track_recipe_changes():
        _ = wrangle_studio.apply_logic
        recipe_pending.set(True)

    @output
    @render.ui
    def recipe_pending_badge_ui():
        if recipe_pending.get():
            return ui.div("⏳ Pending", class_="recipe-pending-badge text-center")
        return ui.div()

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
        cached_plot = bootloader.get_cached_asset(
            proj, coll, plot_id, "ref_plot")
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

    @output
    @render.ui
    def audit_nodes_tier3():
        cfg = active_cfg()
        collection_id = active_collection_id()
        nodes = [
            ui.div(f"Project: {cfg.raw_config.get('id')}",
                   class_="audit-node-tier2"),
            ui.div(f"Collection: {collection_id}", class_="audit-node-tier2"),
        ]
        if "metadata_schema" in cfg.raw_config:
            nodes.append(ui.div(f"Anchor: {collection_id}.parquet (w/ Metadata)",
                         class_="audit-node-tier3"))
        else:
            nodes.append(ui.div(f"Anchor: {collection_id}.parquet (Standalone)",
                         class_="audit-node-tier3"))

        active_nodes = wrangle_studio.logic_stack.get()
        if active_nodes:
            nodes.append(ui.hr())
            nodes.append(ui.h6("Session Transformations (Tier 3)"))
            for i, node in enumerate(active_nodes):
                action = node.get("action", "unknown")
                comment = node.get("comment", "No comment")
                nodes.append(ui.tooltip(
                    ui.div(
                        ui.div(f"⚡ {action}", class_="fw-bold"),
                        ui.div(f"💬 {comment}", style="font-size: 0.8em;"),
                        class_="audit-node-tier3"
                    ),
                    f"Action: {action}", placement="left", id=f"node_tt_{i}"
                ))
        return ui.div(*nodes)

    @output
    @render.ui
    def audit_nodes_tier2():
        cfg = active_cfg()
        collection_id = active_collection_id()
        collections = cfg.raw_config.get("assembly_manifests", {})
        recipe = []
        if collection_id in collections:
            raw_recipe = collections[collection_id].get("recipe", [])
            recipe = DataWrangler._resolve_tier(raw_recipe, "tier1")

        if not recipe:
            return ui.div(ui.div("No Tier 2 steps defined.", class_="audit-node-tier2"))

        nodes = []
        for step in recipe:
            action = step.get("action", "unknown")
            label = step.get("label") or step.get("right_ingredient") or action
            nodes.append(ui.tooltip(
                ui.div(f"[Tier 2] {action}: {label}",
                       class_="audit-node-tier2"),
                f"Action: {action}", placement="left"
            ))
        return ui.div(*nodes)

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
                ui.p("Data Ingestion (ADR-031)",
                     class_="ultra-small fw-bold mb-1"),
                ui.div(
                    ui.input_file("file_ingest", None, multiple=True,
                                  accept=[".yaml"]),
                    class_="upload-row mb-1"
                ),
                ui.input_action_button(
                    "btn_ingest", "🚀 Ingest Manifests", class_="w-100"),
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
                clean_id = col.replace(" ", "_").replace(
                    "(", "").replace(")", "")
                choices = ["All"] + \
                    sorted(lf.select(pl.col(col)).unique(
                    ).collect()[col].to_list())
                filters.append(ui.card(
                    ui.input_select(f"filter_{clean_id}", f"Filter: {col}",
                                    choices=choices, selected="All"),
                    class_="mb-2 border-0 shadow-none bg-transparent"
                ))
            return ui.div(*filters)
        except Exception:
            return ui.div(ui.markdown("*Filters unavailable.*"))

    @reactive.Effect
    @reactive.event(input.btn_max_plot)
    def handle_max_plot():
        theater_state.set("plot")

    @reactive.Effect
    @reactive.event(input.btn_max_table)
    def handle_max_table():
        theater_state.set("table")

    @reactive.Effect
    @reactive.event(input.btn_reset_theater)
    def handle_reset_theater():
        theater_state.set("split")

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

    # --- 🔬 Gallery Taxonomy 'Select All' Logic ---
    @reactive.Effect
    @reactive.event(input.gallery_all_family)
    def _sync_family_all():
        choices = ["Distribution", "Correlation", "Comparison",
                   "Ranking", "Evolution", "Part-to-Whole"]
        selected = choices if input.gallery_all_family() else []
        ui.update_checkbox_group("gallery_filter_family", selected=selected)

    @reactive.Effect
    @reactive.event(input.gallery_all_pattern)
    def _sync_pattern_all():
        checked = input.gallery_all_pattern()
        choices = [
            "1 Numeric", "2 Numeric", "1 Numeric, 1 Categorical",
            "1 Numeric, 2 Categorical", "1 Numeric, 2 Categorical (Faceted)",
            "2 Numeric, 1 Categorical (Faceted)", "Numeric-Numeric"
        ]
        ui.update_checkbox_group(
            "gallery_filter_pattern", selected=choices if checked else [])

    # --- Gallery Initialization (ADR-037) ---
    @reactive.Effect
    def _init_gallery_selector():
        """Ensure all plots are selected by default on startup."""
        index_path = bootloader.get_location("gallery") / "gallery_index.json"
        if index_path.exists():
            with open(index_path, "r") as f:
                idx = json.load(f)
            registry = idx.get("registry", {})
            choices = {rid: entry["name"] for rid, entry in registry.items()}
            choices = dict(sorted(choices.items(), key=lambda item: item[1]))
            ui.update_select("gallery_recipe_select", choices=choices)

    @reactive.Effect
    @reactive.event(input.gallery_all_difficulty)
    def _sync_difficulty_all():
        choices = ["Simple", "Intermediate", "Advanced"]
        selected = choices if input.gallery_all_difficulty() else []
        ui.update_checkbox_group(
            "gallery_filter_difficulty", selected=selected)

    @reactive.Effect
    @reactive.event(input.btn_clone_gallery)
    def handle_gallery_clone():
        recipe_id = _safe_input(input, "gallery_recipe_select", None)
        if not recipe_id:
            return

        index_path = bootloader.get_location("gallery") / "gallery_index.json"
        if not index_path.exists():
            return

        try:
            with open(index_path, "r") as f:
                idx = json.load(f)

            recipe_entry = idx["registry"].get(recipe_id)
            if not recipe_entry:
                return

            file_path = recipe_entry["path"]
            with open(file_path, "r") as f:
                manifest = yaml.safe_load(f)

            wrangling_raw = manifest.get("wrangling", {})
            # Handle both list and dict formats for backward compatibility
            tier3_raw = wrangling_raw.get("tier3", []) if isinstance(
                wrangling_raw, dict) else wrangling_raw

            new_steps = DataWrangler._resolve_tier(tier3_raw, "all")
            valid_nodes = []
            for step in new_steps:
                action = step.get("action", "unknown")
                params = {k: v for k, v in step.items() if k != "action"}
                valid_nodes.append({
                    "action": action,
                    "params": params,
                    "comment": f"Ghost-loaded from Reference: {recipe_id}"
                })
            wrangle_studio.logic_stack.set(valid_nodes)
            ui.notification_show(
                f"✅ Recipe '{recipe_id}' cloned to Sandbox.", type="success")
        except Exception as e:
            print(f"❌ Clone failed: {e}")

    # --- Gallery Content Resolution (ADR-037) ---
    @reactive.Calc
    def _gallery_active_metadata():
        rid = _safe_input(input, "gallery_recipe_select", None)
        if not rid:
            return None
        index_path = bootloader.get_location("gallery") / "gallery_index.json"
        if not index_path.exists():
            return None
        with open(index_path, "r") as f:
            idx = json.load(f)
        return idx["registry"].get(rid)

    @output
    @render.ui
    def gallery_preview_img():
        meta = _gallery_active_metadata()
        if not meta:
            return ui.div("Select a recipe to view preview.", class_="p-5 text-muted")

        path_str = meta.get("path")
        if not path_str:
            return ui.div("Path missing in index.", class_="text-danger")

        img_path = Path(path_str).parent / "preview_plot.png"
        if img_path.exists():
            try:
                with open(img_path, "rb") as f:
                    encoded = base64.b64encode(f.read()).decode("utf-8")
                return ui.div(
                    ui.img(src=f"data:image/png;base64,{encoded}",
                           style="max-width: 100%; border: 1px solid #dee2e6; border-radius: 4px; box-shadow: 0 4px 12px rgba(0,0,0,0.1);"),
                    class_="p-3 text-center"
                )
            except Exception as e:
                return ui.div(f"Error loading preview: {e}", class_="text-danger")
        return ui.div("No preview image found (.png)", class_="p-5 text-muted")

    @output
    @render.table(index=False)
    def gallery_static_data():
        """Render a clean, left-aligned table without row numbers (ADR-033)."""
        meta = _gallery_active_metadata()
        if not meta:
            return None
        path_str = meta.get("path")
        if not path_str:
            return None

        data_path = Path(path_str).parent / "example_data.tsv"
        if data_path.exists():
            try:
                # Polars maintains high-density left alignment by default in Shiny's render.table
                return pl.read_csv(data_path, separator="\t")
            except Exception as e:
                # Fallback to an empty DF with error message for debugging
                return pl.DataFrame({"Error": [f"Could not load data: {e}"]})
        return None

    @output
    @render.text
    def gallery_yaml_preview():
        meta = _gallery_active_metadata()
        if not meta:
            return "Select a recipe"
        path_str = meta.get("path")
        if not path_str:
            return "Manifest path not found"

        if Path(path_str).exists():
            with open(path_str, "r") as f:
                return f.read()
        return "Source YAML not found"

    @output
    @render.ui
    def gallery_md_content():
        meta = _gallery_active_metadata()
        if not meta:
            return ui.div("Select an entry to view guidance.", class_="p-4 text-center text-muted")

        path_str = meta.get("path")
        if not path_str:
            return ui.div("Metadata path not found", class_="text-danger")

        md_path = Path(path_str).parent / "recipe_meta.md"
        if md_path.exists():
            with open(md_path, "r") as f:
                return ui.div(ui.markdown(f.read()), class_="gallery-guidance-styled")
        return ui.div("Educational metadata (recipe_meta.md) missing.", class_="alert alert-warning")

    @reactive.Effect
    @reactive.event(input.btn_apply_gallery_filters, input.sidebar_nav)
    def _update_gallery_options():
        """
        High-Performance Filtering Gate (ADR-037).
        TRIGGERED BY: 'Apply' button OR Tab switch to Gallery.
        """
        # 1. Check if we are actually in the Gallery (don't recalc if switching away)
        if input.sidebar_nav() != "Gallery":
            return
        index_path = bootloader.get_location("gallery") / "gallery_index.json"
        if not index_path.exists():
            ui.notification_show("Indexer not found.", type="error")
            return

        with open(index_path, "r") as f:
            idx = json.load(f)

        # 2. Collect Filter Inputs
        sel_families = input.gallery_filter_family()
        sel_patterns = input.gallery_filter_pattern()
        sel_difficulties = input.gallery_filter_difficulty()

        ui.notification_show("🔍 Filtering recipes...",
                             duration=1, type="message")

        # 2. Pivot-Set Intersection
        registry = idx["registry"]
        pivot = idx["pivot"]

        family_matches = set()
        for f in sel_families:
            family_matches.update(pivot["by_family"].get(f, []))

        pattern_matches = set()
        for p in sel_patterns:
            pattern_matches.update(pivot["by_pattern"].get(p, []))

        difficulty_matches = set()
        for d in sel_difficulties:
            difficulty_matches.update(pivot["by_difficulty"].get(d, []))

        # Perform the final Multi-Set Intersection
        valid_ids = family_matches & pattern_matches & difficulty_matches

        # 3. Build UI Choices
        choices = {vid: registry[vid]["name"] for vid in valid_ids}
        choices = dict(sorted(choices.items(), key=lambda item: item[1]))

        # 4. Push Update to UI
        ui.update_select("gallery_recipe_select",
                         label=ui.span(
                             f"Visual Gallery ({len(choices)} matched)", class_="fw-bold text-success"),
                         choices=choices,
                         selected=None)

        if not choices:
            ui.notification_show(
                "⚠️ No matches found for these filters.", type="warning")

    @output
    @render.ui
    def gallery_browser_anchor():
        """Placeholder for any additional anchor logic if needed."""
        return None

    @reactive.Effect
    @reactive.event(input.btn_ingest)
    def handle_ingest():
        files = _safe_input(input, "file_ingest", None)
        if not files:
            return
        ui.notification_show("⏳ Ingesting...", type="message")
        manifest_dir = bootloader.get_location("manifests")
        for f in files:
            name = f['name']
            path = Path(f['datapath'])
            if name.endswith(".yaml"):
                shutil.copy(path, manifest_dir / name)
        bootloader.__init__(persona=current_persona.get())
        ui.update_select("project_id", choices=list(
            bootloader.available_projects.keys()))
        ui.notification_show("✅ Ingestion complete.", type="success")

    @reactive.Effect
    @reactive.event(input.persona_selector)
    def update_persona_context():
        new_persona = input.persona_selector()
        if new_persona:
            current_persona.set(new_persona)
            bootloader.__init__(persona=new_persona)
            ui.notification_show(f"Persona: {new_persona}", type="message")

    # --- 🏗️ Phase 18: Wrangle Studio Manifest Management ---
    @reactive.Effect
    @reactive.event(input.sidebar_nav)
    def _init_wrangle_manifests():
        """Auto-discovery of Master manifests in config/ directory."""
        if input.sidebar_nav() != "Wrangle Studio":
            return

        config_dir = Path("config/manifests/pipelines")
        if not config_dir.exists():
            config_dir = Path("config")

        all_yamls = list(config_dir.rglob("*.yaml"))
        master_manifests = []
        for path in all_yamls:
            parent_name = path.parent.name
            possible_master = path.parent.parent / f"{parent_name}.yaml"
            if possible_master.exists():
                continue
            master_manifests.append(str(path))

        master_manifests.sort()
        ui.update_select("stored_manifest_selector",
                         choices=master_manifests,
                         selected=master_manifests[0] if master_manifests else None)

    @reactive.Effect
    @reactive.event(input.stored_manifest_selector)
    def _update_dataset_pipelines():
        """Discovers individual dataset workflows within a master manifest."""
        path = input.stored_manifest_selector()
        if not path or not Path(path).exists():
            return

        try:
            cfg = ConfigManager(path)
            schemas = list(cfg.raw_config.get("data_schemas", {}).keys())
            additional = list(cfg.raw_config.get(
                "additional_datasets_schemas", {}).keys())
            assemblies = list(cfg.raw_config.get(
                "assembly_manifests", {}).keys())
            metadata = [
                "metadata_schema"] if "metadata_schema" in cfg.raw_config else []

            all_pipelines = schemas + additional + assemblies + metadata
            ui.update_select("dataset_pipeline_selector",
                             choices=all_pipelines)
        except Exception:
            ui.update_select("dataset_pipeline_selector",
                             choices=["Error parsing manifest"])

    @reactive.Effect
    @reactive.event(input.btn_import_manifest)
    def _handle_manifest_import():
        """Parses a specific dataset pipeline from a master YAML (REPLACE)."""
        path = input.stored_manifest_selector()
        pipeline_id = input.dataset_pipeline_selector()

        if not path or not Path(path).exists():
            return

        try:
            cfg = ConfigManager(path)
            wrangling = _extract_wrangling_for_id(cfg, pipeline_id)
            nodes = _parse_logic_to_nodes(wrangling, f"Master: {pipeline_id}")
            wrangle_studio.logic_stack.set(nodes)

            # Populate Architect Meta-Tiers (ADR-031 Expansion)
            import yaml as pyyaml
            wrangle_studio.active_raw_yaml.set(pyyaml.dump(
                cfg.raw_config, default_flow_style=False, sort_keys=False))

            target = cfg.raw_config.get(
                "data_schemas", {}).get(pipeline_id, {})
            if not target:
                target = cfg.raw_config.get(
                    "additional_datasets_schemas", {}).get(pipeline_id, {})
            if not target:
                target = cfg.raw_config.get(
                    "assembly_manifests", {}).get(pipeline_id, {})

            in_fields = target.get("input_fields", [])
            out_fields = target.get("output_fields", [])
            wrangle_studio.active_fields.set(
                {"input": in_fields, "output": out_fields})

            ui.notification_show(
                f"✅ Imported {len(nodes)} steps from '{pipeline_id}'", type="message")
        except Exception as e:
            ui.notification_show(f"❌ Import failed: {e}", type="error")

    @reactive.Effect
    @reactive.event(input.btn_upload_replace)
    def _handle_upload_replace():
        file_info = input.manifest_uploader()
        if not file_info:
            return
        try:
            cfg = ConfigManager(file_info[0]["datapath"])
            wrangling = cfg.raw_config.get("wrangling", {})
            nodes = _parse_logic_to_nodes(wrangling, "Uploaded (Replace)")
            wrangle_studio.logic_stack.set(nodes)
            ui.notification_show("✅ Stack Replaced.", type="success")
        except Exception as e:
            ui.notification_show(f"❌ Upload failed: {e}", type="error")

    @reactive.Effect
    @reactive.event(input.btn_upload_append)
    def _handle_upload_append():
        file_info = input.manifest_uploader()
        if not file_info:
            return
        try:
            cfg = ConfigManager(file_info[0]["datapath"])
            wrangling = cfg.raw_config.get("wrangling", {})
            new_nodes = _parse_logic_to_nodes(wrangling, "Uploaded (Append)")
            current_stack = wrangle_studio.logic_stack.get()
            wrangle_studio.logic_stack.set(current_stack + new_nodes)
            ui.notification_show(
                f"➕ Appended {len(new_nodes)} nodes.", type="success")
        except Exception as e:
            ui.notification_show(f"❌ Append failed: {e}", type="error")

    def _extract_wrangling_for_id(cfg, lid):
        """Helper to find wrangling block in complex manifest."""
        target = cfg.raw_config.get("data_schemas", {}).get(lid)
        if not target:
            target = cfg.raw_config.get(
                "additional_datasets_schemas", {}).get(lid)
        if not target:
            target = cfg.raw_config.get("assembly_manifests", {}).get(lid)
        if not target and lid == "metadata_schema":
            target = cfg.raw_config.get("metadata_schema")

        if not target:
            return {}
        return target.get("wrangling", target.get("recipe", {}))

    def _parse_logic_to_nodes(wrangling, source_name):
        """
        Normalizes potentially flat manifest nodes into structured UI nodes.
        ADR-031: Supports both Structure (params: {}) and Flat (top-level keys) formats.
        """
        nodes = []
        raw_list = []

        if isinstance(wrangling, list):
            raw_list = wrangling
        elif isinstance(wrangling, dict):
            # Extract from nested tiers if present
            for tier in ["tier1", "tier2", "tier3"]:
                raw_list.extend(wrangling.get(tier, []))

        for node in raw_list:
            if not isinstance(node, dict):
                continue

            n = node.copy()
            action = n.pop("action", "unknown_action")
            comment = n.pop("comment", source_name)

            # If 'params' already exists, use it; otherwise, everything else becomes params
            params = n.pop("params", n)

            nodes.append({
                "action": action,
                "params": params,
                "comment": comment
            })

        return nodes

    @reactive.Effect
    @reactive.event(input.btn_save_internal)
    def _handle_manifest_save_internal():
        path_str = input.stored_manifest_selector()
        if not path_str or not Path(path_str).exists():
            return
        try:
            with open(path_str, "r") as f:
                content = yaml.safe_load(f) or {}
            nodes = wrangle_studio.logic_stack.get()
            if "wrangling" not in content:
                content["wrangling"] = {}
            content["wrangling"]["tier1"] = []
            content["wrangling"]["tier2"] = []
            content["wrangling"]["tier3"] = nodes
            with open(path_str, "w") as f:
                yaml.dump(content, f, default_flow_style=False,
                          sort_keys=False)
            ui.notification_show(
                f"✅ Saved to {Path(path_str).name}", type="success")
        except Exception as e:
            ui.notification_show(f"❌ Save failed: {e}", type="error")

    @render.download(filename=lambda: f"exported_manifest_{datetime.now().strftime('%Y%m%d_%H%M%S')}.yaml")
    def btn_download_manifest():
        nodes = wrangle_studio.logic_stack.get()
        manifest_data = {"wrangling": {
            "tier1": [], "tier2": [], "tier3": nodes}}
        import io
        buf = io.StringIO()
        yaml.dump(manifest_data, buf,
                  default_flow_style=False, sort_keys=False)
        yield buf.getvalue()

    @render.ui
    def comparison_mode_toggle_ui():
        p = current_persona.get()
        if p in ["pipeline_exploration_advanced", "project_independent", "developer"]:
            return ui.div(ui.input_switch("comparison_mode", "Comparison Mode", value=False),
                          class_="d-flex align-items-center me-3", style="height: 36px; padding-top: 4px;")
        return ui.div()
