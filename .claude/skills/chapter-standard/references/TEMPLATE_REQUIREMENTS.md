# metricsAI Chapter Template Requirements

**Version**: 2.0 (Extracted from MASTER_TEMPLATE_CHAPTER_STRUCTURE.md)
**Date**: February 6, 2026
**Primary Source**: `notebooks_colab/MASTER_TEMPLATE_CHAPTER_STRUCTURE.md` (1,280 lines)
**Purpose**: Quick reference for chapter standardization

---

## Primary Template Source

**Authoritative Template**: `notebooks_colab/MASTER_TEMPLATE_CHAPTER_STRUCTURE.md`
- Version 2.0 (January 31, 2026)
- Complete hierarchical structure (H1→H2→H3→H4)
- Two case study approaches (Markdown-only vs Code cells)
- Progressive scaffolding strategies
- Quality checklist
- 1,280 lines of comprehensive guidance

**This document** provides distilled quick reference. **Always consult the master template** for complete details.

---

## Hierarchical Structure

### Header Levels

**H1 (`#`)**: Chapter title only
- Format: `# Chapter X: [Chapter Title]`
- Used exactly once at the beginning

**H2 (`##`)**: Major sections
- Learning Objectives
- Chapter Overview
- Setup
- X.1 through X.N (content sections)
- Key Takeaways
- Practice Exercises
- X.11 Case Studies

**H3 (`###`)**: Case study subsections
- Case Study 1: [Research Title]
- Load the Data
- How to Use These Tasks
- What You've Learned from This Case Study

**H4 (`####`)**: Individual tasks
- Task 1: [Title] (Guided)
- Task 2: [Title] (Semi-guided)
- Task 3: [Title] (Semi-guided)
- Task 4: [Title] (More Independent)
- Task 5: [Title] (Independent)
- Task 6: [Title] (Independent)

### Case Studies Hierarchy

```
H2: X.11 Case Studies
├─ H3: Case Study 1: [Title]
│  └─ Key Concept Box 1 (Theoretical concept)
├─ H3: Load the [Dataset Name]
│  └─ Code cells (data loading + display)
├─ H3: How to Use These Tasks
├─ H4: Task 1 (Guided)
│  └─ Markdown-only or Code cell
├─ H4: Task 2 (Semi-guided)
│  └─ Markdown-only or Code cell
│  └─ Key Concept Box 2 (Data structure/methodology)
├─ H4: Task 3 (Semi-guided)
├─ H4: Task 4 (More Independent)
├─ H4: Task 5 (Independent)
│  └─ Key Concept Box 3 (Interpretation/causality)
├─ H4: Task 6 (Independent)
└─ H3: What You've Learned
```

---

## Cell Composition Targets

### Overall Metrics

| Metric | Target | CH02 Reference |
|--------|--------|----------------|
| **Total cells** | 45-75 | 74 |
| **Markdown cells** | 70-80% | 77% (57 cells) |
| **Code cells** | 20-30% | 23% (17 cells) |
| **Markdown:Code ratio** | 3:1 to 4:1 | 3.35:1 |

### Composition by Section

| Section | Typical Cells | Description |
|---------|---------------|-------------|
| Front matter | 4-6 | Title, objectives, overview, setup |
| Main content | 30-50 | Sections, Key Concepts, code, outputs |
| Back matter | 3-5 | Key Takeaways, exercises, closing |
| Case Studies | 15-25 | Research intro, tasks, summary |

### Cell Count Standards

- **Minimum**: 45 cells (below triggers MINOR issue)
- **Optimal**: 50-70 cells
- **Maximum**: 75 cells (above triggers MINOR issue)
- **CH02**: 74 cells (ideal reference)

---

## Front Matter Structure

### Cell 0: Visual Summary (Markdown)

**Required Elements**:
```html
<p align="center">
  <img src="https://raw.githubusercontent.com/quarcs-lab/metricsai/main/images/ch##_visual_summary.jpg"
       alt="Chapter ## Visual Summary"
       width="65%">
</p>

[2-4 sentence description]
```

**Validation**:
- ✅ Image width exactly `65%`
- ✅ Alt text format: `"Chapter ## Visual Summary"`
- ✅ Blank line after image before description
- ❌ **CRITICAL if missing**

### Cell 1: Learning Objectives (Markdown)

**Format**:
```markdown
## Learning Objectives

By the end of this chapter, you will be able to:

- [Action verb] [specific competency]
- [Action verb] [specific competency]
...
```

