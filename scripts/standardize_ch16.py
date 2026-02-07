#!/usr/bin/env python3
"""Standardize CH16: Checking the Model and Data"""
import json, re

NOTEBOOK = 'notebooks_colab/ch16_Checking_the_Model_and_Data.ipynb'

with open(NOTEBOOK) as f:
    nb = json.load(f)

cells = nb['cells']

def make_md(source):
    return {"cell_type": "markdown", "metadata": {}, "source": [source]}

# ============================================================
# Phase 0: Remove emojis from ALL markdown cells
# ============================================================
emoji_pattern = re.compile(
    "["
    "\U0001F600-\U0001F64F"  # emoticons
    "\U0001F300-\U0001F5FF"  # symbols & pictographs
    "\U0001F680-\U0001F6FF"  # transport & map
    "\U0001F1E0-\U0001F1FF"  # flags
    "\U00002702-\U000027B0"
    "\U000024C2-\U0001F251"
    "\U0001f926-\U0001f937"
    "\U00010000-\U0010ffff"
    "\u2600-\u26FF"
    "\u2700-\u27BF"
    "\u23E9-\u23F3"
    "\u23F8-\u23FA"
    "\u200d"
    "\ufe0f"
    "\u20e3"
    "]+",
    flags=re.UNICODE
)

emoji_count = 0
for i in range(len(cells)):
    if cells[i]['cell_type'] == 'markdown':
        src = ''.join(cells[i]['source'])
        if emoji_pattern.search(src):
            src = emoji_pattern.sub('', src)
            src = re.sub(r'  +', ' ', src)
            cells[i]['source'] = [src]
            emoji_count += 1

print(f"Phase 0: Removed emojis from {emoji_count} cells")

# ============================================================
# Phase 1: Enhance Chapter Overview (cell 1)
# ============================================================
cells[1] = make_md("""## Chapter Overview

This chapter focuses on checking model assumptions and diagnosing data problems. You'll gain both theoretical understanding and practical skills through hands-on Python examples.

**Learning Objectives:**

By the end of this chapter, you will be able to:
1. Identify and diagnose multicollinearity using correlation matrices and VIF
2. Understand the consequences when each of the four core OLS assumptions fails
3. Recognize omitted variable bias and specify appropriate control variables
4. Understand endogeneity and when to use instrumental variables (IV)
5. Detect and address heteroskedasticity using robust standard errors
6. Identify autocorrelation in time series data and apply HAC-robust standard errors
7. Interpret residual diagnostic plots to detect model violations
8. Identify outliers and influential observations using DFITS and DFBETAS
9. Apply appropriate diagnostic tests and remedies for common data problems

**Chapter outline:**
- 16.1 Multicollinearity
- 16.2-16.4 Model Assumptions, Incorrect Models, and Endogeneity
- 16.5 Heteroskedastic Errors
- 16.6 Correlated Errors (Autocorrelation)
- 16.7 Example: Democracy and Growth
- 16.8 Diagnostics: Residual Plots and Influential Observations
- Key Takeaways
- Practice Exercises
- Case Studies

**Datasets used:**
- **AED_EARNINGS_COMPLETE.DTA**: 842 full-time workers with earnings, age, education, and experience (2010)
- **AED_DEMOCRACY.DTA**: 131 countries with democracy, growth, and institutional variables (Acemoglu et al. 2008)
""")

print("Phase 1: Enhanced Chapter Overview")

