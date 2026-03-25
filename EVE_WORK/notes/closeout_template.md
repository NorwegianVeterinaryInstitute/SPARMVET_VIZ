## NEW

@Agent: Execute @dasharch Session Closeout Protocol
1. Pre-Flight Consistency Audit (CRITICAL):
- Rule Validation: Verify that all decorators implemented today (split_column, etc.) strictly follow the standards defined in ./.agents/rules/workspace_standard.md 
- Majority Rule Check: Scan libs/transformer/src/data_wrangler.py. If any function diverges from the crystallized pattern, fix it now or log it as a Critical Blocker.
- Halt & Verify: If you find inconsistencies between the DataSchema YAMLs and the Wrangling YAMLs in the ./config/manifests subdirectories, document the mismatch in ./.antigravity/knowledge/blockers.md.

2. General Audit Logic and actualisation of with last 2 days of work: 
- ./.agents/rules/workspace_standard.md
- ./.antigravity/plans/workspace_standards.md
- ./.antigravity/knowledge/architecture_decisions.md
- ./.antigravity/plans/implementation_plan_master.md
- ./.antigravity/tasks/tasks.md
- ./.antigravity/knowledge/blockers.md
- ./.antigravity/knowledge/milestones.md
- ./docs/*.md
- ./.antigravity/logs/audit_{{YYYY-MM-DD}}.md

3. The Baton Pass (Context Injection):
- Generate a 'Resume Prompt' for the next Agent. It must explicitly command:
    - "Assume persona @dasharch."
    - "Read ./agents/rules/workspace_standard.md (Sections 8 & 9) FIRST to understand the Double Confirmation and Majority Rule protocols."
    - "Read ./.antigravity/knowledge/architecture_decisions.md to align with the Sequential Staging logic."
    - "Report any architectural divergence immediately."

4. Final Mirror: Confirm all files are saved to the local workspace and provide a one-line summary of the "Current State of Truth."

@Agent: Execute @dasharch Session Closeout Protocol update
- add user request to reverify (user manually reopened task for testing decorator  'split_column') to - ./.antigravity/logs/audit_{{YYYY-MM-DD}}.md 
- and add to the Baton Pass prompt for the next agent to reinitiate testing for decorator 'split_column' 

## OLD

@Agent: Execute @dasharch Session Closeout Protocol
1. **Sync State:** Update ./.antigravity/tasks/tasks.md, ./.antigravity/plans/implementation_plan_master.md with yesterdays and todays progress. and ./.antigravity/knowledge/blockers.md  with any new technical hurdles found 
2. **Audit Logic:** 
- Ensure the './.antigravity/knowledge/architecture_decisions.md' reflects our current implementation plan and ./.antigravity/knowledge/milestones.md are actualized. 
<!-- - Check for consistency between our active YAML manifests in ./config/manifests/pipelines/ and any new Python decorators implemented in the transformer/viz layers. -->
3. **Cold Memory:** Append a technical summary to ./.antigravity/logs/audit_{{YYYY-MM-DD}}.md including:
   - Specific files modified.
   - New architectural decisions made (e.g., Polars LazyFrame handling).
   - Any 'In-Flight' logic that isn't yet committed.
   - If ambiguous, keep the most recent decision and note it in the log.
4. **The Baton Pass:** Generate a 'Resume Prompt' that must tell the next Agent exactly which file to read first to achieve 100% context parity AND that specifically instructs the next Agent to:
   - "Assume persona @dasharch."
   - "Read ./.antigravity/knowledge/architecture_decisions.md to align with our Plotnine/Polars standards."
   - "Read ./.antigravity/knowledge/blockers.md to avoid known pitfalls."
   - "Execute the next task in ./.antigravity/tasks/tasks.md."
   - "Read rules and standards in ./.agents/rules/workspace_standard.md." and in ./agents/workflows/verification_protocol.md"
   - "Report any inconsistencies / logical / architectural / documentation / implementation issues found in the files read" 
5. **Final Mirror:** Confirm all these updates are written to the local workspace and ready to be committed for Git versioning.
   