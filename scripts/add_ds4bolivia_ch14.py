#!/usr/bin/env python3
"""Add DS4Bolivia Case Study 2 to CH14 notebook."""

import json
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
NB_PATH = PROJECT_ROOT / 'notebooks_colab' / 'ch14_Regression_with_Indicator_Variables.ipynb'


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
### Case Study 2: Urban-Rural and Regional Divides in Bolivian Development

In previous chapters, we estimated satellite-development regressions treating all Bolivian municipalities identically. But Bolivia's nine departments span diverse geographies---from Andean highlands to Amazonian lowlands. In this case study, we apply Chapter 14's **indicator variable** techniques to model regional differences in development levels and in the satellite-development relationship.

**Research Question**: Do development levels and the NTL-development relationship differ across Bolivia's nine departments?

**Dataset:** DS4Bolivia

```python
import pandas as pd
url_bol = "https://raw.githubusercontent.com/quarcs-lab/ds4bolivia/master/ds4bolivia_v20250523.csv"
bol = pd.read_csv(url_bol)
```

**Key variables:** `mun` (municipality), `dep` (department), `imds` (Municipal Development Index, 0--100), `ln_NTLpc2017` (log nighttime lights per capita)"""),

# ---------- Task 1 ----------
make_md_cell("""\
#### Task 1: Create Indicators and Group Means (Guided)

**Objective**: Create department indicator variables and compare mean development across departments.

**Instructions**:
1. Load the DS4Bolivia dataset and select key variables
2. Use `pd.get_dummies(bol['dep'])` to create department indicators
3. Compute mean `imds` by department with `groupby('dep')['imds'].agg(['mean', 'count'])`
4. Which department has the highest mean IMDS? The lowest?

Run the code below to get started."""),

make_code_cell("""\
# Load DS4Bolivia dataset
url_bol = "https://raw.githubusercontent.com/quarcs-lab/ds4bolivia/master/ds4bolivia_v20250523.csv"
bol = pd.read_csv(url_bol)

# Select key variables
bol_key = bol[['mun', 'dep', 'imds', 'ln_NTLpc2017']].dropna().copy()

print("=" * 70)
print("DS4BOLIVIA: DEPARTMENT INDICATORS AND GROUP MEANS")
print("=" * 70)
print(f"Observations: {len(bol_key)} municipalities")
print(f"Departments: {bol_key['dep'].nunique()}")

# Create department indicator variables
dep_dummies = pd.get_dummies(bol_key['dep'])
print(f"\\nIndicator variables created: {list(dep_dummies.columns)}")

# Mean IMDS by department
print("\\n" + "-" * 70)
print("Mean IMDS by Department")
print("-" * 70)
dept_stats = bol_key.groupby('dep')['imds'].agg(['mean', 'count']).sort_values('mean', ascending=False)
print(dept_stats.round(2))

print(f"\\nHighest mean IMDS: {dept_stats['mean'].idxmax()} ({dept_stats['mean'].max():.2f})")
print(f"Lowest mean IMDS:  {dept_stats['mean'].idxmin()} ({dept_stats['mean'].min():.2f})")"""),

# ---------- Task 2 ----------
make_md_cell("""\
#### Task 2: Regression on Department Indicators (Guided)

**Objective**: Regress IMDS on department indicators to quantify regional development differences.

**Instructions**:
1. Estimate `imds ~ C(dep)` using statsmodels --- `C()` creates dummies automatically
2. Print the regression summary
3. Interpret: Each coefficient is the difference from the **base category** (the omitted department)
4. What is the base department? How much higher or lower is each department relative to the base?

```python
model_dep = ols('imds ~ C(dep)', data=bol_key).fit(cov_type='HC1')
print(model_dep.summary())
```"""),

make_code_cell("""\
# Your code here: Regression of IMDS on department indicators
#
# Steps:
# 1. Estimate model: imds ~ C(dep)
# 2. Print summary
# 3. Identify the base department and interpret coefficients
#
# model_dep = ols('imds ~ C(dep)', data=bol_key).fit(cov_type='HC1')
# print(model_dep.summary())
#
# print(f"\\nBase department: {sorted(bol_key['dep'].unique())[0]}")
# print(f"Intercept = mean IMDS for the base department: {model_dep.params['Intercept']:.2f}")"""),

# ---------- Key Concept 14.9 ----------
make_md_cell("""\
> **Key Concept 14.9: Geographic Indicator Variables**
>
> Department indicators capture **time-invariant regional characteristics** that affect development: altitude, climate, proximity to borders, historical infrastructure investments, and cultural factors. By including department dummies, we control for these systematic regional differences, allowing us to estimate the NTL-development relationship *within* departments rather than across them. The coefficient on NTL then reflects how NTL variation within a department predicts development variation within that department."""),

