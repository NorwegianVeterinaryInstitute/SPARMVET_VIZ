# SPARMVET_VIZ — UI Panel Map & CSS Selector Reference

> Reference for choosing background colors and typography per panel.
> All panels are CSS-controllable via the selectors below.
> Add overrides in `config/ui/theme.css` (section 16+) or in a persona CSS file.

---

## Global Structure (all views)

```
┌───────────────────────────────────────────────────────────────────────────────────┐
│  BANNER                                                         .sparmvet-banner  │
├──────────────────────┬────────────────────────────────┬───────────────────────────┤
│  LEFT SIDEBAR        │  CENTRAL THEATER               │  RIGHT SIDEBAR            │
│  #nav_sidebar        │  .central-theater              │  #audit_sidebar           │
│  width: 340px        │  #main_layout_inner            │  width: 340px             │
│                      │  .theater-container-main       │  (view-dependent)         │
└──────────────────────┴────────────────────────────────┴───────────────────────────┘
```

---

## VIEW 1 — Home (developer)

```
┌───────────────────────────────────────────────────────────────────────────────────────────────┐
│  BANNER  .sparmvet-banner                                                                     │
├───────────────────────────┬───────────────────────────────────────────┬───────────────────────┤
│  LEFT SIDEBAR             │  CENTRAL THEATER                          │  RIGHT SIDEBAR        │
│  #nav_sidebar             │                                           │  #audit_sidebar       │
│                           │                                           │                       │
│ ╔═══════════════════════╗ │ ┌───────────────────────────────────────┐ │ ┌───────────────────┐ │
│ ║  Nav Pills Strip      ║ │ │  Theater Header Strip                 │ │ │  Pipeline Audit   │ │
│ ║  Home · Blueprint ·   ║ │ │  .theater-header-strip                │ │ │  card             │ │
│ ║  Test Lab · Gallery   ║ │ │  "Data to show:" + T1 / T2 / T3       │ │ │  #audit_sidebar   │ │
│ ║  #nav_sidebar         ║ │ └───────────────────────────────────────┘ │ │  .card            │ │
│ ║  .flex-column > .bg-  ║ │                                           │ │                   │ │
│ ║  white                ║ │ ┌───────────────────────────────────────┐ │ │  ── card-header ──│ │
│ ╚═══════════════════════╝ │ │  Main Plot Card                       │ │ │  "Pipeline Audit" │ │
│                           │ │  #central_theater_tabs                │ │ │  #audit_sidebar   │ │
│ ┌───────────────────────┐ │ │                                       │ │ │  .card-header     │ │
│ │  Manifest Choice      │ │ │  ┌─────────────────────────────────┐  │ │ │                   │ │
│ │  accordion panel      │ │ │  │  Plot Tabs (analysis groups)    │  │ │ │  ⏳ Pending       │ │
│ │  #nav_accordion       │ │ │  │  #central_theater_tabs          │  │ │ │  .recipe-pending- │ │
│ │  .accordion-button    │ │ │  │  .card-header .nav-tabs         │  │ │ │  badge            │ │
│ │  .accordion-body      │ │ │  └─────────────────────────────────┘  │ │ │                   │ │
│ └───────────────────────┘ │ │  ┌─────────────────────────────────┐  │ │ │  Tier 2 —         │ │
│                           │ │  │  Plot Content / Data Table      │  │ │ │  Inherited  h6    │ │
│ ┌───────────────────────┐ │ │  │  .card-body                     │  │ │ │                   │ │
│ │  Data Import          │ │ │  │  (plot image or table output)   │  │ │ │  .audit-node-tier2│ │
│ │  accordion panel      │ │ │  └─────────────────────────────────┘  │ │ │  (repeats)        │ │
│ │  #nav_accordion       │ │ └───────────────────────────────────────┘ │ │                   │ │
│ │  .accordion-button    │ │                                           │ │  ── hr ───────── ─│ │
│ │  .accordion-body      │ │ ┌───────────────────────────────────────┐ │ │                   │ │
│ └───────────────────────┘ │ │  Data Preview Accordion               │ │ │  Tier 3 —         │ │
│                           │ │  #acc_home_data                       │ │ │  My Adjustments   │ │
│ ┌───────────────────────┐ │ │  .accordion-button / .accordion-body  │ │ │  h6               │ │
│ │  Filters              │ │ │  (column selector + data grid)        │ │ │                   │ │
│ │  accordion panel      │ │ └───────────────────────────────────────┘ │ │  .audit-node-tier3│ │
│ │  #nav_accordion       │ │                                           │ │  (repeats)        │ │
│ │  .accordion-button    │ │                                           │ │                   │ │
│ │  .accordion-body      │ │                                           │ │  ── bottom ────── │ │
│ └───────────────────────┘ │                                           │ │  [  Apply  ]      │ │
│                           │                                           │ │  #btn_apply       │ │
│ ┌───────────────────────┐ │                                           │ └───────────────────┘ │
│ │  Global Project       │ │                                           │                       │
│ │  Export               │ │                                           │                       │
│ │  accordion panel      │ │                                           │                       │
│ └───────────────────────┘ │                                           │                       │
│                           │                                           │                       │
│ ┌───────────────────────┐ │                                           │                       │
│ │  Session Management   │ │                                           │                       │
│ │  accordion panel      │ │                                           │                       │
│ └───────────────────────┘ │                                           │                       │
└───────────────────────────┴───────────────────────────────────────────┴───────────────────────┘
```

