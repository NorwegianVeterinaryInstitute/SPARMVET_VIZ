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

    # 2b. Module Orchestration (Phase 11-F)
    wrangle_studio = WrangleStudio(session.token)
    # Pass a lambda to reactively fetch Tier 1 columns
    wrangle_studio.define_server(
        input, output, session, lambda: tier1_anchor().columns)

    dev_studio = DevStudio()
    dev_studio.define_server(input, output, session)

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
            ui.notification_show(f"❌ Ingestion Error: {e}", type="error")

    # 4. Agnostic Dynamic Discovery (ADR-029b)
    @output
    @render.text
    def app_title():
        cfg = active_cfg()
        info = cfg.raw_config.get('info', {})
        # Dynamic Header Discovery: Use name/title or fallback to filename
        name = info.get('display_name') or info.get(
            'name') or info.get('title')
        if not name:
            name = f"Untitled Project - {input.project_id()}.yaml"
        return f"SPARMVET_VIZ: {name}"

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
        """Programmatically generates tabs based on manifest definitions."""
        cfg = active_cfg()
        project_id = input.project_id()
        is_split = input.layout_toggle_header()
        state = theater_state.get()
        all_cols = tier1_anchor().columns

        # 0. Route based on Sidebar Navigation (Phase 11-F)
        active_sidebar = input.sidebar_nav()
        if active_sidebar == "Wrangle Studio":
            return wrangle_studio.render_ui()
        if active_sidebar == "Dev Studio":
            return dev_studio.render_ui()

        # Grid layout for plots/tables
        theater_layout = ui.layout_columns(
            ui.card(
                ui.card_header(
                    ui.div(
                        ui.span("Tier 2: Reference (Branch)"),
                        class_="d-flex justify-content-between align-items-center"
                    )
                ),
                ui.output_plot("plot_anchor"),
                ui.output_table("table_anchor"),
                full_screen=True
            ),
            ui.card(
                ui.card_header(
                    ui.div(
                        ui.span("Tier 3: Active Leaf (Filtered)"),
                        ui.div(
                            ui.input_action_button("btn_max_plot", ui.tags.i(
                                class_="bi bi-graph-up"), class_="control-btn", title="Maximize Plot"),
                            ui.input_action_button("btn_max_table", ui.tags.i(
                                class_="bi bi-table"), class_="control-btn", title="Maximize Table"),
                            ui.input_action_button("btn_reset_theater", ui.tags.i(
                                class_="bi bi-grid-1x2"), class_="control-btn", title="Split View"),
                            class_="header-controls"
                        ),
                        class_="d-flex justify-content-between align-items-center"
                    )
                ),
                ui.div(
                    ui.output_plot("plot_leaf"),
                    style="display: none;" if state == "table" else "display: block;"
                ),
                ui.div(
                    ui.hr(),
                    ui.div(
                        ui.input_selectize(
                            "column_visibility_picker",
                            "Column Visibility:",
                            choices=all_cols,
                            selected=all_cols,
                            multiple=True,
                            options={
                                "plugins": ["remove_button"],
                                "placeholder": "Select columns to show..."
                            }
                        ),
                        class_="mb-2"
                    ),
                    ui.output_table("table_leaf"),
                    style="display: none;" if state == "plot" else "display: block;",
                    class_="table-container"
                ),
                full_screen=True
            ),
            col_widths=[6, 6] if is_split else [
                0, 12]  # Hide Tier 2 if not split
        )

        tabs = [
            ui.nav_panel("Analysis Theater", theater_layout),
            ui.nav_panel("Data Inspector", ui.output_table("full_data_table"))
        ]

        # Agnostic Loop: Add tabs for each analysis group defined in manifest
        groups = cfg.raw_config.get("analysis_groups", {})
        for group_id, group_spec in groups.items():
            tabs.append(
                ui.nav_panel(
                    group_spec.get("description", group_id),
                    ui.h4(f"Group: {group_id}"),
                    ui.markdown("Discovery-driven analysis space.")
                )
            )

        return ui.navset_card_tab(*tabs, id="central_theater_tabs")

    # 4. Reactive Tiers (ADR-024 / ADR-031)

    @reactive.Calc
    def tier1_anchor():
        """Scans the physical Parquet anchor (Predicate Pushdown ready)."""
        path = anchor_path.get()
        if not path:
            return pl.DataFrame().lazy()
        return pl.scan_parquet(path)

    @reactive.Calc
    def tier3_leaf():
        """Tier 3: Final reactive view with UI filters and column visibility."""
        lf = tier1_anchor()
        cols = lf.columns

        # 1. Apply UI Row Filters
        for col in cols[:10]:  # Align with sidebar_filters
            try:
                val = getattr(input, f"filter_{col}")()
                if val and val != "All":
                    lf = lf.filter(pl.col(col) == val)
            except:
                pass

        # 2. Apply Column Visibility
        try:
            visible_cols = input.column_visibility_picker()
            if visible_cols:
                # Ensure Primary Keys are always included
                pkeys = primary_keys()
                final_cols = list(set(visible_cols) | set(pkeys))
                # Maintain original order
                ordered_cols = [c for c in cols if c in final_cols]
                lf = lf.select(ordered_cols)
        except:
            pass

        # 3. Apply Wrangle Studio Logic (Phase 11-F)
        # We wrap back to LazyFrame if it was collected previously,
        # but here tier1_anchor() is lazy, and we collected it at the end.
        # Wait, tier3_leaf returns lf.collect(). I should apply logic BEFORE collect.

        # Convert lf (which is a LazyFrame)
        lf = wrangle_studio.apply_logic(lf)

        return lf.collect()

    # 5. Render Outputs

    @output
    @render.plot
    def plot_anchor():
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

        # Additional Data Discovery (11-C)
        additional = cfg.raw_config.get("additional_datasets_schemas", {})
        if additional:
            nodes.append(ui.hr())
            nodes.append(ui.h6("Discovery Extensions"))
            for ads_id in additional.keys():
                nodes.append(
                    ui.div(f"Source: {ads_id}", class_="audit-node-tier2"))

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