# ---------- Task 3 ----------
make_md_cell("""\
#### Task 3: Add NTL Control (Semi-guided)

**Objective**: Compare department coefficients with and without the NTL control variable.

**Instructions**:
1. Estimate `imds ~ C(dep) + ln_NTLpc2017`
2. Compare department coefficients with those from Task 2 (without NTL)
3. Do department differences shrink when NTL is added?
4. What does this tell us about whether NTL explains part of the regional gap?

**Hints**:
- If department coefficients shrink, it means part of the regional gap was due to differences in NTL intensity
- If they remain large, departments differ for reasons beyond what NTL captures"""),

make_code_cell("""\
# Your code here: Add NTL as a continuous control
#
# Steps:
# 1. Estimate: imds ~ C(dep) + ln_NTLpc2017
# 2. Compare department coefficients with Task 2 results
# 3. Interpret changes
#
# model_dep_ntl = ols('imds ~ C(dep) + ln_NTLpc2017', data=bol_key).fit(cov_type='HC1')
# print(model_dep_ntl.summary())
#
# print("\\nComparison: Do department coefficients shrink with NTL control?")
# print("If yes, NTL explains part of the regional development gap.")"""),

# ---------- Task 4 ----------
make_md_cell("""\
#### Task 4: Interaction Terms (Semi-guided)

**Objective**: Test whether the NTL-development slope differs across departments.

**Instructions**:
1. Estimate `imds ~ C(dep) * ln_NTLpc2017` (includes main effects + interactions)
2. Which interaction terms are significant?
3. Interpret: The NTL slope differs by department
4. In which departments does NTL predict development more or less strongly?

**Hints**:
- `C(dep) * ln_NTLpc2017` automatically includes both main effects and all interactions
- A positive interaction means the NTL slope is steeper in that department compared to the base
- A negative interaction means the NTL slope is flatter"""),

make_code_cell("""\
# Your code here: Interaction between department and NTL
#
# Steps:
# 1. Estimate: imds ~ C(dep) * ln_NTLpc2017
# 2. Examine interaction coefficients
# 3. Identify departments where NTL effect is stronger/weaker
#
# model_interact = ols('imds ~ C(dep) * ln_NTLpc2017', data=bol_key).fit(cov_type='HC1')
# print(model_interact.summary())
#
# print("\\nInterpretation:")
# print("  Significant interactions indicate the NTL slope differs by department.")
# print("  Base department NTL slope = coefficient on ln_NTLpc2017")
# print("  Other departments: base slope + interaction coefficient")"""),

# ---------- Key Concept 14.10 ----------
make_md_cell("""\
> **Key Concept 14.10: Heterogeneous Satellite Effects**
>
> Interaction terms between department indicators and NTL allow the **slope of the NTL-development relationship** to differ across regions. This is economically meaningful: in highly urbanized departments (like La Paz or Cochabamba), additional nighttime lights may signal commercial activity, while in rural highland departments (like Potosi), lights primarily reflect basic electrification. A significant interaction indicates that the *economic meaning* of satellite signals varies by geographic context."""),

# ---------- Task 5 ----------
make_md_cell("""\
#### Task 5: Joint F-Test for Department Effects (Independent)

**Objective**: Test the joint significance of all department indicators and all interaction terms.

**Instructions**:
1. Test joint significance of all department indicators using an F-test
2. Also test joint significance of all interaction terms
3. Are regional differences significant? Do NTL effects significantly vary across regions?

**Hints**:
- Use `model.f_test()` or compare restricted vs. unrestricted models
- For interaction terms, compare the model with interactions to the model without
- Report F-statistics and p-values for both tests"""),

make_code_cell("""\
# Your code here: Joint F-tests for department effects
#
# Steps:
# 1. F-test for joint significance of department indicators
# 2. F-test for joint significance of interaction terms
# 3. Compare models with and without regional effects
#
# Approach: Compare nested models using ANOVA
# from statsmodels.stats.anova import anova_lm
#
# model_base = ols('imds ~ ln_NTLpc2017', data=bol_key).fit()
# model_dep_only = ols('imds ~ C(dep) + ln_NTLpc2017', data=bol_key).fit()
# model_full = ols('imds ~ C(dep) * ln_NTLpc2017', data=bol_key).fit()
#
# print("F-test: Department indicators (comparing base vs dep_only)")
# print(anova_lm(model_base, model_dep_only))
#
# print("\\nF-test: Interaction terms (comparing dep_only vs full)")
# print(anova_lm(model_dep_only, model_full))"""),

