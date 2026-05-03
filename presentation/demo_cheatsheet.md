# SPARMVET_VIZ — Demo Cheatsheet (2026-05-04)

## Launch commands

```bash
# Developer persona — full features, Test Lab, Gallery
cd /home/evezeyl/Documents/Insync/gdrive/OBSWORK/20_GITS/SPARMVET_VIZ
export PYTHONPATH=$PYTHONPATH:.
SPARMVET_PERSONA=developer ./.venv/bin/python -m shiny run app/src/main.py --port 8001

# pipeline-static persona — to show persona contrast (read-only view)
SPARMVET_PERSONA=pipeline-static ./.venv/bin/python -m shiny run app/src/main.py --port 8002
```

## Key URLs

| What | URL / Path |
|---|---|
| App (developer) | http://localhost:8001 |
| App (pipeline-static) | http://localhost:8002 |
| Documentation | `_book/index.html` (open in browser) |
| Dependency graph | `assets/dep_graph.html` + `tmp/dep_graph.json` |
| Test project | `1_test_data_ST22_dummy` (select in project selector) |

---

## Demo walk-through (in order)

### 0. Before you start
- Open two terminals: one for developer persona (8001), optionally one for pipeline-static (8002)
- Open `_book/index.html` in a second browser tab
- Have `assets/dep_graph.html` ready in a third tab

---

### 1. Load the test project
- Open http://localhost:8001
- Project selector → pick **1_test_data_ST22_dummy**
- Wait for "Quality Control" tab to appear (T1 materialisation, ~10s on first load)
- **Point out**: the left sidebar accordion — Manifest Choice, Filters, Data Import, Global Project Export, Session Management

---

### 2. QC group → plots render
- Click **Quality Control** tab
- Show **Assembly Quality Dotplot** → coverage vs. contig N50 (DEMO-1 proof)
- Click **Virulence Variants** → dot plot for virulence gene presence (DEMO-2 proof)
- **Say**: "No code written for this specific pipeline — all driven by a YAML manifest"

---

### 3. Gallery (NEW — was not in original demo)
- Click **Gallery** in the left sidebar nav
- Browse the 34 recipes — show 6-axis taxonomy sidebar filters (Family, Pattern, Difficulty, Geom, Show, Sample size)
- Filter to **Distribution** + **2 Categorical** → shows bar/heatmap recipes
- Click a recipe → show the recipe card (preview image, guidance, metadata)
- **Say**: "This is the shared recipe library — scientists can browse what's possible and clone a recipe to their own manifest"

---

### 4. Cat 🐱 group → violin (fun slide)
- Navigate back to project → **Cat 🐱** group → **Miaou**
- Violin plot: assembly quality metric by predicted phenotype
- **Say**: "We added a Cat group to the test data so the demo has a violin plot for the boss"

---

### 5. Filters + propagation
- Expand **Filters** accordion in left sidebar
- Select column: **year**, operator: **gt (>)**, value: **2010** → Add Row
- **Propagate** → modal shows which plots have a `year` column (will apply) vs. which don't (will skip)
- Confirm → all compatible plots update
- **Say**: "Every filter action is logged. You can see what was done, when, and why."

---

### 6. T1 ↔ T2 toggle (on MLST plot)
- Navigate to **Results** → **MLST Bar**
- Toggle **T1 → T2** in the theater header
- Row count drops (wrangling filter applied); era column appears
- **Say**: "T1 is the raw pipeline output. T2 is the analysis-ready view after manifest-defined wrangling. T3 is your personal sandbox on top."

---

### 7. T3 audit trail — add a reason
- With a filter active, click the **Pipeline Audit** right sidebar
- Add a reasoning note in the text field: *"Removed pre-2010 isolates — likely sequenced under earlier protocol, different quality threshold"*
- **Say**: "This is the reproducibility argument. When you publish, you have a full audit trail of every decision with the reasoning. Not just 'I filtered year > 2010' but why."

---

### 8. Export bundle
- Open **Global Project Export** accordion
- Click Export → downloads ZIP with T1/T2/T3 data TSVs, full recipe YAML, audit trail, filter trace
- **Say**: "This ZIP is your methods section. Everything reproducible, citable."

---

### 9. Persona contrast (optional, if time allows)
- Switch to http://localhost:8002 (pipeline-static)
- **Point out**: no Filters accordion, no right sidebar, no Gallery — read-only view
- **Say**: "Same data, different persona. A Galaxy user sees a clean publication view. A developer sees the full sandbox."

---

### 10. Architecture (dep graph + docs)
- Open `assets/dep_graph.html` — show 117 nodes, 222 edges
- Point to the blue app nodes, yellow transformer nodes, green viz_factory nodes
- Open `_book/index.html` — show it's a proper documented system, not just code
- **Say**: "The system is designed to grow. Adding a new pipeline is adding a YAML file, not modifying Python."

---

## What to say if something crashes

```bash
# Clear T1 parquet cache (forces recompute)
rm -f tmp/*.parquet

# Restart with clean session state
rm -rf tmp/session_* && SPARMVET_PERSONA=developer ./.venv/bin/python -m shiny run app/src/main.py --port 8001
```