### Home — CSS selectors per panel

| Panel label | CSS selector | Notes |
|---|---|---|
| Banner | `.sparmvet-banner` | Background + border |
| Nav pills strip | `#nav_sidebar .flex-column > .bg-white` | Home/Blueprint/… pill bar |
| Any accordion header (title bar) | `#nav_sidebar .accordion-button` | All accordion title bars |
| Any accordion body (content) | `#nav_sidebar .accordion-body` | All accordion content areas |
| Theater header strip | `.theater-header-strip` | "Data to show:" + tier toggle |
| Main plot card (whole card) | `#central_theater_tabs` | The big central card |
| Plot tab bar | `#central_theater_tabs .card-header` | Tabs row at top of plot card |
| Plot content area | `#central_theater_tabs .card-body` | Image/table area |
| Data preview accordion | `#acc_home_data` | Whole accordion block |
| Data preview header | `#acc_home_data .accordion-button` | Clickable header |
| Data preview body | `#acc_home_data .accordion-body` | Column picker + grid |
| Audit sidebar card | `#audit_sidebar .card` | Whole right card |
| Audit card header | `#audit_sidebar .card-header` | "Pipeline Audit" title bar |
| Audit card body | `#audit_sidebar .card .card-body` | Tier 2 / Tier 3 content |
| Tier 2 node | `.audit-node-tier2` | Individual T2 step |
| Tier 3 node | `.audit-node-tier3` | Individual T3 step |
| Pending badge | `.recipe-pending-badge` | Yellow ⏳ Pending chip |
| Apply button | `#btn_apply` | Bottom of audit sidebar |

---

## VIEW 2 — Blueprint Architect

