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
    .header-controls { background-color: #f8f9fa; border-radius: 4px; padding: 2px 8px; }
    .control-btn { border: none; background: none; color: #6c757d; padding: 0 5px; cursor: pointer; }
    .control-btn:hover { color: #0d6efd; }
    .table-container { border-top: 1px solid #dee2e6; padding-top: 15px; }
"""

app_ui = ui.page_fillable(
    ui.head_content(
        ui.tags.style(CSS_THEME)
    ),

    # Header
    ui.panel_title(ui.output_text("app_title")),

    # 3-Zone Shell (ADR-029a)
    ui.layout_column_wrap(
        # 1. Navigation Panel (Left)
        ui.sidebar(
            ui.h3("Project Manager"),
            ui.input_select("project_id", "Select Project:",
                            choices=list(
                                bootloader.available_projects.keys()),
                            selected=bootloader.get_default_project()),
            ui.hr(),
            ui.navset_pill_list(
                ui.nav_panel("Project Hub", ui.h5("Available Projects")),
                ui.nav_panel("Wrangle Studio", ui.h5("Transformation Nodes")),
                ui.nav_panel("Visual Designer", ui.h5("Plot Configuration")),
                ui.nav_panel("Gallery", ui.h5("Public Recipes")),
            ),
            ui.hr(),
            ui.h5("Agnostic Filters"),
            ui.output_ui("sidebar_filters"),
            ui.hr(),
            ui.input_select("persona_selector", "Persona:",
                            {"user": "Standard User", "dev": "Developer Mode"},
                            selected="user") if bootloader.is_enabled("developer_mode_enabled") else ui.div(),
            ui.hr(),
            ui.h5("External Ingestion"),
            ui.input_file("file_ingest", "Upload Excel/CSV",
                          accept=[".xlsx", ".csv", ".tsv"]),
            ui.input_action_button(
                "btn_ingest", "🚀 Ingest to Trunk", class_="btn-outline-primary w-100"),
            ui.hr(),
            ui.input_action_button(
                "export_global", "📦 Global Export", class_="btn-primary w-100"),
            id="nav_sidebar",
            bg="#f8f9fa",
            width="250px"
        ),

        # 2. Central Theater (Center)
        ui.div(
            ui.div(
                ui.h4(ui.output_text("active_tab_title")),
                ui.input_switch("layout_toggle_header",
                                "Comparison Mode", value=False),
                class_="d-flex justify-content-between align-items-center mb-3"
            ),
            ui.output_ui("dynamic_tabs"),
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
