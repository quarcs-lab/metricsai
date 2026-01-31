# Master Template: Complete Chapter Structure

**Version:** 2.0 (Updated with Case Studies hierarchical structure)
**Date:** January 31, 2026
**Based on:** Chapter 1 (Analysis of Economics Data) - Full implementation
**Purpose:** Canonical template for all chapters (CH01-CH17)

---

## Document Overview

This master template documents the complete hierarchical structure used in Chapter 1, including the new **Case Studies section with hierarchical organization**. Use this as the reference for applying consistent structure to all chapters.

**Key Features:**
- Clear section hierarchy (H1 → H2 → H3 → H4)
- Pedagogical elements (Learning Objectives, Key Concepts, Practice Exercises)
- New hierarchical Case Studies structure
- Progressive scaffolding approach
- Professional formatting conventions

---

## Complete Chapter Structure

### Level 0: Chapter Metadata (Header Block)

```markdown
# Chapter X: [Chapter Title]

**metricsAI: An Introduction to Econometrics with Python and AI in the Cloud**

*[Carlos Mendez](https://carlos-mendez.org)*

<img src="https://raw.githubusercontent.com/quarcs-lab/metricsai/main/images/chXX_visual_summary.jpg" alt="Chapter XX Visual Summary" width="65%">

[Brief 2-3 sentence description of the chapter]

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/quarcs-lab/metricsai/blob/main/notebooks_colab/chXX_[Chapter_Name].ipynb)
```

**Components:**
- H1 chapter title
- Project subtitle
- Author link
- Visual summary image (65% width)
- Brief description (2-3 sentences)
- Colab badge with link

**Guidelines:**
- Replace `X` or `XX` with chapter number (e.g., `01`, `02`, `17`)
- Replace `[Chapter Title]` with actual title
- Replace `[Chapter_Name]` with filename-friendly version
- Keep visual summary at 65% width for consistency
- Description should be concise and informative

---

### Level 1: Learning Objectives (H2)

```markdown
## Learning Objectives

By the end of this chapter, you will be able to:
- [Learning objective 1]
- [Learning objective 2]
- [Learning objective 3]
- [Learning objective 4]
- [Learning objective 5]
- [Learning objective 6]

---
```

**Guidelines:**
- Use H2 (`##`) for section header
- List 5-8 measurable learning objectives
- Use action verbs: distinguish, identify, understand, recognize, calculate, interpret, apply
- Focus on skills students will gain
- End with horizontal rule (`---`) for visual separation

**Example objectives:**
- "Distinguish between descriptive analysis and statistical inference"
- "Calculate standard errors for regression coefficients"
- "Interpret confidence intervals in economic context"

---

### Level 2: Chapter Overview (H2)

```markdown
## Chapter Overview

[2-3 paragraph introduction to the chapter content]

**What you'll learn:**
- [Key topic 1]
- [Key topic 2]
- [Key topic 3]
- [Key topic 4]

**Dataset used:**
- **DATASET_NAME**: [Brief description]
  - Variables: [List key variables]

**Chapter outline:**
- X.1 [Section Title]
- X.2 [Section Title]
- X.3 [Section Title]
- X.4 [Section Title]
- X.5 [Section Title]
- X.6 [Section Title]
- X.7 [Section Title]
- X.8 [Section Title]
- X.9 [Section Title]
- X.10 Practice Exercises
- X.11 Case Studies
```

**Guidelines:**
- Use H2 (`##`) for section header
- Opening paragraph: Set context and motivate the chapter
- "What you'll learn": 4-6 bullet points on key concepts/methods
- "Dataset used": Describe primary dataset(s) with variables
- "Chapter outline": List all sections with numbering (X.1, X.2, etc.)
- **Always include X.10 Practice Exercises**
- **Always include X.11 Case Studies** (new standard)

---

### Level 3: Setup (H2 + Code Cell)

```markdown
## Setup

Run this cell first to import all required packages and configure the environment. This sets up:
- Data manipulation (pandas, numpy)
- Statistical modeling (statsmodels)
- Visualization (matplotlib)
- Reproducibility (random seeds)
```

**Followed by code cell:**

