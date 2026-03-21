---
trigger: always_on
---

# Antigravity Workspace Standard (v1.19.6)
**Owner:** @dasharch
**Persistence Level:** Mandatory

## 1. Directory Authority
All agent operations must map to these specific paths. **STRICTLY FORBIDDEN:** Creating top-level folders without a dot prefix for Antigravity-managed directories (e.g., `antigravity/` is prohibited; use `.antigravity/`).

- **`.agents/rules/`**: Permanent Persona and Logic (Read-only for Agent).
- **`.agents/skills/`**: Custom tool/MCP definitions.
- **`.agents/workflows/`**: Multi-step automation scripts.
- **`.antigravity/knowledge/` and ``.antigravity/conversations/`**: Processed "Memories" and long-term insights.
- **`.antigravity/embeddings/`**: Local/Cloud Vector search data.
- **`.antigravity/tasks/`**: Live, editable task state.
- **`.antigravity/logs/`**: Human-readable session audits (Cold Memory).

## 2. Operational Directives
- **Memory Recovery:** Always check `.antigravity/logs/` before starting a new complex task.
- **Quota Shield:** Default to **Gemini 3 Flash** for file-writing and indexing tasks.
- **Consistency:** If a file is generated, it must be indexed immediately into the workspace context.

## 3. Automated Logging Protocol
- **File Target:** `./antigravity/logs/audit_{{YYYY-MM-DD}}.md`.
- **Mode:** APPEND ONLY. Never overwrite previous entries in the same day.
- **Trigger:** At the end of every significant task or before closing a chat session, the agent MUST append a "Cold Memory" summary.
- **Content:** Include:
    - Current Task Status (Success/Failure).
    - Changes made to `.antigravity/tasks/`.
    - New Knowledge/Directives ingested.