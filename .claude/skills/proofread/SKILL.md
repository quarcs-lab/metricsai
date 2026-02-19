---
name: proofread
description: Proofread metricsAI Jupyter notebook chapters for text quality issues. Detects missing spaces (concatenated words), doubled words, broken LaTeX, unclosed markdown formatting, inconsistent terminology, and content accuracy. Use after standardization, before final PDF generation, or when reviewing chapter quality. Supports --fix for automated corrections.
argument-hint: [chapter-number] [--fix]
context: fork
agent: Explore
---

# Chapter Proofreading Skill

Automates detection and correction of text quality issues in metricsAI chapter notebooks. Complements the `chapter-standard` skill by focusing on prose quality rather than structural compliance.

## Overview

This skill proofreads chapter notebooks for text quality issues that affect readability and professionalism. It detects concatenated words (missing spaces), doubled words, broken LaTeX, unclosed formatting, and other prose defects.

**Use this skill when:**
- After standardization (chapter-standard score >= 85)
- Before final PDF generation
- When reviewing chapter text quality
- When a rendered notebook shows garbled text (words running together)

**Key Features:**
- Automated detection of 9+ categories of text issues
- Proofreading score (0-100 with issue breakdown)
- Safe automated fixes with backup creation
- JSON output for programmatic use
- Batch processing across all chapters

---

## Quick Start

### Proofread a Chapter
```
/proofread ch08
```

Generates proofreading report showing:
- Proofreading score (0-100)
- CRITICAL issues (concatenated words, missing spaces after punctuation)
- MINOR issues (doubled words, broken LaTeX, emoji remnants)
- SUGGESTIONS (long paragraphs)
- Issue summary by type

### Apply Automated Fixes
```
/proofread ch08 --fix
```

Applies safe fixes:
- Removes doubled words
- Inserts missing spaces after periods/commas
- Splits common concatenation patterns (e.g., "ofthe" -> "of the")
- Removes emoji remnants
- Creates timestamped backup automatically

### Proofread All Chapters
```
/proofread --all
```

Generates summary table across all chapters with scores.

---

## What Gets Checked

### CRITICAL Issues (affect readability)

1. **Concatenated words**: Words >30 chars that are likely multiple words joined together
   - Example: `capturesboththedirecteffectofbedroomsandtheindirecteffectthrough`
   - Detection: Length heuristic + known long-word dictionary exclusion

2. **Common concatenation patterns**: Known preposition+article combinations
   - Patterns: `ofthe`, `inthe`, `tothe`, `andthe`, `forthe`, `onthe`, `isthe`, `bythe`, `atthe`, `fromthe`, `withthe`, `thatthe`, `ofthis`, `inthis`, `tothis`
   - Example: `effectofthe` should be `effect of the`

3. **Missing space after period**: `word.Next` pattern
   - Example: `coefficient.This` should be `coefficient. This`

4. **Missing space after comma**: `word,next` pattern
   - Example: `variable,which` should be `variable, which`

### MINOR Issues (should fix)

5. **Doubled words**: Repeated adjacent words
   - Example: `the the`, `is is`, `to to`
   - Excludes intentional: `ha`, `no`, `so`, `oh`, `go`, `do`, `ok`, `bye`

6. **Broken LaTeX**: Odd number of `$` signs (unmatched math delimiters)
   - Detection: Count `$` after removing `$$` display math pairs

7. **Unclosed formatting**: Odd number of `**` bold markers
   - Detection: Count after stripping code blocks and LaTeX

8. **Broken links**: `[text](` without closing `)`

9. **Emoji remnants**: Any emoji characters left from pre-standardization

10. **CamelCase in prose**: Words >10 chars with camelCase pattern outside code
    - Excludes known: DataFrame, GitHub, NumPy, statsmodels, etc.

### SUGGESTIONS (nice to have)

11. **Long paragraphs**: Prose paragraphs >800 characters
    - Suggestion: Consider splitting for readability

12. **Number-word concatenation**: Numbers immediately followed by capitalized words
    - Example: `1553the` or `0.047Growth`

---

