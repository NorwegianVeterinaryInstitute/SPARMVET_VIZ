---
trigger: always_on
---

# App Structure Rules (ADR-045)

**Authority:** @dasharch
**Status:** FINALIZED / ARCHITECTURAL LOCK (2026-04-23)

This rulebook governs the internal structure of the `app/` package. It enforces the decomposition of `app/src/server.py` into a thin orchestrator plus focused handler modules and a pure manifest introspection module.

---

## 1. The Two-Category Law (The Hard Boundary)

All code in `app/` falls into exactly one of two categories. **Mixing them is a protocol violation.**

| Category | Where it lives | Rule |
|---|---|---|
| **Pure manifest introspection** | `app/modules/manifest_navigator.py` | Zero Shiny imports. Zero `input`/`output`/`session`. Pure Python functions — importable from headless scripts, test suites, DevStudio, and CLI tools without side effects. |
| **Shiny reactive wiring** | `app/handlers/<concern>.py` | Contains `@render.*`, `@reactive.Effect`, `@reactive.Calc`. Receives shared state via explicit `define_server(...)` keyword arguments. **Never imported by non-Shiny contexts.** |

**Violation examples:**
- Adding a `@render.ui` decorator inside `manifest_navigator.py` → FORBIDDEN.
- Importing from `app/handlers/blueprint_handlers.py` in a headless debug script → FORBIDDEN (handler files carry Shiny registration side-effects).
- Calling `build_sibling_map()` directly inside `server.py` without going through a handler → ALLOWED (it is a pure function), but new callers in `server.py` should be delegated to handlers.

---

## 2. Directory Map

```
app/
├── src/
│   ├── server.py          # Thin orchestrator only (~120 lines). See §3.
│   ├── ui.py              # Static Shiny UI shell. CSS. No reactive logic.
│   └── bootloader.py      # Path authority & persona bootstrap (ADR-031).
│
├── modules/               # Importable, testable, Shiny-free modules.
│   ├── manifest_navigator.py   # Pure manifest introspection engine (ADR-045).
│   ├── orchestrator.py         # DataOrchestrator — Tier 1 assembly bridge.
│   ├── wrangle_studio.py       # WrangleStudio — Blueprint Architect UI class.
│   ├── gallery_viewer.py       # GalleryViewer — static gallery browser.
│   ├── dev_studio.py           # DevStudio — developer diagnostic tools.
│   └── exporter.py             # SubmissionExporter — gallery submission.
│
├── handlers/              # Shiny wiring only. One concern per file.
│   ├── __init__.py
│   ├── home_theater.py         # Home mode: tabs, sidebar, filters, plots, tables.
│   ├── audit_stack.py          # Pipeline Audit: T2/T3 nodes, Apply gate, Revert.
│   ├── blueprint_handlers.py   # Blueprint Architect: manifest import, lineage, TubeMap.
│   ├── gallery_handlers.py     # Gallery: filtering, preview, clone, submission.
│   └── ingestion_handlers.py   # Ingestion & persona switching.
│
└── assets/                # Static/utility scripts (no Shiny).
    └── normalize_manifest_fields.py
```

---

## 3. `server.py` Permitted Content (Thin Orchestrator Only)

`server.py` MUST contain ONLY the following. Nothing else.

1. **Imports** of modules, handlers, and libraries.
2. **Module initialisation**: `WrangleStudio(session.id)`, `DevStudio()`, `DataOrchestrator(...)`, `VizFactory(...)`.
3. **Shared reactive state** (`reactive.Value`): `anchor_path`, `recipe_pending`, `snapshot_recipe`, `gallery_refresh_trigger`, `current_persona`.
4. **Shared reactive calcs** (`@reactive.Calc`): `active_collection_id`, `active_cfg`, `tier1_anchor`, `tier_reference`, `tier3_leaf`. These are shared because multiple handlers depend on them.
5. **Shared utility functions**: `_safe_input`, `_apply_tier2_transforms`. These are pure helpers used by multiple handlers.
6. **Five `define_server(...)` delegation calls** — one per handler module, in dependency order.

