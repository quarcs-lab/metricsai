#!/usr/bin/env python3
"""
Extract metadata from a metricsAI chapter .qmd, used by the
add-key-concepts-section skill.

Returns JSON to stdout with everything the skill needs to draft a
high-quality Key Concepts section without re-reading the chapter:
  - title
  - learning_objectives  (bullets under `**What you'll learn:**`)
  - dataset_urls         (URLs in setup cells / read_* calls)
  - dataset_variable_names
  - inline_key_concepts  (existing `> **Key Concept N.M:**` blockquotes)
  - section_headings     (all `^## ` lines, in order)
  - last_outline_bullet  (text of last bullet in the chapter outline,
                          used as anchor for inserting the new section)
  - insertion_point_line (line number of `## Setup`)
  - has_key_concepts_section (True if `^## Key Concepts$` already present)
  - prior_chapters_defined_terms (bold terms from earlier chapters'
                          inline blockquotes and Key Concepts sections)

Usage:
    python3 inspect_chapter.py ch05
    python3 inspect_chapter.py ch05 --pretty
"""

import json
import re
import sys
from pathlib import Path


# Resolve project paths relative to this script
SCRIPT_DIR = Path(__file__).parent
PROJECT_ROOT = SCRIPT_DIR.parent.parent.parent.parent  # skill/scripts -> skill -> .claude/skills -> .claude -> root
QUARTO_DIR = PROJECT_ROOT / "notebooks_quarto"


def find_qmd(chapter_id: str) -> Path:
    matches = sorted(QUARTO_DIR.glob(f"{chapter_id}_*.qmd"))
    if not matches:
        sys.stderr.write(f"Error: no .qmd matches '{chapter_id}_*.qmd' in {QUARTO_DIR}\n")
        sys.exit(2)
    if len(matches) > 1:
        sys.stderr.write(f"Error: multiple .qmd match '{chapter_id}': {[m.name for m in matches]}\n")
        sys.exit(2)
    return matches[0]


def parse_title(text: str) -> str:
    m = re.search(r"^title:\s*(.+?)$", text, re.MULTILINE)
    return m.group(1).strip().strip('"\'') if m else ""


def parse_learning_objectives(text: str) -> list[str]:
    """Bullets under `**What you'll learn:**` inside `## Chapter Overview`."""
    overview = _extract_section(text, "Chapter Overview")
    if not overview:
        return []
    m = re.search(
        r"\*\*What you'll learn:\*\*\s*\n(.*?)(?=\n\*\*|\n##|\Z)",
        overview, re.DOTALL,
    )
    if not m:
        return []
    bullets = re.findall(r"^\s*[-*]\s+(.+?)$", m.group(1), re.MULTILINE)
    return [b.strip() for b in bullets if b.strip()]


def parse_last_outline_bullet(text: str) -> str:
    """The last bullet under `**Chapter outline:**` in `## Chapter Overview`.

    Used as the unique anchor when inserting the new section. Falls back to the
    last bullet of `**What you'll learn:**` if no outline section is found.
    """
    overview = _extract_section(text, "Chapter Overview")
    if not overview:
        return ""
    for label in ("Chapter outline:", "What you'll learn:"):
        m = re.search(
            rf"\*\*{re.escape(label)}\*\*\s*\n(.*?)(?=\n\*\*|\n##|\Z)",
            overview, re.DOTALL,
        )
        if m:
            bullets = re.findall(r"^\s*[-*]\s+(.+?)$", m.group(1), re.MULTILINE)
            if bullets:
                return bullets[-1].strip()
    return ""


def parse_dataset_urls(text: str) -> list[str]:
    """URLs in setup cells and read_* calls."""
    urls = set()
    # Direct URL strings to data files
    for m in re.finditer(
        r"https?://[^\s\"'\)]+\.(?:DTA|dta|csv|tsv|xlsx?|parquet|json)",
        text,
    ):
        urls.add(m.group(0))
    # `pd.read_*('...')` literals (relative paths or constants)
    for m in re.finditer(r"pd\.read_\w+\(\s*['\"]([^'\"]+)['\"]", text):
        urls.add(m.group(1))
    # Concatenations like `GITHUB_DATA_URL + 'AED_HOUSE.DTA'`
    base_match = re.search(
        r"GITHUB_DATA_URL\s*=\s*['\"]([^'\"]+)['\"]", text
    )
    if base_match:
        base = base_match.group(1)
        for m in re.finditer(
            r"GITHUB_DATA_URL\s*\+\s*['\"]([^'\"]+)['\"]", text
        ):
            urls.add(base + m.group(1))
    return sorted(urls)


