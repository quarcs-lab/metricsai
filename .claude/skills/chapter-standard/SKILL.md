---
name: chapter-standard
description: Verifies and standardizes metricsAI chapter notebooks against CH01-04 template. Checks structure (45-75 cells, 70-80% markdown), front matter (visual summary, Learning Objectives, overview, setup), content (section numbering, 7-11 Key Concepts), back matter (Key Takeaways, Practice Exercises). Generates compliance report with CRITICAL/MINOR/SUGGESTIONS. Use when reviewing chapters, before PDF generation, or ensuring consistency. Supports --apply for automated fixes.
context: fork
agent: Explore
---

# Chapter Standard Verification Skill

Automates verification and standardization of metricsAI chapter notebooks against the established CH01-04 template (Part I gold standard).

## Overview

This skill verifies chapter notebooks against the authoritative **MASTER_TEMPLATE_CHAPTER_STRUCTURE.md** (Version 2.0), ensuring consistency across all 17 chapters. It generates compliance reports with prioritized issues and can apply safe automated fixes.

**Use this skill when:**
- Reviewing chapter notebooks for template compliance
- Before generating PDFs (ensure ≥90 compliance score)
- Standardizing remaining chapters (CH07-17)
- Verifying consistency after edits

**Key Features:**
- Compliance scoring (0-100 with issue breakdown)
- Hierarchical structure verification (H1→H2→H3→H4)
- Case Studies progressive scaffolding validation
- Result interpretation placement verification
- Automated fixes for safe structural issues
- Detailed, actionable reports

---

## Quick Start

### Verify a Chapter
```
/chapter-standard ch05
```

Generates compliance report showing:
- Compliance score (0-100)
- CRITICAL issues (must fix)
- MINOR issues (should fix)
- SUGGESTIONS (nice to have)
- Specific cell numbers and examples

### Apply Automated Fixes
```
/chapter-standard ch05 --apply
```

Applies safe fixes:
- Adds missing structural elements
- Inserts placeholders for manual content
- Creates backup automatically
- Reports all changes made

### Verify All Chapters (Future)
```
/chapter-standard --all
```

Generates summary table across all chapters.

---

## What Gets Checked

### Structure & Composition
- ✅ **Cell count**: 45-75 cells (CH02: 74)
- ✅ **Markdown ratio**: 70-80% of total cells
- ✅ **Hierarchical headers**: H1→H2→H3→H4 levels correct
- ✅ **Section numbering**: Sequential X.1-X.N (or documented gaps)

### Front Matter (Cells 0-4)
- ✅ **Cell 0**: Visual summary image (65% width, proper alt text)
- ✅ **Cell 1**: Learning Objectives (6-10 action-oriented bullets)
- ✅ **Cell 2**: Chapter Overview (outline matches actual sections)
- ✅ **Cell 3-4**: Setup section with code cell

### Main Content (X.1 - X.9)
- ✅ **Key Concepts**: 4-6 boxes strategically placed
- ✅ **Transition notes**: 2-4 connecting major sections
- ✅ **Section headers**: Proper format `## X.Y [Title]`
- ✅ **Code cells**: Run without errors (manual verification)

### Back Matter
- ✅ **Key Takeaways**: 5-7 thematic groups with bullets
- ✅ **Practice Exercises**: 6-10 exercises with clear statements
- ✅ **Empty closing cell**: Present for spacing

### Case Studies (if applicable)
- ✅ **Section X.11**: Proper H2 header
- ✅ **H3 subsections**: Research intro, Load Data, What You've Learned
- ✅ **H4 tasks**: 6 progressive tasks (Guided → Independent)
- ✅ **Difficulty labels**: (Guided), (Semi-guided), (More Independent), (Independent)
- ✅ **Key Concepts**: 2-3 boxes interspersed
- ✅ **Approach**: Markdown-only or Code cells (both valid)

### Result Interpretation Placement (NEW)
- ✅ **Correct boundaries**: Text cells after code within proper sections
- ✅ **No misplacements**: Interpretations don't drift to wrong sections
- ⚠️ **Flagged for review**: Potential misplacements identified

### PDF Targets
- ✅ **File size**: 1.0-2.0 MB after generation
- ✅ **Rendering**: All elements display correctly

---

## Verification Workflow

When you invoke this skill, I will follow these steps:

### 1. Parse Arguments

Extract chapter number and flags:
- `ch05` or `5` → normalized to `ch05`
- `--apply` → enable automated fixes
- `--json` → JSON output format
- `--all` → batch processing (future)

Validate chapter exists in `notebooks_colab/`.

### 2. Run Verification Script

