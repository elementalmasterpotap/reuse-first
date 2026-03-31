<div align="center">

# 🔍 Reuse First

**Stop reinventing the wheel. Search before you code.**<br>
Auto-detection · WebSearch enforcement · Ready-made priority

<br>

[![](https://img.shields.io/badge/v1.0.0-0099CC?style=flat-square)](https://github.com/elementalmasterpotap/reuse-first/releases)
[![](https://img.shields.io/badge/Claude_Code-hook-B8860B?style=flat-square)](https://claude.ai/code)
[![](https://img.shields.io/badge/Python-3.8+-3776AB?style=flat-square&logo=python&logoColor=white)](https://python.org)
[![](https://img.shields.io/badge/license-MIT-22AA44?style=flat-square)](LICENSE)
[![](https://img.shields.io/badge/Telegram-channel-26A5E4?style=flat-square&logo=telegram&logoColor=white)](https://t.me/potap_attic)

<br>

<details>
<summary>🇬🇧 English</summary>

<br>

**The first enforcement system that makes Claude Code search for existing solutions before writing code from scratch.**

Every time you ask Claude to create something new — a utility, integration, bot, template — the hook automatically detects it and injects a `[REUSE_FIRST]` signal. Claude then searches the web for ready-made solutions before writing a single line of code.

## Why

AI coding assistants are great at writing code. Too great. They'll happily write from scratch what already exists as a battle-tested library with 10k stars. This wastes your time and tokens — and produces inferior results.

**Reuse First** fixes this by enforcing a simple rule: **search first, code second.**

## How it works

```
You: "create a CLI tool for monitoring Docker containers"
                    │
          ┌─────────▼──────────┐
          │  UserPromptSubmit   │
          │  hook detects:      │
          │  "create" + "tool"  │
          └─────────┬──────────┘
                    │
        🔍 [REUSE_FIRST] injected
                    │
          ┌─────────▼──────────┐
          │  Claude searches:   │
          │  "docker monitor    │
          │   CLI github"       │
          └─────────┬──────────┘
                    │
      ┌─────────────┼─────────────┐
      │             │             │
  ✅ Found      ⚠️ Partial    ❌ Nothing
  lazydocker    dry but old    found
  (40k ⭐)      (200 ⭐)
      │             │             │
  USE IT        Adapt it      Search refs
                              then write
```

## What triggers the search

| Trigger | Examples |
|---------|----------|
| Creating something new | "create", "build", "implement", "make" |
| Utilities & tools | "tool", "script", "parser", "converter" |
| Libraries & packages | "library", "package", "module", "plugin" |
| Automation | "automate", "workflow", "pipeline", "CI/CD" |
| Integrations | "integrate", "connect", "webhook", "OAuth" |
| Templates | "template", "boilerplate", "starter", "scaffold" |
| Effects | "effect", "animation", "shader" |
| CLI apps | "CLI", "command-line tool" |

**Bilingual** — triggers work in both English and Russian.

## What does NOT trigger (write immediately)

- Bug fixes, refactoring, style edits
- Config changes, text/copywriting
- Short answers, questions, read-only tasks

## Install

```bash
git clone https://github.com/elementalmasterpotap/reuse-first
cd reuse-first
python install.py
```

Installs 3 components into `~/.claude/`:

```
~/.claude/
├── rules/reuse-first.md              ← rule (decision tree)
├── scripts/reuse-first-check.py      ← hook (auto-detection)
└── skills/reuse-first/SKILL.md       ← skill (search algorithm)
```

Restart Claude Code after install.

## Uninstall

```bash
python install.py --remove
```

Removes all 3 components + hook registration from `settings.json`.

## Decision criteria

```
✅ Use ready-made:  100+ ⭐, active, MIT/Apache/BSD, solves 80%+
⚠️ Use as base:     20+ ⭐, clean code, covers 50-80%
❌ Write your own:   nothing found / outdated / overengineered
```

## Report format

After searching, Claude reports:
```
🔍 Search: docker monitoring CLI
  ├─ ✅ Found: lazydocker (⭐ 40k) → using it
  └─ No need to write from scratch
```

</details>

<details open>
<summary>🇷🇺 Русский</summary>

<br>

**Первая система принуждения, которая заставляет Claude Code искать готовые решения перед написанием кода с нуля.**

Каждый раз когда просишь Claude создать что-то новое — утилиту, интеграцию, бота, шаблон — хук автоматически детектит это и инжектирует сигнал `[REUSE_FIRST]`. Claude ищет в сети готовые решения прежде чем написать хоть строчку кода.

## Зачем

AI-ассистенты охуенно пишут код. Слишком охуенно. Они с удовольствием напишут с нуля то, что уже существует как проверенная библиотека с 10k звёзд. Это тратит время и токены — и даёт результат хуже.

**Reuse First** чинит это простым правилом: **сначала ищи, потом пиши.**

## Как работает

```
Ты: "создай CLI утилиту для мониторинга Docker контейнеров"
                    │
          ┌─────────▼──────────┐
          │  UserPromptSubmit   │
          │  хук детектит:      │
          │  "создай" + "утилит"│
          └─────────┬──────────┘
                    │
        🔍 [REUSE_FIRST] инжектирован
                    │
          ┌─────────▼──────────┐
          │  Claude ищет:       │
          │  "docker monitor    │
          │   CLI github"       │
          └─────────┬──────────┘
                    │
      ┌─────────────┼─────────────┐
      │             │             │
  ✅ Нашёл      ⚠️ Частичное   ❌ Ничего
  lazydocker    dry но старый   не нашёл
  (40k ⭐)      (200 ⭐)
      │             │             │
ИСПОЛЬЗОВАТЬ   Взять за основу  Искать
                              референсы
                              → писать
```

## Что триггерит поиск

| Триггер | Примеры |
|---------|---------|
| Создание нового | "создай", "напиши", "сделай", "реализуй" |
| Утилиты и инструменты | "утилита", "скрипт", "парсер", "конвертер" |
| Библиотеки и пакеты | "библиотека", "пакет", "модуль", "плагин" |
| Автоматизация | "автоматизация", "workflow", "пайплайн" |
| Интеграции | "интеграция", "подключить", "webhook" |
| Шаблоны | "шаблон", "boilerplate", "стартер" |
| Эффекты | "эффект", "анимация", "шейдер" |
| CLI | "CLI", "консольное приложение" |

**Двуязычный** — триггеры работают на английском и русском.

## Что НЕ триггерит (писать сразу)

- Баг-фиксы, рефакторинг, стилевые правки
- Изменение конфига, тексты/копирайтинг
- Короткие ответы, вопросы, read-only задачи

## Установка

```bash
git clone https://github.com/elementalmasterpotap/reuse-first
cd reuse-first
python install.py
```

Устанавливает 3 компонента в `~/.claude/`:

```
~/.claude/
├── rules/reuse-first.md              ← правило (дерево решений)
├── scripts/reuse-first-check.py      ← хук (автодетекция)
└── skills/reuse-first/SKILL.md       ← скилл (алгоритм поиска)
```

Перезапусти Claude Code после установки.

## Удаление

```bash
python install.py --remove
```

Удаляет все 3 компонента + регистрацию хука из `settings.json`.

## Критерии выбора

```
✅ Использовать готовое:   100+ ⭐, активное, MIT/Apache/BSD, решает 80%+
⚠️ Взять за основу:        20+ ⭐, чистый код, покрывает 50-80%
❌ Писать своё:             ничего не нашёл / устарело / оверинжинирено
```

## Формат отчёта

После поиска Claude отчитывается:
```
🔍 Поиск: docker monitoring CLI
  ├─ ✅ Нашёл: lazydocker (⭐ 40k) → использую
  └─ Писать с нуля не нужно
```

</details>

---

<sub>First-of-its-kind — no similar enforcement systems found in the Claude Code ecosystem (March 2026).</sub>

</div>
