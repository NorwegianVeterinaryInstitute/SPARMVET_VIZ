#!/bin/bash

# Creating context files with repomix
# https://github.com/yamadashy/repomix
# bash /home/evezeyl/Documents/Insync/gdrive/OBSWORK/20_GITS/distrobox/scripts/SPARMVET_VIZ_GEM_context.sh



PROJECT_ROOT="/home/evezeyl/Documents/Insync/gdrive/OBSWORK/20_GITS/SPARMVET_VIZ"

cd "${PROJECT_ROOT}"

# Create a tree of the working directory 
tree_file="tree.txt"
tree  > "${tree_file}"


# Define paths to context files - right now 8 files
## The antigravity GEM initial context uploaded already - only change when needed
## Most important files first RULES 
workspace_standard="${PROJECT_ROOT}/.agents/rules/workspace_standard.md"
rules_aesthetic="${PROJECT_ROOT}/.agents/rules/rules_aesthetic.md"
rules_behavior="${PROJECT_ROOT}/.agents/rules/rules_behavior.md"
rules_runtime="${PROJECT_ROOT}/.agents/rules/rules_runtime.md"
rules_wrangling="${PROJECT_ROOT}/.agents/rules/rules_wrangling.md"

## Architecture & Knowledge and decisions

architecture_decisions="${PROJECT_ROOT}/.antigravity/knowledge/architecture_decisions.md"
project_conventions="${PROJECT_ROOT}/.antigravity/knowledge/project_conventions.md"
protocol_tiered_data="${PROJECT_ROOT}/.antigravity/knowledge/protocol_tiered_data.md"

# rules for testing
verification_protocol="${PROJECT_ROOT}/.agents/workflows/verification_protocol.md"

# Automation implementation viz_factory 
viz_factory_implementation="${PROJECT_ROOT}/.agents/workflows/viz_factory_implementation.md"

# Status files
implementation_plan="${PROJECT_ROOT}/.antigravity/plans/implementation_plan_master.md"
blockers="${PROJECT_ROOT}/.antigravity/knowledge/blockers.md"
milestones="${PROJECT_ROOT}/.antigravity/plans/milestones.md"
tasks="${PROJECT_ROOT}/.antigravity/tasks/tasks.md"

# Logs : are in "${PROJECT_ROOT}/.antigravity/logs/" but we do not add those

# Use distrobox to run repomix and create a unique context file from all the files listed above 

DATE=$(date +%Y%m%d_%H%M%S)
OUTPUT_FILE="${PROJECT_ROOT}/EVE_WORK/GEM_CONTEXT_${DATE}.md"

# Ensure output directory exists
mkdir -p "${PROJECT_ROOT}/EVE_WORK"

echo "Generating context for GEM..."

# Concatenate files in list In order of importance - hum it seems not to respect the order
INCLUDE_LIST="${tree_file},${workspace_standard},${rules_aesthetic},${rules_behavior},${rules_runtime},${rules_wrangling},${architecture_decisions},${project_conventions},${protocol_tiered_data},${verification_protocol},${implementation_plan},${blockers},${milestones},${tasks}"

distrobox enter repomix-env --name repomix-env --no-tty -- \
  repomix --style markdown \
  --parsable-style \
  --no-file-summary \
  --no-directory-structure \
  --include "${INCLUDE_LIST}" \
  --output "${OUTPUT_FILE}"

echo "Context file generated at: ${OUTPUT_FILE}"
echo "Please find the remaining of the updated context for your sync process (one file aggregated file)"