```
┌───────────────────────────────────────────────────────────────────────────────────────────────┐
│  BANNER  .sparmvet-banner                                                                     │
├───────────────────────────┬───────────────────────────────────────────┬───────────────────────┤
│  LEFT SIDEBAR             │  CENTRAL THEATER                          │  RIGHT SIDEBAR        │
│  #nav_sidebar             │                                           │  #audit_sidebar       │
│  (Wrangle Studio mode)    │                                           │  (Blueprint Surgeon)  │
│                           │                                           │                       │
│ ╔═══════════════════════╗ │ ┌───────────────────────────────────────┐ │ ┌───────────────────┐ │
│ ║  Nav Pills Strip      ║ │ │  VIEW TITLE BANNER                    │ │ │  Blueprint Surgeon│ │
│ ║  Home · Blueprint ·   ║ │ │  .view-title-banner                   │ │ │  card             │ │
│ ║  Test Lab · Gallery   ║ │ │  "Blueprint Architect Flight Deck"    │ │ │  ── card-header ──│ │
│ ╚═══════════════════════╝ │ │  "Pipeline overview — …"              │ │ │  "Blueprint       │ │
│                           │ └───────────────────────────────────────┘ │ │   Surgeon"        │ │
│ ┌───────────────────────┐ │ ┌───────────────────────────────────────┐ │ │                   │ │
│ │  Master Manifest      │ │ │  TubeMap Accordion                    │ │ │  🔬 Focused node  │ │
│ │  accordion panel      │ │ │  #blueprint_tubemap_accordion         │ │ │  info             │ │
│ │  #wrangle_sidebar_    │ │ │  (Cytoscape graph)                    │ │ │                   │ │
│ │  accordion            │ │ └───────────────────────────────────────┘ │ │  ── hr ────────── │ │
│ └───────────────────────┘ │ ┌───────────────────────────────────────┐ │ │                   │ │
│ ┌───────────────────────┐ │ │  Tri-tab Work Area (nav-pills)        │ │ │  Active Logic     │ │
│ │  External Exchange    │ │ │  #architect_internal_tabs             │ │ │  Stack  h6        │ │
│ │  accordion panel      │ │ │  Focus · Interface · YAML             │ │ │  .audit-node-tier3│ │
│ └───────────────────────┘ │ └───────────────────────────────────────┘ │ │  (repeats)        │ │
└───────────────────────────┴───────────────────────────────────────────┴───────────────────────┘
```

### Blueprint Architect — CSS selectors per panel

| Panel label | CSS selector | Notes |
|---|---|---|
| Left accordion wrapper | `#wrangle_sidebar_accordion` | Wrangle Studio left panels |
| Master Manifest header | `#wrangle_sidebar_accordion .accordion-button` | Shared with External Exchange |
| Studio main card | `#central_theater_tabs` | Whole central card |
| Blueprint Surgeon card | `#audit_sidebar .card` | Right card |
| Blueprint Surgeon header | `#audit_sidebar .card-header` | Title bar |
| Node focus info | `#audit_sidebar .card .card-body` | Selected node details + stack |

---

## VIEW 3 — Test Lab

```
┌───────────────────────────────────────────────────────────────────────────────────────────────┐
│  BANNER  .sparmvet-banner                                                                     │
├───────────────────────────┬───────────────────────────────────────────┬───────────────────────┤
│  LEFT SIDEBAR             │  CENTRAL THEATER                          │  RIGHT SIDEBAR        │
│  #nav_sidebar             │                                           │  #audit_sidebar       │
│  (standard accordion)     │                                           │  (Dev Inspector)      │
│                           │                                           │                       │
│ ╔═══════════════════════╗ │ ┌───────────────────────────────────────┐ │ ┌───────────────────┐ │
│ ║  Nav Pills Strip      ║ │ │  VIEW TITLE BANNER                    │ │ │  Dev Inspector    │ │
│ ║  Home · Blueprint ·   ║ │ │  .view-title-banner                   │ │ │  card             │ │
│ ║  Test Lab · Gallery   ║ │ │  "Test Lab: Synthetic Engine"         │ │ │  ── card-header ──│ │
│ ╚═══════════════════════╝ │ │  "Generate mock datasets…"            │ │ │  "Dev Inspector"  │ │
│                           │ └───────────────────────────────────────┘ │ │                   │ │
│ ┌───────────────────────┐ │ ┌───────────────────────────────────────┐ │ │  🔧 placeholder   │ │
│ │  Data Import          │ │ │  Generation Configuration card        │ │ │  (UX-DEVINSP-1)   │ │
│ │  accordion panel      │ │ │  + Environment Audit card             │ │ └───────────────────┘ │
│ └───────────────────────┘ │ └───────────────────────────────────────┘ │                       │
│ (+ shared panels per      │                                           │                       │
│  persona flags)           │                                           │                       │
└───────────────────────────┴───────────────────────────────────────────┴───────────────────────┘
```

