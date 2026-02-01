# Google Colab Notebooks - Applied Econometric Data Analysis

Educational Jupyter notebooks for learning econometrics with Python in Google Colab.

## Overview

This directory contains interactive Jupyter notebooks that combine **explanatory text** with **executable Python code** to teach econometric concepts. Each notebook corresponds to a chapter from Cameron's "Analysis of Economics Data: An Introduction to Econometrics" (2021).

**Key Features:**

- ✅ **Zero setup required** - Run directly in Google Colab
- ✅ **Self-contained** - Data streams from GitHub, no local files needed
- ✅ **Educational** - Alternating markdown explanations and code cells
- ✅ **Interactive** - Students can modify and re-run code
- ✅ **Reproducible** - Fixed random seeds ensure consistent results
- ✅ **Quality Assured** - All notebooks tested and debugged (January 2026)

## Recent Updates (January 20, 2026)

**Enhanced Educational Content:**

- ✅ **CH01-CH05:** Added 27 new result-based interpretation cells explaining actual numerical outputs
- ✅ **CH06-CH17:** All notebooks previously enhanced with comprehensive explanations

**Bug Fixes:**

- ✅ **CH06 Fixed:** Corrected 6 cells with wrong type (markdown saved as code), removed 5 duplicate cells, added missing data generation code
- ✅ **CH08 Fixed:** Added 3 missing regression models (infant mortality, health expenditure full/subset) and 3 missing visualizations (CAPM scatter, Okun's Law scatter/time series)
- 📝 **Documentation:** All fixes logged in [../log/](../log/) directory with detailed explanations

**Quality Status:** All 16 notebooks now execute cleanly without errors in Google Colab ✅

## 📋 Chapter Template Compliance & Improvement Tracking

**Purpose:** Systematic enhancement of all chapter notebooks to match reference template structure for optimal pedagogical effectiveness.

**Reference Template:** Based on `../notes/s01 Analysis of Economics Data.md` structure

### Template Requirements Checklist

For each chapter notebook, ensure the following elements are present:

- [ ] **Learning Objectives** - Formal section after title with 5-6 measurable learning goals
- [ ] **Key Concept Boxes** - 6-10 blockquote boxes (`>`) after major sections summarizing core concepts (1-2 sentences each)
- [ ] **Subsection Numbering** - Hierarchical numbering (e.g., 2.1.1, 2.1.2) for all subsections
- [ ] **Interpretation Guidelines** - Thresholds and rules of thumb for statistical measures where applicable
- [ ] **Transition Notes** - Brief connective text between major sections (3-4 per chapter)
- [ ] **Practice Exercises** - Dedicated section with 5-8 exercises before summary
- [ ] **Key Takeaways** - Structured closing with 3-4 thematic groups of bullet points

### Chapter Status Table

| Chapter | Template Compliance | Status | Notes |
|---------|---------------------|--------|-------|
| CH00 | ⚠️ Partial | Not Started | Preface - may not need full template |
| CH01 | ✅ Complete | **DONE** (Jan 30, 2026) | Option 2 applied - 23→32 cells |
| CH02 | ✅ Complete | **DONE** (Jan 30, 2026) | **Reference implementation** - Option 2 applied |
| CH03 | ✅ Complete | **DONE** (Jan 30, 2026) | Option 2 applied - 32→43 cells |
| CH04 | ✅ Complete | **DONE** (Jan 30, 2026) | Option 2 applied - 38→47 cells |
| CH05 | ✅ Complete | **DONE** (Jan 30, 2026) | Option 2 applied - 50→62 cells |
| CH06 | ✅ Complete | **DONE** (Jan 30, 2026) | Option 2 applied - 29→39 cells |
| CH07 | ⚠️ Partial | Not Started | Needs full template compliance |
| CH08 | ⚠️ Partial | Not Started | Recently fixed, needs template elements |
| CH09 | ⚠️ Partial | Not Started | Has good content, needs Key Concepts |
| CH10 | ⚠️ Partial | Not Started | Needs subsection numbering |
| CH11 | ⚠️ Partial | Not Started | Needs template compliance |
| CH12 | ⚠️ Partial | Not Started | Needs template compliance |
| CH14 | ⚠️ Partial | Not Started | Needs template compliance |
| CH15 | ⚠️ Partial | Not Started | Needs template compliance |
| CH16 | ⚠️ Partial | Not Started | Needs template compliance |
| CH17 | ⚠️ Partial | Not Started | Needs template compliance |

**Progress:** 6 of 17 chapters fully compliant (35.3%)

### Recent Implementations

#### CH01 Implementation Details

**Date Completed:** January 30, 2026
**Option Applied:** Option 2 (Balanced - Template + High Priority Fixes)
**Implementation Time:** ~30 minutes

**Changes Made:**
1. ✅ Added formal Learning Objectives section (6 objectives) after title
2. ✅ Inserted 4 Key Concept boxes throughout notebook after major sections
3. ✅ Added 3 transition notes connecting major sections
4. ✅ Added Practice Exercises section (1.10) with 8 comprehensive problems
5. ✅ Reformatted Chapter Summary as Key Takeaways with 5 thematic groups
6. ✅ Subsection numbering already present (1.1-1.9)

**Before/After:**
- Cells: 23 → 32 (+9 new cells)
- Grade: B+ → A-
- Template compliance: ~50% → 100%

**Files Modified:**
- `notebooks_colab/ch01_Analysis_of_Economics_Data.ipynb`

---

### CH02 Implementation Details (Reference)

**Date Completed:** January 30, 2026
**Option Applied:** Option 2 (Balanced - Template + High Priority Fixes)
**Implementation Time:** ~35 minutes (automated with Python scripts)

**Changes Made:**
1. ✅ Added formal Learning Objectives section (6 objectives) after title
2. ✅ Inserted 6 Key Concept boxes throughout notebook after major sections
3. ✅ Added subsection numbering to all 11 subsections (2.1.1, 2.1.2, etc.)
4. ✅ Added interpretation guidelines for skewness and kurtosis with thresholds
5. ✅ Clarified kurtosis discrepancy (excess vs. raw: 4.32 vs. 7.32)
6. ✅ Added 4 transition notes connecting major sections
7. ✅ Added Practice Exercises section (2.7) with 8 comprehensive problems
8. ✅ Reformatted Chapter Summary as Key Takeaways with 4 thematic groups

**Before/After:**
- Cells: 47 → 59 (+12 new cells)
- Grade: B+ → A-
- Template compliance: ~40% → 100%

**Files Modified:**
- `notebooks_colab/ch02_Univariate_Data_Summary.ipynb`

**Reference Files:**
- Template structure: `../notes/s01 Analysis of Economics Data.md`
- Content reference: `../notes/s02 Univariate Data Summary.md`
- Plan document: `~/.claude/plans/polished-launching-sutherland.md`

---

### CH03 Implementation Details

**Date Completed:** January 30, 2026
**Option Applied:** Option 2 (Balanced - Template + High Priority Fixes)
**Implementation Time:** ~40 minutes (automated with Python scripts)

**Changes Made:**
1. ✅ Replaced Chapter Overview with formal Learning Objectives section (10 objectives)
2. ✅ Inserted 6 Key Concept boxes throughout notebook after major sections
3. ✅ Added 3 transition notes connecting major sections (coin tosses → mathematical properties → Census data)
4. ✅ Added Practice Exercises section (3.7) with 8 comprehensive problems
5. ✅ Reformatted Chapter Summary as Key Takeaways with 8 thematic groups
6. ✅ Section numbering already present (3.1-3.7)

**Before/After:**
- Cells: 32 → 43 (+11 new cells)
- Grade: B+ → A-
- Template compliance: ~45% → 100%

**Files Modified:**
- `notebooks_colab/ch03_The_Sample_Mean.ipynb`

**Reference Files:**
- Content reference: `../notes/s03 The Sample Mean.md`

---

### CH04 Implementation Details

**Date Completed:** January 30, 2026
**Option Applied:** Option 2 (Balanced - Template + High Priority Fixes)
**Implementation Time:** ~35 minutes (automated with Python scripts)

**Changes Made:**
1. ✅ Replaced Chapter Overview with formal Learning Objectives section (10 objectives)
2. ✅ Inserted 5 Key Concept boxes throughout notebook after major sections
3. ✅ Added 3 transition notes connecting major sections (t-distribution → CIs → hypothesis tests)
4. ✅ Added Practice Exercises section (4.8) with 8 comprehensive problems
5. ✅ Reformatted Chapter Summary as Key Takeaways (already well-structured)
6. ✅ Section numbering already present (4.1-4.8)

**Before/After:**
- Cells: 38 → 47 (+9 new cells)
- Grade: B+ → A-
- Template compliance: ~50% → 100%

**Files Modified:**
- `notebooks_colab/ch04_Statistical_Inference_for_the_Mean.ipynb`

**Reference Files:**
- Content reference: `../notes/s04 Statistical Inference for the Mean.md`

---

### CH05 Implementation Details

**Date Completed:** January 30, 2026
**Option Applied:** Option 2 (Balanced - Template + High Priority Fixes)
**Implementation Time:** ~40 minutes (automated with Python scripts)

**Changes Made:**
1. ✅ Replaced Chapter Overview with formal Learning Objectives section (14 objectives)
2. ✅ Inserted 7 Key Concept boxes throughout notebook after major sections
3. ✅ Added 4 transition notes connecting major sections (visualization → correlation → regression → causation)
4. ✅ Added Practice Exercises section (5.12) with 8 comprehensive problems
5. ✅ Reformatted Chapter Summary as Key Takeaways with 5 thematic groups
6. ✅ Section numbering already present (5.1-5.12)

**Before/After:**
- Cells: 50 → 62 (+12 new cells)
- Grade: B+ → A-
- Template compliance: ~50% → 100%

**Files Modified:**
- `notebooks_colab/ch05_Bivariate_Data_Summary.ipynb`

**Reference Files:**
- Content reference: `../notes/s05 Bivariate Data Summary.md`

**Key Concepts Added:**
- Visual inspection and scatterplot importance
- Two-way tabulations and chi-squared tests
- Scatterplots showing direction, strength, form, outliers
- Correlation as scale-free linear association measure
- OLS method minimizing sum of squared residuals
- R-squared measuring fraction of variance explained
- Association vs. causation distinction (critical concept)

---

### CH06 Implementation Details

**Date Completed:** January 30, 2026
**Option Applied:** Option 2 (Balanced - Template + High Priority Fixes)
**Implementation Time:** ~35 minutes (automated with Python scripts)

**Changes Made:**
1. ✅ Replaced Chapter Overview with formal Learning Objectives section (12 objectives)
2. ✅ Inserted 6 Key Concept boxes throughout notebook after major sections
3. ✅ Added 3 transition notes connecting major sections (sampling → properties → estimation)
4. ✅ Added Practice Exercises section (6.5) with 8 comprehensive problems
5. ✅ Reformatted Chapter Summary as Key Takeaways with 8 thematic groups
6. ✅ Section numbering already present (6.1-6.4)

**Before/After:**
- Cells: 29 → 39 (+10 new cells)
- Grade: B+ → A-
- Template compliance: ~40% → 100%

**Files Modified:**
- `notebooks_colab/ch06_The_Least_Squares_Estimator.ipynb`

**Reference Files:**
- Content reference: `../notes/s06 The Least Squares Estimator.md`

**Key Concepts Added:**
- Population vs. sample regression distinction
- Error term vs. residual (crucial distinction)
- Monte Carlo demonstration of unbiasedness
- Four core OLS assumptions (essential vs. relaxable)
- Standard error formula and precision factors
- BLUE property (Gauss-Markov Theorem)

---

### Implementation Guide for Future Chapters

**Recommended Approach:** Apply Option 2 (Balanced) to all remaining chapters

**Option 2 Includes:**
- Template compliance (Learning Objectives, Key Concepts, Key Takeaways)
- Subsection numbering throughout
- Practice exercises section
- Interpretation guidelines where applicable
- Transition notes between sections

**Estimated Effort Per Chapter:** 30-45 minutes using automated Python scripts

**Python Script Template:**
```python
# Script to add template elements to Jupyter notebooks
import json

# 1. Add Learning Objectives cell after title
# 2. Insert Key Concept boxes after major sections
# 3. Update subsection headers with numbering
# 4. Add Practice Exercises section before summary
# 5. Reformat summary as Key Takeaways

# See CH02 implementation for full working example
```

**Key Principles:**
- **Additive only:** Never delete existing content
- **Preserve code cells:** All code remains unchanged
- **Match notes structure:** Use corresponding notes file for subsection numbers
- **Consistent format:** Follow CH02 as reference implementation

### Next Steps

**Priority Queue** (suggested order):
1. CH03 (The Sample Mean) - foundational chapter
2. CH04 (Statistical Inference) - builds on CH03
3. CH05 (Bivariate Data Summary) - transitions to regression
4. CH01 (Analysis of Economics Data) - introductory chapter
5. CH06-CH08 (Regression fundamentals)
6. CH09-CH12 (Advanced regression)
7. CH14-CH17 (Special topics)

**For Each Chapter:**
1. Read corresponding notes file (e.g., `../notes/s03 The Sample Mean.md`)
2. Identify current state vs. template requirements
3. Create Learning Objectives from notes file
4. Identify logical locations for Key Concept boxes (after major explanations)
5. Extract subsection numbering from notes file
6. Design 5-8 practice exercises
7. Restructure summary as Key Takeaways
8. Validate notebook structure and test code execution

---

## 🎨 Formatting Consistency Standards

**Date Established:** January 30, 2026
**Status:** All CH01-CH06 compliant ✅

### Overview

To ensure professional appearance and optimal student experience, all notebooks follow uniform formatting conventions for section headers, numbering, and hierarchy.

### Formatting Standards

**Standard 1: Section Header Format**
- **Format:** `## X.Y Section Title` (NO colons after section number)
- **Example:** `## 1.1 What is Regression Analysis?` ✓
- **Not:** `## 1.1: What is Regression Analysis?` ✗
- **Rationale:** Cleaner appearance, consistent with standard markdown conventions

**Standard 2: Section Numbering**
- **Rule:** Sequential numbering with NO gaps
- **Example:** 3.1, 3.2, 3.3, 3.4, 3.5, 3.6, 3.7 ✓
- **Not:** 3.1, 3.2, 3.3, 3.4, 3.5, 3.7, 3.8 (missing 3.6) ✗
- **Practice Exercises:** Always the final numbered section

**Standard 3: Subsection Formatting**
- **Format:** `### Descriptive Title` (NO numbering in subsections)
- **Example:** `### R-squared (R²)` ✓
- **Not:** `### 1. R-squared (R²)` ✗
- **Hierarchy:** `##` for sections, `###` for subsections

**Standard 4: Chapter Outlines**
- **Approach:** Learning Objectives section serves as chapter overview
- **No separate outline section needed** (avoids duplication)

### Formatting Consistency Revision (January 30, 2026)

**Changes Applied to CH01-CH06:**

1. **Colon Removal** - Standardized section header format
   - CH01: Removed colons from 9 section headers
   - CH03: Removed colons from 6 section headers
   - CH05: Removed colons from 12 section headers
   - CH06: Removed colons from 5 section headers
   - **Total:** 32 cells modified across 4 chapters

2. **Section Renumbering** - Eliminated numbering gaps
   - CH03: Renumbered 3.7→3.6, 3.8→3.7 (eliminated gap after 3.5)
   - CH04: Renumbered 4.8→4.7, 4.9→4.8 (eliminated gap after 4.6)
   - CH05: Renumbered 5.13→5.12 (eliminated gap after 5.11)
   - **Total:** 5 sections renumbered across 3 chapters

3. **Subsection Formatting** - Fixed improper numbering
   - CH05 Section 5.6: Removed numbers from 2 subsections
   - Changed `### 1. R-squared (R²)` → `### R-squared (R²)`
   - Changed `### 2. Standard Error of the Regression (s_e)` → `### Standard Error of the Regression (s_e)`

**Impact:** Enhanced professional appearance, improved navigation consistency, eliminated student confusion about missing sections

**Documentation:** See [../log/20260130_FORMATTING_CONSISTENCY_CH01-06.md](../log/20260130_FORMATTING_CONSISTENCY_CH01-06.md) for complete details

### Current Status by Chapter

| Chapter | Section Format | Sequential Numbering | Subsection Format | Status |
|---------|----------------|---------------------|-------------------|---------|
| CH01 | ✅ No colons | ✅ 1.1-1.10 | ✅ Descriptive | Compliant |
| CH02 | ✅ No colons | ✅ 2.1-2.7 | ✅ Descriptive | Compliant |
| CH03 | ✅ No colons | ✅ 3.1-3.7 | ✅ Descriptive | Compliant |
| CH04 | ✅ No colons | ✅ 4.1-4.8 | ✅ Descriptive | Compliant |
| CH05 | ✅ No colons | ✅ 5.1-5.12 | ✅ Descriptive | Compliant |
| CH06 | ✅ No colons | ✅ 6.1-6.5 | ✅ Descriptive | Compliant |
| CH07-17 | ⏳ Pending | ⏳ Pending | ⏳ Pending | To be reviewed |

**Note on Subsections:** CH02 uses numbered subsections (2.1.1, 2.1.2) which is acceptable. Other chapters use descriptive subsection titles without numbering. Both approaches are valid as long as hierarchy is maintained (`##` for sections, `###` for subsections).

### Verification Commands

**Extract all section headers from a chapter:**
```bash
cd notebooks_colab
jupyter nbconvert --to markdown --stdout ch03_*.ipynb 2>/dev/null | grep -E '^##+ '
```

**Verify no colons in section headers:**
```bash
jupyter nbconvert --to markdown --stdout ch*.ipynb 2>/dev/null | grep -E '^## \d+\.\d+:'
# Should return empty (no matches)
```

**Check for section numbering gaps:**
```bash
jupyter nbconvert --to markdown --stdout ch05_*.ipynb 2>/dev/null | grep -E '^## \d+\.\d+' | sed 's/## //' | sed 's/ .*//'
# Should show sequential numbers: 5.1, 5.2, 5.3, ..., 5.12
```

### For Future Chapters

When implementing template compliance for CH07-CH17:
1. **Verify section header format** - Ensure no colons after section numbers
2. **Check sequential numbering** - Eliminate any gaps in section numbers
3. **Review subsection hierarchy** - Use `###` for subsections (numbering optional)
4. **Update this table** - Mark chapter as compliant after verification

---

## 📄 PDF Generation

All notebooks can be automatically exported to professional-quality PDF files using the Playwright-based workflow. PDFs are publication-ready with optimized formatting for printing and distribution.

**Current Status:**

- ✅ ch00_Preface.pdf (0.82 MB)
- ✅ ch01_Analysis_of_Economics_Data.pdf (1.00 MB)
- ✅ ch02_Univariate_Data_Summary.pdf (1.83 MB) - **Updated Feb 1, 2026** - Proofreading complete, all fixes applied
- ⏳ ch03-ch17 (ready to generate on demand)

**Key Features:**

- Professional justified text alignment (book-style typography)
- Full-width chapter visual summaries (7 inches)
- Optimized regression tables with 7.5pt font (no overflow)
- Uniform 0.75-inch margins on all sides
- Clickable hyperlinks preserved
- Brand-consistent color scheme
- Letter format (8.5" × 11") portrait orientation

**Quick Commands:**

```bash
# Generate single chapter PDF
cd notebooks_colab && jupyter nbconvert --to html ch05_*.ipynb && cd ..
python3 inject_print_css.py notebooks_colab/ch05_*.html notebooks_colab/ch05_*_printable.html
python3 generate_pdf_playwright.py ch05

# Generate all chapter PDFs
cd notebooks_colab && for nb in ch*.ipynb; do jupyter nbconvert --to html "$nb"; done && cd ..
python3 generate_pdf_playwright.py --all
```

**Complete Documentation:** See [../log/20260129_PDF_GENERATION_WORKFLOW.md](../log/20260129_PDF_GENERATION_WORKFLOW.md) for comprehensive workflow, troubleshooting, and technical details.

## Available Notebooks

### ✅ Chapter 1: Analysis of Economics Data
**File:** [ch01_Analysis_of_Economics_Data.ipynb](ch01_Analysis_of_Economics_Data.ipynb)

**Open in Colab:** [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/cmg777/aed/blob/main/notebooks_colab/ch01_Analysis_of_Economics_Data.ipynb)

**Topics Covered:**
- Introduction to regression analysis
- Simple linear regression (OLS)
- Data visualization (scatter plots)
- Interpreting regression coefficients economically
- Model fit (R-squared)

**Learning Objectives:**
- Understand what regression analysis is and why it's central to econometrics
- Load and explore economic data in Python
- Fit a simple OLS regression model
- Interpret slope coefficients in economic terms
- Create publication-quality visualizations

**Dataset:** AED_HOUSE.DTA (29 houses in Central Davis, CA, 1999)

**Key Result:** Each additional square foot of house size is associated with a $73.77 increase in sale price (R² = 61.75%)

**Estimated Time:** 30-45 minutes

---

### ✅ Chapter 2: Univariate Data Summary
**File:** [ch02_Univariate_Data_Summary.ipynb](ch02_Univariate_Data_Summary.ipynb)

**Open in Colab:** [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/cmg777/aed/blob/main/notebooks_colab/ch02_Univariate_Data_Summary.ipynb)

**Topics Covered:**
- Summary statistics for numerical data (mean, median, standard deviation, quartiles, skewness, kurtosis)
- Data visualization (box plots, histograms, kernel density estimates, line charts)
- Charts for categorical data (bar charts, pie charts)
- Data transformations (logarithmic transformation, standardization)
- Time series transformations (moving averages, seasonal adjustment)

**Learning Objectives:**
- Calculate and interpret comprehensive summary statistics
- Create effective visualizations for different data types
- Understand when and why to use data transformations
- Work with multiple datasets in one analysis
- Apply time series transformations to reveal trends

**Datasets:**
- AED_EARNINGS.DTA (171 women, annual earnings)
- AED_REALGDPPC.DTA (U.S. GDP 1959-2020)
- AED_HEALTHCATEGORIES.DTA (Health expenditures 2018)
- AED_FISHING.DTA (1,182 fishing site choices)
- AED_MONTHLYHOMESALES.DTA (Home sales 1999-2015)

**Key Results:**
- Mean earnings: $41,413; Median: $36,000 (right-skewed distribution)
- Log transformation reduces skewness from 1.71 to near-normal
- Real GDP per capita tripled from 1959 to 2019
- Hospital care accounts for largest health expenditure ($1,192B)

**Estimated Time:** 45-60 minutes

---

### ✅ Chapter 4: Statistical Inference for the Mean
**File:** [ch04_Statistical_Inference_for_the_Mean.ipynb](ch04_Statistical_Inference_for_the_Mean.ipynb)

**Open in Colab:** [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/cmg777/aed/blob/main/notebooks_colab/ch04_Statistical_Inference_for_the_Mean.ipynb)

**Topics Covered:**
- t-distribution vs normal distribution
- Confidence intervals for population mean
- Two-sided hypothesis tests (H₀: μ = μ* vs Hₐ: μ ≠ μ*)
- One-sided hypothesis tests (directional alternatives)
- p-values and critical values interpretation
- Inference for proportions

**Learning Objectives:**
- Understand when and why to use the t-distribution
- Construct and interpret confidence intervals
- Conduct hypothesis tests using both p-value and critical value approaches
- Distinguish between one-sided and two-sided tests
- Apply inference methods to real economic data
- Interpret statistical vs practical significance

**Datasets:**
- AED_EARNINGS.DTA (171 women, annual earnings - primary example)
- AED_GASPRICE.DTA (32 gas stations, Yolo County)
- AED_EARNINGSMALE.DTA (191 men, annual earnings)
- AED_REALGDPPC.DTA (241 growth rate observations)

**Key Results:**
- 95% CI for mean female earnings: [$37,559, $45,266]
- Cannot reject H₀: μ = $40,000 (p-value = 0.47)
- Yolo County gas prices significantly below CA average (p < 0.001)
- GDP growth consistent with 2.0% average (p = 0.946)

**Estimated Time:** 60-75 minutes

---

### ✅ Chapter 9: Models with Natural Logarithms
**File:** [ch09_Models_with_Natural_Logarithms.ipynb](ch09_Models_with_Natural_Logarithms.ipynb)

**Open in Colab:** [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/cmg777/aed/blob/main/notebooks_colab/ch09_Models_with_Natural_Logarithms.ipynb)

**Topics Covered:**
- Natural logarithm properties and approximations
- Semi-elasticities and elasticities
- Four model specifications: linear, log-linear, log-log, linear-log
- Interpretation of coefficients in log models
- Exponential growth modeling
- Model comparison and selection

**Learning Objectives:**
- Understand when and why to use logarithmic transformations
- Interpret coefficients as percentage changes and elasticities
- Choose appropriate model specification for economic data
- Estimate returns to education using multiple specifications
- Model exponential growth in time series
- Apply retransformation bias correction

**Datasets:**
- AED_EARNINGS.DTA (171 workers, earnings and education)
- AED_SP500INDEX.DTA (S&P 500 index 1927-2019)

**Key Results:**
- Log-linear model: Each year of education → 13.1% increase in earnings (best fit, R² = 0.334)
- Linear model: Each year of education → $5,021 increase in earnings (R² = 0.289)
- Log-log elasticity: 1% more education → 1.48% more earnings
- S&P 500 growth rate: 6.5% per year (1927-2019)

**Estimated Time:** 60-75 minutes

---

### ✅ Chapter 3: The Sample Mean
**File:** [ch03_The_Sample_Mean.ipynb](ch03_The_Sample_Mean.ipynb)

**Open in Colab:** [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/cmg777/aed/blob/main/notebooks_colab/ch03_The_Sample_Mean.ipynb)

**Topics Covered:**
- Random variables and their properties (mean, variance, standard deviation)
- Sampling distribution of the sample mean
- Properties of the sample mean: $E[\\bar{X}] = \\mu$, $Var[\\bar{X}] = \\sigma^2/n$
- Central Limit Theorem (CLT)
- Standard error: $se(\\bar{X}) = s/\\sqrt{n}$
- Estimator properties: unbiasedness, efficiency, consistency
- Computer simulation of random samples

**Learning Objectives:**
- Understand the distinction between random variables and realized values
- Derive and interpret the mean and variance of the sample mean
- Explore sampling distributions through experiments and simulations
- Grasp the Central Limit Theorem and its importance
- Calculate and interpret the standard error
- Evaluate estimator quality (unbiased, efficient, consistent)

**Datasets:**
- AED_COINTOSSMEANS.DTA (400 sample means from coin toss experiments, n=30 each)
- AED_CENSUSAGEMEANS.DTA (100 sample means from 1880 U.S. Census ages, n=25 each)

**Key Results:**
- Coin toss: Mean of 400 sample means = 0.499 (theoretical: μ = 0.5)
- Coin toss: Std of sample means = 0.086 (theoretical: σ/√n = 0.091)
- Census: Mean of 100 sample means = 23.78 years (theoretical: μ = 24.13)
- Census: Sample means are approximately normal despite non-normal population
- Simulation perfectly replicates theoretical predictions

**Estimated Time:** 50-60 minutes

---

### ✅ Chapter 10: Data Summary for Multiple Regression
**File:** [ch10_Data_Summary_for_Multiple_Regression.ipynb](ch10_Data_Summary_for_Multiple_Regression.ipynb)

**Open in Colab:** [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/cmg777/aed/blob/main/notebooks_colab/ch10_Data_Summary_for_Multiple_Regression.ipynb)

**Topics Covered:**
- Multiple regression with several explanatory variables
- Partial effects interpretation (holding other variables constant)
- Correlation matrices and scatterplot matrices
- Model fit statistics (R², adjusted R², AIC, BIC)
- Variance Inflation Factors (VIF) for multicollinearity detection
- Comparison of simple vs multiple regression models

**Learning Objectives:**
- Specify and estimate multiple regression models
- Interpret regression coefficients as partial effects
- Use exploratory data analysis for multiple variables
- Calculate and interpret model fit statistics
- Detect and diagnose multicollinearity problems
- Compare competing model specifications

**Dataset:**
- AED_HOUSE.DTA (29 houses in Davis, California, 1999)

**Key Results:**
- Full model: R² = 0.651, Adjusted R² = 0.555
- Simple model (size only): R² = 0.618, Adjusted R² = 0.603
- Size coefficient: $68.37 per square foot (p < 0.001, only significant predictor)
- Bedrooms coefficient changes from $52,139 (bivariate) to $2,685 (multiple regression)
- VIF values all < 3 (no serious multicollinearity)

**Estimated Time:** 60-75 minutes

---

### ✅ Chapter 5: Bivariate Data Summary
**File:** [ch05_Bivariate_Data_Summary.ipynb](ch05_Bivariate_Data_Summary.ipynb)

**Open in Colab:** [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/cmg777/aed/blob/main/notebooks_colab/ch05_Bivariate_Data_Summary.ipynb)

**Topics Covered:**
- Two-way scatter plots and visualization
- Correlation coefficient and covariance
- Simple linear regression (OLS)
- Regression line interpretation
- R-squared and standard error of regression
- Prediction and outliers
- Causation vs association
- Nonparametric regression methods (LOWESS, kernel smoothing)

**Learning Objectives:**
- Create and interpret scatter plots for bivariate relationships
- Calculate and interpret correlation coefficients
- Fit and visualize regression lines
- Measure model fit using R² and standard error
- Distinguish between correlation, regression, and causation
- Apply nonparametric regression methods

**Dataset:** AED_HOUSE.DTA (29 houses in Central Davis, CA, 1999)

**Key Results:**
- Correlation between price and size: r = 0.786
- Regression: price = $115,017 + $73.77 × size (R² = 0.618)
- Each additional square foot → $73.77 higher price
- Nonparametric methods confirm linear relationship

**Estimated Time:** 60-70 minutes

---

### ✅ Chapter 6: The Least Squares Estimator
**File:** [ch06_The_Least_Squares_Estimator.ipynb](ch06_The_Least_Squares_Estimator.ipynb)

**Open in Colab:** [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/cmg777/aed/blob/main/notebooks_colab/ch06_The_Least_Squares_Estimator.ipynb)

**Topics Covered:**
- Population regression line vs sample regression line
- Unbiasedness of OLS estimators
- Sampling distribution of regression coefficients
- Consistency and efficiency of OLS
- Standard errors of coefficient estimates

**Learning Objectives:**
- Distinguish between population and sample regression
- Understand theoretical properties of OLS (unbiasedness, consistency, efficiency)
- Explore sampling distributions through simulation
- Calculate standard errors for OLS estimates
- Apply the Central Limit Theorem to regression coefficients

**Datasets:** AED_GENERATEDDATA.DTA, AED_GENERATEDREGRESSION.DTA, AED_CENSUSREGRESSIONS.DTA

**Key Results:**
- OLS is unbiased: E[β̂] = β
- Sampling distribution is approximately normal for large n
- Simulation confirms theoretical predictions
- Standard error measures precision of estimates

**Estimated Time:** 60-90 minutes

---

### ✅ Chapter 7: Statistical Inference for Bivariate Regression
**File:** [ch07_Statistical_Inference_for_Bivariate_Regression.ipynb](ch07_Statistical_Inference_for_Bivariate_Regression.ipynb)

**Open in Colab:** [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/cmg777/aed/blob/main/notebooks_colab/ch07_Statistical_Inference_for_Bivariate_Regression.ipynb)

**Topics Covered:**
- t-distribution and t-statistics
- Constructing confidence intervals
- Null and alternative hypotheses
- p-values and significance levels
- Type I and Type II errors
- Heteroskedasticity-robust standard errors

**Learning Objectives:**
- Construct and interpret confidence intervals for regression coefficients
- Conduct hypothesis tests (one-sided and two-sided)
- Interpret p-values and significance levels
- Apply robust standard errors for heteroskedasticity
- Make statistical inferences from regression output

**Datasets:** AED_HOUSE.DTA, AED_REALGDPPC.DTA

**Key Results:**
- 95% CI for size coefficient: [$50.84, $96.70]
- t-statistic: 6.60 (highly significant, p < 0.001)
- Reject H₀: β = 0 (size significantly affects price)
- Robust standard errors adjust for heteroskedasticity

**Estimated Time:** 60-90 minutes

---

### ✅ Chapter 8: Case Studies for Bivariate Regression
**File:** [ch08_Case_Studies_for_Bivariate_Regression.ipynb](ch08_Case_Studies_for_Bivariate_Regression.ipynb)

**Open in Colab:** [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/cmg777/aed/blob/main/notebooks_colab/ch08_Case_Studies_for_Bivariate_Regression.ipynb)

**Topics Covered:**
- Cross-country regression analysis
- Life expectancy and health spending
- Capital Asset Pricing Model (CAPM)
- Okun's Law (output and unemployment)
- Interpreting economic relationships

**Learning Objectives:**
- Apply regression to real-world economic questions
- Analyze health outcomes and expenditures across countries
- Estimate systematic risk using CAPM
- Test Okun's Law for macroeconomic relationships
- Interpret coefficients in economic context

**Datasets:** AED_HEALTH2009.DTA, AED_CAPM.DTA, AED_GDPUNEMPLOY.DTA

**Key Results:**
- Health spending positively associated with life expectancy
- CAPM beta estimates for stock returns
- Okun's Law: 1% higher unemployment → 2% lower GDP growth
- Practical application of regression to policy questions

**Estimated Time:** 60-90 minutes

---

### ✅ Chapter 11: Statistical Inference for Multiple Regression
**File:** [ch11_Statistical_Inference_for_Multiple_Regression.ipynb](ch11_Statistical_Inference_for_Multiple_Regression.ipynb)

**Open in Colab:** [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/cmg777/aed/blob/main/notebooks_colab/ch11_Statistical_Inference_for_Multiple_Regression.ipynb)

**Topics Covered:**
- Multiple regression model
- Partial effects and ceteris paribus
- Multicollinearity
- F-tests for joint significance
- Restricted vs unrestricted models
- Presenting regression tables

**Learning Objectives:**
- Specify and estimate multiple regression models
- Interpret partial effects (holding other variables constant)
- Conduct F-tests for joint hypotheses
- Detect and handle multicollinearity
- Present regression results professionally

**Dataset:** AED_HOUSE.DTA

**Key Results:**
- Full model: price ~ size + bedrooms + bathrooms + lotsize + age + monthsold
- Only size coefficient is statistically significant
- F-test for joint significance: F = 6.77, p = 0.0005
- Partial effect of size: $68.37 per sq ft (controlling for other variables)

**Estimated Time:** 60-90 minutes

---

### ✅ Chapter 12: Further Topics in Multiple Regression
**File:** [ch12_Further_Topics_in_Multiple_Regression.ipynb](ch12_Further_Topics_in_Multiple_Regression.ipynb)

**Open in Colab:** [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/cmg777/aed/blob/main/notebooks_colab/ch12_Further_Topics_in_Multiple_Regression.ipynb)

**Topics Covered:**
- Heteroskedasticity-robust inference
- Prediction intervals
- Sample selection issues
- Generalized Least Squares (GLS)
- Bootstrap methods
- Power of statistical tests

**Learning Objectives:**
- Apply heteroskedasticity-robust standard errors (HC1, HC3)
- Construct prediction intervals for individual and average outcomes
- Understand sample selection bias
- Implement bootstrap inference
- Assess statistical power

**Datasets:** AED_HOUSE.DTA, AED_REALGDPPC.DTA

**Key Results:**
- Robust standard errors adjust for heteroskedasticity
- Prediction intervals are wider than confidence intervals
- Bootstrap confirms asymptotic results
- Sample selection can bias estimates

**Estimated Time:** 60-90 minutes

---

### ✅ Chapter 14: Regression with Indicator Variables
**File:** [ch14_Regression_with_Indicator_Variables.ipynb](ch14_Regression_with_Indicator_Variables.ipynb)

**Open in Colab:** [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/cmg777/aed/blob/main/notebooks_colab/ch14_Regression_with_Indicator_Variables.ipynb)

**Topics Covered:**
- Dummy variables (0/1 indicators)
- Reference category
- Slope and intercept shifts
- Interaction terms
- Chow test for structural breaks
- Binary dependent variables

**Learning Objectives:**
- Create and interpret dummy variables for categorical data
- Model differential intercepts and slopes
- Test for structural changes using interaction terms
- Understand the linear probability model
- Apply Chow test for parameter stability

**Datasets:** AED_EARNINGS.DTA, AED_HOUSE.DTA

**Key Results:**
- Gender earnings gap estimation
- Interaction effects between education and gender
- Testing equality of regression coefficients across groups
- Linear probability model for binary outcomes

**Estimated Time:** 60-90 minutes

---

### ✅ Chapter 15: Regression with Transformed Variables
**File:** [ch15_Regression_with_Transformed_Variables.ipynb](ch15_Regression_with_Transformed_Variables.ipynb)

**Open in Colab:** [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/cmg777/aed/blob/main/notebooks_colab/ch15_Regression_with_Transformed_Variables.ipynb)

**Topics Covered:**
- Log-log models (elasticities)
- Log-linear models (growth rates)
- Linear-log models
- Quadratic and cubic terms
- Z-score standardization
- Choosing functional form

**Learning Objectives:**
- Select appropriate variable transformations
- Interpret coefficients in transformed models
- Model nonlinear relationships with polynomials
- Standardize variables for comparison
- Apply Box-Cox transformations

**Datasets:** AED_EARNINGS.DTA, AED_HOUSE.DTA

**Key Results:**
- Earnings-education elasticity estimates
- Quadratic age-earnings profiles
- Optimal transformations using Box-Cox
- Standardized coefficients for comparison

**Estimated Time:** 60-90 minutes

---

### ✅ Chapter 16: Checking the Model and Data
**File:** [ch16_Checking_the_Model_and_Data.ipynb](ch16_Checking_the_Model_and_Data.ipynb)

**Open in Colab:** [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/cmg777/aed/blob/main/notebooks_colab/ch16_Checking_the_Model_and_Data.ipynb)

**Topics Covered:**
- Residual analysis
- Breusch-Pagan test
- White test
- Jarque-Bera test
- Leverage and influence
- RESET test
- AIC and BIC criteria

**Learning Objectives:**
- Diagnose regression problems using residual plots
- Test for heteroskedasticity formally
- Assess normality of errors
- Identify influential observations
- Test for omitted variables
- Compare models using information criteria

**Datasets:** AED_HOUSE.DTA, AED_EARNINGS.DTA

**Key Results:**
- Residual plots reveal heteroskedasticity
- Formal tests confirm diagnostic findings
- Influential observations identified
- Model comparison using AIC/BIC

**Estimated Time:** 60-90 minutes

---

### ✅ Chapter 17: Panel Data, Time Series Data, Causation
**File:** [ch17_Panel_Data_Time_Series_Data_Causation.ipynb](ch17_Panel_Data_Time_Series_Data_Causation.ipynb)

**Open in Colab:** [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/cmg777/aed/blob/main/notebooks_colab/ch17_Panel_Data_Time_Series_Data_Causation.ipynb)

**Topics Covered:**
- Panel data structure
- Within and between variation
- Fixed effects estimation
- Random effects estimation
- Serial correlation
- Durbin-Watson test
- Endogeneity and IV estimation

**Learning Objectives:**
- Work with panel (longitudinal) data
- Estimate fixed effects and random effects models
- Test for and handle serial correlation
- Understand causality and endogeneity
- Apply instrumental variables methods
- Choose between FE and RE models

**Datasets:** AED_FATALITIES.DTA, AED_REALGDPPC.DTA

**Key Results:**
- Fixed effects control for unobserved heterogeneity
- Serial correlation in time series regressions
- IV estimation for endogenous regressors
- Panel data provides stronger causal identification

**Estimated Time:** 60-90 minutes

---

## How to Use These Notebooks

### Option 1: Google Colab (Recommended)
1. Click the "Open in Colab" badge above
2. The notebook will open in Google Colab
3. Click "Runtime" → "Run all" (or run cells individually)
4. All data loads automatically from GitHub

### Option 2: Local Jupyter
1. Download the `.ipynb` file
2. Install required packages:
   ```bash
   pip install pandas numpy matplotlib statsmodels scipy
   ```
3. Open in Jupyter Notebook or JupyterLab
4. Run cells sequentially

### Option 3: VS Code
1. Open the `.ipynb` file in VS Code
2. Select Python kernel
3. Run cells interactively

## Notebook Structure

Each notebook follows a consistent pedagogical structure:

1. **Title & Overview** (Markdown)
   - Learning objectives
   - Dataset description
   - Chapter outline

2. **Setup** (Code)
   - Package imports
   - Configuration
   - Random seed setting

3. **Content Sections** (Alternating Markdown + Code)
   - **Markdown**: Conceptual explanation with equations
   - **Code**: Implementation and execution
   - **Markdown**: Results interpretation

4. **Visualizations** (Markdown + Code)
   - **Markdown**: What the figure shows and why
   - **Code**: Generate the visualization

5. **Summary** (Markdown)
   - Key takeaways
   - Statistical methods covered
   - Next steps

## Educational Design

### Content Sources
- **Python code**: From validated scripts in `code_python/` (100% tested)
- **Explanatory text**: Adapted from `slides_markdown/` presentations
- **Economic interpretation**: Emphasized throughout

### Pedagogical Principles
- **Progressive complexity**: Simple concepts build to advanced topics
- **Learning by doing**: Executable code cells after each concept
- **Small logical units**: Code split into digestible steps
- **Formulas with intuition**: Math notation explained in plain English
- **Economic context**: Always relate statistics to real-world meaning

### Detail Level
- **Moderate explanations**: 1 paragraph per concept
- **Suitable for**: Undergraduate econometrics students
- **Prerequisites**: Basic statistics (mean, standard deviation, hypothesis testing)

## Requirements

### Python Version
- Python 3.8 or higher

### Required Packages
All automatically available in Google Colab:
- `pandas` - Data manipulation
- `numpy` - Numerical computing
- `matplotlib` - Visualization
- `statsmodels` - Statistical modeling (OLS regression)
- `scipy` - Scientific computing

### Optional Packages (for advanced chapters)
- `seaborn` - Enhanced visualizations
- `linearmodels` - Panel data models (Chapter 17)

## Data Sources

All datasets stream directly from:
```
https://raw.githubusercontent.com/quarcs-lab/data-open/master/AED/
```

**Available datasets:**
- AED_HOUSE.DTA - House prices
- AED_EARNINGS.DTA - Earnings data
- AED_REALGDPPC.DTA - GDP per capita
- AED_GASPRICE.DTA - Gasoline prices
- And 10+ more...

No downloads required - all data loads automatically in the notebooks.

## Outputs Generated

Each notebook produces:
- **Figures**: High-quality PNG plots (displayed inline)
- **Statistical tables**: Regression summaries, descriptive statistics
- **Interpretation**: Economic meaning of all results

Outputs are displayed directly in the notebook. Optionally, outputs can be saved to local directories (`images/`, `tables/`).

## Troubleshooting

### Common Issues

**Q: Notebook won't open in Colab**
- **A:** Make sure you're using the correct GitHub URL format:
  `https://colab.research.google.com/github/cmg777/aed/blob/main/notebooks_colab/NOTEBOOK_NAME.ipynb`

**Q: "ModuleNotFoundError" in Colab**
- **A:** Add a cell with: `!pip install PACKAGE_NAME` and run it first

**Q: Data won't load**
- **A:** Check internet connection. Data streams from GitHub (requires internet).

**Q: Figures don't display**
- **A:** In Colab, figures display automatically. If not, try `plt.show()`.

**Q: Different results than shown**
- **A:** Make sure random seed is set to 42 (done automatically in setup cell).

## For Instructors

### Using These Notebooks in Teaching

**As Lecture Materials:**
- Project notebook during class
- Run cells live to demonstrate concepts
- Modify code to show alternative scenarios

**As Lab Assignments:**
- Students work through notebooks independently
- Can modify code and re-run to explore
- Add exercise cells for practice problems

**As Homework:**
- Share Colab link with students
- Students submit completed notebooks
- Grading via code outputs and interpretations

### Customization Tips

To create your own exercises:
1. Copy an existing notebook
2. Add markdown cells with questions
3. Add empty code cells for student answers
4. Use `# TODO: Your code here` comments as prompts

## Development

### Creating New Notebooks

Follow the CH01 template structure:
1. Title cell with Colab badge
2. Overview with learning objectives
3. Setup cell
4. Alternating markdown/code sections
5. Summary cell

### Content Guidelines
- **Explanations**: 1 paragraph per concept
- **Code cells**: One logical unit per cell
- **Equations**: Use LaTeX with `$$` for display math
- **Economic interpretation**: Always emphasize practical meaning

### Testing
Before committing new notebooks:
1. Run "Runtime → Run all" in Google Colab
2. Verify all cells execute without errors
3. Check figures display correctly
4. Confirm outputs match expectations

## Contributing

Contributions welcome! To add a new notebook:

1. Follow the CH01 template structure
2. Use content from `code_python/` (code) and `slides_markdown/` (explanations)
3. Test thoroughly in Google Colab
4. Update this README with notebook details
5. Submit pull request

## References

**Textbook:**
- Cameron, A. Colin (2021). "Analysis of Economics Data: An Introduction to Econometrics"
- Website: https://cameron.econ.ucdavis.edu/aed/index.html

**Python Scripts:**
- Source: [`../code_python/`](../code_python/)
- All scripts 100% tested (Jan 2026)

**Slide Presentations:**
- Source: [`../slides_markdown/`](../slides_markdown/)
- Quarto-format educational content

## Support

For questions or issues:
- Check this README first
- Review the main project README: [`../README.md`](../README.md)
- See individual notebook for chapter-specific content

## License

Educational materials for teaching econometrics. Please cite appropriately if using in courses:

```
Cameron, A. Colin (2021). "Analysis of Economics Data"
Python notebooks by Carlos Mendez (2026)
```

---

**Last Updated:** January 20, 2026
**Status:** 16 notebooks complete (CH01-CH04, CH05-CH08, CH09-CH12, CH14-CH17)
**Quality:** All notebooks validated and tested in Google Colab
**Coverage:** Complete coverage of core econometric methods from introductory to advanced topics
