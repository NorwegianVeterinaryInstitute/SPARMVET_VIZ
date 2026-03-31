# Architecture Decision Record: Tiered Data Lifecycle (ADR-024)

**Target Component:** libs/transformer & app/server
**Status:** Planned / Pending Implementation (Phase 3 & Phase 4)

## Context & Problem
The pipeline was suffering from severe memory and processing bottlenecks (e.g., 22-minute render times) during visualization operations. This occurred because the system was attempting to rerun the entire multi-source assembly and wrangling pipeline (Layers 1 and 2) for every single UI interaction or visualization request.

## Decision
We implemented a **Tiered Data Lifecycle** to drastically decouple the heavy relational assembly phase from the lightweight UI exploration phase. 
- **Tier 1 (The Anchor)** represents the heavy, one-time generation of the fully joined dataset, strictly materialized to disk via Parquet. 
- **Tier 2 (The View)** represents the transient, ultra-fast queries run against the Parquet anchor using Predicate Pushdown and Lazy evaluation.

Because this is a fundamental architectural decision, we physically split the codebase logic into `persistence/` (for Tier 1) and `performance/` (for Tier 2) subpackages within the `transformer` library.

## Consequences
- **Memory Safety**: We no longer overflow RAM on large datasets (e.g., 200k+ rows).
- **Speed**: UI interactions and VizFactory renderings shifted from minutes to milliseconds.
- **Complexity**: Developers must now manage disk state (`session_anchor.parquet`) and ensure the "Short-Circuit Rule" correctly detects when to skip Tier 1 rebuilds.

## Execution Directives
For the exact operational rules, workflow, and mandate enforcement associated with this ADR, agents MUST refer to the authoritative rulebook:
👉 `[rules_tiered_data.md](../../.agents/rules/rules_tiered_data.md)`