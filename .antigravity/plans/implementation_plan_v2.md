# Implementation Plan v2: Dashboard Core & Plugin Validation
# Authority: @dasharch
# Date: 2026-03-21

## 🚩 THE RESTARTING POINT (2026-03-21)
tatus:
- **Action Registry**: Operational but incomplete.
- **YAML Manifests**: Modular but containing commented-out (unimplemented) steps.
- **Test Data**: ST22 dummy data is ready in `./assets/test_data/`.

We are initiating the **'Decorator-First'** development cycle. 
This aligns our Python execution engine with the active YAML manifest logic verified in `./config/manifests/pipelines/`.

## 1. Goal
Transition from "Scaffolding" to "Functional Prototype" by implementing missing transformer logic and validating it via the modular Shiny frontend.

## 2. Technical Roadmap

### Phase A: 'Decorator-First' Implementation (ACTIVE)

**Objective:** Confirm the decorator-based plugin system works using the fake dataset in `./assets/test_data/`.

Verify status of decorator-based plugin system:
1. **Action:** Execute `python libs/transformer/tests/test_wrangler.py` using synthetic ResFinder data.
2. **Action:** Validate that `@register_action("derive_categories")` correctly processes the `ResFinder_wrangling.yaml` logic found in the active pipeline.
3. **Artifact:** Ensure `actions/` are correctly registered and accessible to the `DataWrangler`.

Implement missing decorator-based actions:
1. **Action:** Implement `@register_action("drop_duplicates")` in `libs/transformer/src/actions/core/`.
2. **Action:** Implement `@register_action("summarize")` in `libs/transformer/src/actions/core/`.
3. **Action:** Uncomment these steps in `config/manifests/pipelines/1_Abromics_general_pipeline/ResFinder_wrangling.yaml`.
4. **Validation:** Execute `python libs/transformer/tests/test_wrangler.py` using synthetic ResFinder data.

### Phase B: Frontend Scaffolding (The "UI Heartbeat")
**Objective:** Replace empty files with a functional layout powered by the `./assets/` logic.
1. **Asset Integration:** Use `create_test_deployment.py` to bind synthetic ST22 dummy data to the Abromics manifest.
2. **UI Implementation (`app/src/ui.py`):**
    - Implement a `sidebar_panel` for dataset/manifest selection.
    - Setup `nav_panel` tabs for:
        - **Pipeline Overview** (Visualization).
        - **Action Registry** (Using the `help_registry` module to show implemented decorators).
        - **Raw Preview** (Initial Polars/Pandas view).
3. **Server Implementation (`app/src/server.py`):**
    - Connect the `help_registry_server` module.
    - Implement basic reactive file loading for the manifest selection.
    - **Logic Linkage:** Ensure the `DataWrangler` is called upon manifest selection.

### Phase C: Architectural Guardrails & Integration
**Objective:** Align the project pillars and enforce the "Walking Skeleton" scope.
1. **YAML Data Contract (Pillar 4):**
    - **Status:** EXCLUSIVE. All data schemas and wrangling are managed via **YAML** manifests.
2. **Connector Layer:** 
    - **Decision:** Formally **DEFER** 'API-driven Mode B'. Focus exclusively on 'Manual/Auto-Load' from `./assets/test_data/`.
3. **Ingestion Layer:**
    - **Decision:** Remove 'Malformed Data Handling' from immediate scope. 
    - **Strategy:** Implement a **'Minimal Dataset'** strategy—assume input data follows the YAML contract for now.

## 3. Verification Plan
- [ ] **Backend:** `test_wrangler.py` passes with implementation of `drop_duplicates` and `summarize`.
- [ ] **Frontend:** `shiny run app.py` launches a visible dashboard with indexed actions and synthetic ResFinder data.
- [ ] **Cleanup:** Remove outdated `./config/manifests/species/` and `templates/` folders.

## 4. Architectural Decisions (ADR)
- **Decision:** Use an explicit decorator pattern to avoid "magic" imports.
- **Decision:** Defer automated API connections to focus on the synthetic "Walking Skeleton" data flow.
- **Decision:** Adopt 'Minimal Dataset' strategy to accelerate UI prototype delivery.
