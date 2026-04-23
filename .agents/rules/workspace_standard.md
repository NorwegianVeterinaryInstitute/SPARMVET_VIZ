---
trigger: always_on
---

# Antigravity Workspace Standard (v1.20.0)

**Authority:** All Active Agents (@dasharch)
**Workspace ID:** SPARMVET_VIZ
**Persistence Level:** Mandatory Authority

## 0. Mandatory Dispatch (Read Order)

To prevent AI Drift and Quota Waste, the Agent MUST follow this sequence upon initialization:

1. **./AGENT_GUIDE.md**: Adopt the high-level Persona and Onboarding Context.
2. **./tree.txt**: Locate the physical file map.
3. **./.antigravity/knowledge/project_conventions.md**: Identify the "Who/Where/How" for every component.
4. **./.agents/rules/rules_runtime_environment.md**: Lock the `./.venv/bin/python` path.

## 1. The Master Index

This file is the **Sole Source of Authority** for agentic behavior in the SPARMVET_VIZ workspace. It is organized into modular rulebooks. Agents MUST read all referenced files before executing logic.

| Rulebook | Scope | File Reference |
| :--- | :--- | :--- |
| **Doc & Aesthetics** | Violet Law, Quarto/Mermaid, CSS Themes, Doc Sync | [rules_documentation_aesthetics.md](./.agents/rules/rules_documentation_aesthetics.md) |
| **Manifest Standards** | Basename Mirroring, YAML Includes | [rules_manifest_structure.md](./.agents/rules/rules_manifest_structure.md) |
| **Data Engine** | 3-Tier Tree Lifecycle (ADR-024), Decorators, Manifests | [rules_data_engine.md](./.agents/rules/rules_data_engine.md) |
| **Validation & Test** | @verify Protocol, Global Wrappers, CLI Mandate | [rules_verification_testing.md](./.agents/rules/rules_verification_testing.md) |
| **Runtime & Env** | VENV, No-Discovery, Pinned Versions, Library Autonomy | [rules_runtime_environment.md](./.agents/rules/rules_runtime_environment.md) |
| **Asset Scripts** | Bootstrappers, Synthetic Data, Governance | [rules_asset_scripts.md](./.agents/rules/rules_asset_scripts.md) |
| **UI Rules** | UI Orchestration & Aesthetics | [rules_ui_dashboard.md](./.agents/rules/rules_ui_dashboard.md) |
| **Viz Factory** | Artist Pillar, Plotnine Parity, Core Geoms | [rules_viz_factory.md](./.agents/rules/rules_viz_factory.md) |
| **UI Contract** | Theater Layout, Tier Toggle, Persona Masking, Audit Stack | [ui_implementation_contract.md](./.agents/rules/ui_implementation_contract.md) |
| **App Structure** | Server decomposition, Handler/Module boundary law | [rules_app_structure.md](./.agents/rules/rules_app_structure.md) |

## 2. Primary Technical Bible

- **Roadmap:** `implementation_plan_master.md (./.antigravity/plans/)`
- **Execution:** `tasks.md (./.antigravity/tasks/)`
- **Architecture:** `architecture_decisions.md (./.antigravity/knowledge/)`

## 3. Operational Mandate

- **Mandatory Halt:** Every significant transformation or rule change requires an explicit `@verify` from the user.
- **Violet Law:** All component references in documentation must follow `ClassName (filename.py)` standard.
- **Single Source of Truth:** Local workspace files (`./.antigravity/`) are the authoritative source over global IDE state.
- **Relative Path Authority:** ALL file paths provided in manifests, rulebooks, and technical documentation MUST be relative to the project root. The use of absolute paths or symbolic links within the project structure is strictly FORBIDDEN.
- Background Mandate: for any script execution (unless specified otherwise) you MUST use background execution flags to ensure the UI remains responsive.

## 4. Temporary Workspace Execution

Two segregated temporary directories exist at the project root. Their use is **strictly non-interchangeable** (see `rules_verification_testing.md` §6 for full protocol):

- **`./tmpAI/`** — Agent-exclusive scratch space. Agents read and write here freely, without halting for user consent. Used for exploratory runs, import checks, intermediate debug artifacts, and headless CI-style validation not yet ready for user review.
- **`./tmp/`** — User-review outputs only. Reserved exclusively for `@verify` evidence that the agent declares to the user as ready for inspection. Writing agent-internal scratch here is a protocol violation.

Both directories are persistent and ignored by the embedding engine. When an agent-internal result is promoted to `@verify` status, the artifact is copied from `./tmpAI/` to `./tmp/` before the halt declaration.

---