```python
# Import required libraries
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import statsmodels.api as sm
from statsmodels.formula.api import ols
import random
import os

# Set random seeds for reproducibility
RANDOM_SEED = 42
random.seed(RANDOM_SEED)
np.random.seed(RANDOM_SEED)
os.environ['PYTHONHASHSEED'] = str(RANDOM_SEED)

# GitHub data URL
GITHUB_DATA_URL = "https://raw.githubusercontent.com/quarcs-lab/data-open/master/AED/"

# Optional: Create directories
IMAGES_DIR = 'images'
TABLES_DIR = 'tables'
os.makedirs(IMAGES_DIR, exist_ok=True)
os.makedirs(TABLES_DIR, exist_ok=True)

print("✓ Setup complete! All packages imported successfully.")
print(f"✓ Random seed set to {RANDOM_SEED} for reproducibility.")
print(f"✓ Data will stream from: {GITHUB_DATA_URL}")
```

**Guidelines:**
- Use H2 (`##`) for "Setup" header
- Markdown cell explains what the setup does
- Code cell imports all necessary packages
- Set reproducibility seed (42)
- Configure data URLs
- Print confirmation messages

---

### Level 4: Content Sections (H2, X.1 - X.9)

```markdown
## X.1 [Section Title]

[Section content - explanation, examples, theory]

[Optional: Mathematical formulas using LaTeX]

[Economic interpretation and context]
```

**Followed by optional code cell:**

```python
# Code demonstrating the concept
[Python code here]
```

**Guidelines:**
- Use H2 (`##`) for section headers
- Number sections sequentially (X.1, X.2, X.3, ...)
- Each section covers one major concept or method
- Include:
  - Clear explanations
  - Economic context
  - Mathematical formulas (when needed)
  - Code examples (when applicable)
  - Interpretation of results
- Typical chapter has 8-10 content sections (X.1 to X.9 or X.10)

**Content section patterns:**
- **Introduction sections (X.1)**: Define concepts, set up framework
- **Data sections (X.2-X.4)**: Load, preview, explore data
- **Visualization sections (X.5)**: Create plots
- **Analysis sections (X.6-X.7)**: Fit models, run tests
- **Interpretation sections (X.8-X.9)**: Explain results, discuss implications

---

### Level 5: Key Concept Boxes (Blockquote)

Insert after relevant content sections:

```markdown
> **Key Concept**: [Concise 2-4 sentence explanation of a critical concept]
```

**Guidelines:**
- Use blockquote format (`>`)
- Bold "Key Concept:" prefix
- 2-4 sentences maximum
- Focus on one key idea
- Place immediately after the section introducing the concept
- Typical chapter has 4-6 Key Concept boxes

**Example:**

```markdown
> **Key Concept**: Descriptive analysis summarizes data using statistics and visualizations, while statistical inference uses sample data to draw conclusions about the broader population. Most econometric analysis involves statistical inference.
```

**Placement strategy:**
- After introducing major theoretical concepts
- After key methodological sections
- Before complex applications
- To reinforce critical distinctions

---

### Level 6: Transition Notes (Blockquote)

Insert between major section groups:

```markdown
**Transition:** [1-2 sentences connecting previous section to next section]
```

**Guidelines:**
- Use bold "Transition:" prefix
- 1-2 sentences only
- Explain logical flow between sections
- Helps students understand structure
- Typical chapter has 2-4 transition notes

**Example:**

```markdown
**Transition:** Before jumping into regression analysis, we need to understand our data. Descriptive statistics reveal the scale, variability, and range of our variables—essential for interpreting regression results.
```

**Placement strategy:**
- Between data exploration and modeling
- Between theory and application
- Before major methodological shifts

---

### Level 7: Key Takeaways (H2)

```markdown
## Key Takeaways

**[Thematic Group 1]:**
- [Takeaway 1]
- [Takeaway 2]
- [Takeaway 3]

**[Thematic Group 2]:**
- [Takeaway 1]
- [Takeaway 2]
- [Takeaway 3]

**[Thematic Group 3]:**
- [Takeaway 1]
- [Takeaway 2]

[Continue for 4-8 thematic groups]

---

**Next Steps:**
- **Chapter X+1**: [Preview of next chapter]
- **Chapter X+2**: [Preview of related chapter]
- **Chapters X+3-X+5**: [Preview of topic progression]

**You have now mastered:**
✓ [Skill 1]
✓ [Skill 2]
✓ [Skill 3]
✓ [Skill 4]

[Closing motivational sentence]
```

