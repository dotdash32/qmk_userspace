#!/usr/bin/env python3
"""Generate an interactive HTML keyboard layout for tmux keybindings with click popups,
modifier toggles, and QMK keymap overlay to show which keys are still available."""

import subprocess
import sys
import re
import os
import json
from html import escape

ROWS = [
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
     ("K", "k", 1), ("L", "l", 1), (";", "\\;", 1), ("'", "'", 1),
     ("Enter", "Enter", 1.75)],
    [("Shift", "Shift", 2.25), ("Z", "z", 1), ("X", "x", 1), ("C", "c", 1),
     ("V", "v", 1), ("B", "b", 1), ("N", "n", 1), ("M", "m", 1),
     (",", ",", 1), (".", ".", 1), ("/", "/", 1), ("Shift", "Shift", 2.25)],
    [("Ctrl", "C-", 1.5), ("Super", "Super", 1.25), ("Alt", "M-", 1.25),
     ("Space", "Space", 6), ("Alt", "M-", 1.25), ("Super", "Super", 1.25),
     ("Ctrl", "C-", 1.5)],
]

ARROW_ROW = [("←", "Left", 1), ("↓", "Down", 1), ("↑", "Up", 1), ("→", "Right", 1)]

CATEGORY_COLORS = {
    "nav": "#5dade2",
    "pane": "#58d68d",
    "window": "#f0b429",
    "session": "#bb8fce",
    "copy": "#ec7063",
    "misc": "#aab7b8",
}

# Map QMK keycodes to the tmux key name they'd produce
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
    "KC_BSLS": "\\", "KC_SCLN": "\\;", "KC_QUOT": "'", "KC_GRV": "`",
    "KC_COMM": ",", "KC_DOT": ".", "KC_SLSH": "/",
    "KC_SPC": "Space", "KC_ENT": "Enter", "KC_TAB": "Tab",
    "KC_BSPC": "BSpace", "KC_DEL": "Delete", "KC_ESC": "Escape",
    "KC_LEFT": "Left", "KC_RGHT": "Right", "KC_UP": "Up", "KC_DOWN": "Down",
    "KC_HOME": "Home", "KC_END": "End", "KC_PGUP": "PgUp", "KC_PGDN": "PgDn",
    "KC_INS": "Insert",
    "KC_F1": "F1", "KC_F2": "F2", "KC_F3": "F3", "KC_F4": "F4",
    "KC_F5": "F5", "KC_F6": "F6", "KC_F7": "F7", "KC_F8": "F8",
    "KC_F9": "F9", "KC_F10": "F10", "KC_F11": "F11", "KC_F12": "F12",
    "KC_PSCR": "PrtSc", "KC_VOLU": "VolUp", "KC_VOLD": "VolDn",
    "KC_MPLY": "MediaPlay", "KC_MPRV": "MediaPrev", "KC_MNXT": "MediaNext",
    "KC_PENT": "KPEnter", "KC_PWR": "Power",
    "KC_LCTL": "LCtrl", "KC_RCTL": "RCtrl", "KC_LSFT": "LShift",
    "KC_RSFT": "RShift", "KC_LALT": "LAlt", "KC_RALT": "RAlt",
    "KC_LGUI": "LGui", "KC_RGUI": "RGui", "KC_APP": "App",
    "KC_NO": None,
}

# The "default" keycode for each physical position index on a standard ANSI 60% layout.
# This is what the key would produce if unremapped — used to detect remaps.
# Index order matches LAYOUT_60_ansi_split_bs_rshift from info.json.
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

def qmk_position_to_grid_key(phys_layout):
    """Map QMK physical layout indices to our grid's tmux key names."""
    idx_to_key = {}
    for idx, pos in enumerate(phys_layout):
        x, y = pos["x"], pos["y"]
        row_idx = int(y)
        if row_idx >= len(ROWS):
            continue
        curr_x = 0.0
        for _, tmux_name, width in ROWS[row_idx]:
            if abs(curr_x - x) < 0.3:
                idx_to_key[idx] = tmux_name
                break
            curr_x += width
    return idx_to_key


