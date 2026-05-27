---
name: frontend-design
description: Apply the 4-step frontend design framework before writing any UI code. Establishes aesthetic direction, color system, typography, and component inventory. Use before building any dashboard, panel, form, or page — especially dark-theme ops tools.
allowed-tools: Read, Glob, Grep
---

# Frontend Design Framework

You are applying a disciplined design framework before writing any UI code. Do not skip steps. Do not start coding until all four steps are complete and acknowledged.

## Step 1 — Aesthetic Direction

Establish the design voice before anything visual. Answer these questions based on the context:

- **Who uses this?** (operator, developer, end-user, admin)
- **What is the emotional register?** (confident/dense, approachable/light, utilitarian/terminal, polished/consumer)
- **What are three reference products this should feel like?** Name them and articulate what specifically to borrow.
- **What must it NOT feel like?** Name the anti-patterns explicitly.

Do not proceed until aesthetic direction is stated and agreed.

## Step 2 — Color System

Define a complete color palette. Every color must have a semantic role — no decorative colors without purpose.

Required roles:
- `bg-primary` — page background
- `bg-secondary` — header, sidebar, nav
- `bg-card` — panel/card backgrounds
- `bg-hover` — interactive hover state
- `border` — default dividers
- `border-active` — focused/selected state
- `text-primary` — main content
- `text-secondary` — labels, descriptions
- `text-muted` — timestamps, hints
- `status-green` — healthy/success
- `status-yellow` — warning/degraded
- `status-red` — critical/error
- `status-grey` — unknown/inactive

For data visualization: define a named palette of 6–8 colors for charts, type distributions, category breakdowns.

State all values as CSS custom properties. Do not use Tailwind color names as the source — derive meaning first, map to values second.

## Step 3 — Typography

Define the complete type system. Every rule must be stated before code.

Required:
- **Body font** + **mono font** — name them, don't assume
- **Metric values** — always mono, never sans
- **Labels** — always sans, never mono
- Scale: define hero (big numbers), heading (panel titles), body, mono, muted — with size and weight
- **Anti-patterns to enforce**: no decorative font weights, no centered body text, no mixing units within a scale

## Step 4 — Component Inventory

Before writing a single component, list every component the feature requires. For each:

- Name
- Purpose (one sentence)
- Props/inputs it accepts
- Which status colors it uses
- Which typography level it uses

Group by: display components (pure render), container components (fetch + render), action components (buttons, forms).

---

## Output Format

Present each step as a section. After Step 4, output:

```
DESIGN PHASE COMPLETE
Aesthetic: [one sentence]
Colors: [count] defined
Typography: [scale name]
Components: [count] inventoried
Ready to build: [component list]
```

Only after this output should any code be written.
