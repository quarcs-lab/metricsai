#!/usr/bin/env python3
"""Add DS4Bolivia Case Study 2 to CH15 notebook."""

import json
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
NB_PATH = PROJECT_ROOT / 'notebooks_colab' / 'ch15_Regression_with_Transformed_Variables.ipynb'


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
### Case Study 2: Nonlinear Satellite-Development Relationships

**Research Question**: What is the best functional form for modeling the relationship between satellite nighttime lights and municipal development in Bolivia?

**Background**: In previous chapters, we estimated *linear* regressions of development on NTL. But the relationship may be nonlinear—additional nighttime lights may have diminishing effects on development. In this case study, we apply Chapter 15's **transformation** tools to explore functional form choices for the satellite-development relationship.

**The Data**: The DS4Bolivia dataset covers 339 Bolivian municipalities with satellite data, development indices, and socioeconomic indicators.

**Key Variables**:
- `mun`: Municipality name
- `dep`: Department (administrative region)
- `imds`: Municipal Sustainable Development Index (0-100)
- `ln_NTLpc2017`: Log nighttime lights per capita (2017)
- `sdg7_1_ec`: Electricity coverage (SDG 7 indicator)"""),

# ---------- Load Data ----------
make_md_cell("""\
#### Load the DS4Bolivia Data"""),

make_code_cell("""\
# Load the DS4Bolivia dataset
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from statsmodels.formula.api import ols

url_bol = "https://raw.githubusercontent.com/quarcs-lab/ds4bolivia/master/ds4bolivia_v20250523.csv"
bol = pd.read_csv(url_bol)

# Select key variables for this case study
key_vars = ['mun', 'dep', 'imds', 'ln_NTLpc2017', 'sdg7_1_ec']
bol_cs = bol[key_vars].copy()

# Create raw NTL variable from log
bol_cs['NTLpc2017_raw'] = np.exp(bol_cs['ln_NTLpc2017'])

print("=" * 70)
print("DS4BOLIVIA: TRANSFORMED VARIABLES CASE STUDY")
print("=" * 70)
print(f"Observations: {len(bol_cs)}")
print(f"\\nKey variable summary:")
print(bol_cs[['imds', 'ln_NTLpc2017', 'NTLpc2017_raw', 'sdg7_1_ec']].describe().round(3))"""),

# ---------- Task 1 ----------
make_md_cell("""\
#### Task 1: Compare Log Specifications (Guided)

**Objective**: Estimate four regression specifications and compare functional forms.

**Instructions**:
1. Estimate four models:
   - (a) `imds ~ ln_NTLpc2017` (level-log)
   - (b) `np.log(imds) ~ ln_NTLpc2017` (log-log)
   - (c) `imds ~ NTLpc2017_raw` (level-level)
   - (d) `np.log(imds) ~ NTLpc2017_raw` (log-level)
2. Compare R² across specifications
3. Interpret the coefficient in each model (elasticity, semi-elasticity, or marginal effect)

**Note**: R² values are not directly comparable across models with different dependent variables (levels vs. logs)."""),

make_code_cell("""\
# Your code here: Compare four functional form specifications
#
# Example structure:
# bol_reg = bol_cs[['imds', 'ln_NTLpc2017', 'NTLpc2017_raw']].dropna()
# bol_reg = bol_reg[bol_reg['imds'] > 0]  # Ensure log is defined
#
# m_a = ols('imds ~ ln_NTLpc2017', data=bol_reg).fit(cov_type='HC1')
# m_b = ols('np.log(imds) ~ ln_NTLpc2017', data=bol_reg).fit(cov_type='HC1')
# m_c = ols('imds ~ NTLpc2017_raw', data=bol_reg).fit(cov_type='HC1')
# m_d = ols('np.log(imds) ~ NTLpc2017_raw', data=bol_reg).fit(cov_type='HC1')
#
# print("Model (a) Level-Log  R²:", m_a.rsquared.round(4))
# print("Model (b) Log-Log    R²:", m_b.rsquared.round(4))
# print("Model (c) Level-Level R²:", m_c.rsquared.round(4))
# print("Model (d) Log-Level  R²:", m_d.rsquared.round(4))"""),

# ---------- Task 2 ----------
make_md_cell("""\
#### Task 2: Quadratic NTL (Guided)

**Objective**: Test whether the NTL-development relationship exhibits diminishing returns.

**Instructions**:
1. Estimate `imds ~ ln_NTLpc2017 + I(ln_NTLpc2017**2)`
2. Test whether the quadratic term is statistically significant
3. Plot the fitted curve against the scatter plot of the data
4. Calculate the turning point: $NTL^* = -\\beta_1 / (2\\beta_2)$
5. Discuss: Is there evidence of diminishing returns to luminosity?"""),

