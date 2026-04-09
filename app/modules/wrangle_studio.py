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

    def render_ui(self):
        actions = list(AVAILABLE_WRANGLING_ACTIONS.keys())

        return ui.div(
            ui.h4("Wrangle Studio: Logic Architect"),
            ui.p("Visually chain transformation nodes to reshape your data."),
            ui.hr(),
            ui.layout_columns(
                ui.card(
                    ui.card_header("available Actions"),
                    ui.input_select("action_selector",
                                    "1. Select Action:", choices=actions),
                    ui.input_select("column_selector", "2. Target Column:", choices=[
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
                    ui.card_header("Logic Stack (Sequential)"),
                    ui.output_ui("logic_stack_ui"),
                    ui.input_action_button(
                        "btn_clear_stack", "🗑️ Clear All nodes", class_="btn-outline-danger btn-sm mt-3")
                ),
                col_widths=[4, 8]
            ),
            class_="wrangle-studio-container"
        )

    def define_server(self, input, output, session, available_cols):

        # Sync column selector with the active dataset
        @reactive.Effect
        def update_column_list():
            cols = available_cols()
            if cols:
                ui.update_select("column_selector", choices=cols)
            else:
                ui.update_select("column_selector", choices=[
                                 "No Columns Detected"])

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
            curr = self.logic_stack.get().copy()
            action = input.action_selector()
            target_col = input.column_selector()
            extra_val = input.new_param_value()

            # Agnostic Param Assembly
            params = {"columns": [target_col]}

            if action == "rename" and extra_val:
                params["new_name"] = extra_val
            elif action == "cast" and extra_val:
                params["dtype"] = extra_val
            elif action == "fill_nulls" and extra_val:
                params["value"] = extra_val

            curr.append({"action": action, "params": params})
            self.logic_stack.set(curr)
            ui.notification_show(
                f"Node added: {action}({target_col})", type="message")

        @reactive.Effect
        @reactive.event(input.btn_clear_stack)
        def clear_stack():
            self.logic_stack.set([])
            ui.notification_show("Logic stack cleared.", type="warning")

        @output
        @render.ui
        def logic_stack_ui():
            nodes = self.logic_stack.get()
            if not nodes:
                return ui.p("No active transformation nodes. Add one to begin.")

            ui_nodes = []
            for i, node in enumerate(nodes):
                ui_nodes.append(
                    ui.div(
                        ui.div(
                            ui.span(
                                f"Node {i+1}: {node['action']}", class_="fw-bold"),
                            ui.span(
                                f"Params: {node['params']}", class_="ms-3 text-muted"),
                        ),
                        class_="p-2 mb-2 border rounded shadow-sm bg-light d-flex justify-content-between align-items-center"
                    )
                )
            return ui.div(*ui_nodes)

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
