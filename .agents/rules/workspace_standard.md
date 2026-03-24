---
trigger: always_on
---

# Antigravity Workspace Standard (v1.19.6)
**Authority:** All Active Agents (Universal Ownership)
**Workspace ID:** SPARMVET_VIZ
**Persistence Level:** Mandatory 

## 1. Directory Authority (The Recovery Toolkit)
The following paths in the project root are the **ONLY Authorized** source of truth for workspace state and versioning. The creation of new top-level folders within `./.antigravity/` is strictly FORBIDDEN without architectural review.

- **`./.antigravity/plans/`**: `implementation_plan_master.md` (**SOLE AUTHORITATIVE ROADMAP**).
- **`./.antigravity/tasks/`**: `tasks.md` (**SOLE SOURCE OF TRUTH FOR EXECUTION**).
- **`./.antigravity/conversations/`**: Archived chat exports and session summaries.
- **`./.antigravity/logs/`**: Daily audit logs and change records.
- **`./.antigravity/knowledge/`**: Persistent codebase knowledge items (KIs).
- **`./.antigravity/embeddings/`**: Local vector storage for tool-layer retrieval.

## 2. Logic Source of Truth (Technical Authority)
The following files are the **Command Rules of Engagement**. Failure to consult these before implementation is a violation of the `@dasharch` authority.

| Path | Role | Rule of Usage |
| :--- | :--- | :--- |
| `./.antigravity/plans/implementation_plan_master.md` | **Sole Roadmap** | Check this to determine the current Phase and Task ID. |
| `./.antigravity/knowledge/architecture_decisions.md` | **Technical Bible** | Consult before writing NEW logic to ensure ADR compliance. |
| `./.antigravity/knowledge/blockers.md` | **Hurdle Tracker** | Review when entering a new Phase to check for unresolved logic blockers. |
| `./.antigravity/knowledge/milestones.md` | **Project Memory** | Refines the historical context of what has been verified. |
| `./.antigravity/tasks/tasks.md` | **Execution Tracker** | MUST be updated after every `@verify` gate. |

## 3. Operational Directives: The Mirror Protocol
- **State Mirroring:** Every time a task is updated or a plan is modified, the Agent MUST write a copy to the respective `./.antigravity/` folder.
- **Chat Archiving:** Before ending a session, the Agent MUST export a summary or full log of the current conversation to `./.antigravity/conversations/`.
- **Conflict Resolution:** If the global IDE state differs from the local workspace files, the **local workspace files** are the authoritative source.
- **No Ghost State:** Technical decisions made in chat are not "real" until they are mirrored into `architecture_decisions.md` or `tasks.md`.

## 3. Environment Authority (VENV)
- **Single VENV:** All execution MUST occur within a `.venv/` directory located at the project root.
- **Agent Restriction:** Agents are FORBIDDEN from creating sub-environments or local `__pypackages__`.
- **Dependency Sync:** Any new library (e.g., `polars`, `plotnine`, `ruamel.yaml`) must be added to `pyproject.toml` before implementation. This for Each library (subdirectory in libs) AND for the general App in app/pyproject.toml.  
- **Cleanup:** All `__pycache__` and `.ipynb_checkpoints` must be ignored by Git and the Agent's scan.

## 4. Commit Readiness
- All mirrored artifacts must use clean Markdown formatting for Git diffing.
- Priority is placed on **First-Time Accuracy** to ensure the mirrored history is a reliable technical record.

## 5. Persistent Access & Permissions
- **Root .venv Access:** The Agent is granted permanent, non-expiring access to `./.venv/` for the duration of the project.
- **No-Prompt Execution:** All calls to `python`, `pytest`, or `pip` within the root `.venv` are pre-authorized to avoid workflow interruptions.
- **Scope:** This access is limited to reading metadata and executing binaries; manual modification of `.venv` internals is reserved for environment-sync tasks only.

## 6. The Logic Conflict Guardrail
- **Rule of Precedence:** Project Rules (workspace_standard.md) and ADRs (architecture_decisions.md) always take precedence over chat prompts.
- **Mandatory Halt:** If a user prompt asks for an implementation that contradicts a Project Rule (e.g., asking for a CSV output when the rule is TSV), the Agent MUST NOT execute.
- **Clarification Loop:** The Agent must state: "I have detected a conflict between your request and [Rule Name]. Should I follow the Rule or the Prompt for this specific task?".

## 7. Documentation Integrity
- Never repeat source code or data content within documentation files. Instead, provide a relative link to the file (e.g., [test_wrangler.py](../tests/test_wrangler.py)). This prevents documentation drift and keeps files lightweight.
