"""app/handlers/audit_stack.py
Pipeline Audit Shiny wiring (ADR-044 / ADR-045, Phase 22-C).

Entry point:
    define_server(input, output, session, *,
                  wrangle_studio, recipe_pending, snapshot_recipe,
                  active_cfg, active_collection_id,
                  home_state=None, session_manager=None)

Concern: T2 violet node rendering, T3 Yellow RecipeNode rendering, btn_apply
         gatekeeper (blocks if any required reason field is empty), recipe
         change tracking, recipe_pending_badge_ui.

Two-Category Law (ADR-045): This file contains @render.* and @reactive.*
decorators only. It MUST NOT be imported by non-Shiny contexts.
"""

from __future__ import annotations

# @deps
# provides: function:define_server (audit_stack)
# consumes: app/modules/wrangle_studio.py, app/modules/session_manager.py, libs/transformer/src/transformer/data_wrangler.py
# consumed_by: app/src/server.py
# doc: .agents/rules/ui_implementation_contract.md#12a-12c, .antigravity/knowledge/architecture_decisions.md#ADR-044
# @end_deps

from shiny import reactive, render, ui

from transformer.data_wrangler import DataWrangler
from app.modules.session_manager import (
    make_recipe_node,
    gatekeeper_blocked,
)

# Node type display config: (icon, label)
_NODE_META = {
    "filter_row":        ("🔍", "Row Filter"),
    "exclusion_row":     ("🚫", "Exclusion"),
    "drop_column":       ("✂️",  "Drop Column"),
    "aesthetic_override":("🎨", "Plot Style"),
    "developer_raw_yaml":("⚙️",  "Dev Fragment"),
}

_REASON_REQUIRED = {"filter_row", "exclusion_row", "drop_column", "developer_raw_yaml"}


def _safe_input_suffix(node_id: str) -> str:
    """Sanitize a RecipeNode id for use in a Shiny input ID.

    Shiny input IDs allow only [A-Za-z0-9_]. Legacy ghost files may contain
    UUID4 strings with hyphens, so we replace any invalid char with '_'.
    Current make_recipe_node() emits hex (no hyphens), so this is a no-op for
    new nodes.
    """
    return "".join(c if c.isalnum() or c == "_" else "_" for c in node_id)


_OP_SYMBOL = {"eq": "=", "ne": "≠", "gt": ">", "ge": "≥",
              "lt": "<", "le": "≤", "in": "∈", "not_in": "∉"}


def _format_value(val) -> str:
    """Render a filter value compactly. Lists become {a, b, c}; long strings truncate."""
    if isinstance(val, (list, tuple)):
        items = [str(v) for v in val]
        if len(items) <= 3:
            return "{" + ", ".join(items) + "}"
        return "{" + ", ".join(items[:3]) + f", … +{len(items)-3}}}"
    s = str(val)
    return s if len(s) <= 30 else s[:30] + "…"


def _params_summary(node: dict) -> str:
    p = node.get("params", {})
    nt = node.get("node_type", "")
    if nt == "filter_row":
        col = p.get("column", "?")
        op = _OP_SYMBOL.get(p.get("op", "eq"), p.get("op", "eq"))
        val = _format_value(p.get("value", ""))
        return f"{col} {op} {val}"
    if nt == "exclusion_row":
        col = p.get("column", "?")
        return f"{col} = {_format_value(p.get('value', ''))}"
    if nt == "drop_column":
        return str(p.get("column", ""))
    if nt == "aesthetic_override":
        keys = [k for k in ("fill", "colour", "alpha", "shape") if k in p]
        return ", ".join(keys) if keys else "overrides"
    if nt == "developer_raw_yaml":
        frag = str(p.get("yaml_fragment", ""))
        return frag[:40] + "…" if len(frag) > 40 else frag
    return str(p)[:40]


