# Tasks (SOLE SOURCE OF TRUTH)

# Workspace ID: SPARMVET_VIZ

# Last Updated: 2026-04-09 by @dasharch

## 🟢 Infrastructure & Recovery (COMPLETED)
>
> Status: COMPLETED. Detailed history moved to: [./.antigravity/tasks/archives/tasks_archive_infrastructure.md]

## 🟢 Layer 1/2 & Assembly Audit (COMPLETED)
>
> Status: COMPLETED. Detailed history moved to: [./.antigravity/tasks/archives/tasks_archive_infrastructure.md]

## 🟡 Backend & Decorator-First (COMPLETED)

### [DONE] Tier 1 (The Trunk): Relational Anchor (sink_parquet/scan_parquet)

- [x] Implement Tier 1 persistence logic. [DONE]
- [x] Integrate Short-Circuit logic. [DONE]
- [x] Verified via `debug_assembler.py`. [DONE]

### [DONE] Tier 2 (The Branch): Plot-Specific Filtered Subsets

- [x] Implement logic for dynamic branch materialization (shared summaries).
- [x] Verify Row-Count reduction for heatmaps and complex plots.
- [x] Implement Reverse Short-Circuit in `DataAssembler`.

### [DONE] Tier 3 (The Leaf): UI-driven Predicate Pushdown

- [x] Implement final filter application at the VizFactory collect gate. [DONE]

### 🛠️ Transformer Actions Status (ACTIVE COMPONENT)

- [x] **Phase 1: Structural Reshaping** (unpivot, explode, unnest, pivot) [DONE]
- [x] **Phase 2: Atomic Expressions** (cast, coalesce, label_if) [DONE]
- [x] **Phase 4: Performance & Summary Layer** (summarize) [CORE DONE]

## 🟢 Phase 9: Triple-Source AMR Integration (COMPLETED)
>
> Status: COMPLETED. Detailed history moved to: [./.antigravity/tasks/archives/tasks_archive_integration_qa.md]

## 🛡️ Library Integrity & QA (COMPLETED)
>
> Status: COMPLETED. Detailed history moved to: [./.antigravity/tasks/archives/tasks_archive_integration_qa.md]

## VIZ_FACTORY IMPLEMENTATION (COMPLETED)
>
> Status: COMPLETED. Detailed history moved to: [./.antigravity/tasks/archives/tasks_archive_viz_factory.md]

## 🔴 Frontend & Visualisation (ACTIVE)

- [x] **Replace viz_factory placeholders with Plotnine decorator logic** [DONE]
- [x] **Prototype Polars-to-Plotnine data handoff** (ADR-010) [DONE]
- [ ] **Reactive State Management:** Implement ADR-021 (Anchor vs. Filter) state hand-off between Shiny and Polars. The integration code bridging the Plot Factory and the Transformer is not fully tested/implemented in the frontend.
- [ ] **Shiny App/Server Basic Setup:** Populating `app/src/ui.py` and `app/src/server.py` with standard library imports. (Note: Four-Pillar registry help tooltips now part of Phase 11-C).

## 🟢 Phase 11-A: Pipeline Demo (COMPLETED)
>
> Status: COMPLETED. All core UI scaffolding, reactive mapping, and export logic documented.

## 🟢 Phase 11-C: UI Shell & Module Orchestration

- [x] **Persona-based Bootloader:** Implement `app/src/bootloader.py` to toggle features via `config/ui/templates/ui_persona_template.yaml`. [DONE]
- [x] **3-Zone Layout Shell:** Build Navigation (Left), Theater (Center), and Audit Stack (Right). [DONE]
- [x] **Aesthetic Lock:** Apply **#f8f9fa** Sidebars and Light Yellow/Green Tooltips. [DONE]
- [ ] **Side-by-Side Plot Logic:** Enable `layout_columns` comparison for Tier 2 (Reference) vs Tier 3 (Active) views.

## 🟢 Phase 11-D: Dynamic Discovery & Interaction

- [x] **Agnostic Integrity Coverage:** ACHIEVED 100% pass rate for Transformer and Viz Factory. [DONE]
- [x] **Dynamic Tab Engine:** Programmatically generate UI tabs from YAML manifest plot IDs. [DONE]
- [x] **Automated Column Filtering:** Generate top-level search/filter boxes for all detected Polars schema fields. [DONE]
- [ ] **Column Visibility Logic:** Implement picker to show/hide columns (Primary Keys locked to visible).
- [ ] **Theater Controls:** Implement Maximize/Minimize icons for plot and data table components.

## 🔴 Phase 11-E: Connectors, Persistence & Gallery (ACTIVE)

- [x] **Path Authority Manager:** Implement `config/connectors/` schema logic to direct system locations, decoupled completely from UI personas. [DONE]
- [ ] **External Ingestion UI:** Build Excel-to-TSV upload helper using existing `assets/scripts/`.
- [ ] **Join Preview Modal:** Implement Primary Key validation check before merging external data.
- [ ] **Ghost Manifest Persistence:** Implement automatic background save in Connector designated auto-save path (`tmp/ui/user/autosave`).
- [ ] **Gallery Engine:** Build browser pointing to Connector Location 5 with defaults (`assets/gallery_data/`).

## 🔴 Phase 11-F: Developer Studio & Expansion (ACTIVE)

- [ ] **WrangleStudio "Design Studio":** Implement visual chaining of Transformer nodes with "Hover-Help" documentation.
- [ ] **Synthetic Data GUI:** Build UI wrapper for `create_test_data.py`.
- [ ] **Outlier "Brush" Modal:** Connect plot selection events to a Tier 1 Anchor data lookup table.
- [ ] **Gallery Submission Engine:** Automate anonymization, README, and LICENSE generation for new recipes.

## 🟡 Integration & Strategy (ACTIVE)

- [ ] **Tier 3 Logic Toggle / Memory Array:** Implement a toggle switch to toggle the memory array of Tier 2 nodes inherited by Tier 3, rendering Raw vs Pre-Filled operations via Predicate Pushdown over Tier 1.
- [ ] **Recipe Pre-filling Architecture:** Ensure Tier 3 safely inherits and isolates Tier 2 logic nodes.
- [ ] **Session Summary Export:** Implement `.zip` bundler (Plot + Data + Audit Log + YAML).
- [ ] **Audit Node UI:** Apply color-coding to Sidebar nodes (Inherited vs. Active) and mandatory comments.

## ⚪ Deferred & Phase 3

- [ ] **Plotly Interactivity:** [DEFERRED] Move native interactivity to Post-Prototype phase.
- [ ] **Mode B API:** [DEFERRED] BioBlend/Galaxy dynamic connector.
- [ ] **Advanced Error Handling:** [DEFERRED] Malformed Data gatekeeping.

---

**NEXT FOCUS:** Phase 11-D (Dynamic Discovery & Interactions) and Phase 10-ADR-021 (Reactive State Management: Shiny/Polars hand-off). 🚀
