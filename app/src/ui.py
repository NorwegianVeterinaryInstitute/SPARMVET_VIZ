# app/src/ui.py
from shiny import ui
from app.src.bootloader import bootloader

# 1. System Aesthetics (ADR-027, ADR-030)
CSS_THEME = """
    .sidebar-left { background-color: #f8f9fa; border-right: 1px solid #dee2e6; height: 100vh; overflow-y: auto; }
    .sidebar-right { background-color: #f8f9fa; border-left: 1px solid #dee2e6; height: 100vh; overflow-y: auto; }
    .sidebar-content { padding: 15px; }
    .central-theater { background-color: #ffffff; padding: 25px; min-height: 100vh; }
    .audit-node-tier2 { background-color: #f3e5f5; border-radius: 4px; padding: 5px; margin-bottom: 5px; border-left: 3px solid #9c27b0; }
    .audit-node-tier3 { background-color: #fffde7; border-radius: 4px; padding: 5px; margin-bottom: 5px; border-left: 3px solid #fbc02d; }
    .header-controls { background-color: #f8f9fa; border-radius: 4px; padding: 4px 12px; border: 1px solid #dee2e6; }
    .control-btn { border: none; background: none; color: #6c757d; padding: 4px 8px; cursor: pointer; border-radius: 4px; }
    .control-btn:hover { color: #0d6efd; background-color: #e9ecef; }
    .table-container { border-top: 1px solid #dee2e6; padding-top: 15px; margin-top: 20px; }
    /* Comparison Theater (ADR-029a Phase 12-A) */
    .reference-pane { background-color: #f8f9fa; border: 1px solid #dee2e6; border-radius: 6px; padding: 15px; box-shadow: inset 0 0 10px rgba(0,0,0,0.02); }
    .reference-label { color: #856404; background: #fff3cd; border: 1px solid #ffbc00; border-radius: 4px; padding: 6px 12px; font-size: 0.85em; margin-bottom: 12px; font-weight: 600; text-transform: uppercase; letter-spacing: 0.5px; }
    .active-pane { background-color: #ffffff; border: 1px solid #dee2e6; border-radius: 6px; padding: 15px; }
    .apply-btn-container { text-align: right; margin-bottom: 15px; }
    .recipe-pending-badge { display: inline-block; background: #ffc107; color: #000; border-radius: 12px; padding: 2px 10px; font-size: 0.75em; font-weight: bold; margin-right: 8px; vertical-align: middle; }
    .soft-note-modal .modal-content { background-color: #fff9c4 !important; border: 1px solid #ffeb3b; box-shadow: 0 10px 30px rgba(0,0,0,0.1); }
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
            ui.div(
                ui.card(
                    ui.card_header(ui.h5("Project Navigator", class_="mb-0")),
                    ui.div(
                        ui.input_select("project_id", "Select Project:",
                                        choices=list(
                                            bootloader.available_projects.keys()),
                                        selected=bootloader.get_default_project()),
                        ui.output_ui("sidebar_nav_ui"),
                        class_="p-3"
                    ),
                    class_="mb-4 shadow-sm"
                ),
                ui.card(
                    ui.card_header(ui.h5("Agnostic Filters", class_="mb-0")),
                    ui.div(
                        ui.output_ui("sidebar_filters"),
                        class_="p-3"
                    ),
                    class_="mb-4 shadow-sm"
                ),
                ui.output_ui("system_tools_ui"),
                class_="shadow-sm"
            ),
            class_="sidebar-content p-2"
        ),
        id="nav_sidebar",
        bg="#f8f9fa",
        width="350px"
    ),
    ui.layout_sidebar(
        # 3. Audit Stack (Right)
        ui.sidebar(
            ui.div(
                ui.card(
                    ui.card_header(ui.h5("Pipeline Audit", class_="mb-0")),
                    ui.div(
                        ui.h6("Tier 2 (Inherited)", class_="text-muted"),
                        ui.output_ui("audit_nodes_tier2"),
                        ui.hr(),
                        ui.h6("Tier 3 (User)", class_="text-muted"),
                        ui.output_ui("audit_nodes_tier3"),
                        class_="p-3"
                    ),
                    class_="mb-4 shadow-sm"
                ),
                ui.div(
                    ui.output_ui("audit_stack_tools_ui"),
                    class_="mt-auto p-2"
                ),
                class_="sidebar-content p-2 d-flex flex-column h-100"
            ),
            id="audit_sidebar",
            bg="#f8f9fa",
            width="350px",
            position="right"
        ),
        # 2. Central Theater (Center)
        ui.div(
            ui.div(
                ui.h4(ui.output_text("active_tab_title")),
                ui.div(
                    ui.input_action_button("btn_max_plot", ui.tags.i(
                        class_="bi bi-graph-up"), class_="control-btn"),
                    ui.input_action_button("btn_max_table", ui.tags.i(
                        class_="bi bi-table"), class_="control-btn"),
                    ui.input_action_button("btn_reset_theater", ui.tags.i(
                        class_="bi bi-grid-1x2"), class_="control-btn"),
                    ui.tags.span(
                        "|", style="color:#dee2e6; margin: 0 10px;"),
                    # Gated comparison toggle
                    ui.output_ui("comparison_mode_toggle_ui"),
                    class_="header-controls d-flex align-items-center bg-white border rounded px-3 py-1"
                ),
                class_="d-flex justify-content-between align-items-center mb-4"
            ),
            ui.output_ui("dynamic_tabs"),
            class_="central-theater p-4 bg-white shadow-sm border rounded"
        ),
        fillable=True
    ),
    fillable=True
)
)
