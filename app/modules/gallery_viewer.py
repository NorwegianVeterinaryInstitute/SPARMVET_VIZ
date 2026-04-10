from shiny import ui, reactive, render
import yaml
from pathlib import Path


class GalleryViewer:
    """
    GalleryViewer (gallery_viewer.py)
    Architectural context: ADR-033 Split-Pane Gallery and Submission Gate.
    """

    def __init__(self):
        pass

    def submission_modal_ui(self):
        """
        Renders the Submission Gate Modal with mandatory checklist.
        ADR-033: Enforce MD file presence before submission.
        """
        return ui.modal(
            ui.h4("Public Gallery: Quality Submission Gate"),
            ui.div(
                ui.p(
                    "Your analysis is ready for sharing. Please verify the documentation triplet:"),
                ui.div(
                    ui.input_checkbox(
                        "check_yaml", "✅ Recipe Logic (.yaml)", value=True),
                    ui.input_checkbox(
                        "check_tsv", "✅ Reference Data (.tsv)", value=True),
                    ui.input_checkbox(
                        "check_png", "✅ Plot Evidence (.png)", value=True),
                    ui.input_checkbox(
                        "check_md", "📄 Educational Metadata (.md)", value=False),
                    class_="p-3 border rounded bg-light mb-3"
                ),
                ui.div(
                    ui.p("Educational metadata is MANDATORY for all Gallery submissions.",
                         class_="text-warning small"),
                    ui.input_action_button(
                        "btn_autofill_meta", "📝 Autofill template from Audit Stack", class_="btn-sm btn-outline-info w-100"),
                    class_="mb-3"
                )
            ),
            ui.div(
                ui.input_action_button(
                    "btn_confirm_submission", "🚀 Confirm & Upload", class_="btn-primary"),
                ui.modal_button("Cancel"),
                class_="d-flex justify-content-end gap-2"
            ),
            title="Gallery Submission",
            size="l",
            easy_close=True
        )

    def split_viewer_layout(self, recipe_id="active"):
        """
        Implements the ADR-033 50/50 Split-Pane UI.
        Left: Technical / Right: Educational (Soft Note Aesthetic).
        """
        return ui.layout_columns(
            # Technical Left Pane
            ui.navset_card_tab(
                ui.nav_panel("Plot Preview", ui.output_plot(
                    "gallery_plot_preview")),
                ui.nav_panel("Data Sample", ui.output_table(
                    "gallery_table_preview")),
                ui.nav_panel("YAML Recipe", ui.output_text_verbatim(
                    "gallery_yaml_preview")),
                id="gallery_tech_tabs"
            ),
            # Educational Right Pane (Soft Note Aesthetic)
            ui.div(
                ui.h5("Visual Cookbook: Guidance", class_="fw-bold"),
                ui.hr(),
                ui.output_ui("gallery_md_content"),
                class_="p-4 rounded border shadow-sm",
                style="background-color: #fff9c4; border-color: #f9eeb1; color: #5f5a3a; min-height: 500px;"
            ),
            col_widths=[6, 6]
        )

    def autofill_meta_from_audit(self, audit_stack, persona="Standard User"):
        """
        Helper to generate the mandatory Markdown headers from session audit data.
        ADR-033: Include Author & License section.
        """
        headers = [
            "# Recipe Meta: Autofilled from Session Audit",
            "",
            "## Author & License",
            f"- **Author**: {persona}",
            f"- **License**: Creative Commons Attribution 4.0 International (CC-BY 4.0)",
            "",
            "## 1. Suitability (When to Use)",
            "- [x] Derived from specific session transformations.",
            "",
            "## 2. Data Schema (Tier 1 Requirements)",
            "- Columns required for visualization mappings.",
            "",
            "## 3. Transformation Logic (Tier 2 Logic)",
            "The following logic nodes were utilized in this recipe:"
        ]

        for i, node in enumerate(audit_stack):
            action = node.get("action", "unknown")
            comment = node.get("comment", "No justification provided.")
            headers.append(f"- **Step {i+1} ({action})**: {comment}")

        headers.extend([
            "",
            "## 4. Interpretations & Assumptions",
            "- Standard SPARMVET interpretation applies."
        ])

        return "\n".join(headers)


# Singleton for import
gallery_viewer = GalleryViewer()