**Guidelines:**
- Use H2 (`##`) for section header
- Organize takeaways into 4-8 thematic groups
- Bold group headers (e.g., "Statistical Methods:", "Python Tools:")
- Comprehensive bullet points (15-25 total takeaways)
- Include "Next Steps" section previewing future chapters
- Include "You have now mastered" checklist with checkmarks (✓)
- End with motivational sentence
- Add horizontal rule (`---`) before closing sections

**Thematic group examples:**
- "Statistical Methods and Data Types"
- "Regression Analysis and Interpretation"
- "Practical Application"
- "Python Tools and Workflow"
- "Mathematical Background"

---

### Level 8: Practice Exercises (H2)

```markdown
## Practice Exercises

Test your understanding of [chapter topic] with these exercises:

**Exercise 1:** [Topic]
- (a) [Question part a]
- (b) [Question part b]
- (c) [Question part c]

**Exercise 2:** [Topic]
- (a) [Question part a]
- (b) [Question part b]
- (c) [Question part c]

**Exercise 3:** [Topic]
- [Question]

**Exercise 4:** [Topic]
- [Question]

**Exercise 5:** [Topic]
- [Question]

**Exercise 6:** [Topic]
- [Question]

**Exercise 7:** [Topic]
- [Question]

**Exercise 8:** [Topic]
- [Question]

---
```

**Guidelines:**
- Use H2 (`##`) for section header
- Opening sentence: "Test your understanding of [topic] with these exercises:"
- 6-10 exercises total
- Progressive difficulty: conceptual → computational → applied
- Multi-part questions for complex topics
- Include Python practice exercises
- End with horizontal rule (`---`)

**Exercise types:**
1. **Conceptual**: Define terms, explain concepts
2. **Data types**: Classify variables
3. **Interpretation**: Interpret regression output
4. **Calculation**: Use formulas, predict values
5. **Critical thinking**: Causation, limitations
6. **Statistical concepts**: R-squared, p-values
7. **Mathematical**: Summation notation, derivatives
8. **Python practice**: Replicate analysis with variations

---

### Level 9: Case Studies (H2 with Hierarchical Subsections)

**NEW SECTION - Now standard for all chapters**

```markdown
## X.11 Case Studies

[1-2 paragraph introduction to case studies section]

**Why case studies matter:**
- [Reason 1]
- [Reason 2]
- [Reason 3]
- [Reason 4]
```

**Followed by hierarchical subsections:**

---

#### Level 9.1: Case Study Introduction (H3)

```markdown
### Case Study 1: [Research Title]

**Research Question**: [Clear research question]

**Background**: [2-3 sentences explaining theoretical context]

**This Research** ([Author, Year](link-to-research)): [2-3 sentences describing the research]

**The Data**: [Description of dataset structure and variables]
- **[Variable category 1]**: [Variables listed]
- **[Variable category 2]**: [Variables listed]
- **[Variable category 3]**: [Variables listed]

**Your Task**: [1-2 sentences describing what students will do]
```

**Guidelines:**
- Use H3 (`###`) for case study title
- Start with clear research question
- Provide theoretical background
- Link to original research
- Describe dataset comprehensively
- Set clear expectations for student work

---

#### Level 9.2: Key Concept Box (after research introduction)

```markdown
> **Key Concept**: [2-4 sentences explaining key theoretical concept from research]
```

**Guidelines:**
- Place immediately after research introduction
- Explain key theoretical concept motivating the research
- Connect to chapter content

**Example:**

```markdown
> **Key Concept**: Beta convergence refers to the hypothesis that poor countries will grow faster than rich countries, eventually "catching up" in terms of income and productivity. However, evidence suggests countries may form distinct "convergence clubs" — groups that converge toward different long-run equilibrium levels rather than a single global level.
```

---

#### Level 9.3: Data Loading Section (H3)

```markdown
### Load the [Dataset Name]

[1-2 sentences explaining what datasets will be loaded]

**Data structure notes:**
- [Note about data organization]
- [Note about indexing or special features]
```

**Followed by code cell:**

```python
# Load primary dataset
df1 = pd.read_csv(
    "[URL to dataset]",
    index_col=["index1", "index2"]  # If applicable
).sort_index()

# Load data dictionary (if available)
df2 = pd.read_csv("[URL to data dictionary]")

# Display basic information
print("=" * 70)
print("[DATASET NAME]")
print("=" * 70)
print(f"Dataset shape: {df1.shape[0]} observations, {df1.shape[1]} variables")
# Add other relevant summary info

print("\n" + "=" * 70)
print("FIRST 5 OBSERVATIONS")
print("=" * 70)
print(df1.head(5))
```

