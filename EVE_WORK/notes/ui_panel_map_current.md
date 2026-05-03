# SPARMVET_VIZ — UI Panel Map & CSS Selector Reference (CURRENT STATE)
# Generated 2026-05-03 — reflects commit 729b2af

> This file documents the **actual DOM structure** as of the most recent commits
> (Session 15 accordion harmonization + 729b2af styling attempt).
> Use it to identify panels precisely when reporting visual bugs.
>
> **Companion file:** `ui_panel_map.md` is the design-reference version.
> **Key divergence from old map:** `#central_theater_tabs` NO LONGER EXISTS in Python.
> CSS rules targeting it in `theme.css §2, §5, §9` are now dead/orphaned.

---

## Global Structure (all views)

```
┌───────────────────────────────────────────────────────────────────────────────────┐
│  BANNER (optional, persona-driven)                          .sparmvet-banner       │
├──────────────────────┬────────────────────────────────┬───────────────────────────┤
│  LEFT SIDEBAR        │  CENTRAL THEATER               │  RIGHT SIDEBAR            │
│  #nav_sidebar        │  .central-theater              │  #audit_sidebar           │
│  (aside.sidebar)     │  output_ui("dynamic_tabs")     │  (persona-gated)          │
│  width: ~340px       │  → renders view-specific HTML  │  width: ~340px            │
└──────────────────────┴────────────────────────────────┴───────────────────────────┘
```

---

## VIEW 1 — Home

```
┌───────────────────────────────────────────────────────────────────────────────────────────────┐
│  BANNER  .sparmvet-banner                                                                     │
├───────────────────────────┬───────────────────────────────────────────┬───────────────────────┤
│  LEFT SIDEBAR             │  CENTRAL THEATER                          │  RIGHT SIDEBAR        │
│  #nav_sidebar             │  div.theater-container-main               │  #audit_sidebar       │
│                           │                                           │                       │
│ ╔═══════════════════════╗ │ ┌───────────────────────────────────────┐ │ ┌───────────────────┐ │
│ ║  Nav Pills Strip      ║ │ │  Theater Header Strip                 │ │ │  Pipeline Audit   │ │
│ ║  Home · Blueprint ·   ║ │ │  div.theater-header-strip             │ │ │  card             │ │
│ ║  Test Lab · Gallery   ║ │ │  "Data to show:" + T1/T2/T3 toggle   │ │ │  #audit_sidebar   │ │
│ ║  #nav_sidebar         ║ │ └───────────────────────────────────────┘ │ │  .card            │ │
│ ║  .flex-column>.bg-    ║ │                                           │ │                   │ │
│ ║  white                ║ │ ┌───────────────────────────────────────┐ │ │  ── card-header ──│ │
│ ╚═══════════════════════╝ │ │  Plots Accordion                      │ │ │  "Pipeline Audit" │ │
│                           │ │  #home_plots_body_accordion           │ │ │  #audit_sidebar   │ │
│ ┌───────────────────────┐ │ │  (bslib accordion, open by default)   │ │ │  .card-header     │ │
│ │  Manifest Choice      │ │ │  header: "📊 Plots"                   │ │ │                   │ │
│ │  accordion panel      │ │ │                                       │ │ │  ⏳ Pending       │ │
│ │  #nav_accordion       │ │ │  ┌─────────────────────────────────┐  │ │ │  .recipe-pending- │ │
│ │  .accordion-button    │ │ │  │  Groups Pill Nav                │  │ │ │  badge            │ │
│ │  .accordion-body      │ │ │  │  ui.navset_pill                 │  │ │ │                   │ │
│ └───────────────────────┘ │ │  │  #home_groups_nav               │  │ │ │  Tier 2 —         │ │
│                           │ │  │  div.spv-panel (wrapper)        │  │ │ │  Inherited  h6    │ │
│ ┌───────────────────────┐ │ │  │                                 │  │ │ │  .audit-node-tier2│ │
│ │  Data Import          │ │ │  │  ┌───────────────────────────┐  │  │ │ │  (repeats)        │ │
│ │  accordion panel      │ │ │  │  │  Active Group Tab         │  │  │ │ │                   │ │
│ └───────────────────────┘ │ │  │  │  div.p-2                  │  │  │ │ │  ── hr ────────── │ │
│                           │ │  │  │                           │  │  │ │ │                   │ │
│ ┌───────────────────────┐ │ │  │  │  ┌─────────────────────┐ │  │  │ │ │  Tier 3 —         │ │
│ │  Filters              │ │ │  │  │  │ Plot Subtab Card    │ │  │  │ │ │  My Adjustments   │ │
│ │  accordion panel      │ │ │  │  │  │ ui.navset_card_tab  │ │  │  │ │ │  h6               │ │
│ └───────────────────────┘ │ │  │  │  │ id=subtabs_{group}  │ │  │  │ │ │  .audit-node-tier3│ │
│                           │ │  │  │  └─────────────────────┘ │  │  │ │ │  (repeats)        │ │
│ ┌───────────────────────┐ │ │  │  └───────────────────────────┘  │  │ │ │                   │ │
│ │  Global Project       │ │ │  └─────────────────────────────────┘  │ │ │  ── bottom ────── │ │
│ │  Export               │ │ └───────────────────────────────────────┘ │ │  [  Apply  ]      │ │
│ │  accordion panel      │ │                                           │ │  #btn_apply       │ │
│ └───────────────────────┘ │ ┌───────────────────────────────────────┐ │ └───────────────────┘ │
│                           │ │  Data Preview Accordion               │ │                       │
│ ┌───────────────────────┐ │ │  #acc_home_data                       │ │                       │
│ │  Session Management   │ │ │  (bslib accordion)                    │ │                       │
│ │  accordion panel      │ │ │  header: "📋 Data Preview"            │ │                       │
│ └───────────────────────┘ │ │  (plain string — no inline style)     │ │                       │
│                           │ │  body: column picker + data grid      │ │                       │
│                           │ └───────────────────────────────────────┘ │                       │
└───────────────────────────┴───────────────────────────────────────────┴───────────────────────┘
```