# ---------- Task 6 ----------
make_md_cell("""\
#### Task 6: Regional Disparities Brief (Independent)

**Objective**: Write a 200--300 word brief on regional development disparities in Bolivia.

**Your brief should address**:
1. What are the main regional divides in Bolivian development?
2. How much do department indicators explain beyond NTL?
3. Does the satellite-development relationship differ across regions?
4. What are the policy implications for targeted regional interventions?

**Use evidence from your analysis**: Cite specific coefficients, R-squared values, and F-test results to support your arguments."""),

make_code_cell("""\
# Your code here: Additional analysis for the policy brief
#
# You might want to:
# 1. Create a summary table comparing R-squared across models
# 2. Visualize department means with confidence intervals
# 3. Plot separate NTL-IMDS regression lines by department
# 4. Calculate specific statistics to cite in your brief
#
# Example: Compare model fit
# print("MODEL COMPARISON")
# print(f"  NTL only:        R² = {model_base.rsquared:.4f}")
# print(f"  + Dept dummies:  R² = {model_dep_only.rsquared:.4f}")
# print(f"  + Interactions:  R² = {model_full.rsquared:.4f}")"""),

# ---------- What You've Learned ----------
make_md_cell("""\
#### What You've Learned from This Case Study

Through this analysis of regional development disparities in Bolivia, you have applied Chapter 14's indicator variable techniques to a real geospatial dataset:

- **Indicator variable creation**: Used `pd.get_dummies()` and `C()` to create department dummies
- **Department dummies in regression**: Quantified development differences across Bolivia's nine departments
- **Controlling for regional effects**: Compared models with and without department indicators to assess how much of the NTL-development relationship reflects regional composition
- **Interaction terms**: Tested whether the satellite-development slope differs across departments
- **Joint F-tests**: Evaluated the overall significance of department effects and interaction terms
- **Policy interpretation**: Connected statistical findings to regional development policy

**Connection to next chapter**: In Chapter 15, we explore *nonlinear* satellite-development relationships using log transformations, polynomials, and elasticities.

---

**Well done!** You've now analyzed both cross-country productivity data and Bolivian municipal development data using indicator variable techniques, demonstrating how geographic dummies capture systematic regional differences and how interactions reveal heterogeneous effects."""),

]


def main():
    with open(NB_PATH, 'r', encoding='utf-8') as f:
        notebook = json.load(f)

    # Step 1: Rename existing "### Case Study:" to "### Case Study 1:" in cell 43
    renamed = False
    for i, cell in enumerate(notebook['cells']):
        if cell.get('cell_type') == 'markdown':
            source = ''.join(cell.get('source', []))
            if '### Case Study: Regional Indicator Variables' in source:
                # Rename header
                new_source = source.replace(
                    '### Case Study: Regional Indicator Variables',
                    '### Case Study 1: Regional Indicator Variables'
                )
                lines = new_source.split('\n')
                cell['source'] = [line + '\n' if j < len(lines) - 1 else line
                                  for j, line in enumerate(lines)]
                renamed = True
                print(f"Renamed Case Study header in cell {i}")
                break

    if not renamed:
        # Check if it already has "Case Study 1:" or another format
        for i, cell in enumerate(notebook['cells']):
            if cell.get('cell_type') == 'markdown':
                source = ''.join(cell.get('source', []))
                if '## Case Studies' in source and '### Case Study' in source:
                    if '### Case Study 1:' not in source:
                        new_source = source.replace(
                            '### Case Study:',
                            '### Case Study 1:'
                        )
                        lines = new_source.split('\n')
                        cell['source'] = [line + '\n' if j < len(lines) - 1 else line
                                          for j, line in enumerate(lines)]
                        renamed = True
                        print(f"Renamed Case Study header in cell {i} (fallback)")
                    else:
                        renamed = True
                        print(f"Case Study 1 header already exists in cell {i}")
                    break

    if not renamed:
        print("WARNING: Could not find Case Study header to rename")

    # Step 2: Find insertion point -- after the "What You've Learned" closing
    # of Case Study 1, which is the last line of the Case Studies cell (cell 43)
    insert_idx = None
    for i, cell in enumerate(notebook['cells']):
        if cell.get('cell_type') == 'markdown':
            source = ''.join(cell.get('source', []))
            if ("What You've Learned" in source and
                "indicator variable techniques" in source and
                "cross-country data" in source):
                insert_idx = i + 1
                break

    if insert_idx is None:
        # Fallback: look for the Case Studies cell and insert after it
        for i, cell in enumerate(notebook['cells']):
            if cell.get('cell_type') == 'markdown':
                source = ''.join(cell.get('source', []))
                if '## Case Studies' in source and 'Regional Indicator Variables' in source:
                    insert_idx = i + 1
                    break

    if insert_idx is None:
        # Last resort: insert before the final empty cell
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

    print(f"Done! Notebook now has {len(notebook['cells'])} cells (was {len(notebook['cells']) - len(cells_to_add)})")


if __name__ == '__main__':
    main()
