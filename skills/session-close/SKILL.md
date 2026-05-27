---
name: session-close
description: Run the full session close ritual. Distills the session, writes the Obsidian session log, syncs repos. Use when Austin says "close" or "done for today".
allowed-tools: Bash, Write, mcp__freecontext__session_close, mcp__freecontext__save_checkpoint, mcp__freecontext__log_exchange
---

# Session Close Ritual

Execute the full session close protocol in order.

## Step 1 — Session Distillation

Call `mcp__freecontext__session_close` with:
- `session_summary`: Date-prefixed summary (e.g. `"[2026-04-28] Built X, fixed Y, decided Z"`)
- `key_observations`: List of notable `[*]` and significant `[**]` observations from the session

Tag significant observations `[**]` if they represent a major decision, architectural insight, or behavior change. Tag notable ones `[*]`.

## Step 2 — FreeContext DB Backup

```python
import sqlite3
src = sqlite3.connect('C:/Users/arogers/dev/proj-freecontext/freecontext/data/freecontext.db')
src.execute('PRAGMA wal_checkpoint(TRUNCATE)')
dst = sqlite3.connect('C:/Users/arogers/dev/proj-freecontext/fc-data/freecontext.db')
src.backup(dst)
dst.close()
src.close()
print('DB sync: freecontext -> fc-data (safe backup)')
```

Also copy episode logs:
```bash
cp "C:/Users/arogers/dev/proj-freecontext/freecontext/data/episodes.jsonl" "C:/Users/arogers/dev/proj-freecontext/fc-data/episodes.jsonl"
cp "C:/Users/arogers/dev/proj-freecontext/freecontext/data/episode_log.jsonl" "C:/Users/arogers/dev/proj-freecontext/fc-data/episode_log.jsonl"
```

## Step 3 — Obsidian Session Log

Write curated session log at `g:/My Drive/Obsidian/Sessions/YYYY-MM-DD.md`.

If the file exists, append a new `## Session N` block above any existing `## Raw episodes` section.

Cover: what was worked on, decisions + rationale, files touched, `[[wikilinks]]` to project pages, next steps. Tag line `#session` + topic tags. Rough and scannable.

## Step 4 — Repo Sync

Commit and push all repos with actual changes:

```bash
for base in "C:/Users/arogers/dev" "g:/My Drive/Project Data/Alpha Team"; do
  for path in proj-freecontext/freecontext proj-freecontext/fc-data proj-alphaskills/alpha-skills proj-fready/fready proj-podspace/pod-space proj-webingest/web-ingest proj-conduit/telegram-dispatch proj-mediaingest/media-ingest proj-claudetolucid/claude-to-lucid proj-snowflakemcp/snowflake-mcp proj-openwhispr/openwhispr proj-aether/aether proj-audiopipeline/audio-pipeline; do
    dir="$base/$path"
    [ -d "$dir/.git" ] || continue
    cd "$dir"
    if [ -n "$(git status --porcelain)" ]; then
      echo "=== $dir ==="
      git add -A && git commit -m "Session sync $(date +%Y-%m-%d)" && git push 2>&1 | tail -3
    fi
  done
done
```

## Step 5 — Report

```
SESSION CLOSED

Distilled:   [summary one line]
Observations: [count] stored
Repos pushed: [list repos that had changes]
Log written:  Sessions/YYYY-MM-DD.md

Issues: [any push failures or errors]
```