def parse_dataset_variable_names(text: str) -> list[str]:
    """Best-effort: pull variable names from documentation and code.

    Sources (in priority order):
      1. `**Variables:**` documentation lines
      2. `data[['var1', 'var2']]` style indexing
      3. `data['var']` style indexing
      4. Formula strings like `'price ~ size'`
    """
    names = set()
    # 1. **Variables:** lines: "  Variables: price, size, ..."
    for m in re.finditer(
        r"(?:Variables|variables)\s*:\s*([a-zA-Z0-9_, \-]+?)(?:\n|, plus|$)",
        text,
    ):
        for tok in re.split(r"[,\s]+", m.group(1)):
            tok = tok.strip().strip("`'\".,;:")
            if tok and re.match(r"^[a-zA-Z_][a-zA-Z0-9_]*$", tok):
                names.add(tok)
    # 2. data[['var1', 'var2']]
    for m in re.finditer(r"\[\s*\[([^\]]+)\]\s*\]", text):
        for tok in re.findall(r"['\"]([a-zA-Z_][a-zA-Z0-9_]*)['\"]", m.group(1)):
            names.add(tok)
    # 3. data['var']
    for m in re.finditer(
        r"\b\w+\[\s*['\"]([a-zA-Z_][a-zA-Z0-9_]*)['\"]\s*\]", text
    ):
        names.add(m.group(1))
    # 4. Formula strings: 'price ~ size + bedrooms'
    for m in re.finditer(
        r"['\"]([a-zA-Z_][a-zA-Z0-9_]*\s*~\s*[a-zA-Z_][a-zA-Z0-9_+\s\*:]*)['\"]",
        text,
    ):
        for tok in re.findall(r"[a-zA-Z_][a-zA-Z0-9_]*", m.group(1)):
            names.add(tok)
    # Drop common non-variable identifiers
    skip = {
        "data", "df", "fit", "feols", "predict", "summary", "coef",
        "describe", "head", "tail", "shape", "columns", "DataFrame",
        "read_stata", "read_csv", "pd", "np", "plt", "data_house",
        "True", "False", "None",
    }
    return sorted(n for n in names if n not in skip)


def parse_inline_key_concepts(text: str) -> list[dict]:
    """Existing `> **Key Concept N.M: Title**` blockquotes."""
    out = []
    for i, line in enumerate(text.splitlines(), start=1):
        m = re.match(
            r"^>\s*\*\*Key Concept\s+(\d+\.\d+)\s*:\s*(.+?)\*\*\s*$",
            line,
        )
        if m:
            out.append({
                "number": m.group(1),
                "title": m.group(2).strip(),
                "line": i,
            })
    return out


def parse_section_headings(text: str) -> list[dict]:
    return [
        {"line": i, "heading": line.rstrip()}
        for i, line in enumerate(text.splitlines(), start=1)
        if re.match(r"^## ", line)
    ]


def has_key_concepts_section(text: str) -> tuple[bool, int]:
    for i, line in enumerate(text.splitlines(), start=1):
        if line.rstrip() == "## Key Concepts":
            return (True, i)
    return (False, -1)


def insertion_point_line(text: str) -> int:
    for i, line in enumerate(text.splitlines(), start=1):
        if line.rstrip() == "## Setup":
            return i
    return -1


def parse_prior_chapters_defined_terms(chapter_id: str) -> list[str]:
    """Bold terms from earlier chapters' inline blockquotes and Key Concepts sections.

    A term is "defined" if it appears as a bold-faced lead-in like
    `**Term:** definition...` inside a Key Concepts section, OR as the
    title portion of an inline `> **Key Concept N.M: Title**` blockquote.

    Used to enforce Pedagogy Rule 2 (don't introduce undefined jargon).
    """
    n = int(re.match(r"ch(\d+)", chapter_id).group(1))
    terms = set()
    for prior in range(0, n):
        prior_id = f"ch{prior:02d}"
        matches = sorted(QUARTO_DIR.glob(f"{prior_id}_*.qmd"))
        if not matches:
            continue
        prior_text = matches[0].read_text(encoding="utf-8")
        # Titles of inline `> **Key Concept N.M: Title**` lines
        for m in re.finditer(
            r"^>\s*\*\*Key Concept\s+\d+\.\d+\s*:\s*(.+?)\*\*\s*$",
            prior_text, re.MULTILINE,
        ):
            terms.add(m.group(1).strip())
        # Bold lead-ins inside a `## Key Concepts` section (if present)
        kc = _extract_section(prior_text, "Key Concepts")
        if kc:
            for m in re.finditer(r"^\*\*([^*]+?):\*\*", kc, re.MULTILINE):
                terms.add(m.group(1).strip())
    return sorted(terms)


def _extract_section(text: str, heading_text: str) -> str:
    """Return the body of `## {heading_text}` up to the next `## ` heading."""
    pattern = (
        r"^##\s+" + re.escape(heading_text) + r"\s*\n(.*?)(?=^## |\Z)"
    )
    m = re.search(pattern, text, re.DOTALL | re.MULTILINE)
    return m.group(1) if m else ""


def main():
    if len(sys.argv) < 2:
        sys.stderr.write(__doc__)
        sys.exit(1)

    chapter_id = sys.argv[1]
    pretty = "--pretty" in sys.argv

    if not re.match(r"^ch(0[0-9]|1[0-7])$", chapter_id):
        sys.stderr.write(
            f"Error: chapter ID must match ch00..ch17 (got '{chapter_id}')\n"
        )
        sys.exit(2)

    qmd = find_qmd(chapter_id)
    text = qmd.read_text(encoding="utf-8")

    has_kc, kc_line = has_key_concepts_section(text)

    metadata = {
        "chapter_id": chapter_id,
        "qmd_path": str(qmd),
        "title": parse_title(text),
        "learning_objectives": parse_learning_objectives(text),
        "last_outline_bullet": parse_last_outline_bullet(text),
        "dataset_urls": parse_dataset_urls(text),
        "dataset_variable_names": parse_dataset_variable_names(text),
        "inline_key_concepts": parse_inline_key_concepts(text),
        "section_headings": parse_section_headings(text),
        "has_key_concepts_section": has_kc,
        "key_concepts_section_line": kc_line,
        "insertion_point_line": insertion_point_line(text),
        "prior_chapters_defined_terms":
            parse_prior_chapters_defined_terms(chapter_id),
    }

    indent = 2 if pretty else None
    print(json.dumps(metadata, indent=indent, ensure_ascii=False))


if __name__ == "__main__":
    main()
