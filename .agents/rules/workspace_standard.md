---
trigger: always_on
---

# Antigravity Workspace Standard (v1.20.0)

**Authority:** All Active Agents (@dasharch)
**Workspace ID:** SPARMVET_VIZ
**Persistence Level:** Mandatory Authority

## 0. Mandatory Dispatch (Read Order)

To prevent AI Drift and Quota Waste, the Agent MUST follow this sequence upon initialization:

1. **./tree.txt**: Locate the physical file map.
2. **./.antigravity/knowledge/project_conventions.md**: Identify the "Who/Where/How" for every component.
3. **./.agents/rules/rules_runtime_environment.md**: Lock the `./.venv/bin/python` path.

## 1. The Master Index

This file is the **Sole Source of Authority** for agentic behavior in the SPARMVET_VIZ workspace. It is organized into modular rulebooks. Agents MUST read all referenced files before executing logic.

| Rulebook | Scope | File Reference |
| :--- | :--- | :--- |
| **Doc & Aesthetics** | Violet Law, Quarto/Mermaid, CSS Themes, Doc Sync | [rules_documentation_aesthetics.md](./.agents/rules/rules_documentation_aesthetics.md) |
| **Data Engine** | 3-Tier Tree Lifecycle (ADR-024), Decorators, Manifests | [rules_data_engine.md](./.agents/rules/rules_data_engine.md) |
| **Validation & Test** | @verify Protocol, Global Wrappers, CLI Mandate | [rules_verification_testing.md](./.agents/rules/rules_verification_testing.md) |
| **Runtime & Env** | VENV, No-Discovery, Pinned Versions, Library Autonomy | [rules_runtime_environment.md](./.agents/rules/rules_runtime_environment.md) |
| **Asset Scripts** | Bootstrappers, Synthetic Data, Governance | [rules_asset_scripts.md](./.agents/rules/rules_asset_scripts.md) |
| **UI rules** | UI Orchestration & Aesthetics | [rules_ui_dashboard.md](./.agents/rules/rules_ui_dashboard.md) |

## 2. Primary Technical Bible

- **Roadmap:** `implementation_plan_master.md (./.antigravity/plans/)`
- **Execution:** `tasks.md (./.antigravity/tasks/)`
- **Architecture:** `architecture_decisions.md (./.antigravity/knowledge/)`

## 3. Operational Mandate

- **Mandatory Halt:** Every significant transformation or rule change requires an explicit `@verify` from the user.
- **Violet Law:** All component references in documentation must follow `ClassName (filename.py)` standard.
- **Single Source of Truth:** Local workspace files (`./.antigravity/`) are the authoritative source over global IDE state.
- **Relative Path Authority:** ALL file paths provided in manifests, rulebooks, and technical documentation MUST be relative to the project root. The use of absolute paths or symbolic links within the project structure is strictly FORBIDDEN.

---
