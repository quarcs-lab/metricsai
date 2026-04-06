---
name: improve-readability
description: Audits and improves readability of metricsAI chapter notebooks (.qmd). Checks code cell clarity, explanation ordering, interpretation guidance, regression output presentation, prose quality, and jargon management. Generates a prioritized report with specific line numbers and before/after suggestions. Use after chapter-standard compliance, before proofread. Supports --apply for automated fixes and --all for batch analysis.
argument-hint: [chapter-number] [--apply] [--all]
---

# Improve Readability Skill

Audits and improves the readability of metricsAI chapter notebooks for a beginner audience. Focuses on making both code and explanations short, clear, and friendly for students encountering econometrics for the first time.

## Overview

This skill sits between `chapter-standard` (structural compliance) and `proofread` (text quality). It focuses on **pedagogical readability**: Are code cells clear? Do explanations come in the right order? Can a beginner follow along?

**Use this skill when:**

- A chapter passes `chapter-standard` but still feels dense or hard to follow
- Before `proofread` (fix readability first, then polish prose)
- After writing or editing a chapter, to check beginner-friendliness
- When improving chapters in batch (`--all`)

**Workflow position:**

```
/chapter-standard ch05  →  /improve-readability ch05  →  /proofread ch05  →  PDF generation
```

---

## Quick Start

### Audit a chapter

```
/improve-readability ch05
```

Generates a readability report with findings across 6 categories, specific line numbers, and concrete suggestions.

### Apply improvements

```
/improve-readability ch05 --apply
```

Applies safe, mechanical fixes (setup cell annotation, magic number comments, framing sentences). Flags items requiring human judgment.

### Audit all chapters

```
/improve-readability --all
```

Generates a summary table with readability scores across all chapters.

---

## What Gets Checked

Six categories, ordered by impact on beginners.

### Category 1: Code Cell Clarity (HIGH)

**1A. Setup cell annotation**

- Does the setup cell group its contents with section comments?
- Are library imports annotated with their purpose?
- Target: 5 labeled groups (Libraries, Reproducibility, Data source, Output dirs, Plotting style)

**1B. Code cells doing too much**

- Any code cell that performs 3+ distinct operations (load + transform + display, etc.)
- Cells longer than 25 lines without internal section breaks
- Target: One concept per cell

**1C. Magic numbers without explanation**

- Bare `1.96`, `0.975`, `ppf(0.975)`, `alpha=0.7`, `s=50`, `figsize` values
- Any numeric constant that a beginner would wonder "why this number?"
- Target: Every magic number has either a comment or a named variable

**1D. Missing intermediate print statements**

- Data loaded without confirming shape/columns
- Statistics calculated but not printed before use
- Simulations/loops running without progress output
- Target: After every major operation, print a status line

**1E. Raw `.summary()` without key extraction**

- `model.summary()` shown before extracting key coefficients
- Beginners see dense output table without knowing what to focus on
- Target: Print estimated equation + R-squared + interpretation BEFORE full summary

### Category 2: Explanation Ordering (HIGH)

**2A. Formula before intuition**

- Mathematical notation (E[X], Var[X], etc.) appears before a plain-English sentence
- Target: Always explain in words first, then show the formula

**2B. Code before context**

- A code cell appears without a preceding sentence explaining what it does and why
- Target: Every code cell has at least one framing sentence before it

**2C. Results before interpretation**

- Code output appears but interpretation comes many lines later (or not at all)
- Target: Interpretation immediately follows the code that produces it

### Category 3: Interpretation Guidance (HIGH)

**3A. Visualizations without "what to look for"**

- Plots shown without guidance on what patterns to notice
- Target: After every visualization, a short "What to look for" paragraph or bullets

**3B. Interpretation buried in code comments**

- Economic interpretation written as Python `# comments` inside code cells
- Target: Move interpretations to markdown cells where they're visible

### Category 4: Regression Output (MEDIUM)

**4A. Summary table shown first**

- `model.summary()` is the first thing shown after fitting
- Target: Extract and print key numbers first, show full summary after

