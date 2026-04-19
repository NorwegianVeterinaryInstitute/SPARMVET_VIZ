# 🛸 SPARMVET_VIZ: Unified Agent Protocol (v1.0)

## 1. Core Authority & Context

- **Root Authority**: `/.agents/rules/workspace_standard.md`
- **Read Order**: You MUST read files in the order defined in the Master Index before generating code.
- **Environment**: OS: Fedora 43 | Python: `./.venv/bin/python` | Pinned: v1.19.6.
- **Mode of action** You are equipped with a modular rule system. Do not guess logic. You MUST identify and read the relevant files defined in next section "## 2. PATH INITIATION:" , from the following directories BEFORE executing a task. 

## 2. PATH INITIATION: 


### 2.1. Rules & Governance (`./.agents/rules/`)

These files define the "how" and "where" of project execution. They are critical for ensuring the agent uses the correct Python environment and follows established coding standards.

|**File Path**|**Short Description**|
|---|---|
|`workspace_standard.md`|**The Technical Bible.** Defines mandatory read order, path authority (VENV), and modular library rules.|
|`rules_runtime_environment.md`|**Environment Lock.** Pinned system versions (IDE v1.19.6), VENV enforcement, and "Clear Lines" library policy.|
|`rules_data_engine.md`|**Data Protocols.** Defines the 3-Tier Lifecycle (Anchor/Branch/Leaf) and the "Law of Decorators".|
|`rules_manifest_structure.md`|**YAML Standards.** Mandates "Basename Mirroring" and `!include` structure for manifest components.|
|`rules_verification_testing.md`|**The Audit Gate.** Establishes the `@verify` protocol and the mandatory use of CLI debuggers in `tmp/`.|
|`rules_ui_dashboard.md`|**UI Contract.** Persona masking rules, Sidebar behaviors, and the `btn_apply` gatekeeper logic.|
|`rules_documentation_aesthetics.md`|**The Violet Law.** Enforces Quarto DRY rules and standard naming for human-facing docs.|
|`rules_asset_scripts.md`|**Utility Governance.** Manages the use of bootstrappers and synthetic data generators in `assets/`.|

---

### 2.2. Workflows (`./.agents/workflows/`)

These provide step-by-step instructions for specific technical tasks. Give these to the agent _only_ when that specific phase is active.

|**File Path**|**Short Description**|
|---|---|
|`implementation_workflow_transformer.md`|Protocol for implementing new wrangling decorators and Tier 1 logic.|
|`viz_factory_implementation.md`|Protocol for the "Artist Pillar"—registering geoms, scales, and themes.|
|`ui_manifest_integration_testing.md`|**The Master Gate.** Strictly prohibits UI testing until all headless audits pass.|
|`transformer_testing.md`|Specific steps for using `debug_assembler.py` and `debug_wrangler.py`.|
|`verification_protocol.md`|Centralized instructions for triggering manual user verification gates.|

---

### 2.3. Knowledge & Architecture (`./.antigravity/knowledge/`)

These track the "why" and the long-term state of project intelligence.

|**File Path**|**Short Description**|
|---|---|
|`architecture_decisions.md`|**ADR Log.** The definitive record of all 35+ major architectural decisions (e.g., ADR-024 Tiering).|
|`project_conventions.md`|**Combat Log.** A compressed registry of class names, key terms, and the path authority strategy.|
|`persona_traceability_matrix.md`|**UI Logic.** Authoritative mapping of which UI elements are visible to which persona profile.|
|`milestones.md`|Historical record of project phases (Legacy → Skeleton → Prototyping).|
|`blockers.md`|Tracking of technical debt and unresolved data orchestration challenges.|

---

### 2.4. Plans & Tasks (`./.antigravity/plans/` & `tasks/`)

These represent the active roadmap and granular execution status.

|**File Path**|**Short Description**|
|---|---|
|`implementation_plan_master.md`|**Authoritative Roadmap.** Tracks high-level phases (currently Phase 12-A) and technical goals.|
|`tasks.md`|**Live Execution Status.** The sole source of truth for what needs to be done _right now_.|

---

## 2. Communication & Handoff Procedure

To prevent AI Drift when switching between Gemini and Claude, follow this mailbox protocol:

- **State File**: `/.antigravity/logs/handoff_active.md`.
- **Handoff Requirement**:
    1. Before stopping, the active agent MUST write the current status, specific file paths modified, and the "Next Step" prompt to the Handoff File.
    2. Upon starting, the new agent MUST read `handoff_active.md` to resume the "Stream of Consciousness."
- **Conflict Resolution**: If instructions in chat conflict with this file, HALT and request `@sync`.

## 4. Verification Gate (@verify)

- All significant logic changes require the **Evidence Loop**: Contract -> CLI Execution -> Materialize to `tmp/` -> Halt for User.
