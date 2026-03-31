#!/usr/bin/env python3
"""
Reuse First v1.1 — installer for Claude Code.

Installs:
  1. Rule         → ~/.claude/rules/reuse-first.md
  2. Hook (UPS)   → ~/.claude/scripts/reuse-first-check.py
  3. Enforce (Pre) → ~/.claude/scripts/reuse-first-enforce.py
  4. Track (Post)  → ~/.claude/scripts/reuse-first-search-track.py
  5. Patterns     → ~/.claude/scripts/reuse_first_patterns.py
  6. Hints        → ~/.claude/scripts/reuse_first_hints.py
  7. Skill        → ~/.claude/skills/reuse-first/SKILL.md

Hooks registered:
  UserPromptSubmit → reuse-first-check.py  (detect + inject prompt)
  PreToolUse       → reuse-first-enforce.py (block Write/Edit/Bash without search)
  PostToolUse      → reuse-first-search-track.py (track WebSearch done)

Usage:
  python install.py           # install everything
  python install.py --remove  # uninstall everything
"""

import json
import os
import shutil
import sys
from pathlib import Path

CLAUDE_DIR = Path.home() / ".claude"
SRC_DIR = Path(__file__).parent / "src"

# ── Files to copy ─────────────────────────────────────────────────────
TARGETS = {
    "rule":     (SRC_DIR / "rule.md",                    CLAUDE_DIR / "rules" / "reuse-first.md"),
    "hook":     (SRC_DIR / "hook.py",                    CLAUDE_DIR / "scripts" / "reuse-first-check.py"),
    "enforce":  (SRC_DIR / "enforce.py",                 CLAUDE_DIR / "scripts" / "reuse-first-enforce.py"),
    "track":    (SRC_DIR / "search_track.py",            CLAUDE_DIR / "scripts" / "reuse-first-search-track.py"),
    "patterns": (SRC_DIR / "reuse_first_patterns.py",    CLAUDE_DIR / "scripts" / "reuse_first_patterns.py"),
    "hints":    (SRC_DIR / "reuse_first_hints.py",       CLAUDE_DIR / "scripts" / "reuse_first_hints.py"),
    "skill":    (SRC_DIR / "SKILL.md",                   CLAUDE_DIR / "skills" / "reuse-first" / "SKILL.md"),
}

# ── Hooks to register ─────────────────────────────────────────────────
HOOKS = {
    "UserPromptSubmit": {
        "matcher": "",
        "hooks": [{
            "type": "command",
            "command": "python ~/.claude/scripts/reuse-first-check.py"
        }]
    },
    "PreToolUse": {
        "matcher": "Write|Edit|Bash",
        "hooks": [{
            "type": "command",
            "command": "python ~/.claude/scripts/reuse-first-enforce.py"
        }]
    },
    "PostToolUse": {
        "matcher": "WebSearch",
        "hooks": [{
            "type": "command",
            "command": "python ~/.claude/scripts/reuse-first-search-track.py"
        }]
    },
}

MARKER = "reuse-first"


def _load_settings():
    path = CLAUDE_DIR / "settings.json"
    if path.exists():
        with open(path, encoding="utf-8") as f:
            return json.load(f)
    return {}


def _save_settings(settings):
    path = CLAUDE_DIR / "settings.json"
    with open(path, "w", encoding="utf-8") as f:
        json.dump(settings, f, indent=2, ensure_ascii=False)


def _hook_exists(hook_list):
    return any(
        MARKER in h.get("command", "")
        for entry in hook_list
        for h in entry.get("hooks", [])
    )


def install():
    print("\n🔍 Reuse First v1.1 — installing...\n")

    # Copy files
    for name, (src, dst) in TARGETS.items():
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, dst)
        print(f"  ✅ {name:8s} → {dst}")

    # Register hooks
    settings = _load_settings()
    hooks = settings.setdefault("hooks", {})
    registered = 0

    for event, entry in HOOKS.items():
        event_hooks = hooks.setdefault(event, [])
        if _hook_exists(event_hooks):
            print(f"  ⚠️  {event:20s} already registered — skipping")
        else:
            event_hooks.append(entry)
            registered += 1
            print(f"  ✅ {event:20s} → settings.json")

    if registered > 0:
        _save_settings(settings)

    print(f"\n🎉 Done! 7 files + {registered} hooks registered.")
    print(f"   Restart Claude Code to activate.\n")


def remove():
    print("\n🗑️  Reuse First — removing...\n")

    # Remove files
    for name, (_, dst) in TARGETS.items():
        if dst.exists():
            dst.unlink()
            print(f"  🗑️  {name:8s} ← {dst}")
            if name == "skill" and dst.parent.exists() and not any(dst.parent.iterdir()):
                dst.parent.rmdir()
        else:
            print(f"  —  {name:8s}    (not found)")

    # Remove state file
    state_path = CLAUDE_DIR / "reuse-first-state.json"
    if state_path.exists():
        state_path.unlink()
        print(f"  🗑️  state    ← {state_path}")

    # Remove hooks from settings.json
    settings = _load_settings()
    hooks = settings.get("hooks", {})
    removed = 0

    for event in HOOKS:
        event_hooks = hooks.get(event, [])
        before = len(event_hooks)
        event_hooks[:] = [
            entry for entry in event_hooks
            if not any(MARKER in h.get("command", "") for h in entry.get("hooks", []))
        ]
        if len(event_hooks) < before:
            removed += 1
            print(f"  🗑️  {event:20s} ← settings.json")

    if removed > 0:
        _save_settings(settings)

    print(f"\n✅ Uninstalled. Restart Claude Code to apply.\n")


if __name__ == "__main__":
    if "--remove" in sys.argv or "--uninstall" in sys.argv:
        remove()
    else:
        install()