**Validation**:
- ✅ 6-10 bullet points (CH02 has 9)
- ✅ Each starts with action verb
- ✅ No duplicates with Key Takeaways
- ❌ **CRITICAL if missing**

**Action Verbs**: Calculate, Interpret, Understand, Analyze, Apply, Create, Distinguish, Identify, Recognize, Evaluate

### Cell 2: Chapter Overview (Markdown)

**Format**:
```markdown
## Chapter Overview

[Opening paragraph: 2-3 sentences]

**What you'll learn:**
- [Key topic 1]
- [Key topic 2]
- [Key topic 3]

**Dataset used:**
- **DATASET.dta**: [Description]

**Chapter outline:**
- X.1 [Section Title]
- X.2 [Section Title]
...
- X.10 Practice Exercises
- X.11 Case Studies
```

**Validation**:
- ✅ Outline matches actual section numbers
- ✅ Includes X.10 and X.11 (standard)
- ⚠️ MINOR if outline mismatch

### Cells 3-4: Setup

**Cell 3 (Markdown)**:
```markdown
## Setup

Run this cell first to import all required packages...
```

**Cell 4 (Code)**:
```python
# Import required libraries
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import statsmodels.api as sm

# Set random seed
RANDOM_SEED = 42
np.random.seed(RANDOM_SEED)

# GitHub data URL
GITHUB_DATA_URL = "..."

print("✓ Setup complete!")
```

**Validation**:
- ✅ Setup header present
- ✅ Code cell imports essentials
- ⚠️ MINOR if missing

---

## Main Content Sections

### Section Numbering

**Pattern**: `## X.Y [Section Title]`

**Standards**:
- **Sequential**: X.1, X.2, X.3, ..., X.N (preferred, like CH04)
- **With Gaps**: Document reason (e.g., "X.7 reserved for future")

**Common Patterns**:
- CH01: 1.1-1.9, 1.10 (reserved), 1.11 (case study)
- CH02: 2.1-2.6, 2.7 (reserved), 2.8 (case study)
- CH03: 3.1-3.5, 3.6 (reserved), 3.7-3.8
- CH04: 4.1-4.8 (sequential, no gaps) ✅ Best

**Validation**:
- ✅ Sequential or documented gaps
- ❌ **CRITICAL if undocumented gaps**

### Key Concept Boxes

**Format**:
```markdown
> **Key Concept**: [2-3 sentence synthesis of main idea. Focus on conceptual understanding, not procedural steps.]
```

**Distribution Requirements**:
- **Main content**: 4-6 boxes
- **Case Studies**: 2-3 boxes
- **Total**: 7-11 per chapter (9+ preferred)

**Strategic Placement**:
- After introducing major theoretical concepts
- After key methodological sections
- Before complex applications
- To reinforce critical distinctions

**CH02 Example Locations**: Cells 11, 20, 27, 34, 40, 47, 54, 61, 70 (9 total)

**Validation**:
- ✅ 7-11 total (CH02: 9)
- ⚠️ **MINOR if count outside range**
- ⚠️ MINOR if poorly distributed

### Transition Notes

**Format**:
```markdown
**Transition:** [1-2 sentences connecting previous section to next section]
```

**Placement**:
- Between data exploration and modeling
- Between theory and application
- Before major methodological shifts

**Validation**:
- ✅ 2-4 per chapter
- 💡 SUGGESTION if count low

---

## Back Matter Structure

### Key Takeaways

**Format**:
```markdown
## Key Takeaways

**[Thematic Group 1]:**
- [Takeaway 1]
- [Takeaway 2]
- [Takeaway 3]

**[Thematic Group 2]:**
- [Takeaway 1]
- [Takeaway 2]

[... 5-7 groups ...]

---

**Next Steps:**
- **Chapter X+1**: [Preview]
- **Chapter X+2**: [Preview]

**You have now mastered:**
✓ [Skill 1]
✓ [Skill 2]
✓ [Skill 3]

[Motivational closing sentence]
```

**Validation**:
- ✅ 5-7 thematic groups
- ✅ 15-25 total bullet points
- ❌ **CRITICAL if missing**

**Thematic Group Examples**:
- "Statistical Methods and Data Types"
- "Python Tools and Workflow"
- "Interpretation and Application"

### Practice Exercises

**Format**:
```markdown
## Practice Exercises

Test your understanding with these exercises:

**Exercise 1:** [Topic]
- (a) [Question]
- (b) [Question]

**Exercise 2:** [Topic]
- [Question]

[... 6-10 total ...]

---
```

