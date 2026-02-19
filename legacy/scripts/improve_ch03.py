#!/usr/bin/env python3
"""
Improve CH03 standardization: 86 → 90+

Fixes:
1. Remove redundant Learning Objectives cell (Cell 1)
2. Add 1 transition note
3. Add empty closing cell
"""

import json

NOTEBOOK = 'notebooks_colab/ch03_The_Sample_Mean.ipynb'

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

    cells.pop(1)
    print("Phase 1: Removed redundant Learning Objectives cell")

    # Phase 2: Add transition note (bottom-to-top)
    # Transition before 3.5 Estimator Properties (from applied examples to theory)
    idx = find_cell_with(cells, '## 3.5 Estimator Properties')
    if idx:
        cells.insert(idx, make_md_cell(
            "*Having seen the Central Limit Theorem at work with both coins and census data, "
            "let's formalize what makes the sample mean a good estimator.*"
        ))
        print(f"Phase 2: Added transition before 3.5 at index {idx}")

    # Phase 3: Add empty closing cell
    last_src = ''.join(cells[-1].get('source', []))
    if last_src.strip():  # Not already empty
        cells.append(make_md_cell(''))
        print("Phase 3: Added empty closing cell")

    # Save
    nb['cells'] = cells
    with open(NOTEBOOK, 'w') as f:
        json.dump(nb, f, indent=1, ensure_ascii=False)

    md = sum(1 for c in cells if c['cell_type'] == 'markdown')
    print(f"\nAfter: {len(cells)} cells ({md} markdown, {len(cells)-md} code)")

if __name__ == '__main__':
    main()
