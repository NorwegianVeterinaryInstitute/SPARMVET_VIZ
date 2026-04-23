"""app/handlers/gallery_handlers.py
Gallery Shiny wiring (ADR-037 / ADR-045).

Entry point: define_server(input, output, session, *, bootloader, wrangle_studio, safe_input)

Concern: Gallery filtering, preview rendering, recipe clone, gallery_browser_anchor.
Two-Category Law (ADR-045): This file contains @render.* and @reactive.* decorators
only. It MUST NOT be imported by non-Shiny contexts.
"""

from __future__ import annotations

# @deps
# provides: function:define_server (gallery_handlers)
# consumes: app/modules/wrangle_studio.py, libs/transformer/src/transformer/data_wrangler.py
# consumed_by: app/src/server.py
# doc: .antigravity/knowledge/architecture_decisions.md#ADR-037, .antigravity/knowledge/architecture_decisions.md#ADR-045
# @end_deps

import base64
import json
from pathlib import Path

import polars as pl
import yaml
from shiny import reactive, render, ui

from transformer.data_wrangler import DataWrangler


def define_server(input, output, session, *, bootloader, wrangle_studio, safe_input):
    """Register all Gallery reactive handlers.

    Parameters
    ----------
    bootloader : Bootloader
        Path Authority instance (ADR-031).
    wrangle_studio : WrangleStudio
        Shared WrangleStudio state (receives cloned recipes).
    safe_input : callable
        Shared utility: safe_input(input_obj, key, default) → value.
    """

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
        recipe_id = safe_input(input, "gallery_recipe_select", None)
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
        rid = safe_input(input, "gallery_recipe_select", None)
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
