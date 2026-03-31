#!/usr/bin/env python3
"""
REUSE FIRST v1.0 — UserPromptSubmit хук для Claude Code.

Детектирует задачи где нужно сначала искать готовое решение.
6 триггерных комбинаций. 400+ паттернов. RU + EN.

Hook: UserPromptSubmit
Output: {"injectedSystemPrompt": "..."} на stdout

Модули:
  reuse_first_patterns.py — SKIP, VERBS, NOUNS, STANDALONE, TECH, DOMAIN
  reuse_first_hints.py    — where_to_search() с 60+ подсказками
"""
import json
import os
import re
import sys

# Добавляем директорию скрипта в PATH для импорта модулей
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# ── State файл для enforcement (PreToolUse хук проверяет) ─────────────
REUSE_STATE_PATH = os.path.expanduser("~/.claude/reuse-first-state.json")

def _write_reuse_state(data):
    try:
        with open(REUSE_STATE_PATH, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False)
    except Exception:
        pass

from reuse_first_patterns import (
    SKIP_PATTERNS,
    CREATE_VERBS_RU, CREATE_VERBS_EN,
    OBJECT_NOUNS_RU, OBJECT_NOUNS_EN,
    STANDALONE_TRIGGERS,
    TECH_KEYWORDS,
    DOMAIN_PHRASES,
)
from reuse_first_hints import where_to_search


def main():
    try:
        data = json.load(sys.stdin)
    except (json.JSONDecodeError, EOFError):
        return

    prompt = (
        data.get("user_message")
        or data.get("user_prompt")
        or data.get("prompt")
        or ""
    ).strip()

    if not prompt or len(prompt) < 15:
        return

    prompt_lower = prompt.lower()

    # ── SKIP check ─────────────────────────────────────────────────────
    for skip in SKIP_PATTERNS:
        if re.search(skip, prompt_lower, re.IGNORECASE):
            return

    # ── Signal detection ───────────────────────────────────────────────
    has_create_verb = bool(
        re.search(CREATE_VERBS_RU, prompt_lower, re.I)
        or re.search(CREATE_VERBS_EN, prompt_lower, re.I)
    )
    has_object_noun = bool(
        re.search(OBJECT_NOUNS_RU, prompt_lower, re.I)
        or re.search(OBJECT_NOUNS_EN, prompt_lower, re.I)
    )
    has_standalone = any(
        re.search(p, prompt_lower, re.I) for p in STANDALONE_TRIGGERS
    )
    has_tech = bool(re.search(TECH_KEYWORDS, prompt_lower, re.I))
    has_domain = any(
        re.search(p, prompt_lower, re.I) for p in DOMAIN_PHRASES
    )

    # ── TRIGGER LOGIC (6 комбинаций) ───────────────────────────────────
    reasons = []
    if has_create_verb and has_object_noun:  reasons.append("verb+noun")
    if has_standalone:                       reasons.append("standalone")
    if has_create_verb and has_tech:         reasons.append("verb+tech")
    if has_tech and has_object_noun:         reasons.append("tech+noun")
    if has_domain:                           reasons.append("domain")
    if has_create_verb and len(prompt) > 60: reasons.append("verb+long")

    if not reasons:
        return

    # ── Write state for enforce hook ──────────────────────────────────
    _write_reuse_state({
        "reuse_required": True,
        "prompt_preview": prompt[:80],
        "reasons": reasons,
    })

    # ── Output ─────────────────────────────────────────────────────────
    where_sources, where_queries = where_to_search(prompt_lower)
    reason_str = "+".join(reasons)

    print(
        f"\n\U0001f50d [REUSE_FIRST] \u0418\u0449\u0438 \u0433\u043e\u0442\u043e\u0432\u043e\u0435 \u2192 {where_sources}\n",
        file=sys.stderr,
    )

    # Build deep search queries block
    q_block = ""
    if where_queries:
        q_lines = " | ".join(where_queries[:6])
        q_block = f" Конкретные источники: {q_lines}."

    hint = (
        f"[REUSE_FIRST] ({reason_str}) "
        f"СТОП! Перед написанием ЛЮБОГО кода — ОБЯЗАТЕЛЬНЫЙ 3-этапный поиск готовых реализаций.\n"
        f"\n"
        f"## ЭТАП 1 — Прямой поиск готового (БЛОКЕР)\n"
        f"Выполни 2-3 WebSearch запроса:\n"
        f"  - \"[суть задачи] github stars:>50\"\n"
        f"  - \"[суть задачи] npm package\" / \"pip install [задача]\"\n"
        f"  - \"awesome [тема]\" / \"[задача] library 2025\"\n"
        f"Где искать: {where_sources}.{q_block}\n"
        f"\n"
        f"## ЭТАП 2 — Оценка найденного\n"
        f"  \u2705 100+ stars, активный, MIT/Apache \u2192 ИСПОЛЬЗОВАТЬ. Не писать своё. [УЛЬТИМАТИВНЫЙ ПРИОРИТЕТ]\n"
        f"  \u26a0\ufe0f 20-100 stars, покрывает 50%+ \u2192 Взять как базу, адаптировать.\n"
        f"  \u274c Ничего подходящего \u2192 перейти к Этапу 3.\n"
        f"\n"
        f"## ЭТАП 3 — Референсы и best practices (если готового нет)\n"
        f"  - \"[задача] best practices 2025\"\n"
        f"  - \"[задача] tutorial\" / \"how to [задача]\"\n"
        f"  - \"[задача] example code\" / \"[задача] implementation guide\"\n"
        f"  Писать на основе найденных референсов, НЕ из памяти.\n"
        f"\n"
        f"## ОТЧЁТ (обязательно в начале ответа)\n"
        f"\U0001f50d Поиск: [что искал]\n"
        f"  \u251c\u2500 \u2705 Найдено: [название] (\u2b50 N, ссылка) \u2192 использую\n"
        f"  \u251c\u2500 \u26a0\ufe0f Частичное: [название] \u2192 беру как базу\n"
        f"  \u2514\u2500 \u274c Не найдено \u2192 пишу с нуля, референсы: [ссылки]\n"
        f"\n"
        f"ГОТОВОЕ РЕШЕНИЕ = УЛЬТИМАТИВНЫЙ ПРИОРИТЕТ. НЕ НАЧИНАЙ писать код пока не выполнил все 3 этапа."
    )
    print(json.dumps({"injectedSystemPrompt": hint}, ensure_ascii=False))


if __name__ == "__main__":
    main()