make_code_cell("""\
# Your code here: Quadratic specification
#
# Example structure:
# m_quad = ols('imds ~ ln_NTLpc2017 + I(ln_NTLpc2017**2)', data=bol_reg).fit(cov_type='HC1')
# print(m_quad.summary())
#
# # Turning point
# b1 = m_quad.params['ln_NTLpc2017']
# b2 = m_quad.params['I(ln_NTLpc2017 ** 2)']
# print(f"\\nTurning point: ln_NTLpc = {-b1/(2*b2):.2f}")
#
# # Plot fitted curve
# x_range = np.linspace(bol_reg['ln_NTLpc2017'].min(), bol_reg['ln_NTLpc2017'].max(), 100)
# y_hat = m_quad.params['Intercept'] + b1*x_range + b2*x_range**2
# fig, ax = plt.subplots(figsize=(10, 6))
# ax.scatter(bol_reg['ln_NTLpc2017'], bol_reg['imds'], alpha=0.4, label='Data')
# ax.plot(x_range, y_hat, 'r-', linewidth=2, label='Quadratic fit')
# ax.set_xlabel('Log NTL per Capita (2017)')
# ax.set_ylabel('IMDS')
# ax.set_title('Quadratic NTL-Development Relationship')
# ax.legend()
# plt.show()"""),

# ---------- Key Concept 15.11 ----------
make_md_cell("""\
> **Key Concept 15.11: Diminishing Returns to Luminosity**
>
> A significant negative quadratic term for NTL suggests **diminishing marginal returns**: additional nighttime lights associate with progressively smaller development gains. In already-bright urban centers, more light reflects commercial excess rather than fundamental development improvement. This nonlinearity has practical implications: satellite-based predictions may be most accurate for municipalities in the middle of the luminosity distribution."""),

# ---------- Task 3 ----------
make_md_cell("""\
#### Task 3: Standardized Coefficients (Semi-guided)

**Objective**: Compare the relative importance of nighttime lights and electricity coverage for predicting development.

**Instructions**:
1. Standardize `imds`, `ln_NTLpc2017`, and `sdg7_1_ec` to mean=0 and sd=1
2. Estimate the regression on standardized variables
3. Compare standardized coefficients: Which predictor has a larger effect in standard deviation terms?

**Hint**: Use `(x - x.mean()) / x.std()` to standardize each variable."""),

make_code_cell("""\
# Your code here: Standardized coefficients
#
# Example structure:
# bol_std = bol_cs[['imds', 'ln_NTLpc2017', 'sdg7_1_ec']].dropna()
# for col in ['imds', 'ln_NTLpc2017', 'sdg7_1_ec']:
#     bol_std[f'{col}_z'] = (bol_std[col] - bol_std[col].mean()) / bol_std[col].std()
#
# m_std = ols('imds_z ~ ln_NTLpc2017_z + sdg7_1_ec_z', data=bol_std).fit(cov_type='HC1')
# print(m_std.summary())
# print("\\nStandardized coefficients (beta weights):")
# print(f"  NTL:         {m_std.params['ln_NTLpc2017_z']:.4f}")
# print(f"  Electricity: {m_std.params['sdg7_1_ec_z']:.4f}")"""),

# ---------- Task 4 ----------
make_md_cell("""\
#### Task 4: Interaction: NTL x Electricity (Semi-guided)

**Objective**: Test whether the effect of nighttime lights on development depends on electricity coverage.

**Instructions**:
1. Estimate `imds ~ ln_NTLpc2017 * sdg7_1_ec`
2. Interpret the interaction term: Does the NTL effect depend on electricity coverage?
3. Calculate the marginal effect of NTL at low (25th percentile) vs. high (75th percentile) electricity levels
4. Discuss: What does this interaction reveal about the satellite-development relationship?

**Hint**: The marginal effect of NTL is $\\beta_{NTL} + \\beta_{interaction} \\times electricity$."""),

make_code_cell("""\
# Your code here: Interaction model
#
# Example structure:
# m_int = ols('imds ~ ln_NTLpc2017 * sdg7_1_ec', data=bol_reg_full).fit(cov_type='HC1')
# print(m_int.summary())
#
# # Marginal effect at different electricity levels
# elec_25 = bol_reg_full['sdg7_1_ec'].quantile(0.25)
# elec_75 = bol_reg_full['sdg7_1_ec'].quantile(0.75)
# me_low = m_int.params['ln_NTLpc2017'] + m_int.params['ln_NTLpc2017:sdg7_1_ec'] * elec_25
# me_high = m_int.params['ln_NTLpc2017'] + m_int.params['ln_NTLpc2017:sdg7_1_ec'] * elec_75
# print(f"\\nMarginal effect of NTL at low electricity ({elec_25:.1f}%): {me_low:.4f}")
# print(f"Marginal effect of NTL at high electricity ({elec_75:.1f}%): {me_high:.4f}")"""),

