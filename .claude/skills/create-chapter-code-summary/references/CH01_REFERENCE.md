# CH01 Reference: Code Summary Design Decisions

This document shows the complete code summary created for Chapter 1 (Analysis of Economics Data) and explains every design decision. Use it as the gold standard when generating summaries for other chapters.

## Web App Key Concepts (guided the code structure)

The CH01 web app has 5 widgets, each teaching one key concept:

| Widget | Key Concept | Code Step |
|--------|-------------|-----------|
| Summary Stats | Descriptive statistics (mean, median, quartiles, skewness) | Step 2 |
| Scatter & Regression | Visualize before modeling; OLS as best-fit line | Steps 3, 4, 5 |
| Prediction Explorer | Slope as marginal effect; extrapolation danger | Step 4 (slope extraction) |
| R² Explained | Proportion of variation explained (TSS = ESS + RSS) | Step 5 (R² in title) |
| Multi-Predictor Comparison | Association is not causation; omitted variable bias | Step 6 |

## Insertion point

Placed after `**Prerequisites and Mathematical Background:**` and before `---` / `**Next Steps:**` in the Key Takeaways section.

## The complete code summary

```markdown
**Python Libraries and Code:**

This single code block reproduces the core workflow of Chapter 1. It is self-contained — copy it into an empty notebook and run it to review the complete pipeline from data loading to regression interpretation.

` ` `python
# =============================================================================
# CHAPTER 1 CHEAT SHEET: Analysis of Economics Data
# =============================================================================

# --- Libraries ---
import pandas as pd                       # data loading and manipulation
import matplotlib.pyplot as plt           # creating plots and visualizations
from statsmodels.formula.api import ols   # OLS regression with R-style formulas

# =============================================================================
# STEP 1: Load data directly from a URL
# =============================================================================
# pd.read_stata() reads Stata .dta files (pandas also supports CSV, Excel, etc.)
url = "https://raw.githubusercontent.com/quarcs-lab/data-open/master/AED/AED_HOUSE.DTA"
data_house = pd.read_stata(url)

print(f"Dataset: {data_house.shape[0]} observations, {data_house.shape[1]} variables")

# =============================================================================
# STEP 2: Descriptive statistics — summarize before modeling
# =============================================================================
# .head() shows the first rows; .describe() gives mean, std, min, quartiles, max
print(data_house[['price', 'size']].describe().round(2))

# =============================================================================
# STEP 3: Scatter plot — always visualize before fitting a regression
# =============================================================================
fig, ax = plt.subplots(figsize=(10, 6))
ax.scatter(data_house['size'], data_house['price'], s=50, alpha=0.7)
ax.set_xlabel('House Size (square feet)')
ax.set_ylabel('House Sale Price (dollars)')
ax.set_title('House Price vs Size')
ax.grid(True, alpha=0.3)
plt.tight_layout()
plt.show()

# =============================================================================
# STEP 4: OLS regression — fit the model
# =============================================================================
# Formula syntax: 'y ~ x' regresses y on x (intercept included automatically)
# IMPORTANT: .fit() estimates the model — without it, nothing is computed!
model = ols('price ~ size', data=data_house).fit()

# Extract key results
slope     = model.params['size']       # marginal effect: $/sq ft
intercept = model.params['Intercept']  # predicted price when size = 0
r_squared = model.rsquared             # proportion of variation explained

print(f"Estimated equation: price = {intercept:,.0f} + {slope:.2f} × size")
print(f"Interpretation: each additional sq ft is associated with ${slope:,.2f} higher price")
print(f"R-squared: {r_squared:.4f} ({r_squared*100:.1f}% of variation explained)")

# Full regression table (coefficients, std errors, t-stats, p-values, R²)
model.summary()

# =============================================================================
# STEP 5: Scatter plot with fitted regression line and R²
# =============================================================================
# model.fittedvalues contains the predicted y-values from the estimated equation
fig, ax = plt.subplots(figsize=(10, 6))
ax.scatter(data_house['size'], data_house['price'], s=50, alpha=0.7, label='Actual prices')
ax.plot(data_house['size'], model.fittedvalues, color='red', linewidth=2, label='Fitted line')
ax.set_xlabel('House Size (square feet)')
ax.set_ylabel('House Sale Price (dollars)')
ax.set_title(f'OLS Regression: price = {intercept:,.0f} + {slope:.2f} × size  (R² = {r_squared:.2%})')
ax.legend()
ax.grid(True, alpha=0.3)
plt.tight_layout()
plt.show()

