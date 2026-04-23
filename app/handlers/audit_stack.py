"""app/handlers/audit_stack.py
Pipeline Audit Shiny wiring (ADR-044 / ADR-045).

Entry point:
    define_server(input, output, session, *,
                  wrangle_studio, recipe_pending, snapshot_recipe,
                  active_cfg, active_collection_id)

Concern: T2/T3 audit node rendering, btn_apply gate, recipe change tracking,
         recipe_pending_badge_ui.
Two-Category Law (ADR-045): This file contains @render.* and @reactive.*
decorators only. It MUST NOT be imported by non-Shiny contexts.
"""

from __future__ import annotations

from shiny import reactive, render, ui

from transformer.data_wrangler import DataWrangler


def define_server(input, output, session, *,
                  wrangle_studio, recipe_pending, snapshot_recipe,
                  active_cfg, active_collection_id):
    """Register all Pipeline Audit reactive handlers.

    Parameters
    ----------
    wrangle_studio : WrangleStudio
        Shared state: logic_stack, apply_logic.
    recipe_pending : reactive.Value[bool]
        Shared flag: True when stack has unsaved changes.
    snapshot_recipe : reactive.Value[list]
        Frozen copy of logic_stack at last btn_apply press.
    active_cfg : callable → ConfigManager
        Zero-arg callable returning the active manifest config.
    active_collection_id : callable → str
        Zero-arg callable returning the active collection ID.
    """

    @reactive.Effect
    @reactive.event(input.btn_apply)
    def handle_apply():
        snapshot_recipe.set(wrangle_studio.logic_stack.get())

    @reactive.Effect
    def track_recipe_changes():
        _ = wrangle_studio.apply_logic
        recipe_pending.set(True)

    @output
    @render.ui
    def recipe_pending_badge_ui():
        if recipe_pending.get():
            return ui.div("⏳ Pending", class_="recipe-pending-badge text-center")
        return ui.div()

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
