#!/usr/bin/env python3
"""Add DS4Bolivia Case Study 2 to CH17 notebook."""

import json
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
NB_PATH = PROJECT_ROOT / 'notebooks_colab' / 'ch17_Panel_Data_Time_Series_Data_Causation.ipynb'


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
### Case Study 2: Luminosity and Development Over Time: A Panel Approach

**Research Question**: How does nighttime luminosity evolve across Bolivia's municipalities over time, and what does within-municipality variation reveal about development dynamics?

**Background**: Throughout this textbook, we have analyzed *cross-sectional* satellite-development relationships. But the DS4Bolivia dataset includes nighttime lights data for 2012-2020, creating a natural **panel dataset**. In this case study, we apply Chapter 17's panel data tools to track how luminosity evolves across municipalities over time, using fixed effects to control for time-invariant characteristics.

**The Data**: The DS4Bolivia dataset covers 339 Bolivian municipalities with annual nighttime lights and population data for 2012-2020, yielding a potential panel of 3,051 municipality-year observations.

**Key Variables**:
- `mun`: Municipality name
- `dep`: Department (administrative region)
- `asdf_id`: Unique municipality identifier
- `ln_NTLpc2012` through `ln_NTLpc2020`: Log nighttime lights per capita (annual)
- `pop2012` through `pop2020`: Population (annual)"""),

# ---------- Load Data ----------
make_md_cell("""\
#### Load the DS4Bolivia Data and Create Panel Structure"""),

make_code_cell("""\
# Load the DS4Bolivia dataset
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from statsmodels.formula.api import ols

url_bol = "https://raw.githubusercontent.com/quarcs-lab/ds4bolivia/master/ds4bolivia_v20250523.csv"
bol = pd.read_csv(url_bol)

# Display available NTL and population variables
ntl_vars = [c for c in bol.columns if c.startswith('ln_NTLpc')]
pop_vars = [c for c in bol.columns if c.startswith('pop') and c[3:].isdigit()]

print("=" * 70)
print("DS4BOLIVIA: PANEL DATA CASE STUDY")
print("=" * 70)
print(f"Cross-sectional units: {len(bol)} municipalities")
print(f"\\nNTL variables available: {ntl_vars}")
print(f"Population variables available: {pop_vars}")"""),

# ---------- Task 1 ----------
make_md_cell("""\
#### Task 1: Create Panel Dataset (Guided)

**Objective**: Reshape the wide-format DS4Bolivia data into a long panel dataset.

**Instructions**:
1. Select municipality identifiers (`mun`, `dep`, `asdf_id`) and annual NTL/population variables
2. Reshape from wide to long format using `pd.melt()` or manual reshaping
3. Create columns: `municipality`, `year`, `ln_NTLpc`, `pop`, `ln_pop`
4. Verify the panel structure: 339 municipalities x 9 years = 3,051 observations
5. Show `head()` and `describe()` for the panel dataset"""),

make_code_cell("""\
# Your code here: Reshape to panel format
#
# Example structure:
# # Reshape NTL variables
# ntl_cols = {f'ln_NTLpc{y}': y for y in range(2012, 2021)}
# pop_cols = {f'pop{y}': y for y in range(2012, 2021)}
#
# # Melt NTL
# ntl_long = bol[['mun', 'dep', 'asdf_id'] + list(ntl_cols.keys())].melt(
#     id_vars=['mun', 'dep', 'asdf_id'],
#     var_name='ntl_var', value_name='ln_NTLpc'
# )
# ntl_long['year'] = ntl_long['ntl_var'].str.extract(r'(\\d{4})').astype(int)
#
# # Melt Population
# pop_long = bol[['asdf_id'] + list(pop_cols.keys())].melt(
#     id_vars=['asdf_id'],
#     var_name='pop_var', value_name='pop'
# )
# pop_long['year'] = pop_long['pop_var'].str.extract(r'(\\d{4})').astype(int)
#
# # Merge
# panel = ntl_long.merge(pop_long[['asdf_id', 'year', 'pop']],
#                        on=['asdf_id', 'year'], how='left')
# panel['ln_pop'] = np.log(panel['pop'])
# panel = panel.sort_values(['asdf_id', 'year']).reset_index(drop=True)
#
# print(f"Panel shape: {panel.shape}")
# print(f"Municipalities: {panel['asdf_id'].nunique()}")
# print(f"Years: {sorted(panel['year'].unique())}")
# print(panel.head(18))  # Show 2 municipalities
# print(panel[['ln_NTLpc', 'ln_pop', 'pop']].describe().round(3))"""),

# ---------- Key Concept 17.10 ----------
make_md_cell("""\
> **Key Concept 17.10: Satellite Panel Data**
>
> Annual nighttime lights observations create **panel datasets** even where traditional economic surveys are unavailable or infrequent. For Bolivia's 339 municipalities over 2012-2020, the NTL panel provides 3,051 municipality-year observations. This temporal dimension allows us to move beyond cross-sectional associations and study *changes within municipalities over time*—a crucial step toward understanding development dynamics rather than just static patterns."""),

