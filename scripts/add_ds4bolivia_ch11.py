#!/usr/bin/env python3
"""Add DS4Bolivia Case Study 2 to CH11 notebook."""

import json
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
NB_PATH = PROJECT_ROOT / 'notebooks_colab' / 'ch11_Statistical_Inference_for_Multiple_Regression.ipynb'


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
### Case Study 2: Which Satellite Features Matter? Joint Tests for Predictive Power

In Chapter 10, we estimated a multiple regression of municipal development on nighttime lights and satellite embeddings. Now we apply Chapter 11's inference tools—t-tests for individual coefficients and F-tests for joint significance—to determine which satellite features add statistically significant predictive power.

**Dataset:** DS4Bolivia — Satellite Data for Sustainable Development
- **Source:** [DS4Bolivia Project](https://github.com/quarcs-lab/ds4bolivia), 339 municipalities
- **Key variables:**
  - `imds` — Municipal Sustainable Development Index (0-100 composite)
  - `ln_NTLpc2017` — Log nighttime lights per capita (2017)
  - `A00`, `A10`, `A20`, `A30`, `A40` — Selected satellite image embedding dimensions

**Research question:** Do satellite image embeddings add statistically significant predictive power for municipal development beyond nighttime lights alone?

```python
# Load the DS4Bolivia dataset
url_bol = "https://raw.githubusercontent.com/quarcs-lab/ds4bolivia/master/ds4bolivia_v20250523.csv"
bol = pd.read_csv(url_bol)

# Select variables and prepare analysis sample
embed_vars = ['A00', 'A10', 'A20', 'A30', 'A40']
analysis_vars = ['imds', 'ln_NTLpc2017'] + embed_vars
bol_cs = bol[['mun', 'dep'] + analysis_vars].dropna(subset=analysis_vars).copy()
print(f"Analysis sample: {len(bol_cs)} municipalities with complete data")
bol_cs[analysis_vars].describe().round(3)
```"""),

# ---------- Task 1 ----------
make_md_cell("""\
#### Task 1: Estimate Full Model (Guided)

Estimate the full multiple regression model with nighttime lights and all five satellite embedding dimensions as predictors of municipal development.

```python
# Estimate: imds = beta_0 + beta_1*ln_NTLpc2017 + beta_2*A00 + ... + beta_6*A40 + u
model_full = ols('imds ~ ln_NTLpc2017 + A00 + A10 + A20 + A30 + A40', data=bol_cs).fit()
print(model_full.summary())
```

**Questions:**
- How many coefficients are estimated (including the intercept)?
- Which coefficients have p-values below 0.05? Below 0.10?
- What is the overall $R^2$? How much variation in development does this model explain?
- Compare this $R^2$ to a model with NTL alone—how much do the embeddings add?"""),

make_code_cell("""\
# Your code here: Estimate the full model
#
# Steps:
# 1. Estimate the full model with NTL and all 5 embeddings
# 2. Print the full summary
# 3. Identify significant coefficients (p < 0.05 and p < 0.10)

# Example structure:
# model_full = ols('imds ~ ln_NTLpc2017 + A00 + A10 + A20 + A30 + A40', data=bol_cs).fit()
# print(model_full.summary())
#
# # Identify significant predictors
# print("\\nSignificance at 5% level:")
# for var in model_full.params.index:
#     p = model_full.pvalues[var]
#     sig = "***" if p < 0.01 else "**" if p < 0.05 else "*" if p < 0.10 else ""
#     print(f"  {var:18s}  p = {p:.4f}  {sig}")"""),

# ---------- Task 2 ----------
make_md_cell("""\
#### Task 2: Confidence Intervals (Guided)

Compute 95% confidence intervals for all coefficients and create a coefficient plot (forest plot) to visualize the estimates and their uncertainty.

```python
# 95% confidence intervals
ci = model_full.conf_int(alpha=0.05)
ci.columns = ['Lower 2.5%', 'Upper 97.5%']
ci['Estimate'] = model_full.params
print(ci[['Estimate', 'Lower 2.5%', 'Upper 97.5%']].round(4))
```

**Questions:**
- Which confidence intervals include zero? What does this imply about significance?
- Which coefficient has the widest confidence interval? The narrowest (excluding intercept)?
- Create a forest plot showing point estimates and 95% CIs for the embedding coefficients
- How do the confidence intervals for embeddings compare in width to the NTL coefficient?"""),

make_code_cell("""\
# Your code here: Confidence intervals and coefficient plot
#
# Steps:
# 1. Compute confidence intervals with model_full.conf_int()
# 2. Print the table of estimates and CIs
# 3. Create a coefficient plot (forest plot) for embedding variables
# 4. Identify which CIs include zero

# Example structure:
# ci = model_full.conf_int(alpha=0.05)
# ci.columns = ['Lower', 'Upper']
# ci['Estimate'] = model_full.params
# print(ci[['Estimate', 'Lower', 'Upper']].round(4))
#
# # Forest plot for embedding coefficients
# embed_vars = ['A00', 'A10', 'A20', 'A30', 'A40']
# fig, ax = plt.subplots(figsize=(8, 5))
# y_pos = range(len(embed_vars))
# estimates = [model_full.params[v] for v in embed_vars]
# errors = [(model_full.params[v] - ci.loc[v, 'Lower'],
#            ci.loc[v, 'Upper'] - model_full.params[v]) for v in embed_vars]
# errors_T = list(zip(*errors))
# ax.errorbar(estimates, y_pos, xerr=errors_T, fmt='o', color='navy',
#             capsize=5, markersize=8)
# ax.axvline(x=0, color='red', linestyle='--', alpha=0.7, label='Zero (no effect)')
# ax.set_yticks(y_pos)
# ax.set_yticklabels(embed_vars)
# ax.set_xlabel('Coefficient Estimate with 95% CI')
# ax.set_title('Coefficient Plot: Satellite Embedding Effects on IMDS')
# ax.legend()
# plt.tight_layout()
# plt.show()"""),

# ---------- Task 3 ----------
make_md_cell("""\
#### Task 3: Individual t-Tests (Semi-guided)

Examine the t-statistics and p-values for each satellite embedding coefficient individually.

**Your tasks:**
1. Extract and display the t-statistic and p-value for each embedding variable (`A00`-`A40`)
2. Classify each as significant at 5%, significant at 10%, or not significant
3. Count how many of the 5 embeddings are individually significant at each level
4. Discuss: If some embeddings are individually insignificant, can we conclude they are "useless"? Why or why not?

**Hint:** Individual insignificance may reflect multicollinearity among embeddings rather than lack of predictive power. The joint F-test in Task 4 will help resolve this."""),

make_code_cell("""\
# Your code here: Individual t-tests for embedding coefficients
#
# Steps:
# 1. Extract t-statistics and p-values for each embedding
# 2. Classify significance levels
# 3. Discuss the implications

# Example structure:
# print("Individual t-Tests for Satellite Embeddings")
# print("=" * 60)
# embed_vars = ['A00', 'A10', 'A20', 'A30', 'A40']
# sig_5 = 0
# sig_10 = 0
# for var in embed_vars:
#     t = model_full.tvalues[var]
#     p = model_full.pvalues[var]
#     if p < 0.05:
#         level = "Significant at 5%  ***"
#         sig_5 += 1
#         sig_10 += 1
#     elif p < 0.10:
#         level = "Significant at 10% *"
#         sig_10 += 1
#     else:
#         level = "Not significant"
#     print(f"  {var}: t = {t:7.3f}, p = {p:.4f}  --> {level}")
# print(f"\\nSignificant at 5%:  {sig_5}/5 embeddings")
# print(f"Significant at 10%: {sig_10}/5 embeddings")"""),

# ---------- Task 4 ----------
make_md_cell("""\
#### Task 4: Joint F-Test (Semi-guided)

Test whether all five satellite embedding coefficients are jointly equal to zero.

$$H_0: \\beta_{A00} = \\beta_{A10} = \\beta_{A20} = \\beta_{A30} = \\beta_{A40} = 0$$

**Your tasks:**
1. Construct a restriction matrix $R$ where each row sets one embedding coefficient to zero
2. Use `model_full.f_test()` with the restriction matrix to compute the joint F-statistic
3. Report the F-statistic, degrees of freedom, and p-value
4. Compare the joint test result with the individual t-test results from Task 3
5. Are embeddings *jointly* significant even if some are individually insignificant?

**Hint:** The restriction matrix has 5 rows (one per restriction) and 7 columns (one per coefficient including intercept). Each row has a 1 in the position of the embedding coefficient being tested and 0s elsewhere."""),

make_code_cell("""\
# Your code here: Joint F-test for all embedding coefficients
#
# Steps:
# 1. Construct the restriction matrix R
# 2. Perform the joint F-test with model_full.f_test(R)
# 3. Report F-statistic and p-value
# 4. Compare with individual t-test results

# Example structure:
# import numpy as np
#
# # Restriction matrix: 5 restrictions (A00=A10=A20=A30=A40=0)
# # Coefficients order: Intercept, ln_NTLpc2017, A00, A10, A20, A30, A40
# R = np.zeros((5, 7))
# R[0, 2] = 1  # A00 = 0
# R[1, 3] = 1  # A10 = 0
# R[2, 4] = 1  # A20 = 0
# R[3, 5] = 1  # A30 = 0
# R[4, 6] = 1  # A40 = 0
#
# f_test = model_full.f_test(R)
# print("Joint F-Test: All Embedding Coefficients = 0")
# print("=" * 50)
# print(f"F-statistic: {f_test.fvalue[0][0]:.4f}")
# print(f"p-value:     {f_test.pvalue:.6f}")
# print(f"df:          ({int(f_test.df_num)}, {int(f_test.df_denom)})")
# print(f"\\nConclusion: {'Reject H0' if f_test.pvalue < 0.05 else 'Fail to reject H0'} at 5% level")"""),

# ---------- Key Concept 11.12 ----------
make_md_cell("""\
> **Key Concept 11.12: Joint Significance of Satellite Features**
>
> Individual satellite embedding coefficients may appear **statistically insignificant** (p > 0.05) in a multiple regression, yet the group of embeddings may be **jointly significant** (F-test p < 0.05). This paradox arises when embeddings are correlated with each other: the individual t-tests cannot distinguish each embedding's unique contribution, but the F-test captures their collective explanatory power. Joint F-tests are essential when evaluating groups of related predictors."""),

# ---------- Task 5 ----------
make_md_cell("""\
#### Task 5: Restricted vs Unrestricted Model Comparison (Independent)

Compare the restricted model (NTL only) with the unrestricted model (NTL + embeddings) to quantify the contribution of satellite embeddings.

**Your tasks:**
1. Estimate Model 1 (restricted): `imds ~ ln_NTLpc2017` (NTL only)
2. Estimate Model 2 (unrestricted): `imds ~ ln_NTLpc2017 + A00 + A10 + A20 + A30 + A40`
3. Compute the F-statistic manually using the formula:

$$F = \\frac{(R^2_u - R^2_r) / q}{(1 - R^2_u) / (n - k - 1)}$$

where $q = 5$ (number of restrictions), $n$ = sample size, $k$ = number of regressors in unrestricted model
4. Compare your manual calculation with `model_full.compare_f_test(model_restricted)`
5. Interpret: How much do the embeddings improve the model's explanatory power?"""),

make_code_cell("""\
# Your code here: Restricted vs unrestricted model comparison
#
# Steps:
# 1. Estimate restricted model (NTL only)
# 2. Compare R-squared values
# 3. Compute F-statistic manually
# 4. Verify with compare_f_test()

# Example structure:
# # Restricted model: NTL only
# model_restricted = ols('imds ~ ln_NTLpc2017', data=bol_cs).fit()
#
# # Compare R-squared
# R2_r = model_restricted.rsquared
# R2_u = model_full.rsquared
# n = model_full.nobs
# k = len(model_full.params) - 1  # number of regressors (excluding intercept)
# q = 5  # number of restrictions (embedding coefficients)
#
# print("Model Comparison")
# print("=" * 50)
# print(f"Restricted (NTL only):      R² = {R2_r:.4f}")
# print(f"Unrestricted (NTL + embed): R² = {R2_u:.4f}")
# print(f"Improvement in R²:          ΔR² = {R2_u - R2_r:.4f}")
#
# # Manual F-statistic
# F_manual = ((R2_u - R2_r) / q) / ((1 - R2_u) / (n - k - 1))
# print(f"\\nManual F-statistic: {F_manual:.4f}")
#
# # Verify with statsmodels
# f_compare = model_full.compare_f_test(model_restricted)
# print(f"compare_f_test:     F = {f_compare[0]:.4f}, p = {f_compare[1]:.6f}")"""),

# ---------- Task 6 ----------
make_md_cell("""\
#### Task 6: Inference Brief (Independent)

Write a 200-300 word inference brief summarizing your statistical findings.

**Your brief should address:**
1. Which satellite features add significant predictive power for municipal development?
2. Does the joint F-test tell a different story than the individual t-tests? Why?
3. How much do satellite embeddings improve explanatory power beyond nighttime lights alone?
4. What are the implications for feature selection in satellite-based prediction models?
5. How should researchers decide which satellite features to include in SDG prediction models?

**Connection to methods:** This analysis demonstrates a core tension in applied econometrics: individual insignificance vs. joint significance. When predictors are correlated (as satellite embeddings often are), individual t-tests may lack power while joint F-tests reveal collective importance."""),

make_code_cell("""\
# Your code here: Additional analysis for the inference brief
#
# You might want to:
# 1. Create a summary table comparing individual and joint test results
# 2. Visualize the R-squared improvement from adding embeddings
# 3. Calculate specific statistics to cite in your brief

# Example: Summary of key inference results
# print("KEY INFERENCE RESULTS")
# print("=" * 60)
# print(f"Sample size: {int(model_full.nobs)} municipalities")
# print(f"R² (NTL only):          {model_restricted.rsquared:.4f}")
# print(f"R² (NTL + embeddings):  {model_full.rsquared:.4f}")
# print(f"R² improvement:         {model_full.rsquared - model_restricted.rsquared:.4f}")
# print(f"\\nJoint F-test p-value:   {f_test.pvalue:.6f}")
# print(f"Individually significant at 5%: {sig_5}/5 embeddings")
# print(f"Individually significant at 10%: {sig_10}/5 embeddings")"""),

# ---------- Key Concept 11.13 ----------
make_md_cell("""\
> **Key Concept 11.13: Feature Selection in Prediction Models**
>
> When many potential predictors are available (e.g., 64 satellite embedding dimensions), selecting which to include requires balancing **explanatory power** against **model parsimony**. Joint F-tests help determine whether *subsets* of features add genuine predictive value beyond what simpler models provide. In the DS4Bolivia context, testing whether 5 selected embeddings improve upon NTL alone informs practical decisions about data collection and model complexity for SDG monitoring."""),

# ---------- What You've Learned ----------
make_md_cell("""\
#### What You've Learned from This Case Study

Through this analysis of satellite features and municipal development in Bolivia, you applied Chapter 11's full inference toolkit to a remote sensing application:

- **Full model estimation**: Estimated a multiple regression with nighttime lights and satellite embeddings as predictors of development
- **Confidence intervals**: Constructed and visualized 95% CIs for all coefficients using a forest plot
- **Individual t-tests**: Assessed the statistical significance of each satellite embedding individually
- **Joint F-tests**: Tested whether all embeddings are jointly significant using restriction matrices
- **Restricted vs unrestricted comparison**: Computed F-statistics manually and verified with `compare_f_test()`
- **Inference interpretation**: Distinguished between individual insignificance and joint significance

**Connection to the next chapter**: In Chapter 12, we address robust standard errors and prediction intervals—crucial for making reliable predictions about individual municipalities.

---

**Well done!** You've now applied the full statistical inference toolkit to two datasets—cross-country productivity and Bolivian satellite data—discovering that joint tests can reveal predictive power hidden from individual tests."""),

]


