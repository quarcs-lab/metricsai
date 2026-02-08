#!/usr/bin/env python3
"""Number and title all Key Concepts across metricsAI chapter notebooks.

Transforms Key Concepts from various formats to the standardized format:
    > **Key Concept X.N: Short Title**
    >
    > Explanation text...

Usage:
    python3 scripts/number_key_concepts.py           # Process all chapters
    python3 scripts/number_key_concepts.py --dry-run  # Preview changes only
    python3 scripts/number_key_concepts.py ch01 ch05  # Process specific chapters
"""

import json
import re
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
NOTEBOOKS_DIR = PROJECT_ROOT / 'notebooks_colab'

# ============================================================
# Pre-defined titles for untitled Key Concepts
# Keyed by (chapter_number, sequential_index_1based)
# ============================================================
TITLES = {
    # CH01: 8 key concepts (5 untitled: #1, #2, #4, #6, #8)
    (1, 1): "Descriptive vs. Inferential Analysis",
    (1, 2): "Observational Data in Economics",
    (1, 4): "Introduction to Regression Analysis",
    (1, 6): "Interpreting Regression Results",
    (1, 8): "Panel Data Structure",

    # CH02: 9 key concepts (all 9 untitled)
    (2, 1): "Summary Statistics",
    (2, 2): "Histograms and Density Plots",
    (2, 3): "Time Series Visualization",
    (2, 4): "Bar Charts for Categorical Data",
    (2, 5): "Frequency Tables and Pie Charts",
    (2, 6): "Logarithmic Transformations",
    (2, 7): "Time Series Transformations",
    (2, 8): "Cross-Country Distributions",
    (2, 9): "Distributional Convergence",

    # CH03: 11 key concepts (9 untitled: #1-#9; #10,#11 titled)
    (3, 1): "Random Variables",
    (3, 2): "Sample Mean as Random Variable",
    (3, 3): "Properties of the Sample Mean",
    (3, 4): "Standard Error of the Mean",
    (3, 5): "The Central Limit Theorem",
    (3, 6): "CLT in Practice",
    (3, 7): "Properties of Good Estimators",
    (3, 8): "Simple Random Sampling Assumptions",
    (3, 9): "Monte Carlo Simulation",

    # CH04: 11 key concepts (4 untitled: #1, #4, #8, #9)
    (4, 1): "Standard Error and Precision",
    (4, 4): "Hypothesis Testing Framework",
    (4, 8): "One-Sided Tests",
    (4, 9): "Inference for Proportions",

    # CH05: 10 key concepts (7 untitled: #1-#7)
    (5, 1): "Visual Data Exploration",
    (5, 2): "Two-Way Tabulations",
    (5, 3): "Scatterplots and Relationships",
    (5, 4): "The Correlation Coefficient",
    (5, 5): "Ordinary Least Squares",
    (5, 6): "R-Squared Goodness of Fit",
    (5, 7): "Association vs. Causation",

    # CH06: 10 key concepts (6 truly untitled: #1-#4, #6, #7)
    (6, 1): "Population Regression Model",
    (6, 2): "The Error Term",
    (6, 3): "OLS Assumptions",
    (6, 4): "Monte Carlo and Unbiasedness",
    (6, 6): "Standard Error of Regression Coefficients",
    (6, 7): "The Gauss-Markov Theorem",

    # CH08: 8 key concepts (all 8 untitled)
    (8, 1): "Economic vs. Statistical Significance",
    (8, 2): "Robust Standard Errors",
    (8, 3): "Income Elasticity of Demand",
    (8, 4): "Outlier Detection and Influence",
    (8, 5): "Systematic Risk and Beta",
    (8, 6): "R-Squared in CAPM",
    (8, 7): "Okun's Law",
    (8, 8): "Structural Breaks",
}


def get_chapter_number(ch_id):
    """Extract chapter number from ch_id like 'ch01' -> 1."""
    return int(ch_id.replace('ch', ''))


def find_notebook(ch_id):
    """Find the notebook file for a chapter ID."""
    matches = list(NOTEBOOKS_DIR.glob(f'{ch_id}_*.ipynb'))
    if not matches:
        raise FileNotFoundError(f"No notebook found for {ch_id}")
    return matches[0]


