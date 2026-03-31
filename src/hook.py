"""
Reuse First — UserPromptSubmit hook for Claude Code.
Detects tasks where you should search for existing solutions first.
Injects [REUSE_FIRST] hint via stderr with context-aware search suggestions.

Hook: UserPromptSubmit
Type: hint (stderr), non-blocking

Install: python install.py
Or manually add to ~/.claude/settings.json → hooks → UserPromptSubmit
"""

import json
import re
import sys


# ── SEARCH TRIGGERS ─────────────────────────────────────────────────────
# (pattern, category, where_to_search)
SEARCH_TRIGGERS = [
    # ── Creating something new ──────────────────────────────────────
    (r"(create|write|make|build|implement|develop|design|generate|set\s?up)\s+.{5,}",
     "new implementation", "GitHub"),
    (r"(созда[йюь]|напиши|сделай|реализуй|разработай|построй|сгенерируй|настрой)\s+.{5,}",
     "new implementation", "GitHub"),

    # ── Utilities and tools ─────────────────────────────────────────
    (r"(utilit|tool|script|parser|converter|formatter|linter|validator|checker|generator|scraper|crawler)",
     "utility/tool", "GitHub + npm/pip"),
    (r"(утилит|инструмент|тул|скрипт|парсер|конвертер|форматтер|линтер|валидатор|генератор|скрейпер)",
     "utility/tool", "GitHub + npm/pip"),

    # ── Libraries and packages ──────────────────────────────────────
    (r"(library|package|module|plugin|extension|sdk|wrapper|client|binding)",
     "library/package", "npm/pip/crates"),
    (r"(библиотек|пакет|модуль|плагин|расширение|обёртк|клиент|биндинг)",
     "library/package", "npm/pip/crates"),

    # ── Automation / CI/CD ──────────────────────────────────────────
    (r"(automat|workflow|pipeline|ci.?cd|cron|scheduler|задач.?планиров)",
     "automation", "GitHub Actions"),
    (r"(автоматиз|пайплайн|деплой.?скрипт|авто.?запуск|планировщик)",
     "automation", "GitHub Actions"),

    # ── Bots / services ─────────────────────────────────────────────
    (r"(bot\s|service|api.?server|microservice|backend|daemon).{3,}(from scratch|new|start|с нуля|нов|запуск)",
     "service from scratch", "GitHub templates"),
    (r"(бот[а ]|сервис|бэкенд|микросервис|демон).{3,}(с нуля|нов|запуск|старт|создай)",
     "service from scratch", "GitHub templates"),

    # ── Templates / boilerplate ─────────────────────────────────────
    (r"(template|boilerplate|starter|scaffold|cookiecutter|archetype)",
     "template", "GitHub templates"),
    (r"(шаблон|стартер|скаффолд|заготовк|болванк)",
     "template", "GitHub templates"),

    # ── Effects / animations / visual ───────────────────────────────
    (r"(effect|animation|transition|shader|particle|parallax|canvas).{2,}(add|create|implement|make)",
     "effect/animation", "CodePen + ShaderToy + GitHub"),
    (r"(эффект|анимаци|шейдер|частиц|параллакс|канвас).{2,}(добавь|сделай|создай|реализуй|прикрути)",
     "effect/animation", "CodePen + ShaderToy + GitHub"),

    # ── Integrations / APIs ─────────────────────────────────────────
    (r"(integrat|connect to|webhook|oauth|sso|api\s+key|stripe|paypal|twilio|sendgrid)",
     "integration", "GitHub + official SDK"),
    (r"(интеграци|подключ|вебхук|авторизаци|платёж|оплат|отправк.?email)",
     "integration", "GitHub + official SDK"),

    # ── CLI apps ────────────────────────────────────────────────────
    (r"(cli|command.?line|terminal|console)\s.{3,}(app|tool|утилит|приложение)",
     "CLI app", "GitHub + npm"),
    (r"(консольн|терминальн|командн.?строк)\s.{3,}(приложение|утилит|тул)",
     "CLI app", "GitHub + npm"),

    # ── Data processing ─────────────────────────────────────────────
    (r"(csv|json|xml|yaml|excel|pdf)\s.*(pars|read|convert|export|import|process)",
     "data processing", "npm/pip"),
    (r"(csv|json|xml|yaml|excel|pdf)\s.*(парс|чита|конверт|экспорт|импорт|обработ)",
     "data processing", "npm/pip"),

    # ── Testing ─────────────────────────────────────────────────────
    (r"(test.?framework|mock|stub|fixture|e2e|тест.?фреймворк|мок|фикстур)",
     "testing tool", "npm/pip"),

    # ── Database / ORM ──────────────────────────────────────────────
    (r"(orm|database.?layer|migration.?tool|query.?builder|миграци.?инструмент)",
     "database tool", "npm/pip + GitHub"),

    # ── Monitoring / logging ────────────────────────────────────────
    (r"(monitor|logger|metric|dashboard|alert|мониторинг|логгер|метрик|дашборд|алерт)",
     "monitoring", "GitHub + npm/pip"),

    # ── Auth / security ─────────────────────────────────────────────
    (r"(auth.?system|login.?system|rbac|permission|jwt|token.?auth|систем.?авториз|вход.?систем)",
     "auth system", "GitHub + npm/pip"),

    # ── Deployment ──────────────────────────────────────────────────
    (r"(deploy.?script|docker.?compose|k8s|terraform|ansible|деплой.?скрипт|докер.?композ)",
     "deployment", "GitHub + Docker Hub"),

    # ── UI components ───────────────────────────────────────────────
    (r"(component|widget|ui.?kit|design.?system|компонент|виджет|дизайн.?систем)",
     "UI component", "npm + GitHub"),

    # ── Best practices request ──────────────────────────────────────
    (r"(как лучше|best way to|recommended approach|лучший способ|оптимальный подход)\s.{10,}",
     "best practices", "StackOverflow + docs"),

    # ── Explicit "need something new" ───────────────────────────────
    (r"(нужен|нужна|нужно|want|need)\s+(новый|новая|новое|new|a)\s+.{5,}",
     "new thing", "GitHub"),
]

