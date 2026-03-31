---
name: reuse-first
description: Search for existing solutions before writing code — ultimate priority for ready-made implementations
user-invocable: false
---

# Reuse First — search for existing solutions first

## When loaded

Automatically via `hook.py` (UserPromptSubmit).
Injects `[REUSE_FIRST]` when task matches a pattern.

## Algorithm

```
1. WebSearch("[task] github") or WebSearch("[task] npm/pip/package")
       │
       ├─ Found ready-made (100+ stars, active, license ok)
       │   └─ USE IT. Install/connect. Don't write your own.
       │
       ├─ Found partial (20+ stars, 50%+ coverage)
       │   └─ Use as base, adapt for the task.
       │
       └─ Nothing ready-made found
           │
           ▼
2. WebSearch("[task] best practices / tutorial / how to")
       │
       ├─ Found advice/references
       │   └─ Write based on them, link in comments.
       │
       └─ Nothing useful
           └─ Write from your knowledge, note that you searched.
```

## Report

```
🔍 Search: [what you searched for]
  ├─ ✅ Found: [name] (⭐ N, link) → using it
  ├─ ⚠️ Partial: [name] → using as base
  └─ ❌ Nothing found → writing from scratch, references: [links]
```

## Rules

- Ready-made = **ultimate priority** (not a "recommendation")
- Don't search for: fixes, refactoring, styles, text, small edits
- Search for: new features, utilities, integrations, services, effects, templates
- Full criteria → `rule.md`
