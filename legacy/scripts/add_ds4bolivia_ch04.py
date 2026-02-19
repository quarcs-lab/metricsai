#!/usr/bin/env python3
"""Add DS4Bolivia Case Study 2 to CH04 notebook."""

import json
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
NB_PATH = PROJECT_ROOT / 'notebooks_colab' / 'ch04_Statistical_Inference_for_the_Mean.ipynb'


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
### Case Study 2: Is Bolivia's Development Equal? Testing Differences Across Departments

**Research Question**: Are there statistically significant differences in development levels across Bolivia's nine departments?

In Chapter 1, we introduced the DS4Bolivia project and explored satellite-development relationships across Bolivia's 339 municipalities. In this case study, we apply Chapter 4's statistical inference tools—confidence intervals and hypothesis tests—to test whether development levels differ significantly across Bolivia's departments.

**The Data**: Cross-sectional dataset covering 339 Bolivian municipalities from the [DS4Bolivia Project](https://github.com/quarcs-lab/ds4bolivia), including:
- **Development outcomes**: Municipal Sustainable Development Index (IMDS, 0-100 composite)
- **Satellite data**: Log nighttime lights per capita (2017)
- **Demographics**: Population (2017), municipality and department names

**Your Task**: Use confidence intervals, one-sample tests, two-sample tests, and one-sided tests to evaluate whether Bolivia's departments differ significantly in development—and whether those differences are large enough to matter for policy."""),

# ---------- Load Data ----------
make_md_cell("""\
#### Load the DS4Bolivia Data

Let's load the DS4Bolivia dataset and prepare the key variables for statistical inference."""),

make_code_cell("""\
# Load the DS4Bolivia dataset
url_bol = "https://raw.githubusercontent.com/quarcs-lab/ds4bolivia/master/ds4bolivia_v20250523.csv"
bol = pd.read_csv(url_bol)

# Select key variables for this case study
key_vars = ['mun', 'dep', 'imds', 'ln_NTLpc2017', 'pop2017']
bol_key = bol[key_vars].dropna().copy()

print("=" * 70)
print("DS4BOLIVIA DATASET — STATISTICAL INFERENCE CASE STUDY")
print("=" * 70)
print(f"Municipalities: {len(bol_key)}")
print(f"Departments:    {bol_key['dep'].nunique()}")
print(f"\\nIMDS summary:")
print(bol_key['imds'].describe().round(2))
print(f"\\nMunicipalities per department:")
print(bol_key['dep'].value_counts().sort_index())"""),

# ---------- Task 1: Confidence Interval for Mean IMDS (Guided) ----------
make_md_cell("""\
#### Task 1: Confidence Interval for Mean IMDS (Guided)

**Learning Goal**: Apply Section 4.3 methods to calculate and interpret a confidence interval for a population mean.

**Economic Question**: "What is the true average development level across all Bolivian municipalities?"

**Instructions**:
1. Calculate the sample mean and standard error of `imds`
2. Construct a 95% confidence interval using `scipy.stats.t.interval()`
3. Print the sample mean, standard error, and CI bounds
4. Interpret the result: "We are 95% confident that the true mean municipal development index lies between X and Y."

**Apply what you learned in Section 4.3**: The formula is $\\bar{x} \\pm t_{\\alpha/2} \\times SE$, where $SE = s/\\sqrt{n}$."""),

make_code_cell("""\
# Your code here: 95% Confidence Interval for national mean IMDS
from scipy import stats

# Calculate sample statistics
n = len(bol_key['imds'])
x_bar = bol_key['imds'].mean()
se = bol_key['imds'].std() / np.sqrt(n)

# 95% confidence interval using t-distribution
ci_low, ci_high = stats.t.interval(0.95, df=n-1, loc=x_bar, scale=se)

print("=" * 70)
print("95% CONFIDENCE INTERVAL FOR MEAN IMDS")
print("=" * 70)
print(f"Sample size (n):       {n}")
print(f"Sample mean:           {x_bar:.4f}")
print(f"Standard error:        {se:.4f}")
print(f"95% CI:                [{ci_low:.4f}, {ci_high:.4f}]")
print(f"\\nInterpretation: We are 95% confident that the true mean")
print(f"municipal development index lies between {ci_low:.2f} and {ci_high:.2f}.")"""),

# ---------- Task 2: Hypothesis Test: National Target (Guided) ----------
make_md_cell("""\
#### Task 2: Hypothesis Test — National Development Target (Guided)

**Learning Goal**: Apply Section 4.4 (two-sided test) to test a hypothesis about a population mean.

**Economic Question**: "Is the average municipality at the midpoint of the development scale?"

A natural benchmark for the IMDS (which ranges from 0 to 100) is the midpoint of 50. If Bolivia's municipalities were, on average, at this midpoint, we would expect $\\mu_{IMDS} = 50$.

**Instructions**:
1. State the hypotheses: $H_0: \\mu = 50$ vs $H_1: \\mu \\neq 50$
2. Use `scipy.stats.ttest_1samp()` to conduct the test
3. Report the t-statistic and p-value
4. State your conclusion at $\\alpha = 0.05$
5. Discuss: Is the average municipality at the midpoint of the development scale?"""),

make_code_cell("""\
# Your code here: One-sample t-test — is mean IMDS = 50?

# Hypothesis test: H0: mu = 50 vs H1: mu != 50
t_stat, p_value = stats.ttest_1samp(bol_key['imds'], popmean=50)

print("=" * 70)
print("HYPOTHESIS TEST: IS MEAN IMDS = 50?")
print("=" * 70)
print(f"H₀: μ = 50  vs  H₁: μ ≠ 50")
print(f"\\nSample mean:   {bol_key['imds'].mean():.4f}")
print(f"t-statistic:   {t_stat:.4f}")
print(f"p-value:       {p_value:.6f}")
print(f"\\nConclusion at α = 0.05:")
if p_value < 0.05:
    print(f"  Reject H₀ (p = {p_value:.6f} < 0.05)")
    print(f"  The average IMDS is significantly different from 50.")
else:
    print(f"  Fail to reject H₀ (p = {p_value:.6f} ≥ 0.05)")
    print(f"  No significant evidence that mean IMDS differs from 50.")"""),

# ---------- Key Concept 4.12 ----------
make_md_cell("""\
> **Key Concept 4.12: Statistical Significance in Development**
>
> A statistically significant difference between departments does not automatically imply a **policy-relevant** gap. With 339 municipalities providing large sample sizes, even small differences can achieve statistical significance. Policy makers must evaluate the **magnitude** of differences alongside p-values. A 2-point difference in IMDS may be statistically significant but practically negligible for resource allocation decisions."""),

# ---------- Task 3: Department-Level Inference (Semi-guided) ----------
make_md_cell("""\
#### Task 3: Department-Level Inference (Semi-guided)

**Learning Goal**: Apply confidence intervals to compare subgroups.

**Economic Question**: "Which departments have significantly different development levels from one another?"

**Instructions**:
1. Calculate the 95% confidence interval for mean `imds` in each of Bolivia's 9 departments
2. Create a **forest plot** (horizontal error bars) showing the CI for each department
3. Identify which departments' CIs overlap (suggesting no significant difference) and which don't
4. Discuss what the pattern reveals about regional inequality

**Hint**: Use `groupby('dep')` to calculate department-level statistics, then `plt.errorbar()` or `plt.barh()` with error bars for the forest plot."""),

make_code_cell("""\
# Your code here: Department-level 95% CIs and forest plot

# Calculate department-level statistics
dept_stats = bol_key.groupby('dep')['imds'].agg(['mean', 'std', 'count']).sort_values('mean')
dept_stats['se'] = dept_stats['std'] / np.sqrt(dept_stats['count'])
dept_stats['ci_low'] = dept_stats['mean'] - 1.96 * dept_stats['se']
dept_stats['ci_high'] = dept_stats['mean'] + 1.96 * dept_stats['se']

print("=" * 70)
print("95% CONFIDENCE INTERVALS FOR MEAN IMDS BY DEPARTMENT")
print("=" * 70)
print(dept_stats[['mean', 'se', 'ci_low', 'ci_high', 'count']].round(2).to_string())

# Forest plot
fig, ax = plt.subplots(figsize=(10, 6))
departments = dept_stats.index
y_pos = range(len(departments))
ax.errorbar(dept_stats['mean'], y_pos,
            xerr=1.96 * dept_stats['se'],
            fmt='o', color='navy', capsize=5, capthick=1.5, markersize=6)
ax.set_yticks(y_pos)
ax.set_yticklabels(departments)
ax.set_xlabel('Mean IMDS (with 95% CI)')
ax.set_title('Forest Plot: Municipal Development by Department')
ax.axvline(x=bol_key['imds'].mean(), color='red', linestyle='--', alpha=0.5, label='National mean')
ax.legend()
ax.grid(axis='x', alpha=0.3)
plt.tight_layout()
plt.show()"""),

# ---------- Task 4: One-Sided Test (Semi-guided) ----------
make_md_cell("""\
#### Task 4: One-Sided Test — Is the Capital Department More Developed? (Semi-guided)

**Learning Goal**: Apply Section 4.6 (one-sided tests) to a directional hypothesis.

**Economic Question**: "Is La Paz department's mean IMDS significantly greater than the national mean?"

**Instructions**:
1. Extract IMDS values for La Paz department
2. Test $H_0: \\mu_{LP} \\leq \\mu_{national}$ vs $H_1: \\mu_{LP} > \\mu_{national}$ using a one-sided t-test
3. Calculate the one-sided p-value (divide the two-sided p-value by 2, checking direction)
4. Report and interpret the result at $\\alpha = 0.05$
5. Discuss: Is the capital department significantly more developed?

**Hint**: Use `scipy.stats.ttest_1samp()` with the national mean as the test value, then adjust for a one-sided test."""),

make_code_cell("""\
# Your code here: One-sided t-test for La Paz department

# Extract La Paz IMDS values
la_paz = bol_key[bol_key['dep'] == 'La Paz']['imds']
national_mean = bol_key['imds'].mean()

# Two-sided test first
t_stat_lp, p_two = stats.ttest_1samp(la_paz, popmean=national_mean)

# One-sided p-value: H1: mu_LP > national_mean
# If t > 0, one-sided p = p_two / 2; if t < 0, one-sided p = 1 - p_two / 2
p_one = p_two / 2 if t_stat_lp > 0 else 1 - p_two / 2

print("=" * 70)
print("ONE-SIDED TEST: LA PAZ > NATIONAL MEAN?")
print("=" * 70)
print(f"H₀: μ_LaPaz ≤ {national_mean:.2f}  vs  H₁: μ_LaPaz > {national_mean:.2f}")
print(f"\\nLa Paz municipalities:  {len(la_paz)}")
print(f"La Paz mean IMDS:       {la_paz.mean():.4f}")
print(f"National mean IMDS:     {national_mean:.4f}")
print(f"t-statistic:            {t_stat_lp:.4f}")
print(f"One-sided p-value:      {p_one:.6f}")
print(f"\\nConclusion at α = 0.05:")
if p_one < 0.05:
    print(f"  Reject H₀ (p = {p_one:.6f} < 0.05)")
    print(f"  La Paz's mean IMDS is significantly greater than the national mean.")
else:
    print(f"  Fail to reject H₀ (p = {p_one:.6f} ≥ 0.05)")
    print(f"  No significant evidence that La Paz exceeds the national mean.")"""),

# ---------- Key Concept 4.13 ----------
make_md_cell("""\
> **Key Concept 4.13: Subnational Inference Challenges**
>
> When testing hypotheses about departmental means, each department contains a different number of municipalities (ranging from ~10 to ~50+). Departments with fewer municipalities have **wider confidence intervals** and less statistical power. This means we may fail to detect real differences for smaller departments—not because the differences don't exist, but because we lack sufficient data to establish them conclusively."""),

# ---------- Task 5: Comparing Two Departments (Independent) ----------
make_md_cell("""\
#### Task 5: Comparing Two Departments (Independent)

**Learning Goal**: Apply two-sample t-tests to compare group means.

**Economic Question**: "Is the development gap between the most and least developed departments statistically significant?"

**Instructions**:
1. Identify the departments with the highest and lowest mean IMDS (from Task 3 results)
2. Use `scipy.stats.ttest_ind()` to perform a two-sample t-test comparing these departments
3. Report the t-statistic and p-value
4. Discuss both **statistical significance** (p-value) and **practical significance** (magnitude of the gap)
5. What does this tell us about regional inequality in Bolivia?"""),

make_code_cell("""\
# Your code here: Two-sample t-test — highest vs lowest IMDS department

# Identify highest and lowest departments
dept_means = bol_key.groupby('dep')['imds'].mean()
top_dept = dept_means.idxmax()
bot_dept = dept_means.idxmin()

# Extract IMDS values for each
top_values = bol_key[bol_key['dep'] == top_dept]['imds']
bot_values = bol_key[bol_key['dep'] == bot_dept]['imds']

# Two-sample t-test
t_stat_2s, p_value_2s = stats.ttest_ind(top_values, bot_values)

print("=" * 70)
print(f"TWO-SAMPLE T-TEST: {top_dept.upper()} vs {bot_dept.upper()}")
print("=" * 70)
print(f"\\nHighest IMDS department: {top_dept}")
print(f"  Mean IMDS:   {top_values.mean():.4f}")
print(f"  N:           {len(top_values)}")
print(f"\\nLowest IMDS department:  {bot_dept}")
print(f"  Mean IMDS:   {bot_values.mean():.4f}")
print(f"  N:           {len(bot_values)}")
print(f"\\nDifference in means:    {top_values.mean() - bot_values.mean():.4f}")
print(f"t-statistic:            {t_stat_2s:.4f}")
print(f"p-value:                {p_value_2s:.6f}")
print(f"\\nConclusion at α = 0.05:")
if p_value_2s < 0.05:
    print(f"  Reject H₀ (p = {p_value_2s:.6f} < 0.05)")
    print(f"  The development gap of {top_values.mean() - bot_values.mean():.2f} points is statistically significant.")
else:
    print(f"  Fail to reject H₀ (p = {p_value_2s:.6f} ≥ 0.05)")
    print(f"  No significant evidence of a development gap.")
print(f"\\nPractical significance: A gap of {top_values.mean() - bot_values.mean():.2f} points on a 0-100 scale")
print(f"represents a {'substantial' if abs(top_values.mean() - bot_values.mean()) > 10 else 'modest'} difference in development outcomes.")"""),

# ---------- Task 6: Policy Brief (Independent) ----------
make_md_cell("""\
#### Task 6: Policy Brief on Regional Inequality (Independent)

**Objective**: Write a 200-300 word policy brief summarizing your statistical findings.

**Your brief should address**:
1. **Are departmental differences statistically significant?** Summarize results from Tasks 3-5.
2. **Which departments need the most attention?** Use the forest plot and CI analysis to identify lagging regions.
3. **How confident are we in these conclusions?** Discuss the confidence levels and what the CIs tell us.
4. **What are the limitations of these tests?** Consider sample sizes, assumptions, and what the tests cannot tell us.

**Format**: Write your brief in the markdown cell below. Support your arguments with specific numbers from your analysis (means, CIs, p-values).

**Tip**: Remember Key Concepts 4.12 and 4.13—distinguish between statistical significance and policy relevance, and consider how unequal sample sizes affect your conclusions."""),

make_code_cell("""\
# Your code here: Additional analysis to support your policy brief
#
# Suggestions:
# 1. Create a summary table of all department CIs and test results
# 2. Calculate effect sizes (Cohen's d) for the two-sample comparison
# 3. Visualize the national IMDS distribution with department means marked

# Example: Summary statistics for the policy brief
print("=" * 70)
print("SUMMARY TABLE FOR POLICY BRIEF")
print("=" * 70)
dept_summary = bol_key.groupby('dep')['imds'].agg(['mean', 'std', 'count']).sort_values('mean', ascending=False)
dept_summary['se'] = dept_summary['std'] / np.sqrt(dept_summary['count'])
dept_summary['ci_95'] = dept_summary.apply(
    lambda r: f"[{r['mean'] - 1.96*r['se']:.1f}, {r['mean'] + 1.96*r['se']:.1f}]", axis=1)
print(dept_summary[['mean', 'std', 'count', 'ci_95']].round(2).to_string())"""),

# ---------- What You've Learned ----------
make_md_cell("""\
#### What You've Learned from This Case Study

Through this analysis of subnational development in Bolivia, you've applied the full Chapter 4 statistical inference toolkit:

- **Confidence intervals** for mean development levels
- **One-sample and two-sample hypothesis tests** to evaluate development benchmarks and compare groups
- **One-sided tests** for directional hypotheses about specific departments
- **Forest plots** for comparing group CIs visually
- **Statistical vs practical significance** in a policy context
- **Critical thinking** about sample size, statistical power, and inference limitations

**Connection to research**: The DS4Bolivia project uses these same statistical tools to evaluate whether satellite-predicted development indicators are significantly different from survey-based measures, providing evidence for the reliability of remote sensing approaches to SDG monitoring.

**Looking ahead**: In Chapter 5, we'll move beyond testing means to exploring *bivariate relationships*—how nighttime lights relate to specific development outcomes across Bolivia's municipalities.

---

**Well done!** You've now tested development hypotheses for both cross-country convergence and Bolivian regional inequality using the tools of statistical inference."""),

]


