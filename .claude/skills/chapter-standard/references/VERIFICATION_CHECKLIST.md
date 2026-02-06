# Chapter Verification Checklist

**Version**: 2.0 (Combined from master template and existing checklist)
**Date**: February 6, 2026
**Purpose**: Human-readable checklist for manual chapter reviews
**For**: metricsAI chapter standardization

---

## How to Use This Checklist

1. **Open the chapter notebook** in Jupyter/VSCode
2. **Work through each section** below sequentially
3. **Check off items** as you verify them
4. **Note issues** in the margins or separate document
5. **Run automated verification** with `/chapter-standard chXX`
6. **Compare findings** with your manual review

**Time estimate**: 10-15 minutes per chapter

---

## Front Matter

### Cell 0: Visual Summary
- [ ] **Present**: Visual summary image exists
- [ ] **Format**: HTML `<img>` tag with proper attributes
- [ ] **Width**: Exactly `65%`
- [ ] **Alt text**: Format `"Chapter ## Visual Summary"`
- [ ] **URL**: Points to GitHub images (metricsai/main/images/)
- [ ] **Spacing**: Blank line after image, before description
- [ ] **Description**: 2-4 sentence chapter overview

**If missing**: ❌ CRITICAL issue

### Cell 1: Learning Objectives
- [ ] **Header**: `## Learning Objectives`
- [ ] **Intro sentence**: "By the end of this chapter, you will be able to:"
- [ ] **Count**: 6-10 bullet points (CH02 has 9)
- [ ] **Action verbs**: Each starts with action verb (Calculate, Interpret, Understand, etc.)
- [ ] **Specificity**: Each objective is measurable and specific
- [ ] **Coverage**: All major topics addressed
- [ ] **No duplicates**: Different from Key Takeaways
- [ ] **Formatting**: Each bullet on separate line

**If missing**: ❌ CRITICAL issue
**If count wrong**: ⚠️ MINOR issue

### Cell 2: Chapter Overview
- [ ] **Header**: `## Chapter Overview`
- [ ] **Opening**: 2-3 paragraph introduction
- [ ] **What you'll learn**: 4-6 bullet points
- [ ] **Dataset used**: Listed with descriptions
- [ ] **Chapter outline**: All sections listed
- [ ] **Outline match**: Matches actual section numbers in notebook
- [ ] **Includes X.10**: Practice Exercises listed
- [ ] **Includes X.11**: Case Studies listed (if applicable)

**If outline mismatch**: ⚠️ MINOR issue

### Cells 3-4: Setup
- [ ] **Cell 3 (Markdown)**: Setup instructions present
- [ ] **Header**: `## Setup` or `## 🔧 Setup`
- [ ] **Cell 4 (Code)**: Imports and configuration
- [ ] **Essential imports**: numpy, pandas, matplotlib, statsmodels
- [ ] **Random seed**: Set for reproducibility
- [ ] **Data URL**: GitHub data URL defined
- [ ] **Confirmation**: Print statement confirming setup
- [ ] **Runs**: Code cell executes without errors

**If missing**: ⚠️ MINOR issue

---

## Structure & Composition

### Overall Metrics
- [ ] **Total cells**: Between 45-75 (CH02: 74)
- [ ] **Markdown ratio**: 70-80% of total
- [ ] **Code ratio**: 20-30% of total
- [ ] **No empty cells**: No cells with empty content (except closing)

**If outside ranges**: ⚠️ MINOR issue

### Header Hierarchy
- [ ] **H1 (`#`)**: Used only for chapter title
- [ ] **H2 (`##`)**: Major sections (Objectives, X.1-X.11, Takeaways, Exercises)
- [ ] **H3 (`###`)**: Case study subsections (if applicable)
- [ ] **H4 (`####`)**: Case study tasks (if applicable)
- [ ] **Proper nesting**: No skipped levels (H2 → H4 without H3)

**If hierarchy wrong**: ⚠️ MINOR to CRITICAL depending on severity

### Section Numbering
- [ ] **Format**: `## X.Y [Section Title]`
- [ ] **No colons**: No colons after section numbers (X.Y not X.Y:)
- [ ] **Sequential**: X.1, X.2, X.3, ... (preferred)
- [ ] **OR documented gaps**: If gaps exist, documented reason
- [ ] **Chapter match**: X matches chapter number

**Examples of valid patterns**:
- ✅ 4.1, 4.2, 4.3, 4.4, 4.5, 4.6, 4.7, 4.8 (CH04: sequential)
- ✅ 1.1-1.9, 1.10 (reserved), 1.11 (CH01: documented gap)

