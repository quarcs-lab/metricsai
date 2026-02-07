#!/usr/bin/env python3
"""
Improve CH04 standardization: 84 → 90+

Fixes:
1. Remove redundant Learning Objectives cell (Cell 1)
2. Merge adjacent Key Concepts to reduce from 14 to ~10
3. Add 2 transition notes
4. Add empty closing cell
"""

import json
import re

NOTEBOOK = 'notebooks_colab/ch04_Statistical_Inference_for_the_Mean.ipynb'

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

    # Count initial Key Concepts
    kc_cells = []
    for i, cell in enumerate(cells):
        src = ''.join(cell.get('source', []))
        if cell['cell_type'] == 'markdown' and 'Key Concept' in src:
            kc_cells.append(i)
    print(f"Initial Key Concepts: {len(kc_cells)} at cells {kc_cells}")

    # Phase 1: Remove redundant Learning Objectives (Cell 1)
    cell1_src = ''.join(cells[1].get('source', []))
    assert '## Learning Objectives' in cell1_src, f"Cell 1 is not LO! Got: {cell1_src[:50]}"

    cells.pop(1)
    print("Phase 1: Removed redundant Learning Objectives cell")
    # All indices shift down by 1

    # Phase 2: Merge adjacent Key Concepts to reduce count
    # After removing cell 1, old indices shift:
    # Old 11,12 → New 10,11 (both about t-distribution, merge into one)
    # Old 41,42 → New 40,41 (contextual interpretation + testing pattern, merge)

    # Find the specific KCs to merge by content
    # Merge pair 1: Two KCs about t-distribution (adjacent)
    idx_t1 = None
    idx_t2 = None
    for i in range(len(cells) - 1):
        src1 = ''.join(cells[i].get('source', []))
        src2 = ''.join(cells[i+1].get('source', []))
        if ('Key Concept' in src1 and 't-distribution is used' in src1 and
            'Key Concept' in src2 and 't-distribution is similar' in src2):
            idx_t1 = i
            idx_t2 = i + 1
            break

    if idx_t1 is not None:
        # Merge: keep first, combine content, remove second
        src1 = ''.join(cells[idx_t1].get('source', []))
        src2 = ''.join(cells[idx_t2].get('source', []))
        # Extract the second KC's content (after the > **Key Concept** prefix)
        # Combine into one comprehensive KC
        merged = (
            "> **Key Concept: The t-Distribution**\n"
            ">\n"
            "> The t-distribution is used when the population standard deviation $\\sigma$ is unknown "
            "and must be estimated from the sample. It is similar to the standard normal N(0,1) "
            "but with fatter tails that reflect the additional uncertainty from estimating $\\sigma$. "
            "As the sample size $n$ grows, the t-distribution approaches the normal distribution, "
            "making the normal a good approximation for large samples."
        )
        cells[idx_t1]['source'] = [merged]
        cells.pop(idx_t2)
        print(f"Phase 2a: Merged t-distribution KCs at {idx_t1}-{idx_t2}")

    # Merge pair 2: Two adjacent KCs about hypothesis testing context
    idx_h1 = None
    idx_h2 = None
    for i in range(len(cells) - 1):
        src1 = ''.join(cells[i].get('source', []))
        src2 = ''.join(cells[i+1].get('source', []))
        if ('Key Concept' in src1 and 'Contextual Interpretation' in src1 and
            'Key Concept' in src2 and 'hypothesis testing pattern' in src2):
            idx_h1 = i
            idx_h2 = i + 1
            break

    if idx_h1 is not None:
        merged = (
            "> **Key Concept: Context and Consistency in Hypothesis Testing**\n"
            ">\n"
            "> Statistical results gain meaning only through economic context -- a statistically "
            "significant coefficient matters because of what it implies for policy, behavior, or theory. "
            "The hypothesis testing pattern (set up hypotheses, compute test statistic, compare to critical "
            "value or p-value) is consistent across diverse applications, from wage analysis to "
            "macroeconomic growth."
        )
        cells[idx_h1]['source'] = [merged]
        cells.pop(idx_h2)
        print(f"Phase 2b: Merged context/consistency KCs at {idx_h1}-{idx_h2}")

    # Merge pair 3: Confidence interval KCs (old 14 and 18 → find them)
    idx_ci1 = None
    idx_ci2 = None
    for i in range(len(cells)):
        src = ''.join(cells[i].get('source', []))
        if 'Key Concept' in src and 'confidence interval provides a range' in src.lower():
            if idx_ci1 is None:
                idx_ci1 = i
            else:
                idx_ci2 = i
                break

    if idx_ci1 is not None and idx_ci2 is not None:
        merged = (
            "> **Key Concept: Confidence Intervals**\n"
            ">\n"
            "> A confidence interval provides a range of plausible values for the population "
            "parameter $\\mu$. A 95% confidence interval means: if we repeated the sampling procedure "
            "many times, approximately 95% of the resulting intervals would contain the true $\\mu$. "
            "The interval is constructed as $\\bar{x} \\pm t_{\\alpha/2} \\times se(\\bar{x})$, where "
            "wider intervals indicate less precision."
        )
        cells[idx_ci1]['source'] = [merged]
        cells.pop(idx_ci2)
        print(f"Phase 2c: Merged confidence interval KCs at {idx_ci1} and {idx_ci2}")

    # Phase 3: Add transition notes (bottom-to-top)
    # Transition before 4.6 One-Sided Tests
    idx = find_cell_with(cells, '## 4.6 One-Sided')
    if idx:
        cells.insert(idx, make_md_cell(
            "*Having mastered two-sided hypothesis tests, let's now consider "
            "situations where we have a directional prediction.*"
        ))
        print(f"Phase 3a: Added transition before 4.6 at index {idx}")

    # Transition before 4.4 Two-Sided Tests
    idx = find_cell_with(cells, '## 4.4 Two-Sided')
    if idx:
        cells.insert(idx, make_md_cell(
            "*Now that we understand confidence intervals, let's formalize "
            "the process of testing specific hypotheses about the population mean.*"
        ))
        print(f"Phase 3b: Added transition before 4.4 at index {idx}")

    # Phase 4: Add empty closing cell
    last_src = ''.join(cells[-1].get('source', []))
    if last_src.strip():
        cells.append(make_md_cell(''))
        print("Phase 4: Added empty closing cell")

    # Save
    nb['cells'] = cells
    with open(NOTEBOOK, 'w') as f:
        json.dump(nb, f, indent=1, ensure_ascii=False)

    # Final count
    kc_final = sum(1 for c in cells if c['cell_type'] == 'markdown' and 'Key Concept' in ''.join(c.get('source', [])))
    md = sum(1 for c in cells if c['cell_type'] == 'markdown')
    print(f"\nAfter: {len(cells)} cells ({md} markdown, {len(cells)-md} code)")
    print(f"Key Concepts: {kc_final}")

if __name__ == '__main__':
    main()
