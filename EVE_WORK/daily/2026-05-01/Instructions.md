On "effort" (extended thinking):

In Claude.ai, the effort slider controls how much reasoning time the model uses before answering — roughly: low = fast/cheap, high = deeper planning.

| Phase 25 step | Recommended | Effort level | Why |
|---|---|---|---|
| 25-A/B/C | Sonnet | Low/off | Mechanical: YAML edits, flag gates, renames |
| 25-D/E | Sonnet | Low/off | Well-defined structural changes |
| 25-F | Opus | High | New reactive component with conditional logic (testing_mode branching) — benefits from planning before writing |
| 25-G | Opus | High | Quarto subprocess integration is new territory, session zip handler needs careful wiring |
| 25-H | Opus | Medium | Smaller scope than 25-F/G but still new |
| 25-I/J | Sonnet | Low/off | CSS tweaks + test additions |

Short answer: Sonnet with no extended thinking for 25-A through 25-E; Opus with high effort for 25-F and 25-G specifically. Those are the two steps where the model needs to think through conditional rendering paths and subprocess calls before touching code.

Want me to clean up tasks.md first, or run the Phase 25 pre-flight and start 25-A?