def define_server(input, output, session, *,
                  wrangle_studio, recipe_pending, snapshot_recipe,
                  active_cfg, active_collection_id,
                  home_state=None, session_manager=None):
    """Register all Pipeline Audit reactive handlers."""

    # ------------------------------------------------------------------
    # btn_apply: commit T3 recipe, ghost save, release gatekeeper
    # ------------------------------------------------------------------

    @reactive.Effect
    @reactive.event(input.btn_apply)
    def handle_apply():
        if home_state is None:
            snapshot_recipe.set(wrangle_studio.logic_stack.get())
            recipe_pending.set(False)
            return

        state = home_state.get()
        # Pull the LATEST reason text from the live input fields before gatekeeping.
        # Done here (not in a continuously-firing Effect) so typing in the reason
        # box does not re-render the right sidebar on every keystroke (§14 R1/R3).
        t3_recipe = [dict(n) for n in state.get("t3_recipe", [])]
        pending = [dict(n) for n in state.get("_pending_t3_nodes", [])]
        for node_list in (t3_recipe, pending):
            for node in node_list:
                nid = node.get("id", "")
                if not nid:
                    continue
                sid = _safe_input_suffix(nid)
                try:
                    val = getattr(input, f"t3_reason_{sid}")()
                    if val is not None:
                        node["reason"] = val
                except Exception:
                    pass

        all_nodes = t3_recipe + pending

        blocked = gatekeeper_blocked(all_nodes)
        if blocked:
            ui.notification_show(
                f"⛔ {len(blocked)} node(s) require a reason before applying.",
                type="error", duration=6,
            )
            # Persist the reason edits even when blocked so the user keeps their text.
            home_state.set({**state, "t3_recipe": t3_recipe, "_pending_t3_nodes": pending})
            return

        new_recipe = t3_recipe + pending
        # Bump t3_apply_count so home_theater clears the left-panel filters
        # (they have been committed to T3 — no point in keeping the same rows
        # available for re-apply).
        new_state = {
            **state,
            "t3_recipe": new_recipe,
            "_pending_t3_nodes": [],
            "t3_apply_count": int(state.get("t3_apply_count", 0)) + 1,
        }
        home_state.set(new_state)

        if session_manager is not None:
            _write_t3_ghost(new_state, session_manager)

        snapshot_recipe.set(wrangle_studio.logic_stack.get())
        recipe_pending.set(False)
        ui.notification_show(
            f"✅ T3 recipe applied — {len(new_recipe)} node(s) in pipeline.",
            type="message", duration=4,
        )

    # ------------------------------------------------------------------
    # Track recipe changes (pending badge)
    # ------------------------------------------------------------------

    @reactive.Effect
    def track_recipe_changes():
        _ = wrangle_studio.apply_logic
        recipe_pending.set(True)

    # ------------------------------------------------------------------
    # recipe_pending_badge_ui
    # ------------------------------------------------------------------

    @output
    @render.ui
    def recipe_pending_badge_ui():
        if recipe_pending.get():
            return ui.div("⏳ Pending", class_="recipe-pending-badge text-center")
        return ui.div()

    # ------------------------------------------------------------------
    # audit_nodes_tier2 — Violet nodes (immutable T1/T2 steps)
    # ------------------------------------------------------------------

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
                ui.div(f"[Tier 2] {action}: {label}", class_="audit-node-tier2"),
                f"Action: {action}", placement="left"
            ))
        return ui.div(*nodes)

    # ------------------------------------------------------------------
    # audit_nodes_tier3 — Yellow RecipeNodes (T3 committed + pending)
    # ------------------------------------------------------------------

    @output
    @render.ui
    def audit_nodes_tier3():
        cfg = active_cfg()
        collection_id = active_collection_id()

        header_nodes = [
            ui.div(f"Project: {cfg.raw_config.get('id')}", class_="audit-node-tier2"),
            ui.div(f"Collection: {collection_id}", class_="audit-node-tier2"),
        ]

        if home_state is None:
            # Legacy fallback
            active_nodes = wrangle_studio.logic_stack.get()
            if not active_nodes:
                return ui.div(*header_nodes)
            header_nodes.append(ui.hr())
            header_nodes.append(ui.h6("Session Transformations (Tier 3)"))
            for i, node in enumerate(active_nodes):
                action = node.get("action", "unknown")
                comment = node.get("comment", "No comment")
                header_nodes.append(ui.tooltip(
                    ui.div(
                        ui.div(f"⚡ {action}", class_="fw-bold"),
                        ui.div(f"💬 {comment}", style="font-size:0.8em;"),
                        class_="audit-node-tier3",
                    ),
                    f"Action: {action}", placement="left", id=f"node_tt_{i}"
                ))
            return ui.div(*header_nodes)

        state = home_state.get()
        t3_recipe = state.get("t3_recipe", [])
        pending = state.get("_pending_t3_nodes", [])
        all_nodes = t3_recipe + pending

        if not all_nodes:
            return ui.div(
                *header_nodes,
                ui.div("No T3 adjustments yet.", class_="text-muted",
                       style="font-size:0.8em; padding:4px;"),
            )

        blocked_ids = set(gatekeeper_blocked(all_nodes))
        header_nodes.append(ui.hr())
        header_nodes.append(
            ui.div(
                ui.h6("My Adjustments (Tier 3)", style="margin:0; flex:1;"),
                ui.span(
                    f"{len(blocked_ids)} need reason",
                    style="font-size:0.72em; color:#dc3545;"
                ) if blocked_ids else ui.span(),
                style="display:flex; align-items:center; gap:6px; margin-bottom:4px;",
            )
        )

        node_els = []
        for node in reversed(all_nodes):  # newest first
            is_pending = node in pending
            is_active = node.get("active", True)
            nt = node.get("node_type", "unknown")
            icon, label = _NODE_META.get(nt, ("❓", nt))
            summary = _params_summary(node)
            reason = node.get("reason", "")
            needs_reason = nt in _REASON_REQUIRED
            reason_empty = needs_reason and not reason.strip()
            node_id = node.get("id", "")
            scope = node.get("plot_scope", "__all__")

            base_style = "opacity:0.45; text-decoration:line-through;" if not is_active else ""

            pending_badge = ui.span(
                "PENDING",
                style="font-size:0.65em; background:#ffc107; border-radius:3px; padding:1px 4px; margin-left:4px;"
            ) if is_pending else ui.span()

            id_suffix = _safe_input_suffix(node_id)

            if needs_reason and is_active:
                reason_field = ui.div(
                    ui.input_text(
                        f"t3_reason_{id_suffix}",
                        label=None,
                        value=reason,
                        placeholder="Reason (required)…",
                    ),
                    style=(
                        "margin-top:2px;"
                        + (" border:1px solid #dc3545; border-radius:4px;" if reason_empty else "")
                    ),
                )
            else:
                reason_field = ui.span()

            node_els.append(
                ui.div(
                    ui.div(
                        ui.span(f"{icon} {label}", class_="fw-bold",
                               style="font-size:0.82em;"),
                        pending_badge,
                        ui.input_action_button(
                            f"t3_delete_{id_suffix}", "🗑",
                            class_="btn btn-sm btn-link p-0",
                            style="margin-left:auto; font-size:0.95em; color:#dc3545; line-height:1;",
                            title="Delete this audit node",
                        ),
                        style="display:flex; align-items:center; gap:4px;",
                    ),
                    ui.div(
                        summary,
                        style=(
                            "font-size:0.82em; color:#212529; margin-top:2px; "
                            "font-family:ui-monospace,SFMono-Regular,Menlo,monospace; "
                            "background:#fff8d6; padding:2px 6px; border-radius:3px; "
                            "word-break:break-word;"
                        ),
                    ),
                    ui.div(
                        f"Scope: {scope}",
                        style="font-size:0.68em; color:#888;"
                    ) if scope != "__all__" else ui.span(),
                    reason_field,
                    class_="audit-node-tier3",
                    style=base_style,
                )
            )

        return ui.div(*header_nodes, *node_els)

    # ------------------------------------------------------------------
    # Reason inputs are NOT eagerly synced to home_state (would re-render the
    # right sidebar on every keystroke, destroying the input mid-typing).
    # Reasons are pulled from input.t3_reason_<id> at btn_apply time — see
    # handle_apply() above. §14 R1/R3 — see ui_implementation_contract.md.
    #
    # _nodes_with_live_reasons(): non-mutating overlay used by the apply-button
    # renders. Reads each reason input and returns a fresh node list with the
    # current text merged in, so the gatekeeper accurately reflects live state
    # WITHOUT writing to home_state.
    # ------------------------------------------------------------------

    def _nodes_with_live_reasons() -> list[dict]:
        if home_state is None:
            return []
        state = home_state.get()
        merged: list[dict] = []
        for n in state.get("t3_recipe", []) + state.get("_pending_t3_nodes", []):
            n = dict(n)
            nid = n.get("id", "")
            if nid:
                sid = _safe_input_suffix(nid)
                try:
                    val = getattr(input, f"t3_reason_{sid}")()
                    if val is not None:
                        n["reason"] = val
                except Exception:
                    pass
            merged.append(n)
        return merged

    # ------------------------------------------------------------------
    # Delete-node handlers — permanent removal from t3_recipe / _pending_t3_nodes
    # ------------------------------------------------------------------
    # We track click counts per-node-id between effect firings; nodes whose
    # click count increased since last seen are removed entirely. This is
    # idempotent — re-clicking a deleted node's ID does nothing because the
    # ID is no longer in state.

    _last_delete_clicks: dict[str, int] = {}

    @reactive.Effect
    def _handle_delete():
        if home_state is None:
            return
        state = home_state.get()
        t3_recipe = list(state.get("t3_recipe", []))
        pending = list(state.get("_pending_t3_nodes", []))

        ids_to_delete: set[str] = set()
        for n in t3_recipe + pending:
            nid = n.get("id", "")
            if not nid:
                continue
            sid = _safe_input_suffix(nid)
            try:
                clicks = int(getattr(input, f"t3_delete_{sid}")() or 0)
            except Exception:
                continue
            prev = _last_delete_clicks.get(nid, 0)
            if clicks > prev:
                ids_to_delete.add(nid)
            _last_delete_clicks[nid] = clicks

        if not ids_to_delete:
            return

        new_recipe = [n for n in t3_recipe if n.get("id") not in ids_to_delete]
        new_pending = [n for n in pending if n.get("id") not in ids_to_delete]
        home_state.set({
            **state,
            "t3_recipe": new_recipe,
            "_pending_t3_nodes": new_pending,
        })
        ui.notification_show(
            f"🗑 {len(ids_to_delete)} audit node(s) deleted.",
            type="message", duration=3,
        )

    # ------------------------------------------------------------------
    # audit_stack_tools_ui — gatekeeper-aware Apply button (right sidebar bottom)
    # ------------------------------------------------------------------
    # Right sidebar is now audit-trail only: T3 nodes are authored in the left
    # panel (filter rows) or via Gallery clone. No Add buttons here.

    @output
    @render.ui
    def audit_stack_tools_ui():
        if home_state is None:
            return ui.div(
                ui.input_action_button("btn_apply", "Apply", class_="btn-primary w-100"),
                class_="p-2",
            )

        all_nodes = _nodes_with_live_reasons()
        blocked = gatekeeper_blocked(all_nodes)

        apply_btn = ui.tooltip(
            ui.input_action_button(
                "btn_apply", "Apply ⛔",
                class_="btn-secondary w-100",
                disabled=True,
            ),
            f"{len(blocked)} node(s) missing reason — fill in reason fields above.",
            placement="top",
        ) if blocked else ui.input_action_button(
            "btn_apply", "Apply",
            class_="btn-primary w-100",
        )

        return ui.div(
            ui.hr(style="margin:4px 0;"),
            apply_btn,
            class_="p-2",
        )

    # ------------------------------------------------------------------
    # btn_apply_ui — gatekeeper-aware Apply button (standalone output)
    # ------------------------------------------------------------------

    @output
    @render.ui
    def btn_apply_ui():
        if home_state is None:
            return ui.input_action_button("btn_apply", "Apply", class_="btn-primary w-100")

        all_nodes = _nodes_with_live_reasons()
        blocked = gatekeeper_blocked(all_nodes)

        if blocked:
            return ui.tooltip(
                ui.input_action_button(
                    "btn_apply", "Apply ⛔",
                    class_="btn-secondary w-100",
                    disabled=True,
                ),
                f"{len(blocked)} node(s) missing reason",
                placement="top",
            )
        return ui.input_action_button("btn_apply", "Apply", class_="btn-primary w-100")


# ---------------------------------------------------------------------------
# Private helpers
# ---------------------------------------------------------------------------

def _write_t3_ghost(state: dict, session_manager) -> None:
    msig = state.get("manifest_sha256") or ""
    dbh = state.get("data_batch_hash") or ""
    if not msig or not dbh:
        return
    from app.modules.session_manager import SessionManager
    session_key = SessionManager.compute_session_key(msig, dbh)
    try:
        session_manager.write_t3_ghost(
            session_key=session_key,
            manifest_id=state.get("manifest_id", ""),
            manifest_sha256=msig,
            data_batch_hash=dbh,
            tier_toggle=state.get("tier_toggle", "T2"),
            t3_recipe=state.get("t3_recipe", []),
            t3_plot_overrides=state.get("t3_plot_overrides", {}),
            label=state.get("t3_ghost_label", ""),
        )
    except Exception:
        pass