### Home — CSS selectors per panel (CURRENT)

| Panel label | CSS selector | Notes |
|---|---|---|
| Banner | `.sparmvet-banner` | Background + border |
| Nav pills strip | `#nav_sidebar .flex-column > .bg-white` | Home/Blueprint/… pill bar |
| Any sidebar accordion header | `#nav_sidebar .accordion-button` | bg `#a0a0a0`, font 0.85rem/700 |
| Any sidebar accordion body | `#nav_sidebar .accordion-body` | bg `#c0c0c0` |
| Theater header strip | `.theater-header-strip` | "Data to show:" + tier toggle |
| **Plots accordion (whole)** | `#home_plots_body_accordion` | NEW — bslib accordion wrapping all plots |
| **Plots accordion header** | `#home_plots_body_accordion .accordion-button` | Header "📊 Plots" — styled by §18b |
| **Plots accordion body** | `#home_plots_body_accordion .accordion-body` | padding: 0 (§18b flush rule) |
| **Plots accordion item** | `#home_plots_body_accordion .accordion-item` | border-radius 8px, overflow hidden |
| Groups pill nav | `#home_groups_nav` | navset_pill — group tabs |
| Groups nav wrapper | `#home_plots_body_accordion .spv-panel` | wraps pill nav, padding 8px 10px 0 10px |
| Active group plot card | `#subtabs_{group_id}` (dynamic) | navset_card_tab per group |
| **⚠️ DEAD SELECTOR** | `#central_theater_tabs` | ID no longer exists in Python — CSS rules orphaned |
| Data preview accordion (whole) | `#acc_home_data` | bslib accordion |
| Data preview header | `#acc_home_data .accordion-button` | header "📋 Data Preview" — §16 + §18b |
| Data preview body | `#acc_home_data .accordion-body` | overflow visible, padding 4px |
| Data preview item | `#acc_home_data .accordion-item` | border-radius 8px, overflow hidden |
| Audit sidebar card | `#audit_sidebar .card` | Whole right card |
| Audit card header | `#audit_sidebar .card-header` | "Pipeline Audit" title bar |
| Audit card body | `#audit_sidebar .card .card-body` | Tier 2 / Tier 3 content |
| Tier 2 node | `.audit-node-tier2` | Blue tint bg |
| Tier 3 node | `.audit-node-tier3` | Teal tint bg |
| Pending badge | `.recipe-pending-badge` | Amber chip |
| Apply button | `#btn_apply` | Bottom of audit sidebar |