# ── SKIP PATTERNS ───────────────────────────────────────────────────────
# Tasks where searching would be wasteful
SKIP_PATTERNS = [
    r"(fix|repair|patch|исправь|почини|поправь|фикс|пофикс)\s",       # point fixes
    r"(change|swap|replace|измени|поменяй|замени|переименуй)\s.{3,30}$",  # small replacements
    r"(refactor|рефактор|отрефач|перепиши.{0,15}$)",                   # refactoring
    r"(style|css|color|font|стил[ья]|цвет|шрифт|отступ)",             # style edits
    r"(changelog|patchnote|commit|патчнот|коммит|README)",             # docs
    r"(explain|show|find|list|describe|объясни|покажи|найди|перечисли|опиши|расскажи)",  # read-only
    r"(delete|remove|удали|убери|вырежи|снеси)\s",                     # deletion
    r"^(yes|no|ok|да|нет|ок|ага|угу|норм|збс|го|погнали|давай|все|всё)",  # short answers
    r"(review|ревью|разбор|compact|сжат|деплой|задеплой)",             # workflow commands
    r"(обнови|update|upgrade|bump)\s.{3,20}$",                         # version bumps
    r"(перенеси|move|переместi|скопируй|copy)\s",                      # file operations
    r"(запусти|run|start|stop|restart|перезапусти)",                    # process commands
    r"(открой|open|прочитай|read|cat|grep|check|проверь)\s",           # inspection
    r"/\w+",                                                            # slash commands
]


def main():
    try:
        data = json.load(sys.stdin)
    except (json.JSONDecodeError, EOFError):
        return

    prompt = data.get("user_prompt", "").strip()
    if not prompt or len(prompt) < 15:
        return

    prompt_lower = prompt.lower()

    # Skip if task doesn't require searching
    for skip in SKIP_PATTERNS:
        if re.search(skip, prompt_lower, re.IGNORECASE):
            return

    # Check triggers
    matched = []
    where_set = set()
    for pattern, category, where in SEARCH_TRIGGERS:
        if re.search(pattern, prompt_lower, re.IGNORECASE):
            if category not in [m[0] for m in matched]:
                matched.append((category, where))
                where_set.update(w.strip() for w in where.split("+"))

    if matched:
        cats = ", ".join(m[0] for m in matched[:3])
        where_hint = " · ".join(sorted(where_set)[:4])

        print(
            f"\n\U0001f50d [REUSE_FIRST] Task detected ({cats})\n"
            f"   → Search first: {where_hint}\n"
            f"   → Ready-made implementations have ultimate priority\n"
            f"   → Nothing found → search for references/advice → write based on them\n",
            file=sys.stderr,
        )


if __name__ == "__main__":
    main()
