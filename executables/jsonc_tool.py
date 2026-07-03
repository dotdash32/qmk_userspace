#!/usr/bin/env python3
"""
Tool to strip and re-apply // comments in JSONC keymap files.

Comments are saved to a .comments.json sidecar file. Each comment is anchored
by its line content and occurrence index in the clean output, so comments
land on the correct line after reformatting.

Workflow:
    1. Edit keymap.json with // comments locally
    2. Run `python jsonc_tool.py strip` before uploading to QMK Configurator
    3. Download the modified file from the configurator
    4. Run `python jsonc_tool.py apply` to restore your comments
"""

import argparse
import json
import sys
from pathlib import Path

USERSPACE_ROOT = Path(__file__).resolve().parent.parent


def resolve_keymap_file(args):
    """Resolve keymap.json path from -kb/-km args or direct file path."""
    if args.file:
        return Path(args.file)
    if args.keyboard and args.keymap:
        path = USERSPACE_ROOT / "keyboards" / args.keyboard / "keymaps" / args.keymap / "keymap.json"
        if not path.exists():
            print(f"Error: keymap not found at {path}", file=sys.stderr)
            sys.exit(1)
        return path
    if args.keyboard or args.keymap:
        print("Error: both -kb and -km are required when not specifying a file path", file=sys.stderr)
        sys.exit(1)
    # Default fallback
    return Path("keymap.json")


def _find_comment_pos(line):
    """Find position of // comment, ignoring those inside string literals."""
    in_string = False
    escape_next = False
    for i, ch in enumerate(line):
        if escape_next:
            escape_next = False
            continue
        if ch == '\\' and in_string:
            escape_next = True
            continue
        if ch == '"':
            in_string = not in_string
        elif ch == '/' and not in_string and i + 1 < len(line) and line[i + 1] == '/':
            return i
    return None


def _strip_to_lines(text):
    """Strip comments and return list of cleaned lines (preserving structure)."""
    lines = text.split("\n")
    result = []
    for line in lines:
        comment_pos = _find_comment_pos(line)
        if comment_pos is not None:
            cleaned = line[:comment_pos].rstrip()
            if cleaned.strip():
                result.append(cleaned)
        else:
            result.append(line)
    return result


def parse_comments(text):
    """Extract comments, computing their occurrence index in the clean output."""
    lines = text.split("\n")

    # First, produce the clean JSON and reformat it to know the target layout
    clean_text = "\n".join(_strip_to_lines(text))
    parsed = json.loads(clean_text)
    formatted = json.dumps(parsed, indent=2)
    formatted_lines = formatted.split("\n")

    # Build occurrence map for the formatted output
    formatted_occurrences = {}
    for fline in formatted_lines:
        stripped = fline.strip()
        formatted_occurrences[stripped] = formatted_occurrences.get(stripped, 0) + 1

    # Now scan original, tracking which formatted-line occurrence each comment maps to
    # Strategy: strip comments from original, reformat, then find where each
    # commented line lands by matching content.

    # Map: for each line in original that has a comment, find its position
    # in the formatted output by matching the code content and counting.
    comments = []
    # Count how many times we've seen each stripped content in the original
    # (only counting lines that survive stripping)
    orig_content_seen = {}

    for lineno, line in enumerate(lines):
        comment_pos = _find_comment_pos(line)

        if comment_pos is None:
            # No comment - just track this line's content for occurrence counting
            stripped = line.strip()
            if stripped:
                orig_content_seen[stripped] = orig_content_seen.get(stripped, 0) + 1
            continue

        comment_text = line[comment_pos + 2:]
        code = line[:comment_pos].rstrip()
        has_code = bool(code.strip())

        if has_code:
            anchor = code.strip()
            occ = orig_content_seen.get(anchor, 0)
            orig_content_seen[anchor] = occ + 1
            comments.append({
                "type": "inline",
                "anchor": anchor,
                "occurrence": occ,
                "text": comment_text,
            })
        else:
            # Standalone: anchor to next non-comment code line
            next_code = ""
            temp_seen = dict(orig_content_seen)
            for future_line in lines[lineno + 1:]:
                fp = _find_comment_pos(future_line)
                if fp is not None:
                    candidate = future_line[:fp].strip()
                else:
                    candidate = future_line.strip()
                if candidate:
                    next_code = candidate
                    break
            occ = orig_content_seen.get(next_code, 0)
            comments.append({
                "type": "standalone",
                "anchor": next_code,
                "occurrence": occ,
                "text": comment_text,
                "indent": len(line) - len(line.lstrip()),
            })

    return comments


