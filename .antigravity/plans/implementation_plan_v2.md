# Implementation Plan v2: Dashboard Core & Plugin Validation
# Authority: @dasharch
# Date: 2026-03-21

## 1. Goal
Transition from "Scaffolding" to "Functional Prototype" by implementing the Shiny frontend and validating the backend plugin architecture.

## 2. Technical Roadmap

### Phase A: Architecture Validation
**Objective:** Confirm the decorator-based plugin system works as intended in the current environment.
1. **Action:** Execute `python libs/transformer/tests/test_wrangler.py`.
2. **Action:** If tests fail due to import paths (common in local envs), fix path resolution in `libs/transformer/src/registry.py`.
3. **Artifact:** Ensure `actions/` are correctly registered in `AVAILABLE_WRANGLING_ACTIONS`.

### Phase B: Frontend Scaffolding (The "UI Heartbeat")
**Objective:** Replace empty files with a functional layout.
1. **UI Implementation (`app/src/ui.py`):**
    - Implement a `sidebar_panel` for dataset/manifest selection.
    - Setup `nav_panel` tabs for:
        - **Pipeline Overview** (Visualization).
        - **Action Registry** (Using the `help_registry` module).
        - **Raw Preview** (Initial Polars/Pandas view).
2. **Server Implementation (`app/src/server.py`):**
    - Connect the `help_registry_server` module.
    - Implement basic reactive file loading for the manifest selection.

### Phase C: Architectural Guardrails & Integration
**Objective:** Align the project pillars and enforce the "Walking Skeleton" scope.
1. **JSON Schema (Pillar 4):**
    - **Status:** In-Progress (Pending Code Audit).
    - **Action:** Perform a deep scan of `./config/schemas/` (if any exist) to identify current validation coverage.
2. **Connector Layer:** 
    - **Decision:** Formally **DEFER** 'API-driven Mode B' (BioBlend/Galaxy).
    - **Priority:** Focus exclusively on 'Manual Upload' for the prototype phase.
3. **Ingestion Layer:**
    - **Decision:** Remove 'Malformed Data Handling' from immediate scope. 
    - **Strategy:** Implement a **'Minimal Dataset'** strategy—assume input data follows the contract for now to accelerate UI progress.

## 3. Verification Plan
- [ ] **Backend:** `test_wrangler.py` passes all assertions.
- [ ] **Frontend:** `shiny run app.py` launches a visible dashboard with indexed actions.
- [ ] **Schema Audit:** Complete scan of local `.json` schema files.

## 4. Architectural Decisions (ADR)
- **Decision:** Use an explicit decorator pattern (already implemented) to avoid "magic" imports.
- **Decision:** Shiny UI will remain modularized in `app/src/ui.py` to support future visualization complexity.
- **Decision:** Defer automated API connections to focus on the "Walking Skeleton" data flow.
