"""
Reuse First — UserPromptSubmit hook for Claude Code.
Detects tasks where you should search for existing solutions first.
Injects [REUSE_FIRST] hint via stderr.

Hook: UserPromptSubmit
Type: hint (stderr), non-blocking

Install: python install.py
Or manually add to ~/.claude/settings.json → hooks → UserPromptSubmit
"""

import json
import re
import sys


# Patterns for tasks where you SHOULD search for existing solutions
SEARCH_TRIGGERS = [
    # Creating something new
    (r"(create|write|make|build|implement|develop|design)\s+.{5,}", "new implementation"),
    # Russian equivalents
    (r"(созда[йюь]|напиши|сделай|реализуй|разработай|построй)\s+.{5,}", "new implementation"),
    # Utilities and tools
    (r"(utilit|tool|script|parser|converter|утилит|инструмент|тул|скрипт|парсер|конвертер)", "utility/tool"),
    # Libraries and packages
    (r"(library|package|module|plugin|extension|библиотек|пакет|модуль|плагин|расширение)", "library/package"),
    # Automation
    (r"(automat|workflow|pipeline|ci.?cd|автоматиз|пайплайн|деплой.?скрипт)", "automation"),
    # Bot / service from scratch
    (r"(bot\s|service|api.?server|бот[а ]|сервис)\s.*(from scratch|new|с нуля|новый)", "service from scratch"),
    # Templates
    (r"(template|boilerplate|starter|scaffold|шаблон|стартер)", "template"),
    # Effects / animations
    (r"(effect|animation|transition|shader|эффект|анимаци|шейдер)\s.*(add|create|implement|добавь|сделай|создай)", "effect/animation"),
    # Integrations
    (r"(integrat|connect|webhook|oauth|sso|интеграци|подключ)", "integration"),
    # CLI
    (r"(cli|command.?line|terminal|консольн)\s.*(app|tool|утилит|приложение)", "CLI app"),
]

# Patterns for tasks where you should NOT search (write immediately)
SKIP_PATTERNS = [
    r"(fix|repair|patch|исправь|почини|поправь|фикс)\s",       # point fixes
    r"(change|swap|replace|измени|поменяй|замени)\s.{3,20}$",   # small replacements
    r"(refactor|рефактор)",                                       # refactoring
    r"(style|css|color|font|стил[ья]|цвет|шрифт)",              # style edits
    r"(changelog|patchnote|commit|патчнот|коммит)",              # documentation
    r"(explain|show|find|list|объясни|покажи|найди|перечисли)",  # read-only
    r"(delete|remove|удали|убери)\s",                             # deletion
    r"^(yes|no|ok|да|нет|ок|ага|угу|норм)",                      # short answers
]


def main():
    try:
        data = json.load(sys.stdin)
    except (json.JSONDecodeError, EOFError):
        return

    prompt = data.get("user_prompt", "").strip().lower()
    if not prompt or len(prompt) < 15:
        return

    # Skip if task doesn't require searching
    for skip in SKIP_PATTERNS:
        if re.search(skip, prompt, re.IGNORECASE):
            return

    # Check triggers
    matched = []
    for pattern, category in SEARCH_TRIGGERS:
        if re.search(pattern, prompt, re.IGNORECASE):
            matched.append(category)

    if matched:
        cats = ", ".join(matched[:2])
        print(
            f"\n\U0001f50d [REUSE_FIRST] Task detected ({cats}) — "
            f"search for existing solutions first (WebSearch). "
            f"Ready-made implementations have ultimate priority. "
            f"Nothing found → search for references/advice → write based on them.\n",
            file=sys.stderr,
        )


if __name__ == "__main__":
    main()
