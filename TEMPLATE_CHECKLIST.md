# Master Template Checklist for Jupyter Notebook Chapters

**Created:** 2026-02-04
**Based on:** Consistency evaluation of Chapters 1-4
**Reference:** CH02 (Univariate Data Summary) - Gold standard implementation

---

## Purpose

This checklist ensures all chapters (CH01-CH17) maintain consistent structure, formatting, and pedagogical quality. Use this BEFORE marking any chapter "complete" to prevent inconsistencies discovered during the CH01-04 evaluation.

---

## Pre-Flight Checks (Before Starting Chapter)

- [ ] Review CH02 reference implementation
- [ ] Review this checklist completely
- [ ] Identify chapter-specific requirements (datasets, statistical methods, etc.)
- [ ] Plan section structure (how many sections, case study topic, etc.)

---

## Section 1: Title Page and Front Matter

### Cell 0: Chapter Title Page

**Required Elements (in order):**

```markdown
# Chapter X: [Chapter Title]

**metricsAI: An Introduction to Econometrics with Python and AI in the Cloud**

*[Carlos Mendez](https://carlos-mendez.org)*

<img src="https://raw.githubusercontent.com/quarcs-lab/metricsai/main/images/ch0X_visual_summary.jpg" alt="Chapter 0X Visual Summary" width="65%">

[Brief description paragraph...]

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](...)
```

**Checklist:**
- [ ] Chapter number and title on first line
- [ ] Blank line after title
- [ ] Book subtitle with double asterisks
- [ ] Blank line after subtitle
- [ ] Author name with link in italics
- [ ] Blank line after author
- [ ] Visual summary image (65% width, proper alt text)
- [ ] Blank line after image
- [ ] Description paragraph (2-4 sentences)
- [ ] Blank line before Colab badge
- [ ] Colab badge with working link
- [ ] All elements properly separated (no text running together)

**Visual Summary Image:**
- [ ] Image exists at specified URL
- [ ] Width exactly "65%"
- [ ] Alt text format: "Chapter 0X Visual Summary"
- [ ] Image displays in notebook
- [ ] Image displays in PDF

---

### Cell 1: Learning Objectives

**Format:**

```markdown
## Learning Objectives

By the end of this chapter, you will be able to:

- [Objective 1...]
- [Objective 2...]
- [Objective 3...]
[... 6-10 objectives total]
```

**Checklist:**
- [ ] Header: "## Learning Objectives"
- [ ] Blank line after header
- [ ] Introductory sentence ("By the end...")
- [ ] Blank line before first bullet
- [ ] Each bullet starts with action verb (Understand, Calculate, Interpret, etc.)
- [ ] 6-10 objectives total
- [ ] Each objective on separate line (no running together)
- [ ] Objectives align with chapter content

---

### Cell 2: Chapter Overview

**Format:**

```markdown
## Chapter Overview

[Opening paragraph describing chapter focus...]

**What you'll learn:**

- [Key skill/concept 1]
- [Key skill/concept 2]
[... 5-7 items]

**Datasets used:**

- **DATASET_NAME.DTA**: Description of dataset
- **DATASET_NAME.DTA**: Description of dataset
[... 2-4 datasets]

**Chapter outline:**

1. **X.1 [Section Title]** - Brief description
2. **X.2 [Section Title]** - Brief description
[... all main sections]
```

**Checklist:**
- [ ] Header: "## Chapter Overview"
- [ ] Opening paragraph (2-3 sentences)
- [ ] "What you'll learn" section with bullets
- [ ] "Datasets used" section with dataset names in bold
- [ ] "Chapter outline" section listing all main sections
- [ ] Each dataset has clear description
- [ ] Outline matches actual section numbers in chapter
- [ ] Professional formatting with proper spacing

---

### Cell 3-4: Setup Section

**Cell 3 (Markdown):**

```markdown
## 🔧 Setup

Before we begin, let's import the necessary Python packages...
```

**Cell 4 (Code):**

```python
# Core packages
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats

# Set random seed for reproducibility
np.random.seed(42)

# Configure plotting
plt.style.use('seaborn-v0_8-darkgrid')
%matplotlib inline
```

