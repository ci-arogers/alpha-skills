---
name: health-check
description: Run a FreeContext health check. Pulls vault stats, episode log status, activity metrics, and surfaces any signals worth acting on. Use at session start or when retrieval feels off.
allowed-tools: Bash, mcp__freecontext__memory_status, mcp__freecontext__reflect
---

# FreeContext Health Check

Run a health check on the FreeContext memory vault. Execute the following steps in order.

## 1. Memory Status

Call `mcp__freecontext__memory_status` to get fragment count, connection status, and model readiness.

## 2. Dashboard Check

If the health dashboard is running at `http://localhost:8420`, fetch `GET /api/health/summary` and report the JSON result.

If the dashboard is not running, run these SQL checks directly via Bash against `C:/Users/arogers/dev/proj-freecontext/freecontext/data/freecontext.db`:

```bash
# Fragment count and type distribution
sqlite3 "C:/Users/arogers/dev/proj-freecontext/freecontext/data/freecontext.db" \
  "SELECT node_type, COUNT(*) as c FROM fragments GROUP BY node_type ORDER BY c DESC"

# Embedding gap
sqlite3 "C:/Users/arogers/dev/proj-freecontext/freecontext/data/freecontext.db" \
  "SELECT COUNT(*) as null_embeddings FROM fragments WHERE embedding IS NULL"

# Recent captures (last 7 days)
sqlite3 "C:/Users/arogers/dev/proj-freecontext/freecontext/data/freecontext.db" \
  "SELECT COUNT(*) FROM fragments WHERE created_at > strftime('%s','now') - 604800"
```

## 3. Episode Backlog

```bash
wc -l "C:/Users/arogers/dev/proj-freecontext/freecontext/data/episodes.jsonl" 2>/dev/null || echo "0"
```

## 4. Report

Present the results as:

```
FREECONTEXT HEALTH

Status:        [green/yellow/red]
Fragments:     [count] total
Type coverage: [any types at 0?]
Dominance:     [any type >40%?]
Embedding gap: [% missing]
Backlog:       [episode count]
Last capture:  [X minutes/hours ago]

Issues: [list any yellow/red signals, or "none"]
```

Flag anything that needs action before proceeding with session work.
