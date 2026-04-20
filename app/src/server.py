# app/src/server.py
from shiny import render, reactive, ui
import polars as pl
from pathlib import Path
from datetime import datetime
import pandas as pd
import shutil
import yaml
import os
import re
import json
import base64

# Authority: Library Sovereignty (ADR-003)
from app.src.bootloader import bootloader
from app.modules.orchestrator import DataOrchestrator
from utils.config_loader import ConfigManager
from viz_factory.viz_factory import VizFactory
from app.modules.wrangle_studio import WrangleStudio
from app.modules.dev_studio import DevStudio
from app.modules.gallery_viewer import gallery_viewer
from transformer.data_wrangler import DataWrangler
from transformer.lookup import lookup_anchor_rows
from app.modules.exporter import SubmissionExporter
from utils.errors import SPARMVET_Error
from viz_gallery.gallery_manager import GalleryManager
from utils.blueprint_mapper import BlueprintMapper
import zipfile


# ── Blueprint Architect: sibling-context map builder ─────────────────────────

def _build_sibling_map(manifest_path_str: str) -> dict:
    """Parse a master manifest WITHOUT resolving !include, then build a map:
      rel_path → {role, schema_id, schema_type, siblings: {input_fields, output_fields, wrangling}}

    Uses a non-resolving subclass of SafeLoader so !include tags are captured
    as plain strings instead of being followed to disk.
    """
    class _CapLoader(yaml.SafeLoader):
        pass

    _MARK = "\x00INC\x00"

    def _capture(loader, node):
        return f"{_MARK}{loader.construct_scalar(node)}"

    # Override any previously registered !include handler on the subclass
    _CapLoader.add_constructor("!include", _capture)

    try:
        raw = Path(manifest_path_str).read_text(encoding="utf-8")
        tree = yaml.load(raw, Loader=_CapLoader)  # noqa: S506 – controlled loader
    except Exception:
        return {}

    if not isinstance(tree, dict):
        return {}

    ctx: dict = {}

    def _inc(val):
        if isinstance(val, str) and val.startswith(_MARK):
            return val[len(_MARK):]
        return None

    def _extract_ingredients(block: dict) -> list:
        """Extract ordered dataset_id list from an ingredients block."""
        raw = block.get("ingredients", [])
        if not isinstance(raw, list):
            return []
        ids = []
        for item in raw:
            if isinstance(item, dict):
                did = item.get("dataset_id")
                if did:
                    ids.append(did)
            elif isinstance(item, str):
                ids.append(item)
        return ids

    def _slot(block: dict, key: str):
        """Return the value for a manifest key as either:
          - a rel_path string  (when value is an !include marker)
          - {"inline": <val>}  (when value is defined inline and non-empty)
          - None               (key absent or empty list/None)
        This means the context map captures BOTH file-linked and inline content.
        """
        raw = block.get(key)
        inc_rel = _inc(raw)
        if inc_rel:
            return inc_rel           # file-linked — a rel_path string
        # Inline: non-None, non-empty list, non-empty dict
        if raw is not None and raw != [] and raw != {}:
            return {"inline": raw}   # inline content — a dict sentinel
        return None

    def _register(section_type: str, schema_id: str, block: dict,
                  ingredients: list | None = None):
        if not isinstance(block, dict):
            return
        inp = _slot(block, "input_fields")
        out = _slot(block, "output_fields")
        wrn = _slot(block, "wrangling")
        rec = _slot(block, "recipe")
        con = _slot(block, "final_contract")

        effective_out = out or con
        effective_wrn = wrn or rec
        sib = {"input_fields": inp, "output_fields": effective_out,
               "wrangling": effective_wrn}
        ings = ingredients or []

        # Only register file-path strings as keys — inline dicts can't be dict keys
        # Assembly wrangling/recipe files get role="assembly" so the import handler
        # can render the multi-ingredient upstream accordion correctly.
        is_assembly = section_type == "assembly_manifests"
        wrn_role = "assembly" if is_assembly else "wrangling"

        def _reg_if_file(slot_val, role):
            if isinstance(slot_val, str):
                ctx[slot_val] = {"role": role, "schema_id": schema_id,
                                 "schema_type": section_type, "siblings": sib,
                                 "ingredients": ings}

        _reg_if_file(inp, "input_fields")
        _reg_if_file(out, "output_fields")
        _reg_if_file(con, "output_fields")
        _reg_if_file(wrn, wrn_role)
        _reg_if_file(rec, wrn_role)

    for section in ("data_schemas", "additional_datasets_schemas"):
        for sid, sdict in (tree.get(section) or {}).items():
            _register(section, sid, sdict)

    meta = tree.get("metadata_schema")
    if isinstance(meta, dict):
        _register("metadata_schema", "metadata_schema", meta)

    for aid, adict in (tree.get("assembly_manifests") or {}).items():
        ings = _extract_ingredients(adict) if isinstance(adict, dict) else []
        _register("assembly_manifests", aid, adict, ingredients=ings)

    # analysis_groups → plots: register each plot spec and optional pre_plot_wrangling
    for group_id, group_spec in (tree.get("analysis_groups") or {}).items():
        if not isinstance(group_spec, dict):
            continue
        for plot_id, plot_spec in (group_spec.get("plots") or {}).items():
            if not isinstance(plot_spec, dict):
                continue
            spec_rel = _inc(plot_spec.get("spec"))
            pre_wrn_rel = _inc(plot_spec.get("pre_plot_wrangling"))

            if spec_rel:
                ctx[spec_rel] = {
                    "role": "plot_spec",
                    "schema_id": plot_id,
                    "schema_type": "plots",
                    "group_id": group_id,
                    # target_dataset lives inside the spec file — resolved at load time
                    # pre_plot_wrangling rel_path stored so lineage chain can prepend it
                    "siblings": {"input_fields": None, "output_fields": None,
                                 "wrangling": pre_wrn_rel},
                    "ingredients": [],
                }

            # Register the pre_plot_wrangling file as its own navigable node
            if pre_wrn_rel:
                ctx[pre_wrn_rel] = {
                    "role": "plot_wrangling",
                    "schema_id": plot_id,
                    "schema_type": "plots",
                    "group_id": group_id,
                    # plot_spec sibling stored so the chain can continue forward
                    "siblings": {"input_fields": None, "output_fields": None,
                                 "wrangling": spec_rel},
                    "ingredients": [],
                }

    return ctx


def _build_lineage_chain(selected_rel: str, ctx_map: dict, target_ds_override: str | None = None) -> list[dict]:
    """
    Constructs an ordered list of components for the Lineage Rail.
    Strategy:
    1. From the selected node, walk *backward* to the earliest ancestor.
    2. Then walk *forward*.
    target_ds_override: optional ID to trigger plot ancestry lookup.
    """
    if selected_rel not in ctx_map:
        return []

    def _node(rel: str, is_active: bool) -> dict:
        e = ctx_map[rel]
        return {
            "rel": rel,
            "schema_id": e.get("schema_id", rel),
            "role": e.get("role", "unknown"),
            "label": e.get("schema_id", rel),
            "is_active": is_active,
        }

    # Build lookup indexes for fast traversal
    # schema_id → list of rels for that schema_id (different roles)
    by_schema: dict[str, list[str]] = {}
    for rel, e in ctx_map.items():
        sid = e.get("schema_id", "")
        by_schema.setdefault(sid, []).append(rel)

    # assembly schema_id → its assembly wrangling rel
    assembly_rels: dict[str, str] = {
        e["schema_id"]: rel
        for rel, e in ctx_map.items()
        if e.get("role") == "assembly"
    }

    # For each assembly schema_id, which plot specs reference it (via target_dataset)?
    # We can't read the plot spec files here (no inc_map), so we note plot_spec rels
    # and their group context — linking happens by schema_id match at display time.
    # Instead, walk forward from assembly via schema_id equality to plot_spec siblings.
    # plot_spec entries don't store target_dataset in ctx_map (it's inside the file).
    # So the chain stops at the assembly level unless we have the target_dataset.

    entry = ctx_map[selected_rel]
    role = entry.get("role", "unknown")
    schema_id = entry.get("schema_id", "")
    sib = entry.get("siblings", {})

    chain: list[dict] = []

    if role == "plot_wrangling":
        # Chain: [plot_wrangling, plot_spec]
        # siblings["wrangling"] stores the associated plot_spec rel_path
        spec_rel = sib.get("wrangling")
        chain = [_node(selected_rel, True)]
        if isinstance(spec_rel, str) and spec_rel in ctx_map:
            chain.append(_node(spec_rel, False))

    elif role == "plot_spec":
        # Chain: [Ancestors..., (pre_plot_wrangling)?, plot_spec(active)]
        target_ds = target_ds_override or entry.get("target_dataset")
        if target_ds:
            # Recursively find the "best" anchor/assembly node for this target
            origin_rels = by_schema.get(target_ds, [])
            priority = ["assembly", "output_fields", "wrangling", "input_fields"]
            best_origin = None
            for p in priority:
                match = [r for r in origin_rels if ctx_map[r]["role"] == p]
                if match:
                    best_origin = match[0]
                    break
            
            if best_origin:
                origin_chain = _build_lineage_chain(best_origin, ctx_map)
                for node in origin_chain:
                    node["is_active"] = False
                    chain.append(node)

        pre_wrn_rel = sib.get("wrangling")
        if isinstance(pre_wrn_rel, str) and pre_wrn_rel in ctx_map:
            chain.append(_node(pre_wrn_rel, False))
        chain.append(_node(selected_rel, True))

    elif role == "assembly":
        # Chain: [ingredient_wranglings..., assembly, ?plots]
        for ing_id in entry.get("ingredients", []):
            ing_rels = by_schema.get(ing_id, [])
            # Prefer the wrangling file for each ingredient
            wrn_rels = [r for r in ing_rels if ctx_map[r]
                        ["role"] == "wrangling"]
            for r in (wrn_rels or ing_rels[:1]):
                chain.append(_node(r, r == selected_rel))
        chain.append(_node(selected_rel, True))
        # Add downstream output_fields node if present
        out_rel = sib.get("output_fields")
        if isinstance(out_rel, str) and out_rel in ctx_map:
            chain.append(_node(out_rel, False))

    elif role == "output_fields":
        # Walk backward: find the wrangling/assembly sibling for the same schema_id
        # then build that chain with output_fields appended
        wrn_rels = [r for r in by_schema.get(schema_id, [])
                    if ctx_map[r]["role"] in ("wrangling", "assembly")]
        if wrn_rels:
            # Recurse on the wrangling node, then replace its is_active with False
            sub = _build_lineage_chain(wrn_rels[0], ctx_map)
            for node in sub:
                node["is_active"] = False
            chain = sub
            chain.append(_node(selected_rel, True))
        else:
            chain = [_node(selected_rel, True)]

    else:
        # input_fields or wrangling (Tier-1)
        # Chain: [input_fields, wrangling, ?assembly, ?output_fields]
        inp_rel = sib.get("input_fields")
        wrn_rel = sib.get("wrangling")
        out_rel = sib.get("output_fields")

        if isinstance(inp_rel, str) and inp_rel in ctx_map:
            chain.append(_node(inp_rel, inp_rel == selected_rel))
        if isinstance(wrn_rel, str) and wrn_rel in ctx_map:
            chain.append(_node(wrn_rel, wrn_rel == selected_rel))

        # Check if this schema_id is an ingredient in any assembly
        for asm_sid, asm_rel in assembly_rels.items():
            asm_entry = ctx_map[asm_rel]
            if schema_id in asm_entry.get("ingredients", []):
                chain.append(_node(asm_rel, False))
                asm_out = asm_entry["siblings"].get("output_fields")
                if isinstance(asm_out, str) and asm_out in ctx_map:
                    chain.append(_node(asm_out, False))
                # show first assembly only (branching handled by Rail UI)
                break

        if not chain:
            chain = [_node(selected_rel, True)]

        if isinstance(out_rel, str) and out_rel in ctx_map and not any(
                n["role"] in ("assembly", "output_fields") for n in chain):
            chain.append(_node(out_rel, False))

    # Deduplicate while preserving order
    seen: set[str] = set()
    deduped = []
    for node in chain:
        if node["rel"] not in seen:
            seen.add(node["rel"])
            deduped.append(node)

    return deduped