def main():
    with open(NB_PATH, 'r', encoding='utf-8') as f:
        notebook = json.load(f)

    # --------------------------------------------------------
    # Step 1: Rename existing "## Case Study:" to "## Case Study 1:"
    # --------------------------------------------------------
    renamed = False
    for i, cell in enumerate(notebook['cells']):
        if cell.get('cell_type') == 'markdown':
            source = ''.join(cell.get('source', []))
            if '## Case Study:' in source and 'Case Study 1:' not in source and 'Case Study 2:' not in source:
                # Rename to Case Study 1
                new_source = source.replace('## Case Study:', '## Case Study 1:')
                lines = new_source.split('\n')
                cell['source'] = [line + '\n' if j < len(lines) - 1 else line
                                  for j, line in enumerate(lines)]
                print(f"Renamed 'Case Study:' to 'Case Study 1:' in cell {i}")
                renamed = True
                break

    if not renamed:
        print("INFO: No '## Case Study:' header found to rename (may already be numbered)")

    # --------------------------------------------------------
    # Step 2: Find insertion point — after "What You've Learned"
    #         closing of Case Study 1
    # --------------------------------------------------------
    insert_idx = None
    for i, cell in enumerate(notebook['cells']):
        if cell.get('cell_type') == 'markdown':
            source = ''.join(cell.get('source', []))
            if "What You've Learned" in source and 'convergence' in source.lower():
                insert_idx = i + 1
                break

    if insert_idx is None:
        # Broader fallback: find "What You've Learned" that mentions Chapter 4
        for i, cell in enumerate(notebook['cells']):
            if cell.get('cell_type') == 'markdown':
                source = ''.join(cell.get('source', []))
                if "What You've Learned" in source and 'chapter 4' in source.lower():
                    insert_idx = i + 1
                    break

    if insert_idx is None:
        # Last resort: insert before the last empty cell
        insert_idx = len(notebook['cells']) - 1
        print(f"WARNING: Could not find Case Study 1 closing. Inserting at index {insert_idx}")
    else:
        print(f"Found Case Study 1 closing at cell {insert_idx - 1}")

    print(f"Inserting {len(cells_to_add)} cells at index {insert_idx}")

    # --------------------------------------------------------
    # Step 3: Insert Case Study 2 cells
    # --------------------------------------------------------
    for j, cell in enumerate(cells_to_add):
        notebook['cells'].insert(insert_idx + j, cell)

    # --------------------------------------------------------
    # Step 4: Write modified notebook
    # --------------------------------------------------------
    original_count = len(notebook['cells']) - len(cells_to_add)
    with open(NB_PATH, 'w', encoding='utf-8') as f:
        json.dump(notebook, f, indent=1, ensure_ascii=False)
        f.write('\n')

    print(f"Done! Notebook now has {len(notebook['cells'])} cells (was {original_count})")


if __name__ == '__main__':
    main()
