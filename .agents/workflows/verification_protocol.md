---
description: Instructions to trigger manual verification by the user
---

# Workflow: Manual Data Verification (@verify)

## 1. Logic Authority
This workflow is now centrally managed in the modular rule system.

**See**: [rules_behavior.md](../rules/rules_behavior.md)

## 2. Trigger
Triggered for any **Polars** transformation (Wrangling) or **Plotnine** factory implementation.

## 3. The Evidence Loop
All implementation work MUST follow the **Evidence Loop** defined in [rules_behavior.md](../rules/rules_behavior.md#1-the-verify-protocol-mandatory-evidence-loop):
1.  **Contract Pre-definition** (Test data & manifest).
2.  **CLI Execution** via `argparse`.
3.  **Materialization** to `tmp/`.
4.  **Terminal Glimpse** via `.glimpse()`.
5.  **Mandatory Halt** for `@verify`.

## 4. Completion
No task is marked [DONE] in `./.antigravity/tasks/tasks.md` without the @verify confirmation.