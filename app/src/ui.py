# app/src/ui.py
from shiny import ui, render, reactive
from app.modules.persona_manager import PersonaManager

# 1. Initialize Persona Manager Bootloader (ADR-026)
persona_manager = PersonaManager(mode="pipeline")

# 2. Define UI Scaffolding
app_ui = ui.page_fluid(
    ui.panel_title("SPARMVET Abromics Pipeline Dashboard"),
    
    ui.layout_sidebar(
        ui.sidebar(
            ui.h3("Tier 3 Filters (Leaf)"),
            # Dynamic Filters (Abromics Demo)
            ui.input_selectize("species_filter", "Species Selection:", 
                              ["E. coli", "Salmonella", "S. aureus"], 
                              multiple=True),
            
            ui.input_action_button("drop_selected", "Drop Selected Rows", class_="btn-danger"),
            
            ui.hr(),
            ui.h4("Session Narrative Audit"),
            ui.output_ui("narrative_log"),
            
            ui.hr(),
            ui.input_action_button("export_zip", "📦 Export Analysis Bundle (.zip)"),
            bg="#f8f9fa",
            width=300
        ),
        
        # 3. Dual-View Analysis (Tab A: Reference | Tab B: Active)
        ui.navset_tab(
            ui.nav_panel(
                "📈 Tab A: Reference Branch (Ground Truth)",
                ui.card(
                    ui.card_header("Tier 2 (Branch) - Baseline Data"),
                    ui.output_table("reference_table")
                )
            ),
            ui.nav_panel(
                "🍃 Tab B: Active Leaf (Exploration)",
                ui.card(
                    ui.card_header("Tier 3 (Leaf) - Filtered View"),
                    ui.output_plot("active_plot"),
                    ui.output_table("active_table")
                )
            ),
            id="analysis_tabs"
        )
    )
)