---

## VIEW 2 — Blueprint Architect

```
┌───────────────────────────────────────────────────────────────────────────────────────────────┐
│  BANNER  .sparmvet-banner                                                                     │
├───────────────────────────┬───────────────────────────────────────────┬───────────────────────┤
│  LEFT SIDEBAR             │  CENTRAL THEATER                          │  RIGHT SIDEBAR        │
│  #nav_sidebar             │  div.wrangle-studio-container             │  #audit_sidebar       │
│  (Wrangle Studio mode)    │                                           │  (Blueprint Surgeon)  │
│                           │                                           │                       │
│ ╔═══════════════════════╗ │ ┌───────────────────────────────────────┐ │ ┌───────────────────┐ │
│ ║  Nav Pills Strip      ║ │ │  VIEW TITLE BANNER                    │ │ │  Blueprint Surgeon│ │
│ ║  Home · Blueprint ·   ║ │ │  div.view-title-banner                │ │ │  card             │ │
│ ║  Test Lab · Gallery   ║ │ │  "👣 Blueprint Architect Flight Deck" │ │ │  ── card-header ──│ │
│ ╚═══════════════════════╝ │ │  "Pipeline overview — …"              │ │ │  "Blueprint       │ │
│                           │ └───────────────────────────────────────┘ │ │   Surgeon"        │ │
│ ┌───────────────────────┐ │ ┌───────────────────────────────────────┐ │ │                   │ │
│ │  Master Manifest      │ │ │  TubeMap Accordion                    │ │ │  🔬 Focused node  │ │
│ │  accordion panel      │ │ │  div.spv-panel.mb-3 (outer wrapper)   │ │ │  info             │ │
│ │  #wrangle_sidebar_    │ │ │    #blueprint_tubemap_accordion        │ │ │                   │ │
│ │  accordion            │ │ │    header: "🗺️ Project Lineage"       │ │ │  ── hr ────────── │ │
│ └───────────────────────┘ │ │    (was blue, NOW #f8f9fa unified)    │ │ │                   │ │
│ ┌───────────────────────┐ │ └───────────────────────────────────────┘ │ │  Active Logic     │ │
│ │  External Exchange    │ │ ┌───────────────────────────────────────┐ │ │  Stack  h6        │ │
│ │  accordion panel      │ │ │  Work Area Accordion                  │ │ │  .audit-node-tier3│ │
│ └───────────────────────┘ │ │  #blueprint_workarea_accordion         │ │ │  (repeats)        │ │
│                           │ │  (bslib accordion, open by default)   │ │ └───────────────────┘ │
│                           │ │  header: "🗂️ Work Area"               │ │                       │
│                           │ │                                       │ │                       │
│                           │ │  ┌─────────────────────────────────┐  │ │                       │
│                           │ │  │  Tri-tab (nav-pills)            │  │ │                       │
│                           │ │  │  #architect_internal_tabs        │  │ │                       │
│                           │ │  │  ui.navset_card_pill             │  │ │                       │
│                           │ │  │  1. Focus · 2. Interface · 3. YAML│ │ │                       │
│                           │ │  └─────────────────────────────────┘  │ │                       │
│                           │ └───────────────────────────────────────┘ │                       │
│                           │ ┌───────────────────────────────────────┐ │                       │
│                           │ │  Live Data Glimpse (Bootstrap card)   │ │                       │
│                           │ │  div.card.mb-1                        │ │                       │
│                           │ │  button → collapses #glimpse_body     │ │                       │
│                           │ │  header: "📋 Live Data Glimpse"       │ │                       │
│                           │ │  (bg #f8f9fa, border-bottom #e9ecef)  │ │                       │
│                           │ └───────────────────────────────────────┘ │                       │
│                           │ ┌───────────────────────────────────────┐ │                       │
│                           │ │  Plot Preview (Bootstrap card)        │ │                       │
│                           │ │  div.card.mb-1                        │ │                       │
│                           │ │  button → collapses #plot_body        │ │                       │
│                           │ │  header: "📈 Plot Preview"            │ │                       │
│                           │ │  (bg #f8f9fa, border-bottom #e9ecef)  │ │                       │
│                           │ └───────────────────────────────────────┘ │                       │
└───────────────────────────┴───────────────────────────────────────────┴───────────────────────┘
```

