---
trigger: always_on
date: 2026-03-29
purpose: Master Index for Workspace Standards
---

# Antigravity Workspace Standard (v1.20.0)
**Authority:** All Active Agents (@dasharch)
**Workspace ID:** SPARMVET_VIZ
**Persistence Level:** Mandatory Authority

## 1. The Master Index
This file is the **Sole Source of Authority** for agentic behavior in the SPARMVET_VIZ workspace. It is organized into modular rulebooks. Agents MUST read all referenced files before executing logic.

| Rulebook | Scope | File Reference |
| :--- | :--- | :--- |
| **Runtime & Env** | VENV, Library Autonomy, Pinned Versions | [rules_runtime.md](./rules_runtime.md) |
| **Wrangling & Data** | Decorators, Manifests (ADR-013), Types | [rules_wrangling.md](./rules_wrangling.md) |
| **Behavior & Flow** | @verify Protocol, Conflict Guardrails, Sync | [rules_behavior.md](./rules_behavior.md) |
| **Aesthetics & Dox** | Violet Law, Quarto/Mermaid, CSS Themes | [rules_aesthetic.md](./rules_aesthetic.md) |

## 2. Primary Technical Bible
- **Roadmap:** `implementation_plan_master.md (./.antigravity/plans/)`
- **Execution:** `tasks.md (./.antigravity/tasks/)`
- **Architecture:** `architecture_decisions.md (./.antigravity/knowledge/)`

## 3. Operational Mandate
- **Mandatory Halt:** Every significant transformation or rule change requires an explicit `@verify` from the user.
- **Violet Law:** All component references must follow `ClassName (filename.py)` standard.
- **Single Source of Truth:** Local workspace files (`./.antigravity/`) are the authoritative source over global IDE state.

---
**Status:** FULLY MIGRATED. Local rule directory is the new absolute Source of Truth.