#!/usr/bin/env python3
"""Build a single combined Markdown file from all chapter .md files.

Usage:
    python3 scripts/build_combined_md.py

Output:
    notebooks_md/metricsAI_complete_book.md
"""

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MD_DIR = ROOT / "notebooks_md"
OUTPUT = MD_DIR / "metricsAI_complete_book.md"

# Book parts structure (matches _quarto.yml)
PARTS = {
    "Part I: Statistical Foundations": ["ch01", "ch02", "ch03", "ch04"],
    "Part II: Bivariate Regression": ["ch05", "ch06", "ch07", "ch08", "ch09"],
    "Part III: Multiple Regression": ["ch10", "ch11", "ch12", "ch13"],
    "Part IV: Advanced Topics": ["ch14", "ch15", "ch16", "ch17"],
}


def extract_title_and_body(filepath: Path) -> tuple[str, str]:
    """Extract the YAML title and body (everything after front matter)."""
    text = filepath.read_text(encoding="utf-8")

    # Extract title from YAML front matter
    title = ""
    fm_match = re.match(r"^---\n(.*?)\n---\n", text, re.DOTALL)
    if fm_match:
        for line in fm_match.group(1).splitlines():
            if line.startswith("title:"):
                title = line.split(":", 1)[1].strip().strip("'\"")
                break
        body = text[fm_match.end():]
    else:
        body = text

    return title, body.strip()


def build_toc(chapters: list[tuple[str, str, str]]) -> str:
    """Build a table of contents with part groupings.

    chapters: list of (ch_id, title, anchor)
    """
    lines = ["## Table of Contents", ""]

    # Preface (ch00) comes before parts
    ch00 = [c for c in chapters if c[0] == "ch00"]
    if ch00:
        _, title, anchor = ch00[0]
        lines.append(f"- [Preface](#{anchor})")
    lines.append("")

    for part_name, ch_ids in PARTS.items():
        lines.append(f"### {part_name}")
        lines.append("")
        for ch_id in ch_ids:
            match = [c for c in chapters if c[0] == ch_id]
            if match:
                _, title, anchor = match[0]
                lines.append(f"- [{title}](#{anchor})")
        lines.append("")

    return "\n".join(lines)


def main():
    # Collect chapter files in order
    md_files = sorted(MD_DIR.glob("ch[0-9][0-9]_*.md"))
    if not md_files:
        print("ERROR: No chapter .md files found in notebooks_md/")
        return

    print(f"Found {len(md_files)} chapter files")

    # Extract titles and bodies
    chapters = []  # (ch_id, title, anchor, body)
    for f in md_files:
        ch_id = f.stem[:4]  # e.g. "ch00"
        title, body = extract_title_and_body(f)
        if not title:
            # Fallback: use filename
            title = f.stem.replace("_", " ")
        anchor = ch_id
        chapters.append((ch_id, title, anchor, body))
        print(f"  {ch_id}: {title}")

    # Build the combined file
    parts = []

    # Book header
    parts.append(
        "---\n"
        "title: \"metricsAI: An Introduction to Econometrics with Python and AI in the Cloud\"\n"
        "author: Carlos Mendez\n"
        "---\n"
    )

    # Cover image
    parts.append(
        '<img src="https://raw.githubusercontent.com/quarcs-lab/metricsai/main/images/'
        'metricsAI_book_cover.jpg" alt="metricsAI Book Cover" width="100%">\n'
    )

    # Book description
    parts.append(
        "# metricsAI: An Introduction to Econometrics with Python and AI in the Cloud\n\n"
        "**Carlos Mendez**\n\n"
        "This is the complete markdown version of the metricsAI textbook. "
        "It contains all 17 chapters plus the preface, with all figures, "
        "code examples, key concepts, and explanations.\n"
    )

    # Table of contents
    toc_data = [(ch_id, title, anchor) for ch_id, title, anchor, _ in chapters]
    parts.append(build_toc(toc_data))

    # Chapter content
    for ch_id, title, anchor, body in chapters:
        parts.append(f"\n\n---\n\n<a id=\"{anchor}\"></a>\n")
        parts.append(body)

    # Write output
    combined = "\n".join(parts)
    OUTPUT.write_text(combined, encoding="utf-8")

    line_count = combined.count("\n") + 1
    size_kb = len(combined.encode("utf-8")) / 1024
    print(f"\nWrote {OUTPUT.name}: {line_count:,} lines, {size_kb:.0f} KB")


if __name__ == "__main__":
    main()
