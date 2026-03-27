# Implementation Plan Master: Dashboard Core & Plugin Validation
# Authority: @dasharch
# Source of Truth for SPARMVET_VIZ Architecture

## 1. Overview & Vision
Transition from "Scaffolding" to "Functional Prototype" by implementing missing transformer logic and validating it via the modular Shiny frontend. We utilize a **'Decorator-First'** development cycle to align the Python execution engine with the active YAML manifest logic verified in `./config/manifests/pipelines/`.

## 2. Architectural Principles
- **Decorator-First:** Explicit decorator patterns for both Wrangling actions (`@register_action`) and Plotting factories (`@register_plot`).
- **YAML Data Contract:** Pursue **YAML-ONLY** validation. Phase out JSON schema dependencies for the core manifest logic.
- **Polars-First:** Mandatory use of **Polars LazyFrames** for all heavy lifting. Materialize only at the Presentation or Export layers.
- **Tidy Data Consistency:** Use **Plotnine** for the Presentation Layer to ensure seamless handoff from Polars-transformed dataframes.

## 3. Environment & Modular Standards
- **Root .venv:** All execution MUST occur within the root `.venv/` directory.
- **Modular package architecture:** 
    - Each subdirectory in `libs/` (e.g., `libs/transformer`, `libs/viz_factory`) MUST be an independent package with its own `pyproject.toml`.
    - Installation in the root `.venv` MUST use the `-e` (editable) flag to maintain modularity and live-syncing of code changes.
- **CLI-argparse for Testing:** Every library in `libs/` must include a CLI-compatible test script. Hardcoded paths inside test logic are forbidden. Use `argparse` to handle data inputs (TSV), configuration manifests (YAML), and output destinations.

## 4. Technical Roadmap

### Phase A: 'Decorator-First' Logic (DONE)
- [x] Verify status of decorator-based plugin system.
- [x] Implement missing decorator-based actions (drop_duplicates, summarize).
- [x] Update ResFinder_wrangling.yaml.

### Phase B: Dynamic Plot Factory (ACTIVE)
- [x] Implement `@register_plot(factory_id)` decorator in `libs/viz_factory/src/registry.py`.
- [x] Refactor `base.py` to replace Plotly placeholders with Plotnine templates.
- [ ] Prototype Polars-to-Plotnine handoff.

### Phase 3: Atomic Layer Optimization (DONE)
- [x] **Decorator Expansion:** Implement `regex_extract`, `drop_columns`, `round_numeric`, and `filter_range`.
- [x] **Contract Verification:** Ensure the `DataWrangler` remains atomic (one input -> one cleaned output).
- [x] **Universal Runner Callability:** Confirm `test_wrangler.py` can be imported as a library by the Orchestrator.
- [x] **Lazy Processing Audit:** Ensure atomic actions do not trigger premature Polars collection.

### Phase 4: The Assembly Factory (DONE)
- [x] **DataAssembler Core:** Implement Layer 2 orchestrator script.
- [x] **Multi-Source Loop:** Call the Wrangler for all datasets defined in the manifest.
- [x] **Cross-Dataset Joins:** Execute Polars `.join()` logic using manifest-defined `join_on`.
- [x] **Final Stage Wrangling:** Support a global wrangling pass across the joined LazyFrame.
- [x] **Relational Decorators:** Registered `join` and `join_filter` in the unified registry.

### Phase 5: Frontend Scaffolding (UI Heartbeat)
- [ ] **Asset Integration:** Use `create_test_deployment.py` to bind synthetic ST22 dummy data to the Abromics manifest.
- [ ] **UI Implementation (`app/src/ui.py`):** Sidebar for dataset/manifest selection. Tabs for Pipeline Overview, Action Registry, and Raw Preview.
- [ ] **Server Implementation (`app/src/server.py`):** Connect `help_registry_server`; call `DataWrangler` upon manifest selection.

### Phase 6: Architectural Guardrails & Integration
- [ ] Implement **`libs/utils/src/data_executor.py`** to center the `.collect()` logic for the Orchestrator.
- [ ] Finalize YAML-only validation logic.
- [ ] Implement responsive UI adjustments for premium branding.

## 5. Verification Protocol v1.6 (@verify Gate)
This protocol is MANDATORY for any Polars transformation (Wrangling) or Plotnine factory implementation.

### 5.1. The Contract (Pre-Implementation)
Before writing core logic, the Agent MUST:
1. **Generate Test Data:** Create a specific subset TSV in `./libs/transformer/tests/data/{{ACTION_NAME}}_test.tsv`.
2. **Draft Test Manifest:** Create a minimal YAML file `./libs/transformer/tests/data/{{ACTION_NAME}}_manifest.yaml` describing the expected transformation.
3. **Contract Halt:** STOP and wait for the user to @confirm_contract in the IDE.

### 5.2. Evidence Loop (Mandatory Steps)
1. **Implementation:** Write the logic in the source files.
2. **CLI-First Testing:** 
    - Test scripts (e.g., `test_wrangler.py`) MUST use `argparse`.
    - Execution Command: `python test_script.py --data path/to/data.tsv --manifest path/to/config.yaml`.
3. **Evidence Generation:**
    - **Data:** Materialize LazyFrame to `tmp/{{ACTION_NAME}}_debug_view.tsv` and `tmp/USER_debug_view.tsv`.
    - **Plots:** Save Plotnine object to `tmp/{{PLOT_NAME}}_debug_plot.png` and `tmp/USER_debug_plot.png`.
4. **Console Glimpse:** Print the first 10 rows and schema using `df.glimpse()`.
5. **The @verify Gate (HALT):**
    - **Data Case:** Provide message: "Data is ready in `tmp/{{ACTION_NAME}}_debug_view.tsv`. Use Excel Viewer to verify. Waiting for @verify."
    - **Plot Case:** Provide message: "Plot is ready in `tmp/{{PLOT_NAME}}_debug_plot.png`. Please open image to verify. Waiting for @verify."

## 6. Architectural Decisions (ADR)
- **ADR-001:** Explicit decorator pattern for Wrangling actions and Plotting factories.
- **ADR-002:** Prioritize Plotnine for Tidy Data consistency.
- **ADR-003:** 'Minimal Dataset' strategy to accelerate UI prototype delivery.
- **ADR-004:** YAML-ONLY validation (Phase out JSON schemas).