# ============================================================
# Phase 4: Replace Chapter Summary (cell 37) with Key Takeaways
# ============================================================
cells[37] = make_md("""## Key Takeaways

**Multicollinearity:**
- Multicollinearity occurs when regressors are highly correlated, making individual coefficients imprecisely estimated
- VIF > 10 indicates serious multicollinearity; VIF > 5 warrants investigation
- OLS remains unbiased and consistent -- the problem is precision, not bias
- Solutions: use joint F-tests, drop redundant variables, center variables before creating interactions, or collect more data

**OLS Assumption Violations:**
- Assumptions 1-2 violations (incorrect model, endogeneity) cause bias and inconsistency -- fundamental problems requiring model changes or IV
- Assumptions 3-4 violations (heteroskedasticity, autocorrelation) do not bias coefficients but invalidate standard errors
- Wrong standard errors lead to incorrect t-statistics, confidence intervals, and hypothesis tests
- Omitted variables bias formula: $\\text{Bias} = \\beta_3 \\times \\delta_{23}$, where $\\beta_3$ is the omitted variable's effect and $\\delta_{23}$ is the correlation

**Heteroskedasticity and Robust Standard Errors:**
- Heteroskedasticity means error variance varies across observations, common in cross-sectional data
- Use heteroskedasticity-robust (HC1/White) standard errors for valid inference
- Robust SEs are typically larger than default SEs, giving more conservative (honest) inference
- Always use robust SEs for cross-sectional regressions as a default practice

**Autocorrelation and HAC Standard Errors:**
- Autocorrelation means errors are correlated over time, common in time series data
- Default SEs are typically too small with autocorrelation, leading to over-rejection
- Use HAC (Newey-West) standard errors that account for both heteroskedasticity and autocorrelation
- Check the ACF of residuals to detect autocorrelation patterns

**Diagnostic Plots:**
- Residual vs. fitted values: detect heteroskedasticity (fan shape) and nonlinearity (curved pattern)
- Component-plus-residual plot: detect nonlinearity in individual regressors
- Added variable plot: isolate partial relationship between y and x, controlling for other variables
- LOWESS smooth helps reveal patterns that are hard to see in raw scatter plots

**Influential Observations:**
- DFITS measures influence on fitted values; threshold $|\\text{DFITS}| > 2\\sqrt{k/n}$
- DFBETAS measures influence on individual coefficients; threshold $|\\text{DFBETAS}| > 2/\\sqrt{n}$
- Investigate influential observations rather than automatically deleting them
- Check whether conclusions change substantially when influential cases are excluded

**Python tools:** `statsmodels` (VIF, OLSInfluence, robust covariance), `matplotlib`/`seaborn` (diagnostic plots), LOWESS smoothing

**Next steps:** Chapter 17 extends these ideas to panel data, where you'll learn fixed effects and random effects models that address unobserved heterogeneity across units.

---

Congratulations! You've completed Chapter 16 on model checking and data diagnostics. You now have both the theoretical understanding and practical Python skills to evaluate regression assumptions, detect problems, and apply appropriate remedies.
""")

print("Phase 4: Replaced Chapter Summary with Key Takeaways")

# ============================================================
# Phase 2 & 3: Insert Key Concepts and Transitions (bottom-to-top)
# ============================================================

insertions = []

# --- Key Concept 8: After cell 36 (DFBETAS plot) ---
insertions.append((37, make_md("""> **Key Concept: Influential Observations -- DFITS and DFBETAS**
>
> DFITS measures influence on fitted values: $DFITS_i$ is the scaled change in $\\hat{y}_i$ when observation $i$ is excluded. DFBETAS measures influence on individual coefficients: $DFBETAS_{j,i}$ is the scaled change in $\\hat{\\beta}_j$. Thresholds for investigation are $|DFITS| > 2\\sqrt{k/n}$ and $|DFBETAS| > 2/\\sqrt{n}$. Don't automatically delete influential points -- investigate whether they represent data errors, genuine outliers, or valid extreme values that carry important information.
""")))

# --- Key Concept 7: After cell 31 (Figure 16.3 diagnostic plots) ---
insertions.append((32, make_md("""> **Key Concept: Diagnostic Plots for Model Validation**
>
> Three complementary plots assess individual regressors: (1) residual vs. regressor checks for patterns suggesting nonlinearity or heteroskedasticity; (2) component-plus-residual plot ($b_j x_j + e$ vs. $x_j$) reveals the partial relationship and detects nonlinearity; (3) added variable plot purges both $y$ and $x_j$ of other regressors, showing the pure partial effect whose slope equals the OLS coefficient $b_j$. LOWESS smoothing helps reveal systematic patterns.
""")))

# --- Transition 3: Before cell 32 (DFITS section) ---
insertions.append((32, make_md("""*Having examined residual diagnostic plots for visual detection of model problems, we now turn to numerical influence measures that quantify how much individual observations affect regression results.*
""")))

# --- Key Concept 6: After cell 25 (multiple regression with controls) ---
insertions.append((26, make_md("""> **Key Concept: Omitted Variables Bias in Practice**
>
> The democracy-growth example demonstrates omitted variables bias: the growth coefficient falls from 0.131 (bivariate) to 0.047 (with controls), a 64% reduction. Institutional variables (religion, executive constraints) were correlated with both democracy and growth, biasing the bivariate estimate upward. Always ask: "What variables might affect my outcome and correlate with my key regressor?" Include relevant controls to reduce bias.
""")))

