# Blockers & Technical Debt (SPARMVET_VIZ)
# Last Updated: 2026-03-21 by @dasharch

## 🧱 Blocker: Data Orchestration - Lazy vs. Eager
**Category:** Implementation Logic
**Priority:** HIGH
**Context:** We use **Polars** as our core engine. Polars operates on **LazyFrames** to optimize query plans, but visualization libraries (Plotnine) require in-memory DataFrames.
**The Undecided Logic:** 
- Should the **Orchestrator** (Server) call `.collect()` when a user triggers a reactive filter?
- Or should the **Viz Factory** be responsible for collecting the LazyFrame before conversion to Pandas?
**Trade-offs:** 
- *Orchestrator Collect*: Faster if multiple plots share the same filtered view. Reduces memory churn.
- *Factory Collect*: Encapsulates the implementation details. 
**Current Status:** Undecided. Pending prototype of Polars-to-Plotnine data handoff.

## 🧱 Blocker: Outdated Directory Confusion
**Category:** Project Structure
**Priority:** MEDIUM
**Context:** `./config/manifests/` contains legacy folders (`species`, `templates`) that follow an older, non-modular architecture.
**Status:** PENDING cleanup.
