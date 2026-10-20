#!/usr/bin/env python3
"""Generate an interactive HTML keyboard layout (full 100% ANSI, no numpad) for
tmux/vim keybindings with click popups, modifier toggles, and QMK keymap overlay.

The QMK overlay only affects the core 60% alphanumeric set; the F-row and nav
cluster are always shown as static keys that can still receive SW bindings.
"""

import subprocess
import sys
import re
import os
import json
from html import escape

# ---------------------------------------------------------------------------
# Layout definitions
# ---------------------------------------------------------------------------

# 60% layout — used ONLY for QMK info.json coordinate matching.
# Tuple: (display_label, tmux_name, width_units)
SIXTY_ROWS = [
    [("Esc", "Escape", 1), ("1", "1", 1), ("2", "2", 1), ("3", "3", 1),
     ("4", "4", 1), ("5", "5", 1), ("6", "6", 1), ("7", "7", 1),
     ("8", "8", 1), ("9", "9", 1), ("0", "0", 1), ("-", "-", 1),
     ("=", "=", 1), ("Bksp", "BSpace", 1.5)],
    [("Tab", "Tab", 1.5), ("Q", "q", 1), ("W", "w", 1), ("E", "e", 1),
     ("R", "r", 1), ("T", "t", 1), ("Y", "y", 1), ("U", "u", 1),
     ("I", "i", 1), ("O", "o", 1), ("P", "p", 1), ("[", "[", 1),
     ("]", "]", 1), ("\\", "\\", 1)],
    [("Caps", "Caps", 1.75), ("A", "a", 1), ("S", "s", 1), ("D", "d", 1),
     ("F", "f", 1), ("G", "g", 1), ("H", "h", 1), ("J", "j", 1),
     ("K", "k", 1), ("L", "l", 1), (";", ";", 1), ("'", "'", 1),
     ("Enter", "Enter", 1.75)],
    [("Shift", "LShift", 2.25), ("Z", "z", 1), ("X", "x", 1), ("C", "c", 1),
     ("V", "v", 1), ("B", "b", 1), ("N", "n", 1), ("M", "m", 1),
     (",", ",", 1), (".", ".", 1), ("/", "/", 1), ("Shift", "RShift", 2.75)],
    [("Ctrl", "LCtrl", 1.25), ("Win", "LGui", 1.25), ("Alt", "LAlt", 1.25),
     ("Space", "Space", 6.25), ("Alt", "RAlt", 1.25), ("Win", "RGui", 1.25),
     ("Menu", "App", 1.25), ("Ctrl", "RCtrl", 1.25)],
]

# Full 100% ANSI layout (no numpad) — used for HTML rendering.
# Each row is a list of items. Each item is either:
#   ("key", display_label, tmux_name, width_units)
#   ("gap", width_units)
FULL_ROWS = [
    # Row 0: F-row
    [
        ("key", "Esc", "Escape", 1),
        ("gap", 1),
        ("key", "F1", "F1", 1), ("key", "F2", "F2", 1),
        ("key", "F3", "F3", 1), ("key", "F4", "F4", 1),
        ("gap", 0.5),
        ("key", "F5", "F5", 1), ("key", "F6", "F6", 1),
        ("key", "F7", "F7", 1), ("key", "F8", "F8", 1),
        ("gap", 0.5),
        ("key", "F9", "F9", 1), ("key", "F10", "F10", 1),
        ("key", "F11", "F11", 1), ("key", "F12", "F12", 1),
        ("gap", 0.25),
        ("key", "PrtSc", "PrtSc", 1), ("key", "ScrLk", "Scroll", 1),
        ("key", "Pause", "Pause", 1),
    ],
    # Row 1: Number row + nav cluster
    [
        ("key", "`~", "`", 1),
        ("key", "1!", "1", 1), ("key", "2@", "2", 1), ("key", "3#", "3", 1),
        ("key", "4$", "4", 1), ("key", "5%", "5", 1), ("key", "6^", "6", 1),
        ("key", "7&", "7", 1), ("key", "8*", "8", 1), ("key", "9(", "9", 1),
        ("key", "0)", "0", 1), ("key", "-_", "-", 1), ("key", "=+", "=", 1),
        ("key", "Bksp", "BSpace", 2),
        ("gap", 0.25),
        ("key", "Ins", "Insert", 1), ("key", "Home", "Home", 1),
        ("key", "PgUp", "PgUp", 1),
    ],
    # Row 2: QWERTY + nav cluster
    [
        ("key", "Tab", "Tab", 1.5),
        ("key", "Q", "q", 1), ("key", "W", "w", 1), ("key", "E", "e", 1),
        ("key", "R", "r", 1), ("key", "T", "t", 1), ("key", "Y", "y", 1),
        ("key", "U", "u", 1), ("key", "I", "i", 1), ("key", "O", "o", 1),
        ("key", "P", "p", 1), ("key", "[{", "[", 1), ("key", "]}", "]", 1),
        ("key", "\\|", "\\", 1.5),
        ("gap", 0.25),
        ("key", "Del", "Delete", 1), ("key", "End", "End", 1),
        ("key", "PgDn", "PgDn", 1),
    ],
    # Row 3: Home row
    [
        ("key", "Caps", "Caps", 1.75),
        ("key", "A", "a", 1), ("key", "S", "s", 1), ("key", "D", "d", 1),
        ("key", "F", "f", 1), ("key", "G", "g", 1), ("key", "H", "h", 1),
        ("key", "J", "j", 1), ("key", "K", "k", 1), ("key", "L", "l", 1),
        ("key", ";:", ";", 1), ("key", "'\"", "'", 1),
        ("key", "Enter", "Enter", 2.25),
    ],
    # Row 4: Bottom row + Up arrow
    [
        ("key", "Shift", "LShift", 2.25),
        ("key", "Z", "z", 1), ("key", "X", "x", 1), ("key", "C", "c", 1),
        ("key", "V", "v", 1), ("key", "B", "b", 1), ("key", "N", "n", 1),
        ("key", "M", "m", 1), ("key", ",<", ",", 1), ("key", ".>", ".", 1),
        ("key", "/?", "/", 1),
        ("key", "Shift", "RShift", 2.75),
        ("gap", 1.25),
        ("key", "↑", "Up", 1),
    ],
    # Row 5: Modifiers + arrows
    [
        ("key", "Ctrl", "LCtrl", 1.25),
        ("key", "Win", "LGui", 1.25),
        ("key", "Alt", "LAlt", 1.25),
        ("key", "Space", "Space", 6.25),
        ("key", "Alt", "RAlt", 1.25),
        ("key", "Win", "RGui", 1.25),
        ("key", "Menu", "App", 1.25),
        ("key", "Ctrl", "RCtrl", 1.25),
        ("gap", 0.25),
        ("key", "←", "Left", 1), ("key", "↓", "Down", 1), ("key", "→", "Right", 1),
    ],
]


