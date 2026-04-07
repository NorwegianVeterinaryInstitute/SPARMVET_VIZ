# app/src/server.py
from shiny import render, reactive, ui
from app.modules.persona_manager import PersonaManager
from viz_factory.viz_factory import VizFactory
import polars as pl
from datetime import datetime

# 1. Bootload Persona-Based Reactive State
def server(input, output, session):
    persona_manager = PersonaManager(mode="pipeline")
    viz_factory = VizFactory()
    
    # --- Data State (Tiers 2 & 3) ---
    
    @reactive.Calc
    def tier2_branch():
        """Tier 2 Branch: Post-wrangling baseline data (The Ground Truth)."""
        # Mocking Abromics demo data baseline
        return pl.DataFrame({
            "sample_date": ["2023-01-01", "2023-01-15", "2023-02-01", "2023-02-20"],
            "species": ["E. coli", "E. coli", "Salmonella", "S. aureus"],
            "amr_class": ["Beta-lactam", "Sulfonamide", "Beta-lactam", "Aminoglycoside"],
            "score": [98, 92, 95, 88]
        })

    @reactive.Calc
    def tier3_leaf():
        """Tier 3 Leaf: Final presentation data with Predicate Pushdown (ADR-024)."""
        # 1. Start with the LazyFrame from the Branch
        lf = tier2_branch().lazy()
        
        # 2. Extract UI filters from the sidebar (Predicate Pushdown)
        # In a real app, these are derived from input values mapped in ui.py
        current_species = input.species_filter() if hasattr(input, "species_filter") else None
        
        if current_species:
            lf = lf.filter(pl.col("species").is_in(current_species))
            
        # 3. Materialize at the gate
        return lf.collect()

    # --- Narrative Audit Trail (ADR-026) ---
    
    audit_trail = reactive.Value([])

    @reactive.Effect
    @reactive.event(input.species_filter)
    def log_filter_change():
        """Appends a timestamped entry to the Narrative Log."""
        ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        entry = f"[{ts}] FILTER: Species restricted to {input.species_filter()}"
        audit_trail.set(audit_trail() + [entry])

    @output
    @render.ui
    def narrative_log():
        """Displays the session trace in the sidebar."""
        return ui.HTML("<br>".join(audit_trail()))

    # --- Manual Exclusions (User Notes) ---
    
    @reactive.Effect
    @reactive.event(input.drop_selected)
    def handle_manual_exclusion():
        """Triggers mandatory User Note modal on data exclusion."""
        m = ui.modal(
            ui.input_text_area("exclusion_note", "Justify this exclusion (Mandatory for Audit Trace)"),
            title="Manual Data Exclusion",
            footer=ui.modal_button("Save Note & Exclude"),
            easy_close=False
        )
        ui.modal_show(m)

    # --- Render Logic (Dual-View Sync) ---
    
    @output
    @render.table
    def reference_table():
        """Syncs Tab A to the Tier 2 Branch immediately."""
        return tier2_branch()

    @output
    @render.table
    def active_table():
        """Syncs Tab B to the Tier 3 Leaf ONLY on interaction."""
        return tier3_leaf()

    @output
    @render.plot
    def active_plot():
        """Presentation Layer Integration (VizFactory)."""
        data = tier3_leaf()
        # Placeholder Render Loop (VizFactory)
        return None