def apply_comments(json_text, comments):
    """Re-apply saved comments to clean JSON text."""
    lines = json_text.split("\n")

    # Index comments by (type, anchor, occurrence)
    comment_map = {}
    for c in comments:
        key = (c["type"], c["anchor"], c["occurrence"])
        comment_map[key] = c

    # Count occurrences of each line content as we scan
    occurrence_counter = {}
    result = []

    for line in lines:
        stripped = line.strip()
        occ = occurrence_counter.get(stripped, 0)

        # Check for standalone comments anchored to this line
        key = ("standalone", stripped, occ)
        if key in comment_map:
            c = comment_map[key]
            indent = c.get("indent", len(line) - len(line.lstrip()))
            result.append(" " * indent + "//" + c["text"])

        # Check for inline comment
        key = ("inline", stripped, occ)
        if key in comment_map:
            c = comment_map[key]
            result.append(line + " //" + c["text"])
        else:
            result.append(line)

        occurrence_counter[stripped] = occ + 1

    return "\n".join(result)


def cmd_strip(args):
    """Strip comments and save them to a sidecar file."""
    fp = resolve_keymap_file(args)
    text = fp.read_text()

    comments = parse_comments(text)
    if not comments:
        print("No comments found.")
        return

    sidecar = args.comments or fp.with_suffix(".comments.json")
    sidecar = Path(sidecar)
    sidecar.write_text(json.dumps(comments, indent=2) + "\n")

    clean = "\n".join(_strip_to_lines(text))
    try:
        parsed = json.loads(clean)
    except json.JSONDecodeError as e:
        print(f"Error: stripped file is not valid JSON: {e}", file=sys.stderr)
        sys.exit(1)

    output = Path(args.output) if args.output else fp
    output.write_text(json.dumps(parsed, indent=2) + "\n")
    print(f"Stripped {len(comments)} comment(s) -> {sidecar.name}")
    print(f"Clean JSON written to {output.name}")


def cmd_apply(args):
    """Re-apply comments from sidecar file."""
    fp = resolve_keymap_file(args)
    sidecar = Path(args.comments) if args.comments else fp.with_suffix(".comments.json")

    if not sidecar.exists():
        print(f"No comments file found at {sidecar}", file=sys.stderr)
        sys.exit(1)

    text = fp.read_text()
    comments = json.loads(sidecar.read_text())

    try:
        json.loads(text)
    except json.JSONDecodeError as e:
        print(f"Error: {fp.name} is not valid JSON: {e}", file=sys.stderr)
        sys.exit(1)

    result = apply_comments(text, comments)

    output = Path(args.output) if args.output else fp
    output.write_text(result)
    print(f"Applied {len(comments)} comment(s) from {sidecar.name}")


def _add_file_args(subparser):
    """Add shared file-resolution arguments to a subparser."""
    subparser.add_argument(
        "file", nargs="?", default=None,
        help="Direct path to keymap file (overrides -kb/-km)",
    )
    subparser.add_argument(
        "-kb", "--keyboard",
        help="Keyboard name (e.g. input_club/infinity60)",
    )
    subparser.add_argument(
        "-km", "--keymap",
        help="Keymap name (e.g. dotdash_hrm1)",
    )


def main():
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    strip_parser = subparsers.add_parser(
        "strip", help="Strip // comments and save them to a sidecar file"
    )
    _add_file_args(strip_parser)
    strip_parser.add_argument(
        "-o", "--output",
        help="Output path for clean JSON (default: overwrite input file)",
    )
    strip_parser.add_argument(
        "-c", "--comments",
        help="Path for comments sidecar (default: <file>.comments.json)",
    )

    apply_parser = subparsers.add_parser(
        "apply", help="Re-apply saved comments from sidecar file"
    )
    _add_file_args(apply_parser)
    apply_parser.add_argument(
        "-o", "--output",
        help="Output path (default: overwrite input file)",
    )
    apply_parser.add_argument(
        "-c", "--comments",
        help="Path to comments sidecar (default: <file>.comments.json)",
    )

    args = parser.parse_args()
    if args.command == "strip":
        cmd_strip(args)
    elif args.command == "apply":
        cmd_apply(args)


if __name__ == "__main__":
    main()
