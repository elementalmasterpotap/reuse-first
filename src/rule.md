# Reuse First — search for existing solutions before writing code

## Principle [BLOCKER]

Before implementing any task — **search for existing solutions first**.
Ready-made implementations have **ultimate priority** over writing from scratch.

```
Task received → "can I find this ready-made?"
       │
       ├─ YES (utility / library / script / template / plugin)
       │       │
       │       ▼
       │   WebSearch: "topic + github/npm/pip/solution"
       │       │
       │       ├─ Found ready-made (100+ stars / active / proven)
       │       │   └─ USE IT. Don't write your own. [ULTIMATE PRIORITY]
       │       │
       │       ├─ Found partial (50%+ coverage)
       │       │   └─ Use as base, adapt. Link in comment.
       │       │
       │       └─ Nothing ready-made found
       │           └─ Search for advice / references / best practices
       │               └─ Write based on them, not from memory
       │
       └─ NO (unique business logic / project-specific)
           └─ Write immediately, but check patterns (StackOverflow, docs)
```

---

## Where to search

```
Task type                         Where to search
───────────────────────────────────────────────────────────────
CLI utility / tool                GitHub (stars, active)
npm package / JS library          npmjs.com, GitHub
Python package                    PyPI, GitHub
Claude Code extension             claude-code-plugins, GitHub
Automation / CI/CD                GitHub Actions marketplace
Template / boilerplate            GitHub templates, cookiecutter
UI component                      npm, CodePen, GitHub
Algorithm / pattern               StackOverflow, docs, MDN
Shader / effect                   ShaderToy, CodePen, GitHub
Telegram bot feature              GitHub, ptb examples
Integration / API                 Official SDK → GitHub wrapper
Monitoring / logging              GitHub, npm/pip
Deployment / Docker               Docker Hub, GitHub
Auth / security                   GitHub, npm/pip
Data processing (CSV/JSON/XML)    npm/pip (pandas, cheerio)
Testing                           npm/pip (pytest, jest)
Database / ORM                    npm/pip + GitHub
```

---

## Criteria: "ready-made is good enough"

```
✅ Use if:
  · 100+ stars (or well-known author)
  · Last commit < 6 months ago
  · Has README with examples
  · Compatible license (MIT / Apache / BSD)
  · Solves 80%+ of the task

⚠️ Use as base if:
  · 20-100 stars but clean code
  · Covers 50-80% of the task
  · Needs minimal adaptation

❌ Write your own if:
  · Nothing suitable found
  · Ready-made is outdated (2+ years without commits, deprecated)
  · Ready-made is overengineered (pulls 50 deps for a simple task)
  · Unique project business logic
```

---

## Search algorithm (3 steps)

```
Step 1 — Direct search:
  "[task] github"
  "[task] npm package" / "pip install"

Step 2 — If no ready-made, search references:
  "[task] best practices 2025"
  "[task] tutorial"
  "how to [task] [language/framework]"

Step 3 — If references are scarce:
  "[task] example code"
  "[task] implementation guide"
```

---

## What NOT to search for (write immediately)

```
· Point bug fix in existing code
· Config / constants change
· Refactoring existing module
· Style edits (CSS, colors, fonts)
· Text / copywriting / changelogs
· Project-specific business logic
· Version bumps / updates
· File operations (move, copy, delete)
· Process commands (run, start, stop)
· Slash commands / workflow operations
```

---

## Report format

When searched — briefly report:

```
🔍 Search: [what you searched for]
  ├─ ✅ Found: [name] (stars, link) → using it
  ├─ ⚠️ Partial: [name] → using as base
  └─ ❌ Nothing found → writing from scratch, references: [links]
```
