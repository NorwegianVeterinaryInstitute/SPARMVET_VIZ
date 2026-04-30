# Handoff — Active State (2026-04-30, Session 9)

**Branch:** dev  
**Last commit:** `0412888` docs: update connector README, add config/deployment and assets/scripts READMEs  
**Active agent:** @dasharch (Claude Sonnet 4.6)

---

## Current State

Phase 21 complete. Phase 22 implemented (22-J live-UI test still pending — user must run). Phase 23-A and 23-B complete. Documentation pass done. **Home Theater split (Phase 24) is designed but gated** — do not implement until 22-J live-UI test passes.

---

## What Was Done (Session 9)

### Phase 23-B: Connector Library — COMPLETED

Four connector classes implemented in `libs/connector/src/connector/`:

- `base.py` — `BaseConnector` ABC
- `filesystem.py` — `FilesystemConnector` (no-op fetch, project_root-aware path resolution)
- `galaxy.py` — `GalaxyConnector` (falls back to `_GALAXY_JOB_HOME_DIR` env var)
- `irida.py` — `IridaConnector` (validates `SPARMVET_IRIDA_TOKEN` + irida block; `fetch_data()` stub for Phase 23-D)
- `__init__.py` — public API + `get_connector(profile)` factory

`libs/connector/tests/test_connectors.py`: 31 tests, all passing. In-memory profiles, no filesystem access.

Full app import: clean.

### Documentation Pass

- `docs/workflows/connector.qmd` — removed stale "rename pending" section (rename was done in 23-A); fixed level-4 path; updated component table with real file paths; updated dev fallback snippet.
- `libs/connector/README.md` — rewritten: was "Phase 23 pending", now reflects completed 23-B reality with usage examples.
- `config/deployment/README.md` — NEW: profile resolution table, deployment types, schema pointer.
- `assets/scripts/README.md` — NEW: all 12 scripts documented with purpose.
- H-2 audit (`assets/scripts/`): all 12 scripts are correctly placed; no moves needed. `materialize_manifest_plots.py` is an intentional shim. `SF_create_manifest.py` is a simpler schema-only variant (keep).

---

## Commits This Session

```
0412888  docs: update connector README, add config/deployment and assets/scripts READMEs
95894c8  docs(23-E): update connector.qmd for Phase 23-A/B reality; mark H-2 done
9301bdb  docs(23-B): update STATUS and log after connector library commit
3cdbdd6  feat(23-B): connector library — BaseConnector, Filesystem, Galaxy, Irida + 31 tests
```

---

## Next Steps (Priority Order)

| # | Item | Notes |
|---|---|---|
| 1 | **22-J Live-UI test** | User runs `tasks_test_22J.md` checklist in the running app — **gates Phase 24** |
| 2 | **ST22 Lineage 2** | Plasmid Dynamics manifest — enables T2/T3 comparison data |
| 3 | **Phase 23-C** | Galaxy XML tool wrapper templates (`tool_amr_pipeline.xml`); bundle profile YAMLs; Galaxy admin docs |
| 4 | **Phase 23-E (partial)** | Per-system admin quick-start guides (Galaxy / IRIDA / server / local) |
| 5 | **Phase 21-F-5** | T3 recipe YAML serialization stub (UI exists, backend not wired) |
| 6 | **Phase 24-A** | `t3_recipe_engine.py` extraction — GATED on 22-J + ST22 Lineage 2 |
| 7 | **Blueprint aesthetics** | TubeMap tighter look, ref→Add rename |

---

## Key Conventions (Do Not Break)

- Persona IDs: **hyphens** (`pipeline-exploration-advanced`). Underscores silently fail all gates.
- `make_recipe_node(node_type, params={...}, ...)` — `params` is a dict, not keyword args.
- `DataAssembler` first ingredient = base frame. Orchestrator MUST preserve `ingredients:` declaration order.
- No `if not out_p.exists()` guards on materialization calls. DataAssembler hash-check handles caching.
- `t3_recipe_by_plot: dict[plot_subtab_id, list[RecipeNode]]` — per-plot stacks since Phase 22-J.
- `comparison_mode` toggle only visible for advanced+ personas AND when `tier_toggle == "T3"`.
- Profile resolution chain documented in `project_conventions.md §4` and `bootloader.py` module header — check there first before investigating missing profiles.
- `libs/connector/` (singular) is the active package — not `libs/connectors/` (plural). The ADR says plural but the actual installed package is singular.
- Phase 24 (`home_theater.py` split): design in ADR-051. **Do not implement** until 22-J live-UI test passes.
