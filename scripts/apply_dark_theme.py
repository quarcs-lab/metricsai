#!/usr/bin/env python3
"""
Apply dark theme to all chapter notebooks (CH03-CH17).

Replaces the whitegrid setup with dark_background + navy rcParams,
and fixes all colors that would be invisible on the dark background.

Color rules:
  - black/navy/darkblue scatter/data → #22d3ee (book cyan)
  - blue fitted/regression lines → #c084fc (book purple)
  - blue in scatter/errorbar → #22d3ee (book cyan)
  - blue in conditional color lists → #22d3ee (book cyan)
  - black/k on axhline/axvline → white, alpha=0.3
  - edgecolor='black' → #3a4a6b (grid color)
  - facecolor='wheat' → #1e2a45 (dark box)
  - darkgreen → #4ade80 (light green)
  - 'b-'/'b--' format strings → '-'/'--' + color='#c084fc'
"""

import json
import re
import glob
import os

# Book color palette
CYAN = '#22d3ee'
PURPLE = '#c084fc'
GRID = '#3a4a6b'
DARK_BOX = '#1e2a45'
LIGHT_GREEN = '#4ade80'

DARK_THEME_SETUP = """# Set plotting style (dark theme matching book design)
plt.style.use('dark_background')
sns.set_style("darkgrid")
plt.rcParams.update({
    'axes.facecolor': '#1a2235',
    'figure.facecolor': '#12162c',
    'grid.color': '#3a4a6b',
    'figure.figsize': (10, 6),
    'text.color': 'white',
    'axes.labelcolor': 'white',
    'xtick.color': 'white',
    'ytick.color': 'white',
    'axes.edgecolor': '#1a2235',
})"""

OLD_SETUP_PATTERN = """# Set plotting style
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (10, 6)"""

# Alternative pattern without the comment (e.g., CH13)
OLD_SETUP_PATTERN_ALT = """sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (10, 6)"""


def process_line(line, current_function):
    """Apply color replacements to a single line based on context."""
    stripped = line.lstrip()

    # Skip comments and print statements
    if stripped.startswith('#') or stripped.startswith('print('):
        return line

    # --- Format strings: 'b-' and 'b--' ---
    line = line.replace("'b-',", f"'-', color='{PURPLE}',")
    line = line.replace("'b--',", f"'--', color='{PURPLE}',")
    # Handle case where format string is last arg before )
    line = line.replace("'b-')", f"'-', color='{PURPLE}')")
    line = line.replace("'b--')", f"'--', color='{PURPLE}')")

    # --- Simple context-free replacements ---
    line = line.replace("edgecolor='black'", f"edgecolor='{GRID}'")
    line = line.replace("color='navy'", f"color='{CYAN}'")
    line = line.replace("color='darkblue'", f"color='{CYAN}'")
    line = line.replace("color='darkgreen'", f"color='{LIGHT_GREEN}'")
    line = line.replace("facecolor='wheat'", f"facecolor='{DARK_BOX}'")

    # Fix alpha on wheat→dark box replacements (same line)
    if f"facecolor='{DARK_BOX}'" in line and "alpha=0.5" in line:
        line = line.replace("alpha=0.5", "alpha=0.9")

    # --- Context-dependent replacements ---
    is_refline = 'axhline' in line or 'axvline' in line

    if is_refline or current_function == 'refline':
        line = line.replace("color='black'", "color='white', alpha=0.3")
        line = line.replace("color='k'", "color='white', alpha=0.3")
        line = line.replace("color='blue'", "color='white', alpha=0.3")
    elif current_function in ('scatter', 'errorbar'):
        line = line.replace("color='black'", f"color='{CYAN}'")
        line = line.replace("color='k'", f"color='{CYAN}'")
        line = line.replace("color='blue'", f"color='{CYAN}'")
    else:
        # Default: scatter/data points get cyan, fitted lines get purple
        line = line.replace("color='black'", f"color='{CYAN}'")
        line = line.replace("color='k'", f"color='{CYAN}'")
        line = line.replace("color='blue'", f"color='{PURPLE}'")

    # --- Bare 'blue' in conditional color lists / tuples ---
    if "else 'blue'" in line:
        line = line.replace("else 'blue'", f"else '{CYAN}'")
    # Handle tuples like ('Male', 'blue') — only when not a color= parameter
    if "'blue'" in line and "color=" not in line:
        line = re.sub(r"(?<=[,(])\s*'blue'(?=\s*[,)])", f" '{CYAN}'", line)

    return line


