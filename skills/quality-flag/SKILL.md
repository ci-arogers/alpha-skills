---
name: quality-flag
description: Flag the current session as feeling off — agent seems less personalized, missing context, wrong tone, or just different. Captures session quality signal with context and queues it for R4 curation review. As simple as thumbs down. Use mid-conversation when something feels wrong.
arguments: note?
allowed-tools: mcp__freecontext__capture_observation, mcp__freecontext__get_memory_context, Bash
---

# Quality Flag

Something feels off in this session. Capturing the signal now.

{{note}}

---

## What I'll do

**Step 1 — Capture the signal**

Call `mcp__freecontext__capture_observation` with:
- `content`: A structured quality flag entry:

```
[QUALITY FLAG] {{note or "session quality degraded — user flagged"}}

Session context:
- Timestamp: [current time]
- Recent queries: [last 2-3 get_memory_context queries from this session if known]
- Note from user: {{note}}
- Flag type: [infer from note: missing-context / wrong-tone / less-personalized / repeating / other]

Queue for R4 curation review.
```

- `node_type`: observation
- `importance`: 2

**Step 2 — Quick self-check**

Run a retrieval smoke test via the health dashboard if reachable:

```bash
curl -s http://localhost:8420/api/health/smoke | python3 -m json.tool 2>/dev/null | grep -E "passed|latency|type_diversity" | head -10
```

Report the smoke test result inline — green means the issue is likely in the vault content (curation needed), not the retrieval engine itself.

**Step 3 — Surface recent curation history**

Check if a curation run happened recently that might explain the drift:

```bash
python3 -c "
import json
from pathlib import Path
log = Path('C:/Users/arogers/dev/proj-freecontext/freecontext/data/audit_log.jsonl')
if log.exists():
    runs = []
    with open(log) as f:
        for line in f:
            if line.strip():
                e = json.loads(line)
                runs.append({'run_id': e.get('run_id'), 'ts': e.get('ts'), 'applied': e.get('applied', 0)})
    runs.sort(key=lambda x: x.get('ts', 0), reverse=True)
    for r in runs[:3]:
        import time
        days_ago = round((time.time() - r['ts']) / 86400, 1)
        print(f'  {r[\"run_id\"]} — {r[\"applied\"]} changes — {days_ago}d ago')
else:
    print('No audit log found')
" 2>/dev/null
```

**Step 4 — Report back**

Tell Austin:
1. The flag was captured and is queued for R4 review
2. Smoke test result (green/yellow/red)
3. Most recent curation run and when it happened
4. Whether the drift is likely retrieval-level (smoke test bad) or vault-quality-level (curation needed)
5. The restore path if needed: `python restore.py --list` to see available snapshots

---

## What happens next

In the current setup: the quality flag is stored as a `[QUALITY FLAG]` observation in FreeContext. The next curation session should surface it and R4 can review the context.

In Tessera: K2SO sees the `[QUALITY FLAG]` observation appear in the vault, notifies R4, R4 runs a targeted curation pass against the fragments that were most recently retrieved in that session.

The flag is permanent until resolved — it won't be auto-deleted by cleanup or compaction.
