"""app/handlers/home_theater.py
Home Theater Shiny wiring (ADR-043 / ADR-044 / ADR-045).

Entry point:
    define_server(input, output, session, *,
                  bootloader, wrangle_studio, dev_studio,
                  orchestrator, viz_factory, gallery_viewer,
                  current_persona, anchor_path, tier1_anchor,
                  tier_reference, tier3_leaf, active_cfg,
                  active_collection_id, safe_input, active_home_subtab, tier_toggle,
                  home_state=None, session_manager=None)

Concern: dynamic_tabs, sidebar_nav_ui, sidebar_tools_ui, right_sidebar_content_ui,
         sidebar_filters, system_tools_ui, plot_reference, table_reference,
         plot_leaf, table_leaf, handle_plot_brush, comparison_mode_toggle_ui.
Two-Category Law (ADR-045): This file contains @render.* and @reactive.*
decorators only. It MUST NOT be imported by non-Shiny contexts.
"""

from __future__ import annotations

# @deps
# provides: function:define_server (home_theater), output:export_bundle_download, output:home_data_preview, output:home_col_selector_ui, output:sidebar_filters, output:system_tools_ui
# consumes: app/modules/orchestrator.py, app/modules/wrangle_studio.py, app/modules/dev_studio.py, libs/viz_factory/src/viz_factory/viz_factory.py, utils/config_loader.py
# consumed_by: app/src/server.py
# doc: .antigravity/knowledge/architecture_decisions.md#ADR-043, .antigravity/knowledge/architecture_decisions.md#ADR-044, .antigravity/knowledge/architecture_decisions.md#ADR-045, .antigravity/knowledge/architecture_decisions.md#ADR-047
# @end_deps

from pathlib import Path

import polars as pl
from transformer.lookup import lookup_anchor_rows
from shiny import reactive, render, ui
from utils.config_loader import ConfigManager


def _collect_all_group_plot_ids(bootloader) -> list[tuple[str, dict]]:
    """Enumerate all (plot_id, spec_dict) pairs from analysis_groups AND top-level plots.

    Called once at server init to register dynamic @render.plot handlers.
    Returns list of (p_id, spec) tuples (spec may be None for unresolved entries).
    """
    seen = set()
    results = []
    for proj_id, manifest_path in bootloader.available_projects.items():
        try:
            cfg = ConfigManager(str(manifest_path))
            # Collect from analysis_groups
            groups = cfg.raw_config.get("analysis_groups", {})
            for _gid, gspec in groups.items():
                for p_id, plot_entry in gspec.get("plots", {}).items():
                    if p_id not in seen:
                        seen.add(p_id)
                        results.append((p_id, plot_entry.get("spec")))
            # Collect from top-level plots (fallback when no analysis_groups)
            top_plots = cfg.raw_config.get("plots", {})
            for p_id, plot_spec in top_plots.items():
                if p_id not in seen:
                    seen.add(p_id)
                    results.append((p_id, plot_spec))
        except Exception:
            pass
    return results


