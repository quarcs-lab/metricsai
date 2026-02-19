#!/usr/bin/env python3
"""Add DS4Bolivia Case Study 2 to CH07 notebook."""

import json
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
NB_PATH = PROJECT_ROOT / 'notebooks_colab' / 'ch07_Statistical_Inference_for_Bivariate_Regression.ipynb'


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
### Case Study 2: Is the Light-Development Relationship Significant?

In Chapter 1, we introduced the DS4Bolivia project and estimated a simple regression of municipal development (IMDS) on nighttime lights (NTL). In Chapter 5, we explored bivariate relationships in depth. Now we apply Chapter 7's inference tools to test whether the NTL-development relationship is statistically significant and construct confidence intervals for the effect.

**Research Question:** Is the association between nighttime lights and municipal development statistically significant, and how precisely can we estimate the effect?

**Data:** Cross-sectional dataset covering 339 Bolivian municipalities from the [DS4Bolivia Project](https://github.com/quarcs-lab/ds4bolivia).

**Key Variables:**
- `imds`: Municipal Sustainable Development Index (0-100)
- `ln_NTLpc2017`: Log nighttime lights per capita (2017)
- `mun`: Municipality name
- `dep`: Department (administrative region)"""),

# ---------- Load Data ----------
make_md_cell("""\
#### Load the DS4Bolivia Data

Load the DS4Bolivia dataset and prepare the regression sample."""),

make_code_cell("""\
# Load the DS4Bolivia dataset
url_bol = "https://raw.githubusercontent.com/quarcs-lab/ds4bolivia/master/ds4bolivia_v20250523.csv"
bol = pd.read_csv(url_bol)

# Select key variables and prepare regression data
key_vars = ['mun', 'dep', 'imds', 'ln_NTLpc2017']
bol_key = bol[key_vars].copy()
reg_data = bol_key[['imds', 'ln_NTLpc2017']].dropna()

print("=" * 70)
print("DS4BOLIVIA DATASET — REGRESSION SAMPLE")
print("=" * 70)
print(f"Total municipalities: {len(bol_key)}")
print(f"Complete cases for regression: {len(reg_data)}")
print(f"\\nDescriptive statistics:")
print(reg_data.describe().round(3))"""),

# ---------- Task 1 ----------
make_md_cell("""\
### Task 1: Estimate and Test Slope (Guided)

**Objective:** Estimate the OLS regression of IMDS on log NTL per capita and test whether the slope is statistically significant.

**Instructions:**
1. Estimate the regression `imds ~ ln_NTLpc2017` using OLS
2. Display the full regression summary
3. Extract the t-statistic and p-value for the slope coefficient
4. Test the null hypothesis H\u2080: \u03b2\u2081 = 0 (no linear relationship)
5. State your conclusion: Can we reject the null at the 5% significance level?"""),

make_code_cell("""\
# Task 1: Estimate OLS and test the slope

# Estimate the model
model = ols('imds ~ ln_NTLpc2017', data=reg_data).fit()
print(model.summary())

# Extract t-statistic and p-value for the slope
t_stat = model.tvalues['ln_NTLpc2017']
p_value = model.pvalues['ln_NTLpc2017']

print("\\n" + "=" * 70)
print("HYPOTHESIS TEST: H\u2080: \u03b2\u2081 = 0")
print("=" * 70)
print(f"Slope coefficient: {model.params['ln_NTLpc2017']:.4f}")
print(f"Standard error:    {model.bse['ln_NTLpc2017']:.4f}")
print(f"t-statistic:       {t_stat:.4f}")
print(f"p-value:           {p_value:.6f}")
print(f"\\nConclusion: {'Reject' if p_value < 0.05 else 'Fail to reject'} H\u2080 at the 5% level.")
print(f"The NTL-development relationship is {'statistically significant' if p_value < 0.05 else 'not statistically significant'}.")"""),

# ---------- Task 2 ----------
make_md_cell("""\
### Task 2: Confidence Interval for Slope (Guided)

**Objective:** Construct and interpret a 95% confidence interval for the NTL coefficient.

**Instructions:**
1. Use `model.conf_int()` to obtain the 95% confidence interval
2. Extract the lower and upper bounds for the slope
3. Interpret: "We are 95% confident that a 1-unit increase in log NTL per capita is associated with between X and Y points of IMDS."
4. Does the confidence interval contain zero? What does that tell us?"""),

make_code_cell("""\
# Task 2: Confidence interval for the slope

ci = model.conf_int(alpha=0.05)
ci_lower = ci.loc['ln_NTLpc2017', 0]
ci_upper = ci.loc['ln_NTLpc2017', 1]

print("=" * 70)
print("95% CONFIDENCE INTERVAL FOR NTL COEFFICIENT")
print("=" * 70)
print(f"Point estimate:  {model.params['ln_NTLpc2017']:.4f}")
print(f"95% CI:          [{ci_lower:.4f}, {ci_upper:.4f}]")
print(f"\\nInterpretation: We are 95% confident that a 1-unit increase in")
print(f"log NTL per capita is associated with between {ci_lower:.2f} and {ci_upper:.2f}")
print(f"points of IMDS.")
print(f"\\nDoes the CI contain zero? {'Yes' if ci_lower <= 0 <= ci_upper else 'No'}")
print(f"This is consistent with {'failing to reject' if ci_lower <= 0 <= ci_upper else 'rejecting'} H\u2080: \u03b2\u2081 = 0.")"""),

# ---------- Task 3 ----------
make_md_cell("""\
### Task 3: Robust Standard Errors (Semi-guided)

**Objective:** Compare default (homoskedastic) standard errors with heteroskedasticity-robust (HC1) standard errors.

**Instructions:**
1. Re-estimate the model with HC1 robust standard errors using `cov_type='HC1'`
2. Compare the standard errors, t-statistics, and p-values between the two models
3. Discuss: Do the robust SEs differ substantially from the default SEs?
4. Why might robust standard errors matter for municipality-level spatial data?

**Hint:** Use `model_robust = ols('imds ~ ln_NTLpc2017', data=reg_data).fit(cov_type='HC1')`"""),

make_code_cell("""\
# Task 3: Robust standard errors

# Re-estimate with HC1 robust standard errors
model_robust = ols('imds ~ ln_NTLpc2017', data=reg_data).fit(cov_type='HC1')

# Compare default vs robust results
print("=" * 70)
print("COMPARISON: DEFAULT vs ROBUST STANDARD ERRORS")
print("=" * 70)
print(f"{'':30s} {'Default':>12s} {'Robust (HC1)':>12s}")
print("-" * 55)
print(f"{'Slope coefficient':30s} {model.params['ln_NTLpc2017']:12.4f} {model_robust.params['ln_NTLpc2017']:12.4f}")
print(f"{'Standard error':30s} {model.bse['ln_NTLpc2017']:12.4f} {model_robust.bse['ln_NTLpc2017']:12.4f}")
print(f"{'t-statistic':30s} {model.tvalues['ln_NTLpc2017']:12.4f} {model_robust.tvalues['ln_NTLpc2017']:12.4f}")
print(f"{'p-value':30s} {model.pvalues['ln_NTLpc2017']:12.6f} {model_robust.pvalues['ln_NTLpc2017']:12.6f}")
print(f"\\nSE ratio (robust/default): {model_robust.bse['ln_NTLpc2017'] / model.bse['ln_NTLpc2017']:.3f}")
print(f"\\nNote: A ratio substantially different from 1.0 signals heteroskedasticity.")"""),

# ---------- Key Concept 7.12 ----------
make_md_cell("""\
> **Key Concept 7.12: Robust Inference with Spatial Data**
>
> Municipality-level data often exhibits **heteroskedasticity**: the variance of development outcomes may differ between urban areas (where IMDS is tightly clustered around high values) and rural areas (where IMDS varies widely). Heteroskedasticity-robust standard errors (HC1) provide valid inference without assuming constant variance. When standard and robust SEs differ substantially, this signals heteroskedasticity in the data."""),

# ---------- Task 4 ----------
make_md_cell("""\
### Task 4: Two-Sided Hypothesis Test (Semi-guided)

**Objective:** Test whether the NTL coefficient equals a specific hypothesized value.

**Instructions:**
1. Test H\u2080: \u03b2\u2081 = 5 (a specific hypothesized effect size)
2. Calculate the t-statistic manually: t = (\u03b2\u0302\u2081 \u2212 5) / SE(\u03b2\u0302\u2081)
3. Compute the two-sided p-value using `scipy.stats.t.sf()`
4. Can we reject that the true effect equals exactly 5?

**Hint:** Use robust standard errors for this test. The degrees of freedom are `model_robust.df_resid`."""),

make_code_cell("""\
# Task 4: Two-sided hypothesis test for H0: beta_1 = 5
from scipy import stats

# Hypothesized value
beta_0_hyp = 5

# Calculate t-statistic manually
beta_hat = model_robust.params['ln_NTLpc2017']
se_robust = model_robust.bse['ln_NTLpc2017']
df = model_robust.df_resid

t_manual = (beta_hat - beta_0_hyp) / se_robust
p_two_sided = 2 * stats.t.sf(abs(t_manual), df=df)

print("=" * 70)
print(f"HYPOTHESIS TEST: H\u2080: \u03b2\u2081 = {beta_0_hyp}")
print("=" * 70)
print(f"Estimated slope:   {beta_hat:.4f}")
print(f"Hypothesized value: {beta_0_hyp}")
print(f"Robust SE:          {se_robust:.4f}")
print(f"t-statistic:        {t_manual:.4f}")
print(f"Degrees of freedom: {df}")
print(f"Two-sided p-value:  {p_two_sided:.6f}")
print(f"\\nConclusion: {'Reject' if p_two_sided < 0.05 else 'Fail to reject'} H\u2080 at the 5% level.")
print(f"{'The effect is significantly different from 5.' if p_two_sided < 0.05 else 'We cannot reject that the effect equals 5.'}") """),

# ---------- Task 5 ----------
make_md_cell("""\
### Task 5: One-Sided Test (Independent)

**Objective:** Test whether the NTL coefficient is positive (NTL has a positive effect on development).

**Instructions:**
1. State the hypotheses: H\u2080: \u03b2\u2081 \u2264 0 vs H\u2081: \u03b2\u2081 > 0
2. Calculate the one-sided p-value from the t-statistic
3. Use robust standard errors
4. Discuss: Is there strong evidence for a positive relationship between nighttime lights and development?

**Hint:** For a right-sided test, the one-sided p-value is `stats.t.sf(t_stat, df=df)`."""),

make_code_cell("""\
# Task 5: One-sided test — H0: beta_1 <= 0 vs H1: beta_1 > 0

# t-statistic for H0: beta_1 = 0 using robust SEs
t_onesided = model_robust.tvalues['ln_NTLpc2017']
p_onesided = stats.t.sf(t_onesided, df=model_robust.df_resid)

print("=" * 70)
print("ONE-SIDED TEST: H\u2080: \u03b2\u2081 \u2264 0 vs H\u2081: \u03b2\u2081 > 0")
print("=" * 70)
print(f"Estimated slope:     {model_robust.params['ln_NTLpc2017']:.4f}")
print(f"Robust SE:           {model_robust.bse['ln_NTLpc2017']:.4f}")
print(f"t-statistic:         {t_onesided:.4f}")
print(f"One-sided p-value:   {p_onesided:.8f}")
print(f"\\nConclusion: {'Reject' if p_onesided < 0.05 else 'Fail to reject'} H\u2080 at the 5% level.")
print(f"There {'is' if p_onesided < 0.05 else 'is not'} strong evidence for a positive NTL-development relationship.")"""),

# ---------- Key Concept 7.13 ----------
make_md_cell("""\
> **Key Concept 7.13: Practical Significance in Development**
>
> A statistically significant regression coefficient must be evaluated for **practical significance**. In the DS4Bolivia context, the NTL coefficient tells us how much IMDS changes for a 1-unit increase in log NTL per capita. Since IMDS ranges from roughly 20 to 80, an effect of, say, 5 points represents about 8% of the total range\u2014a meaningful but not transformative association. Policy decisions should weigh both statistical confidence and effect magnitude."""),

# ---------- Task 6 ----------
make_md_cell("""\
### Task 6: Economic vs Statistical Significance (Independent)

**Objective:** Write a 200-300 word discussion evaluating both the statistical and practical significance of the NTL-development relationship.

**Your discussion should address:**
1. **Statistical significance:** Summarize the hypothesis test results. Is the coefficient significant at the 1%, 5%, and 10% levels?
2. **Effect magnitude:** A 1-unit change in log NTL per capita corresponds to roughly a 172% increase in NTL per capita (since exp(1) \u2248 2.72). What does the estimated coefficient imply for development?
3. **Scale context:** Compare the effect magnitude with the full range of IMDS across municipalities. Is the effect large or small in practical terms?
4. **Policy implications:** If a policy could double NTL per capita in a municipality (a 0.69 increase in log NTL), how much IMDS improvement would we predict? Is that meaningful for SDG progress?
5. **Limitations:** Does statistical significance prove causation? What omitted variables could confound this relationship?"""),

make_code_cell("""\
# Task 6: Supporting analysis for economic vs statistical significance

# Summary statistics for context
imds_range = reg_data['imds'].max() - reg_data['imds'].min()
imds_std = reg_data['imds'].std()
beta = model_robust.params['ln_NTLpc2017']

print("=" * 70)
print("ECONOMIC vs STATISTICAL SIGNIFICANCE — KEY FACTS")
print("=" * 70)
print(f"\\nEstimated slope (robust): {beta:.4f}")
print(f"Robust p-value:           {model_robust.pvalues['ln_NTLpc2017']:.6f}")
print(f"\\nIMDS range:     {reg_data['imds'].min():.1f} to {reg_data['imds'].max():.1f} (range = {imds_range:.1f})")
print(f"IMDS std dev:   {imds_std:.2f}")
print(f"\\nEffect of 1-unit increase in log NTL:")
print(f"  IMDS change:           {beta:.2f} points")
print(f"  As % of IMDS range:    {100 * beta / imds_range:.1f}%")
print(f"  As % of IMDS std dev:  {100 * beta / imds_std:.1f}%")
print(f"\\nEffect of doubling NTL per capita (0.693 increase in log NTL):")
print(f"  Predicted IMDS change: {beta * 0.693:.2f} points")
print(f"  As % of IMDS range:    {100 * beta * 0.693 / imds_range:.1f}%")
print(f"\\nR-squared: {model.rsquared:.4f}")
print(f"NTL explains {model.rsquared * 100:.1f}% of variation in IMDS across municipalities.")"""),

# ---------- What You've Learned ----------
make_md_cell("""\
### What You've Learned

Through this case study on statistical inference for the NTL-development relationship in Bolivia, you practiced:

**Statistical Inference Skills:**
- Estimating OLS regression and extracting test statistics
- Constructing and interpreting 95% confidence intervals
- Computing heteroskedasticity-robust standard errors (HC1)
- Conducting two-sided hypothesis tests for specific values
- Conducting one-sided hypothesis tests for directional claims

**Economic Reasoning Skills:**
- Distinguishing statistical significance from practical significance
- Evaluating effect magnitudes in the context of policy-relevant scales
- Recognizing the role of heteroskedasticity in spatial economic data

**Connection to Future Chapters:**
In Chapters 10-12, we extend this analysis to *multiple regression*\u2014adding satellite embeddings alongside NTL to improve predictive power and test which features matter.

---

**Well done!** You've now applied the full toolkit of regression inference\u2014hypothesis tests, confidence intervals, robust standard errors, and significance evaluation\u2014to real-world satellite development data."""),

]


