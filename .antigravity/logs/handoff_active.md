# Handoff — Active State (2026-04-30, Session 10)

**Branch:** dev
**Last commit:** `283207c` docs+test: filter operator contract — regression suite + user docs + ADR amendment
**Active agent:** @dasharch (Claude Sonnet 4.6)

---

## Current State

Phase 21 complete. Phase 22 implemented; **22-J live-UI test §1 PASSED 2026-04-30** (core per-plot scoping validated). Phase 23-A + 23-B complete. **Monday demo blockers DEMO-1..DEMO-4 all RESOLVED.** Filter pipeline contract is locked down by 21 regression tests, user docs are updated, ADR-049 amendment recorded. App is in solid shape for the Monday demo.

---

## What Was Done (Session 10)

### Demo blockers — all fixed and committed individually for safe rollback

| ID | Commit | What |
|---|---|---|
| **DEMO-1** | `55ab1c5` | viz_factory auto-rotation log KeyError on short-label branches (Virulence Variants plot) |
| **DEMO-2** | `b91dfc9` + `33afa1b` | Quast unpivot moved tier2→tier1 + register `boxplot_logic` factory_id (Assembly Quality dotplot) |
| **DEMO-3** | `4c962e6` | `_apply_filter_rows` reads actual column dtype from LF schema, coerces string operands |
| **DEMO-4** | `8b4f3a4` | viz_factory plot filter loop — same dtype-aware coercion (was the actual MLST year>2022 fix) |
| **BUG-CACHE-1** | `09366fc` | DataAssembler cache hash now includes upstream provenance (manifest_sha256 + data_batch_hash). Edits to TSVs / manifests now invalidate the parquet automatically. |
| **DATA-1** | `4133159` | Quast/FastP/Bracken/Quality_metrics test TSVs realigned to use canonical metadata sample_ids (was zero overlap) |

### Filter pipeline overhaul (UX-FILTER-1, AUDIT-1, PROP-1)

| ID | Commits | What |
|---|---|---|
| **UX-FILTER-1** | `f08b88f` `61e86a8` `f4b1a91` `5c5083f` | Dtype-aware filter widgets. Numeric scalar ops → `ui.input_numeric`. New `between` op → two numeric inputs (was a slider initially; replaced because of render-glitch + locale separator + imprecise input). Inclusivity toggle for `between`: `≤ ≤ inclusive` (default) or `<  < exclusive` → `closed='both'` / `closed='none'`. fb_op dropdown now preserves selection across re-renders (was resetting). |
| **AUDIT-1** | `3c6195f` | ADR-049 amendment: PK-column filtering ALLOWED (no more silent conversion to exclusion_row). Operator is the truth, PK warning is the safety rail. ADR-049a added in `architecture_decisions.md`. |
| **PROP-1** | `b4dcd10` | Propagation modal now shows per-plot column-presence preview BEFORE the user confirms. Three states: ✅ apply / ⚠️ skip (col missing) / ❓ unknown. Encourages "apply one at a time" workflow. |

### Cosmetic / structural

| Description | Commits |
|---|---|
| Cat 🐱 group + miaou violin plot | `f2b7fba` `97506e9` `b74e985` |
| Generalised id sanitiser (any unicode/emoji in group labels) | `7adc48a` `d9d3406` |
| Categorical→String cast before `.str` ops in AMR_Profile_Joint | `beb4b72` |
| Filter operator regression test (21 cases) + user docs | `283207c` |

---

## Documentation Updated

- `docs/user_guide/audit_pipeline.qmd` — Propagation preview section, PK-filter-allowed section, full filter operators reference appendix.
- `.agents/rules/ui_implementation_contract.md` §12g.3 — PK filter table updated.
- `.antigravity/knowledge/architecture_decisions.md` — ADR-049a (2026-04-30 PK amendment).
- `.agents/rules/rules_manifest_structure.md` §8 — Emoji/icon support in group labels (from earlier session).

