# app/src/ui.py
from shiny import ui
from app.src.bootloader import bootloader

print("--- LOADING UI VERSION V5.1 (Aggressive Centering) ---")
# 1. System Aesthetics (ADR-027, ADR-030)
CSS_THEME = """
    body { background-color: #d1d1d1; margin: 0 !important; padding: 0 !important; }
    .sidebar-left { background-color: #c0c0c0; border-right: 1px solid #a0a0a0; height: 100vh; overflow-y: auto; }
    .sidebar-right { background-color: #c0c0c0; border-left: 1px solid #a0a0a0; height: 100vh; overflow-y: auto; }
    .sidebar-content { padding: 0 !important; }
    .central-theater { background-color: transparent !important; padding: 0 !important; min-height: 100vh; }
    .card { margin-bottom: 0px !important; }

    /* ── Shared panel token: white, rounded, soft shadow ───────────────────────
       Applied to every surface card in Home Theater and Blueprint Architect.
       Use class="spv-panel" on any wrapping div. */
    .spv-panel {
        background: #ffffff;
        border-radius: 8px;
        box-shadow: 0 1px 4px rgba(0,0,0,0.08);
        border: 1px solid #e9ecef;
        margin-bottom: 10px;
        overflow: hidden;
    }
    /* All Shiny cards inside a theater get the same rounding */
    .theater-container-main .card,
    .theater-container-main .accordion-item {
        border-radius: 8px !important;
        box-shadow: 0 1px 4px rgba(0,0,0,0.08) !important;
        background: #ffffff !important;
    }
    /* accordion-item top/bottom edges inside a spv-panel: let the panel handle radius */
    .spv-panel > .accordion > .accordion-item:first-child { border-radius: 8px 8px 0 0 !important; }
    .spv-panel > .accordion > .accordion-item:last-child  { border-radius: 0 0 8px 8px !important; }
    /* Wrangle Studio central card: borderless, full-height, scoped to its ID */
    #central_theater_tabs.card.navset-card-tab { margin: 0 !important; border: none !important; border-radius: 0 !important; box-shadow: none !important; }
    .audit-node-tier2 { background-color: #f3e5f5; border-radius: 4px; padding: 2px; margin-bottom: 2px; border-left: 3px solid #9c27b0; font-size: 0.85em; }
    .audit-node-tier3 { background-color: #fffde7; border-radius: 4px; padding: 2px; margin-bottom: 2px; border-left: 3px solid #fbc02d; font-size: 0.85em; }

    /* High-Density Navigation Panel (Aggressive Override) */
    #nav_sidebar .accordion-body { padding: 2px 4px !important; background-color: #c0c0c0; }
    #nav_sidebar .accordion-button { padding: 2px 8px !important; font-size: 0.85rem; font-weight: 700; background-color: #a0a0a0 !important; color: #1a1a1a !important; border-bottom: 1px solid #909090; }
    #nav_sidebar .accordion-item { border: none !important; background-color: transparent !important; }
    #nav_sidebar label { margin-bottom: 0px !important; font-size: 0.72rem !important; font-weight: 700 !important; color: #333 !important; text-transform: uppercase !important; letter-spacing: 0.5px !important; display: block; }
    #nav_sidebar .shiny-input-container { margin-bottom: 1px !important; padding: 0 !important; }
    #nav_sidebar .form-select, #nav_sidebar .form-control { padding: 1px 6px !important; font-size: 0.8rem !important; height: 26px !important; min-height: 26px !important; border-radius: 3px !important; }
    #nav_sidebar .control-label { margin-top: 1px !important; }


    /* Sidebar Toggle Polish (Aggressive Positioning) */
    .collapse-toggle { position: fixed !important; transform: scale(0.65) !important; z-index: 10000 !important; }
    #main_layout_outer > .bslib-sidebar-layout > .collapse-toggle { top: 10px !important; left: 10px !important; }
    #main_layout_inner .bslib-sidebar-layout > .collapse-toggle { top: 10px !important; right: 10px !important; }

    /* Global Card & Theatre Polish */
    .central-theater .card-header { padding: 4px 10px !important; font-size: 0.85rem; font-weight: 600; text-align: center !important; }
    .central-theater .card-header h5, .central-theater .card-header h6 { margin: 0 auto !important; }
    #central_theater_tabs > .card-header .nav-tabs { border-bottom: none !important; }

    /* Right Sidebar Symmetrical Polish */
    #audit_sidebar .card { border-radius: 0 !important; }
    #audit_sidebar .card-header { padding: 4px 8px !important; font-size: 0.85rem; font-weight: 700; background-color: #a0a0a0 !important; text-align: center !important; }

    # Button Harmonization (Drawing #3)
    #btn_revert_sync, #restore_session, #btn_export, #btn_reset_sync, #btn_reset_theater, #btn_ingest, #export_global, #btn_apply { background-color: #0d6efd !important; border-color: #0d6efd !important; color: white !important; font-weight: 600 !important; height: 32px !important; }
    .btn-primary,
    #btn_apply { font-weight: 700; border-radius: 6px !important; }

    .recipe-pending-badge { display: inline-flex; height: 32px !important; align-items: center; background: #ffc107; color: #000; border-radius: 6px !important; padding: 0 12px; font-size: 0.85rem; font-weight: 700; margin-right: 2px; border: 1px solid #e0a800; box-shadow: 0 1px 2px rgba(0,0,0,0.1); line-height: 1; }

    /* Ingest & Upload UI (ADR-031) */
    .upload-row .form-control { height: 32px !important; font-size: 0.8rem !important; border-top-left-radius: 0 !important; border-bottom-left-radius: 0 !important; }
    .upload-row .btn-file { height: 32px !important; padding: 0 8px !important; font-size: 0.8rem !important; line-height: 30px; border-top-right-radius: 0 !important; border-bottom-right-radius: 0 !important; }
    .upload-row label { display: none !important; }
    .upload-row .input-group { height: 32px !important; }

    /* Active View Button State */
    .active-view-btn { background-color: #0d6efd !important; color: white !important; border-color: #0551bc !important; box-shadow: inset 0 3px 5px rgba(0,0,0,0.125) !important; }
    .control-btn { padding: 2px 8px !important; height: 28px !important; min-width: 32px; font-size: 0.9rem; }

    .header-controls { border-radius: 4px; padding: 1px 6px; height: 36px; display: flex; align-items: center !important; }
    .header-controls .form-check-input { margin-top: 0 !important; }
    .header-controls label { margin-bottom: 0 !important; }
    .ultra-small { font-size: 0.65rem; color: #6c757d; }
    .table-container { border-top: 1px solid #dee2e6; padding-top: 4px; margin-top: 4px; }
    /* Wrangle Studio only: full-height card layout (scoped by ID) */
    #central_theater_tabs.card.navset-card-tab { height: calc(100vh - 4px) !important; min-height: calc(100vh - 4px) !important; display: flex; flex-direction: column; }
    #central_theater_tabs.card.navset-card-tab > .card-body { flex: 1 1 auto; overflow-y: auto; padding: 0 !important; }

    /* Comparison Theater (ADR-029a Phase 12-A) */
    .reference-pane { background-color: #f8f9fa; border: 1px solid #dee2e6; border-radius: 6px; padding: 6px; box-shadow: inset 0 0 10px rgba(0,0,0,0.02); }
    .reference-label { color: #856404; background: #fff3cd; border: 1px solid #ffbc00; border-radius: 4px; padding: 2px 6px; font-size: 0.85em; margin-bottom: 4px; font-weight: 600; text-transform: uppercase; letter-spacing: 0.5px; }
    .active-pane { background-color: #ffffff; border: 1px solid #dee2e6; border-radius: 6px; padding: 6px; }
    .apply-btn-container { text-align: right; margin-bottom: 5px; }

    /* Column Picker Width & Spacing (Phase 12-M / 21-F) */
    .column-picker-container { width: 100% !important; flex: 1 1 100% !important; display: block !important; }
    .column-picker-container .selectize-control { width: 100% !important; }
    .column-picker-container .selectize-input { width: 100% !important; border-radius: 4px !important; min-height: 32px !important; box-sizing: border-box !important; }
    .column-picker-container .selectize-input .item { font-size: 0.68em !important; padding: 1px 4px !important; line-height: 1.4 !important; }
    .column-picker-container .selectize-dropdown .option { font-size: 0.75em !important; padding: 3px 8px !important; }
    .column-picker-container .shiny-options-group { display: flex; flex-wrap: wrap; gap: 4px; }
    /* Ensure data preview accordion body doesn't clip selectize */
    #acc_home_data .accordion-body { overflow: visible !important; }
    #acc_home_data .shiny-html-output { width: 100% !important; }

    /* Structural Gaps (ADR-027, User Review Refinement) */
    .bslib-sidebar-layout { --bslib-sidebar-overlap: 0px !important; --bslib-sidebar-gap: 10px !important; --bs-gutter-x: 10px !important; }
    .bslib-grid { gap: 10px !important; }
    #main_layout_inner, #main_layout_outer { padding: 0 !important; }

    .gallery-md-pane img { max-width: 100%; height: auto; border-radius: 8px; margin: 10px 0; box-shadow: 0 4px 6px rgba(0,0,0,0.1); }
    .gallery-filter-title { font-weight: 800; text-decoration: underline; margin-top: 5px; margin-bottom: 5px; font-size: 1.1rem; color: #334155; }
    .gallery-sidebar-group { margin-bottom: 15px; border-bottom: 1px solid #e2e8f0; padding-bottom: 8px; padding-left: 10px; }
    .gallery-sidebar-group .form-check { margin-bottom: 0px !important; }
    .gallery-sidebar-group .shiny-input-checkbox { margin-top: 0 !important; }
    .gallery-sidebar-group .control-label { font-size: 0.8rem !important; font-weight: 600 !important; }
    /* 10px gap from sidebar edges on all sides; children use mb-10 token */
    .theater-container-main { padding: 10px !important; box-sizing: border-box; }
    /* Header strip inside theater: spv-panel without bottom-margin override */
    .theater-header-strip {
        background: #ffffff;
        border-radius: 8px;
        box-shadow: 0 1px 4px rgba(0,0,0,0.08);
        border: 1px solid #e9ecef;
        padding: 6px 14px;
        margin-bottom: 10px;
        display: flex;
        align-items: center;
        min-height: 44px;
    }
    .centered-header { text-align: center !important; margin-bottom: 15px; }

    /* Scientific Table Alignment & Zebra Grid (ADR-033/034) */
    .central-theater table, .gallery-md-pane table { border-collapse: collapse !important; border: 1px solid #cbd5e1; width: 100% !important; }
    .central-theater th, .gallery-md-pane th { text-align: left !important; background-color: #f1f5f9; border: 1px solid #cbd5e1; padding: 6px 10px !important; }
    .central-theater td, .gallery-md-pane td { text-align: left !important; border: 1px solid #cbd5e1; padding: 6px 10px !important; }
    .central-theater tr:nth-child(even), .gallery-md-pane tr:nth-child(even) { background-color: #f8fafc; }
    .central-theater tr:hover, .gallery-md-pane tr:hover { background-color: #f1f5f9; }

    /* Guidance Header Scaling */
    .gallery-md-pane h1 { font-size: 1.4rem !important; margin-top: 10px; font-weight: 800; }
    .gallery-md-pane h2 { font-size: 1.25rem !important; color: #334155; font-weight: 700; }
    .gallery-md-pane h3 { font-size: 1.1rem !important; font-weight: 700; }
    .gallery-md-pane h4, .gallery-md-pane h5 { font-size: 1.0rem !important; text-transform: uppercase; letter-spacing: 0.5px; font-weight: 700; }
"""

