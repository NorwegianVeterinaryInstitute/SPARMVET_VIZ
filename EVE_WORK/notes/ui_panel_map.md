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
│ ║  Nav Pills Strip      ║ │ │  Wrangle Studio Main Card             │ │ │  Blueprint Surgeon│ │
│ ║  Home · Blueprint ·   ║ │ │  #central_theater_tabs                │ │ │  card             │ │
│ ║  Test Lab · Gallery   ║ │ │                                       │ │ │  #audit_sidebar   │ │
│ ╚═══════════════════════╝ │ │  ┌─────────────────────────────────┐  │ │ │  .card            │ │
│                           │ │  │  TubeMap (Cytoscape graph)      │  │ │ │                   │ │
│ ┌───────────────────────┐ │ │  │  (network visualisation)        │  │ │ │  ── card-header ──│ │
│ │  Master Manifest      │ │ │  └─────────────────────────────────┘  │ │ │  "Blueprint       │ │
│ │  accordion panel      │ │ │  ┌─────────────────────────────────┐  │ │ │   Surgeon"        │ │
│ │  #wrangle_sidebar_    │ │ │  │  Studio Panels (tabs)           │  │ │ │                   │ │
│ │  accordion            │ │ │  │  (Spec Editor, Wrangler, etc.)  │  │ │ │  🔬 Focused node  │ │
│ │  .accordion-button    │ │ │  └─────────────────────────────────┘  │ │ │  (selected node   │ │
│ │  .accordion-body      │ │ └───────────────────────────────────────┘ │ │   info)           │ │
│ └───────────────────────┘ │                                           │ │                   │ │
│                           │                                           │ │  ── hr ────────── │ │
│ ┌───────────────────────┐ │                                           │ │                   │ │
│ │  External Exchange    │ │                                           │ │  Active Logic     │ │
│ │  accordion panel      │ │                                           │ │  Stack  h6        │ │
│ │  #wrangle_sidebar_    │ │                                           │ │                   │ │
│ │  accordion            │ │                                           │ │  .audit-node-tier3│ │
│ └───────────────────────┘ │                                           │ │  (repeats)        │ │
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
│ ║  Nav Pills Strip      ║ │ │  Test Lab Main Card                   │ │ │  Dev Inspector    │ │
│ ║  Home · Blueprint ·   ║ │ │  #central_theater_tabs                │ │ │  card             │ │
│ ║  Test Lab · Gallery   ║ │ │  (diagnostic tools, debug outputs)    │ │ │  #audit_sidebar   │ │
│ ╚═══════════════════════╝ │ └───────────────────────────────────────┘ │ │  .card            │ │
│                           │                                           │ │                   │ │
│ ┌───────────────────────┐ │                                           │ │  ── card-header ──│ │
│ │  Data Import          │ │                                           │ │  "Dev Inspector"  │ │
│ │  accordion panel      │ │                                           │ │                   │ │
│ └───────────────────────┘ │                                           │ │  🔧 Developer     │ │
│                           │                                           │ │  diagnostic tools │ │
│ ┌───────────────────────┐ │                                           │ └───────────────────┘ │
│ │  Filters              │ │                                           │                       │
│ │  accordion panel      │ │                                           │                       │
│ └───────────────────────┘ │                                           │                       │
│ ┌───────────────────────┐ │                                           │                       │
│ │  Global Project       │ │                                           │                       │
│ │  Export               │ │                                           │                       │
│ └───────────────────────┘ │                                           │                       │
│ ┌───────────────────────┐ │                                           │                       │
│ │  Session Management   │ │                                           │                       │
│ └───────────────────────┘ │                                           │                       │
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

