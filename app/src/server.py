# app/src/server.py
from shiny import render, reactive, ui
import polars as pl
from pathlib import Path
from datetime import datetime

# Authority: Library Sovereignty (ADR-003)
from app.src.bootloader import bootloader
from app.modules.orchestrator import DataOrchestrator


def server(input, output, session):

    # 1. Path & Logic Authority
    orchestrator = DataOrchestrator(
        manifests_dir=bootloader.get_location("manifests"),
        raw_data_dir=bootloader.get_location("raw_data")
    )

    # 2. State Management (Paths to Anchors)
    anchor_path = reactive.Value(None)

    # 3. Initialization Task (Tier 1 Materialization)
    @reactive.Effect
    def init_data():
        ui.notification_show(
            "🚀 Initializing Tier 1 Data Ingestion...", type="message")

        pipeline_id = "1_Abromics_general_pipeline"
        assembly_id = "AR1_MLST_Serotype_Virulence"
        output_file = bootloader.get_location(
            "curated_data") / "session_anchor.parquet"

        try:
            # Execute Ingestion & Assembly (ADR-024)
            # This triggers sink_parquet inside DataAssembler
            orchestrator.materialize_tier1(
                pipeline_id=pipeline_id,
                assembly_id=assembly_id,
                output_path=output_file
            )

            anchor_path.set(str(output_file))
            ui.notification_show(
                "✅ Tier 1 Materialization Complete.", type="message")
        except Exception as e:
            ui.notification_show(f"❌ Ingestion Error: {e}", type="error")
            print(f"Error: {e}")

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
        # In Phase 11-D, we'll add dynamic filter logic here
        return lf.collect()

    # 5. Render Outputs (Skeleton)

    @output
    @render.table
    def table_anchor():
        # Displaying first 5 rows for verification
        return tier1_anchor().head(5).collect()

    @output
    @render.table
    def table_leaf():
        return tier3_leaf().head(5)

    @output
    @render.plot
    def plot_leaf():
        return None

    @output
    @render.ui
    def audit_nodes_tier3():
        return ui.div(
            ui.div("Pipeline: 1_Abromics_general_pipeline",
                   class_="audit-node-tier2"),
            ui.div("Assembly: AR1_MLST_Serotype_Virulence",
                   class_="audit-node-tier2"),
            ui.div("Step: sink_parquet(session_anchor.parquet)",
                   class_="audit-node-tier3"),
        )

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
