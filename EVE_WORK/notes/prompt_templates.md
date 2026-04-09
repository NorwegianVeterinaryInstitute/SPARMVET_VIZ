### A. The Alignment Prompt (System Reset)

- Use this template to re-seat the IDE Agent when it drifts:

```text
"@Agent: @dasharch - SYSTEM RESET.

Read: 
- workspace standard: ./.agents/rules/workspace_standard.md,
- architecture decisions: ./.antigravity/knowledge/architecture_decisions.md and
- implementation plan: ./.antigravity/plans/implementation_plan_master.md

For any subsequent tasks and prompt, read files that are 
relevant to your tasks execution (as defined in the workspace standard) in 
- ./.agents/rules/
- ./.antigravity/workflows/
- ./.antigravity/plans/
- ./.antigravity/knowledge/
- ./.antigravity/tasks/
- and all the current documentation in ./docs

Current Priority: [Task from ./.antigravity/tasks/tasks.md]. 

Follow Verification Protocol: Generate Contract -> HALT for @verify."

```

### B. The log promt

```text
@Agent: @dasharch - LOG INFORMATION.

Create if not existing, verify and update the log of the todays session
in ./.antigravity/logs/audit_{{YYYY-MM-DD}}.md
Never delete or modify previous information in the log, only append new information.

Update libs/{library_name}/README.md with any new relevant information.

Update User documentation in ./docs with any new relevant information.

Update Project conventions ./antigravity/knowledge/project_conventions.md
with the necessary information.

Update Completed tasks in ./.antigravity/tasks/tasks.md.
```

### C. Consistency Check Prompt

```text
"@Agent: @dasharch - CONSISTENCY CHECK.

Review the current state of the project and identify any inconsistencies, technical debt, or potential pitfalls.
Review the following files for potential inconsistencies:
- ./.agents/rules/
- ./.antigravity/workflows/
- ./.antigravity/plans/
- ./.antigravity/knowledge/
- ./.antigravity/tasks/
- ./docs
```
