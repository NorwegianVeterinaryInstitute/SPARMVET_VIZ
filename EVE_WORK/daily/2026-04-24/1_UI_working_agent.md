---

## Conditional UI Logic — Architectural Clarification

Here is how I understand your intent, and the open questions that need decisions before any implementation:

---
> Here is how I understand your intent, and the open questions that need decisions before any implementation
### 1. Project Navigator — Manifest Selection (1.1)
- **Current state**: Manifest import is in Blueprint Architect (developer/advanced). Home always loads from a pre-selected manifest context.
- **Your intent**: Make manifest selection **persona-gated**:
	- `developer` / `project_independent`: Can browse and select manifests freely
	- Lower personas (`pipeline_static`, `pipeline_exploration_simple`): Manifest is **fixed** — tied to a pipeline, not user-selectable

==**Open question**: Where does the "pipeline → manifest" association live? Options:==

- A) In the connector YAML (`local_connector.yaml`) — `default_manifest: path/to/manifest.yaml`
- B) In the persona/UI template YAML — persona declares its default manifest
- C) Combination: persona picks a pipeline profile, which resolves to a manifest path

**My recommendation**: B — persona template declares `default_manifest`. This keeps the persona self-contained and means swapping persona = swapping pipeline without touching the connector.

**"Other data" flow** (user selects non-default data): This is a significant new feature — user picks a file/directory, associates it with a schema, triggers ingestion. This is **distinct from the current ingestion flow** (which assumes pre-configured paths). This should be scoped as a **Phase 22+ feature** rather than a current blocker.

---

### 2. Metadata Ingestion (1.2)

**Your intent**: Allow uploading updated metadata (partial update — must conform to minimal fields contract). Persona-dependent but broadly available.

**Open questions**:

- Is this a **replacement** (full re-ingest) or an **overlay** (join new metadata onto existing T1)?
- Where does the updated metadata land in the tier model? (Likely re-triggers T1 rebuild via `DataAssembler`)
- Should `MetadataValidator` gate this upload against `input_fields` contract before accepting?

**My recommendation**: Treat as an overlay — upload triggers a partial re-ingest where the new metadata replaces/merges the metadata source in the manifest. Gate with `MetadataValidator`. This is also a **Phase 22+ feature** unless you need it now.

---

### 3. System Tools — Export (2.1)

**Already implemented** (Phase 21-I). Two clarifications to resolve:

**3a. Name field** — Already sanitized with `re.sub(r"[^A-Za-z0-9_-]", "_", raw_name)`. This is correct per your spec (no spaces, no special chars). Label in UI says "Your name (no spaces)" — should we change the label to "Bundle label / name" to make it clearer it's not a username?

**3b. Layout overlap** — You noted the Web/Publication selector overlaps with the Export Bundle button. This is a CSS/layout fix. The radio buttons need more bottom margin or the download button needs a `margin-top`. Minor, can fix now.

**3c. Export active graph** (new feature request):

- Export single active plot (SVG/PNG) + its recipe fragment + the active filters
- **Persona-gated**: available for ≥ `pipeline_exploration_simple` (everyone who can see plots) or higher?
- This is a new `@render.download` handler scoped to the active sub-tab's `plot_id`

