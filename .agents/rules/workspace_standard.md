---
trigger: always_on
---

# Antigravity Workspace Standard (v1.19.6)
**Authority:** All Active Agents (Universal Ownership)
**Workspace ID:** SPARMVET_VIZ
**Persistence Level:** Mandatory 

## 1. Directory Authority (The Recovery Toolkit)
The following paths in the project root are the **Source of Truth** for Git versioning.
- **`./.antigravity/conversations/`**: Archived chat exports and manual history mirrors.
- **`./.antigravity/plans/`**: implementation_plan.md and architectural roadmaps.
- **`./.antigravity/tasks/`**: Live tasks.md tracking progress.
- **`./.antigravity/logs/`**: Daily audit logs and change records.

## 2. Operational Directives: The Mirror Protocol
- **State Mirroring:** Every time a task is updated or a plan is modified, the Agent MUST write a copy to the respective `./.antigravity/` folder.
- **Chat Archiving:** Before ending a session, the Agent MUST export a summary or full log of the current conversation to `./.antigravity/conversations/`.
- **Conflict Resolution:** If the global IDE state differs from the local workspace files, the **local workspace files** are the authoritative source.
- **No Ghost State:** Technical decisions made in chat are not "real" until they are mirrored into `architecture_decisions.md` or `tasks.md`.

## 3. Commit Readiness
- All mirrored artifacts must use clean Markdown formatting for Git diffing.
- Priority is placed on **First-Time Accuracy** to ensure the mirrored history is a reliable technical record.