## Proofreading Workflow

When you invoke this skill, follow these steps:

### 1. Parse Arguments

Extract chapter number and flags:
- `ch08` or `8` -> normalized to `ch08`
- `--fix` -> enable automated fixes (creates backup)
- `--json` -> JSON output format
- `--all` -> batch processing

Validate chapter exists in `notebooks_colab/`.

### 2. Run Detection Script

Execute proofreading:
```bash
python3 .claude/skills/proofread/scripts/proofread_chapter.py ch08
```

Collect findings across all markdown cells:
- Text extraction (strips code blocks, LaTeX, URLs, HTML, markdown formatting)
- Pattern matching for all issue categories
- Score calculation

### 3. Display Report

Format and present findings by severity:

```markdown
# Proofreading Report: ch08_Case_Studies_for_Bivariate_Regression.ipynb

**Proofreading Score**: 75/100
**Quality**: Acceptable (several issues)
**Cells checked**: 33 markdown / 52 total
**Issues found**: 3 critical, 4 minor, 1 suggestion

## CRITICAL Issues (affect readability)
- **Cell 15**: Likely concatenated words: "capturesboththedirecteffect"
  Context: `...the coefficient capturesboththedirecteffect of bedrooms...`
- **Cell 22**: Missing space after period: "...coefficient.This..."
  Context: `...regression coefficient.This means that...`

## MINOR Issues (should fix)
- **Cell 10**: Doubled word: "the the"
  Context: `...examine the the relationship between...`
- **Cell 30**: Odd number of $ signs (3) - possible broken LaTeX

## SUGGESTIONS (nice to have)
- **Cell 18**: Very long paragraph (923 chars) - consider splitting

## Issue Summary by Type
| Type | Count |
|------|-------|
| concatenated_words | 3 |
| doubled_word | 2 |
| missing_space_period | 1 |
| broken_latex | 1 |
| long_paragraph | 1 |
```

### 4. Apply Fixes (if --fix)

If `--fix` flag present:

1. **Create backup** in `notebooks_colab/backups/`
   - Timestamped: `ch08_backup_20260207_143000.ipynb`

2. **Apply safe fixes**:
   - Remove doubled words
   - Insert spaces after periods/commas
   - Split common concatenation patterns
   - Remove emoji remnants

3. **Report changes**:
   ```markdown
   ## Fixes Applied
   - Cell 10: Applied text fixes
   - Cell 15: Applied text fixes
   - Cell 22: Applied text fixes

   Backup: notebooks_colab/backups/ch08_backup_20260207_143000.ipynb
   ```

4. **NOT auto-fixed** (requires manual review):
   - Ambiguous concatenated words (may be technical terms)
   - Broken LaTeX (needs context to fix)
   - Unclosed formatting (may be intentional)
   - Long paragraphs (content decision)

### 5. Manual Review

After automated detection, read each flagged cell and:

1. **Verify automated detections** are true positives
2. **Check content accuracy** (formulas match explanations)
3. **Review pedagogical flow** (clear, progressive explanations)
4. **Assess readability** (appropriate paragraph length, clear language)

Refer to `.claude/skills/proofread/references/PROOFREADING_CHECKLIST.md` for complete manual review checklist.

### 6. Provide Recommendations

Always end with clear next steps:

```markdown
## Recommended Actions

**Immediate**:
1. Fix CRITICAL concatenated words (cells listed above)
2. Review and fix MINOR issues
3. Re-run proofreading to verify fixes

**Before PDF Generation**:
1. Run proofreading again (`/proofread ch08`)
2. Ensure proofreading score >= 90
3. Generate PDF and spot-check rendered text

**After Fixes**:
1. Generate PDF: Follow CLAUDE.md PDF workflow
2. Verify text renders correctly in PDF
3. Commit changes
```

---

## Score Calculation

**100 points total:**

**CRITICAL issues** (-5 points each, max -40):
- Concatenated words
- Missing space after punctuation
- Common concatenation patterns

**MINOR issues** (-2 points each, max -20):
- Doubled words
- Broken LaTeX
- Unclosed formatting
- Broken links
- Emoji remnants
- CamelCase in prose

