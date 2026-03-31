<div align="center">

# Reuse First

**Stop reinventing the wheel. Search before you code.**

Claude Code hook that enforces searching for existing solutions before writing code from scratch.

[![](https://img.shields.io/badge/v1.0.0-0099CC?style=flat-square)](https://github.com/elementalmasterpotap/reuse-first/releases)
[![](https://img.shields.io/badge/Claude_Code-hook-B464FF?style=flat-square)](https://github.com/elementalmasterpotap/reuse-first)
[![](https://img.shields.io/badge/Python-3.9+-3776AB?style=flat-square&logo=python&logoColor=white)](https://python.org)
[![](https://img.shields.io/badge/license-MIT-22AA44?style=flat-square)](LICENSE)
[![](https://img.shields.io/badge/Telegram-channel-26A5E4?style=flat-square&logo=telegram&logoColor=white)](https://t.me/potap_attic)

</div>

---

<details>
<summary>🇬🇧 English</summary>

## Why

AI coding assistants happily write everything from scratch. But most things you ask for already exist as battle-tested libraries, tools, and templates. This hook makes Claude Code **search first, code second**.

## How it works

A `UserPromptSubmit` hook analyzes every prompt. When it detects a task where existing solutions likely exist, it injects `[REUSE_FIRST]` into Claude's system prompt — forcing a web search before any code is written.

### 6 trigger combinations

| # | Combination | Example |
|---|------------|---------|
| 1 | **verb + noun** | "create a monitoring system" |
| 2 | **standalone** | "from scratch", "alternative to X", "best way to" |
| 3 | **verb + tech** | "add oauth", "integrate stripe" |
| 4 | **tech + noun** | "telegram bot", "redis queue" |
| 5 | **domain phrase** | "drag and drop", "rate limiter", "dark mode" |
| 6 | **verb + long prompt** | any create verb in prompt > 60 chars |

### Coverage

- **70+ create verbs** (EN + RU, including slang like "wire up", "spin up")
- **200+ object nouns** across 15 categories (software, data, UI, infra, AI/ML...)
- **30+ standalone triggers** ("from scratch", "how to build", "is there something like...")
- **300+ technology keywords** (frameworks, databases, APIs, clouds, tools)
- **25+ domain phrases** (web dev, devops, security, AI/ML patterns)
- **60+ context-aware search hints** across 6 categories — tells Claude WHERE to search with specific URLs
- **Deep 3-stage search protocol** — structured mandatory workflow, not just "search"

### Smart skip patterns

Won't trigger on: bug fixes, questions, style edits, deletions, short answers, slash commands, deploy/commit, file operations, process control, formatting.

### 3-stage search protocol

```
Stage 1 — Direct search (BLOCKER)
  "[task] github stars:>50" + "[task] npm/pip package" + "awesome [topic]"
  + context-specific sources (Telegram → PTB, CSS → CodePen, etc.)

Stage 2 — Evaluate
  ✅ 100+ stars → USE IT   ⚠️ 50%+ coverage → base   ❌ Nothing → Stage 3

Stage 3 — References (if nothing found)
  "[task] best practices 2025" + "[task] tutorial"
  Write based on references, NOT from memory.
```

## Install

```bash
git clone https://github.com/elementalmasterpotap/reuse-first.git
cd reuse-first
python install.py
```

Installs 7 components:
- `~/.claude/rules/reuse-first.md` — rule file
- `~/.claude/scripts/reuse-first-check.py` — main hook (UserPromptSubmit)
- `~/.claude/scripts/reuse-first-enforce.py` — blocker (PreToolUse on Write/Edit/Bash)
- `~/.claude/scripts/reuse-first-search-track.py` — tracker (PostToolUse on WebSearch)
- `~/.claude/scripts/reuse_first_patterns.py` — detection patterns (400+)
- `~/.claude/scripts/reuse_first_hints.py` — where-to-search hints (60+)
- `~/.claude/skills/reuse-first/SKILL.md` — skill metadata

Registers 3 hooks in `~/.claude/settings.json`:
- `UserPromptSubmit` — detect task, inject search prompt
- `PreToolUse` — block Write/Edit/Bash until WebSearch is done
- `PostToolUse` — track WebSearch completion, unblock enforce

## Uninstall

```bash
python install.py --remove
```

## How Claude responds when triggered

```
🔍 Search: [task description]
  ├─ ✅ Found: [name] (⭐ N, link) → using it
  ├─ ⚠️ Partial: [name] → using as base
  └─ ❌ Nothing found → writing from scratch
```

</details>

<details open>
<summary>🇷🇺 Русский</summary>

## Зачем

AI-ассистенты радостно пишут всё с нуля. Но большинство задач уже решены — есть готовые библиотеки, утилиты, шаблоны. Этот хук заставляет Claude Code **сначала искать, потом писать**.

## Как работает

`UserPromptSubmit` хук анализирует каждый промпт. Когда видит задачу где скорее всего есть готовое решение — инжектирует `[REUSE_FIRST]` в системный промпт Claude, принуждая к веб-поиску до написания кода.

### 6 триггерных комбинаций

| # | Комбинация | Пример |
|---|-----------|--------|
| 1 | **глагол + объект** | "создай систему мониторинга" |
| 2 | **standalone** | "с нуля", "аналог для X", "лучший способ" |
| 3 | **глагол + технология** | "добавь oauth", "прикрути stripe" |
| 4 | **технология + объект** | "telegram бот", "redis очередь" |
| 5 | **доменная фраза** | "drag and drop", "rate limiter", "dark mode" |
| 6 | **глагол + длинный промпт** | любой глагол создания в промпте > 60 символов |

### Покрытие

- **70+ глаголов создания** (RU + EN, включая сленг: "захуярь", "забацай", "склепай")
- **200+ существительных** в 15 категориях (софт, данные, UI, инфра, AI/ML...)
- **30+ standalone триггеров** ("с нуля", "как сделать", "есть что-то типа...")
- **300+ технологий** (фреймворки, БД, API, облака, инструменты)
- **25+ доменных фраз** (веб, devops, безопасность, AI/ML паттерны)
- **60+ контекстных подсказок** в 6 категориях — говорит Claude ГДЕ искать с конкретными URL
- **Глубокий 3-этапный протокол поиска** — не просто "поищи", а структурированный обязательный воркфлоу

### Умные исключения

Не триггерится на: фиксах багов, вопросах, стилевых правках, удалении, коротких ответах, слеш-командах, деплое/коммите, файловых операциях.

### 3-этапный протокол поиска

```
Этап 1 — Прямой поиск (БЛОКЕР)
  "[задача] github stars:>50" + "[задача] npm/pip" + "awesome [тема]"
  + контекстные источники (Telegram → PTB, CSS → CodePen и т.д.)

Этап 2 — Оценка
  ✅ 100+ stars → ИСПОЛЬЗОВАТЬ   ⚠️ 50%+ покрытие → база   ❌ Нет → Этап 3

Этап 3 — Референсы (если готового нет)
  "[задача] best practices 2025" + "[задача] tutorial"
  Писать на основе референсов, НЕ из памяти.
```

## Установка

```bash
git clone https://github.com/elementalmasterpotap/reuse-first.git
cd reuse-first
python install.py
```

Устанавливает 3 компонента:
- `~/.claude/rules/reuse-first.md` — правило
- `~/.claude/scripts/reuse-first-check.py` — скрипт хука
- `~/.claude/skills/reuse-first/SKILL.md` — метаданные скилла

Регистрирует хук в `~/.claude/settings.json` (секция `UserPromptSubmit`).

## Удаление

```bash
python install.py --remove
```

## Как Claude отвечает при срабатывании

```
🔍 Поиск: [описание задачи]
  ├─ ✅ Найдено: [название] (⭐ N, ссылка) → использую
  ├─ ⚠️ Частичное: [название] → беру как базу
  └─ ❌ Не найдено → пишу с нуля
```

</details>
