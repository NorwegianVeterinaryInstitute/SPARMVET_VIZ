#!/bin/bash

# Creating context files with repomix
# https://github.com/yamadashy/repomix
# bash /home/evezeyl/Documents/Insync/gdrive/OBSWORK/20_GITS/distrobox/scripts/SPARMVET_VIZ_GEM_context.sh

PROJECT_ROOT="/home/evezeyl/Documents/Insync/gdrive/OBSWORK/20_GITS/SPARMVET_VIZ"

# Create a tree of the working directory 
tree_file="${PROJECT_ROOT}/tree.txt"
tree "${PROJECT_ROOT}" > "${tree_file}"

# Function to make paths relative to PROJECT_ROOT
to_relative() {
    echo "$1" | sed "s|^${PROJECT_ROOT}/||"
}

# Extra integration - if needed 
## Eg. Find all python files in core libraries recursively
## extra_files=$(find "${PROJECT_ROOT}/libs/connector/src" "${PROJECT_ROOT}/libs/ingestion/src" \
#"${PROJECT_ROOT}/libs/transformer/src" "${PROJECT_ROOT}/libs/viz_factory/src" -name "*.py")
#If want dasharch "${PROJECT_ROOT}/.agents/rules/dasharch.md"
# extra_files="$(find "${PROJECT_ROOT}/assets/template_manifests" -name "*.yaml"; find "${PROJECT_ROOT}/config/manifests/pipelines" \( -name "STRESS*.yaml" -o -name "The*.yaml" \))"
# extra_files=(
#     "${PROJECT_ROOT}/EVE_WORK/daily/2026-04-02/Gemini-chat_UI-Strategic-Next-Steps.md"
#     "${PROJECT_ROOT}/EVE_WORK/daily/2026-04-02/Dashboard_Vision_summary1.md"
#     "${PROJECT_ROOT}/EVE_WORK/daily/2026-04-08/UI_Definition.md"
#     "${PROJECT_ROOT}/EVE_WORK/daily/2026-04-08/UI_AI_Discussion.md"
#     "${PROJECT_ROOT}/EVE_WORK/daily/2026-04-08/Gemini-UI Development Plan Discussion.md"
#     "${PROJECT_ROOT}/EVE_WORK/daily/2026-04-09/clarification_plot_data_showing.md"
#     "${PROJECT_ROOT}/EVE_WORK/daily/2026-04-09/Comparison_SideDataPolts_Tiers_Claude_implementation_plan.md"
#     "${PROJECT_ROOT}/EVE_WORK/daily/2026-04-10/Rgallery_inspiration_reproduction.md"
# )
extra_files=""

# Define paths to context files - right now 8 files
## The antigravity GEM initial context uploaded already - only change when needed
# .agents/rules/
workspace_standard="${PROJECT_ROOT}/.agents/rules/workspace_standard.md"
rules_asset_scripts="${PROJECT_ROOT}/.agents/rules/rules_asset_scripts.md"
rules_data_engine="${PROJECT_ROOT}/.agents/rules/rules_data_engine.md"
rules_documentation_aesthetics="${PROJECT_ROOT}/.agents/rules/rules_documentation_aesthetics.md"
rules_manifest_structure="${PROJECT_ROOT}/.agents/rules/rules_manifest_structure.md"
rules_runtime_environment="${PROJECT_ROOT}/.agents/rules/rules_runtime_environment.md"
rules_ui_dashboard="${PROJECT_ROOT}/.agents/rules/rules_ui_dashboard.md"
rules_verification_testing="${PROJECT_ROOT}/.agents/rules/rules_verification_testing.md"

# .agents/workflows
implementation_workflow_transformer="${PROJECT_ROOT}/.agents/workflows/implementation_workflow_transformer.md"
ingestion_testing="${PROJECT_ROOT}/.agents/workflows/ingestion_testing.md"
transformer_testing="${PROJECT_ROOT}/.agents/workflows/transformer_testing.md"
ui_manifest_integration_testing="${PROJECT_ROOT}/.agents/workflows/ui_manifest_integration_testing.md"
verification_protocol="${PROJECT_ROOT}/.agents/workflows/verification_protocol.md"
viz_factory_implementation="${PROJECT_ROOT}/.agents/workflows/viz_factory_implementation.md"
viz_factory_testing="${PROJECT_ROOT}/.agents/workflows/viz_factory_testing.md"


# .antigravity/knowledge/
architecture_decisions="${PROJECT_ROOT}/.antigravity/knowledge/architecture_decisions.md"
project_conventions="${PROJECT_ROOT}/.antigravity/knowledge/project_conventions.md"
protocol_tiered_data="${PROJECT_ROOT}/.antigravity/knowledge/protocol_tiered_data.md"
persona_traceability_matrix="${PROJECT_ROOT}/.antigravity/knowledge/persona_traceability_matrix.md"

milestones="${PROJECT_ROOT}/.antigravity/knowledge/milestones.md"
blockers="${PROJECT_ROOT}/.antigravity/knowledge/blockers.md"


# .antigravity/plans : implementation plan 
implementation_plan="${PROJECT_ROOT}/.antigravity/plans/implementation_plan_master.md"

# .antigravity/tasks
tasks="${PROJECT_ROOT}/.antigravity/tasks/tasks.md"

DATE=$(date +%Y%m%d_%H%M%S)
OUTPUT_FILE="${PROJECT_ROOT}/EVE_WORK/GEM_CONTEXT_${DATE}.md"

# Ensure output directory exists
mkdir -p "${PROJECT_ROOT}/EVE_WORK"

echo "Generating context for GEM..."

# Building the relative INCLUDE_LIST
# tree_file is mandatory
REL_INCLUDE_LIST="$(to_relative "${tree_file}")"

# Add standard files
for p in "${workspace_standard}" "${rules_asset_scripts}" "${rules_data_engine}" "${rules_documentation_aesthetics}" \
         "${rules_manifest_structure}" "${rules_runtime_environment}" "${rules_ui_dashboard}" "${rules_verification_testing}" \
         "${implementation_workflow_transformer}" "${ingestion_testing}" "${transformer_testing}" \
         "${ui_manifest_integration_testing}" "${verification_protocol}" "${viz_factory_implementation}" \
         "${viz_factory_testing}" \
         "${architecture_decisions}" "${project_conventions}" "${protocol_tiered_data}" "${persona_traceability_matrix}" \
         "${blockers}" "${milestones}" "${implementation_plan}" "${tasks}"; do
    if [ -f "$p" ]; then
        REL_INCLUDE_LIST="${REL_INCLUDE_LIST},$(to_relative "$p")"
    fi
done

# Add extra library files
for f in "${extra_files[@]}"; do
    if [ -f "$f" ]; then
        REL_INCLUDE_LIST="${REL_INCLUDE_LIST},$(to_relative "$f")"
    fi
done

cd "${PROJECT_ROOT}"

distrobox enter repomix-env --name repomix-env --no-tty -- \
  repomix --style markdown \
  --no-directory-structure \
  --parsable-style \
  --no-file-summary \
  --include "${REL_INCLUDE_LIST}" \
  --output "${OUTPUT_FILE}"

echo "Context file generated at: ${OUTPUT_FILE}"
echo "Please find the updated context for your sync process (one aggregated file)"
