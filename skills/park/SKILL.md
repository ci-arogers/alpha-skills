---
name: park
description: Explicitly park a tangent or idea that came up mid-session. Captures it to FreeContext as an intention so it's not lost, then returns focus to the beam.
arguments: idea?
allowed-tools: mcp__freecontext__capture_observation, mcp__freecontext__log_exchange
---

# Park This

{{idea}}

---

Parking the above. Capturing to FreeContext as an intention so it doesn't get lost.

I will call `mcp__freecontext__capture_observation` with:
- `content`: Summary of the parked idea + enough context to pick it up next session
- `node_type`: "intention"
- `importance`: 1

Then returning focus to the active beam.

**Parked.** We can come back to this — it won't be forgotten. Back to the beam.