**If undocumented gaps**: ❌ CRITICAL issue

---

## Main Content (Sections X.1 through X.9/X.10)

### Key Concept Boxes

**Count Requirements**:
- [ ] **Total**: 7-11 Key Concept boxes in entire chapter
- [ ] **Main content**: 4-6 boxes in sections X.1-X.9
- [ ] **Case Studies**: 2-3 boxes in X.11 (if case study present)

**Format Requirements**:
- [ ] **Blockquote syntax**: `> **Key Concept**: [text]`
- [ ] **Bold header**: "Key Concept" is bold
- [ ] **Length**: 2-3 sentences each
- [ ] **Conceptual**: Focus on understanding, not procedures
- [ ] **Placement**: After section explains concept (not before)
- [ ] **Distribution**: One per 2-3 sections (strategic placement)
- [ ] **No duplicates**: Each box unique

**Current count**: _____ (fill in after counting)

**If count wrong**: ⚠️ MINOR issue
**If poorly placed**: 💡 SUGGESTION

### Transition Notes
- [ ] **Count**: 2-4 transition notes total
- [ ] **Format**: `**Transition:** [1-2 sentences]`
- [ ] **Placement**: Between major section groups
- [ ] **Purpose**: Connect previous section to next

**Typical locations**:
- Between data exploration and modeling
- Between theory and application
- Before methodological shifts

**If count low**: 💡 SUGGESTION

### Code Cells
- [ ] **All execute**: No errors when running notebook
- [ ] **Comments**: Non-obvious code explained
- [ ] **Output**: Displays properly
- [ ] **Visualizations**: Render correctly
- [ ] **No debug code**: No commented-out debugging statements

**Manual verification required**

### Result Interpretation Placement (NEW)
- [ ] **After code cells**: Interpretation text follows related code
- [ ] **Same section**: Interpretation within correct section boundaries
- [ ] **Not drifted**: No interpretations in wrong sections

**Check pattern**:
```
## X.Y [Section Title]    <- Section boundary
[Code cell]               <- Code executes here
[Interpretation markdown] <- Must be HERE (same section)
## X.Z [Next Section]     <- Section boundary (interpretation should NOT be here)
```

**If misplaced**: ⚠️ MINOR issue (manual review to confirm)

---

## Back Matter

### Key Takeaways
- [ ] **Header**: `## Key Takeaways`
- [ ] **Thematic groups**: 5-7 bold group headers
- [ ] **Bullet structure**: 2-5 bullets per group
- [ ] **Total bullets**: 15-25 across all groups
- [ ] **Self-contained**: Each bullet complete on its own
- [ ] **No duplicates**: Different from Learning Objectives
- [ ] **Next Steps**: Section previewing future chapters
- [ ] **You have mastered**: Checklist with ✓ checkmarks
- [ ] **Closing**: Motivational sentence
- [ ] **Horizontal rule**: `---` before or after section

**If missing**: ❌ CRITICAL issue
**If structure wrong**: ⚠️ MINOR issue

### Practice Exercises
- [ ] **Header**: `## Practice Exercises`
- [ ] **Intro sentence**: "Test your understanding..."
- [ ] **Count**: 6-10 exercises (CH02 has 8)
- [ ] **Bold titles**: Each exercise has `**Exercise N:** [Topic]`
- [ ] **Clear statements**: Questions are unambiguous
- [ ] **Progressive difficulty**: Easy → Moderate → Hard
- [ ] **Mix of types**: Conceptual, computational, applied
- [ ] **Reference content**: Exercises use chapter concepts
- [ ] **Horizontal rule**: `---` after section

**If missing**: ❌ CRITICAL issue
**If count wrong**: ⚠️ MINOR issue

### Empty Closing Cell
- [ ] **Present**: Empty markdown cell at very end
- [ ] **Purpose**: Visual spacing

**If missing**: 💡 SUGGESTION

---

## Case Studies (If Applicable)

### When Required
- [ ] **Applied chapters**: Statistical methods, regression, inference
- [ ] **OR exception**: Documented reason for no case study (e.g., CH03 is theoretical)

### Section X.11 Case Studies

#### H2: Main Case Studies Section
- [ ] **Header**: `## X.11 Case Studies` (plural)
- [ ] **Introduction**: 1-2 paragraphs explaining case studies
- [ ] **Why section**: "Why case studies matter" with bullets
- [ ] **Proper H2**: Two hashes only

