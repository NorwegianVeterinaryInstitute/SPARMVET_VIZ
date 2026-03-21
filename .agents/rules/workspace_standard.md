---
trigger: always_on
---

# Antigravity Workspace Standard (v1.19.6)
**Authority:** All Active Agents (Universal Ownership)
**Workspace ID:** SPARMVET_VIZ
**Persistence Level:** Mandatory / Split-Root Architecture

## 1. Directory Authority (Absolute Mapping)
All agent operations must map to these specific project-root paths. **STRICTLY FORBIDDEN:** Accessing global `~/.config/Antigravity` for workspace data.

- **`./.agents/`**: Core logic and persona workflows.
- **`./.antigravity/conversations/`**: Primary storage for chat logs and UI-accessible history.
- **`./.antigravity/knowledge/`**: Processed "Memories" (e.g., `blockers.md`, `milestones.md`).
- **`./.antigravity/embeddings/`**: Vector search data (Cloud Default).
- **`./.antigravity/tasks/`**: Live, editable task state and active plans.
- **`./.antigravity/logs/`**: Human-readable session audits and "Cold Memory".



## 2. Operational Directives
**Agent Duty:** Every agent active in this workspace is responsible for maintaining the integrity of the `.antigravity/` folder.
- **History Retrieval:** If the IDE sidebar is empty, the Agent MUST manually scan `./.antigravity/conversations/` to restore context.
- **Model Selection:** Use the model that achieves the highest accuracy for the specific complexity. Priority is placed on **First-Time Success** to prevent expensive "error-correction loops". 
- **Indexing:** Background indexing is handled by the IDE provider; agents must only ensure metadata in `memory_bank_status.md` is technically accurate.
- **Memory Management:**
    - **Short-term:** Active conversation context.
    - **Long-term:** Permanent updates to `./.antigravity/knowledge/`.
- **Indexing:** All new artifacts must be linked in `memory_bank_status.md` immediately.

## 3. Automated Logging Protocol (Cold Memory)
- **File Target:** `./.antigravity/logs/audit_{{YYYY-MM-DD}}.md`.
- **Trigger:** End of session or significant task completion.
- **Requirement:** Append (do not overwrite) Task Status, Knowledge ingestions, and Quota usage notes.

## 4. Artifact & Planning Protocol (Version Controlled)
All project management and architectural artifacts MUST be stored in the local workspace.

- **Implementation Plans:** Store as `./.antigravity/plans/implementation_plan_{{TASK_NAME}}.md`.
- **Live Task Tracking:** Maintain `./.antigravity/tasks/tasks.md` as the primary checklist.
- **Architectural Decisions:** Document in `./.antigravity/knowledge/architecture_decisions.md`.

## 5. System Access & Diagnostics
- **Allowed System Paths:** The Agent is permitted to READ (not write) from `~/.config/Antigravity/logs/` and `~/.config/Antigravity/settings.json` for troubleshooting.
- **Sidebar Sync:** If the sidebar fails to populate, the Agent must attempt to locate the 'global_history_index.json' to see if it is pointing to the wrong folder.

### Directive for Agents:
1. **No Ghost Plans:** Never store a plan only in the chat context. It must be written to a file in `./.antigravity/plans/` before execution begins.
2. **Task Sync:** Update the status in `./.antigravity/tasks/tasks.md` after every successful sub-task completion.
3. **Commit Readiness:** Ensure all artifacts use clean Markdown formatting suitable for Git diffs.