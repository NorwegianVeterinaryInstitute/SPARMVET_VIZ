# Agent realignment examples 


## SYTEM RESET  - IF during VIZ_FACTORY IMPLEMENTATION 

@Agent: @dasharch - SYSTEM RESET.

Read: 
- ./.agents/rules/workspace_standard.md (Master Authority)
- ./.antigravity/knowledge/architecture_decisions.md (Technical Bible)
- ./.antigravity/plans/implementation_plan_master.md (Roadmap)
- ./.antigravity/workflows/viz_factory_implementation.md (testing plotocol for implementation)

Current Priority: [Task from ./.antigravity/tasks/tasks.md]. 

Constraint Check: 
- Polars LazyFrames ONLY.
- Decorator-Based Registry ONLY.
- Follow Verification Protocol: Generate Contract (TSV/YAML) -> CLI Execute -> HALT for @verify evidence check in tmp/.

##  RULE RESYNC 

@Agent: @dasharch - CRITICAL RULE RE-SYNC.

1. **Reload Context:** Immediately re-read ./agents/rules/workspace_standard.md and ./.antigravity/knowledge/architecture_decisions.md, and ./.antigravity/knowledge/project_conventions.md.
2. **State Sync:** Update your internal logic to match the latest versions of these files.
3. **Validation:** If my current request contradicts these updated rules, invoke the Logic Conflict Guardrail and ask for clarification before proceeding.



##  OTHER 
- OLD RULES FORMALIZED
- WORKFLOWS : perfect for repetitive tasks - ensure that the rules are respected and followed

