#!/usr/bin/env python3
"""
Fix verified content issues in metricsAI Jupyter notebooks.

Issues fixed:
1. Missing blank lines before lists (426 instances across 16 chapters)
2. Significance asterisks rendered as bold/italic (2 cells in CH11)
3. Empty markdown cells (19 cells across all 18 chapters)
4. Char-by-char source arrays normalized via nbformat read/write

Usage:
    python scripts/fix_notebook_content.py --dry-run          # Preview changes
    python scripts/fix_notebook_content.py                    # Apply changes
    python scripts/fix_notebook_content.py --dry-run ch16     # Single chapter
    python scripts/fix_notebook_content.py --verbose          # Detailed output

Options:
    --dry-run    Show what would be changed without modifying files
    --verbose    Show detailed change information
"""

import re
import sys
import nbformat
from pathlib import Path


def fix_blank_lines_before_lists(text):
    """Insert blank line before list items that follow non-blank, non-list, non-header lines.

    Returns (new_text, change_count).
    """
    lines = text.split('\n')
    result = []
    changes = 0

    for i, line in enumerate(lines):
        if i > 0:
            stripped = line.strip()
            is_list = bool(re.match(r'^(\s*[-*]\s|\s*\d+\.\s)', line))
            if is_list:
                prev_stripped = lines[i - 1].strip()
                if prev_stripped:  # non-empty previous line
                    prev_is_list = bool(re.match(r'^(\s*[-*]\s|\s*\d+\.\s)', lines[i - 1]))
                    prev_is_header = prev_stripped.startswith('#')
                    prev_is_blockquote = prev_stripped.startswith('>')
                    if not prev_is_list and not prev_is_header and not prev_is_blockquote:
                        result.append('')
                        changes += 1
        result.append(line)

    return '\n'.join(result), changes


def fix_significance_asterisks(text, notebook_name):
    """Wrap significance asterisks in backticks in CH11 to prevent bold/italic rendering.

    Returns (new_text, change_count).
    """
    if 'ch11' not in notebook_name.lower():
        return text, 0

    changes = 0
    replacements = [
        ('- *** for p <', '- `***` for p <'),
        ('- ** for p <', '- `**` for p <'),
        ('- * for p <', '- `*` for p <'),
        ('(*** for $p <', '(`***` for $p <'),
        (', ** for $p <', ', `**` for $p <'),
        (', * for $p <', ', `*` for $p <'),
    ]
    for old, new in replacements:
        if old in text:
            text = text.replace(old, new)
            changes += 1

    return text, changes


def process_notebook(nb_path, dry_run=False, verbose=False):
    """Process a single notebook, applying all fixes. Returns stats dict."""
    nb = nbformat.read(str(nb_path), as_version=4)
    notebook_name = nb_path.name

    stats = {
        'blank_lines': 0,
        'asterisks': 0,
        'empty_removed': 0,
        'cells_modified': 0,
    }

    # Fix 1 and 2: Process markdown cell text
    for i, cell in enumerate(nb.cells):
        if cell.cell_type != 'markdown':
            continue

        text = cell.source
        new_text = text

        # Fix 1: blank lines before lists
        new_text, bl_count = fix_blank_lines_before_lists(new_text)
        stats['blank_lines'] += bl_count

        # Fix 2: significance asterisks
        new_text, ast_count = fix_significance_asterisks(new_text, notebook_name)
        stats['asterisks'] += ast_count

        if new_text != text:
            stats['cells_modified'] += 1
            if verbose and bl_count > 0:
                print(f"    Cell {i}: {bl_count} blank lines inserted")
            if verbose and ast_count > 0:
                print(f"    Cell {i}: {ast_count} asterisk fixes")
            if not dry_run:
                cell.source = new_text

    # Fix 3: remove empty markdown cells
    new_cells = []
    for i, cell in enumerate(nb.cells):
        if cell.cell_type == 'markdown' and cell.source.strip() == '':
            stats['empty_removed'] += 1
            if verbose:
                print(f"    Cell {i}: empty markdown cell removed")
        else:
            new_cells.append(cell)

    if not dry_run:
        nb.cells = new_cells

    # Write back (Fix 4: nbformat normalizes char-by-char source arrays automatically)
    has_changes = stats['blank_lines'] > 0 or stats['asterisks'] > 0 or stats['empty_removed'] > 0
    if not dry_run and has_changes:
        nbformat.write(nb, str(nb_path))

    return stats


def main():
    dry_run = '--dry-run' in sys.argv
    verbose = '--verbose' in sys.argv

    # Get list of notebooks to process
    args = [arg for arg in sys.argv[1:] if not arg.startswith('--')]
    if args:
        # Support both "ch16" and full path
        files = []
        for arg in args:
            if Path(arg).exists():
                files.append(Path(arg))
            else:
                matches = sorted(Path('notebooks_colab').glob(f'{arg}*.ipynb'))
                files.extend(matches)
    else:
        files = sorted(Path('notebooks_colab').glob('ch*.ipynb'))

    if not files:
        print("No notebooks found to process.")
        return

    print("=" * 70)
    if dry_run:
        print("DRY-RUN MODE: No files will be modified")
    else:
        print("APPLYING FIXES: Files will be modified")
    print(f"Notebooks to process: {len(files)}")
    print("=" * 70 + "\n")

    totals = {'blank_lines': 0, 'asterisks': 0, 'empty_removed': 0, 'cells_modified': 0}

    for nb_path in files:
        if verbose:
            print(f"  {nb_path.name}:")

        stats = process_notebook(nb_path, dry_run, verbose)

        has_changes = stats['blank_lines'] > 0 or stats['asterisks'] > 0 or stats['empty_removed'] > 0

        for key in totals:
            totals[key] += stats[key]

        prefix = '[DRY-RUN] ' if dry_run else '\u2713 '
        if has_changes:
            parts = []
            if stats['blank_lines'] > 0:
                parts.append(f"{stats['blank_lines']} blank lines")
            if stats['asterisks'] > 0:
                parts.append(f"{stats['asterisks']} asterisk fixes")
            if stats['empty_removed'] > 0:
                parts.append(f"{stats['empty_removed']} empty cells removed")
            print(f"{prefix}{nb_path.name}: {', '.join(parts)}")
        else:
            if verbose:
                print(f"  {nb_path.name}: no changes needed")

    # Summary
    print("\n" + "=" * 70)
    print("SUMMARY")
    print("=" * 70)
    print(f"Notebooks processed:       {len(files)}")
    print(f"Blank lines inserted:      {totals['blank_lines']}")
    print(f"Asterisk fixes:            {totals['asterisks']}")
    print(f"Empty cells removed:       {totals['empty_removed']}")
    print(f"Total cells modified:      {totals['cells_modified']}")

    if dry_run:
        print("\nThis was a DRY-RUN. No files were modified.")
        print("Run without --dry-run to apply changes.")
    else:
        print("\nAll changes applied successfully!")

    print("=" * 70)


if __name__ == '__main__':
    main()