**Checklist:**
- [ ] Setup header with emoji: "## 🔧 Setup"
- [ ] Brief explanation in markdown cell
- [ ] Code cell follows immediately
- [ ] All necessary imports included
- [ ] Random seed set (if needed)
- [ ] Plotting configuration included
- [ ] Comments in code cell
- [ ] Code runs without errors

---

## Section 2: Main Content Sections

### Section Numbering

**Pattern:** X.1, X.2, X.3, ... X.N

**Checklist:**
- [ ] Sequential numbering (OR documented gaps if reserving sections)
- [ ] Each section has header: "## X.Y [Section Title]"
- [ ] Section numbers match Chapter Overview outline
- [ ] No duplicate section numbers
- [ ] If gaps exist, documented reason (e.g., "X.10 reserved for future content")

**Acceptable Patterns:**
- ✅ Sequential: 1.1, 1.2, 1.3, 1.4, 1.5
- ✅ With documented gaps: 2.1-2.6, 2.8 (2.7 reserved)
- ❌ Random gaps: 3.1, 3.3, 3.7 (without explanation)

---

### Content Organization

**Each section should include:**

**Markdown Content:**
- [ ] Section header (## X.Y Title)
- [ ] Introduction paragraph
- [ ] Conceptual explanation
- [ ] Mathematical formulas (if applicable)
- [ ] Interpretation guidance

**Code Demonstrations:**
- [ ] Relevant code examples
- [ ] Clear comments
- [ ] Output interpretation
- [ ] Visualizations (when appropriate)

**Key Concept Boxes:**
- [ ] At least 1 Key Concept per section (or every 2-3 sections)
- [ ] Placed AFTER explaining the concept
- [ ] Uses blockquote format (see below)

---

### Key Concept Box Format

**Standard Format:**

```markdown
> **Key Concept: [Descriptive Title]**
>
> [Clear explanation of the concept, 2-4 sentences. Include formulas if relevant.]
>
> [Optional: Example or application.]
```

**Checklist per Key Concept:**
- [ ] Blockquote syntax (> at start of each line)
- [ ] Bold title: "**Key Concept: [Title]**"
- [ ] Blank line after title (within blockquote)
- [ ] Clear, concise explanation (2-4 sentences)
- [ ] Proper formatting (no text running together)
- [ ] Renders with purple border in PDF

**Minimum Standard:**
- [ ] **Total: 7-11 Key Concept boxes** per chapter
- [ ] Distribution: At least 1 box per 2-3 sections
- [ ] Strategic placement after important concepts

---

## Section 3: Closing Sections

### Key Takeaways Section

**Format:**

```markdown
## Key Takeaways

**[Topic 1 Heading]:**

1. [Key point 1...]
2. [Key point 2...]

**[Topic 2 Heading]:**

1. [Key point 1...]
2. [Key point 2...]

[... 5-7 topic headings with points]

**Next Steps:**

In the next chapter, we will...

**What You've Achieved:**

✓ [Achievement 1]
✓ [Achievement 2]
[... 4-6 achievements]
```

**Checklist:**
- [ ] Header: "## Key Takeaways"
- [ ] 5-7 major topic headings
- [ ] Each topic has 2-5 bullet points
- [ ] Comprehensive (covers all main concepts)
- [ ] "Next Steps" section (preview next chapter)
- [ ] "What You've Achieved" section (checkmarks)
- [ ] Proper spacing between elements
- [ ] No text running together

---

### Practice Exercises Section

**Format:**

```markdown
## Practice Exercises

Test your understanding with these exercises:

**Exercise 1: [Title]**

[Problem description...]

**Exercise 2: [Title]**

[Problem description...]

[... 6-10 exercises]
```

**Checklist:**
- [ ] Header: "## Practice Exercises"
- [ ] Introductory sentence
- [ ] 6-10 exercises total
- [ ] Each exercise has bold title
- [ ] Clear problem statements
- [ ] Progressive difficulty (easy → hard)
- [ ] Covers main chapter concepts
- [ ] Mix of conceptual and computational problems

---

## Section 4: Case Study (If Applicable)

### When to Include Case Study

**Include case study for:**
- ✅ Applied chapters (statistical methods, regression, inference)
- ✅ Chapters with multiple techniques to integrate
- ✅ Chapters building on previous methods

**Exclude case study for:**
- ❌ Purely theoretical chapters (e.g., CH03: Sample Mean theory)
- ❌ Introductory chapters (e.g., CH00: Preface)

**Decision Rule:** If chapter teaches practical methods, include case study

---

### Case Study Structure

**Required Components:**

1. **Section Header** (numbered)
2. **Research Question** (markdown)
3. **Economic Context** (markdown)
4. **Key Concept Box 1** (methodological or analytical)
5. **Data Loading** (code cell)
6. **Instructions** (markdown: "How to Use These Tasks")
7. **Task 1: GUIDED**
8. **Task 2: SEMI-GUIDED**
9. **Task 3: SEMI-GUIDED**
10. **Key Concept Box 2** (interpretation or significance)
11. **Task 4: MORE INDEPENDENT**
12. **Task 5: INDEPENDENT**
13. **Task 6: INDEPENDENT**
14. **Wrap-up: What You've Learned**

**Total: 13-15 cells** for complete case study

---

### Case Study Section Header

**Format:**

```markdown
## X.Y Case Study: [Descriptive Title]

**Research Question:** "[Clear economic or statistical question]"

[2-3 paragraphs of context...]
```

**Checklist:**
- [ ] Numbered section (X.8 or X.11 typically)
- [ ] "Case Study:" in header
- [ ] Research question clearly stated
- [ ] Economic/statistical context provided
- [ ] Connects to chapter methods

---

### Case Study Tasks - Format Standards

**Task Header Format:**

```markdown
#### Task N: [Descriptive Title] (DIFFICULTY_LEVEL)

**Objective:** [What student will learn/do]

**Instructions:**

[Step-by-step guidance, level depends on difficulty]

**Questions to answer:**

1. [Question 1]
2. [Question 2]
```

**Difficulty Levels and Labels:**

| Task | Label | Code Provided | Hints | Independence |
|------|-------|---------------|-------|--------------|
| Task 1 | (GUIDED) | Full code with 4-6 blanks | Extensive | Low |
| Task 2 | (SEMI-GUIDED) | Partial code with 6-8 blanks | Moderate | Medium-Low |
| Task 3 | (SEMI-GUIDED) | Code structure with blanks | Moderate | Medium |
| Task 4 | (MORE INDEPENDENT) | Outline only | Minimal | Medium-High |
| Task 5 | (INDEPENDENT) | Steps only | Very minimal | High |
| Task 6 | (INDEPENDENT) | Objective only | None | Very High |

**Checklist for Each Task:**
- [ ] Header uses #### (4 hashes)
- [ ] Difficulty label in ALL CAPS in parentheses
- [ ] Clear objective stated
- [ ] Instructions appropriate for difficulty level
- [ ] Economic interpretation emphasized
- [ ] Progressive difficulty maintained

---

### Case Study Key Concepts

**Required: Exactly 2 Key Concept boxes within case study**

**Placement:**
- **Key Concept 1:** Early in case study (after context, before tasks)
  - Focus: Methodological, analytical, or "why this matters"
- **Key Concept 2:** Middle of case study (between Task 3 and Task 4)
  - Focus: Interpretation, significance, or practical application

**Checklist:**
- [ ] Exactly 2 Key Concept boxes (not 1, not 3)
- [ ] First box: Methodological/analytical focus
- [ ] Second box: Interpretation/significance focus
- [ ] Both use proper blockquote format
- [ ] Both relate to case study content

---

### Case Study Wrap-up

**Format:**

```markdown
#### What You've Learned from This Case Study

Through this hands-on analysis, you have:

- ✓ [Skill/concept learned 1]
- ✓ [Skill/concept learned 2]
- ✓ [Skill/concept learned 3]
[... 5-7 items]

**Economic Insights:**

[2-3 sentences about economic findings]

**Statistical Skills:**

[2-3 sentences about methods mastered]

**Next Steps:**

[1-2 sentences connecting to future chapters]
```

**Checklist:**
- [ ] Header: "#### What You've Learned from This Case Study"
- [ ] Bulleted list with checkmarks (5-7 items)
- [ ] Economic insights section
- [ ] Statistical skills section
- [ ] Next steps/forward connection
- [ ] Professional summary of learning

---

## Section 5: Technical Quality Checks

### Markdown Cell Validation

**Run this check BEFORE generating PDF:**

```python
import json

nb = json.load(open('notebooks_colab/ch0X_*.ipynb'))

issues = 0
for i, cell in enumerate(nb['cells']):
    if cell['cell_type'] == 'markdown':
        source = cell['source']

        # Check 1: Newline characters
        missing_newlines = sum(1 for line in source if not line.endswith('\n'))
        if missing_newlines > 0:
            print(f'⚠️  Cell {i}: {missing_newlines} lines missing \\n')
            issues += 1

        # Check 2: Character-by-character corruption
        if len(source) > 50:
            content = ''.join(source[:50])
            if '\n' in content[:10] and len(content[:10]) < 20:
                print(f'🚩 Cell {i}: {len(source)} lines - character-by-character corruption')
                issues += 1

        # Check 3: Header spacing
        content = ''.join(source)
        if '##' in content and not any(f'##\n\n' in content or f'## ' in content):
            print(f'⚠️  Cell {i}: Header may be missing spacing')
            issues += 1

if issues == 0:
    print('✅ All markdown cells look good!')
else:
    print(f'\n❌ Found {issues} potential issues - fix before generating PDF')
```

**Checklist:**
- [ ] All markdown lines end with `\n`
- [ ] No character-by-character corruption (>100 lines for simple text)
- [ ] Headers have proper spacing (##\n\n not ##Text)
- [ ] No text running together

---

### Code Cell Validation

**Checklist:**
- [ ] All code cells have content (no empty cells)
- [ ] All code cells run without errors
- [ ] All imports are used
- [ ] Random seeds set where needed
- [ ] Comments explain non-obvious code
- [ ] Output displays correctly
- [ ] Visualizations render properly

---

### PDF Generation Workflow

**Step 1: Convert to HTML**
```bash
cd notebooks_colab && jupyter nbconvert --to html ch0X_*.ipynb && cd ..
```

**Step 2: Inject CSS**
```bash
python3 inject_print_css.py notebooks_colab/ch0X_*.html notebooks_colab/ch0X_*_printable.html
```

**Step 3: Generate PDF**
```bash
python3 generate_pdf_playwright.py ch0X
```

**Step 4: Verify PDF**
```bash
ls -lh notebooks_colab/ch0X_*.pdf
open notebooks_colab/ch0X_*.pdf
```

**Checklist:**
- [ ] HTML conversion completes (warnings acceptable for missing alt text)
- [ ] CSS injection succeeds
- [ ] PDF generation completes
- [ ] PDF size: 1.0-2.0 MB (reasonable range)
- [ ] PDF opens and displays correctly
- [ ] Visual summary image displays
- [ ] Key Concept boxes have purple borders
- [ ] Code blocks have proper formatting
- [ ] Tables fit without wrapping
- [ ] No text running together
- [ ] Professional appearance throughout

---

## Section 6: Content Quality Standards

### Writing Quality

**Checklist:**
- [ ] Clear, professional academic tone
- [ ] Consistent terminology throughout
- [ ] Proper capitalization
- [ ] Correct grammar and punctuation
- [ ] No typos (run spellcheck)
- [ ] Active voice preferred
- [ ] Technical terms defined on first use

---

### Pedagogical Quality

**Checklist:**
- [ ] Learning Objectives align with content
- [ ] Concepts build progressively
- [ ] Examples support theory
- [ ] Interpretations provided for all results
- [ ] Economic relevance emphasized
- [ ] Student-centered language ("you will...", "we can...")
- [ ] Balance of theory and application
- [ ] Clear transitions between sections

---

### Technical Accuracy

**Checklist:**
- [ ] All formulas correct
- [ ] Statistical methods properly applied
- [ ] Code produces expected results
- [ ] Interpretations match output
- [ ] Data descriptions accurate
- [ ] Citations included where needed
- [ ] No mathematical errors

---

## Section 7: Final Pre-Submission Checklist

### Structure Verification

- [ ] Cell 0: Title page (all elements present and separated)
- [ ] Cell 1: Learning Objectives (6-10 bullets, proper formatting)
- [ ] Cell 2: Chapter Overview (datasets + outline included)
- [ ] Cell 3-4: Setup (markdown + code)
- [ ] Main sections: X.1 through X.N (sequential or documented gaps)
- [ ] Key Concepts: 7-11 total (strategic placement)
- [ ] Key Takeaways: Present and comprehensive
- [ ] Practice Exercises: 6-10 exercises
- [ ] Case Study: Present if applicable (6 tasks, 2 Key Concepts)
- [ ] No empty closing cells

---

### Consistency Verification

**Compare with CH02 (reference template):**
- [ ] Same header hierarchy (##, ###, ####)
- [ ] Same Key Concept format (blockquotes with bold title)
- [ ] Same case study structure (if applicable)
- [ ] Same difficulty labels format (ALL CAPS in parentheses)
- [ ] Similar cell count ratio (markdown:code ≈ 70:30)

---

### Quality Verification

- [ ] Run technical validation script (Section 5)
- [ ] All code cells execute successfully
- [ ] PDF generates without errors
- [ ] Visual inspection of PDF (title page, Key Concepts, spacing)
- [ ] No text running together in PDF
- [ ] All images display in PDF
- [ ] Tables fit within margins

---

### Documentation

- [ ] Update notebooks_colab/README.md with chapter status
- [ ] Create/update log file for chapter work
- [ ] Document any design decisions (e.g., section gaps, no case study)
- [ ] Note PDF file size in README

---

## Section 8: Common Issues and Prevention

### Issue 1: Text Running Together

**Symptoms:**
- Headers and content on same line in PDF
- Bullet lists display as dashes
- Paragraphs merge into one block

**Prevention:**
- ✅ Always add blank line after headers (`##\n\n`)
- ✅ Add blank line before and after lists
- ✅ Ensure all markdown lines end with `\n`
- ✅ Run validation script before PDF generation

**Fix:**
- Add proper spacing with `\n\n` between elements
- Regenerate PDF

---

### Issue 2: Character-by-Character Corruption

**Symptoms:**
- Markdown cell has >100 lines for simple text
- Each character on separate line in JSON
- Text displays one letter per line in PDF

**Prevention:**
- ✅ Don't use `.replace('\n', '')` globally
- ✅ Verify cell structure after programmatic edits
- ✅ Run validation script checking cell line counts

**Fix:**
- Join text: `content = ''.join(cell['source']).replace('\n', '')`
- Add back semantic newlines for proper markdown structure
- Regenerate PDF

---

### Issue 3: Inconsistent Difficulty Labels

**Symptoms:**
- Task labels don't match template ("Independent with Hints" vs "(INDEPENDENT)")
- Inconsistent capitalization
- Missing labels

**Prevention:**
- ✅ Use exactly these labels: (GUIDED), (SEMI-GUIDED), (MORE INDEPENDENT), (INDEPENDENT)
- ✅ ALL CAPS in parentheses
- ✅ Check against CH02 reference

**Fix:**
- Update labels to standard format
- Regenerate PDF

---

### Issue 4: Wrong Number of Key Concepts in Case Study

**Symptoms:**
- Case study has 1 or 3+ Key Concept boxes instead of 2

**Prevention:**
- ✅ Reference template: Exactly 2 Key Concepts in case study
- ✅ Plan placement: 1 early (methodological), 1 middle (interpretation)

**Fix:**
- Merge or remove Key Concepts to reach exactly 2
- Ensure strategic placement
- Regenerate PDF

---

### Issue 5: Section Numbering Gaps

**Symptoms:**
- Non-sequential section numbers without explanation

**Prevention:**
- ✅ Use sequential numbering by default
- ✅ If gaps needed, document reason (e.g., "X.7 reserved for future content")
- ✅ Check Chapter Overview outline matches actual sections

**Fix:**
- Either renumber sequentially OR document gap reason
- Update Chapter Overview to match

---

## Section 9: Template Compliance Levels

### Level 1: Minimum Viable (Not Acceptable for Publication)

- Basic structure (title, sections, exercises)
- Some Key Concepts
- Code runs
- PDF generates

**Status:** ⚠️ Needs work

---

### Level 2: Template Compliant (Acceptable)

- ✅ Complete front matter (title, objectives, overview, setup)
- ✅ 7+ Key Concept boxes
- ✅ Key Takeaways and Practice Exercises
- ✅ Proper formatting (no text running together)
- ✅ PDF quality good

**Status:** ✅ Publication-ready

---

### Level 3: Exemplary (Target for All Chapters)

- ✅ All Level 2 requirements
- ✅ 9+ Key Concept boxes (strategic placement)
- ✅ Case study with 6 progressive tasks (if applicable)
- ✅ 2 Key Concepts in case study
- ✅ Comprehensive Key Takeaways
- ✅ Professional PDF (1.0-2.0 MB)
- ✅ Zero formatting issues

**Status:** ⭐⭐⭐⭐⭐ Exemplary

**Current Exemplary Chapters:** CH02, CH03, CH04

---

## Section 10: Quick Reference

### Cell Order Template

```
Cell 0:  Title Page (markdown)
Cell 1:  Learning Objectives (markdown)
Cell 2:  Chapter Overview (markdown)
Cell 3:  Setup intro (markdown)
Cell 4:  Setup code (code)
Cell 5+: Section X.1 (markdown + code cells)
...
Cell N:  Key Takeaways (markdown)
Cell N+1: Practice Exercises (markdown)
Cell N+2: Case Study Section X.Y (markdown)
Cell N+3+: Case study content (13-15 cells)
```

### Minimum Standards

- **Key Concepts:** 7-11 total (9+ preferred)
- **Case Study Tasks:** 6 progressive (if applicable)
- **Case Study Key Concepts:** Exactly 2
- **Practice Exercises:** 6-10 exercises
- **PDF Size:** 1.0-2.0 MB
- **Cell Count:** 45-75 cells typical

### Difficulty Label Reference

```
(GUIDED)           - Full code with blanks
(SEMI-GUIDED)      - Partial code with hints
(MORE INDEPENDENT) - Outline with minimal hints
(INDEPENDENT)      - Objective only, no code
```

---

## Appendix: Example Reference Cells

### Example: Perfect Title Page (Cell 0)

```markdown
# Chapter 2: Univariate Data Summary

**metricsAI: An Introduction to Econometrics with Python and AI in the Cloud**

*[Carlos Mendez](https://carlos-mendez.org)*

<img src="https://raw.githubusercontent.com/quarcs-lab/metricsai/main/images/ch02_visual_summary.jpg" alt="Chapter 02 Visual Summary" width="65%">

This chapter introduces fundamental methods for summarizing and visualizing univariate data—the foundation of all statistical analysis.

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/quarcs-lab/metricsai/blob/main/notebooks_colab/ch02_Univariate_Data_Summary.ipynb)
```

### Example: Perfect Key Concept Box

```markdown
> **Key Concept: Summary Statistics and Central Tendency**
>
> Summary statistics provide a concise numerical description of a dataset's essential features. The **mean** measures central tendency (typical value), the **median** indicates the middle value (robust to outliers), and the **standard deviation** quantifies dispersion (spread around the mean).
>
> For economic data: Use mean for symmetric distributions, median for skewed data (income, wealth), and standard deviation to assess variability (volatility, inequality).
```

### Example: Perfect Task Header

```markdown
#### Task 3: Visualizing Distributions (SEMI-GUIDED)

**Objective:** Create a 2×2 subplot grid comparing four visualization techniques for labor productivity distribution.

**Instructions:**

Create four subplots showing: (1) histogram, (2) box plot, (3) kernel density estimate, and (4) log-transformed KDE. Use `plt.subplots(2, 2, figsize=(12, 10))` to create the grid.

**Questions to answer:**

1. Which visualization best shows the right-skewed nature of the distribution?
2. How does log transformation affect the distribution shape?
3. What economic insights can you draw from the box plot?
```

---

**End of Master Template Checklist**

**Version:** 1.0
**Last Updated:** 2026-02-04
**Status:** Active - Use for all chapters CH05-CH17
