#!/usr/bin/env python3
"""
Improve CH06 standardization: 88 → 90+

Fixes:
1. Reorder: Move Case Studies after Practice Exercises
2. Add 2 transition notes
"""

import json

NOTEBOOK = 'notebooks_colab/ch06_The_Least_Squares_Estimator.ipynb'

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

    # Phase 1: Reorder sections
    # Find Case Studies start and Key Takeaways start
    case_idx = find_cell_with(cells, '## 6.5 Case Studies')
    takeaways_idx = find_cell_with(cells, '## Key Takeaways')
    exercises_idx = find_cell_with(cells, '## Practice Exercises')

    print(f"Current order: Case Studies({case_idx}), Key Takeaways({takeaways_idx}), Practice Exercises({exercises_idx})")

    if case_idx and takeaways_idx and exercises_idx and case_idx < takeaways_idx:
        # Extract case study cells (from case_idx to takeaways_idx-1)
        case_cells = cells[case_idx:takeaways_idx]
        print(f"  Case Studies block: {len(case_cells)} cells ({case_idx} to {takeaways_idx-1})")

        # Remove case study cells from current position
        del cells[case_idx:takeaways_idx]

        # Now find the new position of Practice Exercises (shifted after removal)
        exercises_idx_new = find_cell_with(cells, '## Practice Exercises')

        # Find the end of Practice Exercises section
        # It's the last cell, or the next H2 section after it
        exercises_end = len(cells)  # default to end
        for i in range(exercises_idx_new + 1, len(cells)):
            src = ''.join(cells[i].get('source', []))
            if src.strip().startswith('## ') and 'Practice' not in src:
                exercises_end = i
                break

        # Insert case study cells after Practice Exercises
        for j, cc in enumerate(case_cells):
            cells.insert(exercises_end + j, cc)

        print(f"Phase 1: Moved Case Studies after Practice Exercises")

        # Verify new order
        new_takeaways = find_cell_with(cells, '## Key Takeaways')
        new_exercises = find_cell_with(cells, '## Practice Exercises')
        new_case = find_cell_with(cells, '## 6.5 Case Studies')
        print(f"  New order: Key Takeaways({new_takeaways}), Practice Exercises({new_exercises}), Case Studies({new_case})")

    # Phase 2: Add transition notes (bottom-to-top)

    # Transition before 6.4 Estimators of Model Parameters
    idx = find_cell_with(cells, '## 6.4 Estimators of Model Parameters')
    if idx:
        cells.insert(idx, make_md_cell(
            "*Now that we understand the theoretical properties of OLS estimators, "
            "let's examine how to estimate the model parameters in practice.*"
        ))
        print(f"Phase 2a: Added transition before 6.4 at index {idx}")

    # Transition before 6.3 Properties
    idx = find_cell_with(cells, '## 6.3 Properties of the Least Squares')
    if idx:
        cells.insert(idx, make_md_cell(
            "*Having seen how sampling variability affects regression estimates, "
            "let's formalize the key properties of the OLS estimator.*"
        ))
        print(f"Phase 2b: Added transition before 6.3 at index {idx}")

    # Save
    nb['cells'] = cells
    with open(NOTEBOOK, 'w') as f:
        json.dump(nb, f, indent=1, ensure_ascii=False)

    md = sum(1 for c in cells if c['cell_type'] == 'markdown')
    print(f"\nAfter: {len(cells)} cells ({md} markdown, {len(cells)-md} code)")

if __name__ == '__main__':
    main()
