#!/usr/bin/env python3
"""Add DS4Bolivia Case Study 2 to CH05 notebook."""

import json
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
NB_PATH = PROJECT_ROOT / 'notebooks_colab' / 'ch05_Bivariate_Data_Summary.ipynb'


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
### Case Study 2: Nighttime Lights and Development: A Bivariate Exploration

In Chapter 1, we introduced the DS4Bolivia project and estimated a simple regression of development on nighttime lights. In this case study, we apply Chapter 5's bivariate tools—scatter plots, correlations, OLS regression, and model fit measures—to explore multiple satellite-development relationships in greater depth.

**Data**: Cross-sectional dataset covering 339 Bolivian municipalities from the [DS4Bolivia Project](https://github.com/quarcs-lab/ds4bolivia).

**Key variables**:
- `mun`: Municipality name
- `dep`: Department (administrative region)
- `imds`: Municipal Sustainable Development Index (0–100 composite)
- `ln_NTLpc2017`: Log nighttime lights per capita (2017)
- `index_sdg1`: SDG 1 Index — No Poverty (0–100)
- `index_sdg4`: SDG 4 Index — Quality Education (0–100)
- `index_sdg8`: SDG 8 Index — Decent Work and Economic Growth (0–100)
- `sdg7_1_ec`: SDG 7.1 — Electricity coverage (%)
- `sdg1_1_ubn`: Unsatisfied Basic Needs (% of population)"""),

# ---------- Task 1: Load and Explore ----------
make_md_cell("""\
#### Task 1: Load and Explore (Guided)

**Objective**: Load the DS4Bolivia dataset, select key variables, and create a two-way frequency table.

**Instructions**:
1. Load the data from the URL below and select the key variables listed above
2. Use `pd.cut()` to bin the `imds` variable into three equal-frequency groups labeled **Low**, **Medium**, and **High** (terciles)
3. Create a two-way frequency table (cross-tabulation) of `imds` terciles against department using `pd.crosstab()`
4. Examine the table: Which departments have the most municipalities in the *Low* development category?"""),

make_code_cell("""\
# Load the DS4Bolivia dataset
url_bol = "https://raw.githubusercontent.com/quarcs-lab/ds4bolivia/master/ds4bolivia_v20250523.csv"
bol = pd.read_csv(url_bol)

# Select key variables for this case study
key_vars = ['mun', 'dep', 'imds', 'ln_NTLpc2017',
            'index_sdg1', 'index_sdg4', 'index_sdg8',
            'sdg7_1_ec', 'sdg1_1_ubn']
bol_cs = bol[key_vars].copy()

print(f"Dataset: {bol_cs.shape[0]} municipalities, {bol_cs.shape[1]} variables")
print(f"Departments: {sorted(bol_cs['dep'].unique())}")
print()

# Bin imds into terciles
bol_cs['imds_group'] = pd.cut(bol_cs['imds'],
                               bins=3,
                               labels=['Low', 'Medium', 'High'])

# Two-way frequency table: imds tercile x department
cross_tab = pd.crosstab(bol_cs['imds_group'], bol_cs['dep'],
                        margins=True, margins_name='Total')
print("Two-Way Frequency Table: IMDS Tercile by Department")
print("=" * 70)
print(cross_tab)"""),

# ---------- Task 2: Scatter Plots ----------
make_md_cell("""\
#### Task 2: Scatter Plots (Guided)

**Objective**: Create a 2×2 grid of scatter plots to compare different satellite-development relationships.

**Instructions**:
1. Create a figure with four subplots arranged in a 2×2 grid
2. Plot the following relationships:
   - (a) `ln_NTLpc2017` vs `imds`
   - (b) `ln_NTLpc2017` vs `index_sdg1`
   - (c) `ln_NTLpc2017` vs `sdg7_1_ec`
   - (d) `sdg1_1_ubn` vs `imds`
3. Add axis labels and subplot titles
4. Discuss: Which relationship appears strongest? Which appears weakest?"""),

make_code_cell("""\
# 2x2 scatter plot grid
fig, axes = plt.subplots(2, 2, figsize=(12, 10))

plot_data = bol_cs.dropna(subset=['ln_NTLpc2017', 'imds', 'index_sdg1',
                                   'sdg7_1_ec', 'sdg1_1_ubn'])

# (a) NTL vs IMDS
axes[0, 0].scatter(plot_data['ln_NTLpc2017'], plot_data['imds'],
                   alpha=0.5, color='#008CB7', s=20)
axes[0, 0].set_xlabel('Log NTL per Capita (2017)')
axes[0, 0].set_ylabel('IMDS')
axes[0, 0].set_title('(a) Nighttime Lights vs Development Index')

# (b) NTL vs SDG1 (No Poverty)
axes[0, 1].scatter(plot_data['ln_NTLpc2017'], plot_data['index_sdg1'],
                   alpha=0.5, color='#7A209F', s=20)
axes[0, 1].set_xlabel('Log NTL per Capita (2017)')
axes[0, 1].set_ylabel('SDG 1 Index (No Poverty)')
axes[0, 1].set_title('(b) Nighttime Lights vs No Poverty')

# (c) NTL vs SDG7.1 (Electricity Coverage)
axes[1, 0].scatter(plot_data['ln_NTLpc2017'], plot_data['sdg7_1_ec'],
                   alpha=0.5, color='#C21E72', s=20)
axes[1, 0].set_xlabel('Log NTL per Capita (2017)')
axes[1, 0].set_ylabel('Electricity Coverage (%)')
axes[1, 0].set_title('(c) Nighttime Lights vs Electricity Coverage')

# (d) UBN vs IMDS
axes[1, 1].scatter(plot_data['sdg1_1_ubn'], plot_data['imds'],
                   alpha=0.5, color='#2E86AB', s=20)
axes[1, 1].set_xlabel('Unsatisfied Basic Needs (%)')
axes[1, 1].set_ylabel('IMDS')
axes[1, 1].set_title('(d) Unsatisfied Basic Needs vs Development Index')

plt.suptitle('Bivariate Relationships: Satellite Data and Development in Bolivia',
             fontsize=14, fontweight='bold', y=1.02)
plt.tight_layout()
plt.show()"""),

# ---------- Key Concept 5.11 (after Task 2) ----------
make_md_cell("""\
> **Key Concept 5.11: Nighttime Lights as Development Proxy**
>
> Nighttime light (NTL) intensity measured by satellites correlates with GDP, electrification, and urbanization across the world. The **log per-capita** transformation serves two purposes: the logarithm compresses the highly skewed raw luminosity values, and dividing by population accounts for the mechanical relationship between more people and more light. After these transformations, NTL becomes a meaningful proxy for *economic intensity* rather than simply population density."""),

# ---------- Task 3: Correlation Analysis ----------
make_md_cell("""\
#### Task 3: Correlation Analysis (Semi-guided)

**Objective**: Calculate and visualize the correlation matrix for key development and satellite variables.

**Instructions**:
1. Select the variables: `imds`, `ln_NTLpc2017`, `index_sdg1`, `index_sdg4`, `index_sdg8`, `sdg7_1_ec`, `sdg1_1_ubn`
2. Calculate the Pearson correlation matrix using `.corr()`
3. Display the results as a heatmap or formatted table
4. Identify: Which variable has the **strongest** correlation with `imds`? Which has the **weakest**?

**Hint**: Use `plt.imshow()` or `sns.heatmap()` (if seaborn is available) to visualize the correlation matrix."""),

make_code_cell("""\
# Your code here: Correlation analysis
#
# Steps:
# 1. Select numeric variables of interest
# 2. Compute correlation matrix
# 3. Display as heatmap or formatted table
# 4. Identify strongest/weakest correlations with imds

# Example structure:
# corr_vars = ['imds', 'ln_NTLpc2017', 'index_sdg1', 'index_sdg4',
#              'index_sdg8', 'sdg7_1_ec', 'sdg1_1_ubn']
# corr_matrix = bol_cs[corr_vars].corr()
# print(corr_matrix.round(3))
#
# # Heatmap
# fig, ax = plt.subplots(figsize=(9, 7))
# im = ax.imshow(corr_matrix, cmap='RdBu_r', vmin=-1, vmax=1)
# ax.set_xticks(range(len(corr_vars)))
# ax.set_yticks(range(len(corr_vars)))
# ax.set_xticklabels(corr_vars, rotation=45, ha='right')
# ax.set_yticklabels(corr_vars)
# for i in range(len(corr_vars)):
#     for j in range(len(corr_vars)):
#         ax.text(j, i, f"{corr_matrix.iloc[i, j]:.2f}",
#                 ha='center', va='center', fontsize=8)
# plt.colorbar(im, ax=ax, label='Pearson Correlation')
# ax.set_title('Correlation Matrix: Development and Satellite Variables')
# plt.tight_layout()
# plt.show()
#
# # Identify strongest/weakest correlations with imds
# imds_corrs = corr_matrix['imds'].drop('imds').abs().sort_values(ascending=False)
# print(f"\\nStrongest correlation with IMDS: {imds_corrs.index[0]} (r = {corr_matrix.loc['imds', imds_corrs.index[0]]:.3f})")
# print(f"Weakest correlation with IMDS: {imds_corrs.index[-1]} (r = {corr_matrix.loc['imds', imds_corrs.index[-1]]:.3f})")"""),

# ---------- Task 4: OLS Regression Line ----------
make_md_cell("""\
#### Task 4: OLS Regression Line (Semi-guided)

**Objective**: Estimate and compare OLS regressions predicting IMDS from different variables.

**Instructions**:
1. Estimate OLS: `imds ~ ln_NTLpc2017`. Report the slope, intercept, and R²
2. Overlay the fitted regression line on a scatter plot of `ln_NTLpc2017` vs `imds`
3. Estimate a second OLS: `imds ~ sdg1_1_ubn`. Report slope, intercept, and R²
4. Compare: Which predictor explains more variation in development?

**Hint**: Use `ols()` from statsmodels as practiced in this chapter."""),

make_code_cell("""\
# Your code here: OLS regression with fitted lines
#
# Steps:
# 1. Estimate imds ~ ln_NTLpc2017
# 2. Overlay fitted line on scatter plot
# 3. Estimate imds ~ sdg1_1_ubn
# 4. Compare R-squared values

# Example structure:
# reg_data = bol_cs[['imds', 'ln_NTLpc2017', 'sdg1_1_ubn']].dropna()
#
# # Model 1: NTL
# model_ntl = ols('imds ~ ln_NTLpc2017', data=reg_data).fit()
# print("Model 1: IMDS ~ Log NTL per Capita")
# print(f"  Slope:     {model_ntl.params['ln_NTLpc2017']:.4f}")
# print(f"  Intercept: {model_ntl.params['Intercept']:.4f}")
# print(f"  R-squared: {model_ntl.rsquared:.4f}")
#
# # Model 2: UBN
# model_ubn = ols('imds ~ sdg1_1_ubn', data=reg_data).fit()
# print("\\nModel 2: IMDS ~ Unsatisfied Basic Needs")
# print(f"  Slope:     {model_ubn.params['sdg1_1_ubn']:.4f}")
# print(f"  Intercept: {model_ubn.params['Intercept']:.4f}")
# print(f"  R-squared: {model_ubn.rsquared:.4f}")
#
# # Scatter + fitted line for Model 1
# fig, ax = plt.subplots(figsize=(8, 6))
# ax.scatter(reg_data['ln_NTLpc2017'], reg_data['imds'], alpha=0.4, color='#008CB7', s=20)
# x_range = np.linspace(reg_data['ln_NTLpc2017'].min(), reg_data['ln_NTLpc2017'].max(), 100)
# ax.plot(x_range, model_ntl.params['Intercept'] + model_ntl.params['ln_NTLpc2017'] * x_range,
#         color='#C21E72', linewidth=2, label=f'OLS: R² = {model_ntl.rsquared:.3f}')
# ax.set_xlabel('Log NTL per Capita (2017)')
# ax.set_ylabel('IMDS')
# ax.set_title('OLS Regression: Nighttime Lights Predicting Development')
# ax.legend()
# plt.tight_layout()
# plt.show()"""),

# ---------- Key Concept 5.12 (after Task 4) ----------
make_md_cell("""\
> **Key Concept 5.12: Prediction vs. Causation with Satellite Data**
>
> A high R² between nighttime lights and development indices does **not** mean that lights *cause* development. Both NTL and IMDS reflect underlying economic activity, infrastructure, and urbanization. NTL is best understood as a **proxy variable**—an observable measure that correlates with the unobserved concept we care about (true economic development). The correlation is useful for prediction but should not be interpreted as a causal relationship."""),

# ---------- Task 5: Departmental Comparisons ----------
make_md_cell("""\
#### Task 5: Departmental Comparisons (Independent)

**Objective**: Assess whether the NTL-development relationship differs across Bolivia's departments.

**Instructions**:
1. Create a scatter plot of `ln_NTLpc2017` vs `imds` with points colored by department
2. Visually assess: Does the relationship appear to differ across departments?
3. Run separate OLS regressions for 2–3 departments and compare slopes and R² values
4. Discuss: What might explain differences in the satellite-development relationship across regions?"""),

make_code_cell("""\
# Your code here: Departmental comparisons
#
# Steps:
# 1. Create scatter plot colored by department
# 2. Run separate regressions for 2-3 departments
# 3. Compare slopes and R-squared

# Example structure:
# plot_data = bol_cs[['ln_NTLpc2017', 'imds', 'dep']].dropna()
# departments = plot_data['dep'].unique()
# colors = plt.cm.tab10(np.linspace(0, 1, len(departments)))
#
# fig, ax = plt.subplots(figsize=(10, 7))
# for dep, color in zip(sorted(departments), colors):
#     subset = plot_data[plot_data['dep'] == dep]
#     ax.scatter(subset['ln_NTLpc2017'], subset['imds'],
#                alpha=0.6, color=color, label=dep, s=25)
# ax.set_xlabel('Log NTL per Capita (2017)')
# ax.set_ylabel('IMDS')
# ax.set_title('NTL vs Development by Department')
# ax.legend(bbox_to_anchor=(1.05, 1), loc='upper left', fontsize=8)
# plt.tight_layout()
# plt.show()
#
# # Separate regressions for selected departments
# for dep_name in ['La Paz', 'Santa Cruz', 'Potosí']:
#     dep_data = plot_data[plot_data['dep'] == dep_name]
#     if len(dep_data) > 5:
#         model_dep = ols('imds ~ ln_NTLpc2017', data=dep_data).fit()
#         print(f"{dep_name}: slope = {model_dep.params['ln_NTLpc2017']:.3f}, "
#               f"R² = {model_dep.rsquared:.3f}, n = {len(dep_data)}")"""),

# ---------- Task 6: Alternative Predictors ----------
make_md_cell("""\
#### Task 6: Alternative Predictors (Independent)

**Objective**: Compare nighttime lights with unsatisfied basic needs (UBN) as predictors of development.

**Instructions**:
1. Compare the R² values from `imds ~ ln_NTLpc2017` and `imds ~ sdg1_1_ubn`
2. Create side-by-side scatter plots with fitted regression lines for both models
3. Discuss: Which predictor has the higher R²? Why might a socioeconomic variable (UBN) predict development better than satellite data (NTL)?
4. Reflect: What are the advantages of satellite data even if its R² is lower?"""),

make_code_cell("""\
# Your code here: Compare NTL vs UBN as predictors of IMDS
#
# Steps:
# 1. Estimate both models (if not already done in Task 4)
# 2. Create side-by-side fitted line plots
# 3. Compare R-squared values
# 4. Discuss advantages and limitations

# Example structure:
# reg_data = bol_cs[['imds', 'ln_NTLpc2017', 'sdg1_1_ubn']].dropna()
# model_ntl = ols('imds ~ ln_NTLpc2017', data=reg_data).fit()
# model_ubn = ols('imds ~ sdg1_1_ubn', data=reg_data).fit()
#
# fig, axes = plt.subplots(1, 2, figsize=(14, 5))
#
# # Left: NTL model
# axes[0].scatter(reg_data['ln_NTLpc2017'], reg_data['imds'], alpha=0.4, color='#008CB7', s=20)
# x1 = np.linspace(reg_data['ln_NTLpc2017'].min(), reg_data['ln_NTLpc2017'].max(), 100)
# axes[0].plot(x1, model_ntl.predict(pd.DataFrame({'ln_NTLpc2017': x1})),
#              color='#C21E72', linewidth=2)
# axes[0].set_xlabel('Log NTL per Capita (2017)')
# axes[0].set_ylabel('IMDS')
# axes[0].set_title(f'Model 1: NTL (R² = {model_ntl.rsquared:.3f})')
#
# # Right: UBN model
# axes[1].scatter(reg_data['sdg1_1_ubn'], reg_data['imds'], alpha=0.4, color='#7A209F', s=20)
# x2 = np.linspace(reg_data['sdg1_1_ubn'].min(), reg_data['sdg1_1_ubn'].max(), 100)
# axes[1].plot(x2, model_ubn.predict(pd.DataFrame({'sdg1_1_ubn': x2})),
#              color='#C21E72', linewidth=2)
# axes[1].set_xlabel('Unsatisfied Basic Needs (%)')
# axes[1].set_ylabel('IMDS')
# axes[1].set_title(f'Model 2: UBN (R² = {model_ubn.rsquared:.3f})')
#
# plt.suptitle('Comparing Predictors of Municipal Development',
#              fontsize=13, fontweight='bold')
# plt.tight_layout()
# plt.show()
#
# print(f"\\nR² comparison:")
# print(f"  NTL model: {model_ntl.rsquared:.4f}")
# print(f"  UBN model: {model_ubn.rsquared:.4f}")
# print(f"  Difference: {abs(model_ubn.rsquared - model_ntl.rsquared):.4f}")"""),

# ---------- What You've Learned ----------
make_md_cell("""\
### What You've Learned from This Case Study

Through this bivariate exploration of satellite data and municipal development in Bolivia, you've applied the full Chapter 5 toolkit:

- **Two-way tabulations** for categorical exploration of development levels across departments
- **Multiple scatter plots** comparing satellite-development relationships across different indicators
- **Correlation analysis** across multiple SDG indicators to identify strongest and weakest associations
- **OLS regression with fitted lines and R²** to quantify the NTL-development relationship
- **Regional heterogeneity** in bivariate relationships across Bolivia's departments
- **Comparing alternative predictors** of development (satellite data vs. socioeconomic measures)

**Connection to the research**: The DS4Bolivia project extends this bivariate analysis to multivariate machine learning models, using 64-dimensional satellite embeddings alongside nighttime lights to achieve higher predictive accuracy for SDG indicators.

**Looking ahead**: In Chapter 7, we'll apply *statistical inference* to these regressions—testing whether the NTL coefficient is significantly different from zero and constructing confidence intervals for the effect of satellite data on development.

---

**Well done!** You've now explored two real-world datasets—cross-country convergence and Bolivian municipal development—using the complete bivariate analysis toolkit from Chapter 5."""),

]