### Test Lab — CSS selectors per panel

| Panel label | CSS selector | Notes |
|---|---|---|
| Left sidebar | same as Home view | Accordion panels shared |
| Test Lab main card | `#central_theater_tabs` | Same card, different content |
| Dev Inspector card | `#audit_sidebar .card` | Right card |
| Dev Inspector header | `#audit_sidebar .card-header` | Title bar |

---

## VIEW 4 — Gallery

> **ADR-057 (2026-05-02):** Gallery filter sidebar moved from internal `ui.layout_sidebar()` to persistent left `#nav_sidebar`. Main content is now full-width.

```
┌───────────────────────────────────────────────────────────────────────────────────────────────┐
│  BANNER  .sparmvet-banner                                                                     │
├───────────────────────────┬───────────────────────────────────────────┬───────────────────────┤
│  LEFT SIDEBAR             │  CENTRAL THEATER  (full width)            │  RIGHT SIDEBAR        │
│  #nav_sidebar             │                                           │  #audit_sidebar       │
│  (Gallery accordion)      │                                           │  (Gallery Explorer)   │
│                           │                                           │                       │
│ ╔═══════════════════════╗ │ ┌───────────────────────────────────────┐ │ ┌───────────────────┐ │
│ ║  Nav Pills Strip      ║ │ │  VIEW TITLE BANNER                    │ │ │  Gallery Explorer │ │
│ ║  Home · Blueprint ·   ║ │ │  .view-title-banner                   │ │ │  card             │ │
│ ║  Test Lab · Gallery   ║ │ │  "📚 Gallery Inspiration"             │ │ │  ── card-header ──│ │
│ ╚═══════════════════════╝ │ │  "Browse visual recipes…"             │ │ │  "Gallery         │ │
│                           │ └───────────────────────────────────────┘ │ │   Explorer"       │ │
│ ┌───────────────────────┐ │ ┌───────────────────────────────────────┐ │ │                   │ │
│ │  🖼️ Recipe            │ │ │  Preview tabs                         │ │ │  placeholder      │ │
│ │  accordion panel      │ │ │  #gallery_tech_tabs                   │ │ │  (UX-GALLEXP-1)   │ │
│ │  #gallery_sidebar_    │ │ │  Plot Preview / Data Sample / YAML    │ │ └───────────────────┘ │
│ │  accordion            │ │ └───────────────────────────────────────┘ │                       │
│ │  gallery_recipe_      │ │ ┌───────────────────────────────────────┐ │                       │
│ │  select + clone btn   │ │ │  Educational Guidance                 │ │                       │
│ └───────────────────────┘ │ │  .gallery-md-pane                     │ │                       │
│ ┌───────────────────────┐ │ │  (yellow sticky-note pane)            │ │                       │
│ │  🔍 Gallery Taxonomy  │ │ └───────────────────────────────────────┘ │                       │
│ │  accordion panel      │ │                                           │                       │
│ │  Family / Pattern /   │ │                                           │                       │
│ │  Difficulty filters   │ │                                           │                       │
│ │  .gallery-sidebar-    │ │                                           │                       │
│ │  group (×3)           │ │                                           │                       │
│ │  [▶ Apply]            │ │                                           │                       │
│ └───────────────────────┘ │                                           │                       │
└───────────────────────────┴───────────────────────────────────────────┴───────────────────────┘
```

### Gallery — CSS selectors per panel

| Panel label | CSS selector | Notes |
|---|---|---|
| Gallery sidebar accordion | `#gallery_sidebar_accordion` | Recipe + Taxonomy panels in nav_sidebar |
| Gallery taxonomy filters | `.gallery-sidebar-group` | Filter groups (Family, Data Pattern, Difficulty) |
| Gallery filter title | `.gallery-filter-title` | 0.85rem/700/uppercase section labels |
| Recipe selector + clone | inside `#gallery_sidebar_accordion` | `#gallery_recipe_select`, `#btn_clone_gallery` |
| View title banner | `.view-title-banner` | "📚 Gallery Inspiration" header |
| Recipe preview/guidance | `.gallery-md-pane` | Markdown educational pane (yellow bg — intentional) |
| Preview tabs | `#gallery_tech_tabs` | Preview / Data / YAML tabs |
| Gallery Explorer card | `#audit_sidebar .card` | Right card (placeholder, UX-GALLEXP-1) |
| Gallery Explorer header | `#audit_sidebar .card-header` | Title bar |