**SUGGESTIONS** (-1 point each, max -10):
- Long paragraphs
- Number-word concatenation

**Score Tiers:**
- **95-100**: Excellent (publication-ready)
- **85-94**: Good (minor fixes needed)
- **70-84**: Acceptable (several issues)
- **< 70**: Needs work (significant issues)

---

## Text Extraction Pipeline

The script processes markdown cells through this pipeline before analysis:

1. **Strip code blocks**: Remove ` ``` ... ``` ` fenced blocks
2. **Strip inline code**: Remove `` `code` `` spans
3. **Strip LaTeX**: Remove `$...$` and `$$...$$` math expressions
4. **Strip URLs**: Remove `https://...` and extract link text from `[text](url)`
5. **Strip HTML**: Remove `<tag>...</tag>` elements
6. **Strip markdown formatting**: Remove `#`, `**`, `*`, `>` markers

This ensures only **prose text** is analyzed, avoiding false positives from code, math, or URLs.

---

## Known Long Words (Not Flagged)

The script maintains a dictionary of legitimate long words common in econometrics:
- `heteroskedasticity`, `homoskedasticity`, `multicollinearity`
- `autocorrelation`, `endogeneity`, `stationarity`
- `counterfactual`, `semiparametric`, `nonparametric`
- `quasiexperimental`, `disproportionately`
- And 60+ more econometric/statistical terms

---

## Integration with Existing Workflow

### After Standardization, Before PDF

```bash
# 1. Verify chapter standard compliance
/chapter-standard ch08

# 2. Proofread text quality
/proofread ch08

# 3. Fix detected issues
/proofread ch08 --fix

# 4. Manual review of flagged items
# [Review cells listed in report]

# 5. Verify again
/proofread ch08

# 6. Generate PDF when score >= 90
cd notebooks_colab && jupyter nbconvert --to html ch08_*.ipynb && cd ..
python3 scripts/inject_print_css.py notebooks_colab/ch08_*.html notebooks_colab/ch08_*_printable.html
python3 scripts/generate_pdf_playwright.py ch08
```

### Batch Quality Check

```bash
# Proofread all chapters
/proofread --all

# Shows summary table:
# | Chapter | Critical | Minor | Suggestions | Score |
# |---------|----------|-------|-------------|-------|
# | ch06    | 0        | 2     | 1           | 95    |
# | ch07    | 1        | 3     | 0           | 89    |
# | ...     | ...      | ...   | ...         | ...   |
```

---

## Troubleshooting

### False Positives for Long Words
**Issue**: Script flags a legitimate technical term as concatenated words

**Solution**: Add the word to `KNOWN_LONG_WORDS` set in `proofread_chapter.py`

### False Positives for CamelCase
**Issue**: Script flags a known library name (e.g., `PanelOLS`)

**Solution**: Add to `known_camel` set in `check_concatenated_words()`

### Fix Mode Changes Too Much
**Issue**: Automated fixes alter content incorrectly

**Solution**:
1. Restore from backup in `notebooks_colab/backups/`
2. Run without `--fix` to review issues first
3. Apply fixes manually for ambiguous cases

### Script Not Found
**Issue**: Error running proofreading script

**Solution**:
1. Verify path: `ls .claude/skills/proofread/scripts/proofread_chapter.py`
2. Check Python 3: `python3 --version`
3. Run directly: `python3 .claude/skills/proofread/scripts/proofread_chapter.py ch08`

---

## Support & Documentation

**Proofreading checklist**: `.claude/skills/proofread/references/PROOFREADING_CHECKLIST.md`
**Detection script**: `.claude/skills/proofread/scripts/proofread_chapter.py`
**Chapter standard skill**: `.claude/skills/chapter-standard/SKILL.md`
**Project instructions**: `CLAUDE.md`
**Progress logs**: `log/` directory

---

**Version**: 1.0
**Created**: February 7, 2026
**Prerequisite**: Chapter standardization (chapter-standard score >= 85)
**Skill Author**: AI-assisted implementation following Claude Code best practices
