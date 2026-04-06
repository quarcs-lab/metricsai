#!/usr/bin/env python3
"""
Export Quarto notebooks (.qmd) to Jupyter notebooks (.ipynb) for Google Colab.

Uses `quarto convert` for the conversion, then post-processes to:
- Remove YAML front matter from the first markdown cell
- Ensure correct kernel metadata for Colab compatibility

Usage:
    python export_qmd_to_ipynb.py ch01
    python export_qmd_to_ipynb.py --all
"""

import json
import re
import subprocess
import sys
from pathlib import Path

# Resolve project paths relative to this script
SCRIPT_DIR = Path(__file__).parent
PROJECT_ROOT = SCRIPT_DIR.parent
QUARTO_DIR = PROJECT_ROOT / "notebooks_quarto"
COLAB_DIR = PROJECT_ROOT / "notebooks_colab"
import shutil as _shutil
QUARTO_BIN = _shutil.which("quarto") or "/Users/carlosmendez/opt/bin/quarto"


def find_qmd(chapter_id: str) -> Path:
    """Find the .qmd file matching a chapter ID like 'ch01'."""
    matches = list(QUARTO_DIR.glob(f"{chapter_id}_*.qmd"))
    if not matches:
        print(f"Error: No .qmd found matching '{chapter_id}_*.qmd'")
        sys.exit(1)
    if len(matches) > 1:
        print(f"Error: Multiple .qmd files match '{chapter_id}': {matches}")
        sys.exit(1)
    return matches[0]


def quarto_convert(qmd_path: Path, ipynb_path: Path) -> None:
    """Run quarto convert to produce the .ipynb file."""
    result = subprocess.run(
        [QUARTO_BIN, "convert", str(qmd_path), "--output", str(ipynb_path)],
        capture_output=True, text=True
    )
    if result.returncode != 0:
        print(f"Error running quarto convert: {result.stderr}")
        sys.exit(1)


def strip_yaml_frontmatter(text: str) -> str:
    """Remove YAML front matter (---...---) from the beginning of text."""
    # Match opening ---, any content, closing ---
    pattern = r'^---\n.*?\n---\n*'
    return re.sub(pattern, '', text, count=1, flags=re.DOTALL).lstrip('\n')


def postprocess_ipynb(ipynb_path: Path) -> None:
    """Post-process the generated .ipynb for Colab compatibility."""
    with open(ipynb_path, 'r', encoding='utf-8') as f:
        nb = json.load(f)

    # Fix kernel metadata for Colab
    nb['metadata'] = {
        'kernelspec': {
            'display_name': 'Python 3 (ipykernel)',
            'language': 'python',
            'name': 'python3'
        },
        'language_info': {
            'name': 'python',
            'version': '3.10.0'
        }
    }

    # Strip YAML front matter from the first markdown cell
    if nb['cells'] and nb['cells'][0]['cell_type'] == 'markdown':
        source = ''.join(nb['cells'][0]['source'])
        cleaned = strip_yaml_frontmatter(source)
        if cleaned != source:
            nb['cells'][0]['source'] = [cleaned]

    # Ensure nbformat is set
    nb['nbformat'] = 4
    nb['nbformat_minor'] = 5

    with open(ipynb_path, 'w', encoding='utf-8') as f:
        json.dump(nb, f, indent=1, ensure_ascii=False)
        f.write('\n')


def export_chapter(chapter_id: str) -> Path:
    """Export a single chapter from .qmd to .ipynb."""
    qmd_path = find_qmd(chapter_id)
    ipynb_name = qmd_path.stem + ".ipynb"
    ipynb_path = COLAB_DIR / ipynb_name

    print(f"Exporting: {qmd_path.name} → {ipynb_name}")

    # Step 1: Run quarto convert
    quarto_convert(qmd_path, ipynb_path)

    # Step 2: Post-process for Colab
    postprocess_ipynb(ipynb_path)

    print(f"  ✓ Written to {ipynb_path}")
    return ipynb_path


def main():
    COLAB_DIR.mkdir(exist_ok=True)

    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)

    if sys.argv[1] == "--all":
        qmd_files = sorted(QUARTO_DIR.glob("ch*_*.qmd"))
        if not qmd_files:
            print("Error: No .qmd files found in notebooks_quarto/")
            sys.exit(1)
        print(f"Exporting {len(qmd_files)} chapters...")
        for qmd in qmd_files:
            chapter_id = qmd.stem.split("_")[0]
            export_chapter(chapter_id)
        print(f"\n✓ All {len(qmd_files)} chapters exported to notebooks_colab/")
    else:
        chapter_id = sys.argv[1]
        export_chapter(chapter_id)


if __name__ == "__main__":
    main()