# =============================================================================
# STEP 6: Compare predictors — association is NOT causation
# =============================================================================
# Running separate regressions with different x-variables shows that each tells
# a different story. High R² does not prove causation — omitted variables
# (location, condition, school district) can bias any single-variable slope.
predictors = {
    'size':      'Size (sq ft)',
    'bedrooms':  'Bedrooms',
    'bathrooms': 'Bathrooms',
    'lotsize':   'Lot size',
    'age':       'Age (years)',
}

print(f"{'Predictor':<18} {'Slope':>10} {'R²':>8}")
print("-" * 38)
for var, label in predictors.items():
    m = ols(f'price ~ {var}', data=data_house).fit()
    print(f"{label:<18} {m.params[var]:>10.2f} {m.rsquared:>8.4f}")
` ` `

**Try it yourself!** Copy this code into an empty Google Colab notebook and run it: [Open Colab](https://colab.research.google.com/notebooks/empty.ipynb)
```

## Design decisions explained

### What was included and why

| Step | What | Why included |
|------|------|-------------|
| Libraries | `pandas`, `matplotlib.pyplot`, `ols` from statsmodels | These are the 3 libraries actually used in the chapter's core workflow. `numpy` was imported in the Setup cell but never called directly in the chapter body — excluded to avoid confusion. |
| Step 1 | `pd.read_stata(url)` | Every chapter starts by loading data. The full URL is hardcoded (not referencing `GITHUB_DATA_URL`) so the block is self-contained. |
| Step 2 | `.describe().round(2)` | Maps to Web App Widget 1 (Summary Stats). Every chapter uses descriptive statistics as a first exploration step. |
| Step 3 | `ax.scatter()` | Maps to Web App Widget 2 (Scatter & Regression). The chapter's central message: "always visualize before fitting a regression." |
| Step 4 | `ols().fit()` + coefficient extraction | Maps to Web App Widgets 2-3. The core analytical method of the chapter. The `.fit()` reminder reinforces the "Common Mistakes to Avoid" section. |
| Step 5 | Scatter + fitted line + R² in title | Maps to Web App Widget 4 (R² Explained). Shows `model.fittedvalues` and puts R² front and center. |
| Step 6 | Loop over 5 predictors, compare slopes and R² | Maps to Web App Widget 5 (Multi-Predictor Comparison). Reinforces the chapter's central warning: association is not causation. |

### What was excluded and why

| Excluded | Why |
|----------|-----|
| `import numpy as np` | Never called directly in the chapter body. `pandas` and `statsmodels` handle everything. Including it would mislead students about which imports they need. |
| `import statsmodels.api as sm` | Imported in Setup but never used — only `ols` from `formula.api` is called. |
| `import random`, `import os` | Infrastructure for reproducibility and directory creation — not core econometrics. |
| `RANDOM_SEED`, `np.random.seed()` | Reproducibility setup. Important for the full chapter but irrelevant for a cheat sheet. |
| `plt.style.use('dark_background')` | Dark theme is a book design choice. The code must work on Colab's default white background. |
| `plt.rcParams.update({...})` | Same — dark theme configuration. |
| `os.makedirs(...)` | Directory creation for saving figures locally. Not relevant for Colab. |
| Case study datasets (Mendez, DS4Bolivia) | Case studies are practice exercises — the cheat sheet covers only the chapter's main teaching examples. |
| Equation text annotation (`ax.text(...)`) | Cosmetic enhancement on the fitted-line plot. Adds complexity without teaching a new concept. |
| Hex color codes (`#22d3ee`, `#c084fc`) | Tuned for the dark theme. Default blue and `'red'` are clearer on Colab's white background. |
| `data_house.head()` | Mentioned in the comment for Step 2 but not executed separately — `.describe()` is more informative. |

### Comment style

- **Inline import comments** explain the library's *role*, not its full name: `# data loading and manipulation` (not `# Python Data Analysis Library`)
- **Step headers** explain *why* the step matters: `always visualize before fitting a regression` (not `create a scatter plot`)
- **Inline result comments** explain the *econometric meaning*: `# marginal effect: $/sq ft` (not `# the slope parameter`)
- **The `.fit()` comment** deliberately echoes the "Common Mistakes to Avoid" blockquote immediately above the code summary in Key Takeaways

### Formatting choices

- **Banner separators** (`# ===...===`) — consistent 77-character width for visual rhythm
- **Step numbering** — sequential integers (STEP 1, STEP 2, ...) for easy reference
- **Aligned assignment** (`slope     = model.params[...]`) — aligns variable names for readability
- **f-strings with formatting** (`:,.0f`, `:.2f`, `:.4f`, `:.2%`) — shows students how to format output for different precision needs
