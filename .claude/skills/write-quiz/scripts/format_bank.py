#!/usr/bin/env python3
"""Rewrite quizzes/banks/chNN.json in the house layout (and renumber ids).

Layout: compact, one option per line, UTF-8, two-space indent (as ch01.json).
Ids are renumbered P01…/E01… in array (display) order, so items can be inserted,
moved, or removed freely while editing.

Usage:
    python3 .claude/skills/write-quiz/scripts/format_bank.py ch05
"""

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]


def J(v):
    return json.dumps(v, ensure_ascii=False)


def item_block(it):
    opts = ",\n".join(
        f'        {{"text": {J(o["text"])}, "correct": {J(o["correct"])}, "feedback": {J(o["feedback"])}}}'
        for o in it["options"]
    )
    return ("    {\n"
            f'      "id": {J(it["id"])},\n      "type": {J(it["type"])},\n      "concept": {J(it["concept"])},\n'
            f'      "stem": {J(it["stem"])},\n      "options": [\n{opts}\n      ],\n'
            f'      "explanation": {J(it["explanation"])}\n    }}')


def dumps(bank: dict) -> str:
    meta = ",\n".join(f"    {J(k)}: {J(v)}" for k, v in bank["meta"].items())
    return ("{\n  \"meta\": {\n" + meta + "\n  },\n"
            + '  "practice": [\n' + ",\n".join(item_block(i) for i in bank["practice"]) + "\n  ],\n"
            + '  "exam": [\n' + ",\n".join(item_block(i) for i in bank["exam"]) + "\n  ]\n}\n")


def main() -> int:
    if len(sys.argv) != 2 or not re.fullmatch(r"ch(0[1-9]|1[0-7])", sys.argv[1]):
        sys.stderr.write("Usage: format_bank.py chNN\n")
        return 2
    path = ROOT / "quizzes" / "banks" / f"{sys.argv[1]}.json"
    bank = json.loads(path.read_text(encoding="utf-8"))
    for set_name, prefix in (("practice", "P"), ("exam", "E")):
        for n, item in enumerate(bank[set_name], 1):
            item["id"] = f"{prefix}{n:02d}"
    out = dumps(bank)
    json.loads(out)  # sanity
    path.write_text(out, encoding="utf-8")
    print(f"formatted {path.relative_to(ROOT)} ({len(bank['practice'])} practice, {len(bank['exam'])} exam)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
