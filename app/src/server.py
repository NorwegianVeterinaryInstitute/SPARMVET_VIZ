# app/src/server.py
from shiny import render, reactive, ui
from app.modules.persona_manager import PersonaManager
from app.modules.exporter import SubmissionExporter
from viz_factory.viz_factory import VizFactory
import polars as pl
import yaml
from pathlib import Path
from datetime import datetime

# 1. Bootload Persona-Based Reactive State
def server(input, output, session):
    persona_manager = PersonaManager(mode="pipeline")
    viz_factory = VizFactory()
    
    # --- Data State (Tiers 2 & 3) ---
    
    @reactive.Calc
    def tier2_branch():
        """Tier 2 Branch: Post-wrangling baseline data (The Ground Truth)."""
        # Improved Abromics mock data (ensures all columns for filters and plots)
        return pl.DataFrame({
            "sample_date": ["2023-01-01", "2023-01-15", "2023-02-01", "2023-02-20"],
            "species": ["E. coli", "E. coli", "Salmonella", "S. aureus"],
            "amr_class": ["Beta-lactam", "Sulfonamide", "Beta-lactam", "Aminoglycoside"],
            "status": ["Resistant", "Intermediate", "Resistant", "Sensitive"],
            "count": [10, 20, 15, 8] # Column required for the y-mapping in manifest
        })

    @reactive.Calc
    def tier3_leaf():
        """Tier 3 Leaf: Final presentation data with Predicate Pushdown (ADR-024)."""
        # 1. Start with the LazyFrame from the Branch
        lf = tier2_branch().lazy()
        
        # 2. Comprehensive Sidebar Filtering (Predicate Pushdown)
        if hasattr(input, "species_filter") and input.species_filter():
            lf = lf.filter(pl.col("species").is_in(list(input.species_filter())))
            
        if hasattr(input, "amr_filter") and input.amr_filter():
            lf = lf.filter(pl.col("amr_class").is_in(list(input.amr_filter())))

        # 3. Handle Date Filtering (Converting to Date type for Polars)
        # Note: input.date_filter() returns (start, end)
        if hasattr(input, "date_filter") and input.date_filter():
           start, end = input.date_filter()
           if start and end:
               lf = lf.filter(pl.col("sample_date").cast(pl.Date).is_between(start, end))

        # 4. Materialize at the gate
        return lf.collect()

    # --- Narrative Audit Trail (ADR-026) ---
    
    audit_trail = reactive.Value([])

    @reactive.Effect
    @reactive.event(input.species_filter, input.amr_filter, input.date_filter)
    def log_filter_change():
        """Appends a timestamped entry to the Narrative Log."""
        ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        entry = f"[{ts}] FILTER UPDATE: Refining exploration via Sidebar."
        audit_trail.set(audit_trail() + [entry])

    @output
    @render.ui
    def narrative_log():
        """Displays the session trace in the sidebar."""
        return ui.HTML("<br>".join(audit_trail()))

    # --- Ghost Manifest Auto-Save (ADR-021) ---

    @reactive.Effect
    def ghost_auto_save():
        """Background task that silently saves the UI state/manifest every 60s."""
        current_state = {
            "active_persona": persona_manager.persona,
            "filters": {
                "species": list(input.species_filter()) if hasattr(input, "species_filter") else [],
                "amr_class": list(input.amr_filter()) if hasattr(input, "amr_filter") else []
            },
            "timestamp": datetime.now().isoformat()
        }
        tmp_path = Path("tmp/last_state.yaml")
        tmp_path.parent.mkdir(parents=True, exist_ok=True)
        with open(tmp_path, "w") as f:
            yaml.dump(current_state, f)
        reactive.invalidate_later(60)

    # --- Render Logic (Dual-View Sync) ---
    
    @output
    @render.table
    def reference_table():
        return tier2_branch()

    @output
    @render.table
    def active_table():
        return tier3_leaf()

    @output
    @render.plot
    def active_plot():
        """Presentation Layer Integration (VizFactory)."""
        data = tier2_branch() # Always start with the Branch LazyFrame
        base_manifest = persona_manager.config
        
        # 1. Update Filters from UI inputs
        plot_cfg = base_manifest.get("plots", {}).get("amr_distribution", {})
        plot_cfg["filters"] = []
        
        if hasattr(input, "species_filter") and input.species_filter():
            plot_cfg["filters"].append({"column": "species", "op": "in", "value": list(input.species_filter())})
        
        if hasattr(input, "amr_filter") and input.amr_filter():
            plot_cfg["filters"].append({"column": "amr_class", "op": "in", "value": list(input.amr_filter())})

        # 2. Render through the Artist Pillar
        try:
            return viz_factory.render(data, base_manifest, "amr_distribution")
        except Exception as e:
            print(f"❌ VizFactory Rendering Error: {e}")
            return None

    # --- Manual Exclusions (User Notes) ---
    
    @reactive.Effect
    @reactive.event(input.drop_selected)
    def handle_manual_exclusion():
        m = ui.modal(
            ui.input_text_area("exclusion_note", "Justify this exclusion (Mandatory for Audit Trace)"),
            title="Manual Data Exclusion",
            footer=ui.modal_button("Save Note & Exclude"),
            easy_close=False
        )
        ui.modal_show(m)

    # --- Export & Reproducibility ---
    
    @reactive.Effect
    @reactive.event(input.export_zip)
    def handle_export():
        ui.notification_show("📦 Initializing Reproducibility Bundle Export...", type="message")
        exporter = SubmissionExporter()
        
        data = tier3_leaf()
        narrative = audit_trail()
        recipe = {"active_persona": persona_manager.persona, "filters": {"species": list(input.species_filter())}}
        
        zip_path = exporter.bundle_package(
            plot_path="tmp/last_plot.png", 
            data_df=data.to_pandas(), 
            manifest=recipe, 
            audit_trail=narrative
        )
        ui.notification_show(f"✅ Export Ready: {Path(zip_path).name}", type="message", duration=10)