**Followed by code cell (data dictionary display):**

```python
print("\n" + "=" * 75)
print("VARIABLE DEFINITIONS")
print("=" * 75)
print(df2)
```

**Guidelines:**
- Use H3 (`###`) for section header
- Explain dataset structure upfront
- Load data from GitHub URLs (no downloads required)
- Display dataset dimensions and structure
- Show first observations
- Display data dictionary (if available)

---

#### Level 9.4: Usage Instructions (Before Tasks)

**NEW: Add before Task 1 to guide students**

```markdown
### How to Use These Tasks

**Instructions:**

1. **Read the task objectives and instructions** in each section below
2. **Review the example code structure** provided
3. **Create a NEW code cell** to write your solution
4. **Follow the structure and fill in the blanks** or write complete code
5. **Run and test your code**
6. **Answer the interpretation questions**

**Progressive difficulty:**

- **Tasks 1-2:** Guided (fill in specific blanks with `_____`)
- **Task 3:** Semi-guided (complete partial code structure)
- **Tasks 4-6:** Independent (write full code from outline)

**Tip:** Type the code yourself rather than copying—it builds understanding!
```

**Guidelines:**
- Use H3 (`###`) for section header
- Explain the task structure and workflow
- Clarify progressive difficulty levels
- Encourage active learning (typing vs copying)
- Place immediately before Task 1

---

#### Level 9.5: Progressive Tasks (H4 with Two Approaches)

**IMPORTANT DECISION: Choose one approach for your chapter:**

### Approach A: Markdown-Only with Embedded Code Examples (Recommended for CH02+)

**Pedagogical Benefits:**
- Forces active engagement (students create their own cells)
- Cleaner notebook (no executed outputs)
- Easier to maintain (no execution dependencies)
- Better for PDF generation (no plot outputs)
- Clear separation between instruction and practice

**Task Structure:** Single markdown cell combining instruction + code example

---

**Task 1: Guided (Easiest) - Markdown-Only Approach**

```markdown
#### Task 1: [Task Name] (Guided)

**Objective:** [Clear learning objective]

**Instructions:**
1. [Detailed step 1]
2. [Detailed step 2]
3. [Detailed step 3]
4. [Detailed step 4]

**Chapter X connection:** [Reference to specific chapter section]

**Example code structure:**

```python
# Task 1: [Task Name] (GUIDED)
# Fill in the blanks below

# Step 1: [Step description]
print(f"Result: {_____}")  # Hint: use .method_name()
print(f"Value: {_____}")  # Hint: calculation description

# Step 2: [Step description]
for item in items:
    result = calculate_something(_____)  # Hint: what parameter?
    print(f"  {item}: {result:.2f}")

# Step 3: [Step description]
final_result = _____  # Hint: combine previous results
print(f"Final: {final_result}")
```

**Hints:**
- Use `.method()` for [specific operation]
- Calculate [formula description]
- Reference chapter section X.Y for guidance
```

**Scaffolding Strategy:**
- Specific blanks (`_____`) for students to fill in
- Inline hints with each blank
- Complete structure provided
- Students only fill missing values/methods

---

**Task 2: Semi-Guided - Markdown-Only Approach**

```markdown
#### Task 2: [Task Name] (Semi-guided)

**Objective:** [Clear learning objective]

**Instructions:**
1. [Instruction with some guidance]
2. [Instruction with some guidance]
3. [Instruction with some guidance]

**Chapter X connection:** [Reference to chapter section]

**Example code structure:**

```python
# Task 2: [Task Name] (SEMI-GUIDED)
# Complete the code by filling in blanks and adding missing sections

# Step 1: [Step description]
result_dict = {
    'Metric1': data.method1(),
    'Metric2': _____,  # Calculate metric2
    'Metric3': _____,  # Calculate metric3
}

# Step 2: [Step description]
grouped = data.groupby(_____)['column'].aggregate(_____)
print(grouped.head())

# Step 3: [Step description]
# Your code here: Create visualization
# Hint: Use plt.subplots() for figure setup
# Hint: Plot data with .plot() or .scatter()
```

**Hints:**
- Use `.method()` for metric calculations
- Group by [column name], aggregate with [function]
- Create [type of plot] with appropriate labels
```

**Scaffolding Strategy:**
- Mix of specific blanks (`_____`) and "Your code here" comments
- Show code structure with key gaps
- Some complete examples, some student-designed sections

