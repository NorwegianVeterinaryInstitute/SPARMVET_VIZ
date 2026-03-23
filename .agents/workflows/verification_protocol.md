---
description: Instructions to trigger manual verification by the user
---

# Workflow: Manual Data Verification (@verify)

## 1. Trigger
Triggered for any **Polars** transformation (Wrangling) or **Plotnine** factory implementation.

## 2. Pre-Implementation (The Contract)
Before writing any core logic, the Agent MUST:
1. **Generate Test Data:** Create a specific subset CSV in `./libs/transformer/tests/data/{{ACTION_NAME}}_test.csv`.
2. **Draft Test Manifest:** Create a minimal YAML file `./libs/transformer/tests/data/{{ACTION_NAME}}_manifest.yaml` describing the expected transformation.
3. **Contract Halt:** STOP and wait for the user to @confirm_contract in the IDE.

## 3. Mandatory Steps (The "Evidence" Loop)
1. **Implementation:** Write the logic in the source files (Python/Polars/Plotnine).
2. **Evidence Generation:**
   - **For Data:** - Materialize LazyFrame to `tmp/{{ACTION_NAME}}_debug_view.csv`.
     - Materialize LazyFrame to `tmp/USER_debug_view.csv` (via `.collect()`)..
   - **For Plots:** - Save the Plotnine object to `tmp/{{PLOT_NAME}}_debug_plot.png`.
     - Save the Plotnine object to `tmp/USER_debug_plot.png`.
3. **Console Glimpse:** Print the first 10 rows and schema to the terminal using `df.glimpse()`.
4. **The Gate (HALT):**
   - The Agent MUST stop all execution and provide the appropriate message:
     - **Data Case:** "Data is ready in `tmp/{{ACTION_NAME}}_debug_view.csv` and `tmp/USER_debug_view.csv`. Use Excel Viewer to verify. Waiting for @verify."
     - **Plot Case:** "Plot is ready in `tmp/{{PLOT_NAME}}_debug_plot.png` and `tmp/USER_debug_plot.png`. Please open the image to verify. Waiting for @verify."

## 4. Completion
No task is marked [DONE] in `./.antigravity/tasks/tasks.md` without the @verify confirmation.
