# Tasks (SOLE SOURCE OF TRUTH)

# Workspace ID: SPARMVET_VIZ

# Last Updated: 2026-04-07 by @dasharch

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
- [ ] **Reactive State Management:** Implement ADR-021 (Anchor vs. Filter) state hand-off.
- [ ] **Shiny App Implementation:** Populating `app/src/ui.py` and `app/src/server.py`.
- [ ] **Four-Pillar Integration:** Link `app/modules/help_registry.py` into dashboard.

### [ACTIVE] UI & Gallery Implementation (Phase 11-C/D)

- [ ] **Implement ADR-027 Layout**: Build side-by-side plot views in `VizViewer`.
- [ ] **Connect Library Registries**: Pull action/plot documentation into UI help tooltips.
- [ ] **Recipe Pre-filling**: Implement inheritance of Tier 2 steps into the Tier 3 sidebar.
- [ ] **Gallery Structure**: Populate `assets/gallery_data/` with credit/license templates.
- [ ] **Exclusion Logic**: Connect "Brush" interaction to Tier 1 Anchor data lookup.

## 🟢 Phase 11-A: Pipeline Demo (COMPLETED)
>
> Status: COMPLETED. All core UI scaffolding, reactive mapping, and export logic documented.

## 🔴 Phase 11-B: Developer Studio & Expansion (ACTIVE)

- [ ] **UI-driven Branching**: Implement "New Branch" from Tier 1 Anchor.
- [ ] **Manifest Helper**: Build the "Design Studio" UI for drag-and-drop wrangling chain construction.
- [ ] **Pre-Flight Validator**: Implement the "Compatibility Dashboard" for data contracts.
- [ ] **Inspiration Gallery**: Integrate the component sandbox and example plot gallery.
- [ ] **State Recovery**: Implement the "Restore from Ghost" logic (tmp/last_state.yaml).

## Integration & Strategy (ACTIVE)

- [ ] We need to check if implementation of the integration (link) beween plot factoryt and the Transformer is done.
- [ ] User need to decide on the frontend implementation -> notes to review in 2026-04-02 daily subdirectory
- [ ] [TASK BLOCKER] USER WANTS YOU TO STOP YOUR ACTIVITIES HERE

## 📘 Documentation Recovery & Phase 11 Sync (COMPLETED)
>
> Status: COMPLETED. Detailed history moved to: [./.antigravity/tasks/archives/tasks_archive_viz_factory.md] and [./.antigravity/tasks/archives/tasks_archive_integration_qa.md]

## ⚪ Deferred & Phase 3

- [ ] **Plotly Interactivity:** [DEFERRED] Move native interactivity to Post-Prototype phase.
- [ ] **Mode B API:** [DEFERRED] BioBlend/Galaxy dynamic connector.
- [ ] **Advanced Error Handling:** [DEFERRED] Malformed Data gatekeeping.

---

**NEXT FOCUS:** Phase 10-ADR-021 (Reactive State Management: Shiny/Polars hand-off). 🚀