# ---------- Task 2 ----------
make_md_cell("""\
#### Task 2: Pooled OLS with Cluster-Robust SEs (Guided)

**Objective**: Estimate a pooled OLS regression of NTL on population with cluster-robust standard errors.

**Instructions**:
1. Estimate `ln_NTLpc ~ ln_pop + year` using all panel observations
2. Use cluster-robust standard errors clustered by municipality
3. Compare default and cluster-robust SEs
4. Interpret: How does population relate to NTL? Is there a significant time trend?"""),

make_code_cell("""\
# Your code here: Pooled OLS with cluster-robust SEs
#
# Example structure:
# panel_reg = panel[['ln_NTLpc', 'ln_pop', 'year', 'mun', 'asdf_id']].dropna()
#
# model_pooled = ols('ln_NTLpc ~ ln_pop + year', data=panel_reg).fit(
#     cov_type='cluster', cov_kwds={'groups': panel_reg['asdf_id']}
# )
# print("POOLED OLS WITH CLUSTER-ROBUST SEs")
# print(model_pooled.summary())"""),

# ---------- Task 3 ----------
make_md_cell("""\
#### Task 3: Fixed Effects (Semi-guided)

**Objective**: Estimate a fixed effects model controlling for time-invariant municipality characteristics.

**Instructions**:
1. Add municipality fixed effects using `C(asdf_id)` or entity demeaning
2. Compare FE coefficients with pooled OLS coefficients
3. How does controlling for time-invariant municipality characteristics change the population-NTL relationship?
4. Discuss: What unobserved factors do municipality fixed effects absorb (altitude, remoteness, climate)?

**Hint**: You can use `C(asdf_id)` in the formula, or manually demean variables by subtracting municipality means. For large datasets, demeaning is more computationally efficient."""),

make_code_cell("""\
# Your code here: Fixed effects estimation
#
# Example structure (demeaning approach):
# # Demean variables within each municipality
# for col in ['ln_NTLpc', 'ln_pop']:
#     panel_reg[f'{col}_dm'] = panel_reg.groupby('asdf_id')[col].transform(
#         lambda x: x - x.mean()
#     )
# panel_reg['year_dm'] = panel_reg['year'] - panel_reg.groupby('asdf_id')['year'].transform('mean')
#
# model_fe = ols('ln_NTLpc_dm ~ ln_pop_dm + year_dm - 1', data=panel_reg).fit(
#     cov_type='cluster', cov_kwds={'groups': panel_reg['asdf_id']}
# )
# print("FIXED EFFECTS (WITHIN ESTIMATOR)")
# print(model_fe.summary())
#
# print("\\nCOMPARISON:")
# print(f"  Pooled OLS ln_pop coef: {model_pooled.params['ln_pop']:.4f}")
# print(f"  Fixed Effects ln_pop coef: {model_fe.params['ln_pop_dm']:.4f}")"""),

# ---------- Key Concept 17.11 ----------
make_md_cell("""\
> **Key Concept 17.11: Fixed Effects for Spatial Heterogeneity**
>
> Municipality fixed effects absorb all **time-invariant characteristics**: altitude, remoteness, climate, historical infrastructure, cultural factors. After removing these fixed differences, the remaining variation identifies how *changes* in population (or other time-varying factors) relate to *changes* in NTL within the same municipality. This within-municipality analysis is more credible for causal interpretation than cross-sectional regressions, because it eliminates bias from unobserved time-invariant confounders."""),

# ---------- Task 4 ----------
make_md_cell("""\
#### Task 4: Time Trends (Semi-guided)

**Objective**: Examine how nighttime lights evolve over time using year fixed effects.

**Instructions**:
1. Replace the linear time trend with year dummy variables: `C(year)`
2. Test whether the year effects are jointly significant
3. Plot the estimated year coefficients to visualize the NTL trajectory
4. Discuss: Did NTL grow steadily, or were there jumps or declines?

**Hint**: Use one year as the reference category. The year coefficients show NTL changes relative to the base year."""),

make_code_cell("""\
# Your code here: Year fixed effects
#
# Example structure:
# # Estimate with year dummies (demeaned for municipality FE)
# panel_reg['year_cat'] = panel_reg['year'].astype(str)
#
# # Simple approach: use year means of demeaned NTL
# year_means = panel_reg.groupby('year')['ln_NTLpc'].mean()
# year_means_dm = year_means - year_means.iloc[0]  # relative to base year
#
# fig, ax = plt.subplots(figsize=(10, 6))
# ax.plot(year_means.index, year_means.values, 'o-', color='navy', linewidth=2)
# ax.set_xlabel('Year')
# ax.set_ylabel('Mean Log NTL per Capita')
# ax.set_title('Average Municipal NTL Over Time (2012-2020)')
# ax.grid(True, alpha=0.3)
# plt.tight_layout()
# plt.show()"""),