# ---------- Key Concept 15.12 ----------
make_md_cell("""\
> **Key Concept 15.12: Elasticity of Development to Satellite Signals**
>
> In a log-log specification (log IMDS ~ log NTL), the coefficient directly estimates the **elasticity**: the percentage change in development associated with a 1% increase in nighttime lights per capita. An elasticity of, say, 0.15 means a 10% increase in NTL per capita is associated with a 1.5% increase in IMDS. Elasticities provide scale-free comparisons across different variables and contexts."""),

# ---------- Task 5 ----------
make_md_cell("""\
#### Task 5: Predictions with Retransformation (Independent)

**Objective**: Generate predictions from the log-log model and apply the Duan smearing correction.

**Instructions**:
1. Estimate the log-log model: `np.log(imds) ~ ln_NTLpc2017`
2. Generate naive predictions: $\\exp(\\widehat{\\ln(imds)})$
3. Apply the Duan smearing correction: multiply predictions by $\\bar{\\exp(\\hat{e})}$ (the mean of exponentiated residuals)
4. Compare naive vs. corrected predictions
5. Discuss: How much does the retransformation correction matter?"""),

make_code_cell("""\
# Your code here: Retransformation bias correction
#
# Example structure:
# m_loglog = ols('np.log(imds) ~ ln_NTLpc2017', data=bol_reg).fit(cov_type='HC1')
#
# # Naive prediction
# naive_pred = np.exp(m_loglog.fittedvalues)
#
# # Duan smearing correction
# smearing_factor = np.exp(m_loglog.resid).mean()
# corrected_pred = naive_pred * smearing_factor
#
# print(f"Smearing factor: {smearing_factor:.4f}")
# print(f"Mean actual IMDS: {bol_reg['imds'].mean():.2f}")
# print(f"Mean naive prediction: {naive_pred.mean():.2f}")
# print(f"Mean corrected prediction: {corrected_pred.mean():.2f}")"""),

# ---------- Task 6 ----------
make_md_cell("""\
#### Task 6: Functional Form Brief (Independent)

**Objective**: Write a 200-300 word brief summarizing your functional form analysis.

**Your brief should address**:
1. Which specification best captures the satellite-development relationship?
2. Is there evidence of nonlinearity (diminishing returns)?
3. What are the elasticity estimates from the log-log model?
4. Does the interaction with electricity coverage reveal important heterogeneity?
5. How important is the retransformation correction for practical predictions?
6. Policy implications: What do the functional form results imply for using satellite data to monitor SDG progress?"""),

make_code_cell("""\
# Your code here: Additional analysis for the brief
#
# You might want to:
# 1. Create a summary comparison table of all specifications
# 2. Plot fitted values from different models on the same graph
# 3. Calculate and compare elasticities across specifications
# 4. Summarize key statistics to cite in your brief"""),

# ---------- What You've Learned ----------
make_md_cell("""\
#### What You've Learned from This Case Study

Through this exploration of functional forms for the satellite-development relationship, you've applied Chapter 15's transformation toolkit to real geospatial data:

- **Functional form comparison**: Estimated level-level, level-log, log-level, and log-log specifications
- **Nonlinearity detection**: Used quadratic terms to test for diminishing returns to luminosity
- **Standardized coefficients**: Compared the relative importance of NTL and electricity coverage
- **Interaction effects**: Examined how electricity coverage moderates the NTL-development relationship
- **Retransformation**: Applied the Duan smearing correction to generate unbiased predictions from log models
- **Critical thinking**: Assessed which functional form best represents satellite-development patterns

**Connection**: In Chapter 16, we apply *diagnostic tools* to check whether our satellite prediction models satisfy regression assumptions.

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
            if '### Case Study: Transformed Variables' in source:
                # Replace the header
                new_source = source.replace(
                    '### Case Study: Transformed Variables',
                    '### Case Study 1: Transformed Variables'
                )
                # Rebuild source list
                lines = new_source.split('\n')
                cell['source'] = [line + '\n' if j < len(lines) - 1 else line
                                  for j, line in enumerate(lines)]
                print(f"Renamed Case Study header in cell {i}")
                break

    # Step 2: Find insertion point — after the case study cell (which contains "What You've Learned")
    insert_idx = None
    for i, cell in enumerate(notebook['cells']):
        if cell.get('cell_type') == 'markdown':
            source = ''.join(cell.get('source', []))
            if "### Case Study 1: Transformed Variables" in source and "What You've Learned" in source:
                insert_idx = i + 1
                break

    if insert_idx is None:
        # Fallback: look for the original name (in case rename didn't happen)
        for i, cell in enumerate(notebook['cells']):
            if cell.get('cell_type') == 'markdown':
                source = ''.join(cell.get('source', []))
                if "### Case Study:" in source and "Transformed Variables" in source:
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