### Blueprint Architect — CSS selectors per panel (CURRENT)

| Panel label | CSS selector | Notes |
|---|---|---|
| View title banner | `.view-title-banner` | White rounded panel, shared with Gallery/TestLab |
| TubeMap outer wrapper | `.wrangle-studio-container .spv-panel.mb-3` | Provides the card shadow/radius for TubeMap |
| TubeMap accordion | `#blueprint_tubemap_accordion` | bslib accordion inside spv-panel |
| TubeMap header | `#blueprint_tubemap_accordion .accordion-button` | Was blue — now `#f8f9fa` / `#1a1a1a` (§9 override) |
| TubeMap viewport | `#tubemap_viewport` | `height: 320px`, bg #fafafa |
| Work Area accordion (whole) | `#blueprint_workarea_accordion` | NEW bslib accordion |
| Work Area header | `#blueprint_workarea_accordion .accordion-button` | "🗂️ Work Area" — styled by §18b |
| Work Area body | `#blueprint_workarea_accordion .accordion-body` | padding: 0 (§18b flush rule) |
| Work Area item | `#blueprint_workarea_accordion .accordion-item` | border-radius 8px, overflow hidden |
| Tri-tab pill nav | `#architect_internal_tabs` | navset_card_pill inside Work Area body |
| Left sidebar accordion | `#wrangle_sidebar_accordion` | Wrangle Studio left panels |
| Blueprint Surgeon card | `#audit_sidebar .card` | Right card |
| Blueprint Surgeon header | `#audit_sidebar .card-header` | Title bar |
| **Live Data Glimpse card** | `.wrangle-studio-container .card.mb-1:first-of-type` | Bootstrap collapse (NOT bslib accordion) |
| **Live Data Glimpse header btn** | `#glimpse_body` closest `.card-header .btn` | fw-bold, bg #f8f9fa, border-bottom |
| **Plot Preview card** | `.wrangle-studio-container .card.mb-1:last-of-type` | Bootstrap collapse (NOT bslib accordion) |
| **Plot Preview header btn** | `#plot_body` closest `.card-header .btn` | Same style as Glimpse |
| Wrangle studio container | `.wrangle-studio-container` | All Blueprint central content |
| Bootstrap collapse buttons | `.wrangle-studio-container .card-header .btn` | Styled by §18 — font-size 0.85rem, fw-bold |
| Bootstrap collapse cards | `.wrangle-studio-container > .card` | Styled by §18 — border none, radius 8px, shadow |

---

## VIEW 3 — Test Lab

*(Structure unchanged from original map — see `ui_panel_map.md`)*

---

## VIEW 4 — Gallery

*(Structure unchanged from original map — see `ui_panel_map.md` and ADR-057)*

---

## What changed in the last two commits (481d1d4 + 729b2af)

### Python changes
| What | Old | New |
|---|---|---|
| Home "Plots" wrapper | Was directly the groups `spv-panel` div | Now `#home_plots_body_accordion` (bslib accordion) |
| Data Preview title | `ui.tags.span("Data Preview", style="font-size:0.8em;...")` | `"📋 Data Preview"` (plain string) |
| Blueprint Work Area | Was tri-tab directly (no accordion) | Now `#blueprint_workarea_accordion` wrapping `#architect_internal_tabs` |
| Blueprint Glimpse/Plot cards | `class_="card shadow-sm mb-2"` | `class_="card mb-1"` (shadow removed) |
| Blueprint card btn style | `fw-semibold`, bg `#e9ecef`, padding `6px 12px` | `fw-bold`, bg `#f8f9fa`, padding `2px 10px`, `border-bottom: 1px solid #e9ecef` |

