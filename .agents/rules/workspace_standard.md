---
trigger: always_on
---

# Antigravity Workspace Standard (v1.20.0)

**Authority:** All Active Agents (@dasharch)
**Workspace ID:** SPARMVET_VIZ
**Persistence Level:** Mandatory Authority

## 1. The Master Index

This file is the **Sole Source of Authority** for agentic behavior in the SPARMVET_VIZ workspace. It is organized into modular rulebooks. Agents MUST read all referenced files before executing logic.

| Rulebook | Scope | File Reference |
| :--- | :--- | :--- |
| **Doc & Aesthetics** | Violet Law, Quarto/Mermaid, CSS Themes, Doc Sync | [rules_documentation_aesthetics.md](./rules_documentation_aesthetics.md) |
| **Data Engine** | 3-Tier Tree Lifecycle, Decorators, Manifests | [rules_data_engine.md](./rules_data_engine.md) |
| **Validation & Test** | @verify Protocol, Global Wrappers, CLI Mandate | [rules_verification_testing.md](./rules_verification_testing.md) |
| **Runtime & Env** | VENV, Library Autonomy, Pinned Versions | [rules_runtime_environment.md](./rules_runtime_environment.md) |
| **Asset Scripts** | Bootstrappers, Synthetic Data, Governance | [rules_asset_scripts.md](./rules_asset_scripts.md) |

## 2. Primary Technical Bible

- **Roadmap:** `implementation_plan_master.md (./.antigravity/plans/)`
- **Execution:** `tasks.md (./.antigravity/tasks/)`
- **Architecture:** `architecture_decisions.md (./.antigravity/knowledge/)`

## 3. Operational Mandate

- **Mandatory Halt:** Every significant transformation or rule change requires an explicit `@verify` from the user.
- **Violet Law:** All component references in documentation must follow `ClassName (filename.py)` standard.
- **Single Source of Truth:** Local workspace files (`./.antigravity/`) are the authoritative source over global IDE state.

---