Execute verification:
```bash
python3 .claude/skills/chapter-standard/scripts/verify_chapter.py ch05 --json
```

Collect findings:
- Cell structure analysis
- Front/back matter checks
- Section numbering validation
- Key Concept count and placement
- Case Studies structure (if present)
- Interpretation placement verification
- Compliance score calculation

### 3. Display Report

Format and present findings by severity:

```markdown
# Chapter 5 Verification Report

**Compliance Score**: 85/100

## CRITICAL Issues (Must Fix)
- ❌ Missing visual summary image in Cell 0
  - Fix: Add <img> tag with visual_summary.png
  - Reference: See CH02 Cell 0 or TEMPLATE_REQUIREMENTS.md

## MINOR Issues (Should Fix)
- ⚠️ Key Concept count: 6 (target: 7-11)
  - Current locations: Cells 12, 20, 28, 35, 42, 50
  - Missing after: Section 5.3 (around cell 25)
  - Fix: Add Key Concept box after Section 5.3

- ⚠️ Interpretation placement issue: Cell 35
  - Text follows code but is 8 cells after Section 5.3 start
  - Preview: "The regression results show that..."
  - Action: Verify interpretation belongs to Section 5.3 code

## SUGGESTIONS (Nice to Have)
- 💡 Cell count: 42 (target: 45-75, lower end)
- 💡 Consider adding transition notes between major sections

## Auto-Fixable Items
The following can be fixed automatically with `--apply`:
- Add visual summary image template
- Add Key Concept placeholder after Section 5.3
- Add empty closing cell

Run: `/chapter-standard ch05 --apply`
```

### 4. Apply Fixes (if --apply)

If `--apply` flag present:

1. **Create backup** in `notebooks_colab/backups/`
   - Timestamped: `ch05_backup_20260206_212530.ipynb`

2. **Run apply script**:
   ```bash
   python3 .claude/skills/chapter-standard/scripts/apply_fixes.py ch05
   ```

3. **Report changes**:
   ```markdown
   Applied fixes to ch05:
   ✅ Added visual summary image
   ✅ Inserted Key Concept placeholder after Section 5.3
   ✅ Added empty closing cell

   Backup: notebooks_colab/backups/ch05_backup_20260206_212530.ipynb

   NEXT STEPS:
   1. Review changes in Jupyter/VSCode
   2. Fill in Key Concept placeholder with actual content
   3. Run verification again to confirm fixes
   4. Generate PDF: `python3 scripts/generate_pdf_playwright.py ch05`
   ```

### 5. Provide Recommendations

Always end with clear next steps:

```markdown
## Recommended Actions

**Immediate**:
1. Fix CRITICAL issues listed above
2. Review CH02 as reference for proper structure
3. Verify all Key Concepts are strategically placed

**Before PDF Generation**:
1. Run verification again (`/chapter-standard ch05`)
2. Ensure compliance score ≥ 90
3. Manual review of content quality

**After Fixes**:
1. Test notebook runs end-to-end without errors
2. Generate PDF and verify size (1.0-2.0 MB target)
3. Check PDF visual quality (images, tables)

**Reference Files**:
- Full template: `.claude/skills/chapter-standard/references/TEMPLATE_REQUIREMENTS.md`
- Checklist: `.claude/skills/chapter-standard/references/VERIFICATION_CHECKLIST.md`
- CH02 example: `.claude/skills/chapter-standard/references/CH02_REFERENCE.md`
- Master template: `legacy/docs/MASTER_TEMPLATE_CHAPTER_STRUCTURE.md`
```

---

## What Gets Auto-Fixed

**Safe, deterministic fixes only** (additive, no deletions):

### 1. Missing Visual Summary
- **Issue**: Cell 0 missing visual summary image
- **Fix**: Insert image template with chapter-specific URL
- **Approach**: Prepend to Cell 0 source

### 2. Missing Key Concept Placeholders
- **Issue**: Section missing Key Concept box
- **Fix**: Insert placeholder with TODO marker
- **Approach**: Add after identified section
- **Manual step**: Fill in actual content

### 3. Empty Closing Cell
- **Issue**: No empty cell at notebook end
- **Fix**: Append empty markdown cell
- **Approach**: Ensure proper spacing

### 4. Spacing Issues
- **Issue**: Missing blank lines after headers
- **Fix**: Add proper spacing
- **Approach**: Format consistently

---

## Manual Review Required

**NOT auto-fixed** (requires human judgment):

### Content Quality
- Key Concept wording and accuracy
- Learning Objectives alignment with content
- Practice Exercise relevance
- Interpretation accuracy