def full_layout_tmux_names():
    """Return the set of all tmux key names in the full layout."""
    names = set()
    for row in FULL_ROWS:
        for item in row:
            if item[0] == "key":
                names.add(item[2])
    return names


# ---------------------------------------------------------------------------
# QMK keycode mapping (unchanged)
# ---------------------------------------------------------------------------

QMK_TO_TMUX_KEY = {
    "KC_A": "a", "KC_B": "b", "KC_C": "c", "KC_D": "d", "KC_E": "e",
    "KC_F": "f", "KC_G": "g", "KC_H": "h", "KC_I": "i", "KC_J": "j",
    "KC_K": "k", "KC_L": "l", "KC_M": "m", "KC_N": "n", "KC_O": "o",
    "KC_P": "p", "KC_Q": "q", "KC_R": "r", "KC_S": "s", "KC_T": "t",
    "KC_U": "u", "KC_V": "v", "KC_W": "w", "KC_X": "x", "KC_Y": "y",
    "KC_Z": "z",
    "KC_1": "1", "KC_2": "2", "KC_3": "3", "KC_4": "4", "KC_5": "5",
    "KC_6": "6", "KC_7": "7", "KC_8": "8", "KC_9": "9", "KC_0": "0",
    "KC_MINS": "-", "KC_EQL": "=", "KC_LBRC": "[", "KC_RBRC": "]",
    "KC_BSLS": "\\", "KC_SCLN": ";", "KC_QUOT": "'", "KC_GRV": "`",
    "KC_COMM": ",", "KC_DOT": ".", "KC_SLSH": "/",
    "KC_SPC": "Space", "KC_ENT": "Enter", "KC_TAB": "Tab",
    "KC_BSPC": "BSpace", "KC_DEL": "Delete", "KC_ESC": "Escape",
    "KC_LEFT": "Left", "KC_RGHT": "Right", "KC_UP": "Up", "KC_DOWN": "Down",
    "KC_HOME": "Home", "KC_END": "End", "KC_PGUP": "PgUp", "KC_PGDN": "PgDn",
    "KC_INS": "Insert",
    "KC_F1": "F1", "KC_F2": "F2", "KC_F3": "F3", "KC_F4": "F4",
    "KC_F5": "F5", "KC_F6": "F6", "KC_F7": "F7", "KC_F8": "F8",
    "KC_F9": "F9", "KC_F10": "F10", "KC_F11": "F11", "KC_F12": "F12",
    "KC_PSCR": "PrtSc", "KC_SLCK": "Scroll", "KC_PAUS": "Pause",
    "KC_VOLU": "VolUp", "KC_VOLD": "VolDn",
    "KC_MPLY": "MediaPlay", "KC_MPRV": "MediaPrev", "KC_MNXT": "MediaNext",
    "KC_PENT": "KPEnter", "KC_PWR": "Power",
    "KC_LCTL": "LCtrl", "KC_RCTL": "RCtrl", "KC_LSFT": "LShift",
    "KC_RSFT": "RShift", "KC_LALT": "LAlt", "KC_RALT": "RAlt",
    "KC_LGUI": "LGui", "KC_RGUI": "RGui", "KC_APP": "App",
    "KC_NO": None,
}

# Default (unremapped) keycode for each physical position on the 60% layout.
DEFAULT_LAYER_0 = [
    "KC_ESC", "KC_1", "KC_2", "KC_3", "KC_4", "KC_5", "KC_6", "KC_7",
    "KC_8", "KC_9", "KC_0", "KC_MINS", "KC_EQL", "KC_BSLS", "KC_GRV",
    "KC_TAB", "KC_Q", "KC_W", "KC_E", "KC_R", "KC_T", "KC_Y", "KC_U",
    "KC_I", "KC_O", "KC_P", "KC_LBRC", "KC_RBRC", "KC_BSPC",
    "KC_LCTL", "KC_A", "KC_S", "KC_D", "KC_F", "KC_G", "KC_H", "KC_J",
    "KC_K", "KC_L", "KC_SCLN", "KC_QUOT", "KC_ENT",
    "KC_LSFT", "KC_Z", "KC_X", "KC_C", "KC_V", "KC_B", "KC_N", "KC_M",
    "KC_COMM", "KC_DOT", "KC_SLSH", "KC_RSFT", "KC_FN",
    "KC_LCTL", "KC_LGUI", "KC_LALT", "KC_SPC", "KC_RALT", "KC_RGUI",
    "KC_APP", "KC_RCTL",
]


# ---------------------------------------------------------------------------
# QMK keymap loading
# ---------------------------------------------------------------------------