#### H3: Case Study 1 Introduction
- [ ] **Header**: `### Case Study 1: [Research Title]`
- [ ] **Research question**: Clearly stated
- [ ] **Background**: 2-3 sentences on theoretical context
- [ ] **This Research**: Citation with link ([Author, Year](URL))
- [ ] **The Data**: Description with variable categories
- [ ] **Your Task**: What students will do
- [ ] **Key Concept 1**: After introduction (theoretical concept)

#### H3: Load the Data
- [ ] **Header**: `### Load the [Dataset Name]`
- [ ] **Explanation**: 1-2 sentences about datasets
- [ ] **Data structure notes**: Bullet points on organization
- [ ] **Code cell(s)**: Load data, display head, show dictionary
- [ ] **Runs**: All code cells execute without errors

#### H3: How to Use These Tasks (Optional but Recommended)
- [ ] **Header**: `### How to Use These Tasks`
- [ ] **Instructions**: 6-step guidance for students
- [ ] **Progressive difficulty**: Explained (Guided → Independent)
- [ ] **Tip**: Encouragement to type code

#### H4: Progressive Tasks (6 Required)

**Task 1: Guided**
- [ ] **Header**: `#### Task 1: [Title] (Guided)`
- [ ] **Label format**: Parentheses, title case (Guided not GUIDED)
- [ ] **Objective**: Clear learning goal
- [ ] **Instructions**: Detailed steps (4-6 steps)
- [ ] **Chapter connection**: Reference to chapter section
- [ ] **Code/scaffold**: Full example with blanks OR code cell
- [ ] **Hints**: Inline hints provided

**Task 2: Semi-guided**
- [ ] **Header**: `#### Task 2: [Title] (Semi-guided)`
- [ ] **Difficulty**: Moderate guidance
- [ ] **Scaffold**: Skeleton code with gaps
- [ ] **Key Concept 2**: After Task 2 (data structure/methodology)

**Task 3: Semi-guided**
- [ ] **Header**: `#### Task 3: [Title] (Semi-guided)`
- [ ] **Difficulty**: Some guidance
- [ ] **Scaffold**: Minimal structure

**Task 4: More Independent**
- [ ] **Header**: `#### Task 4: [Title] (More Independent)`
- [ ] **Difficulty**: High-level instructions only
- [ ] **Scaffold**: Hints and outline

**Task 5: Independent**
- [ ] **Header**: `#### Task 5: [Title] (Independent)`
- [ ] **Difficulty**: Research question format
- [ ] **Scaffold**: Student designs approach
- [ ] **Key Concept 3**: After Task 5 (interpretation/causality)

**Task 6: Independent**
- [ ] **Header**: `#### Task 6: [Title] (Independent)`
- [ ] **Difficulty**: Open-ended
- [ ] **Scaffold**: Minimal to none

**Difficulty Labels Checklist**:
- [ ] All labels use parentheses: `(Guided)` not `GUIDED` or `Guided:`
- [ ] Exact format: `(Guided)`, `(Semi-guided)`, `(More Independent)`, `(Independent)`
- [ ] No variations or creative labels

**Task Approach**:
- [ ] **Identified**: Markdown-only OR Code cells approach used consistently
- [ ] **If Markdown-only**: Code examples in markdown cells
- [ ] **If Code cells**: Separate executable cells after instructions

#### H3: What You've Learned
- [ ] **Header**: `### What You've Learned from This Case Study`
- [ ] **Summary**: 1-2 paragraphs on skills practiced
- [ ] **Bullets**: 5-7 items with ✓ checkmarks
- [ ] **Connection**: 2-3 sentences linking to research
- [ ] **Looking ahead**: Preview of future chapters
- [ ] **Horizontal rule**: `---` after section
- [ ] **Closing**: Motivational message

### Case Studies: Key Concepts
- [ ] **Count**: Exactly 2-3 Key Concept boxes within case study
- [ ] **Location 1**: After research introduction (theoretical)
- [ ] **Location 2**: After Task 2 (data structure/methodology)
- [ ] **Location 3** (optional): After Task 5 (interpretation/causality)

**If count wrong**: ⚠️ MINOR issue (must be exactly 2-3, not 1 or 4)

---

## Formatting Consistency

### Markdown Conventions
- [ ] **Bold**: `**text**` for key terms, section labels
- [ ] **Italics**: `*text*` for emphasis (sparingly)
- [ ] **Code**: `` `code` `` for inline code
- [ ] **Blockquotes**: `>` for Key Concept boxes only
- [ ] **Lists**: `-` for unordered, `1.` for ordered
- [ ] **Spacing**: Blank lines after headers, before/after lists

