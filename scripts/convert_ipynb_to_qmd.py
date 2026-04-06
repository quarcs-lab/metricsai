#!/usr/bin/env python3
"""
Convert Jupyter notebooks (.ipynb) to Quarto notebooks (.qmd).

Uses `quarto convert` for the initial conversion, then post-processes
to clean up YAML front matter and remove cell execution metadata.

Usage:
    python convert_ipynb_to_qmd.py ch01
    python convert_ipynb_to_qmd.py --all
"""

import subprocess
import re
import sys
from pathlib import Path

# Resolve project paths relative to this script
SCRIPT_DIR = Path(__file__).parent
PROJECT_ROOT = SCRIPT_DIR.parent
NOTEBOOKS_SRC = PROJECT_ROOT / "notebooks_colab"
NOTEBOOKS_DST = PROJECT_ROOT / "notebooks_quarto"
import shutil as _shutil
QUARTO_BIN = _shutil.which("quarto") or "/Users/carlosmendez/opt/bin/quarto"


def find_notebook(chapter_id: str) -> Path:
    """Find the .ipynb file matching a chapter ID like 'ch01'."""
    matches = list(NOTEBOOKS_SRC.glob(f"{chapter_id}_*.ipynb"))
    if not matches:
        print(f"Error: No notebook found matching '{chapter_id}_*.ipynb'")
        sys.exit(1)
    if len(matches) > 1:
        print(f"Error: Multiple notebooks match '{chapter_id}': {matches}")
        sys.exit(1)
    return matches[0]


def quarto_convert(ipynb_path: Path, qmd_path: Path) -> None:
    """Run quarto convert to produce the raw .qmd file."""
    result = subprocess.run(
        [QUARTO_BIN, "convert", str(ipynb_path), "--output", str(qmd_path)],
        capture_output=True, text=True
    )
    if result.returncode != 0:
        print(f"Error running quarto convert: {result.stderr}")
        sys.exit(1)


def clean_yaml_frontmatter(content: str) -> str:
    """Clean up YAML front matter: remove jupytext, add execute options."""
    # Split into front matter and body
    parts = content.split("---", 2)
    if len(parts) < 3:
        return content

    yaml_block = parts[1]
    body = parts[2]

    # Extract title
    title_match = re.search(r'^title:\s*(.+)$', yaml_block, re.MULTILINE)
    title = title_match.group(1).strip() if title_match else "Untitled"

    # Build clean YAML
    new_yaml = f"""
title: {title}
execute:
  enabled: false
"""

    return f"---{new_yaml}---{body}"


def remove_execution_metadata(content: str) -> str:
    """Remove #| execution: lines from code cells."""
    lines = content.split("\n")
    cleaned = []
    for line in lines:
        if line.strip().startswith("#| execution:"):
            continue
        cleaned.append(line)
    return "\n".join(cleaned)


def convert_chapter(chapter_id: str) -> Path:
    """Convert a single chapter from .ipynb to .qmd."""
    ipynb_path = find_notebook(chapter_id)
    qmd_name = ipynb_path.stem + ".qmd"
    qmd_path = NOTEBOOKS_DST / qmd_name

    print(f"Converting: {ipynb_path.name} → {qmd_name}")

    # Step 1: Run quarto convert
    quarto_convert(ipynb_path, qmd_path)

    # Step 2: Post-process
    content = qmd_path.read_text()
    content = clean_yaml_frontmatter(content)
    content = remove_execution_metadata(content)
    qmd_path.write_text(content)

    print(f"  ✓ Written to {qmd_path}")
    return qmd_path


def main():
    NOTEBOOKS_DST.mkdir(exist_ok=True)

    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)

    if sys.argv[1] == "--all":
        notebooks = sorted(NOTEBOOKS_SRC.glob("ch*_*.ipynb"))
        if not notebooks:
            print("Error: No notebooks found in notebooks_colab/")
            sys.exit(1)
        print(f"Converting {len(notebooks)} chapters...")
        for nb in notebooks:
            chapter_id = nb.stem.split("_")[0]  # e.g., "ch01"
            convert_chapter(chapter_id)
        print(f"\n✓ All {len(notebooks)} chapters converted to notebooks_quarto/")
    else:
        chapter_id = sys.argv[1]
        convert_chapter(chapter_id)


if __name__ == "__main__":
    main()