app_ui = ui.page_fillable(
    ui.head_content(
        ui.tags.style(CSS_THEME),
        ui.tags.link(
            rel="stylesheet", href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.1/font/bootstrap-icons.css"),
        # [ADR-039] Cytoscape.js Tube-Map Integration (replaces Mermaid + svg-pan-zoom)
        # Cytoscape core + dagre layout plugin for ranked-LR hierarchical DAG.
        ui.tags.script(
            src="https://cdn.jsdelivr.net/npm/cytoscape@3.29.2/dist/cytoscape.min.js"),
        ui.tags.script(
            src="https://cdn.jsdelivr.net/npm/dagre@0.8.5/dist/dagre.min.js"),
        ui.tags.script(
            src="https://cdn.jsdelivr.net/npm/cytoscape-dagre@2.5.0/cytoscape-dagre.js"),
        ui.tags.script("""
// ── [ADR-039] Cytoscape TubeMap Bridge ──────────────────────────────────────
//
// Global instance — one Cytoscape graph per page (the TubeMap is a singleton).
window._cyInstance = null;

// Called by wrangle_studio.py blueprint_tubemap_ui render with the JSON elements string.
function initCyTubeMap(elementsJson, containerId) {
    var container = document.getElementById(containerId || 'cy_tubemap');
    if (!container) return;

    // Destroy previous instance if Shiny replaced the DOM
    if (window._cyInstance) {
        try { window._cyInstance.destroy(); } catch(e) {}
        window._cyInstance = null;
    }

    var elements;
    try { elements = JSON.parse(elementsJson); }
    catch(e) { console.error('TubeMap: bad JSON', e); return; }

    // ── Colour palette (mirrors _CY_COLOURS in blueprint_mapper.py) ──────────
    var palette = {
        trunk:   { bg: '#0d6efd', border: '#0a58ca', text: '#ffffff' },
        ref:     { bg: '#6c757d', border: '#495057', text: '#ffffff' },
        meta:    { bg: '#fd7e14', border: '#dc6a0d', text: '#ffffff' },
        wrangle: { bg: '#ffc107', border: '#e0a800', text: '#212529' },
        branch:  { bg: '#9c27b0', border: '#7b1fa2', text: '#ffffff' },
        plot:    { bg: '#198754', border: '#146c43', text: '#ffffff' },
        info:    { bg: '#e3f2fd', border: '#1976d2', text: '#1a1a1a' },
    };

    function styleFor(role) {
        return palette[role] || { bg: '#adb5bd', border: '#6c757d', text: '#000' };
    }

    // ── Node shape per role ────────────────────────────────────────────────────
    var shapes = {
        trunk:   'ellipse',
        ref:     'ellipse',
        meta:    'ellipse',
        wrangle: 'round-rectangle',
        branch:  'diamond',
        plot:    'round-rectangle',
        info:    'round-rectangle',
    };

    // Build per-role stylesheet entries
    var roleStyles = [];
    Object.keys(palette).forEach(function(role) {
        var c = palette[role];
        roleStyles.push({
            selector: 'node.' + role,
            style: {
                'background-color': c.bg,
                'border-color':     c.border,
                'color':            c.text,
                'shape':            shapes[role] || 'ellipse',
            }
        });
    });

    var cy = cytoscape({
        container: container,
        elements:  elements,

        layout: {
            name:       'dagre',
            rankDir:    'LR',          // left → right pipeline flow
            nodeSep:    18,            // vertical gap between nodes in same tier
            rankSep:    90,            // horizontal gap between tiers
            edgeSep:    8,
            ranker:     'tight-tree',  // compact assignment — prevents gaps
            animate:    false,
        },

        style: [
            // ── Base node ────────────────────────────────────────────────────
            {
                selector: 'node',
                style: {
                    'label':              'data(label)',
                    'text-wrap':          'wrap',
                    'text-max-width':     '80px',
                    'font-size':          '9px',
                    'font-family':        'system-ui, sans-serif',
                    'text-valign':        'center',
                    'text-halign':        'center',
                    'width':              'label',
                    'height':             'label',
                    'padding':            '6px',
                    'border-width':       '1.5px',
                    'border-style':       'solid',
                    'cursor':             'pointer',
                    'transition-property':'border-width border-color',
                    'transition-duration':'0.15s',
                }
            },
            // ── Per-role colours (generated above) ──────────────────────────
            ...roleStyles,
            // ── Active / selected node ───────────────────────────────────────
            {
                selector: 'node.active',
                style: {
                    'border-width':       '3px',
                    'border-color':       '#212529',
                    'border-style':       'dashed',
                    'overlay-opacity':    0,
                }
            },
            {
                selector: 'node:selected',
                style: {
                    'border-width':       '3px',
                    'border-color':       '#212529',
                    'border-style':       'solid',
                }
            },
            // ── Hover ────────────────────────────────────────────────────────
            {
                selector: 'node:active',
                style: { 'overlay-opacity': 0.1, 'overlay-color': '#000' }
            },
            // ── Edges ────────────────────────────────────────────────────────
            {
                selector: 'edge',
                style: {
                    'width':              1.5,
                    'line-color':         '#9e9e9e',
                    'target-arrow-color': '#9e9e9e',
                    'target-arrow-shape':'triangle',
                    'arrow-scale':        0.8,
                    'curve-style':        'unbundled-bezier',
                    'control-point-distances': [20],
                    'control-point-weights':   [0.5],
                }
            },
            // ── Highlighted edge (connected to active node) ──────────────────
            {
                selector: 'edge.highlighted',
                style: {
                    'width':              2.5,
                    'line-color':         '#212529',
                    'target-arrow-color': '#212529',
                    'z-index':            10,
                }
            },
        ],

        userZoomingEnabled:   true,
        userPanningEnabled:   true,
        boxSelectionEnabled:  false,
        autounselectify:      false,
        minZoom:              0.1,
        maxZoom:              8,
    });

    // ── Click → Shiny bridge ─────────────────────────────────────────────────
    cy.on('tap', 'node', function(evt) {
        var node = evt.target;
        var schemaId = node.data('schema_id');
        if (!schemaId) return;
        console.log('TubeMap node clicked: ' + schemaId);
        Shiny.setInputValue('blueprint_node_clicked', schemaId, {priority: 'event'});

        // Highlight connected edges
        cy.edges().removeClass('highlighted');
        node.connectedEdges().addClass('highlighted');
    });

    // ── Tooltip on hover ─────────────────────────────────────────────────────
    cy.on('mouseover', 'node', function(evt) {
        var node = evt.target;
        var tip = document.getElementById('cy_tooltip');
        if (!tip) return;
        var label = node.data('label') || '';
        var role  = node.data('role')  || '';
        var grp   = node.data('group') || '';
        tip.textContent = label.replace(/\\n/g,' ') + ' [' + role + (grp ? ' · ' + grp : '') + ']';
        tip.style.display = 'block';
    });
    cy.on('mouseout', 'node', function() {
        var tip = document.getElementById('cy_tooltip');
        if (tip) tip.style.display = 'none';
    });

    cy.fit(undefined, 20);
    window._cyInstance = cy;
}
window.initCyTubeMap = initCyTubeMap;

// ── Highlight active node (called from server after component load) ───────────
function cyHighlightNode(schemaId) {
    var cy = window._cyInstance;
    if (!cy) return;
    cy.nodes().removeClass('active');
    cy.edges().removeClass('highlighted');
    var matches = cy.nodes().filter(function(n) {
        return n.data('schema_id') === schemaId;
    });
    matches.addClass('active');
    matches.connectedEdges().addClass('highlighted');
    if (matches.length > 0) {
        cy.animate({ fit: { eles: matches, padding: 60 } }, { duration: 250 });
    }
}
window.cyHighlightNode = cyHighlightNode;

// ── Toolbar helpers ──────────────────────────────────────────────────────────
function cyZoomIn()  { if (window._cyInstance) window._cyInstance.zoom(window._cyInstance.zoom() * 1.3); }
function cyZoomOut() { if (window._cyInstance) window._cyInstance.zoom(window._cyInstance.zoom() * 0.77); }
function cyFit()     { if (window._cyInstance) window._cyInstance.fit(undefined, 20); }
window.cyZoomIn  = cyZoomIn;
window.cyZoomOut = cyZoomOut;
window.cyFit     = cyFit;
        """)
    ),

    # 3-Zone Shell (ADR-029a)
    ui.layout_sidebar(
        # 1. Navigation Panel (Left)
        ui.sidebar(
            ui.div(
                # Persistent Global Navigation (Always Visible)
                ui.div(
                    ui.output_ui("sidebar_nav_ui"),
                    class_="px-3 py-2 border-bottom bg-white mb-2"
                ),
                ui.div(
                    ui.output_ui("sidebar_tools_ui"),
                    class_="flex-grow-1 overflow-auto"
                ),
                class_="h-100 w-100 d-flex flex-column"
            ),
            class_="sidebar-content p-0",
            width="340px",
            id="nav_sidebar"
        ),
        # 3. Audit Stack (Right) — excluded entirely for pipeline personas (ADR-052-§1)
        # Returning ui.div() from right_sidebar_content_ui is insufficient because the
        # 340px container stays in the DOM. Read persona at layout build time instead.
        (
            ui.div(
                ui.output_ui("dynamic_tabs"),
                class_="central-theater p-0 bg-transparent h-100",
                id="main_layout_inner",
                style="height:100%; flex:1;"
            )
            if bootloader.persona in ("pipeline-static", "pipeline-exploration-simple")
            else ui.layout_sidebar(
                ui.sidebar(
                    ui.output_ui("right_sidebar_content_ui"),
                    id="audit_sidebar",
                    bg="#c0c0c0",
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
            )
        ),
        id="main_layout_outer",
        fillable=True,
        border=False
    ),
    fillable=True
)
