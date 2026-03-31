# Reuse First — search for existing solutions before writing code

## Principle [BLOCKER]

Before implementing ANY new feature, utility, integration, or system —
**search for existing solutions first**. Ready-made = ultimate priority.

```
Task received → "Can I find something ready-made?"
       │
       ├─ YES (utility / library / template / plugin / effect)
       │       │
       │       ▼
       │   WebSearch: "[task] + github/npm/pip/solution"
       │       │
       │       ├─ Found (50+ stars, active, maintained)
       │       │   └─ USE IT. Don't write your own. [ULTIMATE PRIORITY]
       │       │
       │       ├─ Partial coverage (50%+)
       │       │   └─ Use as base, adapt. Link in comments.
       │       │
       │       └─ Nothing found
       │           └─ Search for advice / references / best practices
       │               └─ Write based on those, not from memory
       │
       └─ NO (unique business logic / project-specific)
           └─ Write immediately, but check patterns (SO, docs)
```

## What NOT to search (write immediately)

- Point bug fixes in existing code
- Config / constant changes
- Refactoring existing modules
- Style edits (CSS, colors, fonts)
- Text / copywriting / patchnotes
- Project-specific business logic
- Workflow operations (deploy, commit)

## Report format

```
🔍 Search: [what you searched for]
  ├─ ✅ Found: [name] (⭐ N, link) → using it
  ├─ ⚠️ Partial: [name] → using as base
  └─ ❌ Nothing found → writing from scratch, references: [links]
```
