#!/usr/bin/env python3
"""Add DS4Bolivia Case Study 2 to CH16 notebook."""

import json
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
NB_PATH = PROJECT_ROOT / 'notebooks_colab' / 'ch16_Checking_the_Model_and_Data.ipynb'


def make_md_cell(source):
    """Create a markdown cell dict."""
    lines = source.split('\n')
    source_list = [line + '\n' if i < len(lines) - 1 else line
                   for i, line in enumerate(lines)]
    return {
        "cell_type": "markdown",
        "metadata": {},
        "source": source_list
    }


def make_code_cell(source):
    """Create a code cell dict."""
    lines = source.split('\n')
    source_list = [line + '\n' if i < len(lines) - 1 else line
                   for i, line in enumerate(lines)]
    return {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": source_list
    }


# ============================================================
# Case Study 2 content cells
# ============================================================

cells_to_add = [

# ---------- Introduction ----------
make_md_cell("""\
### Case Study 2: Diagnosing the Satellite Prediction Model

**Research Question**: How reliable are the satellite-development regression models we have estimated throughout this textbook? Do they satisfy the standard regression assumptions?

**Background**: We have estimated multiple satellite-development regression models throughout this textbook. But how reliable are these models? In this case study, we apply Chapter 16's **diagnostic tools** to check for multicollinearity, heteroskedasticity, influential observations, and other model violations.

**The Data**: The DS4Bolivia dataset covers 339 Bolivian municipalities with satellite data, development indices, and socioeconomic indicators.

**Key Variables**:
- `mun`: Municipality name
- `dep`: Department (administrative region)
- `imds`: Municipal Sustainable Development Index (0-100)
- `ln_NTLpc2017`: Log nighttime lights per capita (2017)
- `A00`, `A10`, `A20`, `A30`, `A40`: Satellite image embedding dimensions"""),

# ---------- Load Data ----------
make_md_cell("""\
#### Load the DS4Bolivia Data"""),

make_code_cell("""\
# Load the DS4Bolivia dataset
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from statsmodels.formula.api import ols
from statsmodels.stats.outliers_influence import variance_inflation_factor, OLSInfluence
import statsmodels.api as sm

url_bol = "https://raw.githubusercontent.com/quarcs-lab/ds4bolivia/master/ds4bolivia_v20250523.csv"
bol = pd.read_csv(url_bol)

# Select key variables for this case study
key_vars = ['mun', 'dep', 'imds', 'ln_NTLpc2017', 'A00', 'A10', 'A20', 'A30', 'A40']
bol_cs = bol[key_vars].copy().dropna()

print("=" * 70)
print("DS4BOLIVIA: REGRESSION DIAGNOSTICS CASE STUDY")
print("=" * 70)
print(f"Observations (complete cases): {len(bol_cs)}")
print(f"\\nKey variable summary:")
print(bol_cs[['imds', 'ln_NTLpc2017', 'A00', 'A10', 'A20', 'A30', 'A40']].describe().round(3))"""),

# ---------- Task 1 ----------
make_md_cell("""\
#### Task 1: Multicollinearity Check (Guided)

**Objective**: Assess whether satellite predictors suffer from multicollinearity.

**Instructions**:
1. Compute the correlation matrix for the predictors (`ln_NTLpc2017`, `A00`, `A10`, `A20`, `A30`, `A40`)
2. Calculate VIF for each variable using `variance_inflation_factor()` from statsmodels
3. Flag variables with VIF > 10
4. Discuss: Are satellite embeddings multicollinear? Does multicollinearity affect the model's predictive power vs. individual coefficient interpretation?"""),

make_code_cell("""\
# Your code here: Multicollinearity diagnostics
#
# Example structure:
# predictors = ['ln_NTLpc2017', 'A00', 'A10', 'A20', 'A30', 'A40']
#
# # Correlation matrix
# print("CORRELATION MATRIX")
# print(bol_cs[predictors].corr().round(3))
#
# # VIF calculation
# X = bol_cs[predictors].copy()
# X = sm.add_constant(X)
# print("\\nVARIANCE INFLATION FACTORS")
# for i, col in enumerate(X.columns):
#     vif = variance_inflation_factor(X.values, i)
#     flag = " *** HIGH" if vif > 10 and col != 'const' else ""
#     print(f"  VIF({col}): {vif:.2f}{flag}")"""),

# ---------- Key Concept 16.11 ----------
make_md_cell("""\
> **Key Concept 16.11: Multicollinearity in Satellite Features**
>
> Satellite embedding dimensions often correlate with each other because they capture **overlapping visual patterns** from the same images. When embeddings A00 and A10 both respond to building density, their collinearity inflates standard errors and makes individual coefficients unstable. The VIF (Variance Inflation Factor) quantifies this: a VIF above 10 signals problematic collinearity. Solutions include dropping redundant features, using principal components, or accepting imprecise individual estimates while maintaining valid joint inference."""),

# ---------- Task 2 ----------
make_md_cell("""\
#### Task 2: Standard vs Robust SEs (Guided)

**Objective**: Detect heteroskedasticity by comparing default and robust standard errors.

**Instructions**:
1. Estimate the full model: `imds ~ ln_NTLpc2017 + A00 + A10 + A20 + A30 + A40`
2. Compare default (homoskedastic) and HC1 (robust) standard errors
3. Compute the ratio of robust to default SEs for each coefficient
4. Discuss: Large differences signal heteroskedasticity. Which coefficients are most affected?"""),

make_code_cell("""\
# Your code here: Compare standard and robust SEs
#
# Example structure:
# model_default = ols('imds ~ ln_NTLpc2017 + A00 + A10 + A20 + A30 + A40',
#                     data=bol_cs).fit()
# model_robust = ols('imds ~ ln_NTLpc2017 + A00 + A10 + A20 + A30 + A40',
#                    data=bol_cs).fit(cov_type='HC1')
#
# comparison = pd.DataFrame({
#     'Default SE': model_default.bse,
#     'Robust SE': model_robust.bse,
#     'Ratio': model_robust.bse / model_default.bse
# })
# print("STANDARD ERROR COMPARISON")
# print(comparison.round(4))
# print(f"\\nMean ratio: {(model_robust.bse / model_default.bse).mean():.3f}")"""),

# ---------- Task 3 ----------
make_md_cell("""\
#### Task 3: Residual Diagnostics (Semi-guided)

**Objective**: Create diagnostic plots to assess model assumptions visually.

**Instructions**:
1. Estimate the model with robust SEs
2. Create three diagnostic plots:
   - (a) Fitted values vs. residuals (check for patterns/heteroskedasticity)
   - (b) Q-Q plot of residuals (check for normality)
   - (c) Histogram of residuals (check for skewness/outliers)
3. Interpret each plot: What do the patterns reveal about model adequacy?

**Hint**: Use `model.fittedvalues` and `model.resid` for the plots. For the Q-Q plot, use `from scipy import stats; stats.probplot(residuals, plot=ax)`."""),

make_code_cell("""\
# Your code here: Residual diagnostic plots
#
# Example structure:
# from scipy import stats
# model = ols('imds ~ ln_NTLpc2017 + A00 + A10 + A20 + A30 + A40',
#             data=bol_cs).fit(cov_type='HC1')
#
# fig, axes = plt.subplots(1, 3, figsize=(15, 5))
#
# # (a) Residuals vs Fitted
# axes[0].scatter(model.fittedvalues, model.resid, alpha=0.4)
# axes[0].axhline(0, color='red', linestyle='--')
# axes[0].set_xlabel('Fitted Values')
# axes[0].set_ylabel('Residuals')
# axes[0].set_title('Residuals vs Fitted')
#
# # (b) Q-Q Plot
# stats.probplot(model.resid, plot=axes[1])
# axes[1].set_title('Q-Q Plot of Residuals')
#
# # (c) Histogram
# axes[2].hist(model.resid, bins=30, edgecolor='black', alpha=0.7)
# axes[2].set_xlabel('Residuals')
# axes[2].set_title('Distribution of Residuals')
#
# plt.tight_layout()
# plt.show()"""),

# ---------- Task 4 ----------
make_md_cell("""\
#### Task 4: Influential Municipalities (Semi-guided)

**Objective**: Identify municipalities that disproportionately influence the regression results.

**Instructions**:
1. Calculate DFITS for all observations
2. Apply the threshold: $|DFITS| > 2\\sqrt{k/n}$ where $k$ = number of parameters and $n$ = sample size
3. Identify the municipalities that exceed the threshold
4. Calculate DFBETAS for the key coefficient (`ln_NTLpc2017`)
5. Discuss: Are the influential municipalities capital cities or special cases?

**Hint**: Use `OLSInfluence(model)` from statsmodels to compute influence measures."""),

make_code_cell("""\
# Your code here: Influential observation analysis
#
# Example structure:
# model = ols('imds ~ ln_NTLpc2017 + A00 + A10 + A20 + A30 + A40',
#             data=bol_cs).fit()
# infl = OLSInfluence(model)
#
# # DFITS
# dfits_vals = infl.dffits[0]
# k = len(model.params)
# n = len(bol_cs)
# threshold = 2 * np.sqrt(k / n)
#
# influential = bol_cs.copy()
# influential['dfits'] = dfits_vals
# influential_muns = influential[np.abs(influential['dfits']) > threshold]
#
# print(f"DFITS threshold: {threshold:.4f}")
# print(f"Influential municipalities: {len(influential_muns)} out of {n}")
# print("\\nInfluential municipalities:")
# print(influential_muns[['mun', 'dep', 'imds', 'ln_NTLpc2017', 'dfits']]
#       .sort_values('dfits', key=abs, ascending=False).to_string(index=False))"""),

# ---------- Key Concept 16.12 ----------
make_md_cell("""\
> **Key Concept 16.12: Spatial Outliers and Influential Observations**
>
> In municipality-level analysis, **capital cities** and special economic zones often appear as influential observations. These municipalities may have unusually high NTL (from concentrated economic activity) or unusual satellite patterns (dense urban cores). A single influential municipality can shift regression coefficients substantially. DFITS and DFBETAS identify such observations, allowing us to assess whether our conclusions depend on a few exceptional cases."""),

# ---------- Task 5 ----------
make_md_cell("""\
#### Task 5: Omitted Variable Analysis (Independent)

**Objective**: Assess potential omitted variable bias by adding department controls.

**Instructions**:
1. Estimate models with and without department fixed effects (`C(dep)`)
2. Compare the satellite coefficients across specifications
3. Discuss: Do satellite coefficients change when adding department dummies?
4. What is the direction of potential omitted variable bias?
5. Consider: What unobserved factors might department dummies capture (geography, climate, policy)?"""),

make_code_cell("""\
# Your code here: Omitted variable analysis
#
# Example structure:
# m_no_dept = ols('imds ~ ln_NTLpc2017 + A00 + A10', data=bol_cs).fit(cov_type='HC1')
# m_with_dept = ols('imds ~ ln_NTLpc2017 + A00 + A10 + C(dep)', data=bol_cs).fit(cov_type='HC1')
#
# print("WITHOUT department controls:")
# print(f"  NTL coef: {m_no_dept.params['ln_NTLpc2017']:.4f} (SE: {m_no_dept.bse['ln_NTLpc2017']:.4f})")
# print(f"  R²: {m_no_dept.rsquared:.4f}")
#
# print("\\nWITH department controls:")
# print(f"  NTL coef: {m_with_dept.params['ln_NTLpc2017']:.4f} (SE: {m_with_dept.bse['ln_NTLpc2017']:.4f})")
# print(f"  R²: {m_with_dept.rsquared:.4f}")
#
# print(f"\\nCoefficient change: {m_with_dept.params['ln_NTLpc2017'] - m_no_dept.params['ln_NTLpc2017']:.4f}")"""),

# ---------- Task 6 ----------
make_md_cell("""\
#### Task 6: Diagnostic Report (Independent)

**Objective**: Write a 200-300 word comprehensive model assessment.

**Your report should address**:
1. **Multicollinearity**: Summarize VIF results for satellite features. Are any problematic?
2. **Heteroskedasticity**: What does the SE comparison reveal? Should we use robust SEs?
3. **Residual patterns**: What do the diagnostic plots show about model specification?
4. **Influential observations**: Which municipalities are most influential? Do they represent special cases?
5. **Omitted variables**: How do department controls affect the satellite coefficients?
6. **Recommendations**: What corrections or modifications would you recommend for the satellite prediction model?"""),

make_code_cell("""\
# Your code here: Additional analysis for the diagnostic report
#
# You might want to:
# 1. Create a summary table of diagnostic findings
# 2. Re-estimate the model excluding influential observations
# 3. Compare results with and without corrections
# 4. Summarize key statistics for your report"""),

# ---------- What You've Learned ----------
make_md_cell("""\
#### What You've Learned from This Case Study

Through this diagnostic analysis of the satellite prediction model, you've applied Chapter 16's complete toolkit to real geospatial data:

- **Multicollinearity assessment**: Computed VIF for satellite features and identified correlated embeddings
- **Heteroskedasticity detection**: Compared standard and robust SEs to assess variance assumptions
- **Residual diagnostics**: Created visual diagnostic plots to check model assumptions
- **Influence analysis**: Used DFITS and DFBETAS to identify municipalities that drive the results
- **Omitted variable assessment**: Tested sensitivity of results to department controls
- **Critical thinking**: Formulated recommendations for improving the satellite prediction model

**Connection**: In Chapter 17, we move to *panel data*—analyzing how nighttime lights evolve over time across municipalities, using fixed effects to control for time-invariant characteristics.

---"""),

]


