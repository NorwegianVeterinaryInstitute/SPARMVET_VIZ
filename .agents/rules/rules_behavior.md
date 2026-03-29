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
- **Verification Required (@verify):** If the Agent accepts disk contents as truth, it must ask to `@verify`.
- **Precedence:** Project Rules and ADRs always take precedence over chat prompts.

## 3. Rule Modification (The Double-Confirmation Protocol)
To prevent architectural drift:
1. **Halt:** Explicitly state: "This request modifies Rule [X]. Is this really your intent?"
2. **Confirmation:** Wait for an second, explicit user confirmation.
3. **Refactoring:** Identify and refactor all components following the old pattern immediately.
4. **Re-testing:** All refactored components must be re-tested in the same session.

## 4. Operational Directives (Mirror Protocol)
- **State Mirroring:** Update `implementation_plan_master.md` and `tasks.md` mirrored in `./.antigravity/`.
- **No Ghost State:** Technical decisions are only real when mirrored into architecture records.
- **Operational Mode:** Standby for single-task prompts; no autonomous execution; mandatory halt for @verify.