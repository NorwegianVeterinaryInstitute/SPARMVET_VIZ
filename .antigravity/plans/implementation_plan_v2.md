# Implementation Plan v2: Dashboard Core & Plugin Validation
# Authority: @dasharch
# Date: 2026-03-21

## 🚩 THE RESTARTING POINT (2026-03-21)
Status:
- **Action Registry**: Operational but incomplete.
- **YAML Manifests**: Modular but containing commented-out (unimplemented) steps.
- **Test Data**: ST22 dummy data is ready in `./assets/test_data/`.

We are initiating the **'Decorator-First'** development cycle. 
This aligns our Python execution engine with the active YAML manifest logic verified in `./config/manifests/pipelines/`.

## 1. Goal
Transition from "Scaffolding" to "Functional Prototype" by implementing missing transformer logic and validating it via the modular Shiny frontend.

## 2. Technical Roadmap

### Phase A: 'Decorator-First' Implementation (DONE)
**Objective:** Confirm the decorator-based plugin system works.
1. [x] **Verify status of decorator-based plugin system.**
2. [x] **Implement missing decorator-based actions:**
    - Action: **Implement `@register_action("drop_duplicates")`**.
    - Action: **Implement `@register_action("summarize")`**.
    - Action: **Updated `ResFinder_wrangling.yaml`**.

### Phase B: Frontend Scaffolding (The "UI Heartbeat")
**Objective:** Replace empty files with a functional layout powered by the `./assets/` logic.
1. **Asset Integration:** Use `create_test_deployment.py` to bind synthetic ST22 dummy data to the Abromics manifest.
2. **UI Implementation (`app/src/ui.py`):**
    - Sidebar selection for dataset/manifest.
    - Tabs for **Pipeline Overview**, **Action Registry**, and **Raw Preview**.
3. **Server Implementation (`app/src/server.py`):**
    - Connect the `help_registry_server` module.
    - **Logic Linkage:** Call the `DataWrangler` upon manifest selection.

### Phase C: Dynamic Plot Factory (ACTIVE)
**Objective:** Convert the hardcoded `viz_factory` into a dynamic **Plotnine** plugin system matching the Transformer.
1. [x] **Implementation:** Created `@register_plot(factory_id)` decorator in `libs/viz_factory/src/registry.py` and refactored `base.py`.
2. [ ] **Refactor:** Replace Plotly Express placeholders with **Plotnine templates**.
3. [ ] **Data Handoff:** Prototype the Polars-to-Plotnine handoff.

### Phase D: Architectural Guardrails & Integration
1. **YAML Data Contract:** Pursue **YAML-ONLY** validation. Stop searching for JSON schemas.
2. **Polars Wrangler:** Mandatory use of **Polars LazyFrames** for all heavy lifting.
3. **Data Executor Recommendation:** Implement **`libs/utils/src/data_executor.py`** once the first wrangling logic and data schema are ready. This will center the `.collect()` logic for the Orchestrator.
4. **Module Dependency Management:** Each subdirectory in `libs/` must be an independent package with its own `pyproject.toml`. The root `.venv` installation must use `-e` (editable) flags to maintain modularity.
5. **Deferrals:** 
    - **API Mode B** (BioBlend/Galaxy) is deferred for the prototype.
    - **Plotly Interactivity** is deferred to Post-Prototype phase.

## 3. Verification Plan
- [ ] **Backend:** `test_wrangler.py` passes with implementation of `drop_duplicates` and `summarize`.
- [ ] **Visualization:** `viz_factory` returns a valid Plotnine object via registered decorators.
- [ ] **End-to-End:** Dashboard displays plots dynamically based on `analysis_groups` in the YAML.

## 4. Architectural Decisions (ADR)
- **Decision:** Use an explicit decorator pattern for BOTH Wrangling actions and Plotting factories.
- **Decision:** Prioritize Plotnine for the Presentation Layer to support Tidy Data consistency.
- **Decision:** Adopt 'Minimal Dataset' strategy to accelerate UI prototype delivery.