---

**Task 3: Semi-Guided - Markdown-Only Approach**

```markdown
#### Task 3: [Task Name] (Semi-guided)

**Objective:** [Clear learning objective]

**Instructions:**
1. [Moderate guidance]
2. [Moderate guidance]
3. [Moderate guidance]

**Chapter X connection:** [Reference to chapter section]

**Example code structure:**

```python
# Task 3: [Task Name] (SEMI-GUIDED)
# Complete the visualization with missing parameters

# Create figure
fig, axes = plt.subplots(_____, _____, figsize=(14, 10))

# Panel 1: [Plot type]
axes[0, 0].plot_type(data, parameter=_____, ...)
axes[0, 0].set_xlabel(_____)
axes[0, 0].set_ylabel(_____)

# Panel 2: [Plot type]
# Your code here: Create second panel
# Hint: Use axes[0, 1] for second subplot

# Panel 3-4: [Plot types]
# Your code here: Complete remaining panels
```

**Hints:**
- Use `plt.subplots(rows, cols)` for multi-panel figures
- Set appropriate parameters for each plot type
- Label all axes clearly
```

**Scaffolding Strategy:**
- Show plot structure with missing parameters
- Mix of blanks and "Your code here" sections
- Students complete partial implementations

---

**Task 4: More Independent - Markdown-Only Approach**

```markdown
#### Task 4: [Task Name] (More Independent)

**Objective:** [Clear learning objective]

**Instructions:**
1. [High-level instruction]
2. [High-level instruction]
3. [High-level instruction]

**Chapter X connection:** [Reference to chapter section]

**Example code structure:**

```python
# Task 4: [Task Name] (MORE INDEPENDENT)
# Follow the outline to complete the analysis

# Step 1: Extract or prepare data
data_subset = original_data[condition]  # Modify condition as needed

# Step 2: Create analysis
# Your code here: Implement main analysis
# - [Specific subtask 1]
# - [Specific subtask 2]
# - [Specific subtask 3]

# Step 3: Visualize results
# Your code here: Create appropriate visualization
# Hint: Consider using [plot type] for this data
```

**Hints:**
- Filter data using [criteria]
- Apply [method] from chapter section X.Y
- Visualize with [suggested plot type]

**Questions to consider:**
- [Interpretation question 1]
- [Interpretation question 2]
```

**Scaffolding Strategy:**
- Step outline with minimal code
- "Your code here" comments with guidance
- Hints and questions for direction

---

**Task 5-6: Independent - Markdown-Only Approach**

```markdown
#### Task 5: [Task Name] (Independent)

**Objective:** [Clear learning objective]

**Instructions:**
1. [High-level goal]
2. [High-level goal]
3. [High-level goal]

**Chapter X connection:** [Reference to chapter sections]

**Example code structure:**

```python
# Task 5: [Task Name] (INDEPENDENT)
# Design your approach to answer the research question

# Step 1: [Conceptual step]
# Your code here: [What to do]
# Hint: Consider [approach suggestion]

# Step 2: [Conceptual step]
# Your code here: [What to do]
# Formula: [mathematical guidance if applicable]

# Step 3: [Conceptual step]
# Your code here: [What to do]
# Hint: Compare [aspect 1] vs [aspect 2]
```

**Hints:**
- [Methodological hint]
- [Calculation hint]
- [Interpretation hint]

**Questions to consider:**
- [Deep interpretation question 1]
- [Deep interpretation question 2]
- [Critical thinking question]
```

**Scaffolding Strategy:**
- Conceptual outline only
- Minimal code structure
- Students design full implementation
- Interpretation questions guide thinking

---

### Approach B: Code Cells with Scaffolding (Original CH01 Approach)

**Pedagogical Benefits:**
- Executable examples available
- Students can run and modify existing code
- Useful for complex implementations
- Good for instructor demonstrations

**Task Structure:** Markdown instruction + separate code cell

---

**Task 1-6: Code Cell Approach**

Same markdown instructions as Approach A, but followed by actual code cells:

```python
# Your code here: [Task description]
#
# Suggested approach:
# 1. [Step 1]
# 2. [Step 2]
# 3. [Step 3]

# Example structure:
# [commented skeleton code]
```

**When to use Code Cell Approach:**
- Complex implementations requiring example
- First few chapters where students need more support
- Tasks involving unfamiliar libraries/methods