def define_server(input, output, session, *,
                  bootloader, wrangle_studio, dev_studio,
                  orchestrator, viz_factory, gallery_viewer,
                  current_persona, anchor_path, tier1_anchor,
                  tier_reference, tier3_leaf, active_cfg,
                  active_collection_id, safe_input,
                  active_home_subtab, tier_toggle,
                  home_state=None, session_manager=None):
    """Register all Home Theater reactive handlers.

    Parameters
    ----------
    bootloader : Bootloader
        Path Authority (ADR-031).
    wrangle_studio : WrangleStudio
        Shared WrangleStudio state (for render_ui routing).
    dev_studio : DevStudio
        Shared DevStudio state.
    orchestrator : DataOrchestrator
        Used for Tier 1 materialization in dynamic_tabs.
    viz_factory : VizFactory
        Plotting engine.
    gallery_viewer : GalleryViewer
        Gallery explorer module.
    current_persona : reactive.Value[str]
        Active persona (ADR-030).
    anchor_path : reactive.Value[str | None]
        Path to active Parquet anchor.
    tier1_anchor : reactive.Calc
        Tier 1 LazyFrame.
    tier_reference : reactive.Calc
        Tier 2 reference LazyFrame.
    tier3_leaf : reactive.Calc
        Tier 3 user-modified DataFrame.
    active_cfg : reactive.Calc
        Active ConfigManager.
    active_collection_id : reactive.Calc
        Active collection ID string.
    safe_input : callable
        Shared utility: safe_input(input_obj, key, default) → value.
    active_home_subtab : reactive.Value[str]
        Phase 21-B: tracks the active plot sub-tab id across groups.
    tier_toggle : reactive.Value[str]
        Phase 21-C: active data tier selection ("T1", "T2", "T3").
    home_state : reactive.Value[dict] | None
        §13 Home Module State Object — survives all panel switches.
        Contains t3_recipe, applied_filters, tier_toggle, and navigation state.
    session_manager : SessionManager | None
        §12d Session ghost save/restore manager.
    """

    # ── Phase 21-B: Dynamic plot handlers for analysis_groups ─────────────────
    # Enumerate all plot IDs at server init time so Shiny can register each
    # @render.plot slot. Handlers read active_cfg() at render time, not init time.
    _all_group_plot_ids = _collect_all_group_plot_ids(bootloader)

    # ── Phase 21-F: Filter recipe builder state ────────────────────────────────
    # List of dicts: {column, op, value, dtype}  — consumed by plot handlers and data preview.
    # Separate from the sidebar_filters render so tier toggle / tab switches don't reset it.
    applied_filters = reactive.Value([])   # committed on Apply
    _pending_filters = reactive.Value([])  # staging area while user builds rows

    def _resolve_active_spec(p_id: str | None) -> dict | None:
        """Return the plot spec dict for the active plot_id, searching groups then top-level."""
        cfg = active_cfg()
        groups = cfg.raw_config.get("analysis_groups", {})
        top_plots = cfg.raw_config.get("plots", {})
        spec = None
        for _gid, gspec in groups.items():
            if p_id and p_id in gspec.get("plots", {}):
                spec = gspec["plots"][p_id].get("spec")
                break
        if spec is None and p_id and p_id in top_plots:
            spec = top_plots[p_id]
        if spec is None:
            for _gid, gspec in groups.items():
                for _pid, pentry in gspec.get("plots", {}).items():
                    spec = pentry.get("spec")
                    break
                if spec:
                    break
        if spec is None:
            for _pid, pspec in top_plots.items():
                spec = pspec
                break
        return spec

    def _resolve_active_lf(spec: dict | None):
        """Return a LazyFrame for the dataset referenced by spec (or tier1_anchor)."""
        if spec is None:
            return tier1_anchor()
        target_ds = spec.get("target_dataset")
        if target_ds:
            anchor_dir = bootloader.get_location("user_sessions") / "anchors"
            out_path = anchor_dir / f"{target_ds}.parquet"
            if out_path.exists():
                return pl.scan_parquet(out_path)
            proj_id = safe_input(input, "project_id", bootloader.get_default_project())
            return orchestrator.materialize_tier1(
                project_id=proj_id,
                collection_id=target_ds,
                output_path=out_path,
            )
        return tier1_anchor()

    def _t3_drop_columns() -> list[str]:
        """Active drop_column targets from t3_recipe (deactivated nodes ignored)."""
        if home_state is None:
            return []
        cols: list[str] = []
        for n in home_state.get().get("t3_recipe", []):
            if not n.get("active", True):
                continue
            if n.get("node_type") != "drop_column":
                continue
            c = n.get("params", {}).get("column", "")
            if c:
                cols.append(c)
        return cols

    def _t3_filter_rows() -> list[dict]:
        """Extract active filter_row RecipeNodes from home_state and convert
        them to the {column, op, value, dtype} format consumed by
        _apply_filter_rows. Inactive (deactivated) nodes are skipped.

        Returns [] when home_state is None or has no t3_recipe — this lets the
        legacy applied_filters path keep working when T3 is empty.
        """
        if home_state is None:
            return []
        rows: list[dict] = []
        for n in home_state.get().get("t3_recipe", []):
            if not n.get("active", True):
                continue
            if n.get("node_type") != "filter_row":
                continue
            p = n.get("params", {})
            if "column" not in p:
                continue
            rows.append({
                "column": p.get("column"),
                "op": p.get("op", "eq"),
                "value": p.get("value"),
                "dtype": p.get("dtype", "Utf8"),
            })
        return rows

    def _apply_filter_rows(lf, filter_rows: list) -> "pl.LazyFrame":
        """
        Apply a list of {column, op, value, dtype} dicts to a LazyFrame.

        Type strategy:
        - Numeric scalar ops (gt/ge/lt/le/eq/ne): cast string value to column dtype.
        - Set ops (in/not_in) with list of strings against a numeric column:
          cast the column to Utf8 for comparison — avoids List[String] cast error.
          This is correct because the filter builder always stores values as strings
          (selectize returns strings regardless of column dtype).
        - Auto-promotes eq/ne to in/not_in when value is a list.
        """
        for f in filter_rows:
            col = f.get("column")
            op = f.get("op", "eq")
            val = f.get("value")
            dtype_str = f.get("dtype", "Utf8")
            if col is None:
                continue

            is_numeric = any(t in dtype_str for t in ("Int", "UInt", "Float"))
            is_list_val = isinstance(val, list)

            # Auto-promote eq/ne to in/not_in when value is a list
            if is_list_val:
                if op in ("eq", "in"):
                    op = "in"
                elif op in ("ne", "not_in"):
                    op = "not_in"

            if op in ("in", "not_in"):
                vals = val if is_list_val else [val]
                str_vals = [str(v) for v in vals]
                if is_numeric:
                    # Cast column to string for comparison — avoids List[String] cast error
                    expr = pl.col(col).cast(pl.Utf8).is_in(str_vals)
                else:
                    expr = pl.col(col).cast(pl.Utf8).is_in(str_vals)
                lf = lf.filter(expr if op == "in" else ~expr)
            else:
                # Scalar ops: coerce value to column dtype
                try:
                    if "Int" in dtype_str or "UInt" in dtype_str:
                        val = int(val)
                    elif "Float" in dtype_str:
                        val = float(val)
                except (ValueError, TypeError):
                    pass
                if op == "eq":
                    lf = lf.filter(pl.col(col) == val)
                elif op == "ne":
                    lf = lf.filter(pl.col(col) != val)
                elif op == "gt":
                    lf = lf.filter(pl.col(col) > val)
                elif op == "ge":
                    lf = lf.filter(pl.col(col) >= val)
                elif op == "lt":
                    lf = lf.filter(pl.col(col) < val)
                elif op == "le":
                    lf = lf.filter(pl.col(col) <= val)
        return lf

    def _spec_discrete_axes(spec: dict | None) -> tuple[set[str], set[str]]:
        """
        Return (discrete_x_cols, discrete_y_cols) — columns declared as discrete
        by scale_x_discrete / scale_y_discrete layers in the plot spec.
        Used by the filter builder to choose widget type for numeric columns.
        """
        if spec is None:
            return set(), set()
        mapping = spec.get("mapping", {})
        x_col = mapping.get("x")
        y_col = mapping.get("y")
        layers = spec.get("layers", [])
        layer_names = {l.get("name", "") for l in layers}
        disc_x = {x_col} if x_col and "scale_x_discrete" in layer_names else set()
        disc_y = {y_col} if y_col and "scale_y_discrete" in layer_names else set()
        return disc_x, disc_y

    def _make_group_plot_handler(p_id: str):
        """Factory: returns a @render.plot fn that renders plot_group_{p_id}."""
        @output(id=f"plot_group_{p_id}")
        @render.plot(alt=f"Plot: {p_id}")
        def _group_plot_handler():
            cfg = active_cfg()
            groups = cfg.raw_config.get("analysis_groups", {})
            # Find the spec for this p_id across all groups
            spec = None
            for _gid, gspec in groups.items():
                plot_entry = gspec.get("plots", {}).get(p_id)
                if plot_entry is not None:
                    spec = plot_entry.get("spec")
                    break
            # Fall back to top-level plots if not found in any group
            if spec is None:
                top_plot = cfg.raw_config.get("plots", {}).get(p_id)
                if top_plot is not None:
                    spec = top_plot
            if spec is None:
                return None

            # Build synthetic manifest so viz_factory.render can be used.
            # Phase 21-F-2: Inject committed filters into plot spec.
            # _apply_filter_rows handles coercion and eq/ne→in/not_in promotion for lists.
            # Here we just strip the 'dtype' key before passing to VizFactory
            # (VizFactory filter dicts don't need it).
            import copy
            plot_spec = copy.deepcopy(spec)
            filter_rows = list(applied_filters.get()) + _t3_filter_rows()
            if filter_rows:
                vf_filters = [
                    {k: v for k, v in f.items() if k != "dtype"}
                    for f in filter_rows
                ]
                # Promote eq/ne to in/not_in when value is a list
                for vf in vf_filters:
                    if isinstance(vf.get("value"), list):
                        if vf["op"] in ("eq", "in"):
                            vf["op"] = "in"
                        elif vf["op"] in ("ne", "not_in"):
                            vf["op"] = "not_in"
                plot_spec["filters"] = vf_filters
            synthetic_manifest = {
                "plots": {p_id: plot_spec},
                "plot_defaults": cfg.raw_config.get("plot_defaults", {}),
            }

            # Resolve data: use target_dataset or fall back to tier1_anchor
            target_ds = spec.get("target_dataset")
            if target_ds:
                proj_id = safe_input(input, "project_id", bootloader.get_default_project())
                coll_id = target_ds
                anchor_dir = bootloader.get_location("user_sessions") / "anchors"
                anchor_dir.mkdir(parents=True, exist_ok=True)
                out_path = anchor_dir / f"{coll_id}.parquet"
                try:
                    if out_path.exists():
                        lf = pl.scan_parquet(out_path)
                    else:
                        lf = orchestrator.materialize_tier1(
                            project_id=proj_id,
                            collection_id=coll_id,
                            output_path=out_path
                        )
                except Exception as e:
                    import matplotlib.pyplot as plt
                    fig, ax = plt.subplots()
                    ax.text(0.5, 0.5, f"Data error: {e}", ha="center", va="center",
                            transform=ax.transAxes, color="red", fontsize=9)
                    ax.axis("off")
                    return fig
            else:
                lf = tier1_anchor()

            # Apply T3 drop_column nodes (audit-committed drops)
            drops = [c for c in _t3_drop_columns() if c in lf.columns]
            if drops:
                lf = lf.drop(drops)

            try:
                return viz_factory.render(lf, synthetic_manifest, p_id)
            except Exception as e:
                import matplotlib.pyplot as plt
                fig, ax = plt.subplots()
                ax.text(0.5, 0.5, f"Render error:\n{e}", ha="center", va="center",
                        transform=ax.transAxes, color="red", fontsize=9,
                        wrap=True)
                ax.axis("off")
                return fig

        return _group_plot_handler

    # Register one handler per discovered plot ID
    for _p_id, _spec in _all_group_plot_ids:
        _make_group_plot_handler(_p_id)

    # 3. Reactive Tab Components (Discovery Architecture)
    @render.ui
    def dynamic_tabs():
        """
        Routes to WrangleStudio, DevStudio, Gallery, or the Unified Home Theater.
        ADR-043 / Phase 21-A: 'Analysis Theater / Viz' nav mode eliminated.
        Home renders exclusively from manifest analysis_groups.
        """
        active_sidebar = safe_input(input, "sidebar_nav", "Home")
        p = current_persona.get()

        # 1. Module Routing (ADR-031 Compliance)
        if active_sidebar == "Wrangle Studio":
            return ui.div(wrangle_studio.render_ui(), class_="theater-container-main")
        if active_sidebar == "Dev Studio":
            return ui.div(dev_studio.render_ui(), class_="theater-container-main")
        if active_sidebar == "Gallery":
            return ui.div(gallery_viewer.render_explorer_ui(), class_="theater-container-main")

        # 2. Results Theater (Home) Logic — ADR-043 Unified Home Theater
        try:
            proj_id = safe_input(input, "project_id", bootloader.get_default_project())
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
            if out_path.exists():
                anchor_path.set(str(out_path))

        except Exception as e:
            return ui.div(ui.markdown(f"**Data Assembly Failed**: {e}"), class_="alert alert-danger")

        # Discover columns (retained for future filter scoping in Phase 21-F)
        all_cols = lf_full.columns  # noqa: F841

        cfg = active_cfg()
        groups = cfg.raw_config.get("analysis_groups", {})

        # --- Thin header: dataset label left, tier toggle right (Phase 21-C/D) ---
        tier_choices = {"T1": "Assembled", "T2": "Analysis-ready"}
        if p in ("pipeline-exploration-advanced", "project-independent", "developer"):
            tier_choices["T3"] = "My adjustments"

        theater_header = ui.div(
            ui.tags.small(
                "Data to show:",
                class_="text-muted fw-semibold me-3",
                style="white-space: nowrap;"
            ),
            ui.input_radio_buttons(
                "tier_toggle",
                label=None,
                choices=tier_choices,
                # Use static default — tier_toggle reactive value is NOT read here
                # so that tier changes do NOT invalidate/re-render dynamic_tabs DOM.
                # The _track_tier_toggle effect keeps tier_toggle reactive in sync.
                selected="T1",
                inline=True,
            ),
            class_="theater-header-strip",
        )

        # Data preview slot — always rendered regardless of groups presence
        # so the Shiny output ID is always mounted.
        data_preview_section = ui.div(
            ui.accordion(
                ui.accordion_panel(
                    ui.tags.span(
                        "Data Preview",
                        title="100 rows from the active plot dataset at the selected tier",
                        style="font-size: 0.8em; color: #6c757d; font-weight: 600;"
                    ),
                    # Phase 21-F-3: Column selector above the DataGrid
                    ui.output_ui("home_col_selector_ui"),
                    ui.output_data_frame("home_data_preview"),
                    value="data_panel",
                ),
                id="acc_home_data",
                open="data_panel",
            ),
            class_="spv-panel",
            style="overflow: visible;"
        )

        # --- No groups: fallback to top-level plots or show guidance ---
        if not groups:
            # Attempt to fall back to top-level plots in the manifest
            top_plots = cfg.raw_config.get("plots", {})
            if top_plots:
                # Wrap top-level plots in a synthetic single group
                plot_subtabs = []
                for p_id, plot_spec in top_plots.items():
                    tab_label = p_id.replace("_", " ").title()
                    plot_subtabs.append(
                        ui.nav_panel(
                            tab_label,
                            ui.output_plot(f"plot_group_{p_id}", height="480px"),
                            value=f"subtab_{p_id}"
                        )
                    )
                plots_card = ui.navset_card_tab(
                    *plot_subtabs, id="subtabs_default_group"
                )
                groups_nav = ui.div(plots_card, class_="spv-panel p-2")
            else:
                groups_nav = ui.p(
                    "Define analysis_groups (or top-level plots) in your manifest to populate this view.",
                    class_="text-muted p-4"
                )
            return ui.div(
                theater_header,
                groups_nav,
                data_preview_section,
                class_="theater-container-main"
            )

        # --- Group nav panels — plots only inside each group (Option B) ---
        # Data preview lives OUTSIDE the group navset (single output ID, no duplicates).
        group_nav_panels = []
        for group_id, group_spec in groups.items():
            # ADR-036 ID sanitation
            safe_sub_id = (
                group_id.replace(' ', '_').replace('📊', 'QC')
                        .replace('💊', 'AMR').lower()
            )
            group_label = group_spec.get("label") or group_spec.get("description", group_id)
            plot_ids = list(group_spec.get("plots", {}).keys())

            plot_subtabs = []
            for p_id in plot_ids:
                tab_label = (
                    group_spec["plots"][p_id].get("label")
                    or p_id.replace("_", " ").title()
                )
                plot_subtabs.append(
                    ui.nav_panel(
                        tab_label,
                        ui.output_plot(f"plot_group_{p_id}", height="480px"),
                        value=f"subtab_{p_id}"
                    )
                )

            # navset_card_tab: gives the card border + built-in tab header — no extra label needed
            plots_card = (
                ui.navset_card_tab(*plot_subtabs, id=f"subtabs_{safe_sub_id}")
                if plot_subtabs
                else ui.card(ui.p("No plots defined for this group.", class_="text-muted p-3"))
            )

            group_nav_panels.append(
                ui.nav_panel(group_label, ui.div(plots_card, class_="p-2"),
                             value=f"group_{safe_sub_id}")
            )

        # Group pill nav wrapped in spv-panel for consistent rounding
        groups_nav = ui.div(
            ui.navset_pill(
                *group_nav_panels,
                id="home_groups_nav",
            ),
            class_="spv-panel",
            style="padding: 8px 10px 0 10px;"
        )

        return ui.div(
            theater_header,
            groups_nav,
            data_preview_section,
            class_="theater-container-main"
        )

    # Phase 21-C: Sync tier_toggle input → reactive.Value so server.py calcs react.
    @reactive.Effect
    def _track_tier_toggle():
        val = safe_input(input, "tier_toggle", "T1")
        if val:
            tier_toggle.set(val)

    # Data change detection — runs as a side-effect separate from dynamic_tabs render.
    # Reads project_id to react when the user switches projects; computes source file
    # hashes, compares to stored data_batch_hash, warns if changed, and always writes
    # manifest_sha256 + data_batch_hash into home_state for session_manager.
    @reactive.Effect
    def _sync_session_provenance():
        if home_state is None:
            return
        proj_id = safe_input(input, "project_id", bootloader.get_default_project())
        if not proj_id:
            return
        try:
            from app.modules.session_manager import SessionManager as _SM
            source_files = orchestrator.get_source_files(proj_id)
            new_dbh = _SM.compute_data_batch_hash(source_files) if source_files else ""
            manifest_path = bootloader.get_location("manifests") / f"{proj_id}.yaml"
            new_msig = _SM.compute_manifest_sha256(manifest_path) if manifest_path.exists() else ""

            cur = home_state.get()
            prev_dbh = cur.get("data_batch_hash") or ""
            if prev_dbh and prev_dbh != new_dbh:
                ui.notification_show(
                    "⚠️ Source data files have changed — re-assembling with updated data.",
                    type="warning", duration=8,
                )
            if cur.get("manifest_sha256") != new_msig or cur.get("data_batch_hash") != new_dbh:
                home_state.set({**cur, "manifest_sha256": new_msig, "data_batch_hash": new_dbh})
        except Exception:
            pass

    # Phase 21-B/D: Track active plot sub-tab across all group navsets.
    # Polls subtabs_{safe_sub_id} for the active group first, then all others.
    @reactive.Effect
    def _track_active_home_subtab():
        cfg = active_cfg()
        groups = cfg.raw_config.get("analysis_groups", {})
        active_group = safe_input(input, "home_groups_nav", None)
        for group_id in groups:
            safe_sub_id = (
                group_id.replace(' ', '_').replace('📊', 'QC')
                        .replace('💊', 'AMR').lower()
            )
            # Prioritise the active group's subtab
            if active_group and active_group != f"group_{safe_sub_id}":
                continue
            val = safe_input(input, f"subtabs_{safe_sub_id}", None)
            if val:
                active_home_subtab.set(val)
                return
        # Fallback: accept any non-None subtab value from groups
        for group_id in groups:
            safe_sub_id = (
                group_id.replace(' ', '_').replace('📊', 'QC')
                        .replace('💊', 'AMR').lower()
            )
            val = safe_input(input, f"subtabs_{safe_sub_id}", None)
            if val:
                active_home_subtab.set(val)
                return
        # No-groups fallback: check the default synthetic group subtab
        val = safe_input(input, "subtabs_default_group", None)
        if val:
            active_home_subtab.set(val)
            return

    # Phase 21-D/F: Data preview — scoped to active plot's dataset, with filters + col selector.
    @output
    @render.data_frame
    def home_data_preview():
        """100-row preview for the active plot's dataset. Applies committed filters + col selector."""
        subtab = active_home_subtab.get()
        p_id = subtab.removeprefix("subtab_") if subtab else None
        spec = _resolve_active_spec(p_id)

        try:
            lf = _resolve_active_lf(spec)
            lf = _apply_filter_rows(lf, list(applied_filters.get()) + _t3_filter_rows())
            # Apply T3 drop_column nodes — committed audit drops.
            drops = [c for c in _t3_drop_columns() if c in lf.columns]
            if drops:
                lf = lf.drop(drops)
            df = lf.head(100).collect()

            # Apply column visibility selection (Phase 21-F-4) — preview-only filter
            visible = safe_input(input, "preview_col_selector", None)
            if visible and isinstance(visible, (list, tuple)):
                visible_cols = [c for c in visible if c in df.columns]
                if visible_cols:
                    df = df.select(visible_cols)

            return render.DataGrid(df, filters=False, height="300px")
        except Exception as e:
            return render.DataGrid(
                pl.DataFrame({"Error": [str(e)]}),
                filters=False
            )

    # Phase 21-F-4: Column selector UI for data preview.
    # Split into two renders so the selectize component is NOT re-rendered on
    # every keystroke (which would reset the user's selection). The selectize
    # only re-renders when its data dependencies change (active subtab, the
    # set of columns, committed T3 drops) — not the user's transient selection.
    @output
    @render.ui
    def home_col_selector_ui():
        subtab = active_home_subtab.get()
        p_id = subtab.removeprefix("subtab_") if subtab else None
        spec = _resolve_active_spec(p_id)
        try:
            lf = _resolve_active_lf(spec)
            committed_drops = set(_t3_drop_columns())
            cols = [c for c in lf.columns if c not in committed_drops]
            in_t3 = tier_toggle.get() == "T3"
            label_text = (
                "Columns (drop unselected via audit):" if in_t3
                else "Visible columns (preview only):"
            )

            return ui.div(
                ui.tags.small(label_text,
                              class_="text-muted fw-semibold d-block mb-1"),
                ui.input_selectize(
                    "preview_col_selector",
                    label=None,
                    choices=cols,
                    selected=cols,
                    multiple=True,
                    options={
                        "placeholder": "Select columns…",
                        "plugins": ["remove_button"],
                    },
                ),
                # Audit-drop button is its own output — only THAT re-renders
                # on selection change, so the selectize stays mounted.
                ui.output_ui("col_drop_audit_btn_ui"),
                class_="mb-2 w-100 column-picker-container",
                style="font-size: 0.75em;"
            )
        except Exception:
            return ui.div()

    @output
    @render.ui
    def col_drop_audit_btn_ui():
        """Live count of deselected columns — re-renders on selection change.

        Kept SEPARATE from home_col_selector_ui so reading the selector input
        here does not invalidate the selectize component itself.
        """
        if tier_toggle.get() != "T3":
            return ui.span()
        subtab = active_home_subtab.get()
        p_id = subtab.removeprefix("subtab_") if subtab else None
        spec = _resolve_active_spec(p_id)
        try:
            lf = _resolve_active_lf(spec)
        except Exception:
            return ui.span()
        committed = set(_t3_drop_columns())
        cols = [c for c in lf.columns if c not in committed]
        visible = safe_input(input, "preview_col_selector", cols)
        vis_set = set(visible) if isinstance(visible, (list, tuple)) else set(cols)
        n_drop = len([c for c in cols if c not in vis_set])
        return ui.input_action_button(
            "col_drop_to_audit", f"➜ Audit drops ({n_drop})",
            class_="btn-warning btn-sm w-100 mt-1",
            style="font-size:0.72em;",
            disabled=(n_drop == 0),
        )

    @render.ui
    def sidebar_nav_ui():
        perm = current_persona.get()
        print(f"DEBUG: Rendering sidebar_nav_ui for Persona: {perm}")

        nav_items = [ui.nav_panel("Home", value="Home")]

        if perm in ["pipeline_exploration_advanced", "project_independent", "developer"]:
            nav_items.append(ui.nav_panel("Blueprint Architect", value="Wrangle Studio"))

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
        active_sidebar = safe_input(input, "sidebar_nav", "Home")

        # 🟢 Discovery Mode (Gallery)
        if active_sidebar == "Gallery":
            return ui.div(
                ui.p("Discovery Mode Active", class_="text-muted p-4 italic"),
                ui.p("Choose a visual recipe to begin.", class_="text-muted px-4 small")
            )

        # 🔵 Manifest Workbench (Wrangle Studio)
        if active_sidebar == "Wrangle Studio":
            return ui.div(
                ui.accordion(
                    ui.accordion_panel(
                        "🗂️ Master Manifest",
                        ui.input_select("stored_manifest_selector", None,
                                        choices=["Scanning config/..."]),
                        ui.tags.small(
                            "Select a project manifest. Click any node in the TubeMap to navigate.",
                            class_="text-muted d-block mt-1"),
                        icon=ui.tags.i(class_="bi bi-diagram-3")
                    ),
                    ui.accordion_panel(
                        "📤 External Exchange",
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
                ),
                # Hidden controls — kept in DOM so Shiny bridge can programmatically
                # update the selection and fire the import trigger via js_eval.
                ui.div(
                    ui.input_select("dataset_pipeline_selector", None,
                                    choices=["Select a Master first"]),
                    ui.input_action_button("btn_import_manifest", "Import",
                                           class_="btn-info btn-sm"),
                    ui.input_action_button("btn_save_internal", "Save",
                                           class_="btn-success btn-sm"),
                    style="display:none;",
                    id="blueprint_hidden_controls"
                )
            )

        # 🏠 Standard Operation Sidebar (Home — ADR-043)
        try:
            proj_choices = list(bootloader.available_projects.keys())
            def_proj = bootloader.get_default_project()
        except Exception:
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

    # --- 📐 Right Sidebar Context Matrix (ADR-039 / ADR-044) ---
    @output
    @render.ui
    def right_sidebar_content_ui():
        """
        Context-sensitive right sidebar (ADR-039).
        Switches content based on the active module.
        """
        active_sidebar = safe_input(input, "sidebar_nav", "Home")

        # --- 🏗️ Blueprint Architect (Wrangle Studio) ---
        if active_sidebar == "Wrangle Studio":
            selected_node = safe_input(input, "blueprint_node_clicked", None)
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
                    ui.div(f"Logic stack: {step_count} step(s)", class_="text-muted small"),
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

        # --- 🏠 Home Theater (ADR-043 / ADR-044) ---
        if active_sidebar in ("Home", None, ""):
            persona = current_persona.get()
            hidden_personas = {"pipeline-static", "pipeline-exploration-simple"}
            # §21-G: suppress right sidebar for lower personas
            if persona in hidden_personas:
                return ui.div()

            return ui.div(
                ui.card(
                    ui.card_header(
                        ui.div(ui.h5("Pipeline Audit", class_="mb-0"),
                               class_="d-flex justify-content-center w-100")
                    ),
                    ui.div(
                        ui.output_ui("recipe_pending_badge_ui"),
                        ui.h6("Tier 2 — Inherited", class_="text-muted",
                              style="font-size:0.75em; text-transform:uppercase; margin-top:4px;"),
                        ui.output_ui("audit_nodes_tier2"),
                        ui.hr(style="margin:6px 0;"),
                        ui.h6("Tier 3 — My Adjustments", class_="text-muted",
                              style="font-size:0.75em; text-transform:uppercase;"),
                        ui.output_ui("audit_nodes_tier3"),
                        class_="p-2",
                        style="overflow-y:auto; flex:1 1 auto;",
                    ),
                    class_="mb-2 shadow-sm border-0 d-flex flex-column",
                    style="flex:1 1 auto; overflow:hidden;",
                ),
                ui.output_ui("audit_stack_tools_ui"),
                class_="sidebar-content p-0 d-flex flex-column h-100"
            )

        # --- 🖼️ Gallery ---
        if active_sidebar == "Gallery":
            return ui.div(
                ui.card(
                    ui.card_header(ui.h5("Gallery Explorer", class_="mb-0 text-center")),
                    ui.div(
                        ui.p("📚 Browse visual recipes.", class_="text-muted small p-2"),
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
                    ui.card_header(ui.h5("Dev Inspector", class_="mb-0 text-center")),
                    ui.div(
                        ui.p("🔧 Developer diagnostic tools.", class_="text-muted small p-2"),
                        class_="p-1"
                    ),
                    class_="mb-2 shadow-sm border-0"
                ),
                class_="sidebar-content p-0"
            )

        # --- Default fallback ---
        return ui.div(
            ui.p("—", class_="text-muted p-3 text-center"),
            class_="sidebar-content p-0"
        )

    @output
    @render.ui
    def system_tools_ui():
        n_active = len(applied_filters.get())
        filter_warning = ui.div()
        if n_active:
            filter_warning = ui.tags.small(
                f"⚠ {n_active} active filter(s) — a note will be embedded in the bundle.",
                class_="text-warning d-block mb-1",
                style="font-size:0.7em;"
            )
        return ui.div(
            # ── Export Results Bundle ─────────────────────────────────────
            ui.div(
                ui.p("Export Results Bundle", class_="ultra-small fw-bold mb-1"),
                ui.input_text(
                    "export_user_name", label=None,
                    placeholder="Your name (no spaces)…",
                    value="",
                ),
                ui.input_radio_buttons(
                    "export_preset",
                    label=None,
                    choices={"web": "Web / Presentation", "publication": "Publication (≥600 DPI)"},
                    selected="web",
                    inline=False,
                ),
                filter_warning,
                ui.download_button(
                    "export_bundle_download",
                    "📦 Export Bundle",
                    class_="btn-success btn-sm w-100 mt-1",
                ),
                class_="mb-3 px-2",
                style="font-size:0.8em;"
            ),
            # ── Export Audit Report (22-E) ────────────────────────────────
            ui.output_ui("export_audit_report_ui"),
            # ── Session Management (22-D) ─────────────────────────────────
            ui.div(
                ui.output_ui("session_management_ui"),
                class_="mb-3 px-2",
            ),
            # ── Data Ingestion ────────────────────────────────────────────
            ui.div(
                ui.p("Data Ingestion (ADR-031)", class_="ultra-small fw-bold mb-1"),
                ui.div(
                    ui.input_file("file_ingest", None, multiple=True, accept=[".yaml"]),
                    class_="upload-row mb-1"
                ),
                ui.input_action_button("btn_ingest", "🚀 Ingest Manifests", class_="w-100"),
                class_="px-2"
            )
        )

    @render.download(filename=lambda: _export_bundle_filename())
    async def export_bundle_download():
        """
        Phase 21-I: Export Results Bundle.

        Produces a zip file containing:
        - plots/          SVG (web preset) or high-DPI PNG (publication preset) per plot
        - data/           T1 TSV for each dataset referenced by active plots
        - recipes/        YAML wrangling recipe(s) for the active project
        - FILTERS.txt     If any applied_filters exist ("No Trace No Export" compliance note)
        - report.qmd      Quarto source report embedding all plots and datasets
        - README.txt      Bundle manifest (timestamp, project, persona, preset)
        """
        import io
        import zipfile
        import tempfile
        import datetime
        import shutil
        import csv
        import copy

        now = datetime.datetime.now()
        ts = now.strftime("%Y%m%d_%H%M%S")
        raw_name = safe_input(input, "export_user_name", "user").strip() or "user"
        # Sanitize: replace spaces/special chars with underscore, lowercase
        import re
        safe_name = re.sub(r"[^A-Za-z0-9_-]", "_", raw_name)[:40]
        preset = safe_input(input, "export_preset", "web")
        persona = current_persona.get()
        dpi = 300 if preset == "web" else 600

        cfg = active_cfg()
        proj_id = safe_input(input, "project_id", bootloader.get_default_project())
        groups = cfg.raw_config.get("analysis_groups", {})
        top_plots = cfg.raw_config.get("plots", {})
        active_filters = applied_filters.get()

        # Collect all (plot_id, spec) pairs for this export
        all_plots: list[tuple[str, dict]] = []
        for _gid, gspec in groups.items():
            for p_id, pentry in gspec.get("plots", {}).items():
                spec = pentry.get("spec")
                if spec:
                    all_plots.append((p_id, spec))
        if not all_plots:
            for p_id, spec in top_plots.items():
                all_plots.append((p_id, spec))

        buf = io.BytesIO()
        with zipfile.ZipFile(buf, mode="w", compression=zipfile.ZIP_DEFLATED) as zf:
            bundle_dir = f"{ts}_{safe_name}"

            # ── FILTERS.txt (No Trace No Export) ─────────────────────────
            if active_filters:
                lines = [
                    "FILTER TRACE — embedded per 'No Trace No Export' protocol.",
                    f"Exported at: {now.isoformat()}",
                    f"Project: {proj_id}",
                    "",
                    "Applied filters at time of export:",
                ]
                for i, f in enumerate(active_filters, 1):
                    col = f.get("column", "?")
                    op = _op_label(f.get("op", "eq"))
                    val = f.get("value", "")
                    val_str = ", ".join(str(v) for v in val) if isinstance(val, list) else str(val)
                    lines.append(f"  {i}. {col} {op} {val_str}")
                zf.writestr(f"{bundle_dir}/FILTERS.txt", "\n".join(lines))

            # ── Render and save plots ─────────────────────────────────────
            rendered_plots = {}  # p_id → figure object
            with tempfile.TemporaryDirectory() as tmpdir:
                tmpdir_path = Path(tmpdir)

                for p_id, spec in all_plots:
                    try:
                        # Build synthetic manifest with applied filters
                        plot_spec = copy.deepcopy(spec)
                        if active_filters:
                            vf_filters = [
                                {k: v for k, v in f.items() if k != "dtype"}
                                for f in active_filters
                            ]
                            for vf in vf_filters:
                                if isinstance(vf.get("value"), list):
                                    vf["op"] = "in" if vf["op"] in ("eq", "in") else "not_in"
                            plot_spec["filters"] = vf_filters

                        synthetic_manifest = {
                            "plots": {p_id: plot_spec},
                            "plot_defaults": cfg.raw_config.get("plot_defaults", {}),
                        }

                        # Resolve dataset
                        target_ds = spec.get("target_dataset")
                        if target_ds:
                            anchor_dir = bootloader.get_location("user_sessions") / "anchors"
                            out_path = anchor_dir / f"{target_ds}.parquet"
                            if out_path.exists():
                                lf = pl.scan_parquet(out_path)
                            else:
                                lf = orchestrator.materialize_tier1(
                                    project_id=proj_id,
                                    collection_id=target_ds,
                                    output_path=out_path
                                )
                        else:
                            lf = tier1_anchor()

                        fig = viz_factory.render(lf, synthetic_manifest, p_id)
                        rendered_plots[p_id] = fig

                        # Save to temp file then read bytes into zip
                        if preset == "web":
                            plot_path = tmpdir_path / f"{p_id}.svg"
                            fig.save(str(plot_path), format="svg", verbose=False)
                        else:
                            plot_path = tmpdir_path / f"{p_id}.png"
                            fig.save(str(plot_path), dpi=dpi, verbose=False)

                        with open(plot_path, "rb") as f:
                            zf.writestr(
                                f"{bundle_dir}/plots/{plot_path.name}",
                                f.read()
                            )
                    except Exception as e:
                        # Write error stub so bundle is still complete
                        zf.writestr(
                            f"{bundle_dir}/plots/{p_id}_ERROR.txt",
                            f"Plot render failed:\n{e}"
                        )

                # ── Export data by tier ───────────────────────────────────
                # T1: always exported.
                # T2: always exported when materialize_tier2 is available (tier_reference).
                # T3: only for advanced+ personas, and only when tier_toggle == "T3".
                #     T3 is the user-adjusted DataFrame (tier3_leaf); deferred if no active T3.
                is_advanced = persona in (
                    "pipeline_exploration_advanced", "project_independent", "developer"
                )
                active_tier = tier_toggle.get()  # "T1", "T2", "T3"
                export_t3 = is_advanced and active_tier == "T3"

                exported_datasets: set[str] = set()
                for p_id, spec in all_plots:
                    target_ds = spec.get("target_dataset")
                    ds_key = target_ds or "__tier1_anchor__"
                    if ds_key in exported_datasets:
                        continue
                    exported_datasets.add(ds_key)

                    # ── T1 ────────────────────────────────────────────────
                    try:
                        if target_ds:
                            anchor_dir = bootloader.get_location("user_sessions") / "anchors"
                            out_path = anchor_dir / f"{target_ds}.parquet"
                            if out_path.exists():
                                lf_t1 = pl.scan_parquet(out_path)
                            else:
                                lf_t1 = orchestrator.materialize_tier1(
                                    project_id=proj_id,
                                    collection_id=target_ds,
                                    output_path=out_path
                                )
                        else:
                            lf_t1 = tier1_anchor()
                        df_t1 = lf_t1.collect()
                        safe_ds = ds_key.replace("/", "_")
                        tsv_path = tmpdir_path / f"{safe_ds}_T1.tsv"
                        df_t1.write_csv(str(tsv_path), separator="\t")
                        with open(tsv_path, "rb") as f:
                            zf.writestr(f"{bundle_dir}/data/{safe_ds}_T1.tsv", f.read())
                    except Exception as e:
                        zf.writestr(
                            f"{bundle_dir}/data/{ds_key}_T1_ERROR.txt",
                            f"T1 data export failed:\n{e}"
                        )

                    # ── T2 ────────────────────────────────────────────────
                    try:
                        lf_t2 = tier_reference()
                        if lf_t2 is not None:
                            df_t2 = lf_t2.collect() if hasattr(lf_t2, "collect") else lf_t2
                            safe_ds = ds_key.replace("/", "_")
                            tsv_path = tmpdir_path / f"{safe_ds}_T2.tsv"
                            df_t2.write_csv(str(tsv_path), separator="\t")
                            with open(tsv_path, "rb") as f:
                                zf.writestr(f"{bundle_dir}/data/{safe_ds}_T2.tsv", f.read())
                    except Exception as e:
                        zf.writestr(
                            f"{bundle_dir}/data/{ds_key}_T2_ERROR.txt",
                            f"T2 data export failed:\n{e}"
                        )

                    # ── T3 (advanced persona + T3 active only) ────────────
                    if export_t3:
                        try:
                            df_t3 = tier3_leaf()
                            if df_t3 is not None:
                                if hasattr(df_t3, "lazy"):
                                    df_t3 = df_t3  # already DataFrame
                                safe_ds = ds_key.replace("/", "_")
                                tsv_path = tmpdir_path / f"{safe_ds}_T3.tsv"
                                df_t3.write_csv(str(tsv_path), separator="\t")
                                with open(tsv_path, "rb") as f:
                                    zf.writestr(
                                        f"{bundle_dir}/data/{safe_ds}_T3.tsv", f.read()
                                    )
                        except Exception as e:
                            zf.writestr(
                                f"{bundle_dir}/data/{ds_key}_T3_ERROR.txt",
                                f"T3 data export failed:\n{e}"
                            )

                # ── Copy YAML recipes ─────────────────────────────────────
                try:
                    proj_manifest_path = bootloader.available_projects.get(proj_id)
                    if proj_manifest_path:
                        proj_dir = Path(str(proj_manifest_path)).parent
                        for yaml_file in proj_dir.rglob("*.yaml"):
                            rel = yaml_file.relative_to(proj_dir)
                            with open(yaml_file, "rb") as f:
                                zf.writestr(
                                    f"{bundle_dir}/recipes/{proj_id}/{rel}",
                                    f.read()
                                )
                except Exception as e:
                    zf.writestr(f"{bundle_dir}/recipes/ERROR.txt", str(e))

            # ── Generate Quarto .qmd report ───────────────────────────────
            plot_ext = "svg" if preset == "web" else "png"
            qmd_lines = [
                "---",
                f'title: "Results Report — {proj_id}"',
                f'date: "{now.strftime("%Y-%m-%d")}"',
                f'author: "{safe_name}"',
                'format:',
                '  html:',
                '    self-contained: true',
                '  pdf:',
                '    documentclass: article',
                "---",
                "",
                "## Overview",
                "",
                f"Project: **{proj_id}**  ",
                f"Persona: **{persona}**  ",
                f"Export preset: **{preset}**  ",
                f"Generated: {now.strftime('%Y-%m-%d %H:%M:%S')}  ",
                "",
            ]
            if active_filters:
                qmd_lines += [
                    "## Active Filters at Export",
                    "",
                    "| Column | Op | Value |",
                    "|--------|-----|-------|",
                ]
                for f in active_filters:
                    col = f.get("column", "?")
                    op = _op_label(f.get("op", "eq"))
                    val = f.get("value", "")
                    val_str = ", ".join(str(v) for v in val) if isinstance(val, list) else str(val)
                    qmd_lines.append(f"| {col} | {op} | {val_str} |")
                qmd_lines.append("")

            qmd_lines += ["## Plots", ""]
            for p_id, spec in all_plots:
                label = spec.get("title") or p_id.replace("_", " ").title()
                qmd_lines += [
                    f"### {label}",
                    "",
                    f"![{label}](plots/{p_id}.{plot_ext}){{width=100%}}",
                    "",
                ]

            qmd_lines += ["## Data", ""]
            tiers_exported = ["T1", "T2"] + (["T3"] if export_t3 else [])
            qmd_lines.append(
                f"Tiers exported: **{', '.join(tiers_exported)}**"
                + ("  *(T3 = user-adjusted)*" if export_t3 else "")
            )
            qmd_lines.append("")
            for ds_key in exported_datasets:
                safe_ds = ds_key.replace("/", "_")
                qmd_lines += [f"### {ds_key}", ""]
                for tier in tiers_exported:
                    qmd_lines.append(f"- {tier}: `data/{safe_ds}_{tier}.tsv`")
                qmd_lines.append("")

            qmd_lines += [
                "---",
                "",
                "> Report generated by SPARMVET-VIZ.",
                "> Recipes are in the `recipes/` folder.",
                "> To render: `quarto render report.qmd`",
            ]
            zf.writestr(f"{bundle_dir}/report.qmd", "\n".join(qmd_lines))

            # ── README.txt ────────────────────────────────────────────────
            readme_lines = [
                "SPARMVET-VIZ Export Bundle",
                "=" * 40,
                f"Timestamp  : {now.isoformat()}",
                f"Project    : {proj_id}",
                f"User       : {safe_name}",
                f"Persona    : {persona}",
                f"Preset     : {preset} (DPI={dpi})",
                f"Plots      : {len(all_plots)}",
                f"Tiers      : {', '.join(tiers_exported)}",
                f"Filters    : {len(active_filters)} active",
                "",
                "Contents:",
                "  plots/      — rendered figures",
                "  data/       — datasets as TSV: <dataset>_T1.tsv, <dataset>_T2.tsv"
                + (", <dataset>_T3.tsv" if export_t3 else ""),
                "  recipes/    — YAML wrangling recipes (T3 updated recipe if applicable)",
                "  report.qmd  — Quarto source report (run: quarto render report.qmd)",
                "  FILTERS.txt — filter trace (if filters were active)",
                "  README.txt  — this file",
            ]
            zf.writestr(f"{bundle_dir}/README.txt", "\n".join(readme_lines))

        buf.seek(0)
        yield buf.read()

    # ── 22-E: Export Audit Report ─────────────────────────────────────────────

    @output
    @render.ui
    def export_audit_report_ui():
        """Audit Report export button — persona-gated (≥ pipeline_exploration_advanced)."""
        from app.modules.exporter import pandoc_available
        persona = current_persona.get()
        advanced_personas = {"pipeline-exploration-advanced", "project-independent", "developer"}
        if persona not in advanced_personas:
            return ui.div()

        # Warn if deactivated nodes exist
        discarded_warning = ui.div()
        if home_state is not None:
            state = home_state.get()
            n_discarded = sum(
                1 for n in state.get("t3_recipe", []) if not n.get("active", True)
            )
            if n_discarded:
                discarded_warning = ui.tags.small(
                    f"⚠️ {n_discarded} deactivated node(s) — you will be prompted before export.",
                    class_="text-warning d-block mb-1",
                    style="font-size:0.7em;",
                )

        pandoc_btn = ui.download_button(
            "export_audit_docx",
            "📄 Export PDF/DOCX (Pandoc)",
            class_="btn-outline-secondary btn-sm w-100 mt-1",
        ) if pandoc_available() else ui.div(
            ui.tags.small(
                "Pandoc not found on PATH — PDF/DOCX export unavailable.",
                class_="text-muted",
                style="font-size:0.68em;",
            )
        )

        return ui.div(
            ui.p("Export Audit Report", class_="ultra-small fw-bold mb-1"),
            discarded_warning,
            ui.download_button(
                "export_audit_report_download",
                "📋 Export Audit Report (HTML)",
                class_="btn-info btn-sm w-100",
            ),
            pandoc_btn,
            class_="mb-3 px-2",
            style="font-size:0.8em;",
        )

    @render.download(filename=lambda: _audit_report_filename("html"))
    async def export_audit_report_download():
        """Generate and stream the Quarto HTML audit report."""
        import tempfile, io
        from app.modules.exporter import render_audit_report

        if home_state is None:
            yield b""
            return

        state = home_state.get()

        # Block if deactivated nodes exist — notify user
        n_discarded = sum(1 for n in state.get("t3_recipe", []) if not n.get("active", True))
        if n_discarded:
            ui.notification_show(
                f"⚠️ {n_discarded} deactivated node(s) exist. "
                "They will NOT appear in the report. Confirm by re-clicking.",
                type="warning", duration=8,
            )

        proj_id = safe_input(input, "project_id", "")
        msig = state.get("manifest_sha256") or ""
        dbh = state.get("data_batch_hash") or ""
        session_key = ""
        if msig and dbh:
            from app.modules.session_manager import SessionManager
            session_key = SessionManager.compute_session_key(msig, dbh)

        with tempfile.TemporaryDirectory() as tmpdir:
            out_path = render_audit_report(
                home_state=state,
                session_key=session_key,
                output_dir=tmpdir,
                manifest_id=proj_id,
            )
            yield Path(out_path).read_bytes()

    @render.download(filename=lambda: _audit_report_filename("docx"))
    async def export_audit_docx():
        """Convert the rendered HTML audit report to DOCX via Pandoc."""
        import tempfile
        from app.modules.exporter import render_audit_report, pandoc_convert

        if home_state is None:
            yield b""
            return

        state = home_state.get()
        proj_id = safe_input(input, "project_id", "")

        with tempfile.TemporaryDirectory() as tmpdir:
            html_path = render_audit_report(
                home_state=state,
                session_key="",
                output_dir=tmpdir,
                manifest_id=proj_id,
            )
            docx_path = pandoc_convert(html_path, fmt="docx")
            if docx_path and Path(docx_path).exists():
                yield Path(docx_path).read_bytes()
            else:
                yield b""

    def _audit_report_filename(fmt: str) -> str:
        import datetime, re
        ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        proj_id = safe_input(input, "project_id", "report")
        safe_id = re.sub(r"[^A-Za-z0-9_-]", "_", proj_id)[:30]
        return f"{ts}_{safe_id}_audit_report.{fmt}"

    # ── 22-D: Session Management Panel ────────────────────────────────────────

    @output
    @render.ui
    def session_management_ui():
        """Session Management panel — persona-gated (≥ pipeline_exploration_advanced)."""
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
            # Restore most-recent T3 ghost into home_state
            latest = t3_ghosts[0]
            new_state = {
                **state,
                "t3_recipe": latest.get("t3_recipe", []),
                "t3_plot_overrides": latest.get("t3_plot_overrides", {}),
                "tier_toggle": latest.get("tier_toggle", "T2"),
                "t3_ghost_file": latest.get("file", ""),
                "t3_ghost_saved_at": latest.get("saved_at", ""),
                "_pending_t3_nodes": [],
            }
            home_state.set(new_state)
            ui.notification_show(
                f"✅ Session restored ({latest.get('saved_at','')[:16]}). "
                f"{len(t3_ghosts)} save(s) available for this batch.",
                type="message", duration=6,
            )
        else:
            ui.notification_show(
                "✅ Assembly session found. No T3 saves — starting fresh T3.",
                type="message", duration=5,
            )

    def _export_bundle_filename() -> str:
        """Generate timestamped zip filename for the export bundle."""
        import datetime, re
        now = datetime.datetime.now()
        ts = now.strftime("%Y%m%d_%H%M%S")
        raw_name = safe_input(input, "export_user_name", "user").strip() or "user"
        safe_name = re.sub(r"[^A-Za-z0-9_-]", "_", raw_name)[:40]
        return f"{ts}_{safe_name}_results.zip"

    @output
    @render.ui
    def sidebar_filters():
        """
        Phase 21-F-1: Static shell — rendered once, never re-renders.
        Mounts stable output slots; child outputs re-render independently.
        Apply label and status are in filter_rows_ui to avoid shell re-renders.
        """
        # Left "Apply" is the single entry point: in T1/T2 it commits transient
        # filters; in T3 it pushes pending RecipeNodes into home_state for the
        # right-sidebar audit panel. No separate "Apply to recipe" button.
        return ui.div(
            ui.output_ui("filter_rows_ui"),
            ui.output_ui("filter_form_ui"),
            ui.div(
                ui.output_ui("filter_controls_ui"),
                class_="mt-2 px-1"
            ),
            style="font-size: 0.8em;"
        )

    @output
    @render.ui
    def filter_rows_ui():
        """Pending filter rows. Reads _pending_filters only — re-renders on Add/Remove."""
        pending = _pending_filters.get()
        if not pending:
            return ui.tags.small(
                "No filters yet. Add rows below.", class_="text-muted d-block px-1 mb-1",
                style="font-size:0.75em;"
            )
        rows = []
        for i, f in enumerate(pending):
            col = f.get("column", "")
            op = f.get("op", "eq")
            val = f.get("value", "")
            dtype_str = f.get("dtype", "")
            val_display = ", ".join(str(v) for v in val) if isinstance(val, list) else str(val)
            rows.append(ui.div(
                ui.div(
                    ui.tags.small(
                        f"{col} {_op_label(op)} {val_display}",
                        class_="text-dark", style="font-size:0.75em;"
                    ),
                    ui.tags.small(f" [{dtype_str}]", class_="text-muted",
                                  style="font-size:0.65em;"),
                    class_="flex-grow-1"
                ),
                ui.input_action_button(
                    f"filter_remove_{i}", "✕",
                    class_="btn-outline-danger btn-sm py-0 px-1",
                    style="font-size:0.7em; line-height:1;"
                ),
                class_="d-flex align-items-center gap-2 mb-1 px-1 py-1 border rounded bg-light",
            ))
        return ui.div(*rows)

    @output
    @render.ui
    def filter_form_ui():
        """
        Add-row form. Reads dataset columns + fb_col/fb_op input state.
        Does NOT read _pending_filters — so appending a row doesn't reset the form.
        Value type coercion happens at apply time in _apply_filter_rows;
        values are always stored as strings here and cast to column dtype when filtering.
        """
        subtab = active_home_subtab.get()
        p_id = subtab.removeprefix("subtab_") if subtab else None
        spec = _resolve_active_spec(p_id)
        disc_x, disc_y = _spec_discrete_axes(spec)
        discrete_cols = disc_x | disc_y

        try:
            lf = _resolve_active_lf(spec)
            sample = lf.head(500).collect()
            all_cols = sample.columns
            dtypes = {c: str(sample[c].dtype) for c in all_cols}
        except Exception:
            all_cols = []
            dtypes = {}
            sample = None

        col_choices = {c: f"{c}  [{dtypes.get(c, '')}]" for c in all_cols} if all_cols else {}
        sel_col = safe_input(input, "fb_col", all_cols[0] if all_cols else None)
        sel_dtype = dtypes.get(sel_col, "Utf8") if sel_col else "Utf8"
        is_discrete = (sel_col in discrete_cols) or (
            "Int" not in sel_dtype and "Float" not in sel_dtype and "UInt" not in sel_dtype
        )

        if is_discrete:
            op_choices = {"in": "∈ any of", "not_in": "∉ none of", "eq": "= exact", "ne": "≠"}
        else:
            op_choices = {"eq": "=", "ne": "≠", "gt": ">", "ge": "≥", "lt": "<", "le": "≤"}

        if is_discrete and sample is not None and sel_col and sel_col in sample.columns:
            unique_vals = sorted([str(v) for v in sample[sel_col].drop_nulls().unique().to_list()])
            value_widget = ui.input_selectize(
                "fb_value", label=None,
                choices=unique_vals, selected=[],
                multiple=True,
                options={"placeholder": "Select value(s)…", "plugins": ["remove_button"]},
            )
        else:
            value_widget = ui.input_text("fb_value", label=None, placeholder="Value…")

        return ui.div(
            ui.tags.small("Add filter row:", class_="fw-semibold text-muted d-block mb-1"),
            # selected=sel_col preserves the user's column choice across re-renders
            ui.input_select("fb_col", label=None, choices=col_choices, selected=sel_col),
            ui.div(
                ui.input_select("fb_op", label=None, choices=op_choices, width="100px"),
                ui.div(value_widget, style="flex:1;"),
                class_="d-flex gap-1 align-items-start"
            ),
            ui.input_action_button(
                "filter_add_row", "+ Add",
                class_="btn-outline-primary btn-sm w-100 mt-1",
                style="font-size:0.75em;"
            ),
            class_="mt-2 pt-2 border-top",
            style="font-size: 0.8em;"
        )

    @output
    @render.ui
    def filter_controls_ui():
        """Apply/Reset buttons + status. Reads _pending_filters + applied_filters.

        In T3 mode the Apply button label changes to indicate that pressing it
        promotes staged rows into the audit pipeline (right sidebar) rather
        than committing a transient view filter.
        """
        n_applied = len(applied_filters.get())
        n_pending = len(_pending_filters.get())
        in_t3 = tier_toggle.get() == "T3"
        apply_label = (f"➜ Audit ({n_pending})" if in_t3
                       else f"Apply ({n_pending})")
        apply_class = ("btn-warning btn-sm flex-grow-1" if in_t3
                       else "btn-primary btn-sm flex-grow-1")
        status = (
            ui.tags.small(f"{n_applied} active", class_="text-success d-block mb-1",
                          style="font-size:0.72em;")
            if n_applied else ui.div()
        )
        return ui.div(
            status,
            ui.div(
                ui.input_action_button(
                    "filter_apply", apply_label,
                    class_=apply_class,
                    style="font-size:0.75em;"
                ),
                ui.input_action_button(
                    "filter_reset", "Reset",
                    class_="btn-outline-secondary btn-sm",
                    style="font-size:0.75em;"
                ),
                class_="d-flex gap-1"
            ),
        )

    def _op_label(op: str) -> str:
        return {"eq": "=", "ne": "≠", "gt": ">", "ge": "≥",
                "lt": "<", "le": "≤", "in": "∈", "not_in": "∉"}.get(op, op)

    # ── Filter recipe builder effects ─────────────────────────────────────────

    @reactive.Effect
    @reactive.event(input.filter_add_row)
    def _filter_add_row():
        """Append a new filter row to _pending_filters from the add-row form."""
        col = safe_input(input, "fb_col", None)
        op = safe_input(input, "fb_op", "eq")
        raw_val = safe_input(input, "fb_value", "")
        if not col:
            return
        # Determine dtype from current sample
        subtab = active_home_subtab.get()
        p_id = subtab.removeprefix("subtab_") if subtab else None
        spec = _resolve_active_spec(p_id)
        try:
            lf = _resolve_active_lf(spec)
            sample = lf.head(10).collect()
            dtype_str = str(sample[col].dtype) if col in sample.columns else "Utf8"
        except Exception:
            dtype_str = "Utf8"

        # raw_val may be a tuple (selectize multi), list, or a string
        if isinstance(raw_val, (list, tuple)):
            value = list(raw_val)
            if not value:
                return  # nothing selected — don't add an empty filter
            # Normalise op: multi-value selection always means set membership
            if op == "eq":
                op = "in"
            elif op == "ne":
                op = "not_in"
        elif isinstance(raw_val, str) and raw_val.strip():
            value = raw_val.strip()
        else:
            return  # empty value — don't add

        new_row = {"column": col, "op": op, "value": value, "dtype": dtype_str}
        current = list(_pending_filters.get())
        current.append(new_row)
        _pending_filters.set(current)

    @reactive.Effect
    @reactive.event(input.filter_apply)
    def _filter_apply():
        """Left-panel Apply.

        T1/T2 mode: commit _pending_filters → applied_filters (transient view).
        T3 mode: build pending T3 RecipeNodes from the staged rows; the right
        sidebar then shows them with mandatory reason fields. No separate
        "Apply to recipe" button — left Apply is the single entry point.
        """
        rows = list(_pending_filters.get())

        if tier_toggle.get() != "T3" or home_state is None:
            applied_filters.set(rows)
            return

        if not rows:
            ui.notification_show(
                "No filter rows to send. Add rows below first (the '+ Add' button).",
                type="warning", duration=5,
            )
            return

        from app.modules.session_manager import make_recipe_node
        state = home_state.get()
        active_subtab = state.get("active_plot_subtab") or "__all__"
        pending_nodes = list(state.get("_pending_t3_nodes", []))

        for frow in rows:
            params = {
                "column": frow.get("column", ""),
                "op": frow.get("op", "eq"),
                "value": frow.get("value", ""),
            }
            if frow.get("dtype"):
                params["dtype"] = frow.get("dtype")
            pending_nodes.append(make_recipe_node(
                "filter_row", params,
                plot_scope=active_subtab,
                reason="",
            ))

        home_state.set({**state, "_pending_t3_nodes": pending_nodes})
        # Clear staging — rows are now pending T3 nodes; plot stays filtered
        # via _t3_filter_rows() reading home_state.
        _pending_filters.set([])
        applied_filters.set([])
        ui.notification_show(
            f"✅ {len(rows)} filter(s) added to T3 pipeline. "
            "Add a reason in the right sidebar before applying.",
            type="message", duration=5,
        )

    @reactive.Effect
    @reactive.event(input.filter_reset)
    def _filter_reset():
        """Clear all pending and applied filters."""
        _pending_filters.set([])
        applied_filters.set([])

    @reactive.Effect
    @reactive.event(input.col_drop_to_audit)
    def _col_drop_to_audit():
        """Push deselected columns into the T3 audit pipeline as drop_column nodes.

        Reads the current preview_col_selector value, computes which dataset
        columns are NOT selected (and not already committed-dropped), and
        appends one `drop_column` RecipeNode per deselected column to
        _pending_t3_nodes. After commit, resets the selector to "all visible".
        """
        if home_state is None:
            return
        if tier_toggle.get() != "T3":
            return

        subtab = active_home_subtab.get()
        p_id = subtab.removeprefix("subtab_") if subtab else None
        spec = _resolve_active_spec(p_id)
        try:
            lf = _resolve_active_lf(spec)
        except Exception:
            return

        committed = set(_t3_drop_columns())
        choosable = [c for c in lf.columns if c not in committed]
        visible = safe_input(input, "preview_col_selector", choosable)
        vis_set = set(visible) if isinstance(visible, (list, tuple)) else set(choosable)
        to_drop = [c for c in choosable if c not in vis_set]

        if not to_drop:
            ui.notification_show(
                "No deselected columns to drop. Uncheck columns above first.",
                type="warning", duration=4,
            )
            return

        from app.modules.session_manager import make_recipe_node
        state = home_state.get()
        active_subtab = state.get("active_plot_subtab") or "__all__"
        pending_nodes = list(state.get("_pending_t3_nodes", []))
        for col in to_drop:
            pending_nodes.append(make_recipe_node(
                "drop_column", {"column": col},
                plot_scope=active_subtab,
                reason="",
            ))
        home_state.set({**state, "_pending_t3_nodes": pending_nodes})

        # Reset the selector so the user starts fresh on the remaining columns.
        remaining = [c for c in choosable if c in vis_set]
        ui.update_selectize("preview_col_selector",
                            choices=remaining, selected=remaining)

        ui.notification_show(
            f"✂️ {len(to_drop)} column(s) added to T3 pipeline. "
            "Add a reason in the right sidebar before applying.",
            type="message", duration=5,
        )

    # When btn_apply commits the T3 recipe, clear the left-panel filter list:
    # those rows are now permanent T3 nodes and should not be re-applicable as
    # transient filters. Triggered via t3_apply_count bumps in audit_stack.
    _last_apply_count = reactive.Value(0)

    @reactive.Effect
    def _clear_filters_on_t3_apply():
        """After T3 apply, clear left-panel filter staging.

        Both _pending_filters (staging UI) and applied_filters (active plot view)
        are cleared because T3 RecipeNodes now drive the plot via _t3_filter_rows
        (the legacy applied_filters path is no longer the source of truth once a
        node is committed to T3).
        """
        if home_state is None:
            return
        cnt = int(home_state.get().get("t3_apply_count", 0))
        if cnt > _last_apply_count.get():
            _last_apply_count.set(cnt)
            _pending_filters.set([])
            applied_filters.set([])

    # Dynamic remove buttons — one effect per row index up to a generous cap
    def _make_remove_handler(idx: int):
        @reactive.Effect
        @reactive.event(getattr(input, f"filter_remove_{idx}", lambda: None))
        def _remove():
            try:
                _ = getattr(input, f"filter_remove_{idx}")()
            except Exception:
                return
            current = list(_pending_filters.get())
            if idx < len(current):
                current.pop(idx)
                _pending_filters.set(current)
        return _remove

    # Register remove handlers for up to 50 filter rows
    _remove_handlers = [_make_remove_handler(i) for i in range(50)]

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
        cached_plot = bootloader.get_cached_asset(proj, coll, plot_id, "ref_plot")
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

    @render.ui
    def comparison_mode_toggle_ui():
        """ADR-043: Comparison Mode toggle (persona-gated, deferred full impl to Phase 21-E)."""
        p = current_persona.get()
        if p in ["pipeline_exploration_advanced", "project_independent", "developer"]:
            return ui.div(
                ui.input_switch("comparison_mode", "Comparison Mode", value=False),
                class_="d-flex align-items-center me-3",
                style="height: 36px; padding-top: 4px;"
            )
        return ui.div()
