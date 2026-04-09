# app/src/server.py
from shiny import render, reactive, ui
import polars as pl
from pathlib import Path
from datetime import datetime

# Authority: Library Sovereignty (ADR-003)
from app.src.bootloader import bootloader
from app.modules.orchestrator import DataOrchestrator
from utils.config_loader import ConfigManager
from viz_factory.viz_factory import VizFactory


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

        # Grid layout for plots/tables
        theater_layout = ui.layout_columns(
            ui.card(
                ui.card_header("Tier 2: Reference (Branch)"),
                ui.output_plot("plot_anchor"),
                ui.output_table("table_anchor"),
                full_screen=True
            ),
            ui.card(
                ui.card_header("Tier 3: Active Leaf (Filtered)"),
                ui.output_plot("plot_leaf"),
                ui.output_table("table_leaf"),
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
        """Tier 3: Final reactive view with UI filters applied."""
        lf = tier1_anchor()
        cols = lf.columns
        for col in cols[:10]:  # Align with sidebar_filters
            try:
                val = getattr(input, f"filter_{col}")()
                if val and val != "All":
                    lf = lf.filter(pl.col(col) == val)
            except:
                pass
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
    @reactive.event(input.restore_session)
    def handle_restore():
        ui.notification_show("🔄 Session State Restored.", type="warning")

    # 7. Ghost Save Logic (ADR-031)
    @reactive.Effect
    def ghost_save_trigger():
        freq = bootloader.get_automation_setting(
            "ghost_save", "frequency_minutes")
        if bootloader.is_enabled("ghost_save_enabled"):
            print(
                f"💾 Ghost Save (State Only) @ {datetime.now().strftime('%H:%M:%S')}")

        reactive.invalidate_later(freq * 60)
