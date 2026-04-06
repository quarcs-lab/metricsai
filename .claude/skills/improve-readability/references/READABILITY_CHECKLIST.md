# Readability Checklist

Detailed detection rules for each category. Use this when auditing a chapter.

---

## Category 1: Code Cell Clarity

### 1A. Setup cell annotation

**How to detect:** Read the first code cell (usually within the `## Setup` section). Check if it has section dividers like `# --- Libraries ---` or equivalent grouping comments.

**Flag if:**

- Setup cell is >20 lines with no internal section breaks
- Library imports lack purpose comments (e.g., `import pandas as pd` with no hint about what it's for)
- Random seed, data URL, output dirs, and plotting style are all in one undivided block

**Template for fix:**

```python
# --- Libraries ---
import numpy as np                        # numerical operations
import pandas as pd                       # data manipulation
import matplotlib.pyplot as plt           # plotting
from statsmodels.formula.api import ols   # OLS with formula syntax

# --- Reproducibility ---
RANDOM_SEED = 42
np.random.seed(RANDOM_SEED)

# --- Data source ---
GITHUB_DATA_URL = "https://..."

# --- Output directories ---
os.makedirs('images', exist_ok=True)

# --- Plotting style ---
plt.style.use('dark_background')
plt.rcParams.update({...})
```

### 1B. Code cells doing too much

**How to detect:** For each ```` ```{python} ```` block, count distinct operations:

- Loading data = 1 operation
- Transforming/creating variables = 1 operation
- Computing statistics = 1 operation
- Creating a visualization = 1 operation
- Fitting a model = 1 operation
- Displaying output (.head(), .describe(), .summary()) = 1 operation

**Flag if:**

- Cell has 3+ distinct operations
- Cell is >25 lines (excluding comments)
- Cell produces multiple unrelated outputs

**Do NOT flag:**

- Setup cells (1 monolithic cell is fine if annotated)
- Visualization cells that set up and display a single plot
- Cells where operations are tightly coupled (load + immediate .head())

### 1C. Magic numbers

**How to detect:** Search code cells for these patterns:

```
1.96           → z-critical for 95% CI
0.975          → upper tail for 95% two-sided
ppf(0.975)     → percent point function call
ppf(0.95)      → one-sided test
alpha=0.7      → transparency
alpha=0.05     → significance level (if bare)
s=50, s=80     → marker size
figsize=(N, M) → figure dimensions
bins=N         → histogram bins
fontsize=N     → only if non-obvious
linewidth=N    → only if non-obvious
```

**Flag if:**

- Number appears with no inline comment AND no named variable
- Exception: `alpha=0.05` in hypothesis tests is universally known (don't flag)

**Fix pattern:** Either add inline comment or assign to named variable:

```python
# Inline comment:
ci = mean + 1.96 * se  # 1.96 = z-critical for 95% CI

# Named variable:
z_crit = 1.96  # 95% CI: P(-1.96 < Z < 1.96) = 0.95
ci = mean + z_crit * se
```

### 1D. Missing intermediate print statements

**How to detect:** Look for these patterns WITHOUT a following `print()`:

- `pd.read_stata(...)` or `pd.read_csv(...)` → should print shape
- `.describe()` → should print key observations
- `ols(...).fit()` → should print key coefficients
- `for i in range(N):` where N > 100 → should print progress
- Variable assignment with no output → should print result

**Flag if:**

- Data loaded with no shape/column confirmation
- Model fitted with no key result extraction
- Loop runs >100 iterations with no progress indicator

### 1E. Raw `.summary()` without key extraction

**How to detect:** Search for `model.summary()` or `.summary()` calls. Check if the same cell (or the cell immediately before) extracts and prints key coefficients.

**Flag if:**

- `.summary()` is the FIRST output after fitting a model
- No preceding `print(f"Slope: ...")` or equivalent
- Key statistics (slope, intercept, R-squared) not extracted into variables

---

## Category 2: Explanation Ordering

### 2A. Formula before intuition

**How to detect:** Find lines containing LaTeX math (`$...$` or `$$...$$`). Check the 1-3 lines BEFORE the formula for a plain-English explanation.

**Flag if:**

- Formula appears with no preceding natural-language sentence
- Formula appears right after a section header with no bridging text
- The only explanation is AFTER the formula

**Exceptions:**

- Inline math within a sentence (e.g., "where $n$ is the sample size") is fine
- Formulas in Key Concept boxes (already structured)

### 2B. Code before context

**How to detect:** For each ```` ```{python} ```` block, check the 1-5 markdown lines immediately before it.

**Flag if:**

- Code cell is preceded by only a section header (## X.Y Title) with no framing text
- Code cell is preceded by another code cell with no markdown in between
- The preceding markdown doesn't mention what the code will do

**Good framing examples:**

- "Let's load the data and check what variables we have."
- "The code below fits the regression and prints the key results."
- "Now we'll create a scatter plot to visualize the relationship."

### 2C. Results before interpretation

**How to detect:** After each code cell that produces output (visualization, table, statistics), check if interpretation follows within the next 10 markdown lines.

**Flag if:**

- Code output followed immediately by a new `## Section` header
- Code output followed by another code cell (no interpretation between)
- Interpretation is >20 lines below the code that produced it

---

## Category 3: Interpretation Guidance

### 3A. Visualizations without "what to look for"

**How to detect:** Find code cells containing `plt.show()`, `plt.savefig()`, or visualization functions (scatter, plot, hist, bar, heatmap). Check the markdown immediately after.

**Flag if:**

- No markdown within 5 lines after the closing ```` ``` ````
- Markdown after doesn't mention specific visual features (direction, pattern, outliers)
- Only a Key Concept box follows (these are generic, not plot-specific)

**Target format:**

```markdown
**What to look for:**

- **Direction**: Positive/negative relationship
- **Form**: Linear, curved, or no clear pattern
- **Strength**: Tight cluster or wide scatter
- **Outliers**: Any points far from the pattern
```

### 3B. Interpretation buried in code comments

**How to detect:** Search code cells for comment blocks that explain economics/statistics rather than code:

```python
# What do you see?
# - Positive relationship: ...
# - Roughly linear: ...

# Interpretation: The slope means...

# Economic story: ...

# Key finding: ...
```

**Flag if:**

- 3+ consecutive `#` comment lines that discuss results (not code logic)
- Comments contain words like "interpretation," "meaning," "suggests," "implies," "notice"

---

## Category 4: Regression Output

### 4A. Summary table shown first

**How to detect:** Find `.summary()` calls. Check if key coefficients are printed before the summary.

**Flag if:**

- `.summary()` is the only output in the cell
- No `print(f"...")` calls precede `.summary()` in the same cell

**Target pattern:**

```python
model = ols('price ~ size', data=df).fit()

# Key results first
print(f"Estimated equation: price = {model.params['Intercept']:,.0f} + {model.params['size']:.2f} x size")
print(f"R-squared: {model.rsquared:.4f}")

# Then full output
model.summary()
```

### 4B. No interpretation bridge

**How to detect:** After a cell containing `.summary()`, check if the next markdown section interprets the coefficients.

**Flag if:**

- Next markdown is a new `## Section` header with no interpretation
- Coefficients are not explained in economic terms anywhere nearby

---

## Category 5: Prose Quality

### 5A. Passive voice in introductions

**How to detect:** Check the first sentence of each `## Section`. Look for passive constructions:

- "X is analyzed..."
- "Results are shown..."
- "The data are loaded..."
- "It can be seen that..."
- "The regression is estimated..."

**Flag if:** The opening sentence of a section uses passive voice. Interior sentences are fine.

### 5B. Orphaned transitions

**How to detect:** Search for sentences matching these patterns:

- "Having [past participle]..." at start of paragraph
- "Now that we have [past participle]..."
- "With [noun] established/completed/done..."

**Flag if:**

- The sentence only restates what the previous section did
- Removing the sentence doesn't lose any new information
- The sentence appears between two sections (at the end of one or start of next)

### 5C. Walls of text

**How to detect:** Count words in each markdown paragraph (text between blank lines).

**Flag if:**

- Paragraph exceeds 100 words
- Multiple 80+ word paragraphs in sequence
- A concept list is written as prose instead of bullets

---

## Category 6: Jargon Management

### 6A. Terms used before definition

**How to detect:** For each technical term, find its first occurrence and check if it's accompanied by a definition.

**Key terms to track:**

- regression, OLS, Ordinary Least Squares
- dependent/independent variable, explanatory variable
- coefficient, intercept, slope
- R-squared, standard error, t-statistic, p-value
- confidence interval, hypothesis test, null hypothesis
- heteroskedasticity, homoskedasticity
- elasticity, semi-elasticity
- degrees of freedom
- multicollinearity, VIF
- endogeneity, omitted variable bias

**Flag if:**

- Term appears without parenthetical explanation or preceding definition
- Term appears in a section header but isn't defined in the section text

**Good pattern:**

```markdown
We use **Ordinary Least Squares (OLS)** — a method that finds the line
minimizing the sum of squared prediction errors.
```

### 6B. Missing cross-references

**How to detect:** In chapters 7+, search for references to earlier concepts. Check if they include a chapter pointer.

**Flag if:**

- "As we saw earlier..." without specifying where
- "Recall that..." without chapter reference
- Concept from ch01-06 used without "(see Chapter N)"

**Good pattern:**

```markdown
We use heteroskedasticity-robust standard errors (see Chapter 7)
to account for non-constant variance.
```
