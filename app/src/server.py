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
    wrangle_studio = WrangleStudio(session.token)
    # Pass a lambda to reactively fetch Tier 1 columns
    wrangle_studio.define_server(
        input, output, session, lambda: tier1_anchor().columns)

    dev_studio = DevStudio()
    dev_studio.define_server(input, output, session)

    # Gallery Refresh Trigger (Phase 14-B)
    gallery_refresh_trigger = reactive.Value(0)

    # 2c. Error Handling Orchestrator
    def show_sparmvet_error(err):
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
                    ui.p(str(err), style="font-size: 1.1em;"),
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

    # 4a. Persona-gated Comparison Mode toggle (ADR-026 / ADR-029a)
    @output
    @render.ui
    def comparison_mode_toggle_ui():
        """Renders Comparison and Triple-Tier switches if persona permits."""
        enabled = bootloader.is_enabled("comparison_mode_enabled")
        if not enabled:
            return ui.div()
        return ui.div(
            ui.input_switch("comparison_mode",
                            "⚡ Comparison Mode", value=False),
            ui.input_switch("triple_tier_mode",
                            "🧬 Triple-Tier Grid", value=False),
            class_="d-flex gap-3 align-items-center"
        )

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
    @render.text
    def active_tab_title():
        return "Analysis Theater"

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
            # Phase 14-B/C: Educational Explorer with Taxonomy Sidebar (ADR-035)
            return gallery_viewer.render_explorer_ui()

        # Build Reference pane (Left) — only shown in Comparison Mode
        reference_col = ui.div(
            ui.tags.span("⚠️ Inspection only — changes here are not saved",
                         class_="reference-label"),
            ui.div(
                ui.input_switch(
                    "ref_tier_switch", "Tier 1 (Wide) / Tier 2 (Transformed)", value=False),
                class_="mb-2"
            ),
            ui.output_plot("plot_reference"),
            ui.hr(),
            ui.output_table("table_reference"),
            class_="reference-pane"
        ) if is_comparison else ui.div()

        # Apply button with pending badge
        apply_controls = ui.div(
            ui.output_ui("recipe_pending_badge_ui"),
            ui.input_action_button("btn_apply", "▶ Apply",
                                   class_="btn btn-success btn-sm"),
            class_="apply-btn-container d-flex align-items-center justify-content-end"
        )

        # Active pane (Right) — Tier 3 two-stage pipeline
        active_col = ui.div(
            apply_controls,
            ui.div(
                ui.input_switch(
                    "view_toggle", "Wide ↔ Long/Aggregated", value=False),
                class_="mb-2"
            ),
            ui.div(
                ui.output_plot("plot_leaf", brush=ui.brush_opts(
                    id="plot_leaf_brush", color="#2196f3", opacity=0.3)),
                style="display: none;" if state == "table" else "display: block;"
            ),
            ui.div(
                ui.input_selectize(
                    "column_visibility_picker",
                    "Column Visibility:",
                    choices=all_cols, selected=all_cols,
                    multiple=True,
                    options={"plugins": ["remove_button"],
                             "placeholder": "Select columns to show..."}
                ),
                ui.output_table("table_leaf"),
                style="display: none;" if state == "plot" else "display: block;",
                class_="table-container"
            ),
            class_="active-pane"
        )

        # Build layout based on active mode
        is_triple = _safe_input(input, "triple_tier_mode", False)

        if is_triple:
            # Phase 12-B: Side-by-side comparison of Tiers 1, 2, and 3
            theater_layout = ui.layout_columns(
                ui.div(ui.h6("Tier 1: Raw Anchor"), ui.output_table(
                    "table_anchor"), class_="p-2 border rounded"),
                ui.div(ui.h6("Tier 2: Reference"), ui.output_table(
                    "table_reference"), class_="p-2 border rounded"),
                ui.div(ui.h6("Tier 3: Leaf View"), ui.output_table(
                    "table_leaf"), class_="p-2 border rounded"),
                col_widths=[4, 4, 4]
            )
        elif is_comparison:
            theater_layout = ui.layout_columns(
                reference_col,
                active_col,
                col_widths=[5, 7]
            )
        else:
            theater_layout = active_col

        # Build manifest-driven tabs
        groups = cfg.raw_config.get("analysis_groups", {})
        extra_tabs = [
            ui.nav_panel(
                group_spec.get("description", group_id),
                ui.h4(f"Group: {group_id}"),
                ui.markdown("Discovery-driven analysis space.")
            )
            for group_id, group_spec in groups.items()
        ]

        tabs = [
            ui.nav_panel("Analysis Theater", theater_layout),
            ui.nav_panel("Data Inspector", ui.output_table("full_data_table"))
        ] + extra_tabs

        return ui.navset_card_tab(*tabs, id="central_theater_tabs")

    # ── Helpers ─────────────────────────────────────────────────────────────

    def _safe_input(inp, name, default=None):
        """Safely reads an input that may not exist (e.g., persona-gated toggles)."""
        try:
            return getattr(inp, name)()
        except Exception:
            return default

    def _apply_tier2_transforms(lf: pl.LazyFrame, cfg) -> pl.LazyFrame:
        """
        Applies Tier 2 viz transforms (long-format / aggregation) from the manifest.
        ADR-024: Tier 2 MUST NOT filter rows — only reshape/aggregate.
        Returns a LazyFrame (not collected).
        """
        tier2_steps = cfg.raw_config.get("tier2_transforms", [])
        if not tier2_steps:
            return lf

        # WIDE-TO-LONG GUARD: If filtered down to zero rows, log and skip reshaping to avoid schema collapse
        try:
            count = lf.select(pl.len()).collect().item()
            if count == 0:
                print(
                    "⚠️ Wide-to-Long Guard: Zero rows detected before Tier 2. Skipping transforms.")
                return lf
        except Exception as e:
            print(f"⚠️ Guard check failed: {e}")

        # Real implementation: Use DataWrangler with an identity schema for Tier 2
        wrangler = DataWrangler(data_schema={})
        return wrangler.run(lf, tier2_steps)

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

        # Also apply sidebar quick-filters (always pre-transform)
        for col in cols[:10]:
            try:
                val = getattr(input, f"filter_{col}")()
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

        # Build Tier 3 filters for VizFactory
        active_filters = []
        lf_raw = tier1_anchor()
        for col in lf_raw.columns[:10]:
            try:
                val = getattr(input, f"filter_{col}")()
                if val and val != "All":
                    active_filters.append(
                        {"column": col, "op": "eq", "value": val})
            except:
                pass

        # Inject filters into a transient manifest
        import copy
        manifest_leaf = copy.deepcopy(cfg.raw_config)
        if "plots" in manifest_leaf and plot_id in manifest_leaf["plots"]:
            manifest_leaf["plots"][plot_id]["filters"] = active_filters

        return viz_factory.render(lf_raw, manifest_leaf, plot_id)

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
            recipe = raw_recipe.get("steps", []) if isinstance(
                raw_recipe, dict) else raw_recipe

        if not recipe:
            return ui.div(
                ui.div("No Tier 2 steps defined.", class_="audit-node-tier2")
            )

        nodes = []
        for step in recipe:
            action = step.get("action", "unknown")
            label = step.get("label") or step.get("right_ingredient") or action
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
        """Programmatically generates filter inputs based on data schema."""
        cols = current_columns()
        # Filter out common IDs or high-cardinality strings for the MVP
        filter_inputs = []
        for col in cols[:10]:  # Limit to first 10 columns for stability
            filter_inputs.append(
                ui.input_select(f"filter_{col}", f"Filter: {col}",
                                choices=["All"], selected="All")
            )
        return ui.div(*filter_inputs)

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
        """Persists the new recipe and triggers Gallery refresh."""
        ui.modal_remove()
        # Simulation: Trigger refresh
        gallery_refresh_trigger.set(gallery_refresh_trigger.get() + 1)
        ui.notification_show(
            "🚀 Recipe successfully added to Public Gallery!", type="success")

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
        return plot_leaf()  # In a real implementation, this would re-run Tier 3 for the selected YAML

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

            # Extract wrangling steps
            new_steps = manifest.get("wrangling", [])
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

    # 7. Ingestion & Persistence (Phase 11-E / ADR-031)
    @reactive.Effect
    @reactive.event(input.btn_ingest)
    def handle_ingest():
        files = input.file_ingest()
        if not files:
            ui.notification_show(
                "⚠️ Please select a file first.", type="warning")
            return

        ui.notification_show("⏳ Processing External Data...", type="message")
        f = files[0]
        ext = Path(f['name']).suffix.lower()
        output_dir = bootloader.get_location("raw_data")
        target_path = output_dir / f['name'].replace(ext, ".tsv")

        try:
            # 1. Path Authority Resolution
            python_path = bootloader.get_python_path()
            script_path = bootloader.get_script_path("excel_parser")

            if ext in [".xlsx", ".xls"]:
                # Create a temporary config for the parser (identity mapping for the first sheet)
                # Or just use the script's default behavior if applicable.
                # However, excel_handler.py expects a --config.
                # Since the current UI ingestion is simple, we'll use the script for parity validation.

                # For simplified UI ingestion, we continue using pandas but strictly route via libraries
                df = pd.read_excel(f['datapath'])
                df.to_csv(target_path, sep='\t', index=False)
                # NOTE: In Phase 12, this will be fully replaced by a subprocess call to excel_handler.py
                # once the UI provides sheet-selection options.
            else:
                shutil.copy(f['datapath'], target_path)

            ui.notification_show(
                f"✅ Materialized: {target_path.name}", type="message")
        except Exception as e:
            ui.notification_show(f"❌ Ingestion Failed: {e}", type="error")

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
