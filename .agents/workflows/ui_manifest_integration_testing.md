---
description: The Master Gate for UI and Manifest Integration Testing
---
# 🖥️ UI Manifest Integration Testing (The Master Gate)

## Authority

This workflow acts as the final overarching **Phase-Gate** ensuring visual integration does not crash due to backend failures.

## Requirement (Headless-First)

Execution of any UI integration tests (e.g. via `app/src/main.py` or Shiny live previews) is **STRICTLY PROHIBITED** until the required headless workflows have successfully cleared their Proof of Life audits:

- ✅ *Ingestion Audit Passed*
- ✅ *Transformer/Assembler Audit Passed*
- ✅ *Viz Factory Audit Passed*

## Validation Steps

1. Verify that all dependencies have generated their verified Headless test artifacts inside `tmp/Manifest_test/{manifest_basename}/`.
2. Confirm the `@verify` of the Headless testing loops has been signed off by the User.
3. Launch the UI Server and interact. Verify that no raw data errors breach through the reactive boundaries.
