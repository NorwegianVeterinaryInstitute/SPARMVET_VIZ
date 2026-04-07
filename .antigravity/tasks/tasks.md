# Tasks (SOLE SOURCE OF TRUTH)

# Workspace ID: SPARMVET_VIZ

# Last Updated: 2026-04-07 by @dasharch

## 🟢 Infrastructure & Recovery (COMPLETED)
>
> Status: COMPLETED. Detailed history moved to: [./.antigravity/tasks/archives/tasks_archive_infrastructure.md]

## 🟢 Layer 1/2 & Assembly Audit (COMPLETED)
>
> Status: COMPLETED. Detailed history moved to: [./.antigravity/tasks/archives/tasks_archive_infrastructure.md]
>
## 🟡 Backend & Decorator-First (ACTIVE FOCUS)

### [DONE] Tier 1 (The Trunk): Relational Anchor (sink_parquet/scan_parquet)

- [x] Implement Tier 1 persistence logic in `persistence/anchor.py`.
- [x] Integrate Short-Circuit logic in `DataAssembler`.
- [x] Verified via `debug_assembler.py`.

### [ACTIVE] Tier 2 (The Branch): Plot-Specific Anchors (Shared filtered subsets)

- [ ] Implement logic for dynamic branch materialization (shared summaries).
- [ ] Verify Row-Count reduction for heatmaps and complex plots.

### [PLANNED] Tier 3 (The Leaf): UI-driven Predicate Pushdown

- [ ] Implement final filter application at the VizFactory collect gate.

### 🛠️ Transformer Actions Status

- [x] **Phase 1: Structural Reshaping** (unpivot, explode, unnest, pivot) [DONE]
- [ ] **Phase 2: Atomic Expressions** (cast, coalesce, label_if) [PLANNED]
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
- [ ] **Reactive State Management** (ADR-021)
- [ ] **Shiny App Implementation** (`app/src/ui.py`, `app/src/server.py`)
- [ ] **Four-Pillar Integration** (`app/modules/help_registry.py`)

## 📘 Documentation Recovery & Phase 11 Sync (COMPLETED)
>
> Status: COMPLETED. Detailed history moved to: [./.antigravity/tasks/archives/tasks_archive_viz_factory.md] and [./.antigravity/tasks/archives/tasks_archive_integration_qa.md]

## ⚪ Deferred & Phase 3

- [ ] Plotly Interactivity, Mode B API, Advanced Error Handling.

---

**NEXT FOCUS:** Phase 10-T2 (Tier 2 Branch materialization). 🚀
