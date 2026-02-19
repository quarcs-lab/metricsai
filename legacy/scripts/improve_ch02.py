#!/usr/bin/env python3
"""
Improve CH02 standardization: 86 → 90+

Fixes:
1. Remove redundant Learning Objectives cell (Cell 1)
2. Add 2 transition notes
"""

import json

NOTEBOOK = 'notebooks_colab/ch02_Univariate_Data_Summary.ipynb'

def make_md_cell(source):
    return {"cell_type": "markdown", "metadata": {}, "source": [source]}

def find_cell_with(cells, text_pattern, start=0):
    for i in range(start, len(cells)):
        src = ''.join(cells[i].get('source', []))
        if text_pattern in src:
            return i
    return None

def main():
    with open(NOTEBOOK) as f:
        nb = json.load(f)
    cells = nb['cells']
    print(f"Before: {len(cells)} cells")

    # Phase 1: Remove redundant Learning Objectives (Cell 1)
    cell1_src = ''.join(cells[1].get('source', []))
    assert '## Learning Objectives' in cell1_src, f"Cell 1 is not LO! Got: {cell1_src[:50]}"
    cell2_src = ''.join(cells[2].get('source', []))
    assert '## Chapter Overview' in cell2_src, "Cell 2 is not Overview!"

    cells.pop(1)
    print("Phase 1: Removed redundant Learning Objectives cell")

    # Phase 2: Add transition notes (bottom-to-top)

    # Transition before 2.5 Data Transformation (from categorical to transformation)
    idx = find_cell_with(cells, '## 2.5 Data Transformation')
    if idx:
        cells.insert(idx, make_md_cell(
            "*Having explored charts for both numerical and categorical data, "
            "let's now examine how data transformations can reveal hidden patterns.*"
        ))
        print(f"Phase 2a: Added transition before 2.5 at index {idx}")

    # Transition before 2.3 Charts by Category (from single-variable to grouped)
    idx = find_cell_with(cells, '## 2.3 Charts for Numerical Data by Category')
    if idx:
        cells.insert(idx, make_md_cell(
            "*Now that we can visualize single-variable distributions, "
            "let's see how distributions differ across categories.*"
        ))
        print(f"Phase 2b: Added transition before 2.3 at index {idx}")

    # Save
    nb['cells'] = cells
    with open(NOTEBOOK, 'w') as f:
        json.dump(nb, f, indent=1, ensure_ascii=False)

    md = sum(1 for c in cells if c['cell_type'] == 'markdown')
    print(f"\nAfter: {len(cells)} cells ({md} markdown, {len(cells)-md} code)")

if __name__ == '__main__':
    main()
