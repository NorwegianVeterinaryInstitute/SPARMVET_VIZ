---
trigger: always_on
---

# Verification & Testing Protocols (rules_verification_testing.md)

**Authority:** Governs the testing patterns, naming standardization, and the @verify operational gate.

## 1. Standardized Test Naming & Architecture

To ensure automated test suites are logically homogenous, all libraries MUST strictly adopt the following naming schema in their `tests/` directories:

- **Component Debuggers (The Engines):** `libs/{lib}/tests/debug_{component}.py`
  - *Purpose:* Specialized runners for isolated logic (e.g., `debug_wrangler.py` for Layer 1 decorators).
- **Global Library Wrapper (The Orchestrator):** `libs/{lib}/tests/{lib}_integrity_suite.py`
  - *Purpose:* A high-level runner that programmatically discovers actions and dispatches them to the appropriate 'Engine' for verification.
  - *Command:* The Orchestrator MUST use the Engines to perform the actual execution; it does not contain the testing logic itself.

## 2. CLI Mandate (argparse Authority)

Every executable Python script within `./libs/` test folders and `./assets/scripts/` MUST be controllable via the command line interface.

- **Rule:** Scripts must use the `argparse` standard library.
- **Rule:** Scripts must provide an explicit docstring mapped to the `--help` argument, describing exactly what the script accomplishes.
- **Rule:** Hardcoding paths in the execution blocks is strictly FORBIDDEN. All paths (data, manifest, output) must receive CLI arguments (with optional transparent defaults).

## 3. The @verify Protocol & Phase-Gating (Evidence Loop)

No task is considered [DONE] without passing the @verify gate, which creates a standalone proof-of-concept limit for operations.
**Phase-Gating Mandate:** UI testing (`app/src/main.py`) is STRICTLY PROHIBITED until the corresponding Headless Audit has passed.

1. **The Contract:** For a new function `[name]`, pre-define its dataset (`name_test.tsv`) and manifest (`name_manifest.yaml`).
2. **CLI Execution:** Execute test logic via the standard `argparse` CLI runner depending on the operational engine.
3. **Evidence Generation & Path Standard:**
   - **For Automatic Library Testing (e.g. implementation of new decorator):** Results MUST be saved in `tmp/{lib}/`.
   - **For Manifest Testing:** Headless results MUST be strictly routed to `tmp/Manifest_test/{manifest_basename}/`.
   - Resulting tables are saved as `USER_debug_view.tsv` (via `.collect()`) and Plots to `USER_debug_{plot}.png`.
4. **Console Glimpse (Proof of Life):** Output `df.glimpse()` to standard output, and present the plot PNG path.
5. **The Halt:** Agents MUST halt autonomous execution and declare: "Data/Plot ready in tmp/... Waiting for @verify."
6. **Transparency Mandate:** Every @verify result MUST list the exact file paths used for Data, Manifests, and Resulting Artifacts.

## 4. Active Visibility Protocol (Skeletal-Archive)

To prevent context-window saturation and maintain a clean active roadmap, the following protocol is mandatory:

- **100% DONE Gate**: Only 100% completed [x] items may be moved to archives. ANY task that is either in-progress [ ] or [DEFERRED] MUST remain in the main tasks.md under its original logical header to ensure immediate visibility.
- **Skeleton Retention**: The main `tasks.md` MUST retain the original Header but replace the completed checklist items with a skeletal pointer: `> Status: COMPLETED. Detailed history moved to: [Archive Path]`.
- **Naming Standard**: Archive files use the `tasks_archive_[unit_name].md` convention.

## 5. Conflict Guardrails (Sync-or-Stop)

- **@sync**: If the Agent detects a discrepancy between the user's intent (chat) and the physical codebase structure, it must halt and ask to `@sync`.
- Project Rules and Architecture Decisions (ADRs) unconditionally overrule generic conversational prompts. Modify them only through Double-Confirmation with the user.

## 6. Dual-Directory Output Segregation (Agent vs User)

Two distinct temporary directories exist at the project root. Their purposes are **strictly non-interchangeable**:

| Directory | Owner | Purpose | Consent required? |
| --- | --- | --- | --- |
| `./tmpAI/` | Agent | Agent-internal testing, scratch scripts, intermediate logs, debug runs that the agent initiates autonomously. | **No** — agent may read and write freely without halting for user approval. |
| `./tmp/` | User | Outputs the user must review: `@verify` evidence, `USER_debug_*.tsv/png` artifacts, Manifest test results. | **Yes** — agent must halt and declare paths per the `@verify` protocol before the user proceeds. |

**Rules:**

- Any test script, log, or artifact that is **agent-internal** (exploratory run, import check, intermediate debug, CI-style headless validation not yet ready for user review) MUST be written to `./tmpAI/`. Sub-directory structure mirrors `./tmp/`: `tmpAI/{lib}/` for library tests, `tmpAI/Manifest_test/{manifest_basename}/` for manifest tests.
- `./tmp/` is **reserved exclusively for `@verify` outputs** — results the agent declares to the user as ready for inspection. Writing agent-internal scratch to `./tmp/` is a protocol violation.
- Both directories are persistent and git-ignored. Neither is scanned by the embedding engine.
- When promoting an agent-internal result to user-review status (i.e., the test passed headlessly and is ready for `@verify`), the agent MUST copy the artifact from `./tmpAI/` to `./tmp/` and then declare the `./tmp/` path per section 3.

## 7. Failure Test Mandate (ADR-034)

To ensure the Diagnostic Layer remains robust, every significant component (Ingestion, Transformer, VizFactory) MUST include at least one "Automated Failure Test" in its integrity suite.

- **Rule**: Developers must provide a "Malformed Manifest" that intentionally triggers a `SPARMVET_Error`.
- **Validation**: The test passes only if the system catches the specific error and returns the appropriate `tip` suggested in the diagnostic registry.
