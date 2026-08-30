#!/usr/bin/env python3
"""
Set CrossOver/Wine DLL overrides required for EDHM/3Dmigoto.

Usage:
  python3 scripts/crossover-edhm-dll-overrides.py "/path/to/Bottles/Elite"

This edits the bottle's user.reg and sets:
  HKCU\Software\Wine\DllOverrides\d3d11 = native,builtin
  HKCU\Software\Wine\DllOverrides\d3dcompiler_47 = native,builtin

Close CrossOver/Elite before running. A timestamped backup of user.reg is made.
"""

from __future__ import annotations

import argparse
import datetime as dt
import shutil
from pathlib import Path

SECTION = r"[Software\\Wine\\DllOverrides]"
OVERRIDES = {
    "d3d11": "native,builtin",
    "d3dcompiler_47": "native,builtin",
}


def quote_reg(name: str, value: str) -> str:
    return f'"{name}"="{value}"'


def patch_user_reg(user_reg: Path) -> bool:
    original = user_reg.read_text(encoding="utf-8", errors="surrogateescape")
    lines = original.splitlines()

    section_index = None
    for i, line in enumerate(lines):
        if line.strip().lower() == SECTION.lower():
            section_index = i
            break

    changed = False
    if section_index is None:
        if lines and lines[-1].strip():
            lines.append("")
        lines.append(f"{SECTION} {int(dt.datetime.now().timestamp())}")
        for name, value in OVERRIDES.items():
            lines.append(quote_reg(name, value))
        changed = True
    else:
        next_section = len(lines)
        for i in range(section_index + 1, len(lines)):
            if lines[i].startswith("["):
                next_section = i
                break

        for name, value in OVERRIDES.items():
            desired = quote_reg(name, value)
            found = False
            prefix = f'"{name.lower()}"='
            for i in range(section_index + 1, next_section):
                if lines[i].lower().startswith(prefix):
                    found = True
                    if lines[i] != desired:
                        lines[i] = desired
                        changed = True
                    break
            if not found:
                lines.insert(next_section, desired)
                next_section += 1
                changed = True

    updated = "\n".join(lines) + "\n"
    if updated != original:
        stamp = dt.datetime.now().strftime("%Y%m%d-%H%M%S")
        backup = user_reg.with_name(f"user.reg.backup-{stamp}")
        shutil.copy2(user_reg, backup)
        user_reg.write_text(updated, encoding="utf-8", errors="surrogateescape")
        print(f"Updated {user_reg}")
        print(f"Backup written to {backup}")
        return True

    print(f"No changes needed: {user_reg}")
    return False


def main() -> int:
    parser = argparse.ArgumentParser(description="Set EDHM DLL overrides in a CrossOver/Wine bottle.")
    parser.add_argument("bottle", type=Path, help="Path to the CrossOver bottle root, e.g. ~/Library/Application Support/CrossOver/Bottles/Elite")
    args = parser.parse_args()

    bottle = args.bottle.expanduser().resolve()
    user_reg = bottle / "user.reg"
    if not user_reg.exists():
        parser.error(f"user.reg not found under bottle: {user_reg}")

    patch_user_reg(user_reg)
    print("Set EDHM overrides: d3d11=native,builtin; d3dcompiler_47=native,builtin")
    print("Restart CrossOver/Elite for changes to take effect.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