### LaTeX Math
- [ ] **Inline**: `$variable$` or `$formula$`
- [ ] **Display**: `$$formula$$`
- [ ] **Renders**: All formulas display correctly

### Horizontal Rules
- [ ] **After**: Learning Objectives
- [ ] **Before/after**: Key Takeaways
- [ ] **After**: Practice Exercises
- [ ] **After**: Case Studies conclusion
- [ ] **Format**: `---` (three hyphens)

**If missing**: 💡 SUGGESTION

---

## PDF Generation

### Pre-Generation Checks
- [ ] **Compliance score**: ≥90 from `/chapter-standard chXX`
- [ ] **All code runs**: Notebook executes end-to-end without errors
- [ ] **No errors**: No Python tracebacks in outputs

### PDF Quality (After Generation)
- [ ] **File size**: 1.0-2.0 MB (CH01: 1.22 MB, CH02: 1.83 MB, CH03: 1.30 MB, CH04: 1.70 MB)
- [ ] **Renders**: All elements display correctly
- [ ] **Images**: Visual summaries at full width
- [ ] **Tables**: Regression tables fit without wrapping
- [ ] **Math**: LaTeX formulas render correctly
- [ ] **Links**: Hyperlinks are clickable

**If outside range**: 💡 SUGGESTION

---

## Content Quality (Manual Review)

### Accuracy
- [ ] **Facts**: All factual statements correct
- [ ] **Math**: Mathematical formulas accurate
- [ ] **Statistics**: Statistical interpretations correct
- [ ] **Economics**: Economic context appropriate
- [ ] **Code**: All code produces correct results
- [ ] **Citations**: References accurate (if present)

### Clarity
- [ ] **Explanations**: Concepts explained clearly
- [ ] **Examples**: Examples relevant and helpful
- [ ] **Instructions**: Task instructions unambiguous
- [ ] **Terminology**: Technical terms defined
- [ ] **Flow**: Logical progression of ideas

### Pedagogy
- [ ] **Scaffolding**: Appropriate support for learning
- [ ] **Difficulty**: Suitable for target audience
- [ ] **Engagement**: Content interesting and motivating
- [ ] **Application**: Theory connected to practice
- [ ] **Assessment**: Exercises test chapter concepts

### Consistency
- [ ] **Style**: Writing style consistent throughout
- [ ] **Formatting**: Markdown formatting uniform
- [ ] **Terminology**: Same terms used consistently
- [ ] **Notation**: Mathematical notation consistent

---

## Final Checks

### Cross-References
- [ ] **Chapter links**: References to other chapters work
- [ ] **Section refs**: Internal section references correct
- [ ] **Figure refs**: Figure/table references accurate
- [ ] **Data URLs**: All external data URLs load

### Proofreading
- [ ] **Spelling**: No spelling errors
- [ ] **Grammar**: No grammatical errors
- [ ] **Punctuation**: Punctuation correct
- [ ] **Capitalization**: Consistent capitalization

### Git Status
- [ ] **Saved**: All changes saved to file
- [ ] **Committed**: Ready to commit (if appropriate)
- [ ] **Message**: Commit message prepared

---

## Compliance Scoring

**Your Assessment**: _____ / 100

**Breakdown**:
- CRITICAL issues (×10): _____ issues = _____ points deducted
- MINOR issues (×5): _____ issues = _____ points deducted
- SUGGESTIONS (×2): _____ issues = _____ points deducted

**Tier**:
- [ ] 90-100: ⭐⭐⭐⭐⭐ Exemplary (publication-ready)
- [ ] 80-89: ⭐⭐⭐⭐ Good (minor fixes needed)
- [ ] 70-79: ⭐⭐⭐ Acceptable (improvements needed)
- [ ] 60-69: ⭐⭐ Needs work (significant issues)
- [ ] < 60: ⭐ Not compliant (major restructuring)

---

## Ready for Publication?

**Final Decision**:
- [ ] **YES** - All CRITICAL issues resolved, compliance ≥90
- [ ] **NO** - See issues list above

**Notes**:
_[Add any specific concerns or recommendations]_

---

**Reviewer**: _________________
**Date**: _________________
**Chapter**: _________________
**Compliance**: _____ / 100

---

**Version**: 2.0
**Created**: February 6, 2026
**Sources**: MASTER_TEMPLATE_CHAPTER_STRUCTURE.md (Quality Checklist) + TEMPLATE_CHECKLIST.md
**For**: Manual chapter verification (complement to automated `/chapter-standard` skill)