def qmk_position_to_grid_key(phys_layout):
    """Map QMK physical layout indices to 60% grid tmux key names via coordinates."""
    idx_to_key = {}
    for idx, pos in enumerate(phys_layout):
        x, y = pos["x"], pos["y"]
        row_idx = int(y)
        if row_idx >= len(SIXTY_ROWS):
            continue
        curr_x = 0.0
        for _, tmux_name, width in SIXTY_ROWS[row_idx]:
            if abs(curr_x - x) < 0.3:
                idx_to_key[idx] = tmux_name
                break
            curr_x += width
    return idx_to_key


def parse_qmk_keycode(kc):
    """Extract the base keycode and modifier info from a QMK keycode string."""
    if kc in ("KC_TRNS", "KC_NO", "KC_TRANSPARENT", "_______", "XXXXXXX"):
        return kc, None

    # LT(layer, kc) - layer tap: tap produces kc, hold activates layer
    m = re.match(r'LT\((\d+),\s*(\w+)\)', kc)
    if m:
        return m.group(2), f"LT({m.group(1)})"

    # Mod-tap: LSFT_T(kc), LCTL_T(kc), LGUI_T(kc), etc
    m = re.match(r'(\w+)_T\((\w+)\)', kc)
    if m:
        return m.group(2), m.group(1)

    # MO(layer), TG(layer), etc - pure layer keys
    m_layer = re.match(r'(MO|TG|TT|OSL|TO)\((\d+)\)', kc)
    if m_layer:
        return "LAYER", kc

    # QK_GESC
    if kc == "QK_GESC":
        return "KC_ESC", "GESC"

    # QK_BOOT, etc
    if kc.startswith("QK_"):
        return kc, None

    return kc, None


def resolve_key_output(base_kc):
    """Resolve a base keycode to what tmux would actually receive."""
    if base_kc in QMK_TO_TMUX_KEY:
        return QMK_TO_TMUX_KEY[base_kc]
    if base_kc.startswith("KC_"):
        return base_kc[3:]
    return base_kc


def find_info_json(keyboard_name, layout_name, keymap_path, qmk_firmware_path=None):
    """Find info.json with the given layout, searching userspace then qmk_firmware."""
    # First, walk up from the keymap directory (works when keymap is inside qmk_firmware)
    keymap_dir = os.path.dirname(os.path.abspath(keymap_path))
    parts = keymap_dir.split("/")
    for i in range(len(parts), 0, -1):
        candidate = "/".join(parts[:i]) + "/info.json"
        if os.path.exists(candidate):
            try:
                with open(candidate) as f_info:
                    info = json.load(f_info)
                if "layouts" in info and layout_name in info["layouts"]:
                    return candidate
            except (json.JSONDecodeError, KeyError):
                continue

    # Fallback: look in qmk_firmware/keyboards/<keyboard_name>/info.json,
    # walking up parent dirs to handle QMK's directory inheritance (e.g. rev1 inherits from parent)
    if qmk_firmware_path:
        kb_parts = keyboard_name.split("/")
        for i in range(len(kb_parts), 0, -1):
            candidate = os.path.join(qmk_firmware_path, "keyboards", *kb_parts[:i], "info.json")
            if os.path.exists(candidate):
                try:
                    with open(candidate) as f_info:
                        info = json.load(f_info)
                    if "layouts" in info and layout_name in info["layouts"]:
                        return candidate
                except (json.JSONDecodeError, KeyError):
                    continue

    return None


def load_qmk_keymap(keymap_path, qmk_firmware_path=None):
    """Load QMK keymap and return per-layer data mapping grid keys to their resolved output."""
    with open(keymap_path) as f:
        keymap = json.load(f)

    keyboard_name = keymap.get("keyboard", "")
    layout_name = keymap.get("layout", "")

    info_path = find_info_json(keyboard_name, layout_name, keymap_path, qmk_firmware_path)
    if not info_path:
        print(f"Warning: Could not find info.json with layout '{layout_name}'", file=sys.stderr)
        return None

    with open(info_path) as f_info:
        info = json.load(f_info)

    phys_layout = info["layouts"][layout_name]["layout"]
    idx_to_key = qmk_position_to_grid_key(phys_layout)

    layers_data = []
    for layer in keymap["layers"]:
        layer_keys = {}
        for idx, kc in enumerate(layer):
            if idx not in idx_to_key:
                continue
            grid_key = idx_to_key[idx]
            base_kc, mod_info = parse_qmk_keycode(kc)

            # Determine what this key resolves to
            if base_kc in ("KC_TRNS", "KC_TRANSPARENT", "_______"):
                status = "transparent"
                resolved = None
                default_kc = DEFAULT_LAYER_0[idx] if idx < len(DEFAULT_LAYER_0) else None
                default_resolved = resolve_key_output(default_kc) if default_kc else None
            elif base_kc in ("KC_NO", "XXXXXXX"):
                status = "blocked"
                resolved = None
                default_resolved = None
            elif base_kc == "LAYER":
                status = "layer"
                resolved = None
                default_resolved = None
            else:
                resolved = resolve_key_output(base_kc)
                default_kc = DEFAULT_LAYER_0[idx] if idx < len(DEFAULT_LAYER_0) else None
                default_resolved = resolve_key_output(default_kc) if default_kc else None

                # Is this a remap? Compare what key produces vs what it "should" produce
                if resolved == default_resolved or (default_kc == "KC_FN"):
                    status = "default"  # produces its normal character — available for tmux
                else:
                    status = "remapped"  # produces something else — annotate it

            layer_keys[grid_key] = {
                "status": status,
                "resolved": resolved,
                "default": default_resolved,
                "mod": mod_info,
                "raw": kc,
            }
        layers_data.append(layer_keys)

    return {
        "keyboard": keyboard_name,
        "keymap": keymap.get("keymap", ""),
        "layers": layers_data,
    }


# ---------------------------------------------------------------------------
# tmux binding parsing
# ---------------------------------------------------------------------------