### Structural Decisions
- Section renumbering (risk of breaking references)
- Key Concept placement optimization
- Task difficulty progression
- Case Study selection

### Pedagogical Soundness
- Concept sequencing
- Example appropriateness
- Exercise difficulty
- Explanation clarity

### Technical Accuracy
- Mathematical formulas
- Code correctness
- Statistical interpretations
- Economic context

---

## Template Reference

### Primary Source

**File**: `legacy/docs/MASTER_TEMPLATE_CHAPTER_STRUCTURE.md` (1,280 lines)
- Version 2.0 (January 31, 2026)
- Authoritative canonical template
- Complete hierarchical structure
- Two case study approaches
- Quality checklist

### Detailed References

**TEMPLATE_REQUIREMENTS.md** (~300 lines)
- Distilled quick reference from master template
- Hierarchical structure (H1→H2→H3→H4)
- Cell composition targets
- Validation rules (CRITICAL/MINOR/SUGGESTIONS)
- Case Studies structure with progressive scaffolding

**VERIFICATION_CHECKLIST.md** (~200 lines)
- Human-readable checklist for manual reviews
- Organized by priority
- Complete with examples

**CH02_REFERENCE.md** (~150 lines)
- Concrete example (CH02 is gold standard)
- Cell-by-cell breakdown
- Key Concept examples with actual text
- What makes it exemplary

### Gold Standard Example

**CH02: Univariate Data Summary**
- 74 cells (77% markdown, 23% code)
- 9 Key Concepts (7 main + 2 case study)
- 1.83 MB PDF
- Compliance: 95-100
- **Use as reference when in doubt**

---

## Common Issues & Solutions

### Issue 1: Low Key Concept Count
**Problem**: Only 5 Key Concepts (target: 7-11)

**Solution**:
1. Review main sections for missing concepts
2. Identify 2-3 sections needing Key Concept boxes
3. Add placeholders with `--apply`
4. Fill in content manually
5. Verify placement is strategic (after explanation)

### Issue 2: Section Numbering Gaps
**Problem**: Sections jump from 5.3 to 5.5

**Solution**:
1. Check if gap is documented (reserved for future content)
2. If undocumented, flag as CRITICAL issue
3. Manual decision: renumber or document
4. **Not auto-fixed** (risk of breaking references)

### Issue 3: Misplaced Interpretations
**Problem**: Interpretation text appears in wrong section

**Solution**:
1. Skill flags potential misplacements with cell numbers
2. Human reviews code output and interpretation content
3. If misplaced, manually move cell to correct section
4. Re-run verification to confirm fix

### Issue 4: Missing Case Study Elements
**Problem**: Case study missing tasks or Key Concepts

**Solution**:
1. Review MASTER_TEMPLATE_CHAPTER_STRUCTURE.md
2. Add missing H4 tasks (6 total required)
3. Insert 2-3 Key Concepts at strategic points
4. Verify progressive difficulty labels
5. Add "What You've Learned" H3 section

### Issue 5: Incorrect Header Hierarchy
**Problem**: Using H2 for tasks instead of H4

**Solution**:
1. Manual correction required
2. Case Studies: H2 X.11 → H3 subsections → H4 tasks
3. Update all task headers to H4 level
4. Ensure difficulty labels present
5. Verify with `--all` after changes

---

## Integration with Existing Workflow

### Before PDF Generation

**Standard Workflow** (enhanced):
```bash
# 1. Verify compliance first
/chapter-standard ch05

# 2. If compliance < 90, apply fixes
/chapter-standard ch05 --apply

# 3. Manual review and content addition
# [Fill in Key Concept placeholders, verify interpretations]

# 4. Verify again
/chapter-standard ch05

# 5. Generate PDF when compliance ≥ 90
cd notebooks_colab && jupyter nbconvert --to html ch05_*.ipynb && cd ..
python3 scripts/inject_print_css.py notebooks_colab/ch05_*.html notebooks_colab/ch05_*_printable.html
python3 scripts/generate_pdf_playwright.py ch05

# 6. Verify PDF
open notebooks_colab/ch05_*.pdf
```

### With Git Workflow

```bash
# Standardize chapter
/chapter-standard ch07 --apply

# Review changes
git diff notebooks_colab/ch07_*.ipynb

# Commit if satisfactory
git add notebooks_colab/ch07_*.ipynb
git commit -m "Standardize CH07 to template (compliance: 92/100)"

# Generate PDF for commit
python3 scripts/generate_pdf_playwright.py ch07
git add notebooks_colab/ch07_*.pdf
git commit -m "Add CH07 PDF (1.5MB, template compliant)"

# Push to remote
git push origin main
```

