#!/usr/bin/env python3
"""
Reuse First — installer for Claude Code.

Installs:
  1. Rule   → ~/.claude/rules/reuse-first.md
  2. Hook   → ~/.claude/scripts/reuse-first-check.py + settings.json registration
  3. Skill  → ~/.claude/skills/reuse-first/SKILL.md

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

TARGETS = {
    "rule":  (SRC_DIR / "rule.md",     CLAUDE_DIR / "rules" / "reuse-first.md"),
    "hook":  (SRC_DIR / "hook.py",     CLAUDE_DIR / "scripts" / "reuse-first-check.py"),
    "skill": (SRC_DIR / "SKILL.md",    CLAUDE_DIR / "skills" / "reuse-first" / "SKILL.md"),
}

HOOK_ENTRY = {
    "matcher": "",
    "hooks": [{
        "type": "command",
        "command": "python ~/.claude/scripts/reuse-first-check.py"
    }]
}


def install():
    print("\n🔍 Reuse First — installing...\n")
    installed = []

    for name, (src, dst) in TARGETS.items():
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, dst)
        print(f"  ✅ {name:6s} → {dst}")
        installed.append(name)

    # Register hook in settings.json
    settings_path = CLAUDE_DIR / "settings.json"
    if settings_path.exists():
        with open(settings_path, encoding="utf-8") as f:
            settings = json.load(f)
    else:
        settings = {}

    hooks = settings.setdefault("hooks", {})
    ups = hooks.setdefault("UserPromptSubmit", [])

    already = any(
        "reuse-first" in h.get("command", "")
        for entry in ups
        for h in entry.get("hooks", [])
    )

    if already:
        print(f"\n  ⚠️  Hook already registered in settings.json — skipping")
    else:
        ups.append(HOOK_ENTRY)
        with open(settings_path, "w", encoding="utf-8") as f:
            json.dump(settings, f, indent=2, ensure_ascii=False)
        print(f"  ✅ hook   → settings.json (UserPromptSubmit)")

    print(f"\n🎉 Done! Installed {len(installed)} components.")
    print(f"   Restart Claude Code to activate.\n")


def remove():
    print("\n🗑️  Reuse First — removing...\n")

    for name, (_, dst) in TARGETS.items():
        if dst.exists():
            dst.unlink()
            print(f"  🗑️  {name:6s} ← {dst}")
            # Clean empty skill dir
            if name == "skill" and dst.parent.exists() and not any(dst.parent.iterdir()):
                dst.parent.rmdir()
        else:
            print(f"  —  {name:6s}    (not found, skipping)")

    # Remove hook from settings.json
    settings_path = CLAUDE_DIR / "settings.json"
    if settings_path.exists():
        with open(settings_path, encoding="utf-8") as f:
            settings = json.load(f)

        ups = settings.get("hooks", {}).get("UserPromptSubmit", [])
        before = len(ups)
        ups[:] = [
            entry for entry in ups
            if not any("reuse-first" in h.get("command", "") for h in entry.get("hooks", []))
        ]
        after = len(ups)

        if before != after:
            with open(settings_path, "w", encoding="utf-8") as f:
                json.dump(settings, f, indent=2, ensure_ascii=False)
            print(f"  🗑️  hook   ← settings.json")
        else:
            print(f"  —  hook      (not found in settings.json)")

    print(f"\n✅ Uninstalled. Restart Claude Code to apply.\n")


if __name__ == "__main__":
    if "--remove" in sys.argv or "--uninstall" in sys.argv:
        remove()
    else:
        install()
