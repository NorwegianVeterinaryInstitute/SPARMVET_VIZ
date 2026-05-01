---
name: Pipeline persona architecture principle
description: pipeline-static and pipeline-exploration-simple are always production-mode personas — testing uses more capable personas, not a testing_mode flag on the pipeline personas themselves
type: project
---

pipeline-static and pipeline-exploration-simple are always production-facing personas. Data arrives via pipeline channels (Galaxy history, Nextflow outputs, etc.) — the dashboard does not control how data is passed, only how it is displayed and processed.

**Why:** Testing a pipeline integration is done by switching to a more capable persona (developer or pipeline-exploration-advanced, both with testing_mode=true and active data selectors). Pipeline personas never need testing_mode=true because testing adds functionality — it doesn't reduce it.

**How to apply:** testing_mode=false is hardcoded for pipeline personas in their template YAMLs. Data Import panel for these personas is SHOW(RO) only — display the configured/injected path, no file selector. Never add a testing_mode toggle to the pipeline persona UI.