CATEGORY_COLORS = {
    "nav": "#5dade2",
    "pane": "#58d68d",
    "window": "#f0b429",
    "session": "#bb8fce",
    "copy": "#ec7063",
    "misc": "#aab7b8",
    "vim": "#e67e22",
}


def categorize_command(cmd):
    cmd_lower = cmd.lower()
    if any(w in cmd_lower for w in ["select-pane", "split-window", "resize-pane", "swap-pane", "kill-pane"]):
        return "pane"
    if any(w in cmd_lower for w in ["select-window", "new-window", "kill-window", "next-window",
                                      "previous-window", "swap-window", "last-window", "rename-window"]):
        return "window"
    if any(w in cmd_lower for w in ["cursor", "scroll", "page", "search", "top", "bottom",
                                      "next-word", "previous-word", "end-of", "start-of",
                                      "history", "halfpage"]):
        return "nav"
    if any(w in cmd_lower for w in ["copy", "paste", "selection", "yank", "buffer",
                                      "begin-selection", "clear-selection"]):
        return "copy"
    if any(w in cmd_lower for w in ["session", "detach", "client", "switch-client", "suspend"]):
        return "session"
    return "misc"


def parse_bindings(table=None):
    try:
        result = subprocess.run(
            ["tmux", "list-keys"] + (["-T", table] if table else []),
            capture_output=True, text=True, check=True
        )
        lines = result.stdout.strip().split("\n")
    except (FileNotFoundError, subprocess.CalledProcessError) as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

    bindings = {}
    for line in lines:
        if not line.strip():
            continue
        m = re.match(r'bind-key\s+(?:-r\s+)?-T\s+(\S+)\s+(\S+)\s+(.*)', line)
        if m:
            tbl, key, cmd = m.group(1), m.group(2), m.group(3)
            if tbl not in bindings:
                bindings[tbl] = {}
            bindings[tbl][key] = cmd.strip()
    return bindings


def build_table_data(all_bindings, tables):
    """Bucket bindings by base key and modifier combination.

    Each entry is stored as binds[base_key][mods_str] where mods_str is the
    canonical ordering of the active modifiers, e.g. "", "S", "C", "M", "SC", "CM"...
    This lets the UI toggle Shift/Ctrl/Alt independently and hit any combination.
    """
    table_data = {}
    for tbl in tables:
        binds = {}
        for tmux_key, cmd in all_bindings[tbl].items():
            cat = categorize_command(cmd)
            entry = {"cmd": cmd, "cat": cat}
            base = tmux_key
            mods = set()
            if "-" in base:
                parts = base.split("-")
                while parts and len(parts[0]) == 1 and parts[0] in ("S", "C", "M"):
                    mods.add(parts.pop(0))
                base = "-".join(parts)
            elif len(base) == 1 and base.isupper():
                base = base.lower()
                mods.add("S")
            mods_str = "".join(m for m in "SCM" if m in mods)
            binds.setdefault(base, {})[mods_str] = entry
        table_data[tbl] = {"binds": binds}
    return table_data


# ---------------------------------------------------------------------------
# Vim command handling
# ---------------------------------------------------------------------------

VIM_BASE_ALIASES = {
    " ": "Space",
    "Esc": "Escape", "ESC": "Escape",
    "BS": "BSpace", "Del": "Delete",
    "PageUp": "PgUp", "PageDown": "PgDn",
    "Tab": "Tab", "CR": "Enter",
    "Home": "Home", "End": "End",
    "Up": "Up", "Down": "Down", "Left": "Left", "Right": "Right",
}


def normalize_vim_first(fk):
    """Normalize a command's 'first' key to a grid key name."""
    if not fk:
        return None
    base = fk["base"]
    mods = {m for m in "SCM" if m in fk.get("mods", [])}
    if base in VIM_BASE_ALIASES:
        base = VIM_BASE_ALIASES[base]
    elif len(base) == 1 and base.isalpha() and base.isupper():
        mods.add("S")
        base = base.lower()
    elif len(base) != 1:
        # Multi-char keys that aren't in aliases (e.g. "Plug", "F1"-"F12")
        if base.startswith("F") and base[1:].isdigit():
            pass  # F-keys are valid
        else:
            return None
    return {"base": base, "mods_str": "".join(m for m in "SCM" if m in mods)}


def merge_vim_cmds(base_data, overlay_data):
    """Merge a custom-mapping overlay on top of the base vim command list."""
    modes = {}
    order = []
    for data in (base_data, overlay_data):
        if not data:
            continue
        for i, mode in enumerate(data["modes"]):
            mid = mode["id"]
            if mid not in modes:
                modes[mid] = {"label": mode["label"], "cells": {}}
                order.append(mid)
            for c in mode["commands"]:
                fk = normalize_vim_first(c.get("first"))
                if not fk:
                    continue
                key = (fk["base"], fk["mods_str"])
                source = "base" if data is base_data else "overlay"
                cells = modes[mid]["cells"]
                cells.setdefault(key, {"base": [], "overlay": []})[source].append(c)

    merged_modes = []
    for mid in order:
        commands = []
        for cell in modes[mid]["cells"].values():
            commands.extend(cell["overlay"] if cell["overlay"] else cell["base"])
        merged_modes.append({"id": mid, "label": modes[mid]["label"], "commands": commands})
    return {"modes": merged_modes}


def build_vim_modes(data):
    """Bucket vim commands by (first key, modifier combo) for grid rendering."""
    grid_keys = full_layout_tmux_names()
    modes = []
    for mode in data["modes"]:
        binds = {}
        for c in mode["commands"]:
            fk = normalize_vim_first(c.get("first"))
            if not fk:
                continue
            base = fk["base"]
            if base not in grid_keys:
                continue
            mods_str = fk["mods_str"]
            binds.setdefault(base, {}).setdefault(mods_str, []).append(c.get("desc", ""))
        out_binds = {}
        for base, modmap in binds.items():
            out_binds[base] = {}
            for mods_str, descs in modmap.items():
                out_binds[base][mods_str] = {
                    "cmd": descs[0] if len(descs) == 1 else f"{len(descs)} commands",
                    "cat": "vim",
                    "cmds": descs,
                }
        if out_binds:
            modes.append({"id": mode["id"], "label": mode["label"], "binds": out_binds})
    return modes


