---
trigger: always_on
deps:
  provides: [rule:persona_flags, rule:feature_dependencies]
  documents: [config/ui/templates/, app/modules/persona_manager.py, app/src/bootloader.py]
  consumed_by: [.antigravity/knowledge/dependency_index.md]
---

# Persona Feature Flags — Authoritative Reference

This document is the single source of truth for all persona feature flags, their groupings, dependency chains, and the consequences of misconfiguration. It governs `config/ui/templates/*.yaml` and the `PersonaManager`.

---

## Flag Groups and Dependency Chains

Flags are grouped by dependency. Enabling a flag in a group without its parent gate has **no effect** — the feature will not appear. This is enforced by `PersonaManager` at bootload: it resolves effective flags after applying dependency rules, and logs a warning for any flag enabled without its dependency.

### Group A — Viewing (no dependencies)

These flags are always meaningful regardless of any other flag.

| Flag | Default (static) | Effect when true |
|---|---|---|
| `export_bundle_enabled` | `true` | Export Results Bundle zip available in System Tools |

No dependencies. Safe to enable in any persona.

---

### Group B — T3 Sandbox

`interactivity_enabled` is the **master gate**. If it is `false`, all flags in this group are silently suppressed regardless of their individual values.

```
interactivity_enabled: true/false   ← MASTER GATE for all below
  │
  ├─ comparison_mode_enabled        ← Comparison Mode toggle in theater
  ├─ session_management_enabled     ← Session Save/Import + ghost save
  └─ export_graph_enabled           ← Export Active Graph (single plot)
```

**Dependency rule:** `PersonaManager` ignores `comparison_mode_enabled`, `session_management_enabled`, and `export_graph_enabled` when `interactivity_enabled: false`. Setting them to `true` in a static persona produces no UI effect and logs a warning.

**Structural consequence:** When `interactivity_enabled: false`, the T3 Tier Toggle buttons (T3-Wrangle, T3-Plot) are absent. The T3 recipe still silently pre-fills from T2 to protect plot rendering — but this is internal and invisible to the user.

**Right sidebar:** Not flag-controlled. Suppressed structurally (layout element excluded, not CSS-hidden) for `pipeline-static` and `pipeline-exploration-simple`. The persona level itself determines this — no flag needed.

---

### Group C — Data Ingestion

`import_helper_enabled` is the **master gate** for general data ingestion. `metadata_ingestion_enabled` is **semi-independent** (see note).

```
import_helper_enabled: true/false   ← MASTER GATE for data_ingestion
  │
  └─ data_ingestion_enabled         ← Multi-file upload, Excel converter, schema association

metadata_ingestion_enabled: true/false   ← SEMI-INDEPENDENT (see below)
```

**`metadata_ingestion_enabled` semi-independence:**
- When `import_helper_enabled: false` AND `metadata_ingestion_enabled: true`: metadata upload appears as a **standalone control** in System Tools (no general data ingestion panel).
- When `import_helper_enabled: true` AND `metadata_ingestion_enabled: true`: metadata upload is nested inside the general ingestion panel.
- When both are `false`: no ingestion controls shown.

**Deployment override:** The deployment profile can set `data_ingestion_enabled: false` to suppress the entire data ingestion section regardless of persona flags. This is for automated-pipeline deployments where data is always pushed by the pipeline. `metadata_ingestion_enabled` is **not** overridden by the deployment profile — correcting metadata is always a legitimate user action.

---

### Group D — Developer Features

`developer_mode_enabled` is the gate for Dev Studio and the full registry.

```
developer_mode_enabled: true/false   ← GATE for Dev Studio
  │
  └─ Dev Studio access (Wrangle Studio, AquaSynthesizer)
  └─ Full @register_action registry in right sidebar

gallery_enabled: true/false          ← INDEPENDENT (can enable without developer mode)
```

`gallery_enabled` can be set independently — a `project-independent` persona could have Gallery access without full developer mode. Currently set to `false` for all non-developer personas, but this is a policy choice, not a technical constraint.

---

## Full Flag Matrix (Authoritative Values)

| Flag | static | simple | advanced | independent | developer |
|---|:---:|:---:|:---:|:---:|:---:|
| `interactivity_enabled` | false | true | true | true | true |
| `wrangle_studio_enabled` | false | true | true | true | true |
| `comparison_mode_enabled` | false | true | true | true | true |
| `session_management_enabled` | false | true | true | true | true |
| `export_bundle_enabled` | true | true | true | true | true |
| `export_graph_enabled` | false | false | true | true | true |
| `metadata_ingestion_enabled` | false | false | true | true | true |
| `import_helper_enabled` | false | false | false | true | true |
| `data_ingestion_enabled` | false | false | false | true | true |
| `developer_mode_enabled` | false | false | false | false | true |
| `gallery_enabled` | false | false | false | false | true |

---

## What PersonaManager Must Enforce

When loading a persona template, `PersonaManager` applies these resolution rules before exposing effective flags to the rest of the app:

1. If `interactivity_enabled == False`:
   - Force `comparison_mode_enabled = False`
   - Force `session_management_enabled = False`
   - Force `export_graph_enabled = False`
   - Log WARNING for each that was set to `True` in the template.

2. If `import_helper_enabled == False`:
   - Force `data_ingestion_enabled = False`
   - Log WARNING if `data_ingestion_enabled` was `True`.

3. If deployment profile sets `data_ingestion_enabled: false`:
   - Override persona `data_ingestion_enabled` to `False`.
   - Do NOT override `metadata_ingestion_enabled`.

4. Right sidebar suppression: enforced structurally in `server.py` / `ui.py` based on persona level string comparison — not via a flag.

**All effective (resolved) flags are accessible via `PersonaManager.get_feature(flag_name: str) -> bool`.**

---

## Consequences of Misconfiguration

| Misconfiguration | Symptom | Fix |
|---|---|---|
| `comparison_mode_enabled: true` with `interactivity_enabled: false` | Comparison Mode toggle absent (silently suppressed). No error shown to user. | PersonaManager resolves and logs warning. Fix the template. |
| `data_ingestion_enabled: true` with `import_helper_enabled: false` | Data ingestion UI absent. No Excel converter. | PersonaManager resolves and logs warning. Fix the template. |
| `default_manifest` absent in profile AND persona hides selector | App fails to start with ConfigurationError: "No manifest source available." | Add `default_manifest` to profile, or use a persona that shows the selector. |
| `data_ingestion_enabled: false` in profile with `project-independent` persona | Data Ingestion section suppressed in System Tools. Metadata upload still available (not overridden). | Expected behaviour for auto-pipeline deployments. |
| `SPARMVET_IRIDA_TOKEN` not set with `deployment_type: irida` | IridaConnector raises AuthenticationError at startup. | Ensure IRIDA injects the token at container launch. |

---

## Files Governed by This Rule

| File | Governed aspect |
|---|---|
| `config/ui/templates/*_template.yaml` | Flag values per persona |
| `app/modules/persona_manager.py` | Flag resolution logic (dependency enforcement) |
| `app/src/bootloader.py` | Persona loading, deployment profile resolution |
| `app/handlers/home_theater.py` | Reads `PersonaManager.get_feature()` to show/hide UI sections |
| `app/src/ui.py` | Right sidebar layout suppression (structural, not flag-based) |
