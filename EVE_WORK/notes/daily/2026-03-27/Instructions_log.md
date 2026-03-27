# 2026-03-26


**Action Audit: 'split_column'** 

- [ ] test one by one the new decorators
- [ ] update documentation (new decorators, architectural decisions)

## Testing 

## List of genes to extract from virulence finder 

- [ ] restart here : checking the abscence of wrangling and correct work of the process 
```bash
./.venv/bin/python ./libs/transformer/tests/test_wrangler.py \
  --data ./assets/ref_data/Virulence_genes_APEC/Virulence_genes_APEC.tsv \
  --manifest ./assets/ref_data/Virulence_genes_APEC/Virulence_genes_APEC_manifest.yaml \
  --output tmp/EVE_TEST.tsv
```

Now we will need to run the command : 
./.venv/bin/python ./libs/transformer/tests/test_wrangler.py \
  --data ./assets/ref_data/Virulence_genes_APEC/Virulence_genes_APEC.tsv \
  --manifest ./assets/ref_data/Virulence_genes_APEC/Virulence_genes_APEC_manifest.yaml \
  --output tmp/EVE_TEST.tsv

 But this data set has a particularity, it should just be imported as is. So only the input_fields should be populated. The script  test_wrangler.py should be adapted such as the ability to take into for empty wrangling and output_fields or (wrangling: [ ], output_fields: [ ]) or ommited wranlging and output fields, in which case the output should be the same as input data. 

## Initiation

@Agent: @dasharch - SYSTEM INITIALIZATION 
1. Mandatory Context Injection (Read First):
- ./.agents/rules/workspace_standard.md (The Law)
- ./.antigravity/knowledge/architecture_decisions.md (The History)
-  ./.agents/workflows/verification_protocol.md (procedure)

2. Environment Lock ( NON-NEGOTIABLE):
- You MUST use the root `./.venv/bin/python`. 
- Verify now: Run `which python` and `python -c "import sys; print(sys.prefix)"`. 
- If it is NOT the project .venv, STOP and report the error.

3. Execution Protocol (Rule 11 & ADR-013):
- Manifests now use: input_fields -> wrangling -> output_fields.
- Do NOT execute tasks autonomously. The user will prompt for specific tasks
- Every task must end with a HALT and a request for @verify.

Confirm your environment is locked to ./.venv and you are ready for Phase 3 manual verification support. @verify

--- 
@Agent: Assume persona @dasharch.
Welcome back. Before generating any code or executing steps, you MUST fulfill the following contextual handoff requirements:
**Read `./EVE_WORK/notes/daily/2026-03-27/Instructions_log.md`** This is the log from yesterday. W we will continue where we left off.

---