### CSS changes (§18 and §18b added, plus §14 and §9 tweaks)
| What | Effect |
|---|---|
| `.theater-container-main .accordion-button` global | All accordion headers in Home theater: `#f8f9fa` bg, 0.85rem/700 |
| `.theater-container-main .accordion-button:not(.collapsed)` | When expanded: `#ffffff` bg, no box-shadow, no border-bottom |
| `.theater-container-main .accordion-item` | `border: none` (removes Bootstrap grey outline) |
| `.wrangle-studio-container .accordion-button` | Same normalization for Blueprint accordions |
| `.wrangle-studio-container > .card` | `border: none`, `radius 8px`, `shadow` |
| `.wrangle-studio-container > .card .card-header` | `bg #f8f9fa`, `padding 0`, top radius |
| `.wrangle-studio-container .card-header .btn` | 0.85rem / fw-bold / #1a1a1a |
| `#home_plots_body_accordion .accordion-item` | `radius 8px`, `overflow hidden`, shadow |
| `#home_plots_body_accordion .accordion-body` | `padding: 0` (flush) |
| `#home_plots_body_accordion .navset-card-tab.card` | `border: none`, `radius 0`, no shadow |
| `#acc_home_data .accordion-item` | `radius 8px`, `overflow hidden`, shadow |
| `#acc_home_data .accordion-body` | `overflow visible`, `padding 4px` |
| `#blueprint_workarea_accordion .accordion-item` | `radius 8px`, `overflow hidden`, shadow |
| `#blueprint_workarea_accordion .accordion-body` | `padding: 0` (flush) |
| `#blueprint_tubemap_accordion .accordion-button` | Was blue `#345beb` — now `#f8f9fa` bg / `#1a1a1a` text |
| `#gallery_preview_accordion .accordion-item` | `border: none`, shadow, `radius 8px` |
| `#gallery_guidance_accordion .accordion-item` | Added `box-shadow: none` |

---

## Dead / Orphaned CSS rules

These selectors exist in `theme.css` but no longer match any element in the Python DOM:

| Selector | Location | Status |
|---|---|---|
| `#central_theater_tabs.card.navset-card-tab` | §2 (line 76), §9 (lines 285–286) | Dead — ID removed from Python |
| `#central_theater_tabs > .card-header .nav-tabs` | §5 (line 137) | Dead — same |

---

## Quick Reference — Colors currently in use

*(Same as `ui_panel_map.md` §Quick Reference — no color changes in these commits)*

| Role | Color | Selector(s) |
|---|---|---|
| Primary blue (buttons, active pills) | `#345beb` | `.btn-primary`, `.nav-pills .nav-link.active`, `#btn_apply` |
| Export / teal | `#10a395` | `#export_*`, `#btn_export`, etc. |
| Reset / amber | `#ffc107` | `#filter_reset`, `.recipe-pending-badge` |
| Sidebar accordion header | `#a0a0a0` | `#nav_sidebar .accordion-button` |
| Sidebar body bg | `#c0c0c0` | `--bslib-sidebar-bg` |
| Page background | `#d1d1d1` | `body` |
| Theater accordion header (collapsed) | `#f8f9fa` (light grey) | `.theater-container-main .accordion-button` |
| Theater accordion header (expanded) | `#ffffff` | `.theater-container-main .accordion-button:not(.collapsed)` |
| Audit node T2 | `#eef0fb` (blue tint) | `.audit-node-tier2` |
| Audit node T3 | `#e6f7f5` (teal tint) | `.audit-node-tier3` |
| TubeMap header (was blue, now) | `#f8f9fa` / `#1a1a1a` | `#blueprint_tubemap_accordion .accordion-button` |

---

## Typography scale (unchanged)

| Tier | Size | Weight | Used for |
|---|---|---|---|
| Primary | `0.85rem` | `700` | Accordion buttons, section headings, badges |
| Secondary | `0.80rem` | `400–600` | Body content, form labels |
| Micro | `0.65rem` | `400` | Helper text, dtype labels |