**Validation**:
- ✅ 6-10 exercises (CH02: 8)
- ✅ Progressive difficulty
- ❌ **CRITICAL if missing**

### Empty Closing Cell

**Format**: Empty markdown cell at very end

**Purpose**: Visual breathing room

**Validation**:
- ✅ Last cell is empty markdown
- 💡 SUGGESTION if missing

---

## Case Studies Structure

### When to Include

**Include Case Studies**:
- ✅ Applied chapters (statistical methods, regression)
- ✅ Chapters with multiple practical techniques

**Exceptions** (no case study):
- ❌ Purely theoretical chapters (like CH03)
- ❌ Introductory overview chapters

### Section X.11 Case Studies

**H2 Header**:
```markdown
## X.11 Case Studies

[1-2 paragraph introduction]

**Why case studies matter:**
- [Reason 1]
- [Reason 2]
- [Reason 3]
```

### H3: Case Study 1 Introduction

**Format**:
```markdown
### Case Study 1: [Research Title]

**Research Question**: [Clear research question]

**Background**: [2-3 sentences explaining theoretical context]

**This Research** ([Author, Year](link)): [2-3 sentences]

**The Data**: [Description]
- **[Variable category 1]**: [Variables]
- **[Variable category 2]**: [Variables]

**Your Task**: [What students will do]
```

**Followed by**: Key Concept Box 1 (Theoretical concept)

### H3: Load the Data

**Format**:
```markdown
### Load the [Dataset Name]

[1-2 sentences explaining datasets]

**Data structure notes:**
- [Note about organization]
- [Note about indexing]
```

**Code cells**:
- Load primary dataset
- Load data dictionary (if available)
- Display basic information

### H3: How to Use These Tasks

**Format**:
```markdown
### How to Use These Tasks

**Instructions:**
1. Read task objectives and instructions
2. Review example code structure
3. Create NEW code cell to write solution
4. Follow structure and fill in blanks
5. Run and test your code
6. Answer interpretation questions

**Progressive difficulty:**
- **Tasks 1-2:** Guided (fill blanks)
- **Task 3:** Semi-guided (complete partial code)
- **Tasks 4-6:** Independent (write full code)

**Tip:** Type code yourself—it builds understanding!
```

### H4: Progressive Tasks (6 Required)

**Task Scaffolding Progression**:

| Task | Level | Difficulty Label | Instructions | Code Provided |
|------|-------|------------------|--------------|---------------|
| 1 | Guided | (Guided) | Detailed steps | Full example with blanks |
| 2 | Semi-guided | (Semi-guided) | Moderate guidance | Skeleton code |
| 3 | Semi-guided | (Semi-guided) | Some guidance | Minimal skeleton |
| 4 | More Independent | (More Independent) | High-level only | Hints only |
| 5 | Independent | (Independent) | Research question | Student designs |
| 6 | Independent | (Independent) | Open-ended | Student designs |

**Difficulty Labels** (exact format):
- `(Guided)`
- `(Semi-guided)`
- `(More Independent)`
- `(Independent)`

**Not**: `(GUIDED)`, `(SEMI-GUIDED)`, or any other variation

### Two Approaches for Tasks

**Approach A: Markdown-Only** (Recommended for CH02+):
- Instructions + code examples in markdown
- Students create their own code cells
- Forces active engagement
- Cleaner notebooks

**Approach B: Code Cells** (Original CH01):
- Markdown instructions + separate code cells
- Executable examples available
- Good for complex implementations

**Both valid** - choose based on chapter level and complexity

### Key Concept Distribution in Case Studies

**Exactly 2-3 Key Concept boxes**:

1. **After research introduction** (Theoretical concept)
2. **After Task 2** (Data structure/methodology)
3. **After Task 5** (Interpretation/causality)

**Not 1, not 4** - exactly 2-3

### H3: What You've Learned

**Format**:
```markdown
### What You've Learned from This Case Study

Through this analysis, you have:
- ✓ [Skill 1]
- ✓ [Skill 2]
[... 5-7 items ...]

**Connection to the research**: [2-3 sentences]

**Looking ahead**:
- **Chapter X+1**: [How next chapter builds]
- **Chapter X+2**: [Future connections]

---

**Great work!** [Motivational sentence]
```

---

## Result Interpretation Placement

### The Issue

**Common Problem**: Text cells that interpret code results drift to wrong sections/subsections.

