#!/usr/bin/env python3
"""House punctuation check for NORD-Holding repositories.

Usage:
  python punctuation_check.py [folder]      # default: the repository root (current folder)

Fails (exit 1) when a Markdown file has a semicolon or a long dash (U+2014, U+2015) in its text. Code blocks,
inline code, HTML entities such as &amp; and URLs are not checked. The short dash (U+2013) is allowed.
Rule: no semicolons anywhere on NORD-Holding's GitHub, never the long dash (decided 19 October 2026).
"""
import re
import sys
from pathlib import Path

SKIP_DIRS = {".git", "node_modules", "dist", "build", "out", "release", "__pycache__", ".venv", "venv"}
SKIP = re.compile(r"`[^`\n]*`|&#?\w+;|https?://[^\s)\]]+|<!--.*?-->")
BAD = {";": "semicolon", "—": "long dash", "―": "long dash"}


def problems(text):
    fence = None
    for n, line in enumerate(text.split("\n"), 1):
        s = line.lstrip()
        if s.startswith(("```", "~~~")):
            mark = s[:3]
            fence = None if fence == mark else (mark if fence is None else fence)
            continue
        if fence:
            continue
        prose = SKIP.sub("", line)
        for ch, name in BAD.items():
            if ch in prose:
                yield n, name, line.strip()[:120]


def main(argv):
    root = Path(argv[1] if len(argv) > 1 else ".").resolve()
    found = 0
    for p in sorted(root.rglob("*.md")):
        if any(part in SKIP_DIRS for part in p.relative_to(root).parts):
            continue
        for n, name, line in problems(p.read_text(encoding="utf-8", errors="replace")):
            found += 1
            print(f"{p.relative_to(root)}:{n}: {name}: {line}")
    if found:
        print(f"{found} punctuation problems. Use a full stop or a comma instead of a semicolon, and the short dash "
              "(–) or a comma instead of the long dash.")
        return 1
    print("Punctuation check passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
