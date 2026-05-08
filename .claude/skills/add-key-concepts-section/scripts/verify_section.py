#!/usr/bin/env python3
"""
Verify that the Key Concepts section has been correctly added to a
metricsAI chapter, used by the add-key-concepts-section skill after
the .qmd has been edited and `sync_chapter.sh` has run.

Checks:
  1. .qmd contains exactly one `^## Key Concepts$` heading.
  2. Rendered HTML book contains `id="key-concepts"` and exactly N
     `class="columns"` blocks (where N is the concept count derived
     from the .qmd).
  3. .ipynb contains zero hits for `## Key Concepts`, `callout-tip`,
     `callout-note`, or `:::` columns markup (i.e., the section was
     stripped by `scripts/export_qmd_to_ipynb.py:strip_key_concepts`).
  4. .md mirror contains the section verbatim.

Exits 0 if all checks pass, 1 otherwise. Always prints a per-check
report to stdout in a fixed format the skill can grep.

Usage:
    python3 verify_section.py ch05
"""

import json
import re
import sys
from pathlib import Path


SCRIPT_DIR = Path(__file__).parent
PROJECT_ROOT = SCRIPT_DIR.parent.parent.parent.parent
QUARTO_DIR = PROJECT_ROOT / "notebooks_quarto"
COLAB_DIR = PROJECT_ROOT / "notebooks_colab"
MD_DIR = PROJECT_ROOT / "notebooks_md"
HTML_DIR = PROJECT_ROOT / "book" / "_book" / "notebooks_quarto"


def find_basename(chapter_id: str) -> str:
    matches = sorted(QUARTO_DIR.glob(f"{chapter_id}_*.qmd"))
    if not matches:
        sys.stderr.write(f"Error: no .qmd matches '{chapter_id}_*.qmd'\n")
        sys.exit(2)
    return matches[0].stem


def count_concept_blocks_in_qmd(qmd_text: str) -> int:
    """Count `::::: {.columns}` blocks inside the Key Concepts section."""
    m = re.search(
        r"^## Key Concepts\s*\n(.*?)(?=^## |\Z)",
        qmd_text, re.DOTALL | re.MULTILINE,
    )
    if not m:
        return 0
    return len(re.findall(r"^::::: \{\.columns\}", m.group(1), re.MULTILINE))


def check_qmd(basename: str) -> tuple[bool, str, int]:
    path = QUARTO_DIR / f"{basename}.qmd"
    text = path.read_text(encoding="utf-8")
    headings = re.findall(r"^## Key Concepts$", text, re.MULTILINE)
    n_blocks = count_concept_blocks_in_qmd(text)
    ok = (len(headings) == 1) and (n_blocks >= 5) and (n_blocks <= 8)
    msg = (
        f".qmd:  {len(headings)}× '## Key Concepts' heading, "
        f"{n_blocks} concept blocks"
        f"  {'✓' if ok else '✗'}"
    )
    return ok, msg, n_blocks


def check_html(basename: str, expected_blocks: int) -> tuple[bool, str]:
    path = HTML_DIR / f"{basename}.html"
    if not path.exists():
        return False, f"HTML:  file not found at {path}  ✗"
    text = path.read_text(encoding="utf-8")
    has_id = bool(re.search(r'id="key-concepts"', text))
    n_columns = len(re.findall(r'class="columns', text))
    ok = has_id and n_columns >= expected_blocks
    msg = (
        f"HTML:  id=\"key-concepts\" {'present' if has_id else 'MISSING'}, "
        f"{n_columns} .columns blocks (expected ≥{expected_blocks})"
        f"  {'✓' if ok else '✗'}"
    )
    return ok, msg


def check_ipynb(basename: str) -> tuple[bool, str]:
    path = COLAB_DIR / f"{basename}.ipynb"
    if not path.exists():
        return False, f"ipynb: file not found at {path}  ✗"
    nb = json.loads(path.read_text(encoding="utf-8"))
    forbidden_substrings = [
        "## Key Concepts",
        "callout-tip",
        "callout-note",
        "::::: {.columns}",
        ":::: {.column",
    ]
    hits: dict[str, int] = {s: 0 for s in forbidden_substrings}
    for cell in nb.get("cells", []):
        if cell.get("cell_type") != "markdown":
            continue
        src = cell.get("source", "")
        if isinstance(src, list):
            src = "".join(src)
        for s in forbidden_substrings:
            if s in src:
                hits[s] += 1
    total = sum(hits.values())
    ok = (total == 0)
    if ok:
        msg = "ipynb: 0 hits for Quarto-only markup  ✓ (stripped)"
    else:
        details = ", ".join(f"{k!r}={v}" for k, v in hits.items() if v)
        msg = f"ipynb: stripping incomplete — found {details}  ✗"
    return ok, msg


def check_md(basename: str) -> tuple[bool, str]:
    path = MD_DIR / f"{basename}.md"
    if not path.exists():
        return False, f"md:    file not found at {path}  ✗"
    text = path.read_text(encoding="utf-8")
    has_section = bool(re.search(r"^## Key Concepts$", text, re.MULTILINE))
    has_callouts = "callout-tip" in text
    ok = has_section and has_callouts
    msg = (
        f"md:    section present={'yes' if has_section else 'no'}, "
        f"callouts preserved={'yes' if has_callouts else 'no'}"
        f"  {'✓' if ok else '✗'}"
    )
    return ok, msg


def main():
    if len(sys.argv) < 2:
        sys.stderr.write(__doc__)
        sys.exit(1)

    chapter_id = sys.argv[1]
    if not re.match(r"^ch(0[0-9]|1[0-7])$", chapter_id):
        sys.stderr.write(
            f"Error: chapter ID must match ch00..ch17 (got '{chapter_id}')\n"
        )
        sys.exit(2)

    basename = find_basename(chapter_id)

    ok_qmd, msg_qmd, n_blocks = check_qmd(basename)
    ok_html, msg_html = check_html(basename, n_blocks)
    ok_ipynb, msg_ipynb = check_ipynb(basename)
    ok_md, msg_md = check_md(basename)

    print(f"Verification for {chapter_id} ({basename}):")
    print(f"  {msg_qmd}")
    print(f"  {msg_html}")
    print(f"  {msg_ipynb}")
    print(f"  {msg_md}")

    all_ok = ok_qmd and ok_html and ok_ipynb and ok_md
    if all_ok:
        print(f"\n✅ All verification checks passed for {chapter_id}.")
        sys.exit(0)
    else:
        print(f"\n❌ Verification failed for {chapter_id}. See ✗ lines above.")
        sys.exit(1)


if __name__ == "__main__":
    main()
