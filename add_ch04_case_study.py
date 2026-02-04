#!/usr/bin/env python3
"""
Add Section 4.8 Case Study to Chapter 4
Inserts case study content at position 49 (after Section 4.7, before Key Takeaways)
"""

import json

# Define all case study cells
case_study_cells = [
    # Cell 1: Section title and research question
    {
        'cell_type': 'markdown',
        'metadata': {},
        'source': [
            '## 4.8 Case Study: Statistical Inference for Labor Productivity\n',
            '\n',
            '**Research Question:** "Has global labor productivity changed significantly over time, and do productivity levels differ significantly across regions?"\n',
            '\n',
            'This case study applies all the statistical inference methods from Chapter 4 to analyze real economic data on labor productivity across 108 countries over 25 years (1990-2014). You\'ll practice:\n',
            '\n',
            '- Constructing and interpreting **confidence intervals** for population means\n',
            '- Conducting **two-sided hypothesis tests** to compare time periods\n',
            '- Performing **one-sided directional tests** for benchmark comparisons\n',
            '- Applying **proportions inference** to binary economic outcomes\n',
            '- Comparing productivity levels across **regional subgroups**\n',
            '- Interpreting results in economic context (development economics, convergence theory)\n',
            '\n',
            'The Mendez convergence clubs dataset provides panel data on labor productivity, GDP, capital, human capital, and total factor productivity for 108 countries from 1990 to 2014.\n'
        ]
    },

    # Cell 2: Economic context
    {
        'cell_type': 'markdown',
        'metadata': {},
        'source': [
            '### Economic Context: Testing Convergence Hypotheses\n',
            '\n',
            'In development economics, the **convergence hypothesis** suggests that poorer countries should grow faster than richer ones, leading to a narrowing of productivity gaps over time. Statistical inference allows us to test whether observed changes in productivity are:\n',
            '\n',
            '- **Statistically significant** (unlikely due to random sampling variation)\n',
            '- **Economically meaningful** (large enough to matter for policy)\n',
            '\n',
            'By applying Chapter 4\'s methods to this dataset, you\'ll answer questions like:\n',
            '\n',
            '1. Has mean global productivity increased significantly from 1990 to 2014?\n',
            '2. Are regional productivity gaps (e.g., Africa vs. Europe) statistically significant?\n',
            '3. What proportion of countries experienced positive productivity growth?\n',
            '4. Can we reject specific hypotheses about productivity benchmarks?\n',
            '\n',
            'These are real questions that economists and policymakers care about when designing development strategies.\n'
        ]
    },

    # Cell 3: Key Concept Box 1
    {
        'cell_type': 'markdown',
        'metadata': {},
        'source': [
            '> **Key Concept: Why Statistical Inference Matters in Economics**\n',
            '>\n',
            '> When analyzing economic data, we rarely observe entire populations. Instead, we work with **samples** (like 108 countries from all countries in the world, or 25 years from a longer historical period). Statistical inference lets us:\n',
            '>\n',
            '> 1. **Quantify uncertainty** - Confidence intervals tell us the range of plausible values for population parameters\n',
            '> 2. **Test theories** - Hypothesis tests evaluate whether data support or contradict economic theories\n',
            '> 3. **Compare groups** - We can determine if differences between regions/periods are real or just noise\n',
            '> 4. **Inform policy** - Statistical significance helps separate meaningful patterns from random fluctuations\n',
            '>\n',
            '> Without inference methods, we couldn\'t distinguish between:\n',
            '> - A real productivity increase vs. random year-to-year variation\n',
            '> - Genuine regional gaps vs. sampling artifacts\n',
            '> - Policy-relevant changes vs. statistical noise\n'
        ]
    },

    # Cell 4: Data loading section
    {
        'cell_type': 'code',
        'metadata': {},
        'execution_count': None,
        'outputs': [],
        'source': [
            '# Load convergence clubs dataset\n',
            'url = "https://raw.githubusercontent.com/quarcs-lab/mendez2020-convergence-clubs-code-data/master/assets/dat.csv"\n',
            'df = pd.read_csv(url)\n',
            '\n',
            '# Set multi-index (country, year)\n',
            'df = df.set_index([\'country\', \'year\'])\n',
            '\n',
            '# Display dataset information\n',
            'print("Dataset Overview:")\n',
            'print(f"Total observations: {len(df):,}")\n',
            'print(f"Countries: {df.index.get_level_values(\'country\').nunique()}")\n',
            'print(f"Years: {df.index.get_level_values(\'year\').min()}-{df.index.get_level_values(\'year\').max()}")\n',
            'print(f"\\nVariables: {list(df.columns)}")\n',
            '\n',
            '# Extract labor productivity for key years\n',
            'lp_1990 = df.loc[df.index.get_level_values(\'year\') == 1990, \'lp\']\n',
            'lp_2014 = df.loc[df.index.get_level_values(\'year\') == 2014, \'lp\']\n',
            '\n',
            'print(f"\\nLabor productivity samples:")\n',
            'print(f"1990: n={len(lp_1990)}, mean=${lp_1990.mean()/1000:.1f}k, std=${lp_1990.std()/1000:.1f}k")\n',
            'print(f"2014: n={len(lp_2014)}, mean=${lp_2014.mean()/1000:.1f}k, std=${lp_2014.std()/1000:.1f}k")\n'
        ]
    },

    # Cell 5: Instructions
    {
        'cell_type': 'markdown',
        'metadata': {},
        'source': [
            '### How to Use These Tasks\n',
            '\n',
            '**Task structure:** The 6 tasks below progress from **guided** (fill-in-the-blank code) to **independent** (design your own analysis).\n',
            '\n',
            '**Working approach:**\n',
            '\n',
            '1. **Read the task description** - Understand the economic question and learning goal\n',
            '2. **Study the code template** - Early tasks provide partial code with blanks (`_____`)\n',
            '3. **Insert a new code cell** below each task\n',
            '4. **Complete the code** - Fill in blanks or write from scratch (depending on task level)\n',
            '5. **Run and interpret** - Execute your code and interpret results economically\n',
            '6. **Check your understanding** - Does your answer make economic sense?\n',
            '\n',
            '**Tips:**\n',
            '\n',
            '- Reference Section 4.1-4.7 for formulas and methods\n',
            '- Use `scipy.stats` functions: `t.ppf()`, `ttest_ind()`, `ttest_1samp()`\n',
            '- Always interpret p-values: "We reject/fail to reject H₀ at α=0.05 because..."\n',
            '- Connect statistical results to economic meaning: "This suggests that..."\n',
            '\n',
            '**Progressive difficulty:**\n',
            '\n',
            '- **Tasks 1-2:** GUIDED (fill 4-8 blanks in provided code)\n',
            '- **Tasks 3-4:** SEMI-GUIDED (complete partial structure)\n',
            '- **Tasks 5-6:** INDEPENDENT (design full implementation)\n'
        ]
    },

    # Cell 6: Task 1 description
    {
        'cell_type': 'markdown',
        'metadata': {},
        'source': [
            '### Task 1: Confidence Intervals for Mean Productivity (GUIDED)\n',
            '\n',
            '**Learning Goal:** Apply Section 4.3 methods to calculate and interpret confidence intervals\n',
            '\n',
            '**Economic Question:** "Can we be 95% confident about the range of global mean labor productivity in 2014?"\n',
            '\n',
            '**Your task:**\n',
            '\n',
            '1. Calculate a 95% confidence interval for mean productivity in 2014\n',
            '2. Calculate a 99% confidence interval for comparison\n',
            '3. Interpret the difference in interval widths\n',
            '4. Compare with a 95% CI for 1990 data\n',
            '\n',
            '**Code template (fill in the 6 blanks):**\n',
            '\n',
            '```python\n',
            'from scipy import stats\n',
            '\n',
            '# 2014 data: Calculate 95% CI\n',
            'n_2014 = len(lp_2014)\n',
            'mean_2014 = _____  # Calculate sample mean\n',
            'std_2014 = _____   # Calculate sample standard deviation\n',
            'se_2014 = std_2014 / np.sqrt(n_2014)\n',
            '\n',
            '# Get t-critical value for 95% CI (two-tailed, df = n-1)\n',
            'alpha_95 = 0.05\n',
            't_crit_95 = stats.t.ppf(1 - alpha_95/2, df=_____)\n',
            '\n',
            '# Calculate margin of error and CI bounds\n',
            'me_95 = t_crit_95 * se_2014\n',
            'ci_95_lower = _____\n',
            'ci_95_upper = _____\n',
            '\n',
            'print(f"2014 Labor Productivity:")\n',
            'print(f"Sample mean: ${mean_2014:,.0f}")\n',
            'print(f"95% CI: [${ci_95_lower:,.0f}, ${ci_95_upper:,.0f}]")\n',
            'print(f"Margin of error: ${me_95:,.0f}")\n',
            '\n',
            '# Calculate 99% CI for comparison\n',
            'alpha_99 = 0.01\n',
            't_crit_99 = stats.t.ppf(1 - alpha_99/2, df=n_2014-1)\n',
            'me_99 = t_crit_99 * se_2014\n',
            'ci_99_lower = mean_2014 - me_99\n',
            'ci_99_upper = mean_2014 + me_99\n',
            '\n',
            'print(f"\\n99% CI: [${ci_99_lower:,.0f}, ${ci_99_upper:,.0f}]")\n',
            'print(f"Margin of error: ${me_99:,.0f}")\n',
            'print(f"\\nInterpretation: The 99% CI is _____ than the 95% CI")  # Fill in: "wider" or "narrower"\n',
            'print(f"because we need more certainty, which requires a larger interval.")\n',
            '\n',
            '# Compare with 1990\n',
            'mean_1990 = lp_1990.mean()\n',
            'std_1990 = lp_1990.std()\n',
            'se_1990 = std_1990 / np.sqrt(len(lp_1990))\n',
            'me_1990 = stats.t.ppf(0.975, df=len(lp_1990)-1) * se_1990\n',
            '\n',
            'print(f"\\n1990 mean: ${mean_1990:,.0f}, 95% CI width: ${2*me_1990:,.0f}")\n',
            'print(f"2014 mean: ${mean_2014:,.0f}, 95% CI width: ${2*me_95:,.0f}")\n',
            '```\n',
            '\n',
            '**Questions to consider:**\n',
            '\n',
            '- Why is the 99% CI wider than the 95% CI?\n',
            '- Did the mean productivity increase from 1990 to 2014?\n',
            '- Which year has more variability in productivity across countries?\n'
        ]
    },

    # Cell 7: Task 2 description
    {
        'cell_type': 'markdown',
        'metadata': {},
        'source': [
            '### Task 2: Testing Productivity Change Over Time (SEMI-GUIDED)\n',
            '\n',
            '**Learning Goal:** Apply Section 4.4 (two-sided tests) to compare time periods\n',
            '\n',
            '**Economic Question:** "Has global mean labor productivity changed significantly from 1990 to 2014?"\n',
            '\n',
            '**Your task:**\n',
            '\n',
            '1. State null and alternative hypotheses\n',
            '2. Conduct a two-sample t-test (independent samples)\n',
            '3. Calculate the test statistic manually\n',
            '4. Compare with `scipy.stats.ttest_ind()` result\n',
            '5. Interpret the p-value at α = 0.05\n',
            '\n',
            '**Code template (fill in the 8 blanks):**\n',
            '\n',
            '```python\n',
            '# State hypotheses\n',
            'print("H₀: μ₁₉₉₀ = μ₂₀₁₄  (no change in mean productivity)")\n',
            'print("Hₐ: μ₁₉₉₀ ≠ μ₂₀₁₄  (mean productivity changed)")\n',
            'print(f"Significance level: α = 0.05\\n")\n',
            '\n',
            '# Manual calculation\n',
            'mean_1990 = lp_1990.mean()\n',
            'mean_2014 = lp_2014.mean()\n',
            'se_1990 = lp_1990.std() / np.sqrt(len(lp_1990))\n',
            'se_2014 = lp_2014.std() / np.sqrt(len(lp_2014))\n',
            '\n',
            '# Calculate pooled standard error for difference in means\n',
            'se_diff = np.sqrt(_____**2 + _____**2)  # Fill in: se_1990 and se_2014\n',
            '\n',
            '# Calculate t-statistic\n',
            't_stat = (_____ - _____) / se_diff  # Fill in: mean_2014 and mean_1990\n',
            '\n',
            '# Degrees of freedom (Welch approximation)\n',
            'n1, n2 = len(lp_1990), len(lp_2014)\n',
            's1, s2 = lp_1990.std(), lp_2014.std()\n',
            'df = ((s1**2/n1 + s2**2/n2)**2) / ((s1**2/n1)**2/(n1-1) + (s2**2/n2)**2/(n2-1))\n',
            '\n',
            '# Calculate two-sided p-value\n',
            'p_value_manual = 2 * (1 - stats.t.cdf(abs(t_stat), df=df))\n',
            '\n',
            'print(f"Manual calculation:")\n',
            'print(f"Difference in means: ${mean_2014 - mean_1990:,.0f}")\n',
            'print(f"SE of difference: ${se_diff:,.0f}")\n',
            'print(f"t-statistic: {t_stat:.3f}")\n',
            'print(f"Degrees of freedom: {df:.1f}")\n',
            'print(f"p-value (two-sided): {p_value_manual:.4f}\\n")\n',
            '\n',
            '# Verify with scipy\n',
            't_stat_scipy, p_value_scipy = stats.ttest_ind(_____, _____, equal_var=False)  # Fill in: lp_2014, lp_1990\n',
            'print(f"scipy.stats.ttest_ind() result:")\n',
            'print(f"t-statistic: {t_stat_scipy:.3f}")\n',
            'print(f"p-value: {p_value_scipy:.4f}\\n")\n',
            '\n',
            '# Decision\n',
            'if p_value_scipy < 0.05:\n',
            '    print(f"Decision: _____ H₀ at α=0.05")  # Fill in: "Reject" or "Fail to reject"\n',
            '    print(f"Interpretation: Mean productivity _____ significantly from 1990 to 2014.")  # Fill in: "changed" or "did not change"\n',
            'else:\n',
            '    print(f"Decision: Fail to reject H₀ at α=0.05")\n',
            '    print(f"Interpretation: Insufficient evidence that mean productivity changed.")\n',
            '```\n',
            '\n',
            '**Questions to consider:**\n',
            '\n',
            '- What does the p-value tell you about the likelihood of observing this difference by chance?\n',
            '- Is the change economically meaningful (not just statistically significant)?\n',
            '- What assumptions does the two-sample t-test make?\n'
        ]
    },

    # Cell 8: Task 3 description
    {
        'cell_type': 'markdown',
        'metadata': {},
        'source': [
            '### Task 3: Comparing Regional Productivity Levels (SEMI-GUIDED)\n',
            '\n',
            '**Learning Goal:** Apply hypothesis testing to compare subgroups\n',
            '\n',
            '**Economic Question:** "Do African countries have significantly lower productivity than European countries (2014 data)?"\n',
            '\n',
            '**Your task:**\n',
            '\n',
            '1. Filter 2014 data by region (use `region` column in dataset)\n',
            '2. Test H₀: μ_Africa = μ_Europe vs Hₐ: μ_Africa ≠ μ_Europe\n',
            '3. Calculate 95% CI for the difference in means\n',
            '4. Visualize distributions with side-by-side box plots\n',
            '\n',
            '**Code structure (complete the analysis):**\n',
            '\n',
            '```python\n',
            '# Filter 2014 data by region\n',
            'df_2014 = df.loc[df.index.get_level_values(\'year\') == 2014]\n',
            '\n',
            '# Extract productivity for Africa and Europe\n',
            'lp_africa = df_2014.loc[df_2014[\'region\'] == \'Africa\', \'lp\']\n',
            'lp_europe = df_2014.loc[df_2014[\'region\'] == \'Europe\', \'lp\']\n',
            '\n',
            'print(f"Sample sizes: Africa n={len(lp_africa)}, Europe n={len(lp_europe)}")\n',
            'print(f"Africa mean: ${lp_africa.mean():,.0f}")\n',
            'print(f"Europe mean: ${lp_europe.mean():,.0f}\\n")\n',
            '\n',
            '# Conduct two-sample t-test\n',
            '# YOUR CODE HERE: Use stats.ttest_ind() to test if means differ\n',
            '# Calculate and print: t-statistic, p-value, decision at α=0.05\n',
            '\n',
            '# Calculate 95% CI for difference in means\n',
            '# YOUR CODE HERE: \n',
            '# 1. Calculate difference in means\n',
            '# 2. Calculate SE of difference\n',
            '# 3. Get t-critical value\n',
            '# 4. Construct CI: (difference - ME, difference + ME)\n',
            '\n',
            '# Visualize distributions\n',
            'fig, ax = plt.subplots(1, 1, figsize=(8, 5))\n',
            'ax.boxplot([lp_africa, lp_europe], labels=[\'Africa\', \'Europe\'])\n',
            'ax.set_ylabel(\'Labor Productivity ($)\')\n',
            'ax.set_title(\'Labor Productivity Distribution by Region (2014)\')\n',
            'ax.grid(axis=\'y\', alpha=0.3)\n',
            'plt.tight_layout()\n',
            'plt.show()\n',
            '```\n',
            '\n',
            '**Questions to consider:**\n',
            '\n',
            '- Is the difference statistically significant?\n',
            '- How large is the productivity gap in dollar terms?\n',
            '- What does the box plot reveal about within-region variation?\n',
            '- Does the CI for the difference include zero? What does that mean?\n'
        ]
    },

    # Cell 9: Key Concept Box 2
    {
        'cell_type': 'markdown',
        'metadata': {},
        'source': [
            '> **Key Concept: Economic vs Statistical Significance**\n',
            '>\n',
            '> A result can be **statistically significant** (p < 0.05) but **economically trivial**, or vice versa:\n',
            '>\n',
            '> **Statistical significance** answers: "Is this difference unlikely to be due to chance?"\n',
            '> - Depends on sample size: larger samples detect smaller differences\n',
            '> - Measured by p-value: probability of observing this result if H₀ is true\n',
            '> - Standard: p < 0.05 means <5% chance of Type I error\n',
            '>\n',
            '> **Economic significance** answers: "Is this difference large enough to matter?"\n',
            '> - Depends on context: a \\$1,000 productivity gap might be huge for low-income countries but trivial for high-income countries\n',
            '> - Measured by effect size: actual magnitude of the difference\n',
            '> - Judgment call: requires domain expertise\n',
            '>\n',
            '> **Example:**\n',
            '> - With n=10,000 countries, a \\$100 productivity difference might be statistically significant (p<0.001) but economically meaningless\n',
            '> - With n=10 countries, a \\$10,000 difference might not be statistically significant (p=0.08) but could be economically important\n',
            '>\n',
            '> **Best practice:** Always report BOTH:\n',
            '> 1. Statistical result: "We reject H₀ at α=0.05 (p=0.003)"\n',
            '> 2. Economic interpretation: "The \\$15,000 productivity gap represents a 35% difference, which is economically substantial for development policy"\n'
        ]
    },

    # Cell 10: Task 4 description
    {
        'cell_type': 'markdown',
        'metadata': {},
        'source': [
            '### Task 4: One-Sided Test for Growth (MORE INDEPENDENT)\n',
            '\n',
            '**Learning Goal:** Apply Section 4.6 (one-sided tests) to directional hypotheses\n',
            '\n',
            '**Economic Question:** "Can we conclude that mean global productivity in 2014 exceeds \\$50,000 (a policy benchmark)?"\n',
            '\n',
            '**Your task:**\n',
            '\n',
            '1. Test H₀: μ ≤ 50,000 vs Hₐ: μ > 50,000\n',
            '2. Use `scipy.stats.ttest_1samp()` with `alternative=\'greater\'`\n',
            '3. Compare one-sided vs two-sided p-values\n',
            '4. Discuss Type I error: what does α=0.05 mean in this context?\n',
            '\n',
            '**Outline (write your own code):**\n',
            '\n',
            '```python\n',
            '# Step 1: State hypotheses clearly\n',
            '# H₀: μ ≤ 50,000 (productivity does not exceed benchmark)\n',
            '# Hₐ: μ > 50,000 (productivity exceeds benchmark)\n',
            '\n',
            '# Step 2: Conduct one-sided t-test\n',
            '# Use: stats.ttest_1samp(lp_2014, popmean=50000, alternative=\'greater\')\n',
            '\n',
            '# Step 3: Calculate two-sided p-value for comparison\n',
            '# Use: stats.ttest_1samp(lp_2014, popmean=50000, alternative=\'two-sided\')\n',
            '\n',
            '# Step 4: Report results\n',
            '# - Sample mean\n',
            '# - t-statistic\n',
            '# - One-sided p-value\n',
            '# - Two-sided p-value\n',
            '# - Decision at α=0.05\n',
            '\n',
            '# Step 5: Interpret Type I error\n',
            '# If we reject H₀, what is the probability we made a mistake?\n',
            '```\n',
            '\n',
            '**Hint:** Remember that for one-sided tests:\n',
            '- If Hₐ: μ > μ₀, use `alternative=\'greater\'`\n',
            '- The one-sided p-value is half the two-sided p-value (when t-stat has correct sign)\n',
            '- Type I error = rejecting H₀ when it\'s actually true\n',
            '\n',
            '**Questions to consider:**\n',
            '\n',
            '- Why is the one-sided p-value smaller than the two-sided p-value?\n',
            '- When is a one-sided test appropriate vs a two-sided test?\n',
            '- What are the policy implications if we reject H₀?\n'
        ]
    },

    # Cell 11: Task 5 description
    {
        'cell_type': 'markdown',
        'metadata': {},
        'source': [
            '### Task 5: Proportions Analysis - Growth Winners (INDEPENDENT)\n',
            '\n',
            '**Learning Goal:** Apply Section 4.7 (proportions) to binary outcomes\n',
            '\n',
            '**Economic Question:** "What proportion of countries experienced productivity growth from 1990 to 2014, and can we conclude that more than half experienced growth?"\n',
            '\n',
            '**Your task:**\n',
            '\n',
            '1. Create country-level dataset with productivity in both 1990 and 2014\n',
            '2. Create binary variable: `growth = 1` if productivity increased, `0` otherwise\n',
            '3. Calculate sample proportion of "growth winners"\n',
            '4. Construct 95% CI for population proportion using normal approximation\n',
            '5. Test H₀: p = 0.50 vs Hₐ: p ≠ 0.50 (are half growth winners?)\n',
            '\n',
            '**Hints:**\n',
            '\n',
            '```python\n',
            '# Hint 1: Reshape data to country-level\n',
            '# df_1990 = df.loc[df.index.get_level_values(\'year\') == 1990, [\'lp\']]\n',
            '# df_2014 = df.loc[df.index.get_level_values(\'year\') == 2014, [\'lp\']]\n',
            '# Merge on country index\n',
            '\n',
            '# Hint 2: Create binary growth indicator\n',
            '# growth = (lp_2014 > lp_1990).astype(int)\n',
            '\n',
            '# Hint 3: Proportions formulas from Section 4.7\n',
            '# p_hat = np.mean(growth)\n',
            '# se_p = np.sqrt(p_hat * (1 - p_hat) / n)\n',
            '# CI: p_hat ± z_crit * se_p\n',
            '# For 95% CI: z_crit = 1.96\n',
            '\n',
            '# Hint 4: Test statistic for proportions\n',
            '# z = (p_hat - p0) / np.sqrt(p0 * (1 - p0) / n)\n',
            '# where p0 = 0.50 under H₀\n',
            '```\n',
            '\n',
            '**Questions to consider:**\n',
            '\n',
            '- What proportion of countries experienced growth?\n',
            '- Does the 95% CI include 0.50? What does that mean?\n',
            '- Is there evidence that the proportion differs from 50%?\n',
            '- Which countries did NOT experience growth? (Bonus: investigate why)\n'
        ]
    },

    # Cell 12: Task 6 description
    {
        'cell_type': 'markdown',
        'metadata': {},
        'source': [
            '### Task 6: Multi-Regional Hypothesis Testing (INDEPENDENT)\n',
            '\n',
            '**Learning Goal:** Integrate multiple inference methods in comprehensive analysis\n',
            '\n',
            '**Economic Question:** "Which regional pairs show statistically significant productivity gaps in 2014?"\n',
            '\n',
            '**Your task:**\n',
            '\n',
            '1. Identify all regions in the dataset (use `df_2014[\'region\'].unique()`)\n',
            '2. Calculate 95% CIs for mean productivity in each region\n',
            '3. Conduct pairwise t-tests (Africa vs Europe, Africa vs Asia, Africa vs Americas, etc.)\n',
            '4. Create a visualization showing CIs for all regions (error bar plot)\n',
            '5. Discuss the **multiple testing problem**: when conducting many tests, what happens to Type I error?\n',
            '\n',
            '**Challenge goals (minimal guidance):**\n',
            '\n',
            '- Design your own analysis structure\n',
            '- Use loops to avoid repetitive code\n',
            '- Create professional visualizations\n',
            '- Write clear economic interpretations\n',
            '\n',
            '**Suggested approach:**\n',
            '\n',
            '```python\n',
            '# Step 1: Get all regions and calculate summary stats\n',
            '# For each region: mean, std, se, 95% CI\n',
            '# Store in a DataFrame or dictionary\n',
            '\n',
            '# Step 2: Conduct all pairwise tests\n',
            '# Use itertools.combinations() to generate pairs\n',
            '# For each pair: run ttest_ind(), store t-stat and p-value\n',
            '\n',
            '# Step 3: Visualize CIs\n',
            '# Create error bar plot: plt.errorbar()\n',
            '# Or bar plot with CI whiskers\n',
            '\n',
            '# Step 4: Report significant differences\n',
            '# Which pairs have p < 0.05?\n',
            '# What is the magnitude of differences?\n',
            '\n',
            '# Step 5: Discuss multiple testing\n',
            '# If you run 10 tests at α=0.05, what\'s the probability of at least one false positive?\n',
            '# Consider Bonferroni correction: α_adjusted = 0.05 / number_of_tests\n',
            '```\n',
            '\n',
            '**Questions to consider:**\n',
            '\n',
            '- Which region has the highest mean productivity? Lowest?\n',
            '- Are all pairwise differences statistically significant?\n',
            '- How does the multiple testing problem affect your conclusions?\n',
            '- What economic factors might explain regional productivity gaps?\n'
        ]
    },

    # Cell 13: Wrap-up reflection
    {
        'cell_type': 'markdown',
        'metadata': {},
        'source': [
            '### What You\'ve Learned\n',
            '\n',
            'By completing this case study, you\'ve practiced **all the major skills from Chapter 4**:\n',
            '\n',
            '**Statistical Methods:**\n',
            '- ✅ Constructed confidence intervals (90%, 95%, 99%) for population means\n',
            '- ✅ Conducted two-sided hypothesis tests to compare groups and time periods\n',
            '- ✅ Performed one-sided directional tests for benchmark comparisons\n',
            '- ✅ Applied proportions inference to binary economic outcomes\n',
            '- ✅ Calculated and interpreted t-statistics, p-values, and margins of error\n',
            '- ✅ Used both manual calculations and `scipy.stats` functions\n',
            '\n',
            '**Economic Applications:**\n',
            '- ✅ Tested convergence hypotheses (did productivity gaps narrow over time?)\n',
            '- ✅ Compared regional development levels (Africa, Europe, Asia, Americas)\n',
            '- ✅ Evaluated policy benchmarks (does productivity exceed thresholds?)\n',
            '- ✅ Identified "growth winners" and "growth losers" among countries\n',
            '- ✅ Distinguished between statistical and economic significance\n',
            '\n',
            '**Programming Skills:**\n',
            '- ✅ Filtered and reshaped panel data (multi-index DataFrames)\n',
            '- ✅ Implemented statistical tests with `scipy.stats`\n',
            '- ✅ Created informative visualizations (box plots, error bars)\n',
            '- ✅ Wrote clear, reproducible analysis code\n',
            '\n',
            '**Critical Thinking:**\n',
            '- ✅ Formulated null and alternative hypotheses from economic questions\n',
            '- ✅ Interpreted p-values in context (not just "significant" vs "not significant")\n',
            '- ✅ Connected statistical results to economic meaning and policy implications\n',
            '- ✅ Recognized limitations (Type I/II errors, multiple testing problem)\n',
            '\n',
            '---\n',
            '\n',
            '**Next steps:**\n',
            '\n',
            'These skills form the foundation for more advanced methods in later chapters:\n',
            '- **Chapter 5:** Regression analysis (relationship between two variables)\n',
            '- **Chapter 6:** Multiple regression (controlling for confounders)\n',
            '- **Chapter 7:** Hypothesis tests in regression models\n',
            '\n',
            'Statistical inference is everywhere in empirical economics. You\'ve now mastered the core toolkit for:\n',
            '- Quantifying uncertainty\n',
            '- Testing economic theories\n',
            '- Making data-driven decisions\n',
            '- Communicating results with precision\n',
            '\n',
            '**Well done!** 🎉\n'
        ]
    }
]

