#!/usr/bin/env python3
"""Parse all_vim_cmds.txt (excerpted Vim :help index) into vim_cmds.json.

The JSON keeps the full key sequence for each command (so e.g. the second key
of "CTRL-W CTRL-B" is preserved), plus a pre-parsed "first" key (base + mods)
so tmux-keys-html.py can quickly map commands onto a keyboard grid by first
keystroke.
"""

import argparse
import json
import os
import re
import sys

# Vim key name -> grid key name used by tmux-keys-html.py
SPECIAL_KEYS = {
    "BS": "BSpace", "Del": "Delete", "Tab": "Tab", "CR": "Enter", "NL": "Enter",
    "Esc": "Escape", "Space": "Space", "Enter": "Enter",
    "Left": "Left", "Right": "Right", "Up": "Up", "Down": "Down",
    "Home": "Home", "End": "End", "PageUp": "PgUp", "PageDown": "PgDn",
    "Insert": "Insert", "F1": "F1", "Help": "Help",
    "Undo": "Undo", "Redo": "Redo",
}

# Single-character keys we accept as-is
ALLOWED_SINGLE = set("-=[]\\;'\",./~`!?@#$%^&*()_+<>:0123456789")


def map_key(k):
    """Map a single vim key name to our grid key name, or None if unmappable."""
    if k in SPECIAL_KEYS:
        return SPECIAL_KEYS[k]
    if len(k) == 1:
        if k.isalpha():
            return k.lower()
        if k == " ":
            return "Space"
        if k == "|":
            return "\\"
        if k in ALLOWED_SINGLE:
            return k
    return None


def parse_first_key(tokens):
    """Parse the first concrete key from a vim command's token list.

    Returns (base_grid_key, mods_str) where mods_str is the canonical "SCM"
    ordering of shift/ctrl/alt, or None if the command has no well-defined
    first key (placeholder first char, key ranges, mouse keys, ...).
    """
    if not tokens:
        return None
    # Strip optional ["x] register prefix (e.g. '["x]dd' activates on 'd')
    tok = re.sub(r'^\["x\]', "", tokens[0])
    if not tok:
        return None
    # Placeholder first char ("{char1}<BS>{char2}") or count range ("1-9")
    if tok.startswith(("{", "'")) or re.fullmatch(r"\d+[-–]\d+", tok):
        return None

    # CTRL-X / CTRL-\ form
    if tok.startswith("CTRL-") and len(tok) == 6:
        base = map_key(tok[5:])
        return (base, "C") if base else None

    # <...> form, e.g. <BS>, <C-Left>, <S-Up>
    if tok.startswith("<") and tok.endswith(">"):
        inner = tok[1:-1]
        mods = ""
        m = re.match(r"([CSM]+)-(.+)", inner)
        if m:
            mods = "".join(x for x in "SCM" if x in m.group(1))
            inner = m.group(2)
        base = map_key(inner)
        return (base, mods) if base else None

    # Plain token: first character is the key (e.g. "g" in "g{char}",
    # "d" in "dd", "z" in "z<CR>")
    base = map_key(tok[0])
    return (base, "") if base else None


def section_mode(major, minor):
    if major == 1:
        return "insert"
    if major == 2:
        if minor == 1:
            return "text-objects"
        if minor == 6:
            return "operator-pending"
        return "normal"
    if major == 3:
        return "visual"
    if major == 4:
        return "command-line"
    if major == 5:
        return "terminal"
    if major == 6:
        return "ex"
    return None


MODE_LABELS = {
    "insert": "Insert mode",
    "normal": "Normal mode",
    "text-objects": "Text objects",
    "operator-pending": "Operator-pending",
    "visual": "Visual mode",
    "command-line": "Command-line",
    "terminal": "Terminal-Job",
    "ex": "Ex commands",
}


def parse_file(path):
    modes = {}  # id -> {"label": ..., "commands": [...]}
    order = []
    current = None

    with open(path, encoding="utf-8") as f:
        for line in f:
            line = line.rstrip("\n")
            if not line.strip():
                continue

            # Section header, e.g. "2. Normal mode" or "2.1 Text objects"
            m = re.match(r"^(\d+)\.(\d+)?\s+\S", line)
            if m:
                current = section_mode(int(m.group(1)), m.group(2) and int(m.group(2)))
                if current and current not in modes:
                    modes[current] = {"label": MODE_LABELS[current], "commands": []}
                    order.append(current)
                elif not current:
                    current = None
                continue

            if not line.startswith("|") or current is None:
                continue  # continuation/sub-header lines (e.g. completion menu)

            parts = [p.strip() for p in line.split("\t") if p.strip()]
            if len(parts) < 3:
                continue
            keys_str, desc = parts[1], parts[2]
            # Strip the leading count/linewise flag column ("2  ...", "1,2  ...")
            desc = re.sub(r"^[12](,[12])?\s+", "", desc).strip()
            tokens = keys_str.split()
            first = parse_first_key(tokens)
            modes[current]["commands"].append({
                "keys": tokens,
                "first": {"base": first[0], "mods": list(first[1])} if first else None,
                "desc": desc,
            })

    return {"modes": [{"id": i, **modes[i]} for i in order]}


def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    parser = argparse.ArgumentParser(description="Parse all_vim_cmds.txt into JSON")
    parser.add_argument("source", nargs="?", default=os.path.normpath(os.path.join(script_dir, "..", "all_vim_cmds.txt")))
    parser.add_argument("output", nargs="?", default=os.path.normpath(os.path.join(script_dir, "..", "vim_cmds.json")))
    args = parser.parse_args()

    data = parse_file(args.source)
    total = sum(len(m["commands"]) for m in data["modes"])
    mapped = sum(1 for m in data["modes"] for c in m["commands"] if c["first"])
    with open(args.output, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=1)
        f.write("\n")
    print(f"Parsed {total} commands ({mapped} with a mappable first key) from {args.source}")
    for m in data["modes"]:
        print(f"  {m['label']}: {len(m['commands'])} commands")
    print(f"Written to: {args.output}")


if __name__ == "__main__":
    main()