def parse_qmk_keycode(kc):
    """Extract the base keycode and modifier info from QMK keycode."""
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
    table_data = {}
    for tbl in tables:
        layers = {"bare": {}, "shift": {}, "ctrl": {}, "alt": {}}
        other_mods = {}
        for tmux_key, cmd in all_bindings[tbl].items():
            cat = categorize_command(cmd)
            entry = {"cmd": cmd, "cat": cat}
            if tmux_key.startswith("C-M-") or tmux_key.startswith("M-C-"):
                other_mods[tmux_key] = entry
            elif tmux_key.startswith("C-"):
                base = tmux_key[2:]
                layers["ctrl"][base] = entry
            elif tmux_key.startswith("M-"):
                base = tmux_key[2:]
                layers["alt"][base] = entry
            elif tmux_key.startswith("S-"):
                base = tmux_key[2:]
                layers["shift"][base] = entry
            elif len(tmux_key) == 1 and tmux_key.isupper():
                layers["shift"][tmux_key.lower()] = entry
            else:
                layers["bare"][tmux_key] = entry
        table_data[tbl] = {"layers": layers, "other_mods": other_mods}
    return table_data


def generate_html(all_bindings, output_path, qmk_data=None):
    preferred_order = ["root", "prefix", "copy-mode-vi", "copy-mode"]
    tables = [t for t in preferred_order if t in all_bindings]
    tables += sorted(t for t in all_bindings if t not in preferred_order)

    table_data = build_table_data(all_bindings, tables)
    binding_json = json.dumps(table_data)
    qmk_json = json.dumps(qmk_data) if qmk_data else "null"

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
    gap: 24px;
    align-items: center;
    margin-bottom: 20px;
    flex-wrap: wrap;
}}
.control-group {{
    display: flex;
    gap: 4px;
    align-items: center;
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
    display: flex;
    flex-direction: column;
    gap: 4px;
    margin-bottom: 20px;
}}
.row {{
    display: flex;
    gap: 4px;
}}
.key {{
    position: relative;
    height: 54px;
    border-radius: 6px;
    border: 1px solid #333;
    background: #16213e;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    font-size: 0.75em;
    cursor: default;
    transition: all 0.15s;
    overflow: hidden;
}}
.key .label {{
    font-weight: 600;
    font-size: 1.1em;
}}
.key .cmd {{
    font-size: 0.8em;
    opacity: 0.7;
    max-width: 90%;
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
    margin-top: 2px;
}}
.key .qmk-label {{
    position: absolute;
    top: 2px;
    right: 4px;
    font-size: 0.65em;
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
    /* Key produces its normal character — fully available for tmux */
    box-shadow: inset 0 0 0 2px rgba(88, 214, 141, 0.3);
}}
.key.qmk-remapped {{
    /* Key produces something different — annotate what it sends */
    background: #2a1a1a;
    border-color: #c0392b;
}}
.key.qmk-remapped .qmk-label {{
    color: #e74c3c;
    font-weight: 600;
    opacity: 0.9;
}}
.key.qmk-transparent {{
    /* Falls through to lower layer — available */
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
.arrow-row {{
    display: flex;
    gap: 4px;
    margin-left: 200px;
    margin-top: 8px;
}}
.modifiers {{
    margin-top: 16px;
    columns: 2;
    column-gap: 32px;
}}
.mod-entry {{
    display: flex;
    align-items: center;
    gap: 8px;
    padding: 4px 8px;
    margin-bottom: 4px;
    border-radius: 4px;
    font-size: 0.82em;
    break-inside: avoid;
}}
.mod-entry:hover {{ background: #16213e; }}
.mod-key {{
    font-weight: 600;
    min-width: 80px;
}}
.mod-cmd {{
    opacity: 0.7;
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
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
</style>
</head>
<body>
<h1>tmux keybindings</h1>
<div class="controls">
  <div class="control-group">
    <span class="control-label">Table:</span>
    <div class="tabs">
"""

    for i, tbl in enumerate(tables):
        active = "active" if i == 0 else ""
        html += f'      <div class="tab {active}" data-table="{tbl}" onclick="switchTab(\'{tbl}\')">{escape(tbl)}</div>\n'

    html += """    </div>
  </div>
  <div class="control-group">
    <span class="control-label">Modifier:</span>
    <button class="mod-toggle active" data-mod="bare" onclick="setModLayer('bare')">None</button>
    <button class="mod-toggle" data-mod="shift" onclick="setModLayer('shift')">Shift</button>
    <button class="mod-toggle" data-mod="ctrl" onclick="setModLayer('ctrl')">Ctrl</button>
    <button class="mod-toggle" data-mod="alt" onclick="setModLayer('alt')">Alt</button>
  </div>
"""

    if qmk_data:
        html += '  <div class="control-group">\n'
        html += '    <span class="control-label">QMK Layer:</span>\n'
        html += '    <button class="qmk-toggle active" data-qmk="-1" onclick="setQmkLayer(-1)">Off</button>\n'
        for i in range(len(qmk_data["layers"])):
            html += f'    <button class="qmk-toggle" data-qmk="{i}" onclick="setQmkLayer({i})">L{i}</button>\n'
        html += '  </div>\n'

    html += '</div>\n'

    # Generate keyboard structure for each table
    for i, tbl in enumerate(tables):
        active = "active" if i == 0 else ""
        html += f'<div class="layer {active}" id="layer-{tbl}">\n'
        html += '  <div class="keyboard">\n'

        for row in ROWS:
            html += '    <div class="row">\n'
            for key_label, tmux_name, width in row:
                px_width = int(width * 54 + (width - 1) * 4)
                html += (f'      <div class="key" data-key="{escape(tmux_name)}" '
                        f'style="width:{px_width}px">'
                        f'<span class="label">{escape(key_label)}</span>'
                        f'<span class="cmd"></span>'
                        f'<span class="qmk-label"></span></div>\n')
            html += '    </div>\n'

        html += '    <div class="arrow-row">\n'
        for key_label, tmux_name, width in ARROW_ROW:
            html += (f'      <div class="key" data-key="{escape(tmux_name)}" '
                    f'style="width:54px">'
                    f'<span class="label">{escape(key_label)}</span>'
                    f'<span class="cmd"></span>'
                    f'<span class="qmk-label"></span></div>\n')
        html += '    </div>\n'
        html += '  </div>\n'

        # Other modifier combos
        data = table_data[tbl]
        if data["other_mods"]:
            html += '  <div class="modifiers">\n'
            html += '    <h3 style="font-size:0.9em;margin-bottom:8px;color:#888;">Other combos</h3>\n'
            for key in sorted(data["other_mods"].keys()):
                entry = data["other_mods"][key]
                html += (f'    <div class="mod-entry">'
                        f'<span class="mod-key cat-{entry["cat"]}">{escape(key)}</span>'
                        f'<span class="mod-cmd">{escape(entry["cmd"])}</span></div>\n')
            html += '  </div>\n'

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
const catLabels = {nav:'navigation', pane:'pane', window:'window', session:'session', copy:'copy', misc:'other'};

let currentTable = '""" + tables[0] + """';
let currentMod = 'bare';
let currentQmkLayer = -1;

function switchTab(name) {
    document.querySelectorAll('.tab').forEach(t => t.classList.remove('active'));
    document.querySelectorAll('.layer').forEach(l => l.classList.remove('active'));
    document.querySelector(`[data-table="${name}"]`).classList.add('active');
    document.getElementById(`layer-${name}`).classList.add('active');
    currentTable = name;
    renderKeys();
    hidePopup();
}

function setModLayer(mod) {
    document.querySelectorAll('.mod-toggle').forEach(b => b.classList.remove('active'));
    document.querySelector(`[data-mod="${mod}"]`).classList.add('active');
    currentMod = mod;
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
    const layer = data.layers[currentMod] || {};
    const qmkLayer = (qmkData && currentQmkLayer >= 0) ? qmkData.layers[currentQmkLayer] : null;
    const activeLayer = document.querySelector('.layer.active');
    if (!activeLayer) return;

    activeLayer.querySelectorAll('.key').forEach(el => {
        const keyName = el.dataset.key;
        const cmdEl = el.querySelector('.cmd');
        const qmkEl = el.querySelector('.qmk-label');
        const entry = layer[keyName];

        // Reset classes
        el.className = 'key';
        el.onclick = null;
        cmdEl.textContent = '';
        qmkEl.textContent = '';

        // Apply QMK overlay
        let qmkInfo = null;
        if (qmkLayer && qmkLayer[keyName]) {
            qmkInfo = qmkLayer[keyName];
            if (qmkInfo.status === 'default') {
                // Key produces its normal char — available for tmux
                el.classList.add('qmk-default');
            } else if (qmkInfo.status === 'remapped') {
                // Key produces something different — show what it resolves to
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
            // Show mod-tap info if present
            if (qmkInfo.mod && qmkInfo.status !== 'layer') {
                const existing = qmkEl.textContent;
                qmkEl.textContent = existing ? qmkInfo.mod + '/' + existing : qmkInfo.mod;
            }
        } else if (qmkLayer) {
            el.classList.add('qmk-default');
        }

        // Apply tmux binding
        if (entry) {
            const cat = entry.cat;
            el.classList.add('bound', 'cat-' + cat);
            const maxLen = Math.max(6, Math.floor(el.offsetWidth / 7));
            cmdEl.textContent = entry.cmd.length > maxLen
                ? entry.cmd.substring(0, maxLen - 1) + '…'
                : entry.cmd;
            el.onclick = function() { showPopup(el, keyName, entry.cmd, cat, qmkInfo); };
        } else if (qmkInfo) {
            el.onclick = function() { showPopup(el, keyName, null, null, qmkInfo); };
            el.style.cursor = 'pointer';
        }
    });
}

function showPopup(el, key, cmd, cat, qmkInfo) {
    const popup = document.getElementById('popup');
    const prefix = currentMod === 'bare' ? '' :
                   currentMod === 'shift' ? 'S-' :
                   currentMod === 'ctrl' ? 'C-' : 'M-';
    document.getElementById('popup-key').textContent = prefix + key;

    const cmdEl = document.getElementById('popup-cmd');
    const catEl = document.getElementById('popup-cat');
    const qmkEl = document.getElementById('popup-qmk');

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
            qmkText += ' (standard — available for tmux)';
        } else if (qmkInfo.status === 'remapped') {
            qmkText += '\\nResolves to: ' + (qmkInfo.resolved || '?');
            if (qmkInfo.default) qmkText += ' (normally: ' + qmkInfo.default + ')';
        } else if (qmkInfo.status === 'transparent') {
            qmkText += ' (transparent — falls through, available for tmux)';
        } else if (qmkInfo.status === 'blocked') {
            qmkText += ' (disabled — no output)';
        } else if (qmkInfo.status === 'layer') {
            qmkText += ' (layer switch)';
        }
        if (qmkInfo.mod) qmkText += '\\nHold: ' + qmkInfo.mod;
        qmkEl.textContent = qmkText;
        qmkEl.style.display = '';
    } else {
        qmkEl.style.display = 'none';
    }

    // Position below the clicked key, clamped to viewport
    const rect = el.getBoundingClientRect();
    popup.style.transform = '';
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


def main():
    import argparse
    parser = argparse.ArgumentParser(description="Generate tmux keybinding HTML visualizer")
    parser.add_argument("output", nargs="?", default=os.path.expanduser("~/tmux-keys.html"),
                       help="Output HTML file path")
    parser.add_argument("-k", "--keymap", help="Path to QMK keymap.json for overlay")
    script_dir = os.path.dirname(os.path.abspath(sys.argv[0]))
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

    path = generate_html(all_bindings, args.output, qmk_data)
    print(f"Written to: {path}")
    print(f"Open with: xdg-open {path}")


if __name__ == "__main__":
    main()