**3d. Export location selector**: Default = Location 4 (from connector). Option to choose local PC = browser download (already how `@render.download` works — it downloads to the browser's download folder, which IS the local PC). If "Location 4" means server-side save (not browser download), this is a distinct server-write path. **Which do you mean?**

---

### 4. Import / Save Session (2.2)

**Your intent**: Rename "Restore Last Session" → "Import / Save Session". Save location = from connector (Location 4 subdirectory, persona-specific).

**Clarification needed**: Is this still deferred, or should we spec it now? The ghost-save mechanism (auto-save on change) is still deferred per ADR-047. Manual save/import is the immediate need.

---

### 5. Data Ingestion (2.3)

**Your intent**: Advanced+ persona only. Supports:

- Full manifest ingestion (dir or multiple files, + button for multi-file)
- Data types: raw data / metadata / extra data — user associates file with manifest role
- Excel → TSV converter as a utility within System Tools

**Key decision**: **Where does the Excel converter live?**

- Option A: System Tools (your suggestion) — available to any persona with data ingestion access
- Option B: Dev Studio — developer-only
- My read of your intent: System Tools, available to personas who have data ingestion access (so advanced+). This makes sense — it's a practical utility for scientists who receive Excel files, not a developer feature.

**Excel converter flow**: User uploads `.xlsx` → system shows sheet names → user assigns each sheet to a role → converter writes TSVs to the user's accessible directory (Location 4). The `ExcelHandler` already exists at `libs/ingestion/src/ingestion/excel_handler.py` — this is a UI wrapper around it.

---

### 6. Filters — Panel Context (Dev Studio)

**Your intent**: In Dev Studio / Blueprint Architect mode, the left sidebar filters are **not applicable**. Filters are a **Home mode-only feature**. The left panel content must be **panel-context-dependent** — different panels show different left sidebar content.

**Current state**: The filter widgets are scoped to Home mode already in the code (`sidebar_filters` only renders in Home). But this needs to be **explicitly formalized in the contract**: the left sidebar has a different content specification per active panel:

|Active Panel|Left Sidebar Content|
|---|---|
|Home|Project Navigator + Filter Recipe Builder + System Tools|
|Blueprint Architect|Manifest/component navigation (current)|
|Gallery|Focus Mode (ADR-038) — operation controls hidden|
|Dev Studio|TBD — what goes here?|

**Open question**: What does the **Dev Studio left sidebar** show? Schema browser? Action registry? This needs speccing before Phase 22.

---

### Summary: What needs a decision now vs. later

|Item|Decision needed?|Implementation timing|
|---|---|---|
|Manifest fixed vs. selectable per persona|**Yes — where does default_manifest bind?**|Phase 22|
|"Other data" custom ingestion|No — Phase 22+|Phase 22+|
|Metadata upload/overlay|**Yes — replacement or overlay?**|Phase 22|
|Export name label change|No — label tweak|Now (trivial)|
|Layout overlap fix|No — CSS fix|Now (minor)|
|Export active graph|**Yes — which personas?**|Phase 22|
|Export location (browser vs server-side)|**Yes — clarify**|Phase 22|
|Session save/import|No — still deferred|Phase 22|
|Data ingestion (advanced+)|No — already scoped|Phase 22|
|Excel → TSV converter location|**Resolved: System Tools, advanced+**|Phase 22|
|Filters = Home-mode only|No — already coded, formalize in contract|Now (doc only)|
|Dev Studio left sidebar content|**Yes — needs spec**|Before Phase 22|

---

**What I'd like to do now** (pending your answers):

1. **Update `ui_implementation_contract.md`** to formalize the left sidebar panel-context dependency and the persona → manifest binding model (with your chosen approach)
2. **Fix the minor CSS layout overlap** in System Tools
3. **Fix the export name field label** if you want it changed
4. **Mark Phase 22 features** in tasks.md so they're tracked

Shall I proceed with the doc update + CSS fix while you answer the open questions? Or do you want to answer everything first?


# **All open questions answered and documented:**

| #    | Question               | Decision                                                                                                   | Where recorded            |
| ---- | ---------------------- | ---------------------------------------------------------------------------------------------------------- | ------------------------- |
| 1.1  | Manifest selection     | Deployment profile (`default_manifest`), not persona                                                       | ADR-048 (Session Block 1) |
| 1.2  | Metadata ingestion     | Full replacement → MetadataValidator gate → T1 rebuild; provenance filename in export                      | §9 of contract            |
| 2.1a | Export label           | "Bundle label / name" (minor code fix pending)                                                             | §7.2 of contract          |
| 2.1b | Layout CSS overlap     | Radio buttons need margin-bottom fix (pending)                                                             | Audit log                 |
| 2.1c | Export active graph    | ≥ `pipeline_exploration_advanced`, deferred Phase 22                                                       | §7.3 of contract          |
| 2.1d | Export location        | Browser download for all deployments; server-side write deferred                                           | §7.2 of contract          |
| 2.2  | Session save/import    | Named sessions in Location 4; ghost save `_autosave.json`; multiple sessions per user; deferred Phase 22   | §7.1 of contract          |
| 2.3  | Data ingestion + Excel | System Tools, `data_ingestion_enabled`, deactivatable per deployment; sheet→role→schema; deferred Phase 22 | §10 of contract           |
| 6    | Dev Studio sidebar     | TBD — deferred to Dev Studio design session                                                                | §11 of contract           |

**All 5 persona templates** updated with the three new flags: `export_graph_enabled`, `metadata_ingestion_enabled`, `data_ingestion_enabled`.

The two pending minor code fixes (label rename + CSS margin) are ready to implement whenever you want — they are small and self-contained.