def _build_schema_registry(manifest_path_str: str,
                           includes_map: dict) -> dict:
    """Build a complete schema-level structural index of a manifest.

    Unlike _build_sibling_map (which indexes *file paths*), this maps:
      schema_id → {
        "schema_type": str,
        "input_fields":  str | {"inline": val} | None,
        "wrangling":     str | {"inline": val} | None,
        "output_fields": str | {"inline": val} | None,
        "ingredients":   list[str],        # assembly only
        "target_dataset": str | None,      # plot only (resolved from spec file)
        "group_id":      str | None,       # plot only
        "source":        dict | None,      # raw data source block
        "info":          dict | str | None,
      }

    Both !include references (stored as rel_path strings) and inline content
    (stored as {"inline": <value>}) are captured, giving a complete structural
    view of the manifest regardless of how authors have factored their YAML.
    """
    class _CapLoader(yaml.SafeLoader):
        pass

    _MARK = "\x00INC\x00"

    def _capture(loader, node):
        return f"{_MARK}{loader.construct_scalar(node)}"

    _CapLoader.add_constructor("!include", _capture)

    try:
        raw = Path(manifest_path_str).read_text(encoding="utf-8")
        tree = yaml.load(raw, Loader=_CapLoader)  # noqa: S506
    except Exception:
        return {}

    if not isinstance(tree, dict):
        return {}

    def _slot(val):
        """Convert a raw block value to either a rel_path, {"inline":<v>}, or None."""
        if val is None:
            return None
        if isinstance(val, str) and val.startswith(_MARK):
            return val[len(_MARK):]
        if val == [] or val == {}:
            return None
        return {"inline": val}

    def _extract_ingredients(block):
        raw = block.get("ingredients", []) if isinstance(block, dict) else []
        ids = []
        for item in (raw if isinstance(raw, list) else []):
            if isinstance(item, dict):
                did = item.get("dataset_id")
                if did:
                    ids.append(str(did))
            elif isinstance(item, str):
                ids.append(item)
        return ids

    def _resolve_target_dataset(spec_slot):
        """If spec_slot is a rel_path, read the file and extract target_dataset."""
        if spec_slot is None or isinstance(spec_slot, dict):
            return None
        abs_path = Path(includes_map.get(spec_slot, ""))
        if not abs_path.exists():
            return None
        try:
            content = yaml.safe_load(
                abs_path.read_text(encoding="utf-8")) or {}
            return content.get("target_dataset") if isinstance(content, dict) else None
        except Exception:
            return None

    reg: dict = {}

    def _add(schema_id, schema_type, block, group_id=None):
        if not isinstance(block, dict):
            return
        entry = {
            "schema_type":   schema_type,
            "input_fields":  _slot(block.get("input_fields")),
            "wrangling":     _slot(block.get("wrangling")),
            "output_fields": _slot(block.get("output_fields") or block.get("final_contract")),
            "recipe":        _slot(block.get("recipe")),
            "ingredients":   _extract_ingredients(block),
            "target_dataset": None,
            "group_id":      group_id,
            "source":        block.get("source") if not isinstance(
                block.get("source"), str) else None,
            "info":          block.get("info"),
        }
        reg[schema_id] = entry

    for section in ("data_schemas", "additional_datasets_schemas"):
        for sid, sdict in (tree.get(section) or {}).items():
            _add(sid, section, sdict)

    meta = tree.get("metadata_schema")
    if isinstance(meta, dict):
        _add("metadata_schema", "metadata_schema", meta)

    for aid, adict in (tree.get("assembly_manifests") or {}).items():
        _add(aid, "assembly_manifests", adict)

    for group_id, group_spec in (tree.get("analysis_groups") or {}).items():
        if not isinstance(group_spec, dict):
            continue
        for plot_id, plot_spec in (group_spec.get("plots") or {}).items():
            if not isinstance(plot_spec, dict):
                continue
            spec_slot = _slot(plot_spec.get("spec"))
            pre_wrn = _slot(plot_spec.get("pre_plot_wrangling"))
            target_ds = _resolve_target_dataset(spec_slot)
            reg[plot_id] = {
                "schema_type":    "plots",
                "input_fields":   None,   # resolved from target_dataset at display time
                "wrangling":      pre_wrn,
                "output_fields":  None,   # plots are terminals
                "recipe":         spec_slot,
                "ingredients":    [],
                "target_dataset": target_ds,
                "group_id":       group_id,
                "source":         None,
                "info":           plot_spec.get("info"),
            }

    return reg


def _load_fields_file(abs_path: Path) -> dict | list:
    """Read a standalone fields YAML file.
    Unwraps a single redundant wrapper key (input_fields / output_fields)
    to mirror ConfigManager's ADR-014 auto-unnesting behaviour.
    """
    try:
        content = yaml.safe_load(abs_path.read_text(encoding="utf-8")) or {}
    except Exception:
        return {}
    if isinstance(content, dict) and len(content) == 1:
        key = next(iter(content))
        if key in ("input_fields", "output_fields"):
            return content[key]
    return content


def _resolve_fields_for_schema(schema_id: str, ctx_map: dict, inc_map: dict,
                               _stack: set | None = None) -> dict:
    """Walk ctx_map to find the output fields for schema_id.

    Priority: output_fields file → input_fields file → transparent assembly
    (recurse into each ingredient and merge).

    Returns an ADR-041 Rich Dict: {slug: {type, ...}} or empty dict.
    Cycle guard via _stack prevents infinite recursion.
    """
    if _stack is None:
        _stack = set()
    if schema_id in _stack:
        return {}
    _stack = _stack | {schema_id}  # immutable copy so siblings don't share state

    rels = [r for r, e in ctx_map.items() if e.get("schema_id") == schema_id]

    # Pass 1: explicit output_fields file
    for r in rels:
        if ctx_map[r].get("role") == "output_fields":
            ap = inc_map.get(r)
            if ap:
                f = _load_fields_file(Path(ap))
                if f:
                    return f if isinstance(f, dict) else {}
            break

    # Pass 2: input_fields file fallback
    for r in rels:
        if ctx_map[r].get("role") == "input_fields":
            ap = inc_map.get(r)
            if ap:
                f = _load_fields_file(Path(ap))
                if f:
                    return f if isinstance(f, dict) else {}
            break

    # Pass 3: transparent assembly — merge ingredients
    for r in rels:
        if ctx_map[r].get("role") == "assembly":
            combined: dict = {}
            for ing_id in ctx_map[r].get("ingredients", []):
                combined.update(
                    _resolve_fields_for_schema(ing_id, ctx_map, inc_map, _stack))
            return combined

    return {}


