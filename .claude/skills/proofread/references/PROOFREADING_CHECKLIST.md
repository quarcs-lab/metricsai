# Proofreading Checklist for metricsAI Notebooks

A comprehensive checklist for reviewing text quality in chapter notebooks. Use alongside the automated `proofread_chapter.py` script for complete coverage.

---

## 1. Text Quality (Automated + Manual)

### Spacing Issues (Automated)
- [ ] No concatenated words (multiple words joined without spaces)
- [ ] No missing spaces after periods (e.g., `word.Next`)
- [ ] No missing spaces after commas (e.g., `word,next`)
- [ ] No doubled words (e.g., `the the`)
- [ ] No number-word concatenation (e.g., `1553the`)

### Grammar and Punctuation (Manual)
- [ ] Consistent use of Oxford comma (or consistent omission)
- [ ] Proper apostrophe usage (its vs. it's, students' vs. student's)
- [ ] No sentence fragments in explanatory text
- [ ] Complete sentences in all prose paragraphs
- [ ] Proper capitalization after colons (consistent style)

### Readability (Manual)
- [ ] Paragraphs are reasonable length (under ~800 characters)
- [ ] One idea per paragraph
- [ ] Active voice preferred over passive voice
- [ ] Technical terms defined on first use
- [ ] Appropriate transition words between ideas

---

## 2. Mathematical Accuracy (Manual)

### Formulas
- [ ] All LaTeX expressions render correctly (matched `$` signs)
- [ ] Variable names in formulas match code variables
- [ ] Subscripts and superscripts are correct
- [ ] Greek letters used consistently (e.g., always beta, not sometimes b)
- [ ] Equation numbers referenced correctly in text

### Interpretations
- [ ] Coefficient interpretations match regression output
- [ ] Units are correct in interpretations
- [ ] Direction of effects is correct (positive/negative)
- [ ] Statistical significance statements match p-values
- [ ] Confidence interval interpretations are correct

### Notation Consistency
- [ ] Same variable always uses same notation
- [ ] Vectors/matrices distinguished from scalars
- [ ] Hats (^) used consistently for estimates
- [ ] Subscripts consistent (i vs. t vs. it)

---

## 3. Code-Text Alignment (Manual)

### Output References
- [ ] Text descriptions match actual code outputs
- [ ] Numerical values cited in text match code results
- [ ] Figure references point to correct plots
- [ ] Table descriptions match table contents

### Variable Names
- [ ] Variable names in prose match code exactly
- [ ] Function names referenced correctly
- [ ] Library names are accurate (e.g., `statsmodels` not `statmodels`)
- [ ] Package import paths are correct

### Code Comments
- [ ] Comments in code cells are accurate
- [ ] No outdated comments from previous versions
- [ ] Technical terms in comments match prose definitions

---

## 4. Pedagogical Flow (Manual)

### Learning Objectives Alignment
- [ ] Each LO is addressed in at least one section
- [ ] Content doesn't significantly exceed stated LOs
- [ ] LOs use appropriate Bloom's taxonomy verbs
- [ ] Progressive difficulty matches stated objectives

### Concept Progression
- [ ] New concepts build on previously introduced ones
- [ ] No forward references to undefined concepts
- [ ] Examples progress from simple to complex
- [ ] Each section has clear purpose and contribution

### Key Concepts
- [ ] Key Concept boxes summarize the preceding section
- [ ] No Key Concept introduces entirely new material
- [ ] Key Concept wording is concise and precise
- [ ] Key Concepts cover the most important ideas

### Practice Exercises
- [ ] Exercises reference concepts covered in the chapter
- [ ] Difficulty progresses from easier to harder
- [ ] Exercise instructions are unambiguous
- [ ] Required data/resources are specified

---

## 5. Consistency (Automated + Manual)

### Terminology (Manual)
- [ ] Consistent use of "regression" vs. "model" vs. "equation"
- [ ] Consistent use of "coefficient" vs. "parameter" vs. "estimate"
- [ ] Consistent use of "standard error" vs. "SE"
- [ ] Consistent use of "significance level" vs. "alpha"
- [ ] Consistent use of "dependent variable" vs. "outcome" vs. "response"
- [ ] Consistent use of "independent variable" vs. "predictor" vs. "regressor"

### Formatting (Automated)
- [ ] No emoji characters remaining
- [ ] Bold markers (`**`) properly closed
- [ ] All markdown links have closing parentheses
- [ ] Headers follow hierarchy (H1 > H2 > H3 > H4)

### Style (Manual)
- [ ] Consistent tone (formal but accessible)
- [ ] Consistent use of "we" vs. "you" vs. passive voice
- [ ] Consistent number formatting (e.g., 1,000 vs. 1000)
- [ ] Consistent decimal places in reported values

---

## 6. Accessibility (Manual)

### Language
- [ ] No undefined jargon or acronyms
- [ ] Acronyms defined on first use (e.g., OLS = Ordinary Least Squares)
- [ ] Analogies and examples are culturally neutral
- [ ] Technical terms are followed by plain-language explanation

### Visual Elements
- [ ] All images have descriptive alt text
- [ ] Figures are referenced in surrounding text
- [ ] Color is not the only distinguishing feature in plots
- [ ] Tables have clear headers and labels

### Structure
- [ ] Headers accurately describe section content
- [ ] Lists are used for 3+ related items
- [ ] Important information is not buried in long paragraphs
- [ ] Cross-references to other chapters are accurate

---

## Common Issues Specific to metricsAI

### Concatenated Words (Most Common)
These typically arise from copy-paste or rendering issues:
- **Bad**: `capturesboththedirecteffectofbedroomsandtheindirecteffectthrough`
- **Good**: `captures both the direct effect of bedrooms and the indirect effect through`
- **Detection**: Words >30 chars or containing patterns like `ofthe`, `inthe`

### Missing Spaces After Punctuation
- **Bad**: `coefficient.This means that`
- **Good**: `coefficient. This means that`
- **Bad**: `variable,which controls for`
- **Good**: `variable, which controls for`

### Doubled Words
- **Bad**: `examine the the relationship`
- **Good**: `examine the relationship`

### Broken LaTeX
- **Bad**: `The estimate $\hat{\beta}_1 is significant` (missing closing `$`)
- **Good**: `The estimate $\hat{\beta}_1$ is significant`

### Inconsistent Terminology
- **Bad**: Using "OLS" in one paragraph and "ordinary least squares" in the next without introduction
- **Good**: "Ordinary Least Squares (OLS)" on first use, then "OLS" consistently

---

## Checklist Usage

### Before Proofreading
1. Ensure chapter has been standardized (`/chapter-standard` score >= 85)
2. Run automated detection: `python3 .claude/skills/proofread/scripts/proofread_chapter.py ch08`
3. Review automated report for critical and minor issues

### During Proofreading
1. Fix all automated detections first (use `--fix` for safe auto-fixes)
2. Read through each markdown cell sequentially
3. Check items from this checklist as you go
4. Focus on Sections 1-3 (text quality, math, code-text alignment)

### After Proofreading
1. Re-run automated detection to verify fixes
2. Target proofreading score >= 90
3. Generate PDF and spot-check rendered text
4. Commit changes with descriptive message

---

**Version**: 1.0
**Created**: February 7, 2026
**Companion script**: `.claude/skills/proofread/scripts/proofread_chapter.py`
