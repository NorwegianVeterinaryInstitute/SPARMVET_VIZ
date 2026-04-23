"""app/handlers/home_theater.py
Home Theater Shiny wiring (ADR-043 / ADR-044 / ADR-045).

Entry point:
    define_server(input, output, session, *,
                  bootloader, wrangle_studio, dev_studio,
                  orchestrator, viz_factory, gallery_viewer,
                  current_persona, anchor_path, tier1_anchor,
                  tier_reference, tier3_leaf, active_cfg,
                  active_collection_id, safe_input, active_home_subtab, tier_toggle)

Concern: dynamic_tabs, sidebar_nav_ui, sidebar_tools_ui, right_sidebar_content_ui,
         sidebar_filters, system_tools_ui, plot_reference, table_reference,
         plot_leaf, table_leaf, handle_plot_brush, comparison_mode_toggle_ui.
Two-Category Law (ADR-045): This file contains @render.* and @reactive.*
decorators only. It MUST NOT be imported by non-Shiny contexts.
"""

from __future__ import annotations

# @deps
# provides: function:define_server (home_theater)
# consumes: app/modules/orchestrator.py, app/modules/wrangle_studio.py, app/modules/dev_studio.py, libs/viz_factory/src/viz_factory/viz_factory.py, utils/config_loader.py
# consumed_by: app/src/server.py
# doc: .antigravity/knowledge/architecture_decisions.md#ADR-043, .antigravity/knowledge/architecture_decisions.md#ADR-044, .antigravity/knowledge/architecture_decisions.md#ADR-045
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
                  active_home_subtab, tier_toggle):
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
            # Phase 21-F-2: Inject committed filters — coerce values to match column dtype.
            import copy
            plot_spec = copy.deepcopy(spec)
            filter_rows = applied_filters.get()
            if filter_rows:
                coerced = []
                for f in filter_rows:
                    fc = dict(f)
                    dtype_str = fc.pop("dtype", "Utf8")
                    val = fc.get("value")
                    try:
                        if "Int" in dtype_str or "UInt" in dtype_str:
                            fc["value"] = int(val) if not isinstance(val, list) else [int(v) for v in val]
                        elif "Float" in dtype_str:
                            fc["value"] = float(val) if not isinstance(val, list) else [float(v) for v in val]
                    except (ValueError, TypeError):
                        pass
                    coerced.append(fc)
                plot_spec["filters"] = coerced
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
        if p in ("pipeline_exploration_advanced", "project_independent", "developer"):
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

            # Apply committed row filters (predicate pushdown)
            for f in applied_filters.get():
                col = f.get("column")
                op = f.get("op", "eq")
                val = f.get("value")
                raw_dtype = f.get("dtype", "str")
                # Coerce value to match raw column dtype
                try:
                    if "Int" in raw_dtype or "UInt" in raw_dtype:
                        val = int(val) if not isinstance(val, list) else [int(v) for v in val]
                    elif "Float" in raw_dtype:
                        val = float(val) if not isinstance(val, list) else [float(v) for v in val]
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
                elif op == "in":
                    vals = val if isinstance(val, list) else [val]
                    lf = lf.filter(pl.col(col).is_in(vals))
                elif op == "not_in":
                    vals = val if isinstance(val, list) else [val]
                    lf = lf.filter(~pl.col(col).is_in(vals))

            df = lf.head(100).collect()

            # Apply column visibility selection (Phase 21-F-4)
            visible = safe_input(input, "preview_col_selector", None)
            if visible and isinstance(visible, (list, tuple)):
                # Keep only columns that exist in df
                visible_cols = [c for c in visible if c in df.columns]
                if visible_cols:
                    df = df.select(visible_cols)

            return render.DataGrid(df, filters=False, height="300px")
        except Exception as e:
            return render.DataGrid(
                pl.DataFrame({"Error": [str(e)]}),
                filters=False
            )

    # Phase 21-F-4: Column selector UI for data preview
    @output
    @render.ui
    def home_col_selector_ui():
        """Selectize multi-select for column visibility in the data preview."""
        subtab = active_home_subtab.get()
        p_id = subtab.removeprefix("subtab_") if subtab else None
        spec = _resolve_active_spec(p_id)
        try:
            lf = _resolve_active_lf(spec)
            cols = lf.columns
            return ui.div(
                ui.input_selectize(
                    "preview_col_selector",
                    label=None,
                    choices=cols,
                    selected=cols,
                    multiple=True,
                    options={"placeholder": "Select columns to show…", "plugins": ["remove_button"]},
                ),
                ui.tags.small("Visible columns (preview only)", class_="text-muted"),
                class_="mb-2",
                style="font-size: 0.8em;"
            )
        except Exception:
            return ui.div()

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
                ui.p("Data Ingestion (ADR-031)", class_="ultra-small fw-bold mb-1"),
                ui.div(
                    ui.input_file("file_ingest", None, multiple=True, accept=[".yaml"]),
                    class_="upload-row mb-1"
                ),
                ui.input_action_button("btn_ingest", "🚀 Ingest Manifests", class_="w-100"),
                class_="px-2"
            )
        )

    @output
    @render.ui
    def sidebar_filters():
        """
        Phase 21-F-1: Filter recipe builder.
        Renders pending filter rows from _pending_filters + an Add Row form.
        Reactive to active_home_subtab (column dropdown scoped to active dataset).
        State (_pending_filters, applied_filters) is NOT reset on tab switch —
        only on explicit Reset or dataset change.
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
            dtypes = {col: str(sample[col].dtype) for col in all_cols}
        except Exception:
            all_cols = []
            dtypes = {}
            sample = None

        pending = _pending_filters.get()

        # --- Render existing filter rows ---
        rows = []
        for i, f in enumerate(pending):
            col = f.get("column", "")
            op = f.get("op", "eq")
            val = f.get("value", "")
            dtype_str = f.get("dtype", "Utf8")

            # Display value as comma-separated if list
            val_display = ", ".join(str(v) for v in val) if isinstance(val, list) else str(val)

            rows.append(ui.div(
                ui.div(
                    ui.tags.small(
                        f"{col}  {_op_label(op)}  {val_display}",
                        class_="text-dark",
                        style="font-size:0.75em;"
                    ),
                    ui.tags.span(
                        ui.tags.small(f"[{dtype_str}]", class_="text-muted"),
                    ),
                    class_="flex-grow-1"
                ),
                ui.input_action_button(
                    f"filter_remove_{i}", "✕",
                    class_="btn-outline-danger btn-sm py-0 px-1",
                    style="font-size:0.7em; line-height:1;"
                ),
                class_="d-flex align-items-center gap-2 mb-1 px-1 py-1 border rounded bg-light",
            ))

        # --- Add row form ---
        col_choices = {c: f"{c}  [{dtypes.get(c,'')}]" for c in all_cols} if all_cols else {}

        # Op choices depend on selected column dtype
        sel_col = safe_input(input, "fb_col", all_cols[0] if all_cols else None)
        sel_dtype = dtypes.get(sel_col, "Utf8") if sel_col else "Utf8"
        is_discrete = (sel_col in discrete_cols) or (
            "Int" not in sel_dtype and "Float" not in sel_dtype and "UInt" not in sel_dtype
        )

        if is_discrete:
            op_choices = {"eq": "=", "ne": "≠", "in": "∈ (any of)", "not_in": "∉ (none of)"}
        else:
            op_choices = {"eq": "=", "ne": "≠", "gt": ">", "ge": "≥", "lt": "<", "le": "≤"}

        # Value widget: multi-select for discrete, numeric input for continuous
        sel_op = safe_input(input, "fb_op", list(op_choices.keys())[0])
        use_multiselect = is_discrete and sel_op in ("eq", "ne", "in", "not_in")

        if use_multiselect and sample is not None and sel_col in sample.columns:
            unique_vals = sorted([
                str(v) for v in sample[sel_col].drop_nulls().unique().to_list()
            ])
            value_widget = ui.input_selectize(
                "fb_value", label=None,
                choices=unique_vals, selected=[],
                multiple=True,
                options={"placeholder": "Select value(s)…", "plugins": ["remove_button"]},
            )
        else:
            value_widget = ui.input_text("fb_value", label=None, placeholder="Value…")

        add_form = ui.div(
            ui.tags.small("Add filter row:", class_="fw-semibold text-muted d-block mb-1"),
            ui.input_select("fb_col", label=None, choices=col_choices),
            ui.div(
                ui.input_select("fb_op", label=None, choices=op_choices,
                                width="90px"),
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

        # --- Apply / Reset buttons ---
        n_applied = len(applied_filters.get())
        apply_label = f"Apply ({len(pending)} row{'s' if len(pending) != 1 else ''})"
        status = (
            ui.tags.small(f"{n_applied} filter(s) active", class_="text-success d-block mb-1")
            if n_applied else ui.div()
        )

        p = current_persona.get()
        t3_btn = ui.div()
        if tier_toggle.get() == "T3" and p in (
                "pipeline_exploration_advanced", "project_independent", "developer"):
            t3_btn = ui.input_action_button(
                "filter_apply_recipe", "Apply to recipe",
                class_="btn-outline-warning btn-sm w-100 mt-1",
                style="font-size:0.75em;"
            )

        controls = ui.div(
            status,
            ui.div(
                ui.input_action_button(
                    "filter_apply", apply_label,
                    class_="btn-primary btn-sm flex-grow-1",
                    style="font-size:0.75em;"
                ),
                ui.input_action_button(
                    "filter_reset", "Reset",
                    class_="btn-outline-secondary btn-sm",
                    style="font-size:0.75em;"
                ),
                class_="d-flex gap-1"
            ),
            t3_btn,
            class_="mt-2 px-1"
        )

        return ui.div(
            ui.div(*rows) if rows else ui.tags.small(
                "No filters. Add rows below.", class_="text-muted d-block px-1 mb-1",
                style="font-size:0.75em;"
            ),
            add_form,
            controls,
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

        # raw_val may be a list (selectize multi) or a string
        if isinstance(raw_val, (list, tuple)):
            value = list(raw_val)
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
        """Commit pending filters → applied_filters (consumed by plots + preview)."""
        applied_filters.set(list(_pending_filters.get()))

    @reactive.Effect
    @reactive.event(input.filter_reset)
    def _filter_reset():
        """Clear all pending and applied filters."""
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