**When to use Markdown-Only Approach:**
- Students have basic Python proficiency
- Encouraging independent problem-solving
- Reducing notebook clutter
- Better PDF generation without outputs

---

### Placeholder Strategies Reference

**Progressive scaffolding through placeholders:**

| Difficulty | Placeholder Type | Example | Use Case |
|-----------|-----------------|---------|----------|
| **Guided** | Specific blanks (`_____`) | `print(f"Mean: {_____}")` | Students fill exact values |
| **Semi-guided** | Blanks + structure | `result = data.groupby(_____)` | Students complete partial code |
| **Semi-guided** | "Your code here" + hints | `# Your code here: Create plot` | Students write code blocks |
| **Independent** | Conceptual steps | `# Step 1: Prepare data` | Students design full implementation |
| **Independent** | Minimal outline | `# Your code here` | Students create from scratch |

**Hint Conventions:**

```python
# Direct hint after blank
result = _____  # Hint: use .mean()

# Inline guidance
# Your code here: Calculate summary statistics
# Hint: Use .describe() method

# Formula hint
# Your code here: Calculate z-scores
# Formula: z = (x - mean) / std
```

---

#### Level 9.5: Key Concept Boxes (Interspersed)

Place 2-3 additional Key Concept boxes strategically:

- **After Task 2**: Concept related to data structure or methodology
- **After Task 5**: Concept related to interpretation or causality

**Example locations:**

```markdown
[After Task 2]

> **Key Concept**: Panel data combines cross-section and time series dimensions, tracking multiple entities (countries) over multiple time periods (years). This structure allows us to study both differences between countries (cross-sectional variation) and changes within countries over time (time series variation). The data is indexed by (country, year) pairs.

[After Task 5]

> **Key Concept**: [Concept about interpretation, causality, or limitations of the analysis method used in the task]
```

---

#### Level 9.6: Learning Summary (H3)

```markdown
### What You've Learned from This Case Study

[1-2 paragraph summary of what students practiced]

**Connection to the research**: [2-3 sentences connecting student work to the original research]

**Looking ahead**:
- **Chapter X**: [How next chapter builds on this]
- **Chapter Y-Z**: [How future chapters connect]
- **Chapter W-Q**: [Advanced methods for this type of problem]

---

**Great work!** [Motivational closing sentence]
```

**Guidelines:**
- Use H3 (`###`) for section header
- Summarize skills practiced (bulleted list)
- Connect student work to published research
- Preview how future chapters extend these methods
- End with motivational message
- Add horizontal rule (`---`) after section

---

### Case Studies: Complete Hierarchical Structure

**Hierarchy Summary:**

```
H2: X.11 Case Studies (Main section)
│
├─ H3: Case Study 1: [Title] (Research introduction)
│  └─ Key Concept Box 1 (Theoretical concept)
│
├─ H3: Load the Data (Data setup section)
│  └─ Code cells (data loading + display)
│
├─ H4: Task 1 (Guided)
│  └─ Code cell (with detailed scaffolding)
│
├─ H4: Task 2 (Semi-guided)
│  └─ Code cell (with moderate scaffolding)
│  └─ Key Concept Box 2 (Data structure/methodology)
│
├─ H4: Task 3 (Semi-guided)
│  └─ Code cell (less scaffolding)
│
├─ H4: Task 4 (More independent)
│  └─ Code cell (minimal scaffolding)
│
├─ H4: Task 5 (Independent with hints)
│  └─ Code cell (student-designed)
│  └─ Key Concept Box 3 (Interpretation/causality)
│
├─ H4: Task 6 (Independent)
│  └─ Code cell (student-designed)
│
└─ H3: What You've Learned (Summary/conclusion)
```

**Task Scaffolding Progression:**

| Task | Level | Instructions | Code Provided | Difficulty |
|------|-------|--------------|---------------|------------|
| 1 | Guided | Detailed steps | Full example | Easiest |
| 2 | Semi-guided | Moderate guidance | Skeleton code | Easy |
| 3 | Semi-guided | Some guidance | Minimal skeleton | Moderate |
| 4 | More independent | High-level only | Hints only | Moderate-Hard |
| 5 | Independent | Research question | Student designs | Hard |
| 6 | Independent | Open-ended | Student designs | Hardest |

---

### Level 10: Empty Cell (Spacer)

```markdown
[Empty markdown cell]
```

