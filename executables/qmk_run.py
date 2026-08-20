#!/usr/bin/env python3
"""
TUI wrapper for QMK keymap operations: comment stripping and compilation.

Discovers keymaps from qmk.json build_targets, presents a picker (or accepts
a number/fuzzy-match argument to skip the picker on repeat runs).

Lives in qmk_userspace but runs qmk commands inside qmk_firmware.
"""

import enum
import json
import subprocess
import sys
from difflib import SequenceMatcher
from pathlib import Path

USERSPACE_ROOT = Path(__file__).resolve().parent.parent
QMK_FIRMWARE = USERSPACE_ROOT.parent / "qmk_firmware"
JSONC_TOOL = USERSPACE_ROOT / "executables" / "jsonc_tool.py"

class Action(enum.Enum):
    COMPILE = "compile"
    FLASH = "flash"
    STRIP = "strip"
    APPLY = "apply"


def load_targets():
    qmk_json = USERSPACE_ROOT / "qmk.json"
    if not qmk_json.exists():
        print(f"Error: {qmk_json} not found", file=sys.stderr)
        sys.exit(1)
    data = json.loads(qmk_json.read_text())
    return data.get("build_targets", [])


def resolve_keymap_dir(keyboard, keymap):
    """Find the keymap.json in userspace, stripping revision from keyboard path."""
    parts = keyboard.split("/")
    # Try progressively shorter keyboard paths to handle revisions
    for end in range(len(parts), 0, -1):
        candidate = USERSPACE_ROOT / "keyboards" / "/".join(parts[:end]) / "keymaps" / keymap
        if candidate.exists():
            return candidate
    return None


def short_keyboard(keyboard):
    """Extract the meaningful board name, skipping revision suffixes."""
    parts = keyboard.split("/")
    if len(parts) < 2:
        return keyboard
    if parts[0] == "handwired":
        return parts[-1]
    return parts[-2]


def display_targets(targets):
    print("\nAvailable keymaps:")
    print("-" * 50)
    for i, (kb, km) in enumerate(targets, 1):
        short_kb = short_keyboard(kb)
        print(f"  {i}) {short_kb}/{km}  [{kb}]")
    print()


def fuzzy_score(query, keyboard, keymap):
    query = query.lower()
    short_kb = short_keyboard(keyboard)
    candidates = [
        keymap.lower(),
        short_kb.lower(),
        f"{short_kb}/{keymap}".lower(),
        keyboard.lower(),
        f"{keyboard}:{keymap}".lower(),
    ]
    return max(SequenceMatcher(None, query, c).ratio() for c in candidates)


def pick_target(targets, selector=None):
    if selector is None:
        display_targets(targets)
        try:
            selector = input("Select keymap (number or name): ").strip()
        except (KeyboardInterrupt, EOFError):
            print()
            sys.exit(0)

    if not selector:
        sys.exit(0)

    # Try as a number first
    try:
        idx = int(selector) - 1
        if 0 <= idx < len(targets):
            return targets[idx]
        print(f"Error: number out of range (1-{len(targets)})", file=sys.stderr)
        sys.exit(1)
    except ValueError:
        pass

    # Fuzzy match
    scored = [(fuzzy_score(selector, kb, km), kb, km) for kb, km in targets]
    scored.sort(key=lambda x: x[0], reverse=True)
    best_score, best_kb, best_km = scored[0]

    if best_score < 0.4:
        print(f"No match found for '{selector}'", file=sys.stderr)
        sys.exit(1)

    short_kb = short_keyboard(best_kb)
    label = f"{short_kb}/{best_km}"

    if best_score < 0.8:
        try:
            confirm = input(f"Did you mean '{label}' [{best_kb}]? (y/N) ").strip().lower()
        except (KeyboardInterrupt, EOFError):
            print()
            sys.exit(0)
        if confirm not in ("y", "yes"):
            sys.exit(0)
    else:
        print(f"Matched: {label}")

    return (best_kb, best_km)


def pick_action():
    print("\nActions:")
    print("  1) compile        - qmk compile")
    print("  2) flash          - qmk flash")
    print("  3) strip comments - strip // comments from keymap.json")
    print("  4) apply comments - restore // comments to keymap.json")
    print()
    try:
        choice = input("Select action (number or name): ").strip().lower()
    except (KeyboardInterrupt, EOFError):
        print()
        sys.exit(0)

    actions = {
        "1": Action.COMPILE, "compile": Action.COMPILE,
        "2": Action.FLASH, "flash": Action.FLASH,
        "3": Action.STRIP, "strip": Action.STRIP,
        "4": Action.APPLY, "apply": Action.APPLY,
    }
    action = actions.get(choice)
    if not action:
        print(f"Unknown action: '{choice}'", file=sys.stderr)
        sys.exit(1)
    return action


def run_qmk_cmd(action: Action, keyboard: str, keymap: str) -> int:
    cmd = ["qmk", action.value, "-kb", keyboard, "-km", keymap]
    print(f"\n> {' '.join(cmd)}")
    print(f"  (cwd: {QMK_FIRMWARE})\n")
    return subprocess.run(cmd, cwd=QMK_FIRMWARE).returncode


def run_jsonc(action: Action, keyboard: str, keymap: str):
    keymap_dir = resolve_keymap_dir(keyboard, keymap)
    if not keymap_dir:
        print(f"Error: cannot find keymap directory for {keyboard}:{keymap}", file=sys.stderr)
        return 1
    keymap_file = keymap_dir / "keymap.json"
    if not keymap_file.exists():
        print(f"Error: {keymap_file} not found", file=sys.stderr)
        return 1

    cmd = [sys.executable, str(JSONC_TOOL), action.value, str(keymap_file)]
    print(f"\n> {' '.join(cmd)}\n")
    return subprocess.run(cmd).returncode


def main():
    import argparse

    parser = argparse.ArgumentParser(
        description="TUI wrapper for QMK keymap operations",
    )
    parser.add_argument(
        "target", nargs="?", default=None,
        help="Keymap selector: number from the list, or fuzzy name match",
    )
    parser.add_argument(
        "-a", "--action", choices=list(Action), type=lambda a: Action(a.lower()),
        help="Action to perform (skip action picker)",
    )
    args = parser.parse_args()

    targets = load_targets()
    if not targets:
        print("No build targets found in qmk.json", file=sys.stderr)
        sys.exit(1)

    keyboard, keymap = pick_target(targets, args.target)
    action = args.action or pick_action()

    print(f"action: {action}")
    if action == Action.COMPILE or action == Action.FLASH:
        rc = run_qmk_cmd(action, keyboard, keymap)
    else:
        rc = run_jsonc(action, keyboard, keymap)

    sys.exit(rc)


if __name__ == "__main__":
    main()