**4B. No interpretation bridge**

- Regression output followed by a new section, with no interpretation in between
- Target: Always interpret coefficients before moving on

### Category 5: Prose Quality (MEDIUM)

**5A. Passive voice in introductions**

- Section intros using "is analyzed," "are shown," "is calculated"
- Target: Active voice — "Let's analyze," "Look at," "We'll calculate"

**5B. Orphaned transitions**

- Sentences like "Having done X, let's do Y" that restate what was just done
- Target: Remove or integrate into the next section's introduction

**5C. Walls of text**

- Paragraphs exceeding 100 words without visual breaks
- Target: Break into bullets, numbered steps, or shorter paragraphs

### Category 6: Jargon Management (MEDIUM)

**6A. Terms used before definition**

- Technical term appears without a plain-English definition at first use
- Common offenders: OLS, homoskedasticity, elasticity, degrees of freedom, p-value, heteroskedasticity
- Target: Brief parenthetical or sentence-level definition at first use

**6B. Missing cross-references (ch07+)**

- Later chapters reference concepts from earlier chapters without pointing back
- Target: Add "(see Chapter X)" when referencing prior material

---

## Audit Workflow

When invoked, follow these steps in order.

### Step 1: Parse Arguments

- `ch05` or `5` → normalized to `ch05`
- `--apply` → enable automated fixes
- `--all` → batch mode (audit all chapters, summary table only)

Find the `.qmd` file: `notebooks_quarto/ch{NN}_*.qmd`

### Step 2: Read the Chapter

Read the entire `.qmd` file. Note total line count and structure:

