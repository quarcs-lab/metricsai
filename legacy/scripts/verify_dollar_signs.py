#!/usr/bin/env python3
"""
Verify dollar sign usage in Jupyter notebooks.

Analyzes markdown cells to count:
- Currency patterns ($1,000, $73.77, etc.)
- Inline math expressions ($\beta$, $\mu$, etc.)
- Display math blocks ($$...$$)
- Already escaped currency (\$1,000)

Usage:
    python verify_dollar_signs.py [notebook.ipynb ...]

If no files specified, processes all .ipynb files in notebooks_colab/
"""

import json
import re
import sys
from pathlib import Path
from collections import defaultdict

# Patterns
CURRENCY_RE = re.compile(r'(?<!\\)\$([0-9]{1,3}(?:,[0-9]{3})*(?:\.[0-9]{2})?|[0-9]+(?:\.[0-9]{2})?)')
ESCAPED_CURRENCY_RE = re.compile(r'\\\$([0-9]+(?:,[0-9]{3})*(?:\.[0-9]{2})?)')
DISPLAY_MATH_RE = re.compile(r'\$\$[^\$]+\$\$', re.DOTALL)
INLINE_MATH_RE = re.compile(r'(?<!\\)\$[^$\n]+\$')

def analyze_notebook(filepath):
    """Analyze a single notebook for dollar sign usage."""
    with open(filepath, 'r', encoding='utf-8') as f:
        nb = json.load(f)

    stats = {
        'currency': [],
        'escaped_currency': [],
        'display_math': [],
        'inline_math': [],
        'total_cells': 0
    }

    for i, cell in enumerate(nb['cells']):
        if cell['cell_type'] == 'markdown':
            text = ''.join(cell['source'])
            stats['total_cells'] += 1

            # Find currency patterns
            for match in CURRENCY_RE.finditer(text):
                context = text[max(0, match.start()-20):match.end()+20]
                stats['currency'].append({
                    'cell': i,
                    'match': match.group(0),
                    'context': context
                })

            # Find escaped currency
            for match in ESCAPED_CURRENCY_RE.finditer(text):
                stats['escaped_currency'].append({
                    'cell': i,
                    'match': match.group(0)
                })

            # Find display math
            for match in DISPLAY_MATH_RE.finditer(text):
                stats['display_math'].append({
                    'cell': i,
                    'preview': match.group(0)[:50] + '...'
                })

            # Find inline math (excluding currency)
            temp_text = CURRENCY_RE.sub('', text)  # Remove currency first
            for match in INLINE_MATH_RE.finditer(temp_text):
                # Filter out likely currency that regex missed
                content = match.group(0)
                if not re.match(r'\$\d+', content):
                    stats['inline_math'].append({
                        'cell': i,
                        'match': content[:30]
                    })

    return stats

def print_report(all_stats):
    """Print comprehensive report."""
    print("\n" + "="*70)
    print("DOLLAR SIGN VERIFICATION REPORT")
    print("="*70)

    total_currency = sum(len(stats['currency']) for stats in all_stats.values())
    total_escaped = sum(len(stats['escaped_currency']) for stats in all_stats.values())
    total_display_math = sum(len(stats['display_math']) for stats in all_stats.values())
    total_inline_math = sum(len(stats['inline_math']) for stats in all_stats.values())

    print(f"\nOVERALL SUMMARY:")
    print(f"  Notebooks analyzed: {len(all_stats)}")
    print(f"  Currency patterns (need escaping): {total_currency}")
    print(f"  Already escaped currency: {total_escaped}")
    print(f"  Display math blocks (preserve): {total_display_math}")
    print(f"  Inline math expressions (preserve): {total_inline_math}")

    print(f"\nPER-NOTEBOOK BREAKDOWN:")
    print(f"{'Notebook':<50} {'Currency':>10} {'Escaped':>10} {'Display':>10} {'Inline':>10}")
    print("-"*90)

    for filename in sorted(all_stats.keys()):
        stats = all_stats[filename]
        print(f"{filename:<50} {len(stats['currency']):>10} {len(stats['escaped_currency']):>10} "
              f"{len(stats['display_math']):>10} {len(stats['inline_math']):>10}")

    print("\nTOP 5 NOTEBOOKS BY CURRENCY INSTANCES:")
    sorted_by_currency = sorted(all_stats.items(), key=lambda x: len(x[1]['currency']), reverse=True)
    for filename, stats in sorted_by_currency[:5]:
        print(f"  {filename}: {len(stats['currency'])} currency instances")

    print("\nSAMPLE CURRENCY PATTERNS (first 5):")
    count = 0
    for filename, stats in sorted_by_currency:
        for item in stats['currency'][:2]:
            if count >= 5:
                break
            print(f"  {filename} (cell {item['cell']}): {item['match']}")
            print(f"    Context: ...{item['context']}...")
            count += 1

    print("\n" + "="*70)

def main():
    if len(sys.argv) > 1:
        files = [Path(arg) for arg in sys.argv[1:]]
    else:
        files = sorted(Path('notebooks_colab').glob('ch*.ipynb'))

    all_stats = {}

    for filepath in files:
        stats = analyze_notebook(filepath)
        all_stats[filepath.name] = stats

    print_report(all_stats)

if __name__ == '__main__':
    main()