def main():
    with open(NB_PATH, 'r', encoding='utf-8') as f:
        notebook = json.load(f)

    # ------------------------------------------------------------------
    # Step 1: Rename existing "### Case Study:" to "### Case Study 1:"
    # ------------------------------------------------------------------
    renamed = False
    for cell in notebook['cells']:
        if cell.get('cell_type') == 'markdown':
            new_source = []
            for line in cell.get('source', []):
                if '### Case Study:' in line and 'Case Study 1' not in line and 'Case Study 2' not in line:
                    line = line.replace('### Case Study:', '### Case Study 1:')
                    renamed = True
                new_source.append(line)
            cell['source'] = new_source

    if renamed:
        print("Renamed '### Case Study:' -> '### Case Study 1:'")
    else:
        print("No rename needed (already numbered or not found)")

    # ------------------------------------------------------------------
    # Step 2: Find insertion point after "What You've Learned" of CS1
    # ------------------------------------------------------------------
    insert_idx = None
    for i, cell in enumerate(notebook['cells']):
        if cell.get('cell_type') == 'markdown':
            source = ''.join(cell.get('source', []))
            if "What You've Learned" in source and "inference toolkit" in source.lower():
                insert_idx = i + 1
                break

    if insert_idx is None:
        # Fallback: insert before the last empty cell
        insert_idx = len(notebook['cells']) - 1
        print(f"WARNING: Could not find Case Study 1 closing. Inserting at index {insert_idx}")
    else:
        print(f"Found Case Study 1 closing at cell {insert_idx - 1}")

    print(f"Inserting {len(cells_to_add)} cells at index {insert_idx}")

    # ------------------------------------------------------------------
    # Step 3: Insert Case Study 2 cells
    # ------------------------------------------------------------------
    for j, cell in enumerate(cells_to_add):
        notebook['cells'].insert(insert_idx + j, cell)

    # ------------------------------------------------------------------
    # Step 4: Write modified notebook
    # ------------------------------------------------------------------
    with open(NB_PATH, 'w', encoding='utf-8') as f:
        json.dump(notebook, f, indent=1, ensure_ascii=False)
        f.write('\n')

    total = len(notebook['cells'])
    original = total - len(cells_to_add)
    print(f"Done! Notebook now has {total} cells (was {original})")


if __name__ == '__main__':
    main()
