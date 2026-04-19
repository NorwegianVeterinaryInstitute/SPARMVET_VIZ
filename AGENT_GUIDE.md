# 🛸 SPARMVET_VIZ: Unified Agent Protocol (v1.0)

## 1. Core Authority & Context

- **Root Authority**: `/.agents/rules/workspace_standard.md`
- **Knowledge Authority directory**: `/.antigravity/knowledge`.
- **Read Order**: You MUST read files in the order defined in the Master Index before generating code.
- **Environment**: OS: Fedora 43 | Python: `./.venv/bin/python` | Pinned: v1.19.6.

## 2. Shared Coding Standards

- **Data Engine**: Polars LazyFrames ONLY. No Pandas except at the terminal plotting gate.
- **Pattern**: 'Decorator-First' logic via `@register_action`.
- **Tiers**: Adhere to the 3-Tier Lifecycle (ADR-024): Anchor (T1) -> Branch (T2) -> Leaf (T3).
- **Aesthetics**: 'Violet Law' naming and 'Deep Violet' code block themes for docs.

## 3. Communication & Handoff Procedure

To prevent AI Drift when switching between Gemini and Claude, follow this mailbox protocol:

- **State File**: `/.antigravity/logs/handoff_active.md`.
- **Handoff Requirement**:
    1. Before stopping, the active agent MUST write the current status, specific file paths modified, and the "Next Step" prompt to the Handoff File.
    2. Upon starting, the new agent MUST read `handoff_active.md` to resume the "Stream of Consciousness."
- **Conflict Resolution**: If instructions in chat conflict with this file, HALT and request `@sync`.

## 4. Verification Gate (@verify)

- All significant logic changes require the **Evidence Loop**: Contract -> CLI Execution -> Materialize to `tmp/` -> Halt for User.