# --- Transition 2: Before cell 22 (16.7 Democracy and Growth) ---
insertions.append((22, make_md("""*Now that we understand the theoretical consequences of assumption violations, let's apply these concepts to a real-world example examining whether democracy promotes economic growth.*
""")))

# --- Key Concept 5: After cell 20 (ACF of residuals) ---
insertions.append((21, make_md("""> **Key Concept: Autocorrelation and HAC Standard Errors**
>
> Autocorrelation means errors are correlated over time ($\\text{Cov}[u_t, u_s] \\neq 0$), common in time series when economic shocks persist. OLS remains unbiased but standard errors are wrong -- typically too small, leading to false significance. Use HAC (Newey-West) standard errors for valid inference. Check the autocorrelation function (ACF) of residuals: significant autocorrelations at multiple lags indicate the problem. Severe autocorrelation drastically reduces the effective sample size.
""")))

# --- Key Concept 4: After cell 16 (SE comparison) ---
insertions.append((17, make_md("""> **Key Concept: Heteroskedasticity and Robust Standard Errors**
>
> Heteroskedasticity means the error variance depends on the regressors: $\\text{Var}[u_i | \\mathbf{x}_i] \\neq \\sigma^2$. OLS coefficients remain unbiased, but default standard errors are wrong -- typically too small, giving false confidence in precision. Use heteroskedasticity-robust (HC1/White) standard errors, which are valid whether or not heteroskedasticity is present. Always use robust SEs for cross-sectional data as a default practice.
""")))

# --- Key Concept 3: After cell 14 (model assumptions code) ---
insertions.append((15, make_md("""> **Key Concept: Consequences of OLS Assumption Violations**
>
> When assumptions 1 or 2 fail (incorrect model or endogeneity), OLS is biased and inconsistent -- a fundamental problem requiring model changes or instrumental variables. When assumptions 3 or 4 fail (heteroskedasticity or autocorrelation), OLS remains unbiased and consistent but standard errors are wrong, invalidating confidence intervals and hypothesis tests. The key distinction: bias requires fixing the model; wrong SEs require only changing the inference method.
""")))

# --- Transition 1: Before cell 13 (16.2-16.4 Model Assumptions) ---
insertions.append((13, make_md("""*Having explored multicollinearity as a data problem that inflates standard errors, we now examine the broader set of OLS assumptions and what happens when each one fails.*
""")))

# --- Key Concept 2: After cell 12 (joint hypothesis tests) ---
insertions.append((13, make_md("""> **Key Concept: Joint Hypothesis Tests Under Multicollinearity**
>
> Even when multicollinearity makes individual t-tests unreliable (high VIF, large standard errors), joint F-tests remain powerful. Testing whether a group of collinear variables is jointly significant avoids the imprecision problem because the F-test evaluates the combined contribution. Always use joint tests for groups of correlated regressors rather than relying on individual significance.
""")))

# --- Key Concept 1: After cell 8 (VIF calculation) ---
insertions.append((9, make_md("""> **Key Concept: Multicollinearity and the Variance Inflation Factor**
>
> The Variance Inflation Factor quantifies multicollinearity: $VIF_j = 1/(1 - R_j^2)$, where $R_j^2$ is from regressing $x_j$ on all other regressors. VIF = 1 means no collinearity; VIF > 10 indicates serious problems (standard errors inflated by $\\sqrt{10} \\approx 3.2\\times$). While OLS remains unbiased, individual coefficients become imprecise and may have "wrong" signs. Predictions and joint tests remain valid despite multicollinearity.
""")))

# Sort insertions bottom-to-top to avoid index shifting
insertions.sort(key=lambda x: x[0], reverse=True)

for idx, cell in insertions:
    cells.insert(idx, cell)

print(f"Phase 2-3: Inserted {len(insertions)} cells (8 Key Concepts + 3 Transitions)")

