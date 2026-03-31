#!/usr/bin/env python3
"""
PostToolUse хук: трекинг WebSearch для reuse-first.

Когда Claude вызывает WebSearch — отмечаем search_done=True в state.
Это разблокирует PreToolUse enforce хук для Write/Edit/Bash.
"""
import sys
import json
import os

STATE_PATH = os.path.expanduser("~/.claude/reuse-first-state.json")

try:
    payload = json.loads(sys.stdin.read())
    tool_name = payload.get("tool_name", "")

    if tool_name != "WebSearch":
        sys.exit(0)

    # Прочитать текущий state
    state = {}
    try:
        with open(STATE_PATH, encoding="utf-8") as f:
            state = json.load(f)
    except Exception:
        pass

    if not state.get("reuse_required"):
        sys.exit(0)

    # Отметить что поиск выполнен
    state["search_done"] = True
    with open(STATE_PATH, "w", encoding="utf-8") as f:
        json.dump(state, f, ensure_ascii=False)

except Exception:
    pass

sys.exit(0)