**Guidelines:**
- Add empty markdown cell at very end
- Provides visual breathing room
- Separates content from notebook footer

---

## Complete Chapter Outline Template

**Quick reference for full chapter structure:**

```
CELL 0: Chapter Header (H1)
  ├─ Title, author, visual summary, Colab badge

CELL 1: Learning Objectives (H2)
  ├─ 5-8 measurable objectives
  └─ Horizontal rule

CELL 2: Chapter Overview (H2)
  ├─ Introduction paragraphs
  ├─ What you'll learn
  ├─ Dataset used
  └─ Chapter outline (including X.10 and X.11)

CELL 3: Setup (H2 + markdown)
CELL 4: Setup (code cell)

CELLS 5-N: Content Sections (H2, X.1 - X.9)
  ├─ Section explanations (markdown)
  ├─ Code cells (when applicable)
  ├─ Key Concept boxes (4-6 total)
  └─ Transition notes (2-4 total)

CELL N+1: Key Takeaways (H2)
  ├─ Thematic groups (4-8 groups)
  ├─ Next Steps
  ├─ You have now mastered
  └─ Closing sentence

CELL N+2: Empty cell (spacer)

CELL N+3: Practice Exercises (H2)
  ├─ 6-10 exercises
  └─ Horizontal rule

CELL N+4: Case Studies Section (H2, X.11)
  ├─ Introduction

CELL N+5: Case Study 1 (H3)
  ├─ Research question, background, data

CELL N+6: Key Concept Box 1 (blockquote)

CELL N+7: Load Data Section (H3)
CELL N+8: Data loading code
CELL N+9: Data dictionary display code

CELL N+10: Task 1 (H4, Guided)
CELL N+11: Task 1 code cell

CELL N+12: Task 2 (H4, Semi-guided)
CELL N+13: Task 2 code cell

CELL N+14: Key Concept Box 2 (blockquote)

CELL N+15: Task 3 (H4, Semi-guided)
CELL N+16: Task 3 code cell

CELL N+17: Task 4 (H4, More independent)
CELL N+18: Task 4 code cell

CELL N+19: Task 5 (H4, Independent)
CELL N+20: Task 5 code cell

CELL N+21: Key Concept Box 3 (blockquote)

CELL N+22: Task 6 (H4, Independent)
CELL N+23: Task 6 code cell

CELL N+24: Learning Summary (H3)

CELL N+25: Empty cell (spacer)
```

**Typical chapter cell counts:**
- Without Case Studies: ~30-35 cells
- With Case Studies: ~50-55 cells

---

## Formatting Conventions

### Markdown Headers

- **H1 (`#`)**: Chapter title only
- **H2 (`##`)**: Major sections (Learning Objectives, Setup, X.1-X.11, Key Takeaways, Practice Exercises)
- **H3 (`###`)**: Case study subsections (Case Study 1, Load Data, Learning Summary)
- **H4 (`####`)**: Individual tasks within case studies

### Text Formatting

- **Bold**: Section labels ("What you'll learn:", "Objective:", "Instructions:"), important terms
- *Italics*: Emphasis, variable names in prose
- `Code`: Variable names, function names, short code snippets
- LaTeX: Mathematical formulas using `$$` for display, `$` for inline

### Code Cells

- **Comments**: Use `#` for all comments
- **Section headers**: Use `# ===` or `print("=" * 70)` for output sections
- **Docstrings**: Not typically needed in notebook code cells
- **Output**: Print informative messages with context

### Lists

- Bullet points: Use `-` for consistency
- Numbered lists: Use when order matters (e.g., instructions)
- Nested lists: Indent 2 spaces per level

### Horizontal Rules

- Use `---` to separate major sections
- Place after: Learning Objectives, Key Takeaways, Practice Exercises, Case Studies conclusion

### Blockquotes

- Key Concept boxes: `> **Key Concept**: [text]`
- Transition notes: `**Transition:** [text]` (bold, not blockquote)

---

## Adapting Template to Other Chapters

### Chapter-Specific Adjustments

**For different chapter types:**

1. **Foundational chapters (CH01-CH04)**:
   - Focus on basic concepts
   - Simpler case study tasks
   - More guided exercises

2. **Bivariate regression (CH05-CH09)**:
   - Emphasize interpretation
   - Case studies with economic applications
   - Progressive complexity in tasks

3. **Multiple regression (CH10-CH17)**:
   - Advanced case study tasks
   - More independent work
   - Complex interpretation exercises

