#!/bin/bash
# Silence LD_PRELOAD warnings for distrobox/NX environments
unset LD_PRELOAD

# Creating context files with repomix
# https://github.com/yamadashy/repomix
# bash /home/evezeyl/Documents/Insync/gdrive/OBSWORK/20_GITS/distrobox/scripts/SPARMVET_VIZ_GEM_context.sh

PROJECT_ROOT="/home/evezeyl/Documents/Insync/gdrive/OBSWORK/20_GITS/SPARMVET_VIZ"

# Create a tree of the working directory 
tree_file="${PROJECT_ROOT}/tree.txt"
tree "${PROJECT_ROOT}" > "${tree_file}"

# Function to make paths relative to PROJECT_ROOT
to_relative() {
    [[ -z "$1" ]] && return
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
# --- 📚 AUTHORITY DIRECTORIES (Exhaustive Discovery) ---
rules_dir="${PROJECT_ROOT}/.agents/rules"
workflows_dir="${PROJECT_ROOT}/.agents/workflows"
knowledge_dir="${PROJECT_ROOT}/.antigravity/knowledge"

# Standard Base Files
agent_guide="${PROJECT_ROOT}/AGENT_GUIDE.md"
implementation_plan="${PROJECT_ROOT}/.antigravity/plans/implementation_plan_master.md"
tasks="${PROJECT_ROOT}/.antigravity/tasks/tasks.md"
handoff_active="${PROJECT_ROOT}/.antigravity/logs/handoff_active.md"

# Structural Anchors
manifest_appendix="${PROJECT_ROOT}/docs/appendix/manifest_structure.yaml"

# Key READMEs
app_readme="${PROJECT_ROOT}/app/README.md"
lib_readmes=$(find "${PROJECT_ROOT}/libs" -name "README.md")


DAILY_DATE=$(date +%Y-%m-%d)
TIME_STAMP=$(date +%H%M%S)
OUTPUT_DIR="${PROJECT_ROOT}/EVE_WORK/daily/${DAILY_DATE}"
OUTPUT_FILE="${OUTPUT_DIR}/GEM_CONTEXT_${DAILY_DATE}_${TIME_STAMP}.md"

# Ensure output directory exists (ADR-045 Hygiene)
mkdir -p "${OUTPUT_DIR}"

echo "Generating context for GEM..."

# Building the relative INCLUDE_LIST
# tree_file is mandatory
REL_INCLUDE_LIST="$(to_relative "${tree_file}")"

# Add standard files (filtering for existence)
for p in "${agent_guide}" "${implementation_plan}" "${tasks}" "${handoff_active}" \
         "${manifest_appendix}" \
         "${app_readme}" ${lib_readmes}; do
    if [[ -f "$p" ]]; then
        rel=$(to_relative "$p")
        [[ -n "$rel" ]] && REL_INCLUDE_LIST="${REL_INCLUDE_LIST},${rel}"
    fi
done

# Add exhaustive directory content (Rules, Workflows, Knowledge)
for dir in "${rules_dir}" "${workflows_dir}" "${knowledge_dir}"; do
    # Explicitly exclude dasharch.md persona protocol
    files=$(find "${dir}" -name "*.md" ! -name "dasharch.md")
    for f in ${files}; do
        rel=$(to_relative "$f")
        [[ -n "$rel" ]] && REL_INCLUDE_LIST="${REL_INCLUDE_LIST},${rel}"
    done
done

# Add recent audit logs (last 3 days)
recent_logs=$(find "${PROJECT_ROOT}/.antigravity/logs" -name "audit_*.md" -mtime -3)
for log in ${recent_logs}; do
    rel=$(to_relative "$log")
    [[ -n "$rel" ]] && REL_INCLUDE_LIST="${REL_INCLUDE_LIST},${rel}"
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
