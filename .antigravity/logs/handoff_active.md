# Handoff — Active State (2026-04-30, Session 8)

**Branch:** dev  
**Last commit:** `ab555cd` feat(21-H): headless verification 76/76 + session 8 handoff docs  
**Active agent:** @dasharch (Claude Sonnet 4.6)

---

## Current State

Phase 21 is effectively complete (21-A through 21-H done). Phase 22 (Session Management + T3 Audit) is fully implemented and awaiting live-UI verification. Phase 23 (Deployment Architecture) is designed but not implemented.

---

## What Was Done (Sessions 7 & 8)

### Session 7 — Orchestrator Fixes & Blueprint Architect

Three bugs fixed in `app/modules/orchestrator.py`:

1. **Wrong base ingredient**: built `assembly_ingredients` from all `data_schemas` instead of declared `ingredients:` list order. `DataAssembler` uses `keys()[0]` as base — order matters.
2. **No Path A for bare data schemas**: `target_dataset` pointing to a `data_schemas` entry fell to wrong fallback assembly. Fixed: Path A writes bare schema directly to parquet.
3. **Join key dtype mismatch**: `Categorical ≠ String` in Polars. Fixed: `per_ingredient_cast`/`base_cast` normalisation before assembling.

Also: removed all `if not out_p.exists()` stale-cache guards. Added hierarchical field cards, collapsible Live View cards, plot error banner to Blueprint Architect.

### Session 8 — Phase 21-E/G/H

- **Phase 21-E (Comparison Mode)**: `comparison_mode_toggle_ui` fixed (persona IDs, tier gate, placed in `theater_header`). `_make_cmp_baseline_handler` registered per plot. `dynamic_tabs` reads `input.comparison_mode`: 2-column T2 baseline vs T3 adjusted layout when ON in T3 tier.
- **Phase 21-G (Sidebar suppression)**: Confirmed already done — `hidden_personas` set in `right_sidebar_content_ui` is correct.
- **Phase 21-H (Headless verification)**: `app/tests/debug_home_theater.py` — 76/76 PASS, 10 test sections, all 5 personas.

---

## Files Changed (Sessions 7–8)

- `app/handlers/home_theater.py` — Phase 21-E comparison mode
- `app/modules/orchestrator.py` — three-path materialization + join-key normalisation
- `app/modules/wrangle_studio.py` — field cards, collapsible live view, Path import
- `app/src/server.py` — stale cache guards removed; Mode B plot upstream
- `app/tests/debug_home_theater.py` — Phase 21-H script (NEW)
- `.antigravity/knowledge/architecture_decisions.md` — ADR-043/044 IMPLEMENTED; ADR-050 added
- `.antigravity/knowledge/persona_traceability_matrix.md` — fully rewritten (current state)
- `.antigravity/knowledge/manifest_data_contract_rules.md` — §11–14 added
- `.antigravity/knowledge/handoff_session7.md` — created
- `.antigravity/knowledge/handoff_session8.md` — created
- `.antigravity/tasks/tasks.md` — Phase 21-E/G/H marked complete
- `EVE_WORK/notes/cheatsheat.md` — persona launch commands + capability matrix

---

## Next Steps (Priority Order)

| # | Item | Notes |
|---|---|---|
| 1 | **22-J Live-UI test** | User runs `tasks_test_22J.md` checklist in the running app |
| 2 | **ST22 Lineage 2** | Plasmid Dynamics manifest — enables T2/T3 comparison data |
| 3 | **Phase 23-A** | Bootloader `SPARMVET_PROFILE` env var resolution chain |
| 4 | **Phase 21-F-5** | T3 recipe YAML serialization stub |
| 5 | **Blueprint aesthetics** | TubeMap tighter look, ref→Add rename |

---

## Key Conventions (Do Not Break)

- Persona IDs: **hyphens** (`pipeline-exploration-advanced`). Underscores silently fail all gates.
- `make_recipe_node(node_type, params={...}, ...)` — `params` is a dict, not keyword args.
- `DataAssembler` first ingredient = base frame. Orchestrator MUST preserve `ingredients:` declaration order.
- No `if not out_p.exists()` guards on materialization calls. DataAssembler hash-check handles caching.
- `t3_recipe_by_plot: dict[plot_subtab_id, list[RecipeNode]]` — per-plot stacks since Phase 22-J.
- `comparison_mode` toggle only visible for advanced+ personas AND when `tier_toggle == "T3"`.
