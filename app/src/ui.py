# app/src/ui.py
from shiny import ui
from app.src.bootloader import bootloader

# 1. System Aesthetics (ADR-027, ADR-030)
CSS_THEME = """
    body { background-color: #d1d1d1; margin: 0 !important; padding: 0 !important; }
    .sidebar-left { background-color: #c0c0c0; border-right: 1px solid #a0a0a0; height: 100vh; overflow-y: auto; }
    .sidebar-right { background-color: #c0c0c0; border-left: 1px solid #a0a0a0; height: 100vh; overflow-y: auto; }
    .sidebar-content { padding: 0 !important; }
    .central-theater { background-color: transparent !important; padding: 0 !important; min-height: 100vh; }
    .card { margin-bottom: 0px !important; }
    .card.navset-card-tab { margin: 0 !important; border: none !important; border-radius: 0 !important; box-shadow: none !important; }
    .audit-node-tier2 { background-color: #f3e5f5; border-radius: 4px; padding: 2px; margin-bottom: 2px; border-left: 3px solid #9c27b0; font-size: 0.85em; }
    .audit-node-tier3 { background-color: #fffde7; border-radius: 4px; padding: 2px; margin-bottom: 2px; border-left: 3px solid #fbc02d; font-size: 0.85em; }
    
    /* High-Density Navigation Panel (Aggressive Override) */
    #nav_sidebar .accordion-body { padding: 2px 4px !important; background-color: #c0c0c0; }
    #nav_sidebar .accordion-button { padding: 2px 8px !important; font-size: 0.85rem; font-weight: 700; background-color: #a0a0a0 !important; color: #1a1a1a !important; border-bottom: 1px solid #909090; }
    #nav_sidebar .accordion-item { border: none !important; background-color: transparent !important; }
    #nav_sidebar label { margin-bottom: 0px !important; font-size: 0.72rem !important; font-weight: 700 !important; color: #333 !important; text-transform: uppercase !important; letter-spacing: 0.5px !important; display: block; }
    #nav_sidebar .shiny-input-container { margin-bottom: 2px !important; padding: 0 !important; }
    #nav_sidebar .form-select, #nav_sidebar .form-control { padding: 1px 6px !important; font-size: 0.8rem !important; height: 28px !important; min-height: 28px !important; border-radius: 3px !important; }
    #nav_sidebar .control-label { margin-top: 2px !important; }
    
    /* Right Sidebar Symmetrical Polish */
    #audit_sidebar .card { border-radius: 0 !important; }
    #audit_sidebar .card-header { padding: 4px 8px !important; font-size: 0.85rem; font-weight: 700; background-color: #a0a0a0 !important; }
    
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
    
    /* Structural Gaps (ADR-027, User Review Refinement) */
    .bslib-sidebar-layout { --bslib-sidebar-overlap: 0px !important; --bslib-sidebar-gap: 10px !important; --bs-gutter-x: 10px !important; }
    .bslib-grid { gap: 10px !important; }
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
                ui.accordion(
                    ui.accordion_panel(
                        "Project Navigator",
                        ui.div(
                            ui.input_select("project_id", "Project Selection",
                                            choices=list(
                                                bootloader.available_projects.keys()),
                                            selected=bootloader.get_default_project()),
                            ui.output_ui("sidebar_nav_ui"),
                            class_="d-flex flex-column gap-1"
                        ),
                        icon=ui.tags.i(class_="bi bi-folder-fill")
                    ),
                    ui.accordion_panel(
                        "Agnostic Filters",
                        ui.div(
                            ui.output_ui("sidebar_filters"),
                            class_="d-flex flex-column gap-1"
                        ),
                        icon=ui.tags.i(class_="bi bi-filter-circle-fill")
                    ),
                    ui.accordion_panel(
                        "System Tools",
                        ui.div(
                            ui.output_ui("system_tools_ui"),
                            class_="d-flex flex-column gap-1"
                        ),
                        icon=ui.tags.i(class_="bi bi-cpu-fill")
                    ),
                    id="nav_accordion",
                    multiple=True,
                    open=["Project Navigator", "Agnostic Filters"]
                ),
                class_="h-100 w-100"
            ),
            class_="sidebar-content p-0",
            width="340px",
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
                            class_="p-2"
                        ),
                        class_="mb-2 shadow-sm border-0"
                    ),
                    ui.div(
                        ui.output_ui("audit_stack_tools_ui"),
                        class_="mt-auto p-2"
                    ),
                    class_="sidebar-content p-0 d-flex flex-column h-100"
                ),
                id="audit_sidebar",
                bg="#c0c0c0",  # Symmetrical grey
                width="340px",
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