def transform_key_concepts_in_text(text, ch_num, concept_counter):
    """Find and transform all Key Concepts in a cell's full text.

    Works on the complete text string (handles character-by-character storage).

    Returns:
        (new_text, concepts_found)
        concepts_found: list of (number_str, title) for each concept found
    """
    concepts_found = []
    lines = text.split('\n')
    new_lines = []
    i = 0

    while i < len(lines):
        line = lines[i]
        stripped = line.strip()

        # Check if this line starts a Key Concept
        if not re.match(r'^>\s*\*\*Key Concept', stripped):
            new_lines.append(line)
            i += 1
            continue

        concept_counter[0] += 1
        num = concept_counter[0]
        number_str = f"{ch_num}.{num}"

        # Pattern 1: "> **Key Concept: Title**" (title on its own line, explanation below)
        m = re.match(r'^(>\s*)\*\*Key Concept:\s*(.+?)\*\*\s*$', stripped)
        if m:
            prefix = '> '
            title = m.group(2).strip()
            new_lines.append(f"{prefix}**Key Concept {number_str}: {title}**")
            concepts_found.append((number_str, title))
            i += 1
            continue

        # Pattern 2: "> **Key Concept: Title**: Description..." (title + inline desc)
        m = re.match(r'^(>\s*)\*\*Key Concept:\s*(.+?)\*\*:?\s+(.+)$', stripped)
        if m:
            prefix = '> '
            title = m.group(2).strip()
            desc = m.group(3).strip()
            new_lines.append(f"{prefix}**Key Concept {number_str}: {title}**")
            # Check if next line is already a blank blockquote
            next_line = lines[i + 1].strip() if i + 1 < len(lines) else ''
            if next_line not in ('>', '> ', '>'):
                new_lines.append('>')
            new_lines.append(f"> {desc}")
            concepts_found.append((number_str, title))
            i += 1
            continue

        # Pattern 3: "> **Key Concept**: Description..." (untitled, colon outside bold)
        m = re.match(r'^(>\s*)\*\*Key Concept\*\*:\s*(.+)$', stripped)
        if m:
            prefix = '> '
            desc = m.group(2).strip()
            lookup_key = (ch_num, num)
            if lookup_key in TITLES:
                title = TITLES[lookup_key]
            else:
                words = desc.split()[:5]
                title = ' '.join(words).rstrip('.,;:')
                print(f"  WARNING: No pre-defined title for Key Concept {number_str}, "
                      f"using auto-generated: '{title}'")
            new_lines.append(f"{prefix}**Key Concept {number_str}: {title}**")
            # Check if next line is already a blank blockquote
            next_line = lines[i + 1].strip() if i + 1 < len(lines) else ''
            if next_line not in ('>', '> ', '>'):
                new_lines.append('>')
            new_lines.append(f"> {desc}")
            concepts_found.append((number_str, title))
            i += 1
            continue

        # Pattern 4: "> **Key Concept:** Description..." (colon inside bold, no title)
        m = re.match(r'^(>\s*)\*\*Key Concept:\*\*\s*(.+)$', stripped)
        if m:
            prefix = '> '
            desc = m.group(2).strip()
            lookup_key = (ch_num, num)
            if lookup_key in TITLES:
                title = TITLES[lookup_key]
            else:
                words = desc.split()[:5]
                title = ' '.join(words).rstrip('.,;:')
                print(f"  WARNING: No pre-defined title for Key Concept {number_str}, "
                      f"using auto-generated: '{title}'")
            new_lines.append(f"{prefix}**Key Concept {number_str}: {title}**")
            # Check if next line is already a blank blockquote
            next_line = lines[i + 1].strip() if i + 1 < len(lines) else ''
            if next_line not in ('>', '> ', '>'):
                new_lines.append('>')
            new_lines.append(f"> {desc}")
            concepts_found.append((number_str, title))
            i += 1
            continue

        # Couldn't match any pattern - keep line, don't count it
        concept_counter[0] -= 1
        new_lines.append(line)
        print(f"  WARNING: Could not parse Key Concept line: {stripped[:80]}...")
        i += 1

    new_text = '\n'.join(new_lines)
    return new_text, concepts_found


def process_notebook(ch_id, dry_run=False):
    """Process a single notebook, numbering all Key Concepts.

    Returns list of (number_str, title) for all concepts found.
    """
    ch_num = get_chapter_number(ch_id)
    nb_path = find_notebook(ch_id)

    with open(nb_path, 'r', encoding='utf-8') as f:
        notebook = json.load(f)

    concept_counter = [0]
    all_concepts = []
    modified = False

    for cell_idx, cell in enumerate(notebook['cells']):
        if cell.get('cell_type') != 'markdown':
            continue

        source = cell.get('source', [])
        # Handle both list-of-strings and single-string source formats
        if isinstance(source, list):
            source_text = ''.join(source)
        else:
            source_text = source

        # Quick check: does this cell contain a Key Concept?
        if '**Key Concept' not in source_text:
            continue

        # Process the full text
        new_text, concepts = transform_key_concepts_in_text(
            source_text, ch_num, concept_counter
        )

        if concepts:
            all_concepts.extend(concepts)
            if new_text != source_text:
                modified = True
                if not dry_run:
                    # Store as list of lines (proper notebook format)
                    new_lines = new_text.split('\n')
                    cell['source'] = [
                        line + '\n' if i < len(new_lines) - 1 else line
                        for i, line in enumerate(new_lines)
                    ]

    if modified and not dry_run:
        with open(nb_path, 'w', encoding='utf-8') as f:
            json.dump(notebook, f, indent=1, ensure_ascii=False)
            f.write('\n')

    return all_concepts, modified


def main():
    args = sys.argv[1:]
    dry_run = '--dry-run' in args
    args = [a for a in args if a != '--dry-run']

    if args:
        chapters = [f'ch{a.replace("ch", "").zfill(2)}' for a in args]
    else:
        chapters = [f'ch{i:02d}' for i in range(1, 18)]

    if dry_run:
        print("=== DRY RUN MODE (no files modified) ===\n")

    total_concepts = 0
    total_modified = 0

    for ch_id in chapters:
        print(f"\n{'='*50}")
        print(f"  Processing {ch_id}")
        print(f"{'='*50}")

        try:
            concepts, modified = process_notebook(ch_id, dry_run=dry_run)
        except FileNotFoundError as e:
            print(f"  SKIP: {e}")
            continue

        total_concepts += len(concepts)
        if modified:
            total_modified += 1

        for num_str, title in concepts:
            print(f"  Key Concept {num_str}: {title}")

        status = "MODIFIED" if modified else "unchanged"
        if dry_run and modified:
            status = "WOULD MODIFY"
        print(f"\n  {len(concepts)} key concepts [{status}]")

    print(f"\n{'='*50}")
    print(f"  SUMMARY")
    print(f"{'='*50}")
    print(f"  Total key concepts: {total_concepts}")
    print(f"  Chapters modified:  {total_modified}")
    if dry_run:
        print(f"\n  (Dry run - no files were changed)")


if __name__ == '__main__':
    main()