- Count code cells (```` ```{python} ```` blocks)
- Count markdown sections (## headers)
- Identify the setup cell, visualization cells, and regression cells

### Step 3: Analyze Each Category

Work through all 6 categories systematically. For each finding, record:

- **Category** and subcategory (e.g., 1C)
- **Line number(s)** in the .qmd file
- **Severity**: HIGH / MEDIUM / LOW
- **Current text** (brief excerpt)
- **Suggested fix** (concrete, not vague)

Use the checklist in [references/READABILITY_CHECKLIST.md](references/READABILITY_CHECKLIST.md) for detailed detection rules.

Use examples in [references/BEFORE_AFTER_EXAMPLES.md](references/BEFORE_AFTER_EXAMPLES.md) for the style of improvements to suggest.

### Step 4: Calculate Score

**100 points total, deductions by category:**

| Category | Per issue | Max deduction |
|----------|-----------|---------------|
| 1. Code Cell Clarity | -3 | -25 |
| 2. Explanation Ordering | -4 | -25 |
| 3. Interpretation Guidance | -4 | -20 |
| 4. Regression Output | -3 | -10 |
| 5. Prose Quality | -2 | -10 |
| 6. Jargon Management | -2 | -10 |

**Score tiers:**

- **90-100**: Excellent — beginner-friendly, ready for proofread
- **80-89**: Good — a few improvements needed
- **70-79**: Acceptable — several readability gaps
- **< 70**: Needs work — significant readability issues

### Step 5: Generate Report

Format findings as:

```markdown
# Readability Report: ch05_Bivariate_Data_Summary.qmd

**Readability Score**: 78/100
**Quality**: Acceptable (several readability gaps)

## HIGH Priority

### Category 1: Code Cell Clarity
- **Line 85**: Setup cell is a 35-line monolith without section comments [1A]
  → Add `# --- Libraries ---`, `# --- Reproducibility ---`, etc.
- **Line 210**: Magic number `alpha=0.7` without comment [1C]
  → Add: `alpha=0.7  # slight transparency to see overlapping points`
- **Line 340**: `model.summary()` shown before key extraction [1E]
  → Extract slope, R-squared, print interpretation first

### Category 2: Explanation Ordering
- **Line 180**: Formula E[X̄] = μ appears before plain-English explanation [2A]
  → Add: "On average, sample means equal the true population mean."
- **Line 250**: Code cell has no framing sentence before it [2B]
  → Add: "Let's fit the regression model and examine the results."

### Category 3: Interpretation Guidance
- **Line 300**: Scatter plot shown without "what to look for" [3A]
  → Add bullets: Direction, Form, Scatter, Outliers

## MEDIUM Priority
[...]

## Summary
| Category | Issues | Deduction |
|----------|--------|-----------|
| Code Cell Clarity | 5 | -15 |
| Explanation Ordering | 3 | -12 |
| Interpretation Guidance | 2 | -8 |
| Regression Output | 1 | -3 |
| Prose Quality | 2 | -4 |
| Jargon Management | 0 | 0 |

## Auto-Fixable (with --apply)
- [1A] Setup cell annotation (template-based)
- [1C] Magic number comments (5 instances)
- [5B] Remove 2 orphaned transition sentences

## Requires Human Judgment
- [2A] Formula-before-intuition rewrites (3 instances)
- [3A] Write "what to look for" guidance for 2 plots
- [4A] Extract and interpret regression coefficients
```

### Step 6: Apply Fixes (if --apply)

Only apply **mechanical, safe fixes**:

| Fix | Category | Method |
|-----|----------|--------|
| Setup cell annotation | 1A | Add section comment lines between groups |
| Magic number comments | 1C | Append inline comments to known patterns |
| Move code-comment interpretations to markdown | 3B | Extract `# What do you see?` blocks to markdown |
| Remove orphaned transitions | 5B | Delete known patterns ("Having done X...") |
| Add framing sentences | 2B | Insert brief "Let's..." sentence before bare code cells |

**NOT auto-fixed** (requires human judgment):

- Splitting long code cells (1B) — need to decide where
- Rewriting formulas-before-intuition (2A) — need domain knowledge
- Writing "what to look for" guidance (3A) — need to understand the plot
- Extracting regression key results (4A/1E) — need to identify which coefficients matter
- Rewriting passive voice (5A) — need context
- Adding jargon definitions (6A) — need to explain correctly

After applying fixes, report what was changed and what still needs manual attention.

### Step 7: Recommendations

Always end with:

```markdown
## Next Steps

1. Address HIGH priority items marked "Requires Human Judgment"
2. Re-run `/improve-readability chNN` to verify improvements
3. Target readability score >= 90 before proceeding
4. Then run `/proofread chNN` for text quality checks
5. Then generate PDF
```

---

## Batch Mode (--all)

When invoked with `--all`, audit every chapter and produce a summary:

```markdown
# Readability Summary: All Chapters

| Chapter | Score | Cat 1 | Cat 2 | Cat 3 | Cat 4 | Cat 5 | Cat 6 | Top Issue |
|---------|-------|-------|-------|-------|-------|-------|-------|-----------|
| ch01    | 92    | 0     | 0     | 0     | -3    | -2    | -3    | Jargon    |
| ch02    | 74    | -12   | -8    | -4    | -3    | 0     | 0     | Code      |
| ...     | ...   | ...   | ...   | ...   | ...   | ...   | ...   | ...       |

Chapters needing attention (score < 80):
- ch02, ch03, ch06, ch12, ch15, ch16, ch17

Recommended order: ch02 → ch03 → ch06 → ch12 → ch15 → ch16 → ch17
(Foundation chapters first, then advanced)
```

---

## Reference Files

- **Detailed checklist**: [references/READABILITY_CHECKLIST.md](references/READABILITY_CHECKLIST.md)
- **Before/after examples**: [references/BEFORE_AFTER_EXAMPLES.md](references/BEFORE_AFTER_EXAMPLES.md)
- **Chapter standard skill**: `.claude/skills/chapter-standard/SKILL.md`
- **Proofread skill**: `.claude/skills/proofread/SKILL.md`
- **Project instructions**: `CLAUDE.md`

---

**Version**: 1.0
**Created**: April 6, 2026
**Prerequisite**: Chapter standardization (`chapter-standard` score >= 85)
**Audience**: Beginner econometrics students
