# app/src/ui.py
from shiny import ui
from app.src.bootloader import bootloader

# 1. System Aesthetics (ADR-027, ADR-030)
CSS_THEME = """
    .sidebar-left { background-color: #f8f9fa; border-right: 1px solid #dee2e6; }
    .sidebar-right { background-color: #f8f9fa; border-left: 1px solid #dee2e6; }
    .central-theater { background-color: #ffffff; padding: 20px; }
    .audit-node-tier2 { background-color: #f3e5f5; border-radius: 4px; padding: 5px; margin-bottom: 5px; }
    .audit-node-tier3 { background-color: #fffde7; border-radius: 4px; padding: 5px; margin-bottom: 5px; }
    .header-controls { background-color: #f8f9fa; border-radius: 4px; padding: 2px 8px; }
    .control-btn { border: none; background: none; color: #6c757d; padding: 0 5px; cursor: pointer; }
    .control-btn:hover { color: #0d6efd; }
    .table-container { border-top: 1px solid #dee2e6; padding-top: 15px; }
    /* Comparison Theater (ADR-029a Phase 12-A) */
    .reference-pane { background-color: #f8f9fa; border-right: 2px solid #dee2e6; border-radius: 6px; padding: 12px; }
    .reference-label { color: #856404; background: #fff3cd; border: 1px solid #ffc107; border-radius: 4px; padding: 4px 10px; font-size: 0.85em; margin-bottom: 8px; display: block; }
    .active-pane { background-color: #ffffff; border-radius: 6px; padding: 12px; }
    .apply-btn-container { text-align: right; margin-bottom: 10px; }
    .recipe-pending-badge { display: inline-block; background: #ffc107; color: #000; border-radius: 10px; padding: 1px 8px; font-size: 0.78em; margin-right: 6px; }
    .soft-note-modal .modal-content { background-color: #fff9c4 !important; border: 1px solid #ffeb3b; }
    .soft-note-modal .modal-header { border-bottom: 1px solid #ffeb3b; }
    .soft-note-modal .modal-footer { border-top: 1px solid #ffeb3b; }
    .gallery-md-pane img { max-width: 100%; height: auto; border-radius: 8px; margin: 10px 0; box-shadow: 0 4px 6px rgba(0,0,0,0.1); }
"""

app_ui = ui.page_fillable(
    ui.head_content(
        ui.tags.style(CSS_THEME),
        ui.tags.link(
            rel="stylesheet", href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.1/font/bootstrap-icons.css")
    ),

    # Header
    ui.panel_title(ui.output_text("app_title")),

    # 3-Zone Shell (ADR-029a)
    ui.layout_sidebar(
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
                *([ui.nav_panel("Wrangle Studio", ui.div(id="wrangle_studio_sidebar_anchor"))]
                  if bootloader.is_enabled("developer_mode_enabled") else []),
                ui.nav_panel("Visual Designer", ui.h5("Plot Configuration")),
                *([ui.nav_panel("Dev Studio", ui.h5("Synthetic Engine"))]
                  if bootloader.is_enabled("developer_mode_enabled") else []),
                *([ui.nav_panel("Gallery", ui.h5("Public Recipes"))]
                  if bootloader.is_enabled("gallery_enabled") else []),
                id="sidebar_nav"
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
        ui.layout_sidebar(
            # 3. Audit Stack (Right)
            ui.sidebar(
                ui.h3("Audit Stack"),
                ui.markdown("---"),
                ui.div(
                    ui.h5("Inherited Logic (Tier 2)"),
                    # ADR-003: Dynamically populated from active manifest
                    ui.output_ui("audit_nodes_tier2"),
                    id="audit_stack_tier2"
                ),
                ui.hr(),
                ui.div(
                    ui.h5("User Logic (Tier 3)"),
                    ui.output_ui("audit_nodes_tier3"),
                    id="audit_stack_tier3"
                ),
                ui.input_action_button(
                    "btn_gallery_open_submission", "🌟 Submit to Gallery", class_="btn-success w-100 mb-2"),
                ui.input_action_button(
                    "restore_session", "🔄 Restore Original", class_="btn-outline-secondary w-100"),
                id="audit_sidebar",
                bg="#f8f9fa",
                width="300px",
                position="right"
            ),
            # 2. Central Theater (Center) — ADR-029a Comparison Theater
            ui.div(
                # Theater Header
                ui.div(
                    ui.h4(ui.output_text("active_tab_title")),
                    ui.div(
                        # Theater state controls
                        ui.input_action_button("btn_max_plot", ui.tags.i(
                            class_="bi bi-graph-up"), class_="control-btn", title="Maximize Plot"),
                        ui.input_action_button("btn_max_table", ui.tags.i(
                            class_="bi bi-table"), class_="control-btn", title="Maximize Table"),
                        ui.input_action_button("btn_reset_theater", ui.tags.i(
                            class_="bi bi-grid-1x2"), class_="control-btn", title="Split View"),
                        ui.tags.span(
                            "|", style="color:#dee2e6; margin: 0 4px;"),
                        # Comparison Mode toggle — gated by persona (ADR-026)
                        ui.output_ui("comparison_mode_toggle_ui"),
                        class_="header-controls d-flex align-items-center gap-1"
                    ),
                    class_="d-flex justify-content-between align-items-center mb-3"
                ),
                ui.output_ui("dynamic_tabs"),
                class_="central-theater"
            ),
            fillable=True
        ),
        fillable=True
    )
)
