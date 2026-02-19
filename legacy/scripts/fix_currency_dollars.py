#!/usr/bin/env python3
"""
Fix currency dollar signs in Jupyter notebook markdown cells.

Converts unescaped currency dollars ($1,000) to escaped form (\$1,000)
while preserving legitimate LaTeX math expressions.

Usage:
    python fix_currency_dollars.py [--dry-run] [--verbose] [notebook.ipynb ...]

If no files specified, processes all .ipynb files in notebooks_colab/

Options:
    --dry-run    Show what would be changed without modifying files
    --verbose    Show detailed change information
"""

import json
import re
import sys
from pathlib import Path
from datetime import datetime

# Currency pattern (to be escaped)
# Matches: $1,000 | $73.77 | $250,000 | $23
# Does NOT match: \$1,000 (already escaped) | $\beta$ (has backslash after)
CURRENCY_RE = re.compile(
    r'(?<!\\)\$([0-9]{1,3}(?:,[0-9]{3})*(?:\.[0-9]{2})?|[0-9]+(?:\.[0-9]{2})?)'
)

# Display math (preserve) - multiline blocks
DISPLAY_MATH_RE = re.compile(r'\$\$[^\$]+\$\$', re.DOTALL)

def escape_currency_dollars(text):
    """
    Escape currency dollars while preserving math expressions.

    Strategy:
    1. Extract and temporarily remove display math blocks ($$...$$)
    2. Replace currency $ with \$ in remaining text
    3. Restore display math blocks unchanged
    """
    # Extract display math blocks
    display_blocks = []

    def save_display_math(match):
        display_blocks.append(match.group(0))
        return f"<<<DISPLAY_MATH_{len(display_blocks)-1}>>>"

    text = DISPLAY_MATH_RE.sub(save_display_math, text)

    # Replace currency dollars with escaped version
    # CURRENCY_RE captures: group(1) is the dollar sign, group(2) is the amount
    # We replace with: \$ followed by the amount
    text = CURRENCY_RE.sub(r'\\$\1', text)

    # Restore display math blocks
    for i, block in enumerate(display_blocks):
        text = text.replace(f"<<<DISPLAY_MATH_{i}>>>", block)

    return text

def process_notebook(filepath, dry_run=False, verbose=False):
    """Process a single notebook."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            nb = json.load(f)
    except json.JSONDecodeError as e:
        print(f"ERROR: Failed to parse {filepath.name}: {e}")
        return []

    changes = []

    for i, cell in enumerate(nb['cells']):
        if cell['cell_type'] == 'markdown':
            original = ''.join(cell['source']) if isinstance(cell['source'], list) else cell['source']
            modified = escape_currency_dollars(original)

            if original != modified:
                # Count how many currency patterns were changed
                currency_count = len(CURRENCY_RE.findall(original))

                changes.append({
                    'cell': i,
                    'count': currency_count,
                    'before_preview': original[:80].replace('\n', ' '),
                    'after_preview': modified[:80].replace('\n', ' ')
                })

                if not dry_run:
                    # Update cell source
                    if isinstance(cell['source'], list):
                        cell['source'] = [modified]
                    else:
                        cell['source'] = modified

    # Write modified notebook
    if not dry_run and changes:
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(nb, f, indent=1, ensure_ascii=False)
        except Exception as e:
            print(f"ERROR: Failed to write {filepath.name}: {e}")
            return []

    return changes

def main():
    dry_run = '--dry-run' in sys.argv
    verbose = '--verbose' in sys.argv

    # Get list of notebooks to process
    args = [arg for arg in sys.argv[1:] if not arg.startswith('--')]
    if args:
        files = [Path(arg) for arg in args]
    else:
        files = sorted(Path('notebooks_colab').glob('ch*.ipynb'))

    if not files:
        print("No notebooks found to process.")
        return

    print("="*70)
    if dry_run:
        print("DRY-RUN MODE: No files will be modified")
    else:
        print("PROCESSING MODE: Files will be modified")
    print(f"Notebooks to process: {len(files)}")
    print("="*70 + "\n")

    total_changes = 0
    total_cells = 0
    processed_files = []

    for nb_path in files:
        changes = process_notebook(nb_path, dry_run, verbose)

        if changes:
            total_changes += len(changes)
            total_cells += sum(c['count'] for c in changes)
            processed_files.append(nb_path.name)

            prefix = '[DRY-RUN] ' if dry_run else '✓ '
            print(f"{prefix}{nb_path.name}: {len(changes)} cells modified, {sum(c['count'] for c in changes)} currency patterns")

            if verbose and changes:
                for change in changes[:3]:  # Show first 3 changes
                    print(f"  Cell {change['cell']} ({change['count']} patterns):")
                    print(f"    Before: {change['before_preview']}...")
                    print(f"    After:  {change['after_preview']}...")
                if len(changes) > 3:
                    print(f"  ... and {len(changes)-3} more cells")

    # Summary
    print("\n" + "="*70)
    print("SUMMARY")
    print("="*70)
    print(f"Total notebooks processed: {len(files)}")
    print(f"Notebooks with changes: {len(processed_files)}")
    print(f"Total cells modified: {total_changes}")
    print(f"Total currency patterns escaped: {total_cells}")

    if dry_run:
        print("\nThis was a DRY-RUN. No files were modified.")
        print("Run without --dry-run to apply changes.")
    else:
        print("\nAll changes have been applied successfully!")
        print("Backup available in: notebooks_colab_backup/")

    print("="*70)

if __name__ == '__main__':
    main()
