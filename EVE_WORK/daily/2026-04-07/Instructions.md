# Instructions and work log

date:: 2026-04-07

- [ ] Review all rules for AI context (first pass). In .agents/rules/
  - [x] rules_documentation_standards.md
  - [x] rules_aesthetic.md -
  - [x] rules_behavior.md
  - [x] rules_runtime.md
  - [x] rules_tiered_data.md
  - [x] rules_wrangling.md
  - [x] workspace_standard.md
- [ ] in .agents/workflows/
  - [ ] implementation_workflow_transformer.md
  - [ ] verification_protocol.md
  - [ ] viz_factory_implementation.md
- [ ] in .antigravity/knowledge/
  - [ ] architecture_decisions.md
  - [ ] blockers.md
  - [ ] milestones.md  
  - [ ] project_conventions.md
  - [ ] protocol_tiered_data.md
- [ ] in .antigravity/plans/
  - [ ] implementation_plan_master.md
- [ ] in .antigravity/tasks/
  - [ ] tasks.md

AI TO DO :
Hi, I attached your !sync file for the context (one large file that concatenates the main context and some other files we will need to review). Please read this context thoroughly.

We need to inspect the context and rules files and propose a new version of the rules files.

1 Do not remove rules unless agreed with me.
2 When we agree at the end of our conversation, and solely then, you will need to prepare a prompt for the antigravity integrated AI with the detail instructions so it can do the necessary changes we agreed upon, using the gemini 3 Flash model. This means you will need to detail all the steps and provide clear instruction of what needs to be changed. I will indicate that all has been reviewed and agreed via @generate_prompt.
3 **Important: All rules and workflow files are limited to 12,000 characters each, Therefore it is important to adopt a correct structure and split the files in logical parts**.

Here are some points I noted for review, but they are not exhaustive (so you will need to review all the and suggest better organization):

A. rules_aesthetic.md and rules_documentation_standards.md : redundancy shoult it be merged  in one single document ? Eventual inconsistencies must be found and resolved.
B. we need to ensure homogeneity in development rules : for the tests scripts eg. naming -> extract rule from the code structure (eg `tests/{lib}_integrity_suite.py`  might need to be renamed to current debug (see tree), we need also to ensure that it is writen in the rules that we an individual test script eg. per decorator / function and then a global wrapper to test the whole library (there are some parts already in the files). But we need to ensure consistency when continuing development.
C. It is important that a rule is given to ensure that all python scripts use argparse, because it needs to be possible for the user to use via command line. Wrappers scripts must adapt to this, running all individual tests via argparse.
D. rules_behavior.md : violet law ? shoult it only appear in the docs ? or should it refered to when necessary (avoid redundancy when not necessary)
E. tiered data protocol : note that a plot might reuse the same basic wrangling, so tier data might need to be stopped at a certain level, which will allow bifurcating the data transformation for different plots. We will need a solution after for update of the tier data2 from user (but need to be at a later stage)
F. should the rules_tiered_data.md merged or at least be mentionned in rules_wrangling.md ? should the context .antigravity/knowledge/protocol_tiered_data.md be mentionned or partially merged with rules_tiered_data.md ... and rules_wrangling.md ... ?
G. we need to create rules for the development of helper scripts for the user, in order consistency and their usage and purpose must also be documented. Scripts to assist uers are in .assets/scripts and I added those scripts to the context file.
H. At the end,  you will need to review the antigravity agent definition (.agents/rules/dasharch.md), and propose improvements of its definition so it can better assist the user in its tasks.
I. When this is settled , .agents/rules/workspace_standard.md will need to be updated, to ensure that the agent has to review the appropriate context files and rules ... as this is the main entry point for the agent (the file that explain what the agent must read and ingest before starting to work)
