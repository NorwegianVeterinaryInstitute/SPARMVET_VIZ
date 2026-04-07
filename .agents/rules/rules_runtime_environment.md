# Runtime & Environment Authority (rules_runtime_environment.md)

**Authority:** Defines constraints on python environments, dependency locators, and module isolation.

## 1. System & IDE Truths (Pinned Lifecycle)

- **IDE Version:** Antigravity v1.19.6 (STABLE/PINNED).
- **OS:** Fedora 43 KDE X1 (Velocifero Compute).
- **Update Policy:** `update.mode: none` (DNF pinned). Do not attempt to upgrade generic apt/dnf OS layers outside of explicit commands.
- **VENV Enforcement:** All execution MUST occur exclusively within the `./.venv/bin/python` environment at the project root.
- **Verification Rule:** Do NOT repeatedly re-run virtual environment checks if the status is already known to be successfully locked.

## 2. Directory Governance (The Master Root)

The following paths in the project root are the **ONLY Authorized** core operational centers. The creation of arbitrary top-level folders within `./.antigravity/` without explicit authorization is strictly FORBIDDEN.

**Boundary Lock (`.aiignore`):** The agent MUST strictly respect the `.aiignore` file located at the project root. Do not scan directories like `EVE_WORK`, `archives`, or `.antigravity/embeddings/` unless the user explicitly grants a "Border-Crossing Permit" for a specific file.

- **`./.antigravity/plans/`**: `implementation_plan_master.md` (Sole authoritative roadmap).
- **`./.antigravity/tasks/`**: `tasks.md` (Sole execution status authority).
- **`./.antigravity/knowledge/`**: Persistent codebase intelligence logs and KIs.
- **`./.antigravity/logs/`**: **Log Authority**. ALL session audits and daily logs MUST be stored in `./.antigravity/logs/audit_{YYYY-MM-DD}.md`. The creation of log files in the project root or `EVE_WORK/` is strictly FORBIDDEN.
- **`./docs/`**: The absolute single source of truth for all human-facing project knowledge, diagrams, and API boundaries.

## 3. Modular Monorepo & Editable Packages (ADR-011 / ADR-016)

The `/libs/` directory contains highly autonomous logic modules. Each directory within must be treated as a wholly independent python package.

- **Editable Mode Mandate**: All core libraries (`ingestion`, `transformer`, `utils`, `viz_factory`) MUST be installed in 'Editable Mode' (`pip install -e`).
- **Dependencies (`pyproject.toml`)**: Libraries must declare their dependencies strictly inside their respective `pyproject.toml` files, bypassing archaic `requirements.txt`.
- **No Path Hacking**: The use of `sys.path.append` or `sys.path.insert` is completely PROHIBITED across the entire project structure. All connections must invoke absolute or standard package imports.

## 4. The "Clear Lines" Library Policy

To retain decoupling between data transformation paradigms and visualization architectures:

- **Standalone Constraint:** Libraries within `./libs/` must be entirely data-agnostic.
- **No Cross-Library Internal Imports:** One library in `./libs/` MUST NEVER import code from another library (`transformer` is strictly forbidden from importing from `ingestion`).
- **The Orchestrator Privilege:** Multi-library dependencies and coordination scripts belong strictly within the **App Layer** (`app/`) or root **Execution Scripts** (`assets/scripts/`).
