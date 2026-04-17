"""Scaffold the build script, HTML template, and plan directory for a new chapter web app.

Usage:
    python3 .claude/skills/web-app/scripts/scaffold_chapter.py chNN "Chapter Title"

Produces:
    scripts/build_chNN_webapp.py
    scripts/chNN_webapp_template.html
    web-apps/chNN/PLAN.md  (starter)

Won't overwrite existing files. Run with --force to overwrite.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

SKILL = Path(__file__).resolve().parent.parent
PROJECT_ROOT = SKILL.parent.parent.parent

TEMPLATES = SKILL / "templates"


def chapter_token(raw: str) -> tuple[str, str]:
    """Normalize a chapter argument to (slug, number)."""
    m = re.fullmatch(r"(?:ch)?(\d{1,2})", raw.lower())
    if not m:
        raise SystemExit(f"Expected chNN or N, got: {raw!r}")
    num = m.group(1).zfill(2)
    return f"ch{num}", num


def render_template(src: Path, dst: Path, replacements: dict[str, str], force: bool) -> None:
    if dst.exists() and not force:
        print(f"[skip] {dst.relative_to(PROJECT_ROOT)} already exists (use --force to overwrite)")
        return
    text = src.read_text(encoding="utf-8")
    for k, v in replacements.items():
        text = text.replace(k, v)
    dst.parent.mkdir(parents=True, exist_ok=True)
    dst.write_text(text, encoding="utf-8")
    print(f"[ok] wrote {dst.relative_to(PROJECT_ROOT)}")


PLAN_TEMPLATE = """# Chapter {num}: {title} — Dashboard Plan

## Context

TODO: why this app exists, what the chapter teaches, what gap in the static chapter this app fills.

## Design decisions

- Charts: Plotly.js
- Data: pre-computed JSON embedded inline
- Theming: light + dark toggle (persisted via localStorage)
- Scope: Key Concepts {{ list those being addressed }}

## Widgets

| Widget | Key Concept | Dataset | Target interaction |
|---|---|---|---|
| TODO | TODO | TODO | TODO |

## Data

TODO: list chapter datasets used. Note any supplementary datasets with attribution.

## Key Concepts deliberately not covered

TODO: list and explain why (definitional, narrative-only, redundant with another widget, etc.).

## Verification

- [ ] Build runs clean
- [ ] Stats match chapter
- [ ] All controls keyboard operable
- [ ] Hash state roundtrips
- [ ] Theme toggle re-renders charts
- [ ] Mobile layout works

## Future improvements

TODO
"""


def main() -> None:
    ap = argparse.ArgumentParser(description="Scaffold a metricsAI chapter web app.")
    ap.add_argument("chapter", help="Chapter slug (e.g. ch05 or 5)")
    ap.add_argument("title", help='Chapter title (e.g. "Bivariate Data Summary")')
    ap.add_argument("--force", action="store_true", help="Overwrite existing files")
    args = ap.parse_args()

    slug, num = chapter_token(args.chapter)
    title = args.title.strip()

    repl = {
        "{{CHAPTER_NUMBER}}": num,
        "{{CHAPTER_TITLE}}": title,
        "{{CHAPTER_SUBTITLE}}": (
            "Slide, toggle, and compare to build intuition for the key concepts "
            "of this chapter — using the same datasets and examples as the book."
        ),
        "{{ATTRIBUTION}}": "",  # fill in later if supplementary data is added
    }

    render_template(
        TEMPLATES / "base.html",
        PROJECT_ROOT / "scripts" / f"{slug}_webapp_template.html",
        repl,
        args.force,
    )
    render_template(
        TEMPLATES / "build_webapp.py",
        PROJECT_ROOT / "scripts" / f"build_{slug}_webapp.py",
        repl,
        args.force,
    )

    plan_path = PROJECT_ROOT / "web-apps" / slug / "PLAN.md"
    if plan_path.exists() and not args.force:
        print(f"[skip] {plan_path.relative_to(PROJECT_ROOT)} already exists")
    else:
        plan_path.parent.mkdir(parents=True, exist_ok=True)
        plan_path.write_text(PLAN_TEMPLATE.format(num=num, title=title), encoding="utf-8")
        print(f"[ok] wrote {plan_path.relative_to(PROJECT_ROOT)}")

    print()
    print("Next steps:")
    print(f"  1. Read the chapter (notebooks_quarto/{slug}_*.qmd) and identify Key Concepts.")
    print(f"  2. Edit web-apps/{slug}/PLAN.md with your widget list + target concepts.")
    print(f"  3. Paste widget patterns from .claude/skills/web-app/templates/widgets/*.md")
    print(f"     into scripts/{slug}_webapp_template.html.")
    print(f"  4. Fill in scripts/build_{slug}_webapp.py with dataset loaders.")
    print(f"  5. Build: python3 scripts/build_{slug}_webapp.py")
    print(f"  6. Verify: python3 .claude/skills/web-app/scripts/verify_app.py web-apps/{slug}/dashboard.html")
    print(f"  7. Walk through .claude/skills/web-app/docs/checklist.md before committing.")


if __name__ == "__main__":
    main()
