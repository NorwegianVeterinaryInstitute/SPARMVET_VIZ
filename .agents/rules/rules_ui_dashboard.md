---
trigger: always_on
---

## 1. UI Orchestration & Aesthetics (ADR-027–030)

- **Library Sovereignty:** UI MUST NOT duplicate logic; it MUST call libraries in `./libs/`.
- **Dynamic discovery:** Tabs and column filters MUST be derived from manifests and Polars schemas at runtime, not hardcoded.
- **Recipe Inheritance:** Tier 3 Sidebar MUST pre-fill with Tier 2 logic nodes as editable components.
- **Aesthetic Lock:** Sidebars use **#f8f9fa**. Tooltips use Light Yellow/Green.
- **Panel Contrast:** Side panels (Left/Right) MUST use **#f8f9fa** to create a visual "recess" from the bright white Central Theater.
- **WrangleStudio Tooltips:** Help popups for action syntax must use a "Soft Note" aesthetic: **#fff9c4** (Light Yellow) for warnings/logic or **#e8f5e9** (Light Green) for success/usage examples.
- **Typography:** Titles must use standard Sans-Serif (Standard Dashboard font). Do not apply 'Deep Violet' branding to UI headers.
- **State Feedback:** When a plot is "In-Calculation" (re-running Tier 1 to 3), the UI must use a dimming overlay rather than a blank screen. A "recalculating" message should be visible.
