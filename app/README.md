## Architecture overview (Phase 12-A)

The SPARMVET App is a **Thin Shiny Shell** that orchestrates three distinct layers:

1. **The Navigation Layer (Left)**: A reactive persona-gated control center (ADR-026).
2. **The Analysis Theater (Center)**: A 2x2 Quadrant Grid supporting side-by-side Ref vs Active comparison (ADR-029a).
3. **The Audit Stack (Right)**: A justification-gated logic trace enforcing ADR-026 compliance.

### Directory Structure

.
├── app.py                 <-- THE BOOTSTRAP (Entry Point)
├── src/                   # Core Interface Logic
│   ├── bootloader.py      # Persona & Path Authority
│   ├── ui.py              # Visual Skeleton (3-Zone)
│   └── server.py          # Reactive Orchestrator
├── modules/               # Persistent App Modules
│   ├── wrangle_studio.py  # Tier 3 Logic Builder
│   └── dev_studio.py      # Admin Manifest Tools
└── tests/                 # Forensic Audit Suite
    ├── test_ui_persona_masking.py  # Silicon-Gate Verification
    └── test_ui_refactoring_audit.py # Orchestractor Stress Test

## Headless Testing Architecture

To ensure 100% architectural stability without browser dependencies, SPARMVET uses a **Logic-First Audit Pattern**:

- **Silicon-Gate Audit**: Headless tests that instantiate the `Bootloader` and `PersonaManager` to verify feature-masking compliance.
- **Orchestrator Stress**: Tests that simulate the `DataOrchestrator` lifecycle (Ingestion -> Tier 1 -> Tier 3) using manifest-ground-truth.

**Recommended Test Command:**

```bash
./.venv/bin/python -m unittest discover app/tests
```