---

## Test Coverage

| Suite | Count | Path |
|---|---|---|
| Filter operators (NEW this session) | 21 | `app/tests/test_filter_operators.py` |
| Connector library | 31 | `libs/connector/tests/test_connectors.py` |

Run all: `PYTHONPATH=. .venv/bin/python -m pytest app/tests/test_filter_operators.py libs/connector/tests/`

---

## Next Steps (Priority Order)

| # | Item | Notes |
|---|---|---|
| 1 | **22-J Live-UI test continued** | Sections 3–9 now testable (PK filter unblocked, types fixed). Walk through `tasks_test_22J.md` with current build. |
| 2 | **AUDIT-2** | Filter→audit operator translation correctness (UI says "exact France" → audit says "any of [France]" — verify single-value selectize→eq path is faithful) |
| 3 | **AUDIT-4** | Compare T2/T3 toggle does not hold state on plot switch — reactive scoping bug |
| 4 | **UX-1..5** | Polish (data preview column-selector width, header visibility, button rename "Send to Audit", trash icon homogenisation) |
| 5 | **BUG-PERF-1** | Wire `SessionManager.restore_t1t2()` fast-path into `home_theater.py:545` (orchestrator currently fires every project switch but DataAssembler short-circuits) |
| 6 | **PROP-4** | Documentation: write user-guide section on propagation rules + screenshots (PROP-1 is in, ready to be documented) |
| 7 | **PROP-2** | Filter inventory panel showing effective filters per plot (enhancement) |
| 8 | **PROP-3** | TubeMap propagation visualisation (enhancement, exploratory — own ADR/design pass) |
| 9 | **NAV-1..6 / TOOLS-1..5** | Left sidebar restructure (Data Navigator, System Tools split) |
| 10 | **Phase 24-A** | `t3_recipe_engine.py` extraction (gate now MET, but lower priority than UX work) |

---

## Key Conventions (Do Not Break)

- **Filter operator contract is now locked down** by `app/tests/test_filter_operators.py`. Any changes to `_apply_filter_rows` (home_theater.py) OR `viz_factory.py` filter loop must keep these tests green.
- **The two filter paths must agree.** Production has TWO filter implementations (data preview + plot render). They must produce identical results for the same filter row, otherwise UI inconsistency. The regression test mirrors both.
- **`closed=` field on `between` filter rows**: 'both' (default) or 'none'. Anything else triggers a defensive fallback to 'both' in `_filter_add_row`.
- **PK filter is ALLOWED** (AUDIT-1 / ADR-049a). Don't reintroduce the `if is_pk: node_type = "exclusion_row"` silent-conversion branch in `home_theater.py`.
- **Cache invalidation is upstream-aware** (BUG-CACHE-1). The orchestrator injects `upstream_provenance` (manifest_sha256[:16] + data_batch_hash[:16]) into the sink_parquet step. Don't strip it via the `__`-prefix purge.
- **Group labels can use any unicode**, plot ids must be snake_case (registration contract). `_safe_id()` in home_theater.py handles internal IDs; visible labels come from `label:`/`description:` fields.
- **Persona IDs use hyphens** (`pipeline-exploration-advanced`); underscores silently fail all gates.
- **Numeric filter widgets emit native types**; the defensive coercion in both filter paths logs `[filter] ⚠️ string operand…` if a string sneaks in. Treat that warning as a bug signal.

---

## App Status (Monday demo)

- App imports clean (`from app.src.main import app`)
- 52/52 tests pass (21 filter + 31 connector)
- All 4 demo blockers resolved + cache correctness fixed
- Filter UI: dtype-aware widgets, between with inclusivity toggle, propagation preview
- Documentation: audit pipeline guide updated end-to-end

Recommended demo path: `1_test_data_ST22_dummy` → walk through QC group → show miaou cat violin → demonstrate audit pipeline (filter year between 2022–2024, exclude S2 from one plot, etc.) → export bundle.


