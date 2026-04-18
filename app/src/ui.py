# app/src/ui.py
from shiny import ui
from app.src.bootloader import bootloader

# 1. System Aesthetics (ADR-027, ADR-030)
CSS_THEME = """
    body { background-color: #d1d1d1; margin: 0 !important; padding: 0 !important; }
    .sidebar-left { background-color: #c0c0c0; border-right: 1px solid #a0a0a0; height: 100vh; overflow-y: auto; }
    .sidebar-right { background-color: #c0c0c0; border-left: 1px solid #a0a0a0; height: 100vh; overflow-y: auto; }
    .sidebar-content { padding: 4px; }
    .central-theater { background-color: transparent !important; padding: 0 !important; min-height: 100vh; }
    .card { margin-bottom: 4px !important; }
    .card.navset-card-tab { margin: 0 !important; border: none !important; border-radius: 0 !important; }
    .audit-node-tier2 { background-color: #f3e5f5; border-radius: 4px; padding: 2px; margin-bottom: 2px; border-left: 3px solid #9c27b0; }
    .audit-node-tier3 { background-color: #fffde7; border-radius: 4px; padding: 2px; margin-bottom: 2px; border-left: 3px solid #fbc02d; }
    .header-controls { border-radius: 4px; padding: 1px 6px; }
    .control-btn { border: none; background: none; color: #6c757d; padding: 1px 4px; cursor: pointer; border-radius: 4px; }
    .control-btn:hover { color: #0d6efd; background-color: #e9ecef; }
    .table-container { border-top: 1px solid #dee2e6; padding-top: 4px; margin-top: 4px; }
    /* Comparison Theater (ADR-029a Phase 12-A) */
    .reference-pane { background-color: #f8f9fa; border: 1px solid #dee2e6; border-radius: 6px; padding: 6px; box-shadow: inset 0 0 10px rgba(0,0,0,0.02); }
    .reference-label { color: #856404; background: #fff3cd; border: 1px solid #ffbc00; border-radius: 4px; padding: 2px 6px; font-size: 0.85em; margin-bottom: 4px; font-weight: 600; text-transform: uppercase; letter-spacing: 0.5px; }
    .active-pane { background-color: #ffffff; border: 1px solid #dee2e6; border-radius: 6px; padding: 6px; }
    .apply-btn-container { text-align: right; margin-bottom: 5px; }
    .recipe-pending-badge { display: inline-block; background: #ffc107; color: #000; border-radius: 12px; padding: 1px 6px; font-size: 0.75em; font-weight: bold; margin-right: 4px; vertical-align: middle; }
    /* Structural Gaps (ADR-027, Drawing #2) */
    .bslib-sidebar-layout { --bslib-sidebar-overlap: 0px !important; --bslib-sidebar-gap: 4px !important; --bs-gutter-x: 4px !important; }
    .bslib-grid { gap: 4px !important; }
    #main_layout_inner, #main_layout_outer { padding: 0 !important; }
    .gallery-md-pane img { max-width: 100%; height: auto; border-radius: 8px; margin: 10px 0; box-shadow: 0 4px 6px rgba(0,0,0,0.1); }
"""

app_ui = ui.page_fillable(
    ui.head_content(
        ui.tags.style(CSS_THEME),
        ui.tags.link(
            rel="stylesheet", href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.1/font/bootstrap-icons.css")
    ),

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
            class_="sidebar-content p-2",
            width="320px",
            id="nav_sidebar"
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
                ui.output_ui("dynamic_tabs"),
                class_="central-theater p-0 bg-transparent h-100"
            ),
            id="main_layout_inner",
            fillable=True,
            border=False
        ),
        id="main_layout_outer",
        fillable=True,
        border=False
    ),
    fillable=True
)