# ---------- Task 5 ----------
make_md_cell("""\
#### Task 5: First Differences (Independent)

**Objective**: Estimate the relationship using first differences as an alternative to fixed effects.

**Instructions**:
1. Compute first differences: $\\Delta ln\\_NTLpc = ln\\_NTLpc_t - ln\\_NTLpc_{t-1}$ and $\\Delta ln\\_pop = ln\\_pop_t - ln\\_pop_{t-1}$
2. Estimate $\\Delta ln\\_NTLpc \\sim \\Delta ln\\_pop$
3. Compare the first-difference coefficient with the fixed effects estimate
4. Discuss: When do FE and FD give different results? What assumptions does each require?"""),

make_code_cell("""\
# Your code here: First differences estimation
#
# Example structure:
# panel_reg = panel_reg.sort_values(['asdf_id', 'year'])
# panel_reg['d_ln_NTLpc'] = panel_reg.groupby('asdf_id')['ln_NTLpc'].diff()
# panel_reg['d_ln_pop'] = panel_reg.groupby('asdf_id')['ln_pop'].diff()
#
# # Drop first year (no difference available)
# fd_data = panel_reg.dropna(subset=['d_ln_NTLpc', 'd_ln_pop'])
#
# model_fd = ols('d_ln_NTLpc ~ d_ln_pop', data=fd_data).fit(
#     cov_type='cluster', cov_kwds={'groups': fd_data['asdf_id']}
# )
# print("FIRST DIFFERENCES ESTIMATION")
# print(model_fd.summary())
#
# print(f"\\nFD coefficient on ln_pop: {model_fd.params['d_ln_pop']:.4f}")"""),

# ---------- Task 6 ----------
make_md_cell("""\
#### Task 6: Panel Brief (Independent)

**Objective**: Write a 200-300 word brief summarizing your panel data analysis.

**Your brief should address**:
1. What do within-municipality changes in NTL reveal about development dynamics?
2. How does the FE population coefficient differ from the cross-sectional (pooled OLS) one?
3. What time trends in NTL are visible across 2012-2020?
4. How do FE and FD estimates compare? Which assumptions matter most?
5. What are the advantages and limitations of satellite panel data for tracking municipal development over time?
6. What additional time-varying variables would improve the analysis?"""),

make_code_cell("""\
# Your code here: Additional analysis for the panel brief
#
# You might want to:
# 1. Decompose variance into between and within components
# 2. Plot NTL trajectories for selected municipalities
# 3. Compare growth rates across departments
# 4. Create a summary table of all estimation results
#
# Example: Variance decomposition
# overall_var = panel_reg['ln_NTLpc'].var()
# between_var = panel_reg.groupby('asdf_id')['ln_NTLpc'].mean().var()
# within_var = panel_reg.groupby('asdf_id')['ln_NTLpc'].apply(lambda x: x - x.mean()).var()
# print(f"Overall variance: {overall_var:.4f}")
# print(f"Between variance: {between_var:.4f}")
# print(f"Within variance:  {within_var:.4f}")
# print(f"Between share:    {between_var/overall_var:.1%}")"""),

# ---------- What You've Learned ----------
make_md_cell("""\
#### What You've Learned from This Case Study

This is the final DS4Bolivia case study in the textbook. Across 12 chapters, you have applied the complete econometric toolkit—from simple descriptive statistics (Chapter 1) through panel data methods (Chapter 17)—to study how satellite data can predict and monitor local economic development. The DS4Bolivia project demonstrates that modern data science and econometrics, combined with freely available satellite imagery, can contribute to SDG monitoring even in data-scarce contexts.

In this panel data analysis, you've applied Chapter 17's complete toolkit:

- **Panel construction**: Reshaped cross-sectional data into a municipality-year panel
- **Pooled OLS**: Estimated baseline relationships with cluster-robust standard errors
- **Fixed effects**: Controlled for time-invariant municipality characteristics
- **Time trends**: Examined the trajectory of nighttime lights across 2012-2020
- **First differences**: Used an alternative estimation strategy and compared with FE
- **Critical thinking**: Assessed what within-municipality variation reveals about development dynamics

**Congratulations!** You have now completed the full DS4Bolivia case study arc across the textbook.

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
            if '### Case Study: Panel Data Analysis' in source:
                new_source = source.replace(
                    '### Case Study: Panel Data Analysis',
                    '### Case Study 1: Panel Data Analysis'
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
            if "### Case Study 1: Panel Data Analysis" in source and "What You've Learned" in source:
                insert_idx = i + 1
                break

    if insert_idx is None:
        for i, cell in enumerate(notebook['cells']):
            if cell.get('cell_type') == 'markdown':
                source = ''.join(cell.get('source', []))
                if "### Case Study:" in source and "Panel Data Analysis" in source:
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
