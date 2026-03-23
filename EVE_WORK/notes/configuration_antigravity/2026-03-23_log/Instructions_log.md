# 2026-03-23 - Restarting development 

> Agent : "Recovery Toolkit Initialization and Consistency check" 

## closing -> as write log, update and put ready new chat for continuing

- See closeout_template.md (only some part to eventually update)



## 2. Step by step building and user control 
- implemented workflow rule for one step at the time
- instructions that dasharch must respect the user testing protocol 


@Agent: @dasharch - Execute Step: Decorator & Wrangler Verification.
1. **Persona & Workflow Sync:** Confirm you are following the './agents/workflows/verification_protocol.md' and the updated './agents/rules/dasharch.md'.
2. **Infrastructure Audit:** 
   - Verify the current implementation stage of current registered actions (register_action decorators) and implement testing of the transformer layer (as this has not been done yet).
3. **Test Update:** - Open and if necessary update `./libs/transformer/tests/test_wrangler.py`.
   - Configure it to load the minimal fake dataset from `./assets/` using Polars. and the specific decorator actions testing
4. **Proceed with test - One decorator at a time:**
   - TRIGGER CONTRACT HALT: Generate the test CSV and YAML manifest in ./libs/transformer/tests/data/ as per the protocol.
   - For each test print `df.glimpse()` to the terminal.
   - STOP: Wait for my @confirm_contract before running the moving to next decorator and the final user test (last step).


## 1. restarting - new chat - avoiding long context
@Agent: Assume persona @dasharch.
1. Read the Recovery Toolkit in ./.antigravity/ (specifically tasks.md and implementation_plan_v2.md).
2. Perform a Consistency Check between the YAML manifests in ./config/manifests/pipelines/ and the code in ./transformer/ and ./libs/viz_factory/.
3. Verify that the Decorator Registry is ready for the first implementation: drop_duplicates and summarize.
4. Initialize libs/transformer/src/actions/core/duplicates.py and summarize.py.
5. Begin the refactor of libs/viz_factory/src/base.py to use a @register_plot decorator, mirroring the success of the Transformer registry.




 