def main():
    """Insert case study cells into Chapter 4 notebook"""

    # Load existing notebook
    notebook_path = 'notebooks_colab/ch04_Statistical_Inference_for_the_Mean.ipynb'

    print(f"Loading notebook: {notebook_path}")
    with open(notebook_path, 'r', encoding='utf-8') as f:
        nb = json.load(f)

    original_cell_count = len(nb['cells'])
    print(f"Original cell count: {original_cell_count}")

    # Find insertion point (after Section 4.7, before Key Takeaways)
    # Look for cell containing "Key Takeaways"
    insertion_index = None
    for i, cell in enumerate(nb['cells']):
        if cell['cell_type'] == 'markdown':
            content = ''.join(cell['source'])
            if 'Key Takeaways' in content and i > 40:  # Make sure it's the final Key Takeaways
                insertion_index = i
                break

    if insertion_index is None:
        print("ERROR: Could not find Key Takeaways section")
        return

    print(f"Insertion point: Cell {insertion_index} (before Key Takeaways)")

    # Insert all case study cells
    for i, cell in enumerate(case_study_cells):
        nb['cells'].insert(insertion_index + i, cell)

    new_cell_count = len(nb['cells'])
    print(f"New cell count: {new_cell_count} (+{new_cell_count - original_cell_count} cells)")

    # Save updated notebook
    with open(notebook_path, 'w', encoding='utf-8') as f:
        json.dump(nb, f, indent=2, ensure_ascii=False)

    print(f"\n✅ Case study added successfully!")
    print(f"\nNew structure:")
    print(f"  - Cells 0-{insertion_index-1}: Original content (Title → Setup → Sections 4.1-4.7)")
    print(f"  - Cells {insertion_index}-{insertion_index + len(case_study_cells) - 1}: NEW Section 4.8 Case Study ({len(case_study_cells)} cells)")
    print(f"  - Cells {insertion_index + len(case_study_cells)}-{new_cell_count-1}: Key Takeaways + Practice Exercises")

    print(f"\nNext steps:")
    print(f"1. Review notebook in Jupyter/Colab")
    print(f"2. Test data loading cell (runs without errors?)")
    print(f"3. Regenerate PDF:")
    print(f"   cd notebooks_colab && jupyter nbconvert --to html ch04_Statistical_Inference_for_the_Mean.ipynb && cd ..")
    print(f"   python3 inject_print_css.py notebooks_colab/ch04_Statistical_Inference_for_the_Mean.html notebooks_colab/ch04_Statistical_Inference_for_the_Mean_printable.html")
    print(f"   python3 generate_pdf_playwright.py ch04")

if __name__ == '__main__':
    main()