```
┌───────────────────────────────────────────────────────────────────────────────────────────────┐
│  BANNER  .sparmvet-banner                                                                     │
├───────────────────────────┬───────────────────────────────────────────┬───────────────────────┤
│  LEFT SIDEBAR             │  CENTRAL THEATER                          │  RIGHT SIDEBAR        │
│  #nav_sidebar             │  (Gallery has its OWN inner sidebar)      │  #audit_sidebar       │
│  (Discovery Mode)         │                                           │  (Gallery Explorer)   │
│                           │                                           │                       │
│ ╔═══════════════════════╗ │ ┌──────────────┬────────────────────────┐ │ ┌───────────────────┐ │
│ ║  Nav Pills Strip      ║ │ │ Gallery      │  Recipe Preview +      │ │ │  Gallery Explorer │ │
│ ║  Home · Blueprint ·   ║ │ │ Inner        │  Guidance Panel        │ │ │  card             │ │
│ ║  Test Lab · Gallery   ║ │ │ Sidebar      │  .gallery-md-pane      │ │ │                   │ │
│ ╚═══════════════════════╝ │ │              │                        │ │ │  ── card-header ──│ │
│                           │ │ Recipe       │  #gallery_tech_tabs    │ │ │  "Gallery         │ │
│ ┌───────────────────────┐ │ │ selector +   │  (Preview / Data /     │ │ │   Explorer"       │ │
│ │  Discovery Mode       │ │ │ Clone btn    │   YAML tabs)           │ │ │                   │ │
│ │  message              │ │ │              │                        │ │ │  📚 Browse visual │ │
│ │  (no accordion here)  │ │ │ Gallery      │                        │ │ │  recipes          │ │
│ │  .text-muted          │ │ │ Taxonomy     │                        │ │ └───────────────────┘ │
│ └───────────────────────┘ │ │ filters      │                        │ │                       │
│                           │ │ .gallery-    │                        │ │                       │
│                           │ │ sidebar-     │                        │ │                       │
│                           │ │ group        │                        │ │                       │
│                           │ └──────────────┴────────────────────────┘ │                       │
└───────────────────────────┴───────────────────────────────────────────┴───────────────────────┘
```

### Gallery — CSS selectors per panel

| Panel label | CSS selector | Notes |
|---|---|---|
| Gallery inner sidebar | `.bslib-sidebar-layout` inside central theater | Gallery's own filter sidebar |
| Gallery taxonomy filters | `.gallery-sidebar-group` | Filter groups (Family, Plot type…) |
| Gallery filter title | `.gallery-filter-title` | Bold underlined group labels |
| Recipe selector block | `.px-3.py-2.border.rounded.bg-white` in gallery sidebar | Recipe picker + Clone button |
| Recipe preview/guidance | `.gallery-md-pane` | Markdown rendered guidance pane |
| Preview tabs | `#gallery_tech_tabs` | Preview / Data / YAML tabs |
| Gallery Explorer card | `#audit_sidebar .card` | Right card |
| Gallery Explorer header | `#audit_sidebar .card-header` | Title bar |

---

## Quick Reference — Colors currently in use

| Role | Color | Selector(s) |
|---|---|---|
| Primary blue (buttons, active pills) | `#345beb` | `.btn-primary`, `.nav-pills .nav-link.active` |
| Primary blue hover | `#2a4bc4` | `.btn-primary:hover` |
| Export teal (all export buttons) | `#10a395` | `#export_bundle_download`, `#export_audit_report_download`, `#btn_export`, `#export_global`, `#btn_download_manifest` |
| Accordion header bg | `#a0a0a0` | `#nav_sidebar .accordion-button` |
| Sidebar body bg | `#c0c0c0` | `--bslib-sidebar-bg` on `#main_layout_outer/inner` |
| Page background | `#d1d1d1` | `body` |
| Audit node T2 bg | `#f3e5f5` (violet-tint) | `.audit-node-tier2` |
| Audit node T3 bg | `#fffde7` (yellow-tint) | `.audit-node-tier3` |
| Info/warning microtext | `#345beb` | `#nav_sidebar .text-info`, `.text-warning` |
| Micro text | `0.65rem / #6c757d` | `.ultra-small` |

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