def detect_function(line):
    """Detect which plotting function a line starts."""
    if '.scatter(' in line:
        return 'scatter'
    elif '.errorbar(' in line:
        return 'errorbar'
    elif '.axhline(' in line or '.axvline(' in line:
        return 'refline'
    elif '.plot(' in line:
        return 'plot'
    elif '.barh(' in line or '.bar(' in line:
        return 'bar'
    elif '.hist(' in line:
        return 'hist'
    return None


def process_cell_source(source_str):
    """Process all lines in a cell's source code."""
    lines = source_str.split('\n')
    result_lines = []
    current_function = None
    paren_depth = 0

    for line in lines:
        # Detect new function call
        new_func = detect_function(line)
        if new_func:
            current_function = new_func
            paren_depth = line.count('(') - line.count(')')
        elif current_function and paren_depth > 0:
            paren_depth += line.count('(') - line.count(')')
        else:
            current_function = None
            paren_depth = 0

        # Apply replacements
        processed = process_line(line, current_function)
        result_lines.append(processed)

        # Reset function tracking when call ends
        if current_function and paren_depth <= 0:
            current_function = None

    return '\n'.join(result_lines)


def process_notebook(filepath):
    """Process a single notebook file."""
    with open(filepath, 'r', encoding='utf-8') as f:
        nb = json.load(f)

    chapter = os.path.basename(filepath)[:4]
    changes = []

    for i, cell in enumerate(nb['cells']):
        if cell['cell_type'] != 'code':
            continue

        source_str = ''.join(cell['source'])
        original = source_str

        # Step 1: Replace setup cell (try both patterns)
        if OLD_SETUP_PATTERN in source_str:
            source_str = source_str.replace(OLD_SETUP_PATTERN, DARK_THEME_SETUP)
            changes.append(f"  Cell {i}: Replaced setup style → dark theme")
        elif OLD_SETUP_PATTERN_ALT in source_str:
            source_str = source_str.replace(OLD_SETUP_PATTERN_ALT, DARK_THEME_SETUP)
            changes.append(f"  Cell {i}: Replaced setup style → dark theme (alt pattern)")

        # Step 2: Apply color replacements
        processed = process_cell_source(source_str)

        if processed != original:
            # Convert back to source list format
            source_lines = processed.split('\n')
            new_source = []
            for j, sl in enumerate(source_lines):
                if j < len(source_lines) - 1:
                    new_source.append(sl + '\n')
                else:
                    # Last line: keep trailing newline only if original had one
                    if original.endswith('\n'):
                        new_source.append(sl + '\n')
                    else:
                        new_source.append(sl)

            cell['source'] = new_source

            if f"Cell {i}:" not in '\n'.join(changes):
                # Count color changes
                diff_count = sum(1 for a, b in zip(original, processed) if a != b)
                changes.append(f"  Cell {i}: Color replacements applied")

    # Write back
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(nb, f, indent=1, ensure_ascii=False)
        f.write('\n')

    return changes


def main():
    base_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'notebooks_colab')

    chapters = [f'ch{i:02d}' for i in range(3, 18)]
    total_changes = 0

    for ch in chapters:
        # Find the notebook file
        pattern = os.path.join(base_dir, f'{ch}_*.ipynb')
        files = glob.glob(pattern)
        if not files:
            print(f"WARNING: No notebook found for {ch}")
            continue

        filepath = files[0]
        chapter_name = os.path.basename(filepath)
        print(f"\n{'='*60}")
        print(f"Processing: {chapter_name}")
        print(f"{'='*60}")

        changes = process_notebook(filepath)
        for change in changes:
            print(change)

        if changes:
            print(f"  → {len(changes)} cell(s) modified")
            total_changes += len(changes)
        else:
            print("  → No changes needed")

    print(f"\n{'='*60}")
    print(f"DONE: {total_changes} total cell(s) modified across {len(chapters)} chapters")
    print(f"{'='*60}")
    print("\nNext steps:")
    print("  1. Re-execute notebooks: jupyter nbconvert --execute --inplace")
    print("  2. Render Quarto book: cd book && quarto render")


if __name__ == '__main__':
    main()
