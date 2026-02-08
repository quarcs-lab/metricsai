#!/usr/bin/env python3
"""Add DS4Bolivia Case Study 2 to CH12 notebook."""

import json
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
NB_PATH = PROJECT_ROOT / 'notebooks_colab' / 'ch12_Further_Topics_in_Multiple_Regression.ipynb'


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
### Case Study 2: Robust Prediction of Municipal Development

In Chapters 10-11, we estimated multiple regression models predicting municipal development from nighttime lights and satellite embeddings, and tested the statistical significance of these predictors. Now we apply Chapter 12's tools for **robust inference** and **prediction**---crucial for translating satellite models into practical SDG monitoring tools.

**The Data**: The [DS4Bolivia project](https://github.com/quarcs-lab/ds4bolivia) provides a comprehensive dataset covering 339 Bolivian municipalities with over 350 variables, including the Municipal Sustainable Development Index (IMDS), nighttime lights per capita, and 64 satellite embedding dimensions. Here we focus on robust standard errors and prediction intervals for the satellite-development model."""),

# ---------- Load Data ----------
make_md_cell("""\
#### Load the DS4Bolivia Data

Let's load the DS4Bolivia dataset and select the key variables for robust inference and prediction analysis."""),

make_code_cell("""\
# Load the DS4Bolivia dataset
url_bol = "https://raw.githubusercontent.com/quarcs-lab/ds4bolivia/master/ds4bolivia_v20250523.csv"
bol = pd.read_csv(url_bol)

# Display basic information
print("=" * 70)
print("DS4BOLIVIA DATASET")
print("=" * 70)
print(f"Dataset shape: {bol.shape[0]} municipalities, {bol.shape[1]} variables")
print(f"\\nDepartments: {bol['dep'].nunique()} unique departments")
print(f"Department names: {sorted(bol['dep'].unique())}")

# Select key variables for this case study
key_vars = ['mun', 'dep', 'imds', 'ln_NTLpc2017',
            'A00', 'A10', 'A20', 'A30', 'A40']
bol_key = bol[key_vars].copy()

print(f"\\nKey variables selected: {len(key_vars)}")
print("\\n" + "=" * 70)
print("FIRST 10 MUNICIPALITIES")
print("=" * 70)
print(bol_key.head(10).to_string())

# Variable descriptions
print("\\n" + "=" * 70)
print("KEY VARIABLE DESCRIPTIONS")
print("=" * 70)
descriptions = {
    'mun': 'Municipality name',
    'dep': 'Department (administrative region, 9 total)',
    'imds': 'Municipal Sustainable Development Index (0-100, composite of all SDGs)',
    'ln_NTLpc2017': 'Log of nighttime lights per capita (2017, satellite-based)',
    'A00-A40': 'Satellite image embedding dimensions (5 of 64 principal features)',
}
for var, desc in descriptions.items():
    print(f"  {var:20s} --- {desc}")"""),

# ---------- Task 1: Default vs Robust SEs (Guided) ----------
make_md_cell("""\
#### Task 1: Default vs Robust Standard Errors (Guided)

**Objective**: Estimate the satellite-development model with both default and HC1 robust standard errors and compare the results.

**Instructions**:
1. Estimate `imds ~ ln_NTLpc2017 + A00 + A10 + A20 + A30 + A40` with default standard errors
2. Re-estimate with HC1 robust standard errors (`cov_type='HC1'`)
3. Compare standard errors side-by-side for each coefficient
4. Identify which coefficients have substantially different SEs under the two methods

**Apply what you learned in section 12.2**: Use `ols().fit()` for default SEs and `ols().fit(cov_type='HC1')` for robust SEs."""),

make_code_cell("""\
# Task 1: Default vs Robust Standard Errors
# ----------------------------------------------------------

# Prepare regression data (drop missing values)
reg_vars = ['imds', 'ln_NTLpc2017', 'A00', 'A10', 'A20', 'A30', 'A40']
reg_data = bol_key[reg_vars + ['dep']].dropna()
print(f"Regression sample: {len(reg_data)} municipalities (after dropping missing values)")

# Estimate with default standard errors
model_default = ols('imds ~ ln_NTLpc2017 + A00 + A10 + A20 + A30 + A40',
                    data=reg_data).fit()

# Estimate with HC1 robust standard errors
model_hc1 = ols('imds ~ ln_NTLpc2017 + A00 + A10 + A20 + A30 + A40',
                data=reg_data).fit(cov_type='HC1')

print("\\n" + "=" * 70)
print("COMPARISON: DEFAULT vs HC1 ROBUST STANDARD ERRORS")
print("=" * 70)
print(f"{'Variable':<18} {'Coef':>10} {'Default SE':>12} {'HC1 SE':>12} {'Ratio':>8}")
print("-" * 62)
for var in model_default.params.index:
    coef = model_default.params[var]
    se_def = model_default.bse[var]
    se_hc1 = model_hc1.bse[var]
    ratio = se_hc1 / se_def
    print(f"{var:<18} {coef:>10.4f} {se_def:>12.4f} {se_hc1:>12.4f} {ratio:>8.3f}")

print(f"\\nR-squared: {model_default.rsquared:.4f}")
print(f"Adj. R-squared: {model_default.rsquared_adj:.4f}")
print(f"\\nNote: Coefficients are identical --- only SEs change.")
print("Ratios > 1 suggest heteroskedasticity inflates default SEs' precision.")"""),

# ---------- Task 2: Cluster-Robust by Department (Guided) ----------
make_md_cell("""\
#### Task 2: Cluster-Robust Standard Errors by Department (Guided)

**Objective**: Re-estimate the model with cluster-robust standard errors grouped by department.

**Instructions**:
1. Re-estimate using `cov_type='cluster'` with `cov_kwds={'groups': reg_data['dep']}`
2. Compare cluster-robust SEs with default and HC1 SEs
3. Discuss: Why might municipalities within a department share unobserved characteristics?

**Apply what you learned in section 12.2**: Cluster-robust SEs account for within-group correlation of errors."""),

make_code_cell("""\
# Task 2: Cluster-Robust Standard Errors by Department
# ----------------------------------------------------------

# Estimate with cluster-robust SEs by department
model_cluster = ols('imds ~ ln_NTLpc2017 + A00 + A10 + A20 + A30 + A40',
                    data=reg_data).fit(cov_type='cluster',
                                      cov_kwds={'groups': reg_data['dep']})

print("=" * 70)
print("COMPARISON: DEFAULT vs HC1 vs CLUSTER-ROBUST STANDARD ERRORS")
print("=" * 70)
print(f"{'Variable':<18} {'Coef':>10} {'Default SE':>12} {'HC1 SE':>12} {'Cluster SE':>12}")
print("-" * 66)
for var in model_default.params.index:
    coef = model_default.params[var]
    se_def = model_default.bse[var]
    se_hc1 = model_hc1.bse[var]
    se_clust = model_cluster.bse[var]
    print(f"{var:<18} {coef:>10.4f} {se_def:>12.4f} {se_hc1:>12.4f} {se_clust:>12.4f}")

n_clusters = reg_data['dep'].nunique()
print(f"\\nNumber of clusters (departments): {n_clusters}")
print(f"Municipalities per department (avg): {len(reg_data) / n_clusters:.0f}")
print("\\nDiscussion: Municipalities within the same department share")
print("geographic, institutional, and cultural characteristics that create")
print("within-cluster correlation. Cluster-robust SEs account for this.")"""),

# ---------- Key Concept 12.11 ----------
make_md_cell("""\
> **Key Concept 12.11: Clustered Observations in Spatial Data**
>
> Municipalities within the same department share geographic, institutional, and cultural characteristics that create **within-cluster correlation**. Standard OLS assumes independent errors, but when municipalities in La Paz share unobserved factors that affect development, their errors are correlated. Cluster-robust standard errors account for this correlation, typically producing *larger* SEs than default or HC1, reflecting the reduced effective sample size."""),

# ---------- Task 3: Predict Conditional Mean (Semi-guided) ----------
make_md_cell("""\
#### Task 3: Predict Conditional Mean (Semi-guided)

**Objective**: Use `model.get_prediction()` to predict average IMDS for a municipality with median values of all predictors.

**Instructions**:
1. Calculate the median value of each predictor variable
2. Use `model_default.get_prediction()` to predict IMDS at the median predictor values
3. Report the predicted value and its 95% confidence interval
4. Interpret: "For a typical municipality, we predict IMDS between X and Y"

**Apply what you learned in section 12.3**: The confidence interval for the conditional mean reflects estimation uncertainty only."""),

make_code_cell("""\
# Task 3: Predict Conditional Mean
# ----------------------------------------------------------

# Your code here: Predict IMDS for a municipality with median predictor values
#
# Steps:
# 1. Calculate median values for each predictor
# 2. Create a DataFrame with those values
# 3. Use model_default.get_prediction() to get prediction and CI
# 4. Report and interpret

# Example structure:
# pred_vars = ['ln_NTLpc2017', 'A00', 'A10', 'A20', 'A30', 'A40']
# median_vals = reg_data[pred_vars].median()
# pred_data = pd.DataFrame([median_vals])
#
# pred = model_default.get_prediction(pred_data)
# pred_frame = pred.summary_frame(alpha=0.05)
# print(pred_frame)
#
# print(f"\\nPredicted IMDS: {pred_frame['mean'].values[0]:.2f}")
# print(f"95% CI for E[IMDS|X]: [{pred_frame['mean_ci_lower'].values[0]:.2f}, "
#       f"{pred_frame['mean_ci_upper'].values[0]:.2f}]")
# print(f"\\nInterpretation: For a typical municipality with median predictor")
# print(f"values, we predict average IMDS between "
#       f"{pred_frame['mean_ci_lower'].values[0]:.1f} and "
#       f"{pred_frame['mean_ci_upper'].values[0]:.1f}.")"""),

# ---------- Task 4: Prediction Interval (Semi-guided) ----------
make_md_cell("""\
#### Task 4: Prediction Interval for an Individual Municipality (Semi-guided)

**Objective**: Compute the 95% prediction interval for an *individual* municipality (not just the mean) and compare it with the confidence interval.

**Instructions**:
1. Use `model_default.get_prediction(...).summary_frame(alpha=0.05)` at the same median predictor values
2. Report the prediction interval using `obs_ci_lower` and `obs_ci_upper`
3. Compare the width of the prediction interval with the confidence interval from Task 3
4. Explain why the prediction interval is wider

**Apply what you learned in section 12.3**: Individual predictions must account for the irreducible error $u^*$, making them fundamentally less precise than conditional mean predictions."""),

make_code_cell("""\
# Task 4: Prediction Interval for an Individual Municipality
# ----------------------------------------------------------

# Your code here: Compute prediction interval and compare with CI
#
# Steps:
# 1. Use the same prediction from Task 3
# 2. Extract obs_ci_lower and obs_ci_upper for the prediction interval
# 3. Compare widths
# 4. Discuss why PI is wider

# Example structure:
# pred_vars = ['ln_NTLpc2017', 'A00', 'A10', 'A20', 'A30', 'A40']
# median_vals = reg_data[pred_vars].median()
# pred_data = pd.DataFrame([median_vals])
#
# pred = model_default.get_prediction(pred_data)
# pred_frame = pred.summary_frame(alpha=0.05)
#
# ci_width = pred_frame['mean_ci_upper'].values[0] - pred_frame['mean_ci_lower'].values[0]
# pi_width = pred_frame['obs_ci_upper'].values[0] - pred_frame['obs_ci_lower'].values[0]
#
# print("=" * 70)
# print("CONFIDENCE INTERVAL vs PREDICTION INTERVAL")
# print("=" * 70)
# print(f"Predicted IMDS: {pred_frame['mean'].values[0]:.2f}")
# print(f"\\n95% CI (conditional mean):  [{pred_frame['mean_ci_lower'].values[0]:.2f}, "
#       f"{pred_frame['mean_ci_upper'].values[0]:.2f}]  width = {ci_width:.2f}")
# print(f"95% PI (individual):        [{pred_frame['obs_ci_lower'].values[0]:.2f}, "
#       f"{pred_frame['obs_ci_upper'].values[0]:.2f}]  width = {pi_width:.2f}")
# print(f"\\nPI/CI width ratio: {pi_width / ci_width:.1f}x wider")
# print(f"\\nThe prediction interval is wider because it includes the")
# print(f"irreducible uncertainty from the individual error term u*.")"""),

# ---------- Key Concept 12.12 ----------
make_md_cell("""\
> **Key Concept 12.12: Prediction Uncertainty for SDG Monitoring**
>
> Satellite-based prediction models can estimate *average* development patterns with reasonable precision (narrow confidence intervals for the conditional mean). However, predicting development for a *specific municipality* involves much greater uncertainty (wide prediction intervals) because individual municipalities deviate from the average relationship. For SDG monitoring, this means satellite predictions are more reliable for identifying broad patterns than for pinpointing the exact development level of any single municipality."""),

# ---------- Task 5: Model Robustness (Independent) ----------
make_md_cell("""\
#### Task 5: Model Robustness Comparison (Independent)

**Objective**: Create a comprehensive comparison table showing coefficient estimates and standard errors under three specifications: default, HC1, and cluster-robust.

**Instructions**:
1. Create a formatted comparison table with coefficients, SEs, and significance stars under all three SE specifications
2. Identify whether any coefficients change sign or statistical significance across specifications
3. Discuss what the comparison reveals about model reliability
4. What does stability (or instability) across SE methods tell us about the trustworthiness of our satellite-development model?

**This extends Chapter 12 concepts**: You're systematically assessing how robust your conclusions are to different assumptions about the error structure."""),

make_code_cell("""\
# Task 5: Model Robustness Comparison
# ----------------------------------------------------------

# Your code here: Create comprehensive comparison table
#
# Steps:
# 1. Extract coefficients and SEs from all three models
# 2. Compute t-statistics and significance levels for each
# 3. Create a formatted comparison table
# 4. Identify any changes in sign or significance

# Example structure:
# def sig_stars(pval):
#     if pval < 0.01: return '***'
#     elif pval < 0.05: return '**'
#     elif pval < 0.10: return '*'
#     else: return ''
#
# print("=" * 90)
# print("MODEL ROBUSTNESS: COEFFICIENT ESTIMATES AND STANDARD ERRORS")
# print("=" * 90)
# print(f"{'Variable':<16} {'Coef':>8} {'SE(Def)':>10} {'SE(HC1)':>10} {'SE(Clust)':>10} "
#       f"{'Sig(D)':>7} {'Sig(H)':>7} {'Sig(C)':>7}")
# print("-" * 90)
# for var in model_default.params.index:
#     coef = model_default.params[var]
#     se_d = model_default.bse[var]
#     se_h = model_hc1.bse[var]
#     se_c = model_cluster.bse[var]
#     sig_d = sig_stars(model_default.pvalues[var])
#     sig_h = sig_stars(model_hc1.pvalues[var])
#     sig_c = sig_stars(model_cluster.pvalues[var])
#     print(f"{var:<16} {coef:>8.4f} {se_d:>10.4f} {se_h:>10.4f} {se_c:>10.4f} "
#           f"{sig_d:>7} {sig_h:>7} {sig_c:>7}")
# print("-" * 90)
# print("Significance: *** p<0.01, ** p<0.05, * p<0.10")
#
# print("\\nDo any coefficients change sign or significance?")
# print("What does this tell us about model reliability?")"""),

# ---------- Task 6: Prediction Brief (Independent) ----------
make_md_cell("""\
#### Task 6: Prediction Brief (Independent)

**Objective**: Write a 200-300 word assessment of prediction uncertainty in satellite-based development models.

**Your brief should address:**
1. How much uncertainty exists in satellite-based development predictions?
2. Are prediction intervals narrow enough to be useful for policy targeting?
3. How does the confidence interval for the conditional mean compare with the prediction interval for individual municipalities?
4. What additional data or methods might reduce prediction uncertainty?
5. Should policymakers rely on satellite predictions for allocating development resources to specific municipalities?

**Connection to Research**: The DS4Bolivia project shows that satellite-based models achieve meaningful but imperfect predictive accuracy. Your analysis quantifies *how much uncertainty* remains and whether it is small enough for practical SDG monitoring applications."""),

make_code_cell("""\
# Your code here: Additional analysis for the prediction brief
#
# You might want to:
# 1. Compare prediction intervals at different predictor values
#    (e.g., low-NTL vs high-NTL municipalities)
# 2. Calculate how many municipalities fall outside prediction intervals
# 3. Visualize actual vs predicted IMDS with confidence bands
#
# Example structure:
# # Actual vs predicted comparison
# reg_data['predicted'] = model_default.predict(reg_data)
# reg_data['residual'] = reg_data['imds'] - reg_data['predicted']
#
# print("=" * 70)
# print("PREDICTION ACCURACY SUMMARY")
# print("=" * 70)
# print(f"RMSE: {np.sqrt(model_default.mse_resid):.2f}")
# print(f"Mean IMDS: {reg_data['imds'].mean():.2f}")
# print(f"RMSE as % of mean: {100 * np.sqrt(model_default.mse_resid) / reg_data['imds'].mean():.1f}%")
# print(f"\\nLargest over-prediction: {reg_data['residual'].min():.2f}")
# print(f"Largest under-prediction: {reg_data['residual'].max():.2f}")"""),

# ---------- What You've Learned ----------
make_md_cell("""\
#### What You've Learned from This Case Study

Through this analysis of robust inference and prediction for Bolivia's satellite-development model, you've practiced:

- **Robust SE comparison**: Compared default, HC1, and cluster-robust standard errors for the same model
- **Cluster-robust inference**: Accounted for within-department correlation among municipalities
- **Conditional mean prediction**: Predicted average IMDS with a narrow 95% confidence interval
- **Prediction intervals**: Quantified the much larger uncertainty in predicting individual municipalities
- **Model robustness assessment**: Evaluated whether conclusions change across different SE specifications

These tools are essential for translating satellite-based models into credible SDG monitoring instruments. Robust inference ensures your significance conclusions hold under realistic data conditions, while prediction intervals honestly communicate the limits of individual-level forecasting.

**Connection to future chapters**: In Chapter 14, we add *indicator variables* for departments to explicitly model regional differences in the satellite-development relationship.

---

**Well done!** You've now applied Chapter 12's advanced inference and prediction tools to the satellite-development model, quantifying both the reliability of your estimates and the precision of your predictions."""),

]