def main():
    with open(NB_PATH, 'r', encoding='utf-8') as f:
        notebook = json.load(f)

    original_count = len(notebook['cells'])

    # Step 1: Rename "### Case Study:" to "### Case Study 1:" in the existing case study cell
    for i, cell in enumerate(notebook['cells']):
        if cell.get('cell_type') == 'markdown':
            source = ''.join(cell.get('source', []))
            if '### Case Study: Regression Diagnostics' in source:
                new_source = source.replace(
                    '### Case Study: Regression Diagnostics',
                    '### Case Study 1: Regression Diagnostics'
                )
                lines = new_source.split('\n')
                cell['source'] = [line + '\n' if j < len(lines) - 1 else line
                                  for j, line in enumerate(lines)]
                print(f"Renamed Case Study header in cell {i}")
                break

    # Step 2: Find insertion point — after the case study cell
    insert_idx = None
    for i, cell in enumerate(notebook['cells']):
        if cell.get('cell_type') == 'markdown':
            source = ''.join(cell.get('source', []))
            if "### Case Study 1: Regression Diagnostics" in source and "What You've Learned" in source:
                insert_idx = i + 1
                break

    if insert_idx is None:
        for i, cell in enumerate(notebook['cells']):
            if cell.get('cell_type') == 'markdown':
                source = ''.join(cell.get('source', []))
                if "### Case Study:" in source and "Regression Diagnostics" in source:
                    insert_idx = i + 1
                    break

    if insert_idx is None:
        insert_idx = len(notebook['cells']) - 1
        print(f"WARNING: Could not find Case Study 1 closing. Inserting at index {insert_idx}")

    print(f"Inserting {len(cells_to_add)} cells at index {insert_idx}")

    # Insert cells
    for j, cell in enumerate(cells_to_add):
        notebook['cells'].insert(insert_idx + j, cell)

    # Write modified notebook
    with open(NB_PATH, 'w', encoding='utf-8') as f:
        json.dump(notebook, f, indent=1, ensure_ascii=False)
        f.write('\n')

    print(f"Done! Notebook now has {len(notebook['cells'])} cells (was {original_count})")


if __name__ == '__main__':
    main()
