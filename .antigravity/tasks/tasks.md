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
>
> Status: COMPLETED (Phases A-B, 3-5). Detailed history moved to: [./.antigravity/tasks/archives/tasks_archive_infrastructure.md]

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
>
> Status: CORE UI SCAFFOLDING COMPLETED (Phases 8, 11-A/C/D).

- [x] **Reactive State Management:** Implement ADR-021 (Anchor vs. Filter). [DONE]
- [x] **Shiny Shell Setup:** (3-Zone Navigation). [DONE]

## 🔴 Phase 11-E: Connectors, Persistence & Gallery (ACTIVE)
>
> Status: CORE INFRASTRUCTURE COMPLETED (Path Authority, Ghost Save).
> Detailed history of completed items moved to: [./.antigravity/tasks/archives/tasks_archive_infrastructure.md]

- [ ] **Gallery Engine:** Build UI browser pointing to Location 5 (`assets/gallery_data/`).
- [ ] **Join Preview Modal:** Implement PK validation check before merging external data.

## 🔴 Phase 11-F: Developer Studio & Expansion (ACTIVE)
>
> Status: CORE LOGIC COMPLETED (Agnostic Refactor, WrangleStack, DevStudio GUI).
> Detailed history of completed items moved to: [./.antigravity/tasks/archives/tasks_archive_infrastructure.md]

- [ ] **Outlier "Brush" Modal:** [ADR-030] Map plot selection to Tier 1 Anchor data lookup.
- [ ] **Gallery Submission Engine:** Automate anonymization, README, and LICENSE generation.

## 🟡 Integration & Strategy (ACTIVE)

- [x] **Audit Node UI Layout:** Color-coded Sidebar nodes (Inherited vs. Active). [DONE]
- [ ] **Audit Node Trace Logic:** Implement mandatory comments and hover-help logic.
- [ ] **Triple-Tier Grid Toggle:** [Phase 12-B] UI switch for side-by-side comparison (Tier 1 vs 2 vs 3).
- [ ] **Session Summary Export:** Implement `.zip` bundler (Plot + Data + Audit Log + YAML).

## 🟣 Phase 12: Advanced Analytics & Universal Schema (ACTIVE)

### Phase 12-A: Universal Schema & Agnostic Finalization

- [ ] **Universal Schema Discovery**: Refactor all UI pickers to derive choices from active Polars LazyFrame schema.
- [ ] **Project-Agnostic Nomenclature**: Finalize transition from "Species/Sample" to "Project/Record".
- [ ] **Dynamic Tab Generation**: Manifest-driven tab population for analysis groups.

## ⚪ Deferred & Phase 3

- [ ] **Plotly Interactivity:** [DEFERRED] move native interactivity to Post-Prototype phase.
- [ ] **Mode B API:** [DEFERRED] BioBlend/Galaxy dynamic connector.
- [ ] **Advanced Error Handling:** [DEFERRED] Malformed Data gatekeeping.

---

**NEXT FOCUS:** Phase 12-A (Universal Schema & Agnostic Finalization) and Phase 11-E (Gallery Engine). 🚀
