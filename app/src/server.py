# app/src/server.py
from shiny import render, reactive, ui
import polars as pl
from pathlib import Path
from datetime import datetime
import pandas as pd
import shutil
import yaml
import os

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
        path = bootloader.get_location("manifests") / f"{project_id}.yaml"
        return ConfigManager(str(path))

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

    def _safe_input(inp, name, default=None):
        """Safely reads an input that may not exist (e.g., persona-gated toggles)."""
        try:
            return getattr(inp, name)()
        except Exception:
            return default

    def is_feature_enabled(feature_key: str) -> bool:
        """Reactive feature gate helper (ADR-026/031)."""
        # Trigger dependency on current_persona
        _ = current_persona.get()
        return bootloader.is_enabled(feature_key)

    def _apply_tier2_transforms(lf: pl.LazyFrame, cfg) -> pl.LazyFrame:
        """
        Applies Tier 2 viz transforms (long-format / aggregation) from the manifest.
        ADR-024: Tier 2 MUST NOT filter rows — only reshape/aggregate.
        Returns a LazyFrame (not collected).
        """
        if cfg is None or cfg.raw_config is None:
            return lf

        wrangling_block = cfg.raw_config.get("wrangling")
        if isinstance(wrangling_block, dict):
            tier2_steps = wrangling_block.get("tier2", [])
        else:
            tier2_steps = cfg.raw_config.get("tier2_transforms", [])

        if not tier2_steps:
            return lf

        # WIDE-TO-LONG GUARD: If filtered down to zero rows, log and skip reshaping to avoid schema collapse
        try:
            # We must collect to check count, but we do it as small as possible
            count_df = lf.select(pl.len()).collect()
            count = count_df.item()
            if count == 0:
                print(
                    "⚠️ Wide-to-Long Guard: Zero rows detected before Tier 2. Skipping transforms.")
                return lf
        except Exception as e:
            print(f"⚠️ Guard check failed: {e}")

        # Real implementation: Use DataWrangler with an identity schema for Tier 2
        wrangler = DataWrangler(data_schema={})
        return wrangler.run(lf, tier2_steps)

    # 3. Initialization Task (Tier 1 Materialization)
    @reactive.Effect
    @reactive.event(input.project_id)
    def init_data():
        ui.notification_show(
            "🚀 Initializing Tier 1 Data Ingestion...", type="message")

        project_id = input.project_id()
        collection_id = active_collection_id()
        output_file = bootloader.get_location(
            "curated_data") / f"{collection_id}.parquet"

        try:
            orchestrator.materialize_tier1(
                project_id=project_id,
                collection_id=collection_id,
                output_path=output_file
            )
            anchor_path.set(str(output_file))
            ui.notification_show(
                f"✅ {collection_id} Materialized.", type="message")
        except Exception as e:
            show_sparmvet_error(e)

    # 4. Agnostic Dynamic Discovery (ADR-029b)
    @output
    @render.text
    def app_title():
        cfg = active_cfg()
        info = cfg.raw_config.get('info', {})
        name = info.get('display_name') or info.get(
            'name') or info.get('title')
        if not name:
            name = f"Untitled Project - {input.project_id()}.yaml"
        return f"SPARMVET_VIZ: {name}"

    # 2b. Persona & Feature Reactivity (ADR-026, ADR-029a)

    @output
    @render.ui
    def comparison_mode_toggle_ui():
        """Renders Comparison and Triple-Tier switches if persona permits."""
        if not is_feature_enabled("comparison_mode_enabled"):
            return ui.div()
        return ui.div(
            ui.input_switch("comparison_mode",
                            "⚡ Comparison Mode", value=False),
            ui.input_switch("triple_tier_mode",
                            "🧬 Triple-Tier Grid", value=False),
            class_="d-flex gap-3 align-items-center"
        )

    @output
    @render.ui
    def sidebar_nav_ui():
        """Agnostic Discovery: Dynamically builds Sidebar nav based on Persona features."""
        tabs = [ui.nav_panel("Hub", ui.div(class_="p-2"))]

        if is_feature_enabled("wrangle_studio_enabled"):
            tabs.append(ui.nav_panel("Wrangle Studio", ui.div(
                id="wrangle_studio_sidebar_anchor")))

        tabs.append(ui.nav_panel("Viz", ui.div(class_="p-2")))

        if is_feature_enabled("developer_mode_enabled"):
            tabs.append(ui.nav_panel("Dev Studio", ui.div(class_="p-2")))

        if is_feature_enabled("gallery_enabled"):
            tabs.append(ui.nav_panel("Gallery", ui.div(class_="p-2")))

        return ui.navset_underline(*tabs, id="sidebar_nav")

    @output
    @render.ui
    def system_tools_ui():
        """Reactive System Tools: Personas, Ingest, Export."""
        is_dev = is_feature_enabled("developer_mode_enabled")

        # Tools nested in a card structure matching ui.py aesthetics
        content = [
            ui.card_header(ui.h5("System Tools", class_="mb-0")),
            ui.div(
                ui.div(
                    ui.input_select("persona_selector", "Persona Profile:",
                                    {
                                        "pipeline-static": "1. Pipeline-static",
                                        "pipeline-exploration-simple": "2. Pipeline-Exploration-simple",
                                        "pipeline-exploration-advanced": "3. Pipeline-Exploration-advanced",
                                        "project-independent": "4. Project-independent",
                                        "developer": "5. Developer-mode"
                                    },
                                    # Use the actual reactive persona state
                                    selected=current_persona.get()),
                    ui.hr()
                ) if is_dev else ui.div(),

                # ADR-026/031: Gated Import Helper
                ui.div(
                    ui.input_file("file_ingest", "Upload Data/Manifests",
                                  multiple=True,
                                  accept=[".xlsx", ".csv", ".tsv", ".yaml", ".zip"]),
                    ui.input_action_button(
                        "btn_ingest", "🚀 Ingest Bundle", class_="btn-outline-primary w-100"),
                    ui.hr()
                ) if is_feature_enabled("import_helper_enabled") else ui.div(),

                # ADR-031: Gated Export
                ui.input_action_button(
                    "export_global", "📦 Export", class_="btn-primary w-100 mt-2") if is_feature_enabled("export_bundle_enabled") else ui.div(),
                class_="p-3"
            )
        ]
        return ui.card(*content, class_="mb-4 shadow-sm")

    @output
    @render.ui
    def audit_stack_tools_ui():
        """Gated Audit Stack tools (Gallery and Session Reset)."""
        btns = []
        if is_feature_enabled("gallery_enabled"):
            btns.append(ui.input_action_button(
                "btn_gallery_open_submission", "🌟 Gallery Submit", class_="btn-success w-100 mb-2"))

        btns.append(ui.input_action_button(
            "restore_session", "🔄 Reset Sync", class_="btn-outline-secondary w-100"))

        return ui.div(*btns)

    # 2c. The Mandatory Audit Gatekeeper (The Gate)
    @reactive.Calc
    def is_recipe_valid():
        """Verifies EVERY node in the Tier 3 stack has a comment justification."""
        stack = wrangle_studio.logic_stack.get()
        if not stack:
            # Empty stack is valid (Identity Case)
            return True
        for node in stack:
            comment = node.get("comment", "").strip()
            if not comment:
                return False
        return True

    @reactive.Effect
    def gate_apply_button():
        """Dynamically enables/disables btn_apply based on recipe health."""
        # Contract: Disabled if no pending changes OR invalid comments
        pending = recipe_pending.get()
        valid = is_recipe_valid()

        btn_label = "▶ Apply" if valid else "⚠️ Comments Missing"
        btn_class = "btn-success" if valid else "btn-secondary"

        ui.update_action_button(
            "btn_apply", label=btn_label, disabled=not (pending and valid))

    # --- Agnostic Discovery: Plot Output Registration (ADR-003, ADR-029b) ---
    def _discover_all_plots():
        ids = set()
        m_dir = bootloader.get_location("manifests")
        for p in m_dir.glob("*.yaml"):
            try:
                with open(p, "r") as f:
                    mf = yaml.safe_load(f)
                if not mf:
                    continue
                if "plots" in mf:
                    ids.update(mf["plots"].keys())
                for g in mf.get("analysis_groups", {}).values():
                    if "plots" in g:
                        ids.update(g["plots"].keys())
            except:
                pass
        return list(ids)

    # Register EVERY possible plot ID found across the workspace
    discovered_plots = _discover_all_plots()
    print(
        f"🔍 [Agnostic Discovery] Found {len(discovered_plots)} unique plot IDs: {discovered_plots}")

    for p_id in discovered_plots:
        def make_renderer(pid):
            @render.plot
            def dynamic_plot_renderer():
                print(f"🎨 [VizFactory] Rendering dynamic plot: {pid}")
                cfg = active_cfg()
                lf = tier3_leaf().lazy()
                return viz_factory.render(lf, cfg.raw_config, pid)
            return dynamic_plot_renderer

        # Bind to the session output object
        output_id = f"plot_group_{p_id}"
        print(f"🔗 [Agnostic Discovery] Binding output ID: {output_id}")
        setattr(output, output_id, make_renderer(p_id))

    @reactive.Calc
    def primary_keys():
        """Agnostic Discovery: Introspects manifests to find Primary Keys."""
        cfg = active_cfg()
        pkeys = set()

        # Helper to extract from a schema dict
        def extract_keys(schema):
            fields = schema.get("input_fields", {})
            for fid, spec in fields.items():
                if spec.get("is_primary_key"):
                    pkeys.add(fid)

        # Search all possible schema locations
        for schema in cfg.raw_config.get("data_schemas", {}).values():
            extract_keys(schema)
        for schema in cfg.raw_config.get("additional_datasets_schemas", {}).values():
            extract_keys(schema)
        if "metadata_schema" in cfg.raw_config:
            extract_keys(cfg.raw_config["metadata_schema"])

        return list(pkeys)

    @output
    # --- Analysis Theater Orchestration ---
    @output
    @render.ui
    def dynamic_tabs():
        """Routes to WrangleStudio, DevStudio, or the Comparison Theater."""
        cfg = active_cfg()
        is_comparison = _safe_input(input, "comparison_mode", False)
        state = theater_state.get()
        all_cols = tier1_anchor().columns

        # Route based on Sidebar Nav (Phase 11-F)
        active_sidebar = input.sidebar_nav()
        if active_sidebar == "Wrangle Studio":
            return wrangle_studio.render_ui()
        if active_sidebar == "Dev Studio":
            return dev_studio.render_ui()
        if active_sidebar == "Gallery":
            return gallery_viewer.render_explorer_ui()

        # Shared Header Controls (ADR-029a)
        header_controls = ui.div(
            ui.h4(f"SPARMVET Analysis Theater", class_="mb-0"),
            ui.div(
                ui.input_action_button("btn_max_plot", ui.tags.i(
                    class_="bi bi-graph-up"), class_="control-btn"),
                ui.input_action_button("btn_max_table", ui.tags.i(
                    class_="bi bi-table"), class_="control-btn"),
                ui.input_action_button("btn_reset_theater", ui.tags.i(
                    class_="bi bi-grid-1x2"), class_="control-btn"),
                ui.tags.span("|", style="color:#dee2e6; margin: 0 10px;"),
                ui.output_ui("comparison_mode_toggle_ui"),
                class_="header-controls d-flex align-items-center bg-white border rounded px-3 py-1"
            ),
            class_="d-flex justify-content-between align-items-center w-100 p-2"
        )

        # --- Theater Layout (2x2 Quadrant Philosophy - ADR-029a) ---

        # 🟢 Quadrant A: Reference Plot
        ref_plot_quad = ui.card(
            ui.card_header(ui.tags.span(
                "Plot Reference (T1/T2)", class_="reference-label")),
            ui.output_plot("plot_reference"),
            class_="shadow-none border-0 bg-transparent flex-grow-1"
        )

        # 🟢 Quadrant B: Reference Table
        ref_table_quad = ui.card(
            ui.card_header(ui.tags.span(
                "Table Reference", class_="reference-label")),
            ui.div(ui.input_switch("ref_tier_switch",
                                   "T1 ↔ T2", value=False), class_="small"),
            ui.output_table("table_reference"),
            class_="shadow-none border-0 bg-transparent flex-grow-1"
        )

        # 🔵 Quadrant C: Active Plot (T3)
        active_plot_quad = ui.card(
            ui.card_header(ui.h6("Active Visualization (Tier 3)"),
                           class_="d-flex justify-content-between"),
            ui.output_plot("plot_leaf", brush=ui.brush_opts(
                fill="#2196f3", opacity=0.3)),
            class_="shadow-none border-0 bg-transparent flex-grow-1"
        )

        # 🔵 Quadrant D: Active Table (T3)
        active_table_quad = ui.card(
            ui.card_header(ui.h6("Active Data Sandbox")),
            ui.div(ui.input_switch("view_toggle",
                                   "Wide ↔ Long", value=False), class_="small"),
            ui.input_selectize("column_visibility_picker", None,
                               choices=all_cols, selected=all_cols, multiple=True,
                               options={"plugins": ["remove_button"]}),
            ui.output_table("table_leaf"),
            class_="shadow-none border-0 bg-transparent flex-grow-1"
        )

        # Apply button with pending badge
        apply_controls = ui.div(
            ui.output_ui("recipe_pending_badge_ui"),
            ui.input_action_button(
                "btn_apply", "▶ Apply", class_="btn btn-success btn-sm"),
            class_="apply-btn-container d-flex align-items-center justify-content-end"
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
        groups = cfg.raw_config.get("analysis_groups", {})
        extra_tabs = []

        # Internal helper to avoid circular dependency
        def _get_group_metrics(gid):
            spec = groups.get(gid, {})
            p_count = len(spec.get("plots", {}))

            # Count schemas by category match
            schemas = cfg.raw_config.get("data_schemas", {})
            add_schemas = cfg.raw_config.get("additional_datasets_schemas", {})
            all_s = {**schemas, **add_schemas}
            s_count = len([s for s in all_s.values() if s.get(
                "info", {}).get("category") == gid])
            return {"plots": p_count, "schemas": s_count}

        for group_id, group_spec in groups.items():
            plot_ids = list(group_spec.get("plots", {}).keys())
            metrics = _get_group_metrics(group_id)

            group_content = [
                ui.div(
                    ui.div(
                        ui.h4(f"Group: {group_id}", class_="mb-0"),
                        ui.markdown(group_spec.get("description",
                                    "Discovery-driven analysis space.")),
                        class_="flex-grow-1"
                    ),
                    # Stats Card
                    ui.div(
                        ui.card(
                            ui.div(
                                ui.div(ui.h3(metrics['plots'], class_="text-primary mb-0"), ui.p(
                                    "Plots", class_="text-muted small mb-0")),
                                ui.div(
                                    style="width: 1px; background: #dee2e6; margin: 0 15px;"),
                                ui.div(ui.h3(metrics['schemas'], class_="text-success mb-0"), ui.p(
                                    "Schemas", class_="text-muted small mb-0")),
                                class_="d-flex align-items-center p-2"
                            ),
                            class_="shadow-none border-0 bg-light"
                        ),
                        style="width: 200px;"
                    ),
                    class_="d-flex justify-content-between align-items-start mb-3"
                ),
                ui.hr()
            ]

            # If multiple plots, use a grid
            plot_grid = []
            for p_id in plot_ids:
                plot_grid.append(
                    ui.card(
                        ui.card_header(ui.h6(p_id, class_="mb-0")),
                        ui.output_plot(f"plot_group_{p_id}"),
                        class_="mb-3 shadow-sm border-0"
                    )
                )

            if plot_grid:
                group_content.append(
                    ui.layout_columns(*plot_grid, col_widths=12))
            else:
                group_content.append(
                    ui.p("No plots defined for this group.", class_="text-muted"))

            extra_tabs.append(ui.nav_panel(group_spec.get(
                "description", group_id), group_content))

        tabs = [
            ui.nav_panel("Theater", theater_layout),
            ui.nav_panel("Inspector", ui.output_table("full_data_table"))
        ] + extra_tabs

        return ui.navset_card_tab(
            *tabs,
            id="central_theater_tabs",
            header=header_controls
        )

    # ── Helpers ─────────────────────────────────────────────────────────────

    @reactive.Effect
    @reactive.event(input.persona_selector)
    def update_persona_context():
        new_persona = input.persona_selector()
        if new_persona:
            print(f"🎭 [Persona Switch] Transitioning to: {new_persona}")
            current_persona.set(new_persona)
            # Bootloader is global but since SPARMVET is single-user session-driven
            # for this MVP, we re-initialize settings.
            bootloader.__init__(persona=new_persona)
            ui.notification_show(
                f"UI Context updated: {new_persona}", type="message")

        # 4. Reactive Tiers (ADR-024 / ADR-031)

    @reactive.Calc
    def tier1_anchor():
        """Scans the physical Parquet anchor (Predicate Pushdown ready)."""
        path = anchor_path.get()
        if not path:
            return pl.DataFrame().lazy()
        return pl.scan_parquet(path)

    @reactive.Calc
    def tier_reference():
        """
        Reference sandbox data — NEVER affected by user filters or recipe.
        Reads Tier 1 (wide) or Tier 2 (viz-transformed) based on ref_tier_switch.
        ADR-029a: This reactive is the SOLE data source for the left Reference Pane.
        """
        lf = tier1_anchor()
        show_tier2 = _safe_input(input, "ref_tier_switch", False)
        if show_tier2:
            cfg = active_cfg()
            lf = _apply_tier2_transforms(lf, cfg)
        return lf  # LazyFrame — NOT collected; callers collect as needed

    @reactive.Calc
    # Apply gate — only recalculate on explicit click
    @reactive.event(input.btn_apply)
    def tier3_leaf():
        """
        Position-Aware Two-Stage Tier 3 Pipeline (ADR-024 / ADR-029a Phase 12-A).

        Stage 1 (pre-transform): User steps placed ABOVE inherited Tier 2 nodes.
                                  Applied to wide Tier 1 data (row filters, excludes).
        Stage 2 (inherited):      Tier 2 viz transforms (long-format, aggregation).
                                  Applied if view_toggle requests long/aggregated view.
        Stage 3 (post-transform): User steps placed BELOW inherited Tier 2 nodes.
                                  Applied after viz transforms (column selection, etc.).

        The committed recipe comes from snapshot_recipe (set when Apply is clicked).
        This reactive is NOT triggered by incremental UI edits — only by btn_apply.
        """
        lf = tier1_anchor()
        cfg = active_cfg()
        cols = lf.columns
        recipe = snapshot_recipe.get()  # Committed recipe nodes
        show_long = _safe_input(input, "view_toggle", False)

        # Split recipe at the inherited Tier 2 boundary
        pre_steps = [s for s in recipe if s.get("stage") == "pre_transform"]
        post_steps = [s for s in recipe if s.get("stage") == "post_transform"]

        # Stage 1: Pre-transform user filters (applied to wide Tier 1)
        for step in pre_steps:
            action = step.get("action", "")
            col = step.get("column")
            val = step.get("value")
            if action == "filter_eq" and col and val is not None:
                try:
                    lf = lf.filter(pl.col(col) == val)
                except Exception:
                    pass

        # 1. Apply UI-driven Filters (Predicate Pushdown)
        # ADR-003: Dynamically discovery columns from Tier 1 Anchor
        lf_anchor = tier1_anchor()
        for col in lf_anchor.columns[:10]:
            clean_col = col.replace(" ", "_").replace("(", "").replace(")", "")
            try:
                # Retrieve value from sanitized ID
                val = getattr(input, f"filter_{clean_col}")()
                if val and val != "All":
                    lf = lf.filter(pl.col(col) == val)
            except Exception:
                pass

        # Stage 2: Inherited Tier 2 viz transforms
        if show_long:
            lf = _apply_tier2_transforms(lf, cfg)

        # Stage 3: Post-transform user steps
        for step in post_steps:
            action = step.get("action", "")
            cols_select = step.get("columns")
            if action == "select_columns" and cols_select:
                try:
                    lf = lf.select(cols_select)
                except Exception:
                    pass

        # Column visibility (always post-transform)
        try:
            visible_cols = input.column_visibility_picker()
            if visible_cols:
                pkeys = primary_keys()
                final_cols = list(set(visible_cols) | set(pkeys))
                ordered_cols = [c for c in lf.columns if c in final_cols]
                lf = lf.select(ordered_cols)
        except Exception:
            pass

        # Apply WrangleStudio recipe (Phase 11-F)
        lf = wrangle_studio.apply_logic(lf)

        # WIDE-TO-LONG GUARD: Materialize check (ADR-029c)
        result = lf.collect()

        # User notification on empty result
        if result.height == 0:
            ui.notification_show("⚠️ Current filters returned no data. Adjust sidebar settings.",
                                 type="warning", duration=20)

        recipe_pending.set(False)  # Clear pending flag after successful Apply
        return result

    @reactive.Effect
    @reactive.event(input.btn_apply)
    def handle_apply():
        """Commits the current WrangleStudio recipe on Apply click."""
        # Snapshot current recipe state from WrangleStudio.logic_stack
        current_recipe = wrangle_studio.logic_stack.get()
        snapshot_recipe.set(current_recipe)

    # Track recipe changes to show pending badge
    @reactive.Effect
    def track_recipe_changes():
        """Sets recipe_pending=True whenever the WrangleStudio recipe changes."""
        _ = wrangle_studio.apply_logic  # Trigger re-run on logic change
        recipe_pending.set(True)

    # 5. Render Outputs

    @output
    @render.ui
    def recipe_pending_badge_ui():
        """Shows a 'Pending' badge when recipe has unsaved changes."""
        if recipe_pending.get():
            return ui.tags.span("⏳ Pending", class_="recipe-pending-badge")
        return ui.div()

    @output
    @render.plot
    def plot_reference():
        """
        Reference plot from tier_reference() (Tier 1 or Tier 2 viz-transformed).
        NEVER affected by user recipe or sidebar filters.
        """
        cfg = active_cfg()
        plot_ids = list(cfg.raw_config.get("plots", {}).keys())
        if not plot_ids:
            return None
        lf = tier_reference()
        return viz_factory.render(lf, cfg.raw_config, plot_ids[0])

    @output
    @render.table
    def table_reference():
        """
        Read-only exploration table from tier_reference().
        Users may visually inspect (filter/sort locally) but NO writes are persisted.
        """
        return tier_reference().head(100).collect()

    @output
    @render.plot
    def plot_anchor():
        """Legacy: Tier 2 reference plot (kept for backward compat, routes to plot_reference)."""
        cfg = active_cfg()
        plot_ids = list(cfg.raw_config.get("plots", {}).keys())
        if not plot_ids:
            return None
        return viz_factory.render(tier1_anchor(), cfg.raw_config, plot_ids[0])

    @output
    @render.plot
    def plot_leaf():
        cfg = active_cfg()
        plot_ids = list(cfg.raw_config.get("plots", {}).keys())
        if not plot_ids:
            return None
        plot_id = plot_ids[0]

        # Use the fully processed Tier 3 Leaf data (filtered + transformed)
        # ADR-024: Tier 3 is the interactive view.
        lf = tier3_leaf().lazy()
        return viz_factory.render(lf, cfg.raw_config, plot_id)

    @output
    @render.table
    def table_anchor():
        return tier1_anchor().head(5).collect()

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
            ui.div(f"Collection: {collection_id}",
                   class_="audit-node-tier2"),
        ]

        # Optional Metadata Enforcement (ADR-014)
        if "metadata_schema" in cfg.raw_config:
            nodes.append(
                ui.div(f"Anchor: {collection_id}.parquet (w/ Metadata)",
                       class_="audit-node-tier3")
            )
        else:
            nodes.append(
                ui.div(f"Anchor: {collection_id}.parquet (Standalone)",
                       class_="audit-node-tier3")
            )

        # Discovery-driven active nodes from WrangleStudio
        active_nodes = wrangle_studio.logic_stack.get()
        if active_nodes:
            nodes.append(ui.hr())
            nodes.append(ui.h6("Session Transformations (Tier 3)"))
            for i, node in enumerate(active_nodes):
                action = node.get("action", "unknown")
                comment = node.get("comment", "No comment")
                params = node.get("params", {})
                nodes.append(
                    ui.tooltip(
                        ui.div(
                            ui.div(f"⚡ {action}", class_="fw-bold"),
                            ui.div(f"💬 {comment}",
                                   style="font-size: 0.8em; color: #555;"),
                            class_="audit-node-tier3"
                        ),
                        f"Action: {action} | Spec: {params}",
                        placement="left",
                        id=f"node_tt_{i}"
                    )
                )

        return ui.div(*nodes)

    @output
    @render.ui
    def audit_nodes_tier2():
        """
        Dynamically renders the Tier 2 (Branch) logic nodes in the Audit Stack.
        Introspects the active manifest's assembly recipe to list inherited steps.
        Satisfies: ui.output_ui('audit_nodes_tier2') in ui.py (ADR-003, ADR-027).
        """
        cfg = active_cfg()
        collection_id = active_collection_id()
        collections = cfg.raw_config.get("assembly_manifests", {})
        recipe = []
        if collection_id in collections:
            raw_recipe = collections[collection_id].get("recipe", [])
            # ADR-024: Resolve Tier 1 (Relational/Cleaning) for Audit Visualization
            recipe = DataWrangler._resolve_tier(raw_recipe, "tier1")

        if not recipe:
            return ui.div(
                ui.div("No Tier 2 steps defined.", class_="audit-node-tier2")
            )

        nodes = []
        for step in recipe:
            action = step.get("action", "unknown")
            label = step.get("label") or step.get(
                "right_ingredient") or action
            params = step.get("params", {})
            nodes.append(
                ui.tooltip(
                    ui.div(f"[Tier 2] {action}: {label}",
                           class_="audit-node-tier2"),
                    f"YAML Spec: {params}",
                    placement="left"
                )
            )
        return ui.div(*nodes)

    # 5. Dynamic Schema Introspection (11-D)
    @reactive.Calc
    def current_columns():
        """Returns the list of columns available in the Tier 3 LazyFrame."""
        lf = tier1_anchor()
        return lf.columns

    @output
    @render.ui
    def sidebar_filters():
        """Generates dynamic filter inputs based on the Active Project's columns."""
        try:
            lf = tier1_anchor()
            # Limit to first 6 columns to avoid UI bloat in stress test
            cols = lf.columns[:6]
            filters = []
            for col in cols:
                # Sanitize ID for Shiny (ADR-031 Compliance)
                clean_id = col.replace(" ", "_").replace(
                    "(", "").replace(")", "")
                choices = [
                    "All"] + sorted(lf.select(pl.col(col)).unique().collect()[col].to_list())
                filters.append(
                    ui.card(
                        ui.input_select(f"filter_{clean_id}", f"Filter: {col}",
                                        choices=choices, selected="All"),
                        class_="mb-2 border-0 shadow-none bg-transparent"
                    )
                )
            return ui.div(*filters)
        except Exception as e:
            return ui.div(ui.markdown(f"*Filters unavailable for this schema.*"))

    # 6. Global Actions
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
    @reactive.event(input.restore_session)
    def handle_restore():
        ui.notification_show("🔄 Session State Restored.", type="warning")

    # 6. Outlier Brush & Advanced Interaction (ADR-030)
    @reactive.Effect
    @reactive.event(input.plot_leaf_brush)
    def handle_plot_brush():
        """Connects UI telemetry to libs/transformer/lookup.py for Outlier quick-view."""
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

        if not x_col or not y_col:
            ui.notification_show(
                "❌ Cannot perform lookup: Axis mapping missing.", type="error")
            return

        # CALL LIBRARIES (ADR-003): Perform Tier 1 lookup
        outliers = lookup_anchor_rows(
            brush,
            anchor_path.get(),
            x_col=x_col,
            y_col=y_col
        )

        if outliers.is_empty():
            ui.notification_show(
                "ℹ️ No rows matched the selected area.", type="message")
            return

        # Show Quick-View Modal (ADR-030)
        m = ui.modal(
            ui.h4(f"Outlier Quick-View ({outliers.height} rows)"),
            ui.output_table("brush_results_table"),
            ui.div(
                ui.input_action_button(
                    "btn_save_outliers", "💾 Push to Branch"),
                ui.modal_button("Close"),
                class_="d-flex justify-content-end gap-2 mt-3"
            ),
            size="xl",
            easy_close=True
        )
        ui.modal_show(m)

        # Store for display
        @output
        @render.table
        def brush_results_table():
            return outliers.head(20)

    @reactive.Effect
    @reactive.event(input.btn_gallery_open_submission)
    def handle_gallery_submit_open():
        """Opens the ADR-033 Submission Gate."""
        ui.modal_show(gallery_viewer.submission_modal_ui())

    @reactive.Effect
    @reactive.event(input.btn_confirm_submission)
    def handle_submission_confirm():
        """Persist the new recipe and trigger Gallery refresh.
        Enforces mandatory checklist items before submission.
        """
        # Validate required checklist items
        required = {
            "check_yaml": input.check_yaml(),
            "check_tsv": input.check_tsv(),
            "check_png": input.check_png(),
            "check_md": input.check_md()
        }
        missing = [k for k, v in required.items() if not v]
        if missing:
            ui.notification_show(
                f"❌ Submission blocked: missing required items {', '.join(missing)}",
                type="error"
            )
            return

        # Gather recipe, data, and metadata
        recipe = wrangle_studio.logic_stack.get()
        data = tier3_leaf()
        meta_path = bootloader.get_location("gallery") / "tmp_meta.md"
        meta_content = ""
        if meta_path.exists():
            with open(meta_path, "r") as f:
                meta_content = f.read()
        else:
            ui.notification_show(
                "⚠️ No metadata file found; proceeding with empty metadata.", type="warning")

        # Persist using GalleryManager (defaults to assets/gallery_data)
        manager = GalleryManager()
        bundle_path = manager.submit_recipe(
            name=f"Submission_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            recipe=recipe,
            data=data,
            meta_markdown=meta_content
        )

        # Cleanup temporary metadata file
        if meta_path.exists():
            try:
                meta_path.unlink()
            except Exception:
                pass

        ui.modal_remove()
        gallery_refresh_trigger.set(gallery_refresh_trigger.get() + 1)
        ui.notification_show(
            f"🚀 Recipe successfully added to Public Gallery!\nBundle: {bundle_path}",
            type="success"
        )

    @reactive.Effect
    @reactive.event(input.btn_autofill_meta)
    def handle_autofill_start():
        """Prompts for Family selection before generating metadata (ADR-035)."""
        ui.modal_show(
            ui.modal(
                ui.h4("Autofill Metadata: Taxonomy Select"),
                ui.input_select("autofill_family_select", "Select Plot Family (Purpose):",
                                choices=["Distribution", "Correlation", "Comparison", "Ranking", "Evolution", "Part-to-Whole"]),
                ui.input_select("autofill_pattern_select", "Select Data Pattern:",
                                choices=["1 Numeric", "2 Numeric", "1 Numeric, 1 Categorical", "1 Numeric, 2 Categorical", "Numeric-Numeric"]),
                ui.input_select("autofill_difficulty_select", "Select Difficulty:",
                                choices=["Simple", "Intermediate", "Advanced"]),
                ui.div(
                    ui.input_action_button(
                        "btn_confirm_autofill", "📝 Generate Content", class_="btn-primary"),
                    ui.modal_button("Cancel"),
                    class_="d-flex justify-content-end gap-2 mt-3"
                ),
                title="Metadata Taxonomy Prompt",
                easy_close=True
            )
        )

    @reactive.Effect
    @reactive.event(input.btn_confirm_autofill)
    def handle_autofill_process():
        """Generates the education template with pre-selected taxonomy."""
        ui.modal_remove()
        family = input.autofill_family_select()
        pattern = input.autofill_pattern_select()
        diff = input.autofill_difficulty_select()

        stack = wrangle_studio.logic_stack.get()
        persona = input.persona_selector() if hasattr(
            input, "persona_selector") else "Standard User"

        meta_content = gallery_viewer.autofill_meta_from_audit(
            stack, persona=persona)

        # Inject real values (Phase 14-C Enrichment)
        meta_content = meta_content.replace(
            "[Distribution | Correlation | Comparison | Ranking]", family)
        meta_content = meta_content.replace(
            "[1 Numeric | 2 Numeric | 1 Numeric, 1 Categorical]", pattern)
        meta_content = meta_content.replace(
            "[Simple | Intermediate | Advanced]", diff)

        # Save to local session (Simulation)
        target = bootloader.get_location("gallery") / "tmp_meta.md"
        with open(target, "w") as f:
            f.write(meta_content)

        ui.notification_show(
            f"✅ Metadata ({family}/{diff}) saved: {target.name}", type="success")

    @reactive.Effect
    @reactive.event(input.export_global)
    def handle_global_export():
        """Implements Phase 14-C Global Session Export bundling."""
        ui.notification_show("📦 Bundling session artifacts...", type="message")

        try:
            # 1. Gather Tiers
            tiers = {
                "tier1_anchor": tier1_anchor().collect().to_pandas(),
                "tier2_reference": tier_reference().collect().to_pandas(),
                "tier3_leaf": tier3_leaf().to_pandas()
            }

            # 2. Gather Manifest & Audit
            manifest = active_cfg().raw_config
            audit_trail = [
                f"{n.get('action')}: {n.get('comment')}" for n in wrangle_studio.logic_stack.get()]

            # 3. Call Exporter
            exporter = SubmissionExporter()
            zip_path = exporter.bundle_global_export(
                project_id=input.project_id(),
                plot_path=None,
                tiers=tiers,
                manifest=manifest,
                audit_trail=audit_trail
            )

            ui.notification_show(
                f"✅ Global Export Ready: {Path(zip_path).name}", type="success", duration=15)
        except Exception as e:
            ui.notification_show(f"❌ Export Failed: {e}", type="error")

    @output
    @render.ui
    def gallery_md_content():
        """Renders the Educational Markdown panel (Right Pane)."""
        file_path = input.gallery_recipe_select() if hasattr(
            input, "gallery_recipe_select") else None
        if not file_path:
            # Show the blank template if no recipe selected
            template_path = bootloader.get_location(
                "gallery") / "recipe_template.md"
            if template_path.exists():
                with open(template_path, "r") as f:
                    return ui.markdown(f.read())
            return ui.p("Select a recipe to view educational guidance.")

        # Lookup associated .md file (recipe_name.md)
        md_path = Path(file_path).with_suffix(".md")
        if md_path.exists():
            with open(md_path, "r") as f:
                return ui.markdown(f.read())

        return ui.div(
            ui.p("⚠️ No educational documentation found for this recipe.",
                 class_="text-danger"),
            ui.p("Please contribute a recipe_meta.md file to help other analysts."),
            class_="alert alert-warning"
        )

    @output
    @render.plot
    def gallery_plot_preview():
        """Ghost-loads the plot for the selected gallery recipe (Simulation)."""
        # In a real implementation, this would re-run Tier 3 for the selected YAML
        return plot_leaf()

    @output
    @render.table
    def gallery_table_preview():
        """Ghost-loads the data sample for the selected gallery recipe."""
        return tier3_leaf().head(10)

    @output
    @render.text
    def gallery_yaml_preview():
        """Displays the raw YAML for verification."""
        file_path = input.gallery_recipe_select() if hasattr(
            input, "gallery_recipe_select") else None
        if file_path and Path(file_path).exists():
            with open(file_path, "r") as f:
                return f.read()
        return "No recipe selected."

        # 7. Ingestion & Persistence (Phase 11-E / ADR-031)
    @output
    @render.ui
    def gallery_browser_anchor():
        """Scans Location 5 (Gallery) and renders discovery controls (ADR-031/033/035)."""
        # Reactive trigger (Phase 14-B Submission)
        gallery_refresh_trigger.get()

        # Get filters (ADR-035)
        family_filter = _safe_input(input, "gallery_filter_family", [])
        pattern_filter = _safe_input(input, "gallery_filter_pattern", [])
        diff_filter = _safe_input(input, "gallery_filter_difficulty", [])

        try:
            gallery_path = bootloader.get_location("gallery")
            # Scan for individual folder-based recipes
            yaml_files = list(gallery_path.glob("**/recipe_manifest.yaml"))
        except Exception:
            yaml_files = []

        # Real-time filtering based on MD metadata
        filtered_files = []
        for f in yaml_files:
            meta_path = f.parent / "recipe_meta.md"
            if not meta_path.exists():
                # Allow unfiltered if no metadata exists (Backward compatibility)
                if not family_filter and not diff_filter and not pattern_filter:
                    filtered_files.append(f)
                continue

            with open(meta_path, "r") as m:
                meta_txt = m.read()
                # Check for explicit tags in the axis-based taxonomy
                # ## Family (Purpose): Distribution | ## Data Pattern: 1 Numeric
                is_family_match = any(
                    fam in meta_txt for fam in family_filter) if family_filter else True
                is_pattern_match = any(
                    pat in meta_txt for pat in pattern_filter) if pattern_filter else True
                is_diff_match = any(
                    diff in meta_txt for diff in diff_filter) if diff_filter else True

                if is_family_match and is_pattern_match and is_diff_match:
                    filtered_files.append(f)

        if not filtered_files:
            return ui.div(
                ui.h6("No recipes match the active filters.",
                      class_="text-muted mt-3"),
                class_="p-3 border rounded bg-light"
            )

        # We use a select input to choose which to clone
        file_names = {str(f): f.parent.name for f in filtered_files}

        return ui.div(
            ui.h5("Public Recipe Gallery"),
            ui.input_select("gallery_recipe_select",
                            "Select Template to Ghost-Load:", choices=file_names),
            ui.input_action_button(
                "btn_clone_gallery", "📥 Clone to Active Session", class_="btn-primary w-100"),
            class_="p-3 border rounded bg-light shadow-sm mt-2"
        )

    @reactive.Effect
    @reactive.event(input.btn_clone_gallery)
    def handle_gallery_clone():
        """Ghost-loads the selected Gallery manifest into WrangleStudio."""
        file_path = input.gallery_recipe_select()
        if not file_path:
            return

        try:
            with open(file_path, "r") as f:
                manifest = yaml.safe_load(f)

            # ADR-024: Resolve both tiers for Ghost-Loading
            wrangling_raw = manifest.get("wrangling", [])
            new_steps = DataWrangler._resolve_tier(wrangling_raw, "all")

            if not isinstance(new_steps, list):
                new_steps = []

            # Map existing steps to logic_stack format (ensuring comments exist)
            valid_nodes = []
            for step in new_steps:
                action = step.get("action", "unknown")
                # Params are all keys except 'action'
                params = {k: v for k, v in step.items() if k != "action"}
                valid_nodes.append({
                    "action": action,
                    "params": params,
                    "comment": "Ghost-loaded from Reference Gallery."
                })

            # GHOST-LOAD: Update the WrangleStudio stack directly
            wrangle_studio.logic_stack.set(valid_nodes)
            ui.notification_show(
                "✅ Recipe cloned to active Session Stack. Click 'Apply' to visualize.", type="success")

        except Exception as e:
            ui.notification_show(f"❌ Clone failed: {e}", type="error")

    # 8. Ghost Save Logic (ADR-031 / Phase 11-F)
    @reactive.Effect
    def ghost_save_trigger():
        freq = (bootloader.get_automation_setting(
            "ghost_save", "frequency_minutes") or 2)
        autosave_dir = bootloader.get_location("user_sessions") / "autosave"

        if bootloader.is_enabled("ghost_save_enabled"):
            try:
                if not autosave_dir.exists():
                    autosave_dir.mkdir(parents=True, exist_ok=True)

                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                project_id = input.project_id()
                save_path = autosave_dir / \
                    f"ghost_{project_id}_{timestamp}.yaml"

                cfg = active_cfg().raw_config
                with open(save_path, "w") as f:
                    yaml.safe_dump(cfg, f)

                # 5-Version Rotation Logic
                saves = sorted(list(autosave_dir.glob(
                    "ghost_*.yaml")), key=os.path.getmtime)
                if len(saves) > 5:
                    for old_save in saves[:-5]:
                        old_save.unlink()

                ui.notification_show("💾 Ghost Save (Success)", type="message")
                print(
                    f"💾 Ghost Save rotated @ {datetime.now().strftime('%H:%M:%S')}")
            except Exception as e:
                print(f"⚠️ Ghost Save Failed: {e}")

        reactive.invalidate_later(freq * 60)

    @reactive.Effect
    @reactive.event(input.btn_ingest)
    def handle_ingest():
        files = input.file_ingest()
        if not files:
            ui.notification_show(
                "⚠️ Please select files first.", type="warning")
            return

        ui.notification_show("⏳ Processing External Bundle...", type="message")

        manifest_dir = bootloader.get_location("manifests")
        raw_data_dir = bootloader.get_location("raw_data")

        ingested_count = 0
        manifest_count = 0

        for f in files:
            name = f['name']
            path = Path(f['datapath'])
            ext = Path(name).suffix.lower()

            try:
                if ext == ".yaml":
                    # SEGREGATION: YAMLs go to manifests/
                    target = manifest_dir / name
                    shutil.copy(path, target)
                    manifest_count += 1
                elif ext == ".zip":
                    # COMPLEX STRUCTURE: Unzip into raw_data or manifests based on contents
                    with zipfile.ZipFile(path, 'r') as zip_ref:
                        # Inspect contents to decide destination
                        # ADR-012: If it contains a .yaml, it likely belongs in manifest_dir
                        has_yaml = any(fi.filename.endswith(
                            '.yaml') for fi in zip_ref.infolist())
                        dest = manifest_dir if has_yaml else raw_data_dir
                        zip_ref.extractall(dest)
                        ui.notification_show(
                            f"📦 Unzipped {name} to {dest.name}", type="message")
                else:
                    # DATA: TSV/CSV/Excel go to raw_data/
                    target = raw_data_dir / name
                    if ext in [".xlsx", ".xls"]:
                        # Convert to TSV for system consistency if possible
                        df = pd.read_excel(str(path))
                        target_tsv = raw_data_dir / name.replace(ext, ".tsv")
                        df.to_csv(target_tsv, sep='\t', index=False)
                        target = target_tsv
                    else:
                        shutil.copy(path, target)
                    ingested_count += 1
            except Exception as e:
                ui.notification_show(
                    f"❌ Failed to ingest {name}: {e}", type="error")

        if manifest_count > 0 or ingested_count > 0:
            ui.notification_show(
                f"✅ Success: {manifest_count} manifests, {ingested_count} datasets added.",
                type="success"
            )
            # Reload projects in bootloader
            bootloader.__init__(persona=current_persona.get())
            ui.update_select("project_id", choices=list(
                bootloader.available_projects.keys()))
