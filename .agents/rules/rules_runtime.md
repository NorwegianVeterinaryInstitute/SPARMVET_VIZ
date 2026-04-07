---
trigger: always_on
---

# Runtime & Environment Authority (rules_runtime.md)

## 1. System Truths (Pinned Lifecycle)

- **IDE Version:** Antigravity v1.19.6 (STABLE/PINNED).
- **OS:** Fedora 43 KDE X1 (Velocifero Compute).
- **Update Policy:** `update.mode: none` (DNF pinned).
- **VENV:** All execution MUST use `./.venv/bin/python`.

## 2. Directory Authority (The Recovery Toolkit)

The following paths in the project root are the **ONLY Authorized** source of truth for workspace state and versioning. The creation of new top-level folders within `./.antigravity/` is strictly FORBIDDEN.

- **`./.antigravity/plans/`**: `implementation_plan_master.md` (**SOLE AUTHORITATIVE ROADMAP**).
- **`./.antigravity/tasks/`**: `tasks.md` (**SOLE SOURCE OF TRUTH FOR EXECUTION**).
- **`./.antigravity/knowledge/`**: Persistent codebase knowledge items (KIs).

## 3. Logic Source of Truth (Technical Authority)

The following files are the **Command Rules of Engagement**:

- `./.agents/rules/workspace_standard.md` (**MASTER AUTHORITY INDEX**)
- `./.antigravity/knowledge/architecture_decisions.md` (**TECHNICAL BIBLE**)
- `./.antigravity/knowledge/project_conventions.md` (**ESSENTIAL FILES/CONVENTIONS**)

## 4. Environment Authority (VENV)

- **Single VENV:** All execution MUST occur within `./.venv/` at the root.STATUS: Verified Active (Prefix: /home/evezeyl/Documents/Insync/gdrive/OBSWORK/20_GITS/SPARMVET_VIZ/.venv). Do NOT re-run environment checks.
- **Dependency Sync:** Libraries (e.g., `polars`, `plotnine`) must be added to `pyproject.toml` in both `libs/[lib_name]/` and `app/`.
- **Package-First Authority:** All core libraries (`ingestion`, `transformer`, `utils`, `viz_factory`) MUST be installed in 'Editable Mode' (`pip install -e`).
- **No Path Hacking:** Use of `sys.path.append` or `sys.path.insert` is strictly PROHIBITED. All imports must be standard package imports.

## 5. Modular Library Autonomy (Clear Lines Policy)

- **Standalone Modules:** Libraries in `./libs/` must be data-agnostic and developed as if in separate repos.
- **Data-Agnostic Logic:** Internal lib logic must not fetch raw data files; it receives `LazyFrames` from the caller.
- **NO Cross-Library Imports:** It is FORBIDDEN for one library in `./libs/` to import from another (e.g., `transformer` MUST NOT import `ingestion`).
- **Orchestration Layer:** Coordination between libraries is restricted to the **App Layer** (`app/`) or top-level **Execution Scripts** (`assets/scripts/`).
