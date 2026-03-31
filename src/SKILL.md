---
name: reuse-first
description: Search for existing solutions before writing code — ultimate priority for ready-made implementations
user-invocable: false
---

# Reuse First

Automated hook that detects when you're about to write something that probably already exists.

## How it works

UserPromptSubmit hook analyzes every prompt and triggers when it detects:

```
6 trigger combinations:
  verb + noun       "create a system", "write a parser"
  standalone        "from scratch", "alternative to", "best way to"
  verb + tech       "add oauth", "integrate stripe"
  tech + noun       "telegram bot", "redis queue"
  domain phrase     "drag and drop", "rate limiter", "dark mode"
  verb + long       any create verb in a prompt > 60 chars
```

## Coverage

- 70+ create verbs (RU + EN, including slang)
- 200+ object nouns across 15 categories
- 30+ standalone trigger phrases
- 300+ technology keywords (frameworks, databases, APIs, tools)
- 25+ domain-specific phrases (web, devops, AI/ML, security)
- Context-aware search hints (npm, pip, CodePen, Docker Hub, etc.)

## Skip patterns (no false positives)

Bug fixes, read-only questions, style edits, deletions, short answers,
slash commands, workflow ops, file operations, process control.

## Output

Injects `[REUSE_FIRST]` via `injectedSystemPrompt` — Claude MUST search
before writing code. Terminal hint via stderr for the user.