def main():
    with open(NB_PATH, 'r', encoding='utf-8') as f:
        notebook = json.load(f)

    # ----------------------------------------------------------------
    # Step 1: Find the Case Study 1 cell (the large cell 69 with the
    #         Mendez convergence case study) and insert AFTER it
    # ----------------------------------------------------------------
    insert_idx = None
    for i, cell in enumerate(notebook['cells']):
        if cell.get('cell_type') == 'markdown':
            source = ''.join(cell.get('source', []))
            if ('Case Study 1: Capital and Productivity' in source
                    and "What You've Learned" in source):
                insert_idx = i + 1
                break

    if insert_idx is None:
        # Fallback: look for the "5.12 Case Studies" heading
        for i, cell in enumerate(notebook['cells']):
            if cell.get('cell_type') == 'markdown':
                source = ''.join(cell.get('source', []))
                if '5.12 Case Studies' in source:
                    insert_idx = i + 1
                    break

    if insert_idx is None:
        # Last resort: insert before the final empty cell
        insert_idx = len(notebook['cells']) - 1
        print(f"WARNING: Could not find Case Study 1. Inserting at index {insert_idx}")

    original_count = len(notebook['cells'])
    print(f"Inserting {len(cells_to_add)} cells at index {insert_idx}")

    # ----------------------------------------------------------------
    # Step 2: Check if Case Study heading needs renumbering
    # ----------------------------------------------------------------
    # The existing heading is already "### Case Study 1:" so no rename needed.
    # But let's verify and rename if it says "### Case Study:" without a number.
    for i, cell in enumerate(notebook['cells']):
        if cell.get('cell_type') == 'markdown':
            source_lines = cell.get('source', [])
            for j, line in enumerate(source_lines):
                if '### Case Study:' in line and '### Case Study 1:' not in line:
                    source_lines[j] = line.replace('### Case Study:', '### Case Study 1:')
                    print(f"Renamed 'Case Study:' -> 'Case Study 1:' in cell {i}")

    # ----------------------------------------------------------------
    # Step 3: Insert new cells
    # ----------------------------------------------------------------
    for j, cell in enumerate(cells_to_add):
        notebook['cells'].insert(insert_idx + j, cell)

    # ----------------------------------------------------------------
    # Step 4: Write modified notebook
    # ----------------------------------------------------------------
    with open(NB_PATH, 'w', encoding='utf-8') as f:
        json.dump(notebook, f, indent=1, ensure_ascii=False)
        f.write('\n')

    print(f"Done! Notebook now has {len(notebook['cells'])} cells (was {original_count})")


if __name__ == '__main__':
    main()