def server(input, output, session):

    @reactive.Calc
    def active_collection_id():
        """Agnostic Discovery: fetches the first collection in the manifest."""
        cfg = active_cfg()
        collections = list(cfg.raw_config.get("assembly_manifests", {}).keys())
        if not collections:
            return "Untitled_Collection"
        return collections[0]

    # 1. Reactive Manifest Authority (Universal Architecture)
    @reactive.Calc
    def active_cfg():
        project_id = input.project_id()
        cached = bootloader.get_cached_asset(
            project_id, "manifest", "raw", "cfg")
        if cached is not None:
            return cached

        path = bootloader.get_location("manifests") / f"{project_id}.yaml"
        cfg = ConfigManager(str(path))
        bootloader.set_cached_asset(project_id, "manifest", "raw", "cfg", cfg)
        return cfg

    orchestrator = DataOrchestrator(
        manifests_dir=bootloader.get_location("manifests"),
        raw_data_dir=bootloader.get_location("raw_data")
    )
    viz_factory = VizFactory()

    # --- 🏗️ Module Initialization (Phase 11-F / ADR-039) ---
    wrangle_studio = WrangleStudio(session.id)
    dev_studio = DevStudio()

    # --- 📦 State Management (Universal) ---
    anchor_path = reactive.Value(None)
    theater_state = reactive.Value("split")
    recipe_pending = reactive.Value(False)
    snapshot_recipe = reactive.Value([])
    gallery_refresh_trigger = reactive.Value(0)

    persona_val = bootloader.persona() if callable(
        bootloader.persona) else bootloader.persona
    print(f"DEBUG: Initializing Server with Persona: {persona_val}")
    current_persona = reactive.Value(persona_val)

    # --- 🔄 Dependency Resolution: Data Tiers (Phase 18 Final) ---
    @reactive.Calc
    def tier1_anchor():
        """Scans the physical Parquet anchor (Predicate Pushdown ready)."""
        project_id = _safe_input(input, "project_id", "default")
        coll_id = active_collection_id()
        cached_lf = bootloader.get_cached_asset(
            project_id, coll_id, "anchor", "lf")
        if cached_lf is not None:
            return cached_lf
        path = anchor_path.get()
        if not path:
            return pl.DataFrame().lazy()
        lf = pl.scan_parquet(path)
        bootloader.set_cached_asset(project_id, coll_id, "anchor", "lf", lf)
        return lf

    @reactive.Calc
    def tier_reference():
        lf = tier1_anchor()
        if _safe_input(input, "ref_tier_switch", False):
            lf = _apply_tier2_transforms(lf, active_cfg())
        return lf

    @reactive.Calc
    @reactive.event(input.btn_apply)
    def tier3_leaf():
        lf = tier1_anchor()
        cfg = active_cfg()
        recipe = snapshot_recipe.get()
        show_long = _safe_input(input, "view_toggle", False)

        # Stage 1: Pre-transform filters
        pre_steps = [s for s in recipe if s.get("stage") == "pre_transform"]
        for step in pre_steps:
            action, col, val = step.get("action", ""), step.get(
                "column"), step.get("value")
            if action == "filter_eq" and col and val is not None:
                try:
                    lf = lf.filter(pl.col(col) == val)
                except Exception:
                    pass

        # Global Sidebar Filters
        for col in lf.columns[:10]:
            clean_col = col.replace(" ", "_").replace("(", "").replace(")", "")
            try:
                val = getattr(input, f"filter_{clean_col}")()
                if val and val != "All":
                    lf = lf.filter(pl.col(col) == val)
            except Exception:
                pass

        if show_long:
            lf = _apply_tier2_transforms(lf, cfg)

        result = lf.collect()
        if result.height == 0:
            ui.notification_show(
                "⚠️ No data. Adjust filters.", type="warning", duration=10)
        recipe_pending.set(False)
        return result

    @reactive.Effect
    @reactive.event(input.btn_apply)
    def handle_apply():
        snapshot_recipe.set(wrangle_studio.logic_stack.get())

    @reactive.Effect
    def track_recipe_changes():
        _ = wrangle_studio.apply_logic
        recipe_pending.set(True)

    # --- 🔌 Module Server Definitions ---
    wrangle_studio.define_server(
        input, output, session, lambda: tier1_anchor().columns, tier1_anchor, viz_factory,
        get_schema_registry=lambda: _schema_registry.get(),
        get_includes_map=lambda: _includes_map.get(),
    )
    dev_studio.define_server(input, output, session)

    # --- 🧬 Extended Reactives ---

    def show_sparmvet_error(err):
        """Unified SPARMVET Error Display."""
        if isinstance(err, SPARMVET_Error):
            title = f"❗ {err.context} Error"
            tip = err.tip
        else:
            title = "❗ Unexpected Error"
            tip = "Check system logs for architectural trace."

        ui.modal_show(
            ui.modal(
                ui.div(
                    ui.h3(title, class_="text-danger"),
                    ui.p(str(err), style="font-size: 1.1em; text-align: left;"),
                    ui.hr(),
                    ui.div(
                        ui.h5("💡 Debugging Tip", class_="fw-bold"),
                        ui.p(tip),
                        class_="p-3 rounded border",
                        style="background-color: #fff9c4; border-color: #f9eeb1; color: #5f5a3a;"
                    ),
                    class_="soft-note-modal"
                ),
                title="System Alert",
                easy_close=True,
                footer=ui.modal_button("Close")
            )
        )

    def _safe_input(input_obj, key, default):
        try:
            val = getattr(input_obj, key)()
            return val if val is not None else default
        except Exception:
            return default

    def _apply_tier2_transforms(lf, cfg):
        """Reusable wrapper for Tier 2 viz-factory baseline transforms."""
        # Introspect for first plot definition
        plot_ids = list(cfg.raw_config.get("plots", {}).keys())
        if not plot_ids:
            return lf

        plot_id = plot_ids[0]
        spec = cfg.raw_config["plots"][plot_id]

        # Apply viz-factory data-wrangling baseline
        lf = viz_factory.prepare_data(lf, spec)
        return lf

    def primary_keys():
        """Returns the list of primary keys from the active manifest."""
        cfg = active_cfg()
        return cfg.raw_config.get("primary_keys", [])

    # 3. Reactive Tab Components (Discovery Architecture)
    @render.ui
    def dynamic_tabs():
        """
        Routes to WrangleStudio, DevStudio, Gallery, or the Analysis Theater.
        ADR-029a / Phase 11-F Routing Hierarchy.
        """
        active_sidebar = _safe_input(input, "sidebar_nav", "Home")
        p = current_persona.get()
        state = theater_state.get()
        is_comparison = _safe_input(input, "comparison_mode", False)

        # 1. Module Routing (ADR-031 Compliance)
        if active_sidebar == "Wrangle Studio":
            return ui.div(wrangle_studio.render_ui(), class_="theater-container-main")
        if active_sidebar == "Dev Studio":
            return ui.div(dev_studio.render_ui(), class_="theater-container-main")
        if active_sidebar == "Gallery":
            return ui.div(gallery_viewer.render_explorer_ui(), class_="theater-container-main")

        # 'Viz' follows the same layout as the Theater but can have different headers
        # if active_sidebar == "Viz":
        #    ... (rest of the theater logic handles Home and Viz)

        # 2. Results Theater (Home) Logic
        # Developer persona 'Clean Slate' only applies to the Theater logic below if needed.
        # But we allow access to the Theater structure.

        # Force state for restricted personas (ADR-030)
        if p == "pipeline_static":
            state = "split"
        elif p == "pipeline_exploration_simple":
            if state == "split":
                state = "plot"

        # Dynamically fetch active collection Data
        try:
            proj_id = _safe_input(input, "project_id",
                                  bootloader.get_default_project())
            coll_id = active_collection_id()
            # ADR-024: Materialize to persistent session location
            anchor_dir = bootloader.get_location("user_sessions") / "anchors"
            if not anchor_dir.exists():
                anchor_dir.mkdir(parents=True, exist_ok=True)
            out_path = anchor_dir / f"{coll_id}.parquet"

            lf_full = orchestrator.materialize_tier1(
                project_id=proj_id,
                collection_id=coll_id,
                output_path=out_path
            )
            # Commit to reactive trigger for anchor discovery
            if out_path.exists():
                anchor_path.set(str(out_path))
        except Exception as e:
            return ui.div(ui.markdown(f"**Data Assembly Failed**: {e}"), class_="alert alert-danger")

        # Discover columns for filter generation
        all_cols = lf_full.columns

        # Metrics overview (Top ribbon)
        metrics = []
        try:
            count = lf_full.select(pl.len()).collect().item()
            metrics.append(ui.div(f"Rows: {count:,}",
                                  class_="metric-pill",
                                  style="margin-right: 12px;"))
            metrics.append(ui.div(f"Cols: {len(all_cols)}",
                                  class_="metric-pill",
                                  style="margin-right: 12px;"))
        except Exception:
            pass

        metrics_ui = ui.div(*metrics,
                            class_="d-flex align-items-center me-auto",
                            style="margin-left: 10px;") if metrics else None

        # --- Sub-Header: Branding & Persona Status ---
        theater_header = ui.div(
            ui.div(
                ui.div(
                    ui.h4(f"SPARMVET Dashboard ({active_sidebar})",
                          class_="mb-0"),
                    ui.tags.small(f"Manifest: {input.project_id()} | Persona: {p.replace('_', ' ').title()}",
                                  class_="text-muted"),
                    class_="flex-grow-1"
                ),
                class_="d-flex align-items-center"
            ),
            class_="theater-header-branding mb-2",
            style="padding: 10px 15px; background: white; border-bottom: 1px solid #dee2e6;"
        )

        # Shared Header Controls (Aggressive Alighment ADR-029a)
        header_controls = ui.div(
            ui.div(
                # Left Side: Metrics + Control Buttons
                ui.div(
                    ui.div(metrics_ui if metrics_ui else ui.div(),
                           style="display: flex; align-items: center;"),
                    ui.div(
                        ui.input_action_button("btn_max_plot", ui.tags.i(class_="bi bi-graph-up"),
                                               class_=f"control-btn {'active-view-btn' if state == 'plot' else ''}",
                                               title="Maximize Plot View"),
                        ui.input_action_button("btn_max_table", ui.tags.i(class_="bi bi-table"),
                                               class_=f"control-btn {'active-view-btn' if state == 'table' else ''}",
                                               title="Maximize Table View"),
                        ui.input_action_button("btn_reset_theater", ui.tags.i(class_="bi bi-grid-1x2"),
                                               class_=f"control-btn {'active-view-btn' if state == 'split' else ''}",
                                               title="Grid Quadrant View"),
                        class_="btn-group d-flex align-items-center ms-2",
                        style="height: 28px;"
                    ),
                    class_="d-flex align-items-center",
                    style="height: 36px;"
                ),
                # Right Side: Toggles
                ui.div(
                    ui.div(ui.input_switch("view_toggle", "Wide ↔ Long", value=False),
                           class_="d-flex align-items-center me-3", style="height: 36px; padding-top: 4px;"),
                    ui.output_ui("comparison_mode_toggle_ui"),
                    class_="d-flex align-items-center",
                    style="height: 36px;"
                ),
                class_="d-flex justify-content-between align-items-center w-100 bg-light border p-1 rounded",
                style="height: 38px;"
            ),
            class_="d-flex align-items-center w-100 p-0",
            style="margin-top: -2px; padding: 0 10px !important; height: 40px;"
        )

        # --- Theater Layout (2x2 Quadrant Philosophy - ADR-029a) ---

        # 🟢 Quadrant A: Reference Plot
        ref_plot_quad = ui.card(
            ui.card_header(ui.tags.span(
                "Plot Reference (T1/T2)", class_="reference-label")),
            ui.output_plot("plot_reference"),
            class_="shadow-sm flex-grow-1"
        )

        # 🟢 Quadrant B: Reference Table
        ref_table_quad = ui.card(
            ui.card_header(ui.tags.span(
                "Table Reference", class_="reference-label")),
            ui.div(ui.input_switch("ref_tier_switch",
                                   "T1 ↔ T2", value=False), class_="small"),
            ui.output_table("table_reference"),
            class_="shadow-sm flex-grow-1"
        )

        # 🔵 Quadrant C: Active Plot (T3)
        active_plot_quad = ui.card(
            ui.card_header(ui.h6("Active Visualization (Tier 3)"),
                           class_="d-flex justify-content-between"),
            ui.output_plot("plot_leaf", brush=ui.brush_opts(
                fill="#2196f3", opacity=0.3)),
            class_="shadow-sm flex-grow-1"
        )

        # 🔵 Quadrant D: Active Data Sandbox (Drawing #3 - Wider Column Picker)
        pkeys = primary_keys()
        data_cols = [c for c in all_cols if c not in pkeys]
        active_table_quad = ui.card(
            ui.card_header(ui.h6("Active Data Sandbox")),
            ui.div(
                ui.input_selectize("column_visibility_picker", None,
                                   choices=data_cols, selected=data_cols, multiple=True,
                                   options={"plugins": ["remove_button"]}),
                class_="px-2 pt-1 pb-1 w-100 column-picker-container"
            ),
            ui.output_table("table_leaf"),
            class_="shadow-sm flex-grow-1"
        )

        # Apply button with pending badge (ADR-029a Synchronization)
        apply_controls = ui.div(
            ui.div(ui.output_ui("recipe_pending_badge_ui"),
                   style="height: 31px; display: flex; align-items: center;"),
            ui.input_action_button(
                "btn_apply", "▶ Apply", class_="btn btn-success btn-sm", style="height: 31px;"),
            class_="apply-btn-container d-flex align-items-center justify-content-end mb-2 gap-2"
        )

        # Implementation logic for Grid States (ADR-030)
        if state == "plot":
            # Maximized Plot View
            active_col = ui.div(
                apply_controls, active_plot_quad, class_="active-pane h-100")
            reference_col = ui.div(
                ref_plot_quad, class_="reference-pane h-100")
        elif state == "table":
            # Maximized Table View
            active_col = ui.div(
                apply_controls, active_table_quad, class_="active-pane h-100")
            reference_col = ui.div(
                ref_table_quad, class_="reference-pane h-100")
        else:
            # Standard Quadrant Stack
            active_col = ui.div(
                apply_controls,
                ui.layout_columns(active_plot_quad,
                                  active_table_quad, col_widths=12),
                class_="active-pane h-100"
            )
            reference_col = ui.div(
                ui.layout_columns(
                    ref_plot_quad, ref_table_quad, col_widths=12),
                class_="reference-pane h-100"
            )

        is_triple = _safe_input(input, "triple_tier_mode", False)

        # Final Assembly (Comparison VS Single)
        if is_triple:
            theater_layout = ui.layout_columns(
                ui.div(ui.h6("T1: Raw"), ui.output_table(
                    "table_anchor"), class_="p-1 border rounded small"),
                ui.div(ui.h6("T2: Ref"), ui.output_table(
                    "table_reference"), class_="p-1 border rounded small"),
                ui.div(ui.h6("T3: Leaf"), ui.output_table(
                    "table_leaf"), class_="p-1 border rounded small"),
                col_widths=[4, 4, 4]
            )
        elif is_comparison:
            theater_layout = ui.layout_columns(
                reference_col, active_col, col_widths=[5, 7])
        else:
            theater_layout = active_col

        # Build manifest-driven tabs
        cfg = active_cfg()
        groups = cfg.raw_config.get("analysis_groups", {})
        extra_tabs = []

        for group_id, group_spec in groups.items():
            plot_ids = list(group_spec.get("plots", {}).keys())

            # --- 2. Sub-Tabs for individual plots ---
            plot_subtabs = []
            for p_id in plot_ids:
                plot_subtabs.append(
                    ui.nav_panel(
                        p_id.replace("_", " ").title(),
                        ui.card(
                            ui.output_plot(f"plot_group_{p_id}"),
                            class_="shadow-none border-0 mt-0",
                            style="min-height: 550px;"
                        )
                    )
                )

            if not plot_subtabs:
                group_content = ui.div(
                    ui.hr(class_="my-1"),
                    ui.p("No plots defined for this group.",
                         class_="text-muted p-4")
                )
            else:
                group_content = ui.div(
                    ui.div(
                        ui.navset_underline(
                            *plot_subtabs, id=f"subtabs_{group_id.replace(' ', '_')}"),
                        class_="px-3 pb-3"
                    )
                )

            # --- ID Sanitation Audit ---
            safe_id = group_id.replace(' ', '_').replace(
                '📊', 'QC').replace('💊', 'AMR').lower()
            extra_tabs.append(ui.nav_panel(
                group_spec.get("description", group_id),
                group_content,
                value=f"tab_{safe_id}"
            ))

        tabs = [
            ui.nav_panel("Theater", theater_layout),
            ui.nav_panel("Inspector", ui.output_table("full_data_table"))
        ] + extra_tabs

        return ui.div(
            theater_header,
            ui.navset_card_tab(
                *tabs,
                id="central_theater_tabs",
                header=header_controls
            ),
            class_="theater-container-main"
        )

    @render.ui
    def sidebar_nav_ui():
        perm = current_persona.get()
        print(f"DEBUG: Rendering sidebar_nav_ui for Persona: {perm}")

        # Persona-based sidebar masking (ADR-030)
        nav_items = [
            ui.nav_panel("Home", value="Home")
        ]

        if perm in ["pipeline_exploration_advanced", "project_independent", "developer"]:
            nav_items.append(ui.nav_panel(
                "Blueprint Architect", value="Wrangle Studio"))
            nav_items.append(ui.nav_panel("Analysis Theater", value="Viz"))

        if perm in ["developer"]:
            nav_items.append(ui.nav_panel("Dev Studio", value="Dev Studio"))

        nav_items.append(ui.nav_panel("Gallery", value="Gallery"))

        return ui.navset_pill(
            *nav_items,
            id="sidebar_nav",
            header=ui.h6(f"Active: {perm.replace('_', ' ').title()}",
                         class_="text-muted px-2 py-1 mb-1 border-bottom", style="font-size: 0.7em;")
        )

    # 4. Sidebar Tools (Contextual Manifest Workbench)
    @output(id="sidebar_tools_ui")
    @render.ui
    def sidebar_tools_ui():
        """
        Relocated Sidebar Management (ADR-038).
        Enforces dedicated Persona-based control clusters.
        """
        active_sidebar = _safe_input(input, "sidebar_nav", "Home")

        # 🟢 Discovery Mode (Gallery)
        if active_sidebar == "Gallery":
            return ui.div(
                ui.p("Discovery Mode Active", class_="text-muted p-4 italic"),
                ui.p("Choose a visual recipe to begin.",
                     class_="text-muted px-4 small")
            )

        # 🔵 Manifest Workbench (Wrangle Studio)
        if active_sidebar == "Wrangle Studio":
            return ui.accordion(
                ui.accordion_panel(
                    "Blueprint Discovery",
                    ui.input_select("stored_manifest_selector", "1. Master Manifest:",
                                    choices=["Scanning config/..."]),
                    ui.input_select("dataset_pipeline_selector", "2. Target Blueprint Component:",
                                    choices=["Select a Master first"]),
                    ui.div(
                        ui.tags.small(
                            "Info: This selects a specific processing track (e.g. a dataset or assembly) from the Master Manifest to load into your workbench.", class_="text-muted"),
                        class_="mb-2"
                    ),
                    ui.input_action_button("btn_import_manifest", "📥 Import (Replace)",
                                           class_="btn-info btn-sm w-100 mt-2"),
                    ui.input_action_button("btn_save_internal", "💾 Save to Project",
                                           class_="btn-success btn-sm w-100 mt-1"),
                    icon=ui.tags.i(class_="bi bi-search")
                ),
                ui.accordion_panel(
                    "External Exchange",
                    ui.input_file("manifest_uploader", "Select YAML...",
                                  accept=[".yaml"], multiple=False),
                    ui.input_action_button("btn_upload_replace", "📥 Upload (Replace)",
                                           class_="btn-info btn-sm w-100 mb-1"),
                    ui.input_action_button("btn_upload_append", "➕ Upload & Append",
                                           class_="btn-outline-primary btn-sm w-100"),
                    ui.hr(),
                    ui.download_button("btn_download_manifest", "💾 Download/Export",
                                       class_="btn-outline-primary w-100"),
                    icon=ui.tags.i(class_="bi bi-cloud-arrow-up")
                ),
                id="wrangle_sidebar_accordion"
            )

        # 🏠 Standard Operation Sidebar (Home/Viz)
        try:
            proj_choices = list(bootloader.available_projects.keys())
            def_proj = bootloader.get_default_project()
        except:
            proj_choices = []
            def_proj = None

        return ui.accordion(
            ui.accordion_panel(
                "Project Navigator",
                ui.div(
                    ui.input_select("project_id", "Project Selection",
                                    choices=proj_choices,
                                    selected=def_proj),
                    class_="d-flex flex-column gap-1"
                ),
                icon=ui.tags.i(class_="bi bi-folder-fill")
            ),
            ui.accordion_panel(
                "Filters",
                ui.div(
                    ui.output_ui("sidebar_filters"),
                    class_="d-flex flex-column gap-0"
                ),
                icon=ui.tags.i(class_="bi bi-filter-circle-fill")
            ),
            ui.accordion_panel(
                "System Tools",
                ui.div(
                    ui.output_ui("system_tools_ui"),
                    class_="d-flex flex-column gap-1"
                ),
                icon=ui.tags.i(class_="bi bi-cpu-fill")
            ),
            id="nav_accordion",
            multiple=True,
            open=["Project Navigator", "Filters"]
        )

    # --- 🧬 Blueprint Architect Visual Sync (ADR-039 / Independent from Home) ---
    @reactive.Effect
    def sync_blueprint_mapper():
        """Syncs TubeMap from the Architect's own manifest selector — independent of Home.
        Uses ConfigManager to resolve !include tags and flatten analysis_groups plots."""
        if _safe_input(input, "sidebar_nav", "Home") != "Wrangle Studio":
            return
        path_str = _safe_input(input, "stored_manifest_selector", None)
        if not path_str:
            return
        from pathlib import Path as _Path
        if not _Path(path_str).exists():
            return
        try:
            # Resolves !include + flattens analysis_groups
            cfg = ConfigManager(str(path_str))
            info = wrangle_studio.active_component_info.get()
            active_node = info.get("schema_id") if info else None
            mapper = BlueprintMapper(cfg.raw_config, active_node=active_node)
            mermaid_code = mapper.generate_mermaid()
            wrangle_studio.active_tubemap_mermaid.set(mermaid_code)
            # Store resolved config as YAML for the viewer
            import yaml as _yaml
            wrangle_studio.active_raw_yaml.set(
                _yaml.dump(cfg.raw_config, default_flow_style=False,
                           allow_unicode=True)
            )
        except Exception as e:
            print(f"[sync_blueprint_mapper] Failed: {e}")

    # --- 📐 Right Sidebar Context Matrix (ADR-039 / Phase 18) ---
    @output
    @render.ui
    def right_sidebar_content_ui():
        """
        Context-sensitive right sidebar (ADR-039).
        Switches content based on the active module.
        """
        active_sidebar = _safe_input(input, "sidebar_nav", "Home")

        # --- 🏗️ Blueprint Architect (Wrangle Studio) ---
        if active_sidebar == "Wrangle Studio":
            selected_node = _safe_input(input, "blueprint_node_clicked", None)
            stack = wrangle_studio.logic_stack.get()
            step_count = len(stack)

            node_info = ui.div(
                ui.p("No node selected. Click a TubeMap node to begin surgical focus.",
                     class_="text-muted small italic"),
                class_="p-2"
            )
            if selected_node:
                node_info = ui.div(
                    ui.div(
                        ui.span("🔬 ", class_="me-1"),
                        ui.span(f"Focused: {selected_node}", class_="fw-bold"),
                        class_="mb-1"
                    ),
                    ui.div(
                        f"Logic stack: {step_count} step(s)", class_="text-muted small"),
                    class_="p-2 bg-white border rounded shadow-sm mb-2"
                )

            return ui.div(
                ui.card(
                    ui.card_header(
                        ui.div(ui.h5("Blueprint Surgeon", class_="mb-0"),
                               class_="d-flex justify-content-center w-100")
                    ),
                    ui.div(
                        node_info,
                        ui.hr(),
                        ui.h6("Active Logic Stack", class_="text-muted px-2"),
                        ui.output_ui("audit_nodes_tier3"),
                        class_="p-2"
                    ),
                    class_="mb-2 shadow-sm border-0"
                ),
                class_="sidebar-content p-0 d-flex flex-column h-100"
            )

        # --- 🎭 Analysis Theater (Home / Viz) ---
        if active_sidebar in ("Home", "Viz", None, ""):
            return ui.div(
                ui.card(
                    ui.card_header(
                        ui.div(ui.h5("Pipeline Audit", class_="mb-0"),
                               class_="d-flex justify-content-center w-100")
                    ),
                    ui.div(
                        ui.h6("Tier 2 (Inherited)", class_="text-muted"),
                        ui.output_ui("audit_nodes_tier2"),
                        ui.hr(),
                        ui.h6("Tier 3 (User)", class_="text-muted"),
                        ui.output_ui("audit_nodes_tier3"),
                        class_="p-2"
                    ),
                    class_="mb-2 shadow-sm border-0"
                ),
                ui.div(
                    ui.output_ui("audit_stack_tools_ui"),
                    class_="mt-auto p-2"
                ),
                class_="sidebar-content p-0 d-flex flex-column h-100"
            )

        # --- 🖼️ Gallery ---
        if active_sidebar == "Gallery":
            return ui.div(
                ui.card(
                    ui.card_header(
                        ui.h5("Gallery Explorer", class_="mb-0 text-center")),
                    ui.div(
                        ui.p("📚 Browse visual recipes.",
                             class_="text-muted small p-2"),
                        ui.p("Select a recipe to copy its YAML into the Architect sandbox.",
                             class_="text-muted small px-2"),
                        class_="p-1"
                    ),
                    class_="mb-2 shadow-sm border-0"
                ),
                class_="sidebar-content p-0"
            )

        # --- 🛠️ Dev Studio ---
        if active_sidebar == "Dev Studio":
            return ui.div(
                ui.card(
                    ui.card_header(
                        ui.h5("Dev Inspector", class_="mb-0 text-center")),
                    ui.div(
                        ui.p("🔧 Developer diagnostic tools.",
                             class_="text-muted small p-2"),
                        class_="p-1"
                    ),
                    class_="mb-2 shadow-sm border-0"
                ),
                class_="sidebar-content p-0"
            )

        # --- Default fallback (future modes) ---
        return ui.div(
            ui.p("—", class_="text-muted p-3 text-center"),
            class_="sidebar-content p-0"
        )

    # --- (Deduplicated tiers moved to top) ---

    @output
    @render.ui
    def recipe_pending_badge_ui():
        if recipe_pending.get():
            return ui.div("⏳ Pending", class_="recipe-pending-badge text-center")
        return ui.div()

    @output
    @render.plot
    def plot_reference():
        cfg = active_cfg()
        plot_ids = list(cfg.raw_config.get("plots", {}).keys())
        if not plot_ids:
            return None
        plot_id = plot_ids[0]

        proj = cfg.raw_config.get("id", input.project_id())
        coll = active_collection_id()
        cached_plot = bootloader.get_cached_asset(
            proj, coll, plot_id, "ref_plot")
        if cached_plot is not None:
            return cached_plot

        plt = viz_factory.render(tier_reference(), cfg.raw_config, plot_id)
        bootloader.set_cached_asset(proj, coll, plot_id, "ref_plot", plt)
        return plt

    @output
    @render.table
    def table_reference():
        return tier_reference().head(100).collect()

    @output
    @render.plot
    def plot_leaf():
        cfg = active_cfg()
        plot_ids = list(cfg.raw_config.get("plots", {}).keys())
        if not plot_ids:
            return None
        return viz_factory.render(tier3_leaf().lazy(), cfg.raw_config, plot_ids[0])

    @output
    @render.table
    def table_leaf():
        return tier3_leaf().head(5)

    @output
    @render.ui
    def audit_nodes_tier3():
        cfg = active_cfg()
        collection_id = active_collection_id()
        nodes = [
            ui.div(f"Project: {cfg.raw_config.get('id')}",
                   class_="audit-node-tier2"),
            ui.div(f"Collection: {collection_id}", class_="audit-node-tier2"),
        ]
        if "metadata_schema" in cfg.raw_config:
            nodes.append(ui.div(f"Anchor: {collection_id}.parquet (w/ Metadata)",
                         class_="audit-node-tier3"))
        else:
            nodes.append(ui.div(f"Anchor: {collection_id}.parquet (Standalone)",
                         class_="audit-node-tier3"))

        active_nodes = wrangle_studio.logic_stack.get()
        if active_nodes:
            nodes.append(ui.hr())
            nodes.append(ui.h6("Session Transformations (Tier 3)"))
            for i, node in enumerate(active_nodes):
                action = node.get("action", "unknown")
                comment = node.get("comment", "No comment")
                nodes.append(ui.tooltip(
                    ui.div(
                        ui.div(f"⚡ {action}", class_="fw-bold"),
                        ui.div(f"💬 {comment}", style="font-size: 0.8em;"),
                        class_="audit-node-tier3"
                    ),
                    f"Action: {action}", placement="left", id=f"node_tt_{i}"
                ))
        return ui.div(*nodes)

    @output
    @render.ui
    def audit_nodes_tier2():
        cfg = active_cfg()
        collection_id = active_collection_id()
        collections = cfg.raw_config.get("assembly_manifests", {})
        recipe = []
        if collection_id in collections:
            raw_recipe = collections[collection_id].get("recipe", [])
            recipe = DataWrangler._resolve_tier(raw_recipe, "tier1")

        if not recipe:
            return ui.div(ui.div("No Tier 2 steps defined.", class_="audit-node-tier2"))

        nodes = []
        for step in recipe:
            action = step.get("action", "unknown")
            label = step.get("label") or step.get("right_ingredient") or action
            nodes.append(ui.tooltip(
                ui.div(f"[Tier 2] {action}: {label}",
                       class_="audit-node-tier2"),
                f"Action: {action}", placement="left"
            ))
        return ui.div(*nodes)

    @render.ui
    def system_tools_ui():
        return ui.div(
            ui.div(
                ui.p("Session Management", class_="ultra-small fw-bold mb-1"),
                ui.div(
                    ui.input_action_button(
                        "restore_session", "Restore Last Session", class_="btn-sm w-100 mb-1"),
                    ui.input_action_button(
                        "export_global", "Export Full Dataset", class_="btn-sm w-100"),
                ),
                class_="mb-3 px-2"
            ),
            ui.div(
                ui.p("Data Ingestion (ADR-031)",
                     class_="ultra-small fw-bold mb-1"),
                ui.div(
                    ui.input_file("file_ingest", None, multiple=True,
                                  accept=[".yaml"]),
                    class_="upload-row mb-1"
                ),
                ui.input_action_button(
                    "btn_ingest", "🚀 Ingest Manifests", class_="w-100"),
                class_="px-2"
            )
        )

    @output
    @render.ui
    def sidebar_filters():
        try:
            lf = tier1_anchor()
            cols = lf.columns[:6]
            filters = []
            for col in cols:
                clean_id = col.replace(" ", "_").replace(
                    "(", "").replace(")", "")
                choices = ["All"] + \
                    sorted(lf.select(pl.col(col)).unique(
                    ).collect()[col].to_list())
                filters.append(ui.card(
                    ui.input_select(f"filter_{clean_id}", f"Filter: {col}",
                                    choices=choices, selected="All"),
                    class_="mb-2 border-0 shadow-none bg-transparent"
                ))
            return ui.div(*filters)
        except Exception:
            return ui.div(ui.markdown("*Filters unavailable.*"))

    @reactive.Effect
    @reactive.event(input.btn_max_plot)
    def handle_max_plot():
        theater_state.set("plot")

    @reactive.Effect
    @reactive.event(input.btn_max_table)
    def handle_max_table():
        theater_state.set("table")

    @reactive.Effect
    @reactive.event(input.btn_reset_theater)
    def handle_reset_theater():
        theater_state.set("split")

    @reactive.Effect
    @reactive.event(input.plot_leaf_brush)
    def handle_plot_brush():
        brush = input.plot_leaf_brush()
        if not brush:
            return
        cfg = active_cfg()
        plot_ids = list(cfg.raw_config.get("plots", {}).keys())
        if not plot_ids:
            return
        plot_id = plot_ids[0]
        mapping = cfg.raw_config["plots"][plot_id].get("mapping", {})
        x_col = mapping.get("x")
        y_col = mapping.get("y")

        outliers = lookup_anchor_rows(
            brush, anchor_path.get(), x_col=x_col, y_col=y_col)
        if outliers.is_empty():
            return

        m = ui.modal(
            ui.h4(f"Outlier Quick-View ({outliers.height} rows)"),
            ui.output_table("brush_results_table"),
            ui.modal_button("Close"),
            size="xl", easy_close=True
        )
        ui.modal_show(m)

        @output
        @render.table
        def brush_results_table():
            return outliers.head(20)

    # --- 🔬 Gallery Taxonomy 'Select All' Logic ---
    @reactive.Effect
    @reactive.event(input.gallery_all_family)
    def _sync_family_all():
        choices = ["Distribution", "Correlation", "Comparison",
                   "Ranking", "Evolution", "Part-to-Whole"]
        selected = choices if input.gallery_all_family() else []
        ui.update_checkbox_group("gallery_filter_family", selected=selected)

    @reactive.Effect
    @reactive.event(input.gallery_all_pattern)
    def _sync_pattern_all():
        checked = input.gallery_all_pattern()
        choices = [
            "1 Numeric", "2 Numeric", "1 Numeric, 1 Categorical",
            "1 Numeric, 2 Categorical", "1 Numeric, 2 Categorical (Faceted)",
            "2 Numeric, 1 Categorical (Faceted)", "Numeric-Numeric"
        ]
        ui.update_checkbox_group(
            "gallery_filter_pattern", selected=choices if checked else [])

    # --- Gallery Initialization (ADR-037) ---
    @reactive.Effect
    def _init_gallery_selector():
        """Ensure all plots are selected by default on startup."""
        index_path = bootloader.get_location("gallery") / "gallery_index.json"
        if index_path.exists():
            with open(index_path, "r") as f:
                idx = json.load(f)
            registry = idx.get("registry", {})
            choices = {rid: entry["name"] for rid, entry in registry.items()}
            choices = dict(sorted(choices.items(), key=lambda item: item[1]))
            ui.update_select("gallery_recipe_select", choices=choices)

    @reactive.Effect
    @reactive.event(input.gallery_all_difficulty)
    def _sync_difficulty_all():
        choices = ["Simple", "Intermediate", "Advanced"]
        selected = choices if input.gallery_all_difficulty() else []
        ui.update_checkbox_group(
            "gallery_filter_difficulty", selected=selected)

    @reactive.Effect
    @reactive.event(input.btn_clone_gallery)
    def handle_gallery_clone():
        recipe_id = _safe_input(input, "gallery_recipe_select", None)
        if not recipe_id:
            return

        index_path = bootloader.get_location("gallery") / "gallery_index.json"
        if not index_path.exists():
            return

        try:
            with open(index_path, "r") as f:
                idx = json.load(f)

            recipe_entry = idx["registry"].get(recipe_id)
            if not recipe_entry:
                return

            file_path = recipe_entry["path"]
            with open(file_path, "r") as f:
                manifest = yaml.safe_load(f)

            wrangling_raw = manifest.get("wrangling", {})
            # Handle both list and dict formats for backward compatibility
            tier3_raw = wrangling_raw.get("tier3", []) if isinstance(
                wrangling_raw, dict) else wrangling_raw

            new_steps = DataWrangler._resolve_tier(tier3_raw, "all")
            valid_nodes = []
            for step in new_steps:
                action = step.get("action", "unknown")
                params = {k: v for k, v in step.items() if k != "action"}
                valid_nodes.append({
                    "action": action,
                    "params": params,
                    "comment": f"Ghost-loaded from Reference: {recipe_id}"
                })
            wrangle_studio.logic_stack.set(valid_nodes)
            ui.notification_show(
                f"✅ Recipe '{recipe_id}' cloned to Sandbox.", type="success")
        except Exception as e:
            print(f"❌ Clone failed: {e}")

    # --- Gallery Content Resolution (ADR-037) ---
    @reactive.Calc
    def _gallery_active_metadata():
        rid = _safe_input(input, "gallery_recipe_select", None)
        if not rid:
            return None
        index_path = bootloader.get_location("gallery") / "gallery_index.json"
        if not index_path.exists():
            return None
        with open(index_path, "r") as f:
            idx = json.load(f)
        return idx["registry"].get(rid)

    @output
    @render.ui
    def gallery_preview_img():
        meta = _gallery_active_metadata()
        if not meta:
            return ui.div("Select a recipe to view preview.", class_="p-5 text-muted")

        path_str = meta.get("path")
        if not path_str:
            return ui.div("Path missing in index.", class_="text-danger")

        img_path = Path(path_str).parent / "preview_plot.png"
        if img_path.exists():
            try:
                with open(img_path, "rb") as f:
                    encoded = base64.b64encode(f.read()).decode("utf-8")
                return ui.div(
                    ui.img(src=f"data:image/png;base64,{encoded}",
                           style="max-width: 100%; border: 1px solid #dee2e6; border-radius: 4px; box-shadow: 0 4px 12px rgba(0,0,0,0.1);"),
                    class_="p-3 text-center"
                )
            except Exception as e:
                return ui.div(f"Error loading preview: {e}", class_="text-danger")
        return ui.div("No preview image found (.png)", class_="p-5 text-muted")

    @output
    @render.table(index=False)
    def gallery_static_data():
        """Render a clean, left-aligned table without row numbers (ADR-033)."""
        meta = _gallery_active_metadata()
        if not meta:
            return None
        path_str = meta.get("path")
        if not path_str:
            return None

        data_path = Path(path_str).parent / "example_data.tsv"
        if data_path.exists():
            try:
                # Polars maintains high-density left alignment by default in Shiny's render.table
                return pl.read_csv(data_path, separator="\t")
            except Exception as e:
                # Fallback to an empty DF with error message for debugging
                return pl.DataFrame({"Error": [f"Could not load data: {e}"]})
        return None

    @output
    @render.text
    def gallery_yaml_preview():
        meta = _gallery_active_metadata()
        if not meta:
            return "Select a recipe"
        path_str = meta.get("path")
        if not path_str:
            return "Manifest path not found"

        if Path(path_str).exists():
            with open(path_str, "r") as f:
                return f.read()
        return "Source YAML not found"

    @output
    @render.ui
    def gallery_md_content():
        meta = _gallery_active_metadata()
        if not meta:
            return ui.div("Select an entry to view guidance.", class_="p-4 text-center text-muted")

        path_str = meta.get("path")
        if not path_str:
            return ui.div("Metadata path not found", class_="text-danger")

        md_path = Path(path_str).parent / "recipe_meta.md"
        if md_path.exists():
            with open(md_path, "r") as f:
                return ui.div(ui.markdown(f.read()), class_="gallery-guidance-styled")
        return ui.div("Educational metadata (recipe_meta.md) missing.", class_="alert alert-warning")

    @reactive.Effect
    @reactive.event(input.btn_apply_gallery_filters, input.sidebar_nav)
    def _update_gallery_options():
        """
        High-Performance Filtering Gate (ADR-037).
        TRIGGERED BY: 'Apply' button OR Tab switch to Gallery.
        """
        # 1. Check if we are actually in the Gallery (don't recalc if switching away)
        if input.sidebar_nav() != "Gallery":
            return
        index_path = bootloader.get_location("gallery") / "gallery_index.json"
        if not index_path.exists():
            ui.notification_show("Indexer not found.", type="error")
            return

        with open(index_path, "r") as f:
            idx = json.load(f)

        # 2. Collect Filter Inputs
        sel_families = input.gallery_filter_family()
        sel_patterns = input.gallery_filter_pattern()
        sel_difficulties = input.gallery_filter_difficulty()

        ui.notification_show("🔍 Filtering recipes...",
                             duration=1, type="message")

        # 2. Pivot-Set Intersection
        registry = idx["registry"]
        pivot = idx["pivot"]

        family_matches = set()
        for f in sel_families:
            family_matches.update(pivot["by_family"].get(f, []))

        pattern_matches = set()
        for p in sel_patterns:
            pattern_matches.update(pivot["by_pattern"].get(p, []))

        difficulty_matches = set()
        for d in sel_difficulties:
            difficulty_matches.update(pivot["by_difficulty"].get(d, []))

        # Perform the final Multi-Set Intersection
        valid_ids = family_matches & pattern_matches & difficulty_matches

        # 3. Build UI Choices
        choices = {vid: registry[vid]["name"] for vid in valid_ids}
        choices = dict(sorted(choices.items(), key=lambda item: item[1]))

        # 4. Push Update to UI
        ui.update_select("gallery_recipe_select",
                         label=ui.span(
                             f"Visual Gallery ({len(choices)} matched)", class_="fw-bold text-success"),
                         choices=choices,
                         selected=None)

        if not choices:
            ui.notification_show(
                "⚠️ No matches found for these filters.", type="warning")

    @output
    @render.ui
    def gallery_browser_anchor():
        """Placeholder for any additional anchor logic if needed."""
        return None

    @reactive.Effect
    @reactive.event(input.btn_ingest)
    def handle_ingest():
        files = _safe_input(input, "file_ingest", None)
        if not files:
            return
        ui.notification_show("⏳ Ingesting...", type="message")
        manifest_dir = bootloader.get_location("manifests")
        for f in files:
            name = f['name']
            path = Path(f['datapath'])
            if name.endswith(".yaml"):
                shutil.copy(path, manifest_dir / name)
        bootloader.__init__(persona=current_persona.get())
        ui.update_select("project_id", choices=list(
            bootloader.available_projects.keys()))
        ui.notification_show("✅ Ingestion complete.", type="success")

    @reactive.Effect
    @reactive.event(input.persona_selector)
    def update_persona_context():
        new_persona = input.persona_selector()
        if new_persona:
            current_persona.set(new_persona)
            bootloader.__init__(persona=new_persona)
            ui.notification_show(f"Persona: {new_persona}", type="message")

    # --- 🏗️ Phase 18: Wrangle Studio Manifest Management ---
    @reactive.Effect
    @reactive.event(input.sidebar_nav)
    def _init_wrangle_manifests():
        """Auto-discovery of Master manifests in config/ directory."""
        if input.sidebar_nav() != "Wrangle Studio":
            return

        config_dir = Path("config/manifests/pipelines")
        if not config_dir.exists():
            config_dir = Path("config")

        all_yamls = list(config_dir.rglob("*.yaml"))
        master_manifests = []
        for path in all_yamls:
            parent_name = path.parent.name
            possible_master = path.parent.parent / f"{parent_name}.yaml"
            if possible_master.exists():
                continue
            master_manifests.append(str(path))

        master_manifests.sort()
        ui.update_select("stored_manifest_selector",
                         choices=master_manifests,
                         selected=master_manifests[0] if master_manifests else None)

    # Per-session cache: rel_path → abs_path for all !include files in active manifest
    _includes_map: reactive.Value = reactive.Value({})
    # rel_path → {role, schema_id, schema_type, siblings, ingredients}
    _component_ctx_map: reactive.Value = reactive.Value({})
    # schema_id → complete structural entry (both !include and inline content)
    _schema_registry: reactive.Value = reactive.Value({})

    @reactive.Effect
    @reactive.event(input.stored_manifest_selector)
    def _update_dataset_pipelines():
        """Discovers all actual !include files referenced by the manifest.
        Each entry is a real file on disk that can be directly loaded and saved.
        Files are grouped by subdirectory type (wrangling/, plots/, input_fields/, ...).
        """
        path = input.stored_manifest_selector()
        if not path or not Path(path).exists():
            return
        try:
            manifest_path = Path(path)
            manifest_dir = manifest_path.parent
            raw_text = manifest_path.read_text(encoding="utf-8")

            rel_paths = re.findall(r"!include\s+['\"]([^'\"]+)['\"]", raw_text)

            inc_map: dict = {}
            groups: dict = {}  # subdir_type → {rel_path: display_name}
            seen: set = set()

            for rel_path in rel_paths:
                if rel_path in seen:
                    continue
                seen.add(rel_path)
                abs_path = (manifest_dir / rel_path).resolve()
                if not abs_path.exists():
                    print(f"[Blueprint] Included file not found: {abs_path}")
                    continue
                inc_map[rel_path] = str(abs_path)

            _includes_map.set(inc_map)
            ctx_map = _build_sibling_map(path)
            _component_ctx_map.set(ctx_map)
            _schema_registry.set(_build_schema_registry(path, inc_map))

            # Build display groups using semantic labels from sibling map
            for rel_path in inc_map:
                abs_path = Path(inc_map[rel_path])
                ctx_entry = ctx_map.get(rel_path, {})
                if ctx_entry:
                    display = f"{ctx_entry.get('schema_id', abs_path.stem)} — {ctx_entry.get('role', '?')}"
                else:
                    display = abs_path.name
                parts = Path(rel_path).parts
                subdir = parts[-2] if len(parts) >= 2 else "root"
                if subdir not in groups:
                    groups[subdir] = {}
                # value=rel_path, label=semantic
                groups[subdir][rel_path] = display

            if groups:
                ui.update_select("dataset_pipeline_selector", choices=groups)
            else:
                ui.update_select("dataset_pipeline_selector",
                                 choices=["No !include files found"])
        except Exception as e:
            print(f"[_update_dataset_pipelines] Error: {e}")
            ui.update_select("dataset_pipeline_selector",
                             choices=["⚠️ Error – see console"])

    @reactive.Effect
    @reactive.event(input.blueprint_node_clicked)
    def _sync_selector_from_node_click():
        """Syncs Blueprint selector to whichever node was clicked in the TubeMap,
        then programmatically triggers the import button for full component load.

        TubeMap node IDs are safe_schema_id strings (spaces/dashes → underscores).
        Selector values are rel_path strings. This bridge finds the best rel_path
        for the clicked schema_id using _component_ctx_map.
        """
        try:
            node_id = input.blueprint_node_clicked()
            if not node_id or node_id.startswith("INFO_"):
                return

            ctx_map = _component_ctx_map.get()
            if not ctx_map:
                return

            # Role priority: prefer the most informative component for this schema
            _ROLE_PRIORITY = {
                "assembly": 0, "wrangling": 1, "plot_spec": 2,
                "plot_wrangling": 3, "output_fields": 4, "input_fields": 5,
            }

            # node_id from TubeMap is safe_schema_id — match against schema_id
            # after applying the same sanitization used in BlueprintMapper
            best_rel: str | None = None
            best_priority: int = 999
            for rel, entry in ctx_map.items():
                raw_sid = entry.get("schema_id", "")
                safe_sid = raw_sid.replace(" ", "_").replace("-", "_")
                if safe_sid != node_id:
                    continue
                role = entry.get("role", "")
                priority = _ROLE_PRIORITY.get(role, 99)
                if priority < best_priority:
                    best_priority = priority
                    best_rel = rel

            if best_rel:
                ui.update_select("dataset_pipeline_selector", selected=best_rel)
                ui.js_eval(
                    "document.getElementById('btn_import_manifest').click();")
        except Exception:
            pass

    @reactive.Effect
    @reactive.event(input.btn_import_manifest)
    def _handle_manifest_import():
        """Loads a specific !include component file into the Blueprint workspace."""
        master_path = input.stored_manifest_selector()
        selected = input.dataset_pipeline_selector()

        if not master_path or not selected:
            return

        # --- Mode A: direct file load from includes map ---
        inc_map = _includes_map.get()
        if selected in inc_map:
            abs_file = Path(inc_map[selected])
            target_ds = None # [Hardening] Initialized for any-role access
            try:
                raw_text = abs_file.read_text(encoding="utf-8")
                try:
                    file_content = yaml.safe_load(raw_text) or {}
                except Exception:
                    file_content = {}

                # Extract wrangling / recipe / list from the file
                if isinstance(file_content, list):
                    wrangling = file_content
                elif isinstance(file_content, dict):
                    wrangling = file_content.get(
                        "wrangling",
                        file_content.get("recipe",
                                         file_content.get("tier1", []))
                    )
                else:
                    wrangling = []

                nodes = _parse_logic_to_nodes(wrangling, abs_file.name)
                wrangle_studio.logic_stack.set(nodes)
                wrangle_studio.active_raw_yaml.set(
                    raw_text)  # Show the actual file content

                # --- Context-aware field loading (ADR-039 / Phase 18) ---
                # Determine role from the sibling-context map built at manifest-load time.
                ctx = _component_ctx_map.get().get(selected, {})
                role = ctx.get("role", "unknown")
                sib = ctx.get("siblings", {})
                schema_id = ctx.get("schema_id", "")
                schema_type = ctx.get("schema_type", "")
                ingredients = ctx.get("ingredients", [])

                # --- Populate lineage component info ---
                wrangle_studio.active_component_info.set({
                    "role": role,
                    "schema_id": schema_id,
                    "schema_type": schema_type,
                    "ingredients": ingredients,
                    "wrangling": sib.get("wrangling"),
                })

                if role == "input_fields":
                    # This file IS the input fields — upstream is terminal (raw data)
                    in_fields = _load_fields_file(abs_file)
                    out_fields = []
                    wrangle_studio.active_upstream.set([])
                    wrangle_studio.active_downstream.set(in_fields)

                elif role == "output_fields":
                    # This file IS the output fields — downstream is consumers
                    in_fields = []
                    out_fields = _load_fields_file(abs_file)
                    wrangle_studio.active_upstream.set(out_fields)
                    wrangle_studio.active_downstream.set([])

                elif role == "wrangling":
                    # Show associated input AND output fields from sibling files
                    inp_rel = sib.get("input_fields")
                    out_rel = sib.get("output_fields")
                    in_fields = _load_fields_file(Path(inc_map[inp_rel])) \
                        if inp_rel and inp_rel in inc_map else []
                    out_fields = _load_fields_file(Path(inc_map[out_rel])) \
                        if out_rel and out_rel in inc_map else []
                    wrangle_studio.active_upstream.set(in_fields)
                    wrangle_studio.active_downstream.set(out_fields)

                elif role == "assembly":
                    # Multi-ingredient: upstream accordion — one card per ingredient.
                    # `ingredients` contains schema_ids; resolve each to its output_fields
                    # file via the sibling map (look for ctx entries with matching schema_id
                    # and role="output_fields").
                    ctx_map = _component_ctx_map.get()
                    # Build schema_id → output_fields rel_path index from ctx_map
                    id_to_out_rel = {}
                    for rel, entry in ctx_map.items():
                        if entry.get("role") == "output_fields":
                            sid = entry.get("schema_id", "")
                            if sid and sid not in id_to_out_rel:
                                id_to_out_rel[sid] = rel

                    ing_items = []
                    for ing_id in ingredients:
                        out_rel_for_ing = id_to_out_rel.get(ing_id)
                        ing_abs = inc_map.get(
                            out_rel_for_ing) if out_rel_for_ing else None
                        fields = _load_fields_file(
                            Path(ing_abs)) if ing_abs else []
                        ing_items.append({"id": ing_id, "fields": fields})

                    out_rel = sib.get("output_fields")
                    out_fields = _load_fields_file(Path(inc_map[out_rel])) \
                        if isinstance(out_rel, str) and out_rel in inc_map else []
                    in_fields = []
                    wrangle_studio.active_upstream.set(ing_items)
                    wrangle_studio.active_downstream.set(out_fields)

                elif role == "plot_spec":
                    # Upstream: output_fields for the target_dataset.
                    target_ds = file_content.get("target_dataset") \
                        if isinstance(file_content, dict) else None

                    ctx_map = _component_ctx_map.get()
                    upstream_fields: list = []
                    if target_ds:
                        # Use the module-level recursive resolver:
                        # output_fields → input_fields → transparent assembly merge
                        resolved = _resolve_fields_for_schema(target_ds, ctx_map, inc_map)
                        if resolved:
                            upstream_fields = resolved

                    in_fields = []
                    out_fields = []
                    wrangle_studio.active_upstream.set(upstream_fields)
                    wrangle_studio.active_downstream.set([])  # plot is terminal
                    # Wire Live View: set viz_id so architect_active_plot can render
                    wrangle_studio.active_viz_id.set(schema_id)

                    # [ADR-040] Surgical Materialization: ensure data exists for architect
                    if target_ds:
                        try:
                            anchor_dir = bootloader.get_location("user_sessions") / "anchors"
                            anchor_dir.mkdir(parents=True, exist_ok=True)
                            out_p = anchor_dir / f"{target_ds}.parquet"
                            # Derive project_id from the master manifest stem (not Home selector)
                            bp_project_id = Path(master_path).stem
                            if not out_p.exists():
                                print(f"🚀 [Architect] Materializing '{target_ds}' from '{bp_project_id}'")
                                orchestrator.materialize_tier1(
                                    project_id=bp_project_id,
                                    collection_id=target_ds,
                                    output_path=out_p
                                )
                            wrangle_studio.active_anchor_path.set(str(out_p))
                        except Exception as e:
                            print(f"⚠️ Surgical materialization failed: {e}")

                elif role == "plot_wrangling":
                    # Pre-plot wrangling: sits between assembly output and plot spec.
                    # Upstream: assembly output_fields for the target plot's dataset.
                    # Downstream: none (plot spec is terminal after this step).
                    # target_dataset read from file_content if available; otherwise empty.
                    target_ds = file_content.get("target_dataset") \
                        if isinstance(file_content, dict) else None

                    ctx_map = _component_ctx_map.get()
                    upstream_fields: list = []
                    if target_ds:
                        resolved = _resolve_fields_for_schema(target_ds, ctx_map, inc_map)
                        if resolved:
                            upstream_fields = resolved
                    
                    # Proactive materialization for wrangling preview
                    if target_ds:
                        try:
                            anchor_dir = bootloader.get_location("user_sessions") / "anchors"
                            anchor_dir.mkdir(parents=True, exist_ok=True)
                            out_p = anchor_dir / f"{target_ds}.parquet"
                            bp_project_id = Path(master_path).stem
                            if not out_p.exists():
                                orchestrator.materialize_tier1(
                                    project_id=bp_project_id,
                                    collection_id=target_ds,
                                    output_path=out_p
                                )
                            wrangle_studio.active_anchor_path.set(str(out_p))
                        except Exception: pass

                    # Extract wrangling steps from file content
                    if isinstance(file_content, list):
                        wrangling = file_content
                    elif isinstance(file_content, dict):
                        wrangling = file_content.get(
                            "wrangling",
                            file_content.get("recipe",
                                             file_content.get("tier1", [])))
                    else:
                        wrangling = []
                    nodes = _parse_logic_to_nodes(wrangling, abs_file.name)
                    wrangle_studio.logic_stack.set(nodes)

                    in_fields = []
                    out_fields = []
                    wrangle_studio.active_upstream.set(upstream_fields)
                    wrangle_studio.active_downstream.set([])

                else:
                    # Fallback: try standard wrapper keys then empty
                    in_fields = file_content.get("input_fields", []) \
                        if isinstance(file_content, dict) else []
                    out_fields = file_content.get("output_fields", []) \
                        if isinstance(file_content, dict) else []
                    wrangle_studio.active_upstream.set(in_fields)
                    wrangle_studio.active_downstream.set(out_fields)

                wrangle_studio.active_fields.set(
                    {"input": in_fields, "output": out_fields})

                # --- Build and set the lineage chain for the Rail ---
                chain = _build_lineage_chain(
                    selected, _component_ctx_map.get(), target_ds_override=target_ds)
                wrangle_studio.active_lineage_chain.set(chain)
                # Store master path so architect_active_plot can load the full manifest
                wrangle_studio.active_manifest_path.set(master_path)

                # --- Refresh TubeMap with active node highlight ---
                # sync_blueprint_mapper only fires on manifest change; re-generate
                # here so the selected schema_id gets the activeNode highlight.
                try:
                    cfg_for_map = ConfigManager(master_path)
                    mapper = BlueprintMapper(cfg_for_map.raw_config, active_node=schema_id)
                    wrangle_studio.active_tubemap_mermaid.set(mapper.generate_mermaid())
                except Exception as _e:
                    print(f"[TubeMap highlight] Failed: {_e}")

                msg = f"✅ Loaded '{abs_file.name}' ({len(nodes)} step(s))"
                ui.notification_show(msg, type="message")
            except Exception as e:
                ui.notification_show(
                    f"❌ Failed to load file: {e}", type="error")
            return

        # --- Mode B: fallback — treat selected as component ID via ConfigManager ---
        if not Path(master_path).exists():
            return
        try:
            cfg = ConfigManager(master_path)
            wrangling = _extract_wrangling_for_id(cfg, selected)
            nodes = _parse_logic_to_nodes(wrangling, f"Master: {selected}")
            wrangle_studio.logic_stack.set(nodes)
            wrangle_studio.active_raw_yaml.set(
                yaml.dump(cfg.raw_config, default_flow_style=False, sort_keys=False))

            target = (cfg.raw_config.get("data_schemas", {}).get(selected)
                      or cfg.raw_config.get("additional_datasets_schemas", {}).get(selected)
                      or cfg.raw_config.get("assembly_manifests", {}).get(selected))
            in_f = target.get("input_fields", []) if isinstance(
                target, dict) else []
            out_f = target.get("output_fields", []) if isinstance(
                target, dict) else []
            wrangle_studio.active_fields.set({"input": in_f, "output": out_f})

            ui.notification_show(
                f"✅ Imported {len(nodes)} steps from '{selected}'", type="message")
        except Exception as e:
            ui.notification_show(f"❌ Import failed: {e}", type="error")

    @reactive.Effect
    @reactive.event(input.btn_normalize_fields)
    def _handle_normalize_fields():
        """Normalize legacy {column: type} input_fields/output_fields in the active component file.
        Triggered by the '⚙️ Fix Format' button in the Interface (Fields) tab.
        Writes the file in-place (with .bak backup) then reloads the workspace.
        """
        from app.assets.normalize_manifest_fields import normalize_file as _normalize_file

        selected = _safe_input(input, "dataset_pipeline_selector", None)
        inc_map = _includes_map.get()

        if not selected or selected not in inc_map:
            ui.notification_show(
                "⚠️ No component file loaded. Import a blueprint component first.",
                type="warning"
            )
            return

        abs_path = Path(inc_map[selected])
        changes, success, message = _normalize_file(abs_path, write=True)

        if not success:
            ui.notification_show(
                f"❌ Normalize failed: {message}", type="error")
            return

        if not changes:
            ui.notification_show(f"ℹ️ {message}", type="message")
            return

        # Reload the file into the workspace so the viewers refresh immediately
        try:
            raw_text = abs_path.read_text(encoding="utf-8")
            file_content = yaml.safe_load(raw_text) or {}
            in_fields = file_content.get("input_fields", []) \
                if isinstance(file_content, dict) else []
            out_fields = file_content.get("output_fields", []) \
                if isinstance(file_content, dict) else []
            wrangle_studio.active_fields.set(
                {"input": in_fields, "output": out_fields})
            wrangle_studio.active_raw_yaml.set(raw_text)
        except Exception as e:
            print(f"[_handle_normalize_fields] Reload failed after write: {e}")

        ui.notification_show(f"✅ {message}", type="success")

    @reactive.Effect
    @reactive.event(input.btn_upload_replace)
    def _handle_upload_replace():
        file_info = input.manifest_uploader()
        if not file_info:
            return
        try:
            cfg = ConfigManager(file_info[0]["datapath"])
            wrangling = cfg.raw_config.get("wrangling", {})
            nodes = _parse_logic_to_nodes(wrangling, "Uploaded (Replace)")
            wrangle_studio.logic_stack.set(nodes)
            ui.notification_show("✅ Stack Replaced.", type="success")
        except Exception as e:
            ui.notification_show(f"❌ Upload failed: {e}", type="error")

    @reactive.Effect
    @reactive.event(input.btn_upload_append)
    def _handle_upload_append():
        file_info = input.manifest_uploader()
        if not file_info:
            return
        try:
            cfg = ConfigManager(file_info[0]["datapath"])
            wrangling = cfg.raw_config.get("wrangling", {})
            new_nodes = _parse_logic_to_nodes(wrangling, "Uploaded (Append)")
            current_stack = wrangle_studio.logic_stack.get()
            wrangle_studio.logic_stack.set(current_stack + new_nodes)
            ui.notification_show(
                f"➕ Appended {len(new_nodes)} nodes.", type="success")
        except Exception as e:
            ui.notification_show(f"❌ Append failed: {e}", type="error")

    def _extract_wrangling_for_id(cfg, lid):
        """Helper to find wrangling block in complex manifest."""
        target = cfg.raw_config.get("data_schemas", {}).get(lid)
        if not target:
            target = cfg.raw_config.get(
                "additional_datasets_schemas", {}).get(lid)
        if not target:
            target = cfg.raw_config.get("assembly_manifests", {}).get(lid)
        if not target and lid == "metadata_schema":
            target = cfg.raw_config.get("metadata_schema")

        if not target:
            return {}
        return target.get("wrangling", target.get("recipe", {}))

    def _parse_logic_to_nodes(wrangling, source_name):
        """
        Normalizes potentially flat manifest nodes into structured UI nodes.
        ADR-031: Supports both Structure (params: {}) and Flat (top-level keys) formats.
        """
        nodes = []
        raw_list = []

        if isinstance(wrangling, list):
            raw_list = wrangling
        elif isinstance(wrangling, dict):
            # Extract from nested tiers if present
            for tier in ["tier1", "tier2", "tier3"]:
                raw_list.extend(wrangling.get(tier, []))

        for node in raw_list:
            if not isinstance(node, dict):
                continue

            n = node.copy()
            action = n.pop("action", "unknown_action")
            comment = n.pop("comment", source_name)

            # If 'params' already exists, use it; otherwise, everything else becomes params
            params = n.pop("params", n)

            nodes.append({
                "action": action,
                "params": params,
                "comment": comment
            })

        return nodes

    @reactive.Effect
    @reactive.event(input.btn_save_internal)
    def _handle_manifest_save_internal():
        path_str = input.stored_manifest_selector()
        if not path_str or not Path(path_str).exists():
            return
        try:
            with open(path_str, "r") as f:
                content = yaml.safe_load(f) or {}
            nodes = wrangle_studio.logic_stack.get()
            if "wrangling" not in content:
                content["wrangling"] = {}
            content["wrangling"]["tier1"] = []
            content["wrangling"]["tier2"] = []
            content["wrangling"]["tier3"] = nodes
            with open(path_str, "w") as f:
                yaml.dump(content, f, default_flow_style=False,
                          sort_keys=False)
            ui.notification_show(
                f"✅ Saved to {Path(path_str).name}", type="success")
        except Exception as e:
            ui.notification_show(f"❌ Save failed: {e}", type="error")

    @render.download(filename=lambda: f"exported_manifest_{datetime.now().strftime('%Y%m%d_%H%M%S')}.yaml")
    def btn_download_manifest():
        nodes = wrangle_studio.logic_stack.get()
        manifest_data = {"wrangling": {
            "tier1": [], "tier2": [], "tier3": nodes}}
        import io
        buf = io.StringIO()
        yaml.dump(manifest_data, buf,
                  default_flow_style=False, sort_keys=False)
        yield buf.getvalue()

    @render.ui
    def comparison_mode_toggle_ui():
        p = current_persona.get()
        if p in ["pipeline_exploration_advanced", "project_independent", "developer"]:
            return ui.div(ui.input_switch("comparison_mode", "Comparison Mode", value=False),
                          class_="d-flex align-items-center me-3", style="height: 36px; padding-top: 4px;")
        return ui.div()