---

# Handoff — Demo state (2026-04-30, end of Session 11)

**Last commit:** `870f0e6` (refactor PERSONA-1a) + post-handoff: PERSONA-2 + DATA-2 + log + this handoff.

## Demo readiness

✅ App imports clean. 90/90 pytest pass. All 4 Monday-demo blockers fixed (DEMO-1..4) plus cache correctness (BUG-CACHE-1) plus test-data alignment (DATA-1).

**Demo path recommendation**: launch with `SPARMVET_PERSONA=developer`, load `1_test_data_ST22_dummy`. Walk through:
1. QC group → demonstrate plots rendering (Virulence Variants + Assembly Quality dotplot now work)
2. Cat 🐱 group → miaou violin shows assembly metrics by source
3. Filter UI → dtype-aware widgets, between with inclusivity toggle, audit propagation preview
4. Toggle T1 ↔ T2 on a MLST-related plot → visible difference (era column + year filter)
5. Export Bundle → comprehensive ZIP

**Known issues to acknowledge during demo (non-blocking)**:
- T3 toggle / panel-switch causes plot flicker (STATE-1/2)
- Compare T2/T3 button doesn't hold (AUDIT-4 = STATE-2)
- Notifications disappear too fast (UX-NOTIF-1 — bell button design queued)
- Single-graph export not wired (EXPORT-1, deferred from Phase 22)

## Personas available

| Persona | Use |
|---|---|
| `developer` | Full feature surface — for the demo |
| `project-independent` | Advanced + data ingestion |
| `pipeline-exploration-advanced` | T3 audit, no data ingestion |
| `pipeline-exploration-simple` | Filtering only, no T3 audit authoring |
| `pipeline-static` | Read-only |
| `qa` (NEW, PERSONA-2) | All flags ON + ghost_save OFF — for automated UI tests |

## Test commands

```bash
# Quick (sub-second, run before every commit)
PYTHONPATH=. ./.venv/bin/python -m pytest libs/ app/tests/ -q

# Long (full PNG render audit)
PYTHONPATH=. ./.venv/bin/python libs/viz_factory/tests/viz_factory_integrity_suite.py --output_dir tmp/viz_factory/

# Long (transformer assembler audit)
PYTHONPATH=. ./.venv/bin/python libs/transformer/tests/transformer_integrity_suite.py --output_dir tmp/transformer/
```

## Open priorities for next session (post-demo)

1. **STATE-1/STATE-2 + AUDIT-4**: trace the reactive scoping bug — active plot subtab is being reset by toggle effects somewhere
2. **UX-NOTIF-1 (bell button)**: persistent alert log in right sidebar
3. **PERSONA-1b**: resolve doc-drift on `simple` persona's Comparison/Session Mgmt visibility
4. **Phase 24-A**: extract `t3_recipe_engine.py` (the safe pure-function piece of the home_theater split)
5. **EXPORT-1**: wire the deferred single-plot export

## Files most likely to bite next agent

- `app/handlers/home_theater.py` (~3000 lines now, refactor pending — Phase 24)
- Any change to filter logic must keep `app/tests/test_filter_operators.py` (21 cases) green
- Cache invalidation: do NOT remove `upstream_provenance` from sink_parquet step in `app/modules/orchestrator.py:materialize_tier1` — that's BUG-CACHE-1's keystone

## Conventions enforced

- Persona IDs: HYPHENS only (`pipeline-exploration-advanced`, never underscores)
- Filter widgets emit native types; coercion in apply paths is defensive (logs `[filter] ⚠️` if string sneaks in on numeric column)
- Group labels accept any unicode (`_safe_id()` sanitises internal IDs); plot ids must be snake_case
- Cache hash includes upstream_provenance (BUG-CACHE-1) — manifest/TSV edits invalidate parquet
