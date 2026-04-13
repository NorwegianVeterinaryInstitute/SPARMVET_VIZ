# Instructions 2026-04-13

# Nr1

Hi, here is your context for sync.

We will need an agent prompt for a new chat (the agent can have access to all the files in the project - some directories need request but has the same context files as you do):

1. Initialization

2. We need a ui testing workflow : .agent/workflows/ui_manifest_integration_testing.md

3. A. It needs to include the testing of the whole manifest (that the manifest is defined correctly and is complete - and that all libraries that use the manifest - and that the ui depend upon - are producing the expected output)

- structure of the manifest (maybe we need to write a document for the structure of yaml manifests. Example to use for this is `assets/template_manifests/*`) there is a main yaml and several files that are included in the main yaml (those included files are deposited a directory with the same basename as the main yaml and at the same level as the main yaml)
- The manifest must be completely tested and used for:
- transformer library (wrangling, assembly, production of data tiers) using the manifest
- viz factory (production of plot objects) using the manifest. Verififcation of the plot object is required (halt for verify if necessary)
- same procedure for other layers, if they are dependent on the correct specification of manifest (#REVIEW : should we add more libraries to the automatic testing?)

- audit in `tmp/Manifest_test/{manifest_basename}/*` - Then it must verify session_anchor.parquet exists and matches output_fields; that the `USER_debug_{plot_id}.png` is high-resolution and matches the mapping, and present the `.glimpse()` of the data and the rendered PNG to the user. This can include a halt for verify if the agent is not sure about the output or cannot automatically test the success of the test.

2.B When the tests in A are successfull, and ONLY then the ui testing can procede.

- The previous agent in antigravity started autonomous development and ui testing (not horrible because actually advanced a lot on debugging ui - but it needs to respect the rules, development plan and testing procedures). Some task were marked as done but are not completely finished (gallery not completed, different persona modes testing in ui not completed). We must ensure that the agent respects the rules, development plan and testing procedures.