# ============================================================
# Phase 5: Append Practice Exercises
# ============================================================
practice = make_md("""## Practice Exercises

**Exercise 1: Irrelevant Variables vs. Omitted Variables**

You estimate $y_i = \\beta_1 + \\beta_2 x_{2i} + \\beta_3 x_{3i} + u_i$ by OLS.

(a) If $x_3$ should not appear in the model (irrelevant variable), what happens to the OLS estimates of $\\beta_1$ and $\\beta_2$? Are they biased?

(b) If a relevant variable $x_4$ was omitted from the model, and $x_4$ is correlated with $x_2$, what happens to $\\hat{\\beta}_2$? Write the omitted variables bias formula.

**Exercise 2: VIF Interpretation**

A regression of earnings on age, education, and experience yields VIF values of 22.0 (age), 17.3 (education), and 36.9 (experience).

(a) Which variable has the most severe multicollinearity problem? Explain.

(b) Calculate the $R^2$ from the auxiliary regression for the variable with the highest VIF.

(c) By what factor are the standard errors inflated compared to the no-collinearity case?

**Exercise 3: Choosing Standard Error Types**

For each scenario below, state which type of standard errors you would use (default, HC-robust, HAC, or cluster-robust) and why:

(a) Cross-sectional regression of wages on education and experience for 5,000 workers.

(b) Time series regression of GDP growth on interest rates using 200 quarterly observations.

(c) Regression of test scores on class size using data from 50 schools with multiple classrooms per school.

**Exercise 4: Heteroskedasticity Detection**

You estimate a regression and obtain the following SE comparison:

| Variable | Standard SE | Robust SE | Ratio |
|----------|-------------|-----------|-------|
| Education | 570 | 642 | 1.13 |
| Age | 154 | 151 | 0.98 |

(a) Is there evidence of heteroskedasticity? Which variable's inference is most affected?

(b) If you used standard SEs and the t-statistic for education was 2.05, would the conclusion change with robust SEs?

**Exercise 5: DFITS Threshold Calculation**

In a regression with $k = 7$ regressors and $n = 131$ observations:

(a) Calculate the DFITS threshold for identifying influential observations.

(b) If 8 observations exceed this threshold, what percentage of the sample is flagged as potentially influential?

(c) Describe the steps you would take to investigate these influential observations.

**Exercise 6: Autocorrelation Consequences**

A time series regression yields a first-lag residual autocorrelation of $\\rho_1 = 0.80$.

(a) Is this evidence of autocorrelation? What does it mean for the residual pattern?

(b) Approximate the factor by which the effective sample size is reduced (use the formula $\\frac{1+\\rho}{1-\\rho}$).

(c) A coefficient has a default t-statistic of 4.5. If the HAC standard error is 3 times larger than the default, what is the corrected t-statistic? Is the coefficient still significant at 5%?
""")

cells.append(practice)
print("Phase 5: Added 6 Practice Exercises")

