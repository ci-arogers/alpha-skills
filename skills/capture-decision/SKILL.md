---
name: capture-decision
description: Guided structured decision capture. Walks through situation, options considered, choice made, and rationale. Stores to FreeContext. Use when a significant architectural, product, or strategic decision has been made.
arguments: topic?
allowed-tools: mcp__freecontext__capture_decision
---

# Capture Decision

{{topic}}

---

Walk through the decision structure. Answer each field — don't skip any.

**Situation:** What triggered or required this decision? What was the context?

**Options considered:** What alternatives existed? List at least 2, even if one was clearly wrong.

**Choice:** What was chosen?

**Rationale:** Why this option? Be specific about what made the alternatives worse.

**Outcome (optional):** What happened as a result, if already known?

---

Once you've answered the above, I will call `mcp__freecontext__capture_decision` with:
- `situation` — from your answer
- `choice` — from your answer
- `rationale` — from your answer
- `options_considered` — from your answer
- `outcome` — if provided
- `domain` — inferred from context (technical / business / architecture / personal)
- `importance` — 1 (notable) or 2 (significant), I will judge based on scope

Confirm before storing, or say "just store it."
