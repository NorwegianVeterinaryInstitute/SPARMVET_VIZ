---
trigger: always_on
---

# Verification & Testing Protocols (rules_verification_testing.md)

**Authority:** Governs the testing patterns, naming standardization, and the @verify operational gate.

## 1. Standardized Test Naming & Architecture

To ensure automated test suites are logically homogenous, all libraries MUST strictly adopt the following naming schema in their `tests/` directories:

- **Global Library Wrapper:** `libs/{lib}/tests/{lib}_integrity_suite.py`
  - *Purpose:* Programmatically query the registry, ingest all registered manifest-data combinations, execute them, and yield an automated `{lib}_integrity_report.txt`.
  - *Rule:* The global library wrapper script MUST be launched to ensure the entire system functions organically during broad refactorings.
- **Component Debuggers:** `libs/{lib}/tests/debug_{component_name}.py`
  - *Purpose:* Isolated testing for individual features, decorators, or core modules during active development.

## 2. CLI Mandate (argparse Authority)

Every executable Python script within `./libs/` test folders and `./assets/scripts/` MUST be controllable via the command line interface.

- **Rule:** Scripts must use the `argparse` standard library.
- **Rule:** Scripts must provide an explicit docstring mapped to the `--help` argument, describing exactly what the script accomplishes.
- **Rule:** Hardcoding paths in the execution blocks is strictly FORBIDDEN. All paths (data, manifest, output) must receive CLI arguments (with optional transparent defaults).

## 3. The @verify Protocol (Evidence Loop)

No task is considered [DONE] without passing the @verify gate, which creates a standalone proof-of-concept limit for operations.

1. **The Contract:** For a new function `[name]`, pre-define its dataset (`name_test.tsv`) and manifest (`name_manifest.yaml`).
2. **CLI Execution:** Execute test logic via the standard `argparse` CLI runner.
3. **Evidence Generation:**
   - Write out tables to `tmp/USER_debug_view.tsv` (via `.collect()`).
   - Save Plots to `tmp/USER_debug_plot.png`.
4. **Console Glimpse:** Output `df.glimpse()` to standard output.
5. **The Halt:** Agents MUST halt autonomous execution and declare: "Data/Plot ready in tmp/... Waiting for @verify."

## 4. Conflict Guardrails (Sync-or-Stop)

- **@sync**: If the Agent detects a discrepancy between the user's intent (chat) and the physical codebase structure, it must halt and ask to `@sync`.
- Project Rules and Architecture Decisions (ADRs) unconditionally overrule generic conversational prompts. Modify them only through Double-Confirmation with the user.