---

## Quick Reference — Colors currently in use

> Updated Phase 26. Canonical three-color system in `config/ui/theme.css` section 6.

| Role | Color | Selector(s) |
|---|---|---|
| Primary blue (buttons, active pills) | `#345beb` | `.btn-primary`, `.nav-pills .nav-link.active`, `#btn_apply`, `#btn_generate_data`, `#btn_apply_gallery_filters` |
| Primary blue hover | `#2a4bc4` | `.btn-primary:hover` |
| Export / exchange teal | `#10a395` | `#export_bundle_download`, `#export_audit_report_download`, `#btn_export`, `#export_global`, `#btn_download_manifest`, `#export_single_graph`, `#session_export_active`, `#filter_add_row`, `#btn_upload_replace`, `#btn_upload_append`, `#btn_import_manifest` |
| Reset / discard amber | `#ffc107` | `#filter_reset`, `.recipe-pending-badge` |
| Accordion header bg | `#a0a0a0` | `#nav_sidebar .accordion-button` |
| Sidebar body bg | `#c0c0c0` | `--bslib-sidebar-bg` on `#main_layout_outer/inner` |
| Page background | `#d1d1d1` | `body` |
| Audit node T2 bg | `#eef0fb` (blue tint) | `.audit-node-tier2` |
| Audit node T3 bg | `#e6f7f5` (teal tint) | `.audit-node-tier3` |
| TubeMap accordion header | `#345beb` | `#blueprint_tubemap_accordion .accordion-button` |
| Micro text | `0.65rem / #6c757d` | `.ultra-small` |

## Typography scale (3-tier, all views)

| Tier | Size | Weight | Used for |
|---|---|---|---|
| Primary | `0.85rem` | `700` | Section headings, accordion buttons, badges |
| Secondary | `0.80rem` | `400–600` | Body content, form labels, filter choices |
| Micro | `0.65rem` | `400` | Helper text, dtype labels, meta |

## View title banners (ADR-056)

| View | Title | Subtitle | CSS class |
|---|---|---|---|
| Blueprint Architect | "Blueprint Architect Flight Deck" | "Pipeline overview — helps you build manifests." | `.view-title-banner` |
| Test Lab | "Test Lab: Synthetic Engine" | "Generate mock datasets to verify pipeline robustness across any schema." | `.view-title-banner` |
| Gallery | "📚 Gallery Inspiration" | "Browse visual recipes for inspiration. Did you see a nice figure? Send us a request for recipe implementation." | `.view-title-banner` |

## Per-panel background — add here when colors decided

```css
/* ── Panel backgrounds (fill in chosen colors) ─────────────────────────── */
/* Nav pills strip     */ #nav_sidebar .flex-column > .bg-white           { background-color: ??? !important; }
/* Theater header      */ .theater-header-strip                            { background-color: ???; }
/* Main plot card      */ #central_theater_tabs                            { background-color: ???; }
/* Plot tab bar        */ #central_theater_tabs .card-header               { background-color: ???; }
/* Data preview        */ #acc_home_data                                   { background-color: ???; }
/* Audit sidebar card  */ #audit_sidebar .card                             { background-color: ???; }
/* Audit card header   */ #audit_sidebar .card-header                      { background-color: ???; }
/* Audit card body     */ #audit_sidebar .card .card-body                  { background-color: ???; }
/* T2 nodes            */ .audit-node-tier2                                { background-color: ???; }
/* T3 nodes            */ .audit-node-tier3                                { background-color: ???; }
```