### Case Study Selection

**Criteria for selecting case studies:**

1. **Relevance**: Uses methods from the chapter
2. **Accessibility**: Dataset publicly available
3. **Interest**: Addresses interesting economic question
4. **Appropriateness**: Complexity matches chapter level
5. **Diversity**: Varies across chapters (labor, growth, policy, etc.)

**Suggested case study topics by chapter:**

- **CH02-04**: Wage distributions, survey data, statistical testing
- **CH05-07**: Education returns, labor economics, health economics
- **CH08-09**: Case studies in bivariate regression
- **CH10-13**: Growth regressions, policy evaluation, multiple predictors
- **CH14-17**: Panel data, advanced methods, causal inference

### Task Design Guidelines

**Number of tasks**: 6 tasks (standard)

**Scaffolding levels:**
- Tasks 1-2: Guided/semi-guided (detailed instructions)
- Tasks 3-4: Semi-guided/more independent (moderate instructions)
- Tasks 5-6: Independent (minimal instructions)

**Task types to include:**
1. Data exploration (always Task 1)
2. Descriptive statistics (usually Task 2)
3. Visualization (usually Task 3)
4. Time series or grouping (usually Task 4)
5. Main analysis method from chapter (usually Task 5)
6. Comparative or advanced application (usually Task 6)

---

## Quality Checklist

Before finalizing a chapter, verify:

### Structure
- [ ] Chapter header with all metadata
- [ ] Learning Objectives (5-8 items)
- [ ] Chapter Overview with complete outline
- [ ] Setup section with code cell
- [ ] Content sections numbered correctly (X.1 - X.9)
- [ ] Key Takeaways with thematic groups
- [ ] Practice Exercises (6-10 exercises)
- [ ] Case Studies section (X.11) with hierarchical structure
- [ ] Empty cell at end

### Pedagogical Elements
- [ ] 4-6 Key Concept boxes throughout chapter
- [ ] 2-4 Transition notes between major sections
- [ ] Progressive scaffolding in case study tasks
- [ ] Clear connection between chapter content and case study

### Case Studies Specific
- [ ] Research introduction (H3) with research question
- [ ] Key Concept box after research intro
- [ ] Data loading section (H3) with code
- [ ] 6 tasks with proper hierarchy (H4)
- [ ] Task 1-2: Guided/semi-guided
- [ ] Task 3-4: Semi-guided/more independent
- [ ] Task 5-6: Independent
- [ ] Key Concept boxes after Tasks 2 and 5
- [ ] Learning summary (H3) at end

### Formatting
- [ ] Consistent header hierarchy (H1→H2→H3→H4)
- [ ] Horizontal rules in appropriate locations
- [ ] Code cells properly formatted with comments
- [ ] All URLs functional
- [ ] LaTeX formulas render correctly
- [ ] No broken links

### Content Quality
- [ ] All code cells execute without errors
- [ ] Data loads successfully from URLs
- [ ] Instructions are clear and actionable
- [ ] Exercises test chapter concepts
- [ ] Case study matches chapter difficulty level

---

## File Locations

**When creating/updating chapters:**

- **Notebooks**: `notebooks_colab/chXX_[Chapter_Name].ipynb`
- **Notes**: `notes/sXX [Chapter Title].md`
- **Images**: `images/chXX_visual_summary.jpg`
- **Documentation**: `notebooks_colab/README.md` (update chapter status)
- **Logs**: `log/YYYYMMDD_HHMM_chXX_completion.md`

---

## Version History

- **Version 1.0** (January 30, 2026): Original template from CH01-CH06 enhancements
- **Version 2.0** (January 31, 2026): Updated with hierarchical Case Studies structure

---

## Next Steps

**To apply this template to other chapters:**

1. Read existing chapter notebook
2. Read corresponding notes file (`notes/sXX [Chapter Title].md`)
3. Identify appropriate case study for the chapter
4. Design 6 progressive tasks using chapter methods
5. Create implementation script (or manual editing)
6. Verify all components present
7. Test all code cells execute
8. Update README.md
9. Create log file
10. Generate PDF

**Chapters remaining**: 11 chapters (CH07-CH17)

**Estimated effort**: 35-45 minutes per chapter

---

**Template Author**: Claude (Sonnet 4.5)
**Reference Implementation**: Chapter 1 (Analysis of Economics Data)
**Last Updated**: January 31, 2026
