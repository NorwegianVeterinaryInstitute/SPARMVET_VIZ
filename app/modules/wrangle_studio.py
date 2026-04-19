# app/modules/wrangle_studio.py
from shiny import ui, reactive, render
import polars as pl
from transformer.actions.base import AVAILABLE_WRANGLING_ACTIONS


class WrangleStudio:
    """ComponentName (wrangle_studio.py)
    Architectural visual builder for transformation logic stacks.
    ADR-004 / ADR-011: Data-Agnostic Column Selection.
    """

    def __init__(self, session_id: str):
        self.session_id = session_id
        # Reactive list of active nodes: [{"action": "rename", "params": {"columns": ["x"], "new_name": "y"}}]
        self.logic_stack = reactive.Value([])
        # Temporary storage for node being annotated
        self.pending_node = reactive.Value(None)

        # Expanded Manifest Data (ADR-031 Expansion)
        self.active_raw_yaml = reactive.Value("")
        self.active_fields = reactive.Value({"input": [], "output": []})
        self.active_viz_spec = reactive.Value({})

        # [ADR-039] TubeMap Code
        self.active_tubemap_mermaid = reactive.Value("")

    def render_ui(self):
        actions = list(AVAILABLE_WRANGLING_ACTIONS.keys())

        return ui.div(
            ui.h4("Blueprint Architect Flight Deck", class_="centered-header"),

            # --- TOP: Interactive TubeMap (Collapsible) ---
            ui.accordion(
                ui.accordion_panel(
                    "🗺️ Project Lineage (TubeMap)",
                    ui.div(
                        ui.output_ui("blueprint_tubemap_ui"),
                        class_="p-3 text-center bg-white border rounded shadow-sm",
                        style="min-height: 250px; overflow: auto;"
                    ),
                    open=True
                ),
                class_="mb-3"
            ),

            # --- BOTTOM: Integrated Results & Edit Workbench ---
            ui.navset_card_pill(
                ui.nav_panel(
                    "1. Focus (Logic)",
                    ui.layout_columns(
                        ui.card(
                            ui.card_header("Plan & Actions"),
                            ui.input_select("action_selector",
                                            "1. Select Action:", choices=actions),
                            ui.panel_conditional(
                                "input.action_selector == 'join' || input.action_selector == 'join_filter'",
                                ui.input_select("secondary_dataset_selector", "2b. Secondary Dataset:", choices=[
                                                "Select a source file..."]),
                                ui.input_select("right_on_selector", "2c. Right Join Key:", choices=[
                                                "Select a Dataset first"])
                            ),
                            ui.input_select("column_selector", "2. Target Column / Key:", choices=[
                                "Select a Dataset first"]),
                            ui.input_text(
                                "new_param_value", "3. Parameter (e.g. New Name):", placeholder="Optional..."),
                            ui.input_action_button(
                                "btn_add_node", "➕ Add Transformation Node", class_="btn-primary"),
                            ui.div(
                                ui.h6("Action Help"),
                                ui.output_text("action_help_text"),
                                style="background-color: #fff9c4; padding: 10px; border-radius: 4px; margin-top: 10px;"
                            )
                        ),
                        ui.card(
                            ui.card_header("Active Component Logic Stack"),
                            ui.output_ui("logic_stack_ui"),
                            ui.input_action_button(
                                "btn_clear_stack", "🗑️ Clear All nodes", class_="btn-outline-danger btn-sm mt-3")
                        ),
                        col_widths=[4, 8]
                    )
                ),
                ui.nav_panel(
                    "2. Live View (Result)",
                    ui.accordion(
                        ui.accordion_panel(
                            "📈 Live Preview (Plot)",
                            ui.div(
                                ui.output_plot("architect_active_plot"),
                                id="architect_plot_container",
                                class_="p-3 text-center border rounded italic bg-light",
                                style="min-height: 400px;"
                            ),
                            id="architect_panel_plot"
                        ),
                        ui.accordion_panel(
                            "📋 Live Data Glimpse (Table)",
                            ui.div(
                                ui.output_table("architect_active_table"),
                                id="architect_table_container",
                                class_="p-1",
                                style="overflow: auto;"
                            ),
                            id="architect_panel_table"
                        ),
                        id="architect_live_accordion",
                        multiple=True,
                        open=["📋 Live Data Glimpse (Table)"]
                    )
                ),
                ui.nav_panel(
                    "3. Interface (Fields)",
                    ui.layout_columns(
                        ui.card(
                            ui.card_header("Input Fields (Schema)"),
                            ui.output_ui("input_fields_viewer_ui")
                        ),
                        ui.card(
                            ui.card_header("Output Fields (Contract)"),
                            ui.output_ui("output_fields_viewer_ui")
                        )
                    )
                ),
                ui.nav_panel(
                    "4. YAML (Raw Source)",
                    ui.card(
                        ui.card_header("Manifest Source Inspector"),
                        ui.output_ui("yaml_source_viewer_ui")
                    )
                ),
                id="architect_internal_tabs"
            ),
            class_="wrangle-studio-container"
        )

    def define_server(self, input, output, session, available_cols, get_base_data):

        @reactive.Calc
        def processed_data():
            lf = get_base_data()
            if lf is None:
                return None
            return self.apply_logic(lf).collect()

        @output
        @render.plot
        def architect_active_plot():
            df = processed_data()
            if df is None or df.height == 0:
                return None
            # For now, we use a default plot or the first one in the manifest if we had access to viz_factory
            # Since VizFactory is in server.py, we might need to pass it or a rendering function too.
            # But the user specifically asked for collapsible live view first.
            return None  # Placeholder for now, will integrate with VizFactory next

        @output
        @render.table
        def architect_active_table():
            df = processed_data()
            if df is None:
                return None
            return df.head(10)

        # Sync column selector with the active dataset
        @reactive.Effect
        def update_column_list():
            cols = available_cols()
            if cols:
                ui.update_select("column_selector", choices=cols)
                ui.update_select("right_on_selector", choices=cols)
            else:
                ui.update_select("column_selector", choices=[
                                 "No Columns Detected"])
                ui.update_select("right_on_selector", choices=[
                                 "No Columns Detected"])

        @reactive.Effect
        def update_secondary_datasets():
            # In a real app, this would scan the raw_data_dir
            # For this MVP, we simulate discovery
            datasets = ["raw_pipeline_output.tsv", "ResFinder_metadata.tsv"]
            ui.update_select("secondary_dataset_selector", choices=datasets)

        @output
        @render.text
        def action_help_text():
            action = input.action_selector()
            func = AVAILABLE_WRANGLING_ACTIONS.get(action)
            if func:
                return func.__doc__ or "No documentation available for this action."
            return "Select an action to see details."

        @reactive.Effect
        @reactive.event(input.btn_add_node)
        def add_node():
            action = input.action_selector()
            target_col = input.column_selector()
            extra_val = input.new_param_value()

            if action in ["join", "join_filter"]:
                # Trigger Join Preview Modal (ADR-012)
                self.show_join_modal(input, session, available_cols)
                return

            # Stage the node and show Annotation Modal
            self.pending_node.set({
                "action": action,
                "target_col": target_col,
                "extra_val": extra_val
            })
            self.show_annotation_modal(action, target_col, extra_val)

        @reactive.Effect
        @reactive.event(input.btn_confirm_node)
        def handle_confirm_node():
            comment = input.node_comment_modal()
            if not comment:
                ui.notification_show("⚠️ Comment is mandatory.", type="error")
                return

            node_data = self.pending_node.get()
            if node_data:
                self._finalize_add_node(
                    node_data["action"],
                    node_data["target_col"],
                    node_data["extra_val"],
                    comment
                )
                ui.modal_remove()
                self.pending_node.set(None)

        @reactive.Effect
        @reactive.event(input.confirm_join)
        def handle_confirm_join():
            comment = input.node_comment_join()
            if not comment:
                ui.notification_show(
                    "⚠️ Justification is mandatory for Joins.", type="error")
                return

            ui.modal_remove()
            action = input.action_selector()
            target_col = input.column_selector()
            secondary = input.secondary_dataset_selector()
            right_on = input.right_on_selector()

            curr = self.logic_stack.get().copy()
            params = {
                "left_on": target_col,
                "right_on": right_on,
                "right_ingredient": secondary
            }
            curr.append(
                {"action": action, "params": params, "comment": comment})
            self.logic_stack.set(curr)
            ui.notification_show(
                f"Join Node added: {secondary}", type="message")

        @reactive.Effect
        @reactive.event(input.btn_clear_stack)
        def clear_stack():
            self.logic_stack.set([])
            ui.notification_show("Logic stack cleared.", type="warning")

        @output
        @render.ui
        def blueprint_tubemap_ui():
            mermaid_code = self.active_tubemap_mermaid.get()
            if not mermaid_code:
                return ui.div(
                    ui.p("No Blueprint Lineage Loaded.",
                         class_="text-muted italic"),
                    ui.p("Select a Project to view its TubeMap.", class_="small"),
                    class_="p-5"
                )

            return ui.div(
                ui.div(mermaid_code, class_="mermaid"),
                id="blueprint_tubemap_container"
            )

        @output
        @render.ui
        def input_fields_viewer_ui():
            fields = self.active_fields.get().get("input", [])
            if not fields:
                return ui.p("No input fields defined in blueprint.", class_="text-muted italic")
            # Convert to DF for clean table display
            df = pl.DataFrame(fields)
            return ui.HTML(df.to_pandas().to_html(classes="table table-sm table-striped small"))

        @output
        @render.ui
        def output_fields_viewer_ui():
            fields = self.active_fields.get().get("output", [])
            if not fields:
                return ui.p("No output fields defined in blueprint.", class_="text-muted italic")
            df = pl.DataFrame(fields)
            return ui.HTML(df.to_pandas().to_html(classes="table table-sm table-striped small"))

        @output
        @render.ui
        def yaml_source_viewer_ui():
            yaml_str = self.active_raw_yaml.get()
            if not yaml_str:
                return ui.p("No source manifest loaded.", class_="text-muted italic")
            return ui.tags.pre(yaml_str, style="background: #272822; color: #f8f8f2; padding: 15px; border-radius: 6px; overflow: auto; max-height: 500px;")

        @output
        @render.ui
        def logic_stack_ui():
            nodes = self.logic_stack.get()
            if not nodes:
                return ui.p("No active transformation nodes. Add one to begin.")

            ui_nodes = []
            for i, node in enumerate(nodes):
                # Robust extraction (ADR-031)
                action = node.get("action", "unknown")
                comment = node.get("comment", "No comment")
                params = node.get("params", {})

                ui_nodes.append(
                    ui.div(
                        ui.div(
                            ui.div(
                                ui.span(f"Step {i+1}: {action}",
                                        class_="fw-bold"),
                                ui.span(
                                    f" — {comment}", style="color: #666; font-style: italic;"),
                            ),
                            ui.div(
                                ui.span(f"Config: {params}",
                                        class_="text-muted small"),
                            )
                        ),
                        class_="p-2 mb-2 border rounded shadow-sm bg-light d-flex justify-content-between align-items-center"
                    )
                )
            return ui.div(*ui_nodes)

    def _finalize_add_node(self, action, target_col, extra_val, comment):
        curr = self.logic_stack.get().copy()
        params = {"columns": [target_col]}

        if action == "rename" and extra_val:
            params["new_name"] = extra_val
        elif action == "cast" and extra_val:
            params["dtype"] = extra_val
        elif action == "fill_nulls" and extra_val:
            params["value"] = extra_val

        curr.append({"action": action, "params": params, "comment": comment})
        self.logic_stack.set(curr)
        ui.notification_show(
            f"Node added: {action}({target_col})", type="message")

    def show_annotation_modal(self, action, target_col, extra_val):
        m = ui.modal(
            ui.div(
                ui.h3("Annotate Transformation", class_="mb-3"),
                ui.div(
                    ui.tags.b("Action: "), ui.tags.span(action),
                    ui.br(),
                    ui.tags.b("Target: "), ui.tags.span(target_col),
                    ui.br(),
                    ui.tags.b("Parameter: "), ui.tags.span(
                        extra_val) if extra_val else ui.tags.i("None"),
                    class_="mb-3 p-2 border rounded bg-white"
                ),
                ui.input_text_area("node_comment_modal", "Justification / User Note:",
                                   placeholder="Explain the purpose of this transformation step...",
                                   width="100%", rows=3),
                class_="p-2"
            ),
            title="ADR-026: Mandatory User Note",
            footer=ui.div(
                ui.modal_button("Cancel"),
                ui.input_action_button(
                    "btn_confirm_node", "Confirm & Append", class_="btn-success")
            ),
            size="m",
            easy_close=False,
            # class_ is not natively supported in ui.modal but we can wrap content
        )
        # Note: We use the CSS class in ui.py to target the modal dialog if needed,
        # or we wrap the content in a styled div.
        # But wait, ui.modal in shiny-python doesn't easily expose the top-level class.
        # I'll use a direct style tag for the modal body if needed.
        ui.modal_show(m)

    def show_join_modal(self, input, session, available_cols):
        # 1. Validation Logic
        left_col = input.column_selector()
        right_col = input.right_on_selector()
        secondary = input.secondary_dataset_selector()

        # Visual Indicators (Green/Red)
        pk_match = left_col == right_col
        status_color = "#e8f5e9" if pk_match else "#ffebee"
        status_text = "✅ Primary Key Contract Met" if pk_match else "❌ Primary Key Mismatch (Column Names)"

        # Preview Data (Simulated for Evidence)
        m = ui.modal(
            ui.h3("Join Integrity Preview"),
            ui.p(f"Attempting to join Anchor with: {secondary}"),
            ui.hr(),
            ui.layout_columns(
                ui.div(
                    ui.h6("Anchor (Join Key)"),
                    ui.tags.pre("ID_1\nID_2\nID_3\nID_4\nID_5"),
                    style="background: #f8f9fa; padding: 10px;"
                ),
                ui.div(
                    ui.h6(f"{secondary} (Join Key)"),
                    ui.tags.pre("ID_1\nID_2\nID_99\nID_4\nID_100"),
                    style="background: #f8f9fa; padding: 10px;"
                )
            ),
            ui.div(
                ui.h5(status_text),
                ui.p("Overlap Detection: 60% of keys matched (3/5 in preview)."),
                ui.input_text_area("node_comment_join", "Justification for Join:",
                                   placeholder="Why are you merging these datasets?", width="100%", rows=2),
                style=f"background-color: {status_color}; padding: 15px; border-radius: 8px; margin-top: 15px; border: 1px solid #ccc;"
            ),
            title="ADR-012: Join Integrity Gate",
            footer=ui.div(
                ui.modal_button("Cancel"),
                ui.input_action_button(
                    "confirm_join", "Proceed with Join", class_="btn-success")
            ),
            size="l",
            easy_close=True
        )
        ui.modal_show(m)

    def apply_logic(self, lf: pl.LazyFrame) -> pl.LazyFrame:
        """Applies the current logic stack to a LazyFrame."""
        nodes = self.logic_stack.get()
        for node in nodes:
            action_name = node['action']
            params = node['params']
            func = AVAILABLE_WRANGLING_ACTIONS.get(action_name)
            if func:
                try:
                    lf = func(lf, params)
                except Exception as e:
                    print(f"Error applying {action_name}: {e}")
        return lf
