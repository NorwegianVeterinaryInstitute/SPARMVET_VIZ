# app/src/ui.py
from shiny import ui
from app.src.bootloader import bootloader

# 1. System Aesthetics (ADR-027, ADR-030)
CSS_THEME = """
    .sidebar-left { background-color: #f8f9fa !format; border-right: 1px solid #dee2e6; }
    .sidebar-right { background-color: #f8f9fa !format; border-left: 1px solid #dee2e6; }
    .central-theater { background-color: #ffffff; padding: 20px; }
    .audit-node-tier2 { background-color: #f3e5f5; border-radius: 4px; padding: 5px; margin-bottom: 5px; }
    .audit-node-tier3 { background-color: #fffde7; border-radius: 4px; padding: 5px; margin-bottom: 5px; }
"""

app_ui = ui.page_fillable(
    ui.head_content(
        ui.tags.style(CSS_THEME)
    ),

    # Header
    ui.panel_title("SPARMVET_VIZ: Abromics Intelligence Dashboard",
                   "SPARMVET Dashboard"),

    # 3-Zone Shell (ADR-029a)
    ui.layout_column_wrap(
        # 1. Navigation Panel (Left)
        ui.sidebar(
            ui.h3("Navigation"),
            ui.navset_pill_list(
                ui.nav_panel("Pipeline Hub", ui.h5("Active Pipelines")),
                ui.nav_panel("Wrangle Studio", ui.h5("Transformation Nodes")),
                ui.nav_panel("Visual Designer", ui.h5("Plot Configuration")),
                ui.nav_panel("Gallery", ui.h5("Public Recipes")),
            ),
            ui.hr(),
            ui.input_select("persona_selector", "Persona:",
                            {"user": "Standard User", "dev": "Developer Mode"},
                            selected="user") if bootloader.is_enabled("developer_mode_enabled") else ui.div(),

            ui.spacer(),
            ui.input_action_button(
                "export_global", "📦 Global Export", class_="btn-primary w-100"),
            id="nav_sidebar",
            bg="#f8f9fa",
            width="250px"
        ),

        # 2. Central Theater (Center)
        ui.div(
            ui.navset_card_tab(
                ui.nav_panel(
                    "Analysis Theater",
                    ui.layout_column_wrap(
                        ui.card(
                            ui.card_header("Tier 1/2: Reference (Anchor)"),
                            ui.output_table("table_anchor"),
                            full_screen=True
                        ),
                        ui.card(
                            ui.card_header("Tier 3: Active Leaf (Filtered)"),
                            ui.output_plot("plot_leaf"),
                            ui.output_table("table_leaf"),
                            full_screen=True
                        ),
                        width=1/1  # Stacked by default, can be toggled to side-by-side
                    )
                ),
                ui.nav_panel("Data Inspector",
                             ui.output_table("full_data_table")),
                id="central_theater_tabs"
            ),
            class_="central-theater"
        ),

        # 3. Audit Stack (Right)
        ui.sidebar(
            ui.h3("Audit Stack"),
            ui.markdown("---"),
            ui.div(
                ui.h5("Inherited Logic (Tier 2)"),
                ui.div("Column selection: species, amr_class",
                       class_="audit-node-tier2"),
                ui.div("Merge: metadata_v1", class_="audit-node-tier2"),
                id="audit_stack_tier2"
            ),
            ui.hr(),
            ui.div(
                ui.h5("User Logic (Tier 3)"),
                ui.output_ui("audit_nodes_tier3"),
                id="audit_stack_tier3"
            ),
            ui.spacer(),
            ui.input_action_button(
                "restore_session", "🔄 Restore Original", class_="btn-outline-secondary w-100"),
            id="audit_sidebar",
            bg="#f8f9fa",
            width="300px",
            position="right"
        ),

        width=1,  # This forces the layout to handle sidebars correctly
        heights_equal="all"
    )
)