def main():
    with open(NB_PATH, 'r', encoding='utf-8') as f:
        notebook = json.load(f)

    # ----------------------------------------------------------
    # Step 1: Check if existing Case Study heading needs renaming
    # ----------------------------------------------------------
    renamed = False
    for cell in notebook['cells']:
        if cell.get('cell_type') == 'markdown':
            source = ''.join(cell.get('source', []))
            # Match "### Case Study:" without a number (but NOT "### Case Study 1:")
            if '### Case Study:' in source and '### Case Study 1:' not in source:
                # Rename to "### Case Study 1:"
                new_source = source.replace('### Case Study:', '### Case Study 1:')
                lines = new_source.split('\n')
                cell['source'] = [line + '\n' if i < len(lines) - 1 else line
                                  for i, line in enumerate(lines)]
                renamed = True
                print("Renamed '### Case Study:' -> '### Case Study 1:'")
                break

    if not renamed:
        print("Existing heading already uses '### Case Study 1:' -- no rename needed.")

    # ----------------------------------------------------------
    # Step 2: Find insertion point after "What You've Learned"
    # closing of Case Study 1
    # ----------------------------------------------------------
    insert_idx = None
    for i, cell in enumerate(notebook['cells']):
        if cell.get('cell_type') == 'markdown':
            source = ''.join(cell.get('source', []))
            if "What You've Learned" in source and "case study" in source.lower():
                # Verify this is the Case Study 1 closing by checking content keywords
                if any(kw in source.lower() for kw in ['robust', 'cluster',
                                                        'productivity',
                                                        'you\'ve practiced',
                                                        'reliable']):
                    insert_idx = i + 1
                    print(f"Found Case Study 1 closing at cell index {i}")
                    break

    if insert_idx is None:
        # Fallback: insert before the last cell
        insert_idx = len(notebook['cells']) - 1
        print(f"WARNING: Could not find Case Study 1 closing. Inserting at index {insert_idx}")

    # ----------------------------------------------------------
    # Step 3: Insert Case Study 2 cells
    # ----------------------------------------------------------
    print(f"Inserting {len(cells_to_add)} cells at index {insert_idx}")

    original_count = len(notebook['cells'])
    for j, cell in enumerate(cells_to_add):
        notebook['cells'].insert(insert_idx + j, cell)

    # ----------------------------------------------------------
    # Step 4: Write modified notebook
    # ----------------------------------------------------------
    with open(NB_PATH, 'w', encoding='utf-8') as f:
        json.dump(notebook, f, indent=1, ensure_ascii=False)
        f.write('\n')

    print(f"Done! Notebook now has {len(notebook['cells'])} cells (was {original_count})")


if __name__ == '__main__':
    main()
