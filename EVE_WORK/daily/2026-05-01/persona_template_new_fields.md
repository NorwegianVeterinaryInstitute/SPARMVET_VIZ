# New persona template fields — Phase 25 design

These fields need to be added to all `config/ui/templates/*_template.yaml` files
and validated by a new `PersonaValidator` at app startup.

## New `manifest_selector` section

Controls whether the user can switch manifests in the UI or gets a fixed one from config.

```yaml
manifest_selector:
  visible: true          # false = hide the Manifest Choice dropdown entirely
  fixed_manifest: null   # REQUIRED when visible=false. Path to the manifest YAML.
                         # Example: config/manifests/my_pipeline.yaml
                         # Ignored when visible=true.
```

| Persona | visible | fixed_manifest |
|---|---|---|
| pipeline-static | false | REQUIRED |
| pipeline-exploration-simple | false | REQUIRED |
| pipeline-exploration-advanced | true | null |
| project-independent | true | null |
| developer | true | null |
| qa | true | null |

**Validator rule:** if `manifest_selector.visible == false` then `manifest_selector.fixed_manifest` must be a non-null string pointing to an existing file.

---

## New `testing_mode` flag

Controls whether the app uses default test data paths from the manifest, or requires
data to be provided by the user / pipeline.

```yaml
testing_mode: true   # true  = use default test data defined in the manifest
                     # false = data must be passed by pipeline (automated) OR chosen by user (manual)
```

| Persona | testing_mode | Rationale |
|---|---|---|
| pipeline-static | false | Production pipeline — data injected automatically |
| pipeline-exploration-simple | false | Production pipeline |
| pipeline-exploration-advanced | true | Interactive exploration — use test data by default |
| project-independent | true | Independent analysis — use test data by default |
| developer | true | Development / testing |
| qa | true | Test harness — always use known test data |

**Behaviour when testing_mode=false:** Data Import panel shows active file/directory selector.
The user must provide data OR the pipeline must inject it before the app can assemble.

**Behaviour when testing_mode=true:** Data Import panel shows read-only display of the
test data paths from the manifest. Selector is hidden.

---

## Persona capability matrix (updated)

Adds two new capability columns: `passive_exploration` and `t3_audit`.

| Persona | passive_exploration | t3_audit | Blueprint | Gallery | Session | Export bundle | Export graph | Metadata upload | Data ingestion | Test Lab |
|---|---|---|---|---|---|---|---|---|---|---|
| pipeline-static | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ | ❌ | ❌ | ❌ | ❌ |
| pipeline-exploration-simple | ✅ | ❌ | ✅ | ❌ | ✅ | ✅ | ❌ | ❌ | ❌ | ❌ |
| pipeline-exploration-advanced | ✅ | ✅ | ✅ | ❌ | ✅ | ✅ | ⏳ | ✅ | ❌ | ❌ |
| project-independent | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ⏳ | ✅ | ✅ | ❌ |
| developer | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ⏳ | ✅ | ✅ | ✅ |
| qa | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ⏳ | ✅ | ✅ | ✅ |

**passive_exploration:** can apply filters and drop columns to explore the view (T1/T2 — plot updates temporarily, nothing saved, no audit trail).
**t3_audit:** can promote filters/drops to the T3 audit pipeline (right sidebar, propagation modal, reason gatekeeper, recipe export).
⏳ = deferred (Phase 22, Single Graph Export)

---

## Validator checks (PersonaValidator — new module)

At app startup, before `define_server()` is called:

1. If `manifest_selector.visible == false`: `manifest_selector.fixed_manifest` is a non-null path to an existing file.
2. If `testing_mode == false` and persona is not pipeline-static: at least one data source must be configured or injectable.
3. `persona_id` matches the filename (e.g. `pipeline-static_template.yaml` → `persona_id: pipeline-static`).
4. All known feature flags are present (no missing keys — use defaults if absent but warn).
