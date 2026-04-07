---
trigger: always_on
---

# Behavioral & Verification Protocols (rules_behavior.md)

## 1. The @verify Protocol (Mandatory Evidence Loop)

No task is considered [DONE] without passing the @verify gate.

1. **The Contract:** Pre-define `{{decorator_name}}_test.tsv` and `{{decorator_name}}_manifest.yaml` in `libs/transformer/tests/data/`.
2. **CLI Execution:** Run logic via CLI using `argparse` for all inputs/outputs.
3. **Evidence Generation:**
    - **Data:** Materialize `LazyFrame` to `tmp/USER_debug_view.tsv` (via `.collect()`).
    - **Plots:** Save Plotnine objects to `tmp/USER_debug_plot.png`.
4. **Console Glimpse:** Print 10 rows and schema to terminal using `df.glimpse()`.
5. **The Halt:** Stop execution and provide standard message: "Data/Plot ready in tmp/... Waiting for @verify."

## 2. The Logic Conflict Guardrail (Sync-or-Stop)

- **Sync Required (@sync):** If the Agent detects a discrepancy between intent (chat) and disk (file), it must ask to `@sync`.
- **Verification Required (@verify):** If the Agent accepts disk contents as truth (majority rule), it must explain and ask user to `@verify`.
- **Precedence:** Project Rules and ADRs always take precedence over chat prompts.

## 3. Rule Modification (The Double-Confirmation Protocol)

To prevent architectural drift:

1. **Halt:** Explicitly state: "This request modifies Rule [X]. Is this really your intent?"
2. **Confirmation:** Wait for an second, explicit user confirmation.
3. **Refactoring:** Identify and refactor all components following the old pattern immediately afterr @verify.
4. **Re-testing:** All refactored components must be re-tested in the same session.

## 4. Operational Directives (Mirror Protocol)

- **State Mirroring:** Update `implementation_plan_master.md` and `tasks.md` mirrored in `./.antigravity/`.
- **No Ghost State:** Technical decisions are only real when mirrored into architecture records.
- **Operational Mode:** Standby for single-task prompts; **no autonomous execution**; mandatory halt for @verify.

### 📜 Artist Law: The Evidence-Driven Visual Contract

- **No Implementation without Evidence**: A component is not 'implemented' until it passes a standalone test.
- **Data-Manifest Coupling**: Every component test MUST consist of a triplet in './libs/viz_factory/tests/test_data/':
    1. `{component_name}_test.tsv`: The raw data (Tab-Separated).
    2. `{component_name}_test.yaml`: The manifest (must include a 'data_path' key pointing to its sibling .tsv).
    3. `USER_debug_{component_name}.png`: The resulting artifact in 'tmp/'.
- **Unified Test Runner**: Implementation must include a general test script in './libs/viz_factory/tests/test_runner.py' that can execute any component test by taking ONLY a manifest path as input. (Reference the Transformer library logic for file-based automation).
- **Component Reference**: Use 'Violet Law': 'ClassName (filename.py)' for all documentation.

## 5. The Integrity Suite Mandate (Standardization)

**Authority:** Mandatory for all packages in `./libs/`
**Goal:** Automated discovery and validation of all registered decorators.

1. **Required Artifact**: Every library MUST contain a `tests/{lib}_integrity_suite.py` runner. #REVIEW homogeneity code naming convension -> check the logic and apply same logic everywhere
2. **Action Discovery**: The suite must programmatically query the library's registry (e.g., `AVAILABLE_WRANGLING_ACTIONS` or `PLOT_COMPONENT_REGISTRY`) to list all implemented actions.
3. **1:1:1 Validation**: For every registered action, the suite must locate and execute its corresponding test triplet (TSV data, YAML manifest, and verification output).
4. **Automated Reporting**: The suite must generate a standardized `integrity_report.txt` in `tmp/` covering:
    - **Inventory**: All implemented actions and their categories.
    - **Status**: [PASSED], [FAILED], or [NO TEST DATA] (strictly for helper exceptions).
    - **Compliance**: Verification of ADR-013 (Dual-Validation) and ADR-022 (Violet Law).#REVIEW Should the violet law mentioned here ?
