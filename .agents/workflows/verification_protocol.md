---
description: Instructions to trigger manual verification by the user
---

# Workflow: Manual Data Verification (@verify)

## 1. Trigger
Triggered for any **Polars** transformation or **Plotnine** factory implementation.

## 2. Mandatory Steps (The "Evidence" Loop)
1. **Implementation:** Write the logic in the source files.
2. **Evidence Generation:**
   - **For Data:** Materialize LazyFrame to `tmp/debug_view.csv` (via `.collect()`).
   - **For Plots:** Save the Plotnine object to `tmp/debug_plot.png`.
3. **Console Glimpse:** Print the first 10 rows and schema to the terminal using `df.glimpse()`.
4. **The Gate (HALT):**
   - The Agent MUST stop  all execution and provide the appropriate message:
     - **Data Case:** "Data is ready in `tmp/debug_view.csv`. Use Excel Viewer to verify. Waiting for @verify."
     - **Plot Case:** "Plot is ready in `tmp/debug_plot.png`. Please open the image to verify. Waiting for @verify."

## 3. Completion
No task is marked [DONE] in `./.antigravity/tasks/tasks.md` without the @verify confirmation.