"""app/handlers/session_handlers.py
Session Management panel + import/restore/delete reactive handlers.

Extracted from home_theater.py in Phase 24-B (ADR-051).

Two-Category Law (ADR-045): this module contains @render.* / @reactive.*
decorators only. It MUST NOT be imported by non-Shiny contexts.
"""

from __future__ import annotations

# @deps
# provides: function:define_session_server, output:session_management_ui
# consumes: shiny, pathlib
# consumed_by: app/handlers/home_theater.py
# doc: .antigravity/knowledge/architecture_decisions.md#ADR-045, .antigravity/knowledge/architecture_decisions.md#ADR-051
# @end_deps

from pathlib import Path

from shiny import reactive, render, ui


def define_session_server(input, output, session, *,
                          session_manager, current_persona, home_state):
    """Register session-management UI + import/restore/delete reactive handlers.

    Parameters
    ----------
    session_manager : SessionManager | None
        Session persistence facade. May be None when launched without persistence.
    current_persona : reactive.Value[str]
        Active launch persona (hyphen form, e.g. "pipeline-exploration-advanced").
    home_state : reactive.Value[dict] | None
        Shared home dashboard state (manifest_sha256, t3_recipe_by_plot, etc.).
    """

    # ── 22-D: Session Management Panel ────────────────────────────────────────

    @output
    @render.ui
    def session_management_ui():
        """Session Management panel — persona-name gated for now.

        TODO (PERSONA-1 doc-drift): three sources disagree on whether
        pipeline-exploration-simple should see this panel:
          - Old code hid it (advanced+ only)
          - persona_traceability_matrix.md says visible
          - rules_persona_feature_flags.md + template say visible
        Switching to bootloader.is_enabled('session_management_enabled')
        would flip visibility for `simple`. Held off pending doc alignment;
        see PERSONA-1 in tasks.md.
        """
        persona = current_persona.get()
        advanced_personas = {
            "pipeline-exploration-advanced", "project-independent", "developer"
        }
        if persona not in advanced_personas:
            return ui.div()

        if session_manager is None:
            return ui.div(ui.p("Session manager unavailable.", class_="text-muted small"))

        sessions = session_manager.list_all_sessions()

        header = ui.div(
            ui.p("Session Management", class_="ultra-small fw-bold mb-1"),
            ui.div(
                ui.input_file(
                    "session_import_upload", None,
                    accept=[".zip"], multiple=False,
                ),
                ui.tags.small("Import a .zip session", class_="text-muted"),
                class_="upload-row mb-1",
            ),
        )

        if not sessions:
            return ui.div(
                header,
                ui.p("No saved sessions.", class_="text-muted small"),
            )

        # Group sessions by manifest_sha256[:12]
        groups: dict[str, list] = {}
        for s in sessions:
            grp = s.get("manifest_sha256", "")[:12] or "unknown"
            groups.setdefault(grp, []).append(s)

        cards = []
        for grp_key, grp_sessions in groups.items():
            manifest_id = grp_sessions[0].get("manifest_id", grp_key)
            group_panels = []
            for s in grp_sessions:
                sk = s["session_key"]
                batch_short = s.get("data_batch_hash", "")[:8] or "?"
                t3_count = s.get("t3_count", 0)
                last_saved = s.get("latest_t3_saved_at") or s.get("assembled_at", "")
                label = session_manager.get_session_label(sk) or "(no label)"

                group_panels.append(
                    ui.div(
                        ui.div(
                            ui.tags.small(
                                f"Batch: {batch_short} · {t3_count} save(s)",
                                class_="text-muted d-block",
                                style="font-size:0.7em;",
                            ),
                            ui.tags.small(
                                label,
                                style="font-size:0.72em; font-style:italic; color:#555;",
                            ),
                            ui.tags.small(
                                last_saved[:16].replace("T", " ") if last_saved else "—",
                                class_="text-muted d-block",
                                style="font-size:0.68em;",
                            ),
                        ),
                        ui.div(
                            ui.input_action_button(
                                f"session_restore_{sk.replace(':', '_')}",
                                "Restore",
                                class_="btn-primary btn-sm",
                                style="font-size:0.72em; padding:1px 6px;",
                            ),
                            ui.download_button(
                                f"session_export_{sk.replace(':', '_')}",
                                "Export",
                                class_="btn-outline-secondary btn-sm",
                                style="font-size:0.72em; padding:1px 6px;",
                            ),
                            ui.input_action_button(
                                f"session_delete_{sk.replace(':', '_')}",
                                "✕",
                                class_="btn-outline-danger btn-sm",
                                style="font-size:0.72em; padding:1px 4px;",
                            ),
                            class_="d-flex gap-1 mt-1 flex-wrap",
                        ),
                        class_="spv-panel p-2 mb-1",
                        style="font-size:0.78em;",
                    )
                )

            cards.append(
                ui.accordion_panel(
                    f"📁 {manifest_id}",
                    *group_panels,
                )
            )

        return ui.div(
            header,
            ui.accordion(*cards, id="session_groups_accordion", multiple=True),
        )

    # Session import handler
    @reactive.Effect
    @reactive.event(input.session_import_upload)
    def _handle_session_import():
        if session_manager is None:
            return
        file_info = input.session_import_upload()
        if not file_info:
            return
        try:
            zip_bytes = Path(file_info[0]["datapath"]).read_bytes()
            restored_key = session_manager.import_session_zip(zip_bytes)
            ui.notification_show(
                f"✅ Session imported: {restored_key}", type="message", duration=5
            )
        except Exception as e:
            ui.notification_show(f"❌ Import failed: {e}", type="error", duration=8)

    # Session restore + delete handlers are registered dynamically per session.
    # Because Shiny requires input IDs to be registered at render time, we use
    # a single reactive scan over all known sessions to catch clicks.
    @reactive.Effect
    def _handle_session_actions():
        if session_manager is None or home_state is None:
            return
        sessions = session_manager.list_all_sessions()
        for s in sessions:
            sk = s["session_key"]
            safe_sk = sk.replace(":", "_")

            # Restore
            restore_id = f"session_restore_{safe_sk}"
            try:
                clicks = getattr(input, restore_id)()
                if clicks and clicks > 0:
                    _restore_session(sk)
            except Exception:
                pass

            # Delete
            delete_id = f"session_delete_{safe_sk}"
            try:
                clicks = getattr(input, delete_id)()
                if clicks and clicks > 0:
                    session_manager.delete_session(sk)
                    ui.notification_show(
                        f"🗑 Session deleted: {sk[:24]}…",
                        type="message", duration=4,
                    )
            except Exception:
                pass

    def _restore_session(session_key: str) -> None:
        """Run T1/T2 restore + open T3 ghost picker notification."""
        if session_manager is None or home_state is None:
            return

        ghost = session_manager.read_assembly_ghost(session_key)
        if ghost is None:
            ui.notification_show("❌ Session assembly record not found.", type="error", duration=6)
            return

        # Check manifest SHA256 vs current
        state = home_state.get()
        current_msig = state.get("manifest_sha256") or ""
        saved_msig = ghost.get("manifest_sha256", "")
        if current_msig and saved_msig and current_msig != saved_msig:
            ui.notification_show(
                "⚠️ Session was saved against a different manifest version. "
                "Recipe nodes may not match current columns.",
                type="warning", duration=8,
            )

        # Load T3 ghosts list for this session
        t3_ghosts = session_manager.list_t3_ghosts(session_key)
        if t3_ghosts:
            # Restore most-recent T3 ghost into home_state.
            # Phase 22-J: list_t3_ghosts emits both flat t3_recipe (legacy) and
            # t3_recipe_by_plot (current). Legacy ghosts have nodes bucketed
            # under "__legacy__" — they're surfaced as orphans in the audit
            # panel until the user re-targets or deletes them.
            latest = t3_ghosts[0]
            by_plot = latest.get("t3_recipe_by_plot") or {}
            new_state = {
                **state,
                "t3_recipe_by_plot": by_plot,
                "t3_plot_overrides": latest.get("t3_plot_overrides", {}),
                "tier_toggle": latest.get("tier_toggle", "T2"),
                "t3_ghost_file": latest.get("file", ""),
                "t3_ghost_saved_at": latest.get("saved_at", ""),
                "_pending_t3_nodes": [],
            }
            home_state.set(new_state)
            legacy_n = len(by_plot.get("__legacy__", []))
            extra = (f" ({legacy_n} orphaned legacy node(s) — see audit panel)"
                     if legacy_n else "")
            ui.notification_show(
                f"✅ Session restored ({latest.get('saved_at','')[:16]}){extra}. "
                f"{len(t3_ghosts)} save(s) available for this batch.",
                type="message", duration=6,
            )
        else:
            ui.notification_show(
                "✅ Assembly session found. No T3 saves — starting fresh T3.",
                type="message", duration=5,
            )
