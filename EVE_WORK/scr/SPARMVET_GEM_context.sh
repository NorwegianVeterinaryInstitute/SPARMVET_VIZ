#!/bin/bash

# Creating context files with repomix
# https://github.com/yamadashy/repomix
# bash /home/evezeyl/Documents/Insync/gdrive/OBSWORK/20_GITS/distrobox/scripts/SPARMVET_VIZ_GEM_context.sh



PROJECT_ROOT="/home/evezeyl/Documents/Insync/gdrive/OBSWORK/20_GITS/SPARMVET_VIZ"

cd "${PROJECT_ROOT}"

# Create a tree of the working directory 
tree_file="tree.txt"
tree  > "${tree_file}"

# REVIEW  case by case : Extra : integration : can be modular 
# extra="${PROJECT_ROOT}/assets/scripts/*.py"
extra=""

# antigravity agent definition 
agent_definition="${PROJECT_ROOT}/.agents/rules/dasharch.md"

# Define paths to context files - right now 8 files
## The antigravity GEM initial context uploaded already - only change when needed
# .agents/rules/
workspace_standard="${PROJECT_ROOT}/.agents/rules/workspace_standard.md"
#rules_aesthetic="${PROJECT_ROOT}/.agents/rules/rules_aesthetic.md"
rules_asset_scripts="${PROJECT_ROOT}/.agents/rules/rules_asset_scripts.md"
rules_behavior="${PROJECT_ROOT}/.agents/rules/rules_behavior.md"
rules_data_engine="${PROJECT_ROOT}/.agents/rules/rules_data_engine.md"
rules_documentation_aesthetics="${PROJECT_ROOT}/.agents/rules/rules_documentation_aesthetics.md"
#rules_documentation_standards="${PROJECT_ROOT}/.agents/rules/rules_documentation_standards.md"
rules_runtime_environment="${PROJECT_ROOT}/.agents/rules/rules_runtime_environment.md"
#rules_runtime=
rules_tiered_data="${PROJECT_ROOT}/.agents/rules/rules_tiered_data.md"
rules_verification_testing="${PROJECT_ROOT}/.agents/rules/rules_verification_testing.md"
rules_wrangling="${PROJECT_ROOT}/.agents/rules/rules_wrangling.md"

# .agents/workflows
implementation_workflow_transformer="${PROJECT_ROOT}/.agents/workflows/implementation_workflow_transformer.md"
verification_protocol="${PROJECT_ROOT}/.agents/workflows/verification_protocol.md"
viz_factory_implementation="${PROJECT_ROOT}/.agents/workflows/viz_factory_implementation.md"

# .antigravity/knowledge/
## Knowledge: Architecture & Knowledge and decisions
architecture_decisions="${PROJECT_ROOT}/.antigravity/knowledge/architecture_decisions.md"
project_conventions="${PROJECT_ROOT}/.antigravity/knowledge/project_conventions.md"
protocol_tiered_data="${PROJECT_ROOT}/.antigravity/knowledge/protocol_tiered_data.md"

##  Status 
milestones="${PROJECT_ROOT}/.antigravity/knowledge/milestones.md"
blockers="${PROJECT_ROOT}/.antigravity/knowledge/blockers.md"

# .antigravity/plans : implementation plan 
implementation_plan="${PROJECT_ROOT}/.antigravity/plans/implementation_plan_master.md"

# .antigravity/tasks
tasks="${PROJECT_ROOT}/.antigravity/tasks/tasks.md"

# Logs : are in "${PROJECT_ROOT}/.antigravity/logs/" but we do not add those


# Use distrobox to run repomix and create a unique context file from all the files listed above 

DATE=$(date +%Y%m%d_%H%M%S)
OUTPUT_FILE="${PROJECT_ROOT}/EVE_WORK/GEM_CONTEXT_${DATE}.md"

# Ensure output directory exists
mkdir -p "${PROJECT_ROOT}/EVE_WORK"

echo "Generating context for GEM..."


# Concatenate files in list In order of importance - hum it seems not to respect the order
# eg INCLUDE_LIST="${tree_file},${workspace_standard},${rules_aesthetic},${rules_behavior},${rules_runtime},${rules_wrangling},${architecture_decisions},${project_conventions},${protocol_tiered_data},${verification_protocol},${implementation_plan},${blockers},${milestones},${tasks}"
INCLUDE_LIST="${tree_file},\
${workspace_standard},${rules_aesthetic},${rules_behavior},${rules_documentation_standards},\
${rules_runtime},${rules_tiered_data},${rules_wrangling},\
${implementation_workflow_transformer},${verification_protocol},${viz_factory_implementation},\
${architecture_decisions},${project_conventions},${protocol_tiered_data},\
${milestones},${blockers},${implementation_plan},${tasks}"



# If extra files not empty they need to be added to the INCLUDE_LIST 
# This needs to be flexibile 
add_extra=""
if [ -n "$extra" ]; then
    # The loop is now flexible to any pattern defined in the 'extra' variable
    for item in $extra; do
        if [ -d "$item" ]; then
            # If a directory matches, find all files within it
            files=$(find "$item" -maxdepth 1 -type f | paste -sd "," -)
            [ -n "$files" ] && add_extra="${add_extra}${add_extra:+,}${files}"
        elif [ -e "$item" ]; then
            # If a file (or anything else) matches, add it directly
            # This respects the pattern (e.g. *.py, *.sh) defined in $extra
            add_extra="${add_extra}${add_extra:+,}${item}"
        fi
    done
fi

# adding to the list
if [ -n "$add_extra" ]; then
    INCLUDE_LIST="${INCLUDE_LIST},${add_extra}"
fi



distrobox enter repomix-env --name repomix-env --no-tty -- \
  repomix --style markdown \
  --parsable-style \
  --no-file-summary \
  --no-directory-structure \
  --include "${INCLUDE_LIST}" \
  --output "${OUTPUT_FILE}"

echo "Context file generated at: ${OUTPUT_FILE}"
echo "Please find the remaining of the updated context for your sync process (one file aggregated file)"



