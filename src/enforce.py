#!/usr/bin/env python3
"""
PreToolUse хук: enforcement для [REUSE_FIRST].

Срабатывает ПЕРЕД Write/Edit/Bash — если UPS хук выставил reuse_required=True,
а WebSearch ещё не вызывался → БЛОКИРОВАТЬ до выполнения поиска.

Проверяет:
1. reuse-first-state.json → reuse_required == True
2. search_done == False
3. Claude пытается Write/Edit/Bash (начинает кодить)
→ BLOCK с инструкцией сначала сделать WebSearch

Когда Claude вызывает WebSearch → state обновляется через search-track.py
"""
import sys
import json
import os

STATE_PATH = os.path.expanduser("~/.claude/reuse-first-state.json")


def _read_state():
    try:
        with open(STATE_PATH, encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {}


try:
    payload = json.loads(sys.stdin.read())
    tool_name = payload.get("tool_name", "")

    # Только для инструментов записи/выполнения
    if tool_name not in ("Write", "Edit", "Bash"):
        sys.exit(0)

    # Не блокировать запись в state-файл и служебные файлы
    if tool_name in ("Write", "Edit"):
        file_path = payload.get("tool_input", {}).get("file_path", "")
        if "reuse-first-state" in file_path or "settings.json" in file_path:
            sys.exit(0)

    # Bash: пропускать нерелевантные команды (ls, git, mkdir, rm и т.д.)
    if tool_name == "Bash":
        cmd = payload.get("tool_input", {}).get("command", "")
        # Разрешаем всё кроме создания файлов/скриптов
        write_indicators = [
            "cat <<", "cat >", "echo >", "tee ", "printf >",
            "python ", "py ", "node ", "pip install",
        ]
        if not any(ind in cmd for ind in write_indicators):
            sys.exit(0)

    state = _read_state()

    if not state.get("reuse_required"):
        sys.exit(0)

    if state.get("search_done"):
        sys.exit(0)

    # Reuse required, поиск НЕ выполнен, Claude начинает кодить → BLOCK
    result = {
        "decision": "block",
        "reason": (
            "⛔ [REUSE_FIRST] Сначала WebSearch!\n"
            "Выполни 2-3 WebSearch запроса перед написанием кода.\n"
            "Отчёт: 🔍 Поиск: [запрос] → ✅/⚠️/❌ результат.\n"
            "Только после отчёта о поиске — начинай кодить."
        ),
    }
    print(json.dumps(result, ensure_ascii=False))

except Exception:
    pass

sys.exit(0)
