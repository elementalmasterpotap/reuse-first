<div align="center">

# 🔍 Reuse First

**Search for existing solutions before writing code.**<br>
Claude Code hook · 30+ triggers · bilingual (EN+RU) · context-aware hints

<br>

[![](https://img.shields.io/badge/v2.0.0-0099CC?style=flat-square)](https://github.com/elementalmasterpotap/reuse-first/releases)
[![](https://img.shields.io/badge/Claude_Code-hook-B464FF?style=flat-square)](https://claude.ai/code)
[![](https://img.shields.io/badge/Python-3.8+-3776AB?style=flat-square&logo=python&logoColor=white)](https://python.org)
[![](https://img.shields.io/badge/license-MIT-22AA44?style=flat-square)](LICENSE)
[![](https://img.shields.io/badge/Telegram-channel-26A5E4?style=flat-square&logo=telegram&logoColor=white)](https://t.me/potap_attic)

</div>

---

<details>
<summary>🇬🇧 English</summary>

## Why

AI coding assistants jump straight to writing code. But often there's already a battle-tested library, a proven template, or a well-documented approach that does exactly what you need.

**Reuse First** makes Claude Code search for existing solutions before writing anything from scratch. Ready-made implementations have **ultimate priority**.

## How it works

```
You type a prompt
        │
        ▼
Hook analyzes your request (30+ regex patterns)
        │
        ├─ Matches "create parser", "build bot", "make CLI tool"...
        │       │
        │       ▼
        │   [REUSE_FIRST] → search GitHub / npm / pip / CodePen first
        │   Context hint: WHERE to search based on task category
        │       │
        │       ├─ Found ready-made (100+ ⭐) → USE IT
        │       ├─ Found partial match → use as BASE
        │       └─ Nothing found → search references → write based on them
        │
        ├─ Matches "fix bug", "refactor", "change color"...
        │   └─ SKIP — no search needed, write immediately
        │
        └─ Short prompt / no match
            └─ SKIP — pass through
```

## What's new in v2.0

- **30+ trigger patterns** (was 10) across 17 categories
- **Context-aware hints** — suggests WHERE to search (GitHub, npm, pip, CodePen, ShaderToy...)
- **14 skip patterns** (was 8) — fewer false positives
- **Bilingual** — English + Russian triggers in every category
- **New categories**: data processing, testing, database/ORM, monitoring, auth, deployment, UI components

## Trigger categories

| Category | Example prompts | Search hint |
|----------|----------------|-------------|
| New implementation | "create a parser", "build an API" | GitHub |
| Utility / tool | "script for converting", "validator" | GitHub + npm/pip |
| Library / package | "SDK wrapper", "plugin for X" | npm/pip/crates |
| Automation | "CI/CD pipeline", "cron scheduler" | GitHub Actions |
| Bot / service | "telegram bot from scratch" | GitHub templates |
| Template | "boilerplate for React app" | GitHub templates |
| Effect / animation | "add parallax effect" | CodePen + ShaderToy |
| Integration | "connect Stripe", "OAuth setup" | GitHub + official SDK |
| CLI app | "command-line tool for..." | GitHub + npm |
| Data processing | "CSV parser", "JSON converter" | npm/pip |
| Testing | "test framework", "mock setup" | npm/pip |
| Database / ORM | "migration tool", "query builder" | npm/pip + GitHub |
| Monitoring | "logger", "metrics dashboard" | GitHub + npm/pip |
| Auth | "JWT auth system", "RBAC" | GitHub + npm/pip |
| Deployment | "Docker compose", "deploy script" | GitHub + Docker Hub |
| UI component | "design system", "widget library" | npm + GitHub |
| Best practices | "best way to handle X" | StackOverflow + docs |

## What does NOT trigger (write immediately)

- Bug fixes, patches (`fix`, `repair`, `patch`)
- Small replacements (`change X to Y`)
- Refactoring existing code
- Style edits (CSS, colors, fonts)
- Documentation, changelogs, commits
- Read-only tasks (explain, show, find, list)
- Deletions, file operations, process commands
- Short answers, slash commands

## Install

```bash
git clone https://github.com/elementalmasterpotap/reuse-first.git
cd reuse-first
python install.py
```

This copies 3 files to `~/.claude/` and registers the hook in `settings.json`:

```
~/.claude/
  ├── rules/reuse-first.md              ← decision tree + criteria
  ├── scripts/reuse-first-check.py      ← UserPromptSubmit hook
  └── skills/reuse-first/SKILL.md       ← knowledge skill
```

## Uninstall

```bash
python install.py --remove
```

## Decision criteria

```
✅ Use ready-made:  100+ stars · active · README · MIT/Apache/BSD · 80%+ coverage
⚠️ Use as base:     20-100 stars · clean code · 50-80% coverage
❌ Write your own:   nothing found · outdated · overengineered · unique logic
```

## Report format

When the hook triggers, Claude reports what it found:

```
🔍 Search: JWT authentication library python
  ├─ ✅ Found: PyJWT (⭐ 5.2k) → using it
  └─ References: jwt.io docs, OWASP auth guide
```

</details>

<details open>
<summary>🇷🇺 Русский</summary>

## Зачем

AI-ассистенты сразу прыгают в написание кода. Но часто уже есть проверенная библиотека, готовый шаблон или задокументированный подход который делает ровно то же самое.

**Reuse First** заставляет Claude Code искать готовые решения перед написанием чего-либо с нуля. Готовые реализации имеют **ультимативный приоритет**.

## Как работает

```
Ты пишешь промпт
        │
        ▼
Хук анализирует запрос (30+ regex паттернов)
        │
        ├─ Матчит "создай парсер", "сделай бота", "напиши CLI"...
        │       │
        │       ▼
        │   [REUSE_FIRST] → сначала искать на GitHub / npm / pip / CodePen
        │   Контекстная подсказка: ГДЕ искать по категории задачи
        │       │
        │       ├─ Нашёл готовое (100+ ⭐) → ИСПОЛЬЗОВАТЬ
        │       ├─ Частичное совпадение → взять как БАЗУ
        │       └─ Ничего нет → искать референсы → писать по ним
        │
        ├─ Матчит "исправь баг", "рефактор", "поменяй цвет"...
        │   └─ ПРОПУСК — поиск не нужен, пишем сразу
        │
        └─ Короткий промпт / нет совпадения
            └─ ПРОПУСК — проходит дальше
```

## Что нового в v2.0

- **30+ триггерных паттернов** (было 10) в 17 категориях
- **Контекстные подсказки** — говорит ГДЕ искать (GitHub, npm, pip, CodePen, ShaderToy...)
- **14 skip-паттернов** (было 8) — меньше ложных срабатываний
- **Двуязычные** — английские + русские триггеры в каждой категории
- **Новые категории**: парсинг данных, тестирование, БД/ORM, мониторинг, авторизация, деплой, UI-компоненты

## Категории триггеров

| Категория | Примеры промптов | Где искать |
|-----------|-----------------|------------|
| Новая реализация | "создай парсер", "реализуй API" | GitHub |
| Утилита / тул | "скрипт для конвертации", "валидатор" | GitHub + npm/pip |
| Библиотека / пакет | "обёртка для SDK", "плагин для X" | npm/pip/crates |
| Автоматизация | "CI/CD пайплайн", "планировщик задач" | GitHub Actions |
| Бот / сервис | "telegram бот с нуля" | GitHub templates |
| Шаблон | "стартер для React приложения" | GitHub templates |
| Эффект / анимация | "добавь параллакс эффект" | CodePen + ShaderToy |
| Интеграция | "подключить Stripe", "настроить OAuth" | GitHub + official SDK |
| CLI приложение | "консольная утилита для..." | GitHub + npm |
| Парсинг данных | "CSV парсер", "JSON конвертер" | npm/pip |
| Тестирование | "тест-фреймворк", "настройка моков" | npm/pip |
| БД / ORM | "инструмент миграций", "query builder" | npm/pip + GitHub |
| Мониторинг | "логгер", "дашборд метрик" | GitHub + npm/pip |
| Авторизация | "JWT система", "RBAC" | GitHub + npm/pip |
| Деплой | "Docker compose", "деплой-скрипт" | GitHub + Docker Hub |
| UI-компонент | "дизайн-система", "библиотека виджетов" | npm + GitHub |
| Best practices | "лучший способ сделать X" | StackOverflow + docs |

## Что НЕ триггерит (пишем сразу)

- Фиксы багов (`исправь`, `почини`, `поправь`)
- Мелкие замены (`поменяй X на Y`)
- Рефакторинг существующего кода
- Стилевые правки (CSS, цвета, шрифты)
- Документация, патчноты, коммиты
- Read-only задачи (объясни, покажи, найди, перечисли)
- Удаление, файловые операции, управление процессами
- Короткие ответы, slash-команды

## Установка

```bash
git clone https://github.com/elementalmasterpotap/reuse-first.git
cd reuse-first
python install.py
```

Копирует 3 файла в `~/.claude/` и регистрирует хук в `settings.json`:

```
~/.claude/
  ├── rules/reuse-first.md              ← дерево решений + критерии
  ├── scripts/reuse-first-check.py      ← UserPromptSubmit хук
  └── skills/reuse-first/SKILL.md       ← knowledge скилл
```

## Удаление

```bash
python install.py --remove
```

## Критерии выбора

```
✅ Использовать:  100+ stars · активное · README · MIT/Apache/BSD · 80%+ покрытие
⚠️ Взять как базу: 20-100 stars · чистый код · 50-80% покрытие
❌ Писать своё:    ничего нет · устарело · overengineered · уникальная логика
```

## Формат отчёта

Когда хук сработал, Claude отчитывается:

```
🔍 Поиск: JWT authentication library python
  ├─ ✅ Найдено: PyJWT (⭐ 5.2k) → использую
  └─ Референсы: jwt.io docs, OWASP auth guide
```

## Первый в своём роде

Это первый open-source инструмент, который заставляет AI-ассистента искать готовые решения перед написанием кода. Мы проверили — аналогов на GitHub нет (март 2026).

</details>

---

<div align="center">

Made by **Potap** · [@potap_attic](https://t.me/potap_attic)

</div>