**Hard limit:** `server.py` MUST NOT grow beyond ~250 lines. Any new reactive output/effect belongs in a handler.

---

## 4. `app/modules/manifest_navigator.py` — Public API

The `ManifestNavigator (manifest_navigator.py)` module exports five public functions (no leading underscore). Internal sub-helpers within those functions remain private.

| Public Function | Signature | Returns |
|---|---|---|
| `build_sibling_map(manifest_path_str)` | `str → dict` | `rel_path → {role, schema_id, schema_type, siblings, ingredients}` |
| `build_schema_registry(manifest_path_str, includes_map)` | `str, dict → dict` | `schema_id → {schema_type, input_fields, wrangling, output_fields, …}` |
| `build_lineage_chain(selected_rel, ctx_map)` | `str, dict → list[dict]` | Ordered `[{rel, schema_id, role, label, is_active}]` |
| `load_fields_file(abs_path)` | `Path → dict` | ADR-041 Rich Dict with ADR-014 unnesting |
| `resolve_fields_for_schema(schema_id, ctx_map, inc_map)` | `str, dict, dict → dict` | ADR-041 Rich Dict, recursive with cycle guard |

**Import pattern** (from any context):
```python
from app.modules.manifest_navigator import (
    build_sibling_map, build_schema_registry, build_lineage_chain,
    load_fields_file, resolve_fields_for_schema
)
```

---

## 5. Handler `define_server(...)` Contract

Every handler module MUST expose exactly one entry point:

```python
def define_server(input, output, session, *, <explicit_dependencies>):
    """Registers all @render.* and @reactive.* for <concern>."""
    ...
```

**Rules:**
- `input, output, session` are always the first three positional arguments.
- All shared state and calcs MUST be passed as **keyword-only arguments** (after `*`) to prevent positional errors.
- The function MUST NOT `return` anything. Side effects (registrations) only.
- Dependencies MUST be minimal — only pass what the handler actually uses.

**Example signature:**
```python
# app/handlers/home_theater.py
def define_server(input, output, session, *,
                  active_cfg, tier1_anchor, tier_reference, tier3_leaf,
                  current_persona, anchor_path, recipe_pending, snapshot_recipe,
                  wrangle_studio, orchestrator, viz_factory, bootloader):
```

---

## 6. Ownership Matrix — Where to Make Changes

| I need to change... | Edit this file |
|---|---|
| How the Home tabs are built / what the left sidebar shows | `app/handlers/home_theater.py` |
| The Pipeline Audit stack (Violet/Yellow nodes, Apply gate) | `app/handlers/audit_stack.py` |
| Blueprint Architect manifest import / TubeMap / Lineage Rail | `app/handlers/blueprint_handlers.py` |
| Gallery filtering, preview, clone, submission | `app/handlers/gallery_handlers.py` |
| Data ingestion / persona switching | `app/handlers/ingestion_handlers.py` |
| How manifests are parsed structurally (sibling map, registry, lineage) | `app/modules/manifest_navigator.py` |
| The static Shiny HTML shell / CSS | `app/src/ui.py` |
| Path authority / persona bootstrap | `app/src/bootloader.py` |
| Shared reactive state or tier calcs | `app/src/server.py` (§3 only) |
| Tier 1 assembly / Parquet materialization | `app/modules/orchestrator.py` |
| Visual plot composition | `libs/viz_factory/` |
| Data wrangling actions | `libs/transformer/` |

---

## 7. Verification Protocol

The decomposition refactor (Phase 22) is **behaviour-neutral** — no logic changes, only structural relocation. Verification complete (2026-04-23):

1. **Import check**: `python -c "from app.src.server import server"` — ✅ passed.
2. **Navigator unit check**: `python -c "from app.modules.manifest_navigator import build_sibling_map; print('OK')"` — ✅ passed.
3. **Live UI check**: UI smoke test by user — no major regressions detected. ✅
