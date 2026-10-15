#!/usr/bin/env python3
"""
Inspect a metricsAI chapter for the write-quiz skill.

Prints JSON with everything the skill needs to size and blueprint a quiz:
  - scope           in-scope line range (stops at the end-of-chapter Case Studies;
                    ch08 and ch13 are case-study chapters, so everything is in scope)
  - counts / units  numbered `## N.M` sections + inline Key Concepts +
                    "What you'll learn" bullets + `## Key Concepts` glossary terms
  - sizing          n_items = units rounded UP to a multiple of 5, clamped to 20-40;
                    minutes = 1.5 x n_items rounded UP to a multiple of 5; pass 80%
  - targets         type mix (~63% single / ~17% multi / ~20% tf) and
                    difficulty mix (~15% recall / 35% understanding / 50% application)
  - lists           sections, inline Key Concepts, learning objectives, glossary terms
  - datasets        data files loaded in scope, with local copies under data/ if present
  - existing        whether a bank / page / fact-check already exists for the chapter

Usage:
    python3 .claude/skills/write-quiz/scripts/inspect_chapter.py ch05
    python3 .claude/skills/write-quiz/scripts/inspect_chapter.py ch05 --table   # one-line summary
    python3 .claude/skills/write-quiz/scripts/inspect_chapter.py --all --table  # every chapter
"""

import json
import math
import re
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR.parents[3]  # scripts -> write-quiz -> skills -> .claude -> root
QUARTO_DIR = PROJECT_ROOT / "notebooks_quarto"
DATA_DIR = PROJECT_ROOT / "data"
QUIZ_DIR = PROJECT_ROOT / "quizzes"

# Reuse the chapter parsers from the add-key-concepts-section skill.
sys.path.insert(0, str(PROJECT_ROOT / ".claude/skills/add-key-concepts-section/scripts"))
from inspect_chapter import (  # noqa: E402
    find_qmd,
    parse_dataset_urls,
    parse_inline_key_concepts,
    parse_learning_objectives,
    parse_title,
)

CASE_STUDY_CHAPTERS = {"ch08", "ch13"}  # whole chapters made of case studies: quiz them
MIN_ITEMS, MAX_ITEMS, PASS_PCT, MIN_PER_ITEM = 20, 40, 80, 1.5


def ceil5(x: float) -> int:
    return int(math.ceil(x / 5.0) * 5)


def size_quiz(units: int) -> tuple[int, int]:
    n_items = min(MAX_ITEMS, max(MIN_ITEMS, ceil5(units)))
    return n_items, ceil5(n_items * MIN_PER_ITEM)


def type_mix(n: int) -> dict:
    tf = round(0.20 * n)
    multi = round(0.17 * n)
    return {"single": n - tf - multi, "multi": multi, "tf": tf}


def difficulty_mix(n: int) -> dict:
    recall = round(0.15 * n)
    understanding = round(0.35 * n)
    return {"recall": recall, "understanding": understanding, "application": n - recall - understanding}


def case_study_line(lines: list[str]) -> int | None:
    """Line number (1-based) of the end-of-chapter `## … Case Stud…` heading, if any."""
    for i, line in enumerate(lines, start=1):
        if re.match(r"^## .*Case Stud", line):
            return i
    return None


def glossary_terms(lines: list[str]) -> list[str]:
    """Bold `**Term:**` entries inside the `## Key Concepts` glossary section."""
    terms, inside = [], False
    for line in lines:
        if line.rstrip() == "## Key Concepts":
            inside = True
            continue
        if inside and line.startswith("## "):
            break
        m = re.match(r"^\*\*([^*]+?):\*\*", line) if inside else None
        if m:
            terms.append(m.group(1).strip())
    return terms


def inspect(chapter: str) -> dict:
    qmd = find_qmd(chapter)
    text = qmd.read_text(encoding="utf-8")
    lines = text.splitlines()

    cs_line = None if chapter in CASE_STUDY_CHAPTERS else case_study_line(lines)
    end = (cs_line - 1) if cs_line else len(lines)
    scope_text = "\n".join(lines[:end])

    sections = [ln.strip() for ln in lines[:end] if re.match(r"^## \d+\.\d+", ln)]
    key_concepts = [kc for kc in parse_inline_key_concepts(text) if kc["line"] <= end]
    objectives = parse_learning_objectives(text)
    glossary = glossary_terms(lines)
    units = len(sections) + len(key_concepts) + len(objectives) + len(glossary)
    n_items, minutes = size_quiz(units)

    datasets = []
    for url in parse_dataset_urls(scope_text):
        name = url.rsplit("/", 1)[-1]
        if name.startswith("file.") or "/" not in url and not name.lower().endswith((".dta", ".csv")):
            continue  # illustrative placeholders such as 'file.dta'
        local = DATA_DIR / name
        datasets.append({"url": url, "file": name, "local": str(local.relative_to(PROJECT_ROOT)) if local.exists() else None})

    return {
        "chapter": chapter,
        "qmd": str(qmd.relative_to(PROJECT_ROOT)),
        "title": parse_title(text),
        "case_study_chapter": chapter in CASE_STUDY_CHAPTERS,
        "scope": {"first_line": 1, "last_line": end, "case_studies_heading_line": cs_line},
        "counts": {
            "sections": len(sections),
            "inline_key_concepts": len(key_concepts),
            "learning_objectives": len(objectives),
            "glossary_terms": len(glossary),
        },
        "units": units,
        "sizing": {"n_items": n_items, "minutes": minutes, "pass_pct": PASS_PCT},
        "type_mix": type_mix(n_items),
        "difficulty_mix": difficulty_mix(n_items),
        "sections": sections,
        "inline_key_concepts": [f"{kc['number']} {kc['title']}" for kc in key_concepts],
        "learning_objectives": objectives,
        "glossary_terms": glossary,
        "datasets": datasets,
        "existing": {
            "bank": (QUIZ_DIR / "banks" / f"{chapter}.json").exists(),
            "page": (QUIZ_DIR / f"{chapter}.html").exists(),
            "factcheck": (QUIZ_DIR / "checks" / f"{chapter}_factcheck.py").exists(),
        },
    }


def table_row(info: dict) -> str:
    c = info["counts"]
    s = info["sizing"]
    return (f"{info['chapter']}  units={info['units']:>2} (sec {c['sections']}, kc {c['inline_key_concepts']}, "
            f"lo {c['learning_objectives']}, gloss {c['glossary_terms']}) -> {s['n_items']} items, {s['minutes']} min"
            f"{'  [bank exists]' if info['existing']['bank'] else ''}")


def main() -> int:
    args = sys.argv[1:]
    table = "--table" in args
    args = [a for a in args if a != "--table"]
    if args == ["--all"]:
        chapters = [f"ch{i:02d}" for i in range(1, 18)]
    elif len(args) == 1 and re.fullmatch(r"ch(0[1-9]|1[0-7])", args[0]):
        chapters = args
    else:
        sys.stderr.write("Usage: inspect_chapter.py chNN [--table] | --all --table   (chNN in ch01-ch17)\n")
        return 2
    for ch in chapters:
        info = inspect(ch)
        print(table_row(info) if table else json.dumps(info, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