def main():
    with open(NB_PATH, 'r', encoding='utf-8') as f:
        notebook = json.load(f)

    # ---- Step 1: Rename "### Case Study:" to "### Case Study 1:" ----
    renamed = False
    for i, cell in enumerate(notebook['cells']):
        if cell.get('cell_type') == 'markdown':
            source = ''.join(cell.get('source', []))
            if '### Case Study:' in source and '### Case Study 1:' not in source:
                # Replace in the source list
                new_source = []
                for line in cell['source']:
                    new_source.append(line.replace('### Case Study:', '### Case Study 1:'))
                cell['source'] = new_source
                renamed = True
                print(f"Renamed '### Case Study:' to '### Case Study 1:' in cell {i}")
                break

    if not renamed:
        print("NOTE: '### Case Study:' heading not found (may already be numbered)")

    # ---- Step 2: Find insertion point ----
    # Insert after "What You've Learned" closing of Case Study 1
    insert_idx = None
    for i, cell in enumerate(notebook['cells']):
        if cell.get('cell_type') == 'markdown':
            source = ''.join(cell.get('source', []))
            if "What You've Learned" in source and 'convergence' in source.lower():
                insert_idx = i + 1
                break

    # Fallback: look for "What You've Learned" with productivity/capital keywords
    if insert_idx is None:
        for i, cell in enumerate(notebook['cells']):
            if cell.get('cell_type') == 'markdown':
                source = ''.join(cell.get('source', []))
                if ("What You've Learned" in source
                        and ('productivity' in source.lower()
                             or 'confidence interval' in source.lower()
                             or 'heteroskedasticity' in source.lower())):
                    insert_idx = i + 1
                    break

    if insert_idx is None:
        # Last resort: insert before the final empty cell
        insert_idx = len(notebook['cells']) - 1
        print(f"WARNING: Could not find Case Study 1 closing. Inserting at index {insert_idx}")
    else:
        print(f"Found Case Study 1 closing at cell {insert_idx - 1}")

    print(f"Inserting {len(cells_to_add)} cells at index {insert_idx}")

    # ---- Step 3: Insert cells ----
    for j, cell in enumerate(cells_to_add):
        notebook['cells'].insert(insert_idx + j, cell)

    # ---- Step 4: Write modified notebook ----
    with open(NB_PATH, 'w', encoding='utf-8') as f:
        json.dump(notebook, f, indent=1, ensure_ascii=False)
        f.write('\n')

    total_cells = len(notebook['cells'])
    original_cells = total_cells - len(cells_to_add)
    print(f"Done! Notebook now has {total_cells} cells (was {original_cells})")


if __name__ == '__main__':
    main()