def load_vim_cmds(path, overlay_path=None):
    base = None
    if path and os.path.exists(path):
        with open(path, encoding="utf-8") as f:
            base = json.load(f)
    if overlay_path:
        if not os.path.exists(overlay_path):
            print(f"Warning: vim overlay file not found: {overlay_path}", file=sys.stderr)
        else:
            with open(overlay_path, encoding="utf-8") as f:
                overlay = json.load(f)
            base = merge_vim_cmds(base or {"modes": []}, overlay)
    if not base:
        return []
    return build_vim_modes(base)


# ---------------------------------------------------------------------------
# HTML generation
# ---------------------------------------------------------------------------

def generate_html(all_bindings, output_path, qmk_data=None, vim_modes=None):
    preferred_order = ["root", "prefix", "copy-mode-vi", "copy-mode"]
    tables = [t for t in preferred_order if t in all_bindings]
    tables += sorted(t for t in all_bindings if t not in preferred_order)

    tmux_tables = list(tables)
    table_data = build_table_data(all_bindings, tmux_tables)
    tab_labels = {t: f"tmux: {t}" for t in tmux_tables}
    vim_tables = []
    if vim_modes:
        for vm in vim_modes:
            name = f"vim-{vm['id']}"
            table_data[name] = {"binds": vm["binds"]}
            tables.append(name)
            vim_tables.append(name)
            tab_labels[name] = f"vim: {vm['label']}"
    binding_json = json.dumps(table_data)
    qmk_json = json.dumps(qmk_data) if qmk_data else "null"

    # Build the keyboard HTML (shared across all layers)
    keyboard_html = _build_keyboard_html()

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>tmux keybindings</title>
<style>
* {{ margin: 0; padding: 0; box-sizing: border-box; }}
body {{
    background: #1a1a2e;
    color: #e0e0e0;
    font-family: 'JetBrains Mono', 'Fira Code', 'SF Mono', monospace;
    padding: 24px;
    min-height: 100vh;
}}
h1 {{
    font-size: 1.4em;
    margin-bottom: 16px;
    color: #fff;
}}
.controls {{
    display: flex;
    flex-direction: column;
    align-items: flex-start;
    gap: 10px;
    margin-bottom: 20px;
}}
.control-group {{
    display: flex;
    gap: 4px;
    align-items: center;
    flex-wrap: wrap;
}}
.control-label {{
    font-size: 0.8em;
    color: #888;
    margin-right: 4px;
}}
.tabs {{
    display: flex;
    gap: 4px;
    flex-wrap: wrap;
}}
.tab {{
    padding: 8px 16px;
    background: #16213e;
    border: 1px solid #333;
    border-radius: 6px;
    cursor: pointer;
    font-size: 0.85em;
    transition: all 0.15s;
}}
.tab:hover {{ background: #1f3460; }}
.tab.active {{
    background: #0f3460;
    border-color: #5dade2;
    color: #5dade2;
}}
.mod-toggle {{
    padding: 6px 12px;
    background: #16213e;
    border: 1px solid #333;
    border-radius: 4px;
    color: #ccc;
    cursor: pointer;
    font-size: 0.8em;
    font-family: inherit;
    transition: all 0.15s;
}}
.mod-toggle:hover {{ background: #1f3460; }}
.mod-toggle.active {{
    background: #1a3a5c;
    border-color: #5dade2;
    color: #5dade2;
}}
.qmk-toggle {{
    padding: 6px 12px;
    background: #16213e;
    border: 1px solid #333;
    border-radius: 4px;
    color: #ccc;
    cursor: pointer;
    font-size: 0.8em;
    font-family: inherit;
    transition: all 0.15s;
}}
.qmk-toggle:hover {{ background: #1f3460; }}
.qmk-toggle.active {{
    background: #2d1a3a;
    border-color: #bb8fce;
    color: #bb8fce;
}}
.layer {{ display: none; }}
.layer.active {{ display: block; }}
.keyboard {{
    position: relative;
    margin-bottom: 20px;
}}
.key {{
    position: absolute;
    border-radius: 5px;
    border: 1px solid #333;
    background: #16213e;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    font-size: 0.7em;
    cursor: default;
    transition: all 0.15s;
    overflow: hidden;
}}
.key .label {{
    font-weight: 600;
    font-size: 1.1em;
    line-height: 1.2;
    white-space: pre;
    text-align: center;
}}
.key .cmd {{
    font-size: 0.75em;
    opacity: 0.7;
    max-width: 95%;
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
    margin-top: 2px;
}}
.key .qmk-label {{
    position: absolute;
    top: 2px;
    right: 4px;
    font-size: 0.6em;
    opacity: 0.6;
    color: #bb8fce;
}}
.key.bound {{
    border-width: 2px;
    cursor: pointer;
}}
.key.bound:hover {{
    transform: translateY(-2px);
    box-shadow: 0 4px 12px rgba(0,0,0,0.4);
    z-index: 10;
}}
.key.qmk-default {{
    box-shadow: inset 0 0 0 2px rgba(88, 214, 141, 0.3);
}}
.key.qmk-remapped {{
    background: #2a1a1a;
    border-color: #c0392b;
}}
.key.qmk-remapped .qmk-label {{
    color: #e74c3c;
    font-weight: 600;
    opacity: 0.9;
}}
.key.qmk-transparent {{
    box-shadow: inset 0 0 0 2px rgba(88, 214, 141, 0.2);
    background: #16213e;
}}
.key.qmk-blocked {{
    background: #1a0a0a;
    opacity: 0.3;
}}
.key.qmk-layer {{
    background: #1a1a2a;
    border-color: #666;
}}
.legend {{
    display: flex;
    gap: 16px;
    margin-top: 20px;
    padding-top: 16px;
    border-top: 1px solid #333;
    flex-wrap: wrap;
}}
.legend-item {{
    display: flex;
    align-items: center;
    gap: 6px;
    font-size: 0.82em;
}}
.legend-dot {{
    width: 12px;
    height: 12px;
    border-radius: 3px;
}}
.popup {{
    display: none;
    position: absolute;
    background: #0f1a2e;
    border: 2px solid #5dade2;
    border-radius: 8px;
    padding: 16px 20px;
    z-index: 1000;
    min-width: 250px;
    max-width: 420px;
    box-shadow: 0 6px 24px rgba(0,0,0,0.7);
}}
.popup.visible {{ display: block; }}
.popup .popup-key {{
    font-size: 1.4em;
    font-weight: 700;
    margin-bottom: 8px;
}}
.popup .popup-cmd {{
    font-size: 1em;
    font-family: monospace;
    background: #1a1a2e;
    border-radius: 4px;
    padding: 10px 14px;
    margin-top: 8px;
    word-break: break-all;
    white-space: pre-wrap;
    line-height: 1.5;
}}
.popup .popup-cat {{
    display: inline-block;
    font-size: 0.8em;
    padding: 2px 8px;
    border-radius: 4px;
    margin-top: 10px;
    opacity: 0.8;
}}
.popup .popup-qmk {{
    font-size: 0.85em;
    margin-top: 8px;
    padding-top: 8px;
    border-top: 1px solid #333;
    color: #bb8fce;
    white-space: pre-wrap;
}}
.popup .popup-close {{
    position: absolute;
    top: 10px;
    right: 14px;
    cursor: pointer;
    font-size: 1.2em;
    color: #888;
    transition: color 0.15s;
}}
.popup .popup-close:hover {{ color: #fff; }}
.cat-nav {{ border-color: {CATEGORY_COLORS['nav']}; color: {CATEGORY_COLORS['nav']}; }}
.cat-pane {{ border-color: {CATEGORY_COLORS['pane']}; color: {CATEGORY_COLORS['pane']}; }}
.cat-window {{ border-color: {CATEGORY_COLORS['window']}; color: {CATEGORY_COLORS['window']}; }}
.cat-session {{ border-color: {CATEGORY_COLORS['session']}; color: {CATEGORY_COLORS['session']}; }}
.cat-copy {{ border-color: {CATEGORY_COLORS['copy']}; color: {CATEGORY_COLORS['copy']}; }}
.cat-misc {{ border-color: {CATEGORY_COLORS['misc']}; color: {CATEGORY_COLORS['misc']}; }}
.cat-vim {{ border-color: {CATEGORY_COLORS['vim']}; color: {CATEGORY_COLORS['vim']}; }}
</style>
</head>
<body>
<h1>tmux keybindings</h1>
<div class="controls">
  <div class="control-group">
    <div class="tabs">
"""

    for i, tbl in enumerate(tmux_tables):
        active = "active" if i == 0 else ""
        html += f'      <div class="tab {active}" data-table="{tbl}" onclick="switchTab(\'{tbl}\')">{escape(tab_labels[tbl])}</div>\n'

    html += """    </div>
  </div>
"""

    if vim_tables:
        html += '  <div class="control-group">\n'
        html += '    <div class="tabs">\n'
        for tbl in vim_tables:
            html += f'      <div class="tab" data-table="{tbl}" onclick="switchTab(\'{tbl}\')">{escape(tab_labels[tbl])}</div>\n'
        html += '    </div>\n  </div>\n'

    html += '  <div class="control-group">\n'
    html += '    <span class="control-label">Modifiers (toggle):</span>\n'
    html += '    <button class="mod-toggle" data-mod="shift" onclick="toggleMod(\'shift\')">Shift</button>\n'
    html += '    <button class="mod-toggle" data-mod="ctrl" onclick="toggleMod(\'ctrl\')">Ctrl</button>\n'
    html += '    <button class="mod-toggle" data-mod="alt" onclick="toggleMod(\'alt\')">Alt</button>\n'

    if qmk_data:
        html += '    <span class="control-label" style="margin-left:16px;">QMK Layer (60% only):</span>\n'
        html += '    <button class="qmk-toggle active" data-qmk="-1" onclick="setQmkLayer(-1)">Off</button>\n'
        for i in range(len(qmk_data["layers"])):
            html += f'    <button class="qmk-toggle" data-qmk="{i}" onclick="setQmkLayer({i})">L{i}</button>\n'

    html += '  </div>\n</div>\n'

    # Generate a layer div for each table (all share the same keyboard structure)
    for i, tbl in enumerate(tables):
        active = "active" if i == 0 else ""
        html += f'<div class="layer {active}" id="layer-{tbl}">\n'
        html += keyboard_html
        html += '</div>\n'

    # Legend
    html += '<div class="legend">\n'
    for cat, color in CATEGORY_COLORS.items():
        html += (f'  <div class="legend-item">'
                f'<div class="legend-dot" style="background:{color}"></div>'
                f'{cat}</div>\n')
    if qmk_data:
        html += '  <div class="legend-item"><div class="legend-dot" style="background:#58d68d;opacity:0.4"></div>available (default/transparent)</div>\n'
        html += '  <div class="legend-item"><div class="legend-dot" style="background:#c0392b"></div>remapped (sends different key)</div>\n'
        html += '  <div class="legend-item"><div class="legend-dot" style="background:#1a0a0a;border:1px solid #333"></div>blocked (KC_NO)</div>\n'
    html += '</div>\n'

    # Popup and JS
    html += """
<div class="popup" id="popup">
  <span class="popup-close" onclick="hidePopup()">&times;</span>
  <div class="popup-key" id="popup-key"></div>
  <div class="popup-cmd" id="popup-cmd"></div>
  <div class="popup-cat" id="popup-cat"></div>
  <div class="popup-qmk" id="popup-qmk"></div>
</div>

<script>
const bindingData = """ + binding_json + """;
const qmkData = """ + qmk_json + """;
const catColors = """ + json.dumps(CATEGORY_COLORS) + """;
const catLabels = {nav:'navigation', pane:'pane', window:'window', session:'session', copy:'copy', misc:'other', vim:'vim'};

let currentTable = '""" + tables[0] + """';
let currentMods = {shift: false, ctrl: false, alt: false};
let currentQmkLayer = -1;

function activeModString() {
    return (currentMods.shift ? 'S' : '') + (currentMods.ctrl ? 'C' : '') + (currentMods.alt ? 'M' : '');
}

function activeModPrefix() {
    return activeModString().split('').map(c => c + '-').join('');
}

function switchTab(name) {
    document.querySelectorAll('.tab').forEach(t => t.classList.remove('active'));
    document.querySelectorAll('.layer').forEach(l => l.classList.remove('active'));
    document.querySelector(`[data-table="${name}"]`).classList.add('active');
    document.getElementById(`layer-${name}`).classList.add('active');
    currentTable = name;
    renderKeys();
    hidePopup();
}

function toggleMod(mod) {
    currentMods[mod] = !currentMods[mod];
    document.querySelector(`[data-mod="${mod}"]`).classList.toggle('active', currentMods[mod]);
    renderKeys();
    hidePopup();
}

function setQmkLayer(idx) {
    document.querySelectorAll('.qmk-toggle').forEach(b => b.classList.remove('active'));
    document.querySelector(`[data-qmk="${idx}"]`).classList.add('active');
    currentQmkLayer = idx;
    renderKeys();
    hidePopup();
}

function renderKeys() {
    const data = bindingData[currentTable];
    if (!data) return;
    const modsStr = activeModString();
    const binds = data.binds;
    const qmkLayer = (qmkData && currentQmkLayer >= 0) ? qmkData.layers[currentQmkLayer] : null;
    const activeLayer = document.querySelector('.layer.active');
    if (!activeLayer) return;

    activeLayer.querySelectorAll('.key').forEach(el => {
        const keyName = el.dataset.key;
        const cmdEl = el.querySelector('.cmd');
        const qmkEl = el.querySelector('.qmk-label');
        const entry = (binds[keyName] || {})[modsStr];

        // Reset classes
        el.className = 'key';
        el.onclick = null;
        cmdEl.textContent = '';
        qmkEl.textContent = '';

        // Apply QMK overlay (only affects 60% keys that exist in qmkLayer)
        let qmkInfo = null;
        if (qmkLayer && qmkLayer[keyName]) {
            qmkInfo = qmkLayer[keyName];
            if (qmkInfo.status === 'default') {
                el.classList.add('qmk-default');
            } else if (qmkInfo.status === 'remapped') {
                el.classList.add('qmk-remapped');
                qmkEl.textContent = qmkInfo.resolved || '';
            } else if (qmkInfo.status === 'transparent') {
                el.classList.add('qmk-transparent');
            } else if (qmkInfo.status === 'blocked') {
                el.classList.add('qmk-blocked');
            } else if (qmkInfo.status === 'layer') {
                el.classList.add('qmk-layer');
                qmkEl.textContent = qmkInfo.raw;
            }
            if (qmkInfo.mod && qmkInfo.status !== 'layer') {
                const existing = qmkEl.textContent;
                qmkEl.textContent = existing ? qmkInfo.mod + '/' + existing : qmkInfo.mod;
            }
        } else if (qmkLayer) {
            el.classList.add('qmk-default');
        }

        // Apply SW binding
        if (entry) {
            const cat = entry.cat;
            el.classList.add('bound', 'cat-' + cat);
            const maxLen = Math.max(4, Math.floor(el.offsetWidth / 7));
            cmdEl.textContent = entry.cmd.length > maxLen
                ? entry.cmd.substring(0, maxLen - 1) + '\\u2026'
                : entry.cmd;
            el.onclick = function() {{ showPopup(el, keyName, entry, qmkInfo); }};
        } else if (qmkInfo) {
            el.onclick = function() {{ showPopup(el, keyName, null, qmkInfo); }};
            el.style.cursor = 'pointer';
        }
    });
}

function showPopup(el, key, entry, qmkInfo) {
    const popup = document.getElementById('popup');
    document.getElementById('popup-key').textContent = activeModPrefix() + key;

    const cmdEl = document.getElementById('popup-cmd');
    const catEl = document.getElementById('popup-cat');
    const qmkEl = document.getElementById('popup-qmk');

    const cmd = entry ? (entry.cmds && entry.cmds.length > 1 ? entry.cmds.join('\\n') : entry.cmd) : null;
    const cat = entry ? entry.cat : null;

    if (cmd) {
        cmdEl.textContent = cmd;
        cmdEl.style.display = '';
        catEl.textContent = catLabels[cat] || cat;
        catEl.style.background = catColors[cat] + '33';
        catEl.style.color = catColors[cat];
        catEl.style.display = '';
    } else {
        cmdEl.style.display = 'none';
        catEl.style.display = 'none';
    }

    if (qmkInfo) {
        let qmkText = 'QMK: ' + qmkInfo.raw;
        if (qmkInfo.status === 'default') {
            qmkText += '\\n(standard \\u2014 available for tmux)';
        } else if (qmkInfo.status === 'remapped') {
            qmkText += '\\nResolves to: ' + (qmkInfo.resolved || '?');
            if (qmkInfo.default) qmkText += ' (normally: ' + qmkInfo.default + ')';
        } else if (qmkInfo.status === 'transparent') {
            qmkText += '\\n(transparent \\u2014 falls through)';
        } else if (qmkInfo.status === 'blocked') {
            qmkText += '\\n(disabled \\u2014 no output)';
        } else if (qmkInfo.status === 'layer') {
            qmkText += '\\n(layer switch)';
        }
        if (qmkInfo.mod) qmkText += '\\nHold: ' + qmkInfo.mod;
        qmkEl.textContent = qmkText;
        qmkEl.style.display = '';
    } else {
        qmkEl.style.display = 'none';
    }

    const rect = el.getBoundingClientRect();
    popup.classList.add('visible');
    const popupRect = popup.getBoundingClientRect();
    let left = rect.left + window.scrollX + rect.width / 2 - popupRect.width / 2;
    const minLeft = 8;
    const maxLeft = window.innerWidth - popupRect.width - 8;
    left = Math.max(minLeft, Math.min(left, maxLeft));
    popup.style.top = (rect.bottom + window.scrollY + 8) + 'px';
    popup.style.left = left + 'px';
}

function hidePopup() {
    document.getElementById('popup').classList.remove('visible');
}

document.addEventListener('keydown', function(e) {
    if (e.key === 'Escape') hidePopup();
});
document.addEventListener('click', function(e) {
    const popup = document.getElementById('popup');
    if (!popup.contains(e.target) && !e.target.closest('.key')) {
        hidePopup();
    }
});

// Initial render
renderKeys();
</script>
</body>
</html>
"""

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html)
    return output_path


# ---------------------------------------------------------------------------
# Keyboard HTML builder
# ---------------------------------------------------------------------------

UNIT = 52   # pixels per key unit
GAP = 4     # visual gap between adjacent keys (baked into width calc)


def _compute_layout():
    """Compute absolute (x, y, w) in pixels for every key in FULL_ROWS.

    Uses the formula: a key at unit-position x with width w units occupies
    pixels [x*UNIT, (x+w)*UNIT) with a GAP-pixel inset on each side.
    This guarantees perfect alignment regardless of key grouping.
    """
    keys = []  # list of (label, tmux_name, x_px, y_px, w_px, h_px)
    for row_idx, row in enumerate(FULL_ROWS):
        x_units = 0.0
        for item in row:
            if item[0] == "gap":
                x_units += item[1]
            else:
                _, label, tmux_name, width = item
                x_px = int(x_units * UNIT)
                y_px = int(row_idx * UNIT)
                w_px = int(width * UNIT) - GAP
                h_px = UNIT - GAP
                keys.append((label, tmux_name, x_px, y_px, w_px, h_px))
                x_units += width
    return keys


def _layout_bounds(keys):
    """Return (total_width, total_height) in pixels for the layout."""
    max_x = max(k[2] + k[4] + GAP for k in keys)
    max_y = max(k[3] + k[5] + GAP for k in keys)
    return max_x, max_y


def _build_keyboard_html():
    """Build the shared keyboard grid HTML using absolute positioning."""
    keys = _compute_layout()
    total_w, total_h = _layout_bounds(keys)

    html = f'  <div class="keyboard" style="width:{total_w}px;height:{total_h}px">\n'
    for label, tmux_name, x, y, w, h in keys:
        label_escaped = escape(label)
        html += (f'    <div class="key" data-key="{escape(tmux_name)}" '
                 f'style="left:{x}px;top:{y}px;width:{w}px;height:{h}px">'
                 f'<span class="label">{label_escaped}</span>'
                 f'<span class="cmd"></span>'
                 f'<span class="qmk-label"></span></div>\n')
    html += '  </div>\n'
    return html


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    import argparse
    parser = argparse.ArgumentParser(description="Generate tmux keybinding HTML visualizer")
    script_dir = os.path.dirname(os.path.abspath(sys.argv[0]))
    parser.add_argument("output", nargs="?", default=os.path.expanduser("~/tmux-keys.html"),
                       help="Output HTML file path")
    parser.add_argument("-k", "--keymap", help="Path to QMK keymap.json for overlay")
    parser.add_argument("--vim-cmds",
                       default=os.path.normpath(os.path.join(script_dir, "..", "vim_cmds.json")),
                       help="Path to parsed vim commands JSON (default: ../vim_cmds.json)")
    parser.add_argument("--vim-cmds-overlay",
                       default=os.path.normpath(os.path.join(script_dir, "..", "keymap-overlay.json")),
                       help="Custom mapping dump to overlay on the base vim commands "
                            "(default: ../keymap-overlay.json)")
    default_qmk = os.path.normpath(os.path.join(script_dir, "..", "..", "qmk_firmware"))
    parser.add_argument("--qmk-firmware", default=default_qmk,
                       help=f"Path to qmk_firmware repo (default: {default_qmk})")
    args = parser.parse_args()

    qmk_fw = args.qmk_firmware if os.path.isdir(args.qmk_firmware) else None

    all_bindings = parse_bindings()
    if not all_bindings:
        print("No tmux bindings found. Is tmux running?")
        sys.exit(1)

    qmk_data = None
    if args.keymap:
        qmk_data = load_qmk_keymap(args.keymap, qmk_firmware_path=qmk_fw)
        if qmk_data:
            print(f"Loaded QMK keymap: {qmk_data['keymap']} ({len(qmk_data['layers'])} layers)")

    vim_modes = load_vim_cmds(args.vim_cmds, args.vim_cmds_overlay)
    if vim_modes:
        overlay_note = f" (overlay: {args.vim_cmds_overlay})" if args.vim_cmds_overlay else ""
        print(f"Loaded vim commands{overlay_note}: {', '.join(m['label'] for m in vim_modes)}")

    path = generate_html(all_bindings, args.output, qmk_data, vim_modes)
    print(f"Written to: {path}")
    print(f"Open with: xdg-open {path}")


if __name__ == "__main__":
    main()