---

## Compliance Score Breakdown

### Score Calculation

**100 points total:**

**CRITICAL issues** (-10 points each, max -40):
- Missing visual summary (-10)
- Missing Learning Objectives (-10)
- Missing Key Takeaways (-10)
- Missing Practice Exercises (-10)

**MINOR issues** (-5 points each, max -25):
- Section numbering gaps (-5)
- Key Concept count outside 7-11 range (-5)
- Cell count outside 45-75 range (-5)
- Misplaced interpretations (-5)
- Missing transition notes (-5)

**SUGGESTIONS** (-2 points each, max -10):
- Markdown ratio outside 70-80% (-2)
- Empty closing cell missing (-2)
- Horizontal rules missing (-2)
- Minor spacing issues (-2)

**Score Tiers:**
- **90-100**: Exemplary (publication-ready)
- **80-89**: Good (minor fixes needed)
- **70-79**: Acceptable (several improvements needed)
- **60-69**: Needs work (significant issues)
- **< 60**: Not compliant (major restructuring needed)

---

## Troubleshooting

### Skill Won't Invoke
**Issue**: Error when calling `/chapter-standard ch05`

**Solutions**:
1. Verify skill exists: `ls .claude/skills/chapter-standard/SKILL.md`
2. Check YAML frontmatter is valid
3. Ensure scripts are executable
4. Check Python dependencies installed

### Script Execution Fails
**Issue**: Python script errors

**Solutions**:
1. Verify notebook exists: `ls notebooks_colab/ch05_*.ipynb`
2. Check Python 3 installed: `python3 --version`
3. Verify script permissions: `chmod +x .claude/skills/chapter-standard/scripts/*.py`
4. Test script directly: `python3 .claude/skills/chapter-standard/scripts/verify_chapter.py ch05`

### Backup Not Created
**Issue**: No backup file in notebooks_colab/backups/

**Solutions**:
1. Verify directory exists: `ls notebooks_colab/backups/`
2. Check write permissions
3. Ensure enough disk space
4. Review apply_fixes.py logs

### False Positives
**Issue**: Skill reports issues that aren't real problems

**Solutions**:
1. Review TEMPLATE_REQUIREMENTS.md for intentional variations
2. Check if issue is documented (e.g., section gaps)
3. Verify against CH02 reference implementation
4. Report false positive for skill improvement

---

## Advanced Usage

### JSON Output Mode

```bash
# For programmatic processing
/chapter-standard ch05 --json
```

Returns structured JSON:
```json
{
  "file": "ch05_Bivariate_Data_Summary.ipynb",
  "compliance_score": 85,
  "critical": [],
  "minor": [
    {
      "issue": "Key Concept count",
      "current": 6,
      "target": "7-11",
      "cells": [12, 20, 28, 35, 42, 50]
    }
  ],
  "suggestions": [],
  "auto_fixable": ["add_key_concept_placeholder"]
}
```

### Batch Processing (Future)

```bash
# Verify all chapters
/chapter-standard --all

# Generates summary table
# Similar to verify_ch01_04_consistency.py output
```

---

## Success Metrics

After using this skill, you should see:

✅ **Reduced verification time**: 30 min → 2 min
✅ **Clear, prioritized issues**: CRITICAL/MINOR/SUGGESTIONS
✅ **Actionable recommendations**: Specific cell numbers and fixes
✅ **Safe automation**: Backups + additive-only changes
✅ **Consistent quality**: All chapters meet exemplary standard
✅ **Efficient workflow**: Seamless PDF generation integration

---

## Support & Documentation

**Questions about the template?**
- Read: `legacy/docs/MASTER_TEMPLATE_CHAPTER_STRUCTURE.md`
- Reference: `.claude/skills/chapter-standard/references/TEMPLATE_REQUIREMENTS.md`
- Example: `.claude/skills/chapter-standard/references/CH02_REFERENCE.md`

**Questions about verification?**
- Checklist: `.claude/skills/chapter-standard/references/VERIFICATION_CHECKLIST.md`
- Scripts: `.claude/skills/chapter-standard/scripts/`

**Need help?**
- Project README: `README.md`
- Logs: `log/` directory (especially `20260204_PROJECT_STATUS_UPDATE.md`)
- CLAUDE.md: Project-specific instructions

---

**Version**: 1.0
**Created**: February 6, 2026
**Based on**: CH01-04 Part I (compliance: 4.95/5)
**Primary Template**: `legacy/docs/MASTER_TEMPLATE_CHAPTER_STRUCTURE.md` (v2.0)
**Skill Author**: AI-assisted implementation following best practices
