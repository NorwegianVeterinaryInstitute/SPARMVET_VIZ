"""app/handlers/data_import_handlers.py
Data Import accordion panel — testing_mode-aware data path display + ingestion slots.

New in Phase 25-F (ADR-052). Replaces the data ingestion slots that previously
lived in system_tools_ui.

Two-Category Law (ADR-045): this module contains @render.* / @reactive.*
decorators only. It MUST NOT be imported by non-Shiny contexts.

Display rules
-------------
- testing_mode == False  (pipeline-static, pipeline-exploration-simple):
    Read-only display of the configured/injected data paths derived from
    the active manifest's data_schemas. The user cannot override paths;
    they are fixed by the deployment configuration.
- testing_mode == True   (developer, qa, pipeline-exploration-advanced,
    project-independent):
    Same listing but framed as the *current default* and accompanied by
    the manifest replacement upload (gated by metadata_ingestion_enabled)
    and the multi-file ingestion slot (gated by data_ingestion_enabled).

Reactive value passed in: active_cfg (so the listing refreshes on project
switch).
"""

from __future__ import annotations

# @deps
# provides: function:define_data_import_server, output:data_import_ui
# consumes: app/modules/orchestrator.py, app/src/bootloader.py, shiny
# consumed_by: app/handlers/home_theater.py
# doc: .antigravity/knowledge/architecture_decisions.md#ADR-045, .antigravity/knowledge/architecture_decisions.md#ADR-052
# @end_deps

from shiny import render, ui

from app.src.bootloader import bootloader


def define_data_import_server(input, output, session, *,
                              orchestrator, active_cfg, safe_input):
    """Register the Data Import panel render handler.

    Parameters
    ----------
    orchestrator : DataOrchestrator
        Used to resolve the active project's source-file paths.
    active_cfg : reactive.Calc
        Active ConfigManager — read so the panel refreshes on project switch.
    safe_input : callable
        safe_input(input, key, default) → value.
    """

    @output
    @render.ui
    def data_import_ui():
        cfg = active_cfg()  # subscribe to project switches
        proj_id = safe_input(input, "project_id", bootloader.get_default_project())
        testing_mode = bootloader.get_testing_mode()
        prefer_discovery = bootloader.connector_config.get("prefer_discovery", False)

        # ── Source-file listing ─────────────────────────────────────────────
        if prefer_discovery:
            # Production path: data injected by connector — show raw_data_dir
            raw_data_dir = bootloader.get_location("raw_data")
            files_block = ui.div(
                ui.tags.small(
                    "Data location (provided by deployment):",
                    class_="text-muted fw-semibold d-block mb-1",
                    style="font-size:0.7em;",
                ),
                ui.tags.code(
                    str(raw_data_dir),
                    style="font-size:0.7em; word-break:break-all;",
                ),
                class_="px-2",
            )
        else:
            try:
                source_files = orchestrator.get_source_files(proj_id) if proj_id else {}
            except Exception:
                source_files = {}

            if source_files:
                file_rows = [
                    ui.div(
                        ui.tags.small(
                            f"{ds_id}: ",
                            class_="text-muted fw-semibold",
                            style="font-size:0.7em;",
                        ),
                        ui.tags.code(
                            str(path),
                            style="font-size:0.7em; word-break:break-all;",
                        ),
                        class_="mb-1",
                    )
                    for ds_id, path in sorted(source_files.items())
                ]
                files_block = ui.div(
                    *file_rows,
                    class_="px-2",
                    style="max-height:80px; overflow-y:auto;",
                )
            else:
                files_block = ui.tags.small(
                    "No source files resolved for this manifest.",
                    class_="text-muted px-2 d-block",
                    style="font-size:0.7em;",
                )

        if not testing_mode:
            # Pipeline personas: read-only — explicit framing so the user
            # understands the paths are fixed by deployment configuration.
            return ui.div(
                ui.tags.small(
                    "🔒 Data paths are set by the deployment configuration (read-only).",
                    class_="text-info d-block mb-1 px-2",
                    style="font-size:0.7em;",
                ),
                files_block,
                class_="mb-2",
                style="font-size:0.8em;",
            )

        # ── Testing mode: same listing + override + ingestion slots ────────
        upload_blocks: list = []

        if bootloader.is_enabled("metadata_ingestion_enabled"):
            upload_blocks.append(
                ui.div(
                    ui.tags.small(
                        "Metadata replacement (TSV)",
                        class_="text-muted fw-semibold d-block mb-1",
                        style="font-size:0.72em;",
                    ),
                    ui.input_file(
                        "data_import_metadata_upload", None,
                        accept=[".tsv", ".csv"], multiple=False,
                    ),
                    class_="mb-2 px-2",
                )
            )

        if bootloader.is_enabled("data_ingestion_enabled"):
            upload_blocks.append(
                ui.div(
                    ui.tags.small(
                        "Multi-file / Excel ingestion",
                        class_="text-muted fw-semibold d-block mb-1",
                        style="font-size:0.72em;",
                    ),
                    ui.input_file(
                        "data_import_multi_upload", None,
                        accept=[".tsv", ".csv", ".xlsx", ".xls"], multiple=True,
                    ),
                    ui.tags.small(
                        "Mapping each file to its dataset is performed at apply time.",
                        class_="text-muted d-block",
                        style="font-size:0.65em;",
                    ),
                    class_="mb-2 px-2",
                )
            )

        return ui.div(
            ui.tags.small(
                "Current default data paths (override below for testing):",
                class_="text-muted d-block mb-1 px-2",
                style="font-size:0.7em;",
            ),
            files_block,
            ui.hr(style="margin:6px 0;") if upload_blocks else ui.div(),
            *upload_blocks,
            class_="mb-2",
            style="font-size:0.8em;",
        )
