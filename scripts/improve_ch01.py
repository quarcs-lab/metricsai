#!/usr/bin/env python3
"""
Improve CH01 standardization: 83 → 90+

Fixes:
1. Remove redundant Learning Objectives cell (Cell 1)
2. Add 2 Key Concept boxes (after 1.5 and 1.7)
3. Add 2 transition notes
"""

import json

NOTEBOOK = 'notebooks_colab/ch01_Analysis_of_Economics_Data.ipynb'

def make_md_cell(source):
    return {
        "cell_type": "markdown",
        "metadata": {},
        "source": [source]
    }

def main():
    with open(NOTEBOOK) as f:
        nb = json.load(f)

    cells = nb['cells']
    print(f"Before: {len(cells)} cells")

    # ============================================================
    # Phase 1: Remove redundant Learning Objectives (Cell 1)
    # Cell 1 has standalone "## Learning Objectives"
    # Cell 2 has Chapter Overview with "What you'll learn"
    # Template requires only ONE. Keep the integrated form.
    # ============================================================

    # Verify Cell 1 is the Learning Objectives cell
    cell1_src = ''.join(cells[1].get('source', []))
    assert '## Learning Objectives' in cell1_src, "Cell 1 is not Learning Objectives!"

    # Verify Cell 2 has the Chapter Overview with integrated LOs
    cell2_src = ''.join(cells[2].get('source', []))
    assert '## Chapter Overview' in cell2_src, "Cell 2 is not Chapter Overview!"
    assert "What you'll learn" in cell2_src, "Cell 2 missing 'What you'll learn'!"

    # Remove Cell 1
    cells.pop(1)
    print("Phase 1: Removed redundant Learning Objectives cell")

    # After removal, all indices shift down by 1:
    # Old Cell 2 (Overview) → New Cell 1
    # Old Cell 5 (1.1) → New Cell 4
    # etc.

    # ============================================================
    # Phase 2: Add Key Concept boxes (work bottom-to-top)
    # Current KCs at (old indices): 6, 15, 20, 28, 34, 42 → (new): 5, 14, 19, 27, 33, 41
    # Sections without KCs: 1.2(old 7→new 6), 1.3(9→8), 1.5(16→15), 1.7(22→21), 1.8(24→23)
    # Add KC after 1.7 Interpreting Results (new cell 21→insert after 22)
    # Add KC after 1.5 Visualizing (new cell 15→insert after 17, since code cell at 16)
    # ============================================================

    # Find exact positions by searching for section headers (more robust than hardcoded indices)
    def find_cell_with(text_pattern, start=0):
        for i in range(start, len(cells)):
            src = ''.join(cells[i].get('source', []))
            if text_pattern in src:
                return i
        return None

    # KC after 1.7 Interpreting Results
    # Insert after the last cell in section 1.7 (before 1.8 starts)
    sec_18_idx = find_cell_with('## 1.8 Visualizing the Fitted Line')
    if sec_18_idx:
        kc_interpreting = make_md_cell(
            "> **Key Concept: Reading Regression Output**\n"
            ">\n"
            "> The key elements of regression output are: the coefficient estimate "
            "(magnitude and direction of the relationship), the standard error "
            "(precision of the estimate), the t-statistic and p-value "
            "(statistical significance), and R-squared (proportion of variation explained). "
            "Together, these tell us whether the relationship is economically meaningful "
            "and statistically reliable."
        )
        cells.insert(sec_18_idx, kc_interpreting)
        print(f"Phase 2a: Added Key Concept after 1.7 at index {sec_18_idx}")

    # KC after 1.5 Visualizing the Relationship
    # Insert after the code cell that creates the scatter plot (before 1.6)
    sec_16_idx = find_cell_with('## 1.6 Fitting a Regression Line')
    if sec_16_idx:
        kc_visualizing = make_md_cell(
            "> **Key Concept: Visual Exploration Before Regression**\n"
            ">\n"
            "> Always plot your data before running a regression. Scatter plots reveal "
            "the direction, strength, and form of relationships between variables, "
            "and can expose outliers or nonlinearities that summary statistics alone would miss. "
            "Visual exploration is the essential first step in any empirical analysis."
        )
        cells.insert(sec_16_idx, kc_visualizing)
        print(f"Phase 2b: Added Key Concept after 1.5 at index {sec_16_idx}")

    # ============================================================
    # Phase 3: Add transition notes (work bottom-to-top)
    # Need 1-2 more transitions (currently 1)
    # ============================================================

    # Transition between data exploration (1.4) and visualization (1.5)
    sec_15_idx = find_cell_with('## 1.5 Visualizing the Relationship')
    if sec_15_idx:
        trans_visual = make_md_cell(
            "*Now that we have explored the data numerically, let's visualize "
            "the relationship between house size and price.*"
        )
        cells.insert(sec_15_idx, trans_visual)
        print(f"Phase 3a: Added transition before 1.5 at index {sec_15_idx}")

    # Transition between fitted line (1.8) and economic interpretation (1.9)
    sec_19_idx = find_cell_with('## 1.9 Economic Interpretation')
    if sec_19_idx:
        trans_econ = make_md_cell(
            "*Having fitted and visualized our regression model, let's now "
            "interpret what these results mean in economic terms.*"
        )
        cells.insert(sec_19_idx, trans_econ)
        print(f"Phase 3b: Added transition before 1.9 at index {sec_19_idx}")

    # ============================================================
    # Save
    # ============================================================
    nb['cells'] = cells
    with open(NOTEBOOK, 'w') as f:
        json.dump(nb, f, indent=1, ensure_ascii=False)

    md_count = sum(1 for c in cells if c['cell_type'] == 'markdown')
    code_count = sum(1 for c in cells if c['cell_type'] == 'code')
    print(f"\nAfter: {len(cells)} cells ({md_count} markdown, {code_count} code)")
    print("Done! Run verify_chapter.py ch01 to check score.")

if __name__ == '__main__':
    main()