# ============================================================
# Phase 6: Case Study (Mendez dataset)
# ============================================================
case_study = make_md("""## Case Studies

### Case Study: Regression Diagnostics for Cross-Country Productivity Analysis

In this case study, you will apply the diagnostic techniques from this chapter to analyze cross-country labor productivity using the Mendez convergence clubs dataset.

**Dataset:** Mendez (2020) convergence clubs data
- **Source:** `https://raw.githubusercontent.com/quarcs-lab/mendez2020-convergence-clubs-code-data/master/assets/dat.csv`
- **Sample:** 108 countries, 1990-2014
- **Variables:** `lp` (labor productivity), `rk` (physical capital), `hc` (human capital), `rgdppc` (real GDP per capita), `tfp` (total factor productivity), `region`

**Research question:** What econometric issues arise when modeling cross-country productivity, and how do diagnostic tools help detect and address them?

---

#### Task 1: Detect Multicollinearity (Guided)

Load the dataset and estimate a regression of log labor productivity (`np.log(lp)`) on log physical capital (`np.log(rk)`), human capital (`hc`), and log GDP per capita (`np.log(rgdppc)`), using the year 2014 cross-section.

```python
import pandas as pd
import numpy as np
from statsmodels.formula.api import ols
from statsmodels.stats.outliers_influence import variance_inflation_factor
import statsmodels.api as sm

url = "https://raw.githubusercontent.com/quarcs-lab/mendez2020-convergence-clubs-code-data/master/assets/dat.csv"
dat = pd.read_csv(url)
dat2014 = dat[dat['year'] == 2014].copy()
dat2014['ln_lp'] = np.log(dat2014['lp'])
dat2014['ln_rk'] = np.log(dat2014['rk'])
dat2014['ln_rgdppc'] = np.log(dat2014['rgdppc'])

# Estimate the model
model = ols('ln_lp ~ ln_rk + hc + ln_rgdppc', data=dat2014).fit(cov_type='HC1')
print(model.summary())

# Calculate VIF
X = dat2014[['ln_rk', 'hc', 'ln_rgdppc']].dropna()
X = sm.add_constant(X)
for i, col in enumerate(X.columns):
    print(f"VIF({col}): {variance_inflation_factor(X.values, i):.2f}")
```

Interpret the VIF values. Is multicollinearity a concern? Which variables are most collinear and why?

---

#### Task 2: Compare Standard and Robust Standard Errors (Guided)

Estimate the same model with both default and robust (HC1) standard errors. Create a comparison table.

```python
model_default = ols('ln_lp ~ ln_rk + hc', data=dat2014).fit()
model_robust = ols('ln_lp ~ ln_rk + hc', data=dat2014).fit(cov_type='HC1')

comparison = pd.DataFrame({
    'Default SE': model_default.bse,
    'Robust SE': model_robust.bse,
    'Ratio': model_robust.bse / model_default.bse
})
print(comparison)
```

Is there evidence of heteroskedasticity? Which coefficient's inference is most affected?

---

#### Task 3: Residual Diagnostic Plots (Semi-guided)

Create the three diagnostic plots for the productivity model:
1. Actual vs. fitted values with LOWESS smooth
2. Residuals vs. fitted values with LOWESS smooth
3. Residuals vs. `ln_rk` (component-plus-residual plot)

*Hint:* Use `from statsmodels.nonparametric.smoothers_lowess import lowess` for the LOWESS smooth. Plot residuals from the robust model.

What do the diagnostic plots reveal about the model specification?

---

#### Task 4: Identify Influential Countries (Semi-guided)

Calculate DFITS and DFBETAS for the productivity regression. Identify countries that exceed the thresholds.

*Hint:* Use `OLSInfluence(model).dffits[0]` and `OLSInfluence(model).dfbetas`. The DFITS threshold is $2\\sqrt{k/n}$ and the DFBETAS threshold is $2/\\sqrt{n}$.

Which countries are most influential? Investigate whether removing them changes the key coefficients substantially.

---

#### Task 5: Regional Heterogeneity Analysis (Independent)

Test whether the relationship between capital and productivity varies across regions:
1. Add region dummy variables and region-capital interactions
2. Test for heteroskedasticity by comparing default and robust SEs across specifications
3. Conduct an F-test for joint significance of regional interactions

Does allowing for regional heterogeneity improve the model diagnostics?

---

#### Task 6: Diagnostic Report (Independent)

Write a 200-300 word diagnostic report for the cross-country productivity regression. Your report should:

1. Summarize the multicollinearity assessment (VIF results)
2. Document the heteroskedasticity evidence (SE comparison)
3. Describe what the residual plots reveal about model specification
4. List the most influential countries and their potential impact
5. Recommend the appropriate standard error type and any model modifications

> **Key Concept: Systematic Regression Diagnostics**
>
> A complete regression diagnostic workflow includes: (1) check multicollinearity via VIF before interpreting individual coefficients; (2) compare standard and robust SEs to detect heteroskedasticity; (3) examine residual plots for nonlinearity and patterns; (4) identify influential observations with DFITS and DFBETAS; (5) document all findings and report robust results. Always investigate problems rather than mechanically applying fixes.

> **Key Concept: Cross-Country Regression Challenges**
>
> Cross-country regressions face specific diagnostic challenges: multicollinearity among development indicators (GDP, capital, education are highly correlated), heteroskedasticity across countries at different development levels, and influential observations from outlier countries. Using robust standard errors and carefully examining influential cases is essential for credible cross-country analysis.

**What You've Learned:**
In this case study, you applied the complete diagnostic toolkit to cross-country productivity data. You detected multicollinearity among development indicators, compared standard and robust standard errors, created diagnostic plots, and identified influential countries. These skills ensure that your regression results are reliable and your conclusions are credible.
""")

cells.append(case_study)
print("Phase 6: Added Case Study (Mendez dataset)")

# ============================================================
# Phase 7: Closing cell
# ============================================================
cells.append(make_md(""))
print("Phase 7: Added closing cell")

# ============================================================
# Save
# ============================================================
nb['cells'] = cells

with open(NOTEBOOK, 'w') as f:
    json.dump(nb, f, indent=1, ensure_ascii=False)

print(f"\nDone! Total cells: {len(cells)}")
print(f"Markdown cells: {sum(1 for c in cells if c['cell_type'] == 'markdown')}")
print(f"Code cells: {sum(1 for c in cells if c['cell_type'] == 'code')}")
