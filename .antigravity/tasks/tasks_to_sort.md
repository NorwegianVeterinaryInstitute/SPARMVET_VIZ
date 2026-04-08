
Tasks (SOLE SOURCE OF TRUTH)

**Workspace ID:** SPARMVET\_VIZ **Last Updated:** 2026-04-08 by @dasharch (Architecture Sync)

🔴 Frontend & Visualisation (ACTIVE)
------------------------------------

* \[ \] **Reactive State Management:** Implement ADR-021 (Anchor vs. Filter) state hand-off between Shiny and Polars.
* \[ \] **Shiny App Implementation:** Populating `app/src/ui.py` and `app/src/server.py` with standard library imports.
* \[ \] **Four-Pillar Integration:** Link `app/modules/help_registry.py` into the dashboard sidebar.

### 🔴 Phase 11-C: UI Shell & Module Orchestration (ACTIVE)

* \[ \] **Persona-based Bootloader:** Implement `app/src/bootloader.py` to toggle features via `ui_config.yaml`.
* \[ \] **3-Zone Layout Shell:** Build Navigation (Left), Theater (Center), and Audit Stack (Right).
* \[ \] **Aesthetic Lock:** Apply **#f8f9fa** Sidebars and Light Yellow/Green Tooltips.
* \[ \] **Side-by-Side Plot Logic:** Enable `layout_columns` comparison for Tier 2 (Reference) vs Tier 3 (Active) views.

### 🔴 Phase 11-D: Dynamic Discovery & Interaction (ACTIVE)

* \[ \] **Dynamic Tab Engine:** Programmatically generate UI tabs from YAML manifest plot IDs.
* \[ \] **Automated Column Filtering:** Generate top-level search/filter boxes for all detected Polars schema fields.
* \[ \] **Column Visibility Logic:** Implement picker to show/hide columns (Primary Keys locked to visible).
* \[ \] **Theater Controls:** Implement Maximize/Minimize icons for plot and data table components.

### 🔴 Phase 11-E: Ingestion, Persistence & Gallery (ACTIVE)

* \[ \] **External Ingestion UI:** Build Excel-to-TSV upload helper using existing `assets/scripts/`.
* \[ \] **Join Preview Modal:** Implement Primary Key validation check before merging external data.
* \[ \] **Ghost Manifest Persistence:** Implement automatic background save (last 5 versions) in `tmp/sessions/`.
* \[ \] **Gallery Engine:** Build browser for `assets/gallery_data/` with mandatory license/credit display.

### 🔴 Phase 11-F: Developer Studio & Expansion (ACTIVE)

* \[ \] **WrangleStudio "Design Studio":** Implement visual chaining of Transformer nodes with "Hover-Help" documentation.
* \[ \] **Synthetic Data GUI:** Build UI wrapper for `create_test_data.py`.
* \[ \] **Outlier "Brush" Modal:** Connect plot selection events to a Tier 1 Anchor data lookup table.
* \[ \] **Gallery Submission Engine:** Automate anonymization, README, and LICENSE generation for new recipes.

* * *

🟡 Integration & Strategy (ACTIVE)
----------------------------------

* \[ \] **Recipe Pre-filling:** Ensure Tier 3 inherits Tier 2 logic nodes as editable components (Inheritance Logic).
* \[ \] **Session Summary Export:** Implement `.zip` bundler (Plot + Data + Audit Log + YAML).
* \[ \] **Audit Node UI:** Apply color-coding to Sidebar nodes (Inherited vs. Active) and mandatory comments.

⚪ Deferred & Phase 3
--------------------

* \[ \] **Plotly Interactivity:** \[DEFERRED\] Move native interactivity to Post-Prototype phase.
* \[ \] **Mode B API:** \[DEFERRED\] BioBlend/Galaxy dynamic connector.
* \[ \] **Advanced Error Handling:** \[DEFERRED\] Malformed Data gatekeeping.