**Example**:
- Code executes in Section 5.3
- Interpretation text appears in Section 5.4 (WRONG)
- Breaks logical flow

### Verification Pattern

**Correct Pattern**:
```
## 5.3 [Section Title]       <- Section boundary
[Explanation text]
[Code cell]                   <- Code executes
[Interpretation markdown]     <- MUST be here (same section)
## 5.4 [Next Section]         <- Section boundary
```

**Incorrect Pattern**:
```
## 5.3 [Section Title]
[Code cell]                   <- Code executes
## 5.4 [Next Section]         <- Section boundary
[Interpretation markdown]     <- WRONG (different section)
```

### Detection

Skill flags:
- Markdown cells following code cells
- Distance from section start
- Potential misplacements for manual review

**Not auto-fixable** - requires human judgment about content relationships

---

## PDF Generation Targets

### File Size

**Target**: 1.0-2.0 MB

**Examples**:
- CH01: 1.22 MB ✅
- CH02: 1.83 MB ✅
- CH03: 1.30 MB ✅
- CH04: 1.70 MB ✅

**Validation**:
- ✅ Within 1.0-2.0 MB
- 💡 SUGGESTION if outside range

### Page Format

- Letter (8.5" × 11"), portrait
- 0.75" margins (uniform)
- Justified text alignment
- Full-width visual summaries (7")
- Optimized regression tables (7.5pt font)

---

## Validation Rules

### CRITICAL Issues (Must Fix) (-10 points each)

- ❌ Missing visual summary image
- ❌ Missing Learning Objectives section
- ❌ Missing Key Takeaways section
- ❌ Missing Practice Exercises section

**Threshold**: Any CRITICAL issue requires immediate fixing before PDF generation

### MINOR Issues (Should Fix) (-5 points each)

- ⚠️ Section numbering gaps (undocumented)
- ⚠️ Key Concept count outside 7-11 range
- ⚠️ Cell count outside 45-75 range
- ⚠️ Misplaced result interpretations
- ⚠️ Missing transition notes

**Threshold**: Fix MINOR issues before considering chapter complete

### SUGGESTIONS (Nice to Have) (-2 points each)

- 💡 Markdown ratio outside 70-80%
- 💡 Empty closing cell missing
- 💡 Horizontal rules missing
- 💡 Minor spacing issues

**Threshold**: Consider for polish and consistency

---

## Compliance Score Tiers

| Score | Tier | Status | Action |
|-------|------|--------|--------|
| 90-100 | ⭐⭐⭐⭐⭐ Exemplary | Publication-ready | Generate PDF |
| 80-89 | ⭐⭐⭐⭐ Good | Minor fixes needed | Address MINOR issues |
| 70-79 | ⭐⭐⭐ Acceptable | Several improvements | Review CRITICAL + MINOR |
| 60-69 | ⭐⭐ Needs work | Significant issues | Major revision needed |
| < 60 | ⭐ Not compliant | Restructuring needed | Restart with template |

**Target**: ≥90 before PDF generation

---

## Quick Reference: CH01-04 Standards

| Metric | CH01 | CH02 | CH03 | CH04 |
|--------|------|------|------|------|
| **Total cells** | 53 | 74 | 48 | 65 |
| **Markdown %** | 75% | 77% | 73% | 74% |
| **Key Concepts** | 7 | 9 | 9 | 11 |
| **- Main** | 4 | 7 | 9 | 9 |
| **- Case Study** | 3→2* | 2 | 0 | 2 |
| **PDF Size** | 1.22 MB | 1.83 MB | 1.30 MB | 1.70 MB |
| **Compliance** | 95/100 | 98/100 | 96/100 | 97/100 |
| **Status** | ✅ Ready | ✅ Template | ✅ Ready | ✅ Ready |

*CH01 fixed from 3 to 2 in case study (Feb 4, 2026)

---

## Reference Implementation

**Gold Standard**: CH02 (Univariate Data Summary)

**Why CH02?**
- Complete template compliance
- Exemplary structure (74 cells, 9 Key Concepts)
- Professional PDF (1.83 MB)
- Case study with 6 progressive tasks
- All sections present and well-formatted

**When in doubt**: Reference CH02 for concrete examples

---

**Version**: 2.0
**Created**: February 6, 2026
**Based on**: `notebooks_colab/MASTER_TEMPLATE_CHAPTER_STRUCTURE.md` (v2.0)
**For**: `chapter-standard` skill verification
**Always refer to**: Master template for complete details
