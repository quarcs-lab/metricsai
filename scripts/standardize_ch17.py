#!/usr/bin/env python3
"""Standardize CH17: Panel Data, Time Series Data, Causation"""
import json, re

NOTEBOOK = 'notebooks_colab/ch17_Panel_Data_Time_Series_Data_Causation.ipynb'

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
    "\U0001F600-\U0001F64F"
    "\U0001F300-\U0001F5FF"
    "\U0001F680-\U0001F6FF"
    "\U0001F1E0-\U0001F1FF"
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

This chapter focuses on three important topics that extend basic regression methods: panel data, time series analysis, and causal inference. You'll gain both theoretical understanding and practical skills through hands-on Python examples.

**Learning Objectives:**

By the end of this chapter, you will be able to:
1. Apply cluster-robust standard errors for panel data with grouped observations
2. Understand panel data methods including random effects and fixed effects estimators
3. Decompose panel data variation into within and between components
4. Use fixed effects to control for time-invariant unobserved heterogeneity
5. Interpret results from logit models and calculate marginal effects
6. Recognize time series issues including autocorrelation and nonstationarity
7. Apply HAC (Newey-West) standard errors for time series regressions
8. Understand autoregressive and distributed lag models for dynamic relationships
9. Use instrumental variables and other methods for causal inference

**Chapter outline:**
- 17.2 Panel Data Models
- 17.3 Fixed Effects Estimation
- 17.4 Random Effects Estimation
- 17.5 Time Series Data
- 17.6 Autocorrelation
- 17.7 Causality and Instrumental Variables
- Key Takeaways
- Practice Exercises
- Case Studies

**Datasets used:**
- **AED_NBA.DTA**: NBA team revenue data (29 teams, 10 seasons, 2001-2011)
- **AED_EARNINGS_COMPLETE.DTA**: 842 full-time workers with earnings, age, and education (2010)
- **AED_INTERESTRATES.DTA**: U.S. Treasury interest rates, monthly (January 1982 - January 2015)
""")

print("Phase 1: Enhanced Chapter Overview")

# ============================================================
# Phase 4: Replace Chapter Summary (cell 38) with Key Takeaways
# ============================================================
cells[38] = make_md("""## Key Takeaways

**Panel Data Methods:**
- Panel data combines cross-sectional and time series dimensions, observing multiple individuals over multiple periods
- Variance decomposition separates total variation into within (over time) and between (across individuals) components
- Pooled OLS ignores panel structure; always use cluster-robust standard errors clustered by individual
- Fixed effects controls for time-invariant unobserved heterogeneity by using only within-individual variation
- Random effects is more efficient than FE but assumes individual effects are uncorrelated with regressors
- FE is preferred when individual effects are likely correlated with regressors (use Hausman test to decide)

**Nonlinear Models:**
- Logit models estimate the probability of binary outcomes using the logistic function
- Marginal effects ($\\hat{p}(1-\\hat{p})\\beta_j$) give the change in probability from a one-unit change in $x_j$
- Logit marginal effects and linear probability model coefficients are typically similar in magnitude

**Time Series Analysis:**
- Time series data exhibit autocorrelation, where observations are correlated with their past values
- Non-stationary series (trending) can produce spurious regressions with misleadingly high $R^2$
- First differencing removes trends and reduces autocorrelation, transforming non-stationary series to stationary
- HAC (Newey-West) standard errors account for both heteroskedasticity and autocorrelation in time series
- Default SEs can be dramatically too small with autocorrelation (3-8x understatement is common)

**Dynamic Models:**
- Autoregressive (AR) models capture persistence by including lagged dependent variables
- Autoregressive distributed lag (ADL) models include lags of both the dependent and independent variables
- The correlogram (ACF plot) helps determine the appropriate number of lags
- Total multiplier from an ADL model gives the long-run effect of a permanent change in $x$

**Causality and Instrumental Variables:**
- Correlation does not imply causation; endogeneity (omitted variables, reverse causation, measurement error) biases OLS
- Instrumental variables require relevance ($\\text{Corr}(z,x) \\neq 0$) and exogeneity ($\\text{Corr}(z,u) = 0$)
- Fixed effects, difference-in-differences, regression discontinuity, and matching are complementary causal methods
- Credible causal inference requires a convincing identification strategy, not just adding control variables

**Python tools:** `linearmodels` (PanelOLS, RandomEffects), `statsmodels` (OLS, logit, HAC, ACF), `matplotlib`/`seaborn` (visualization)

**Next steps:** Apply these methods to your own research questions. Panel data methods, time series models, and causal inference strategies are essential tools for any applied econometrician working with observational data.

---

Congratulations! You've completed Chapter 17, the final chapter covering panel data, time series, and causal inference. You now have a comprehensive toolkit of econometric methods for analyzing real-world data.
""")

print("Phase 4: Replaced Chapter Summary with Key Takeaways")

# ============================================================
# Phase 2 & 3: Insert Key Concepts and Transitions (bottom-to-top)
# ============================================================

insertions = []

# --- Key Concept 8: After cell 37 (causality code) ---
insertions.append((38, make_md("""> **Key Concept: Instrumental Variables and Causal Inference**
>
> Endogeneity (regressors correlated with errors) biases OLS estimates. Sources include omitted variables, measurement error, and simultaneity. Instrumental variables (IV) provide a solution: find a variable $z$ that is correlated with the endogenous regressor (relevance) but uncorrelated with the error (exogeneity). The IV estimator $\\hat{\\beta}_{IV} = \\text{Cov}(z,y)/\\text{Cov}(z,x)$ is consistent even when OLS is biased. Complementary causal methods include RCTs, DiD, RD, and matching.
""")))

# --- Transition 3: Before cell 36 (17.7 Causality) ---
insertions.append((36, make_md("""*Having developed tools for handling panel data and time series, we now address the fundamental question of causality -- how to move from correlation to causal inference using econometric methods.*
""")))

# --- Key Concept 7: After cell 31 (first differences regression) ---
insertions.append((32, make_md("""> **Key Concept: First Differencing for Nonstationary Data**
>
> First differencing ($\\Delta y_t = y_t - y_{t-1}$) transforms non-stationary trending series into stationary ones, eliminating spurious regression problems. After differencing, the residual autocorrelation drops dramatically (from $\\rho_1 \\approx 0.95$ to $\\rho_1 \\approx 0.25$ in the interest rate example). The coefficient interpretation changes from levels to changes: a 1-percentage-point change in the 1-year rate is associated with a 0.72-percentage-point change in the 10-year rate.
""")))

# --- Key Concept 6: After cell 27 (autocorrelation check) ---
insertions.append((28, make_md("""> **Key Concept: Detecting and Correcting Autocorrelation**
>
> The correlogram (ACF plot) reveals autocorrelation patterns in residuals. Slowly decaying autocorrelations (e.g., $\\rho_1 = 0.95$, $\\rho_{10} = 0.42$) indicate non-stationarity and persistent shocks. With autocorrelation, default SEs are too small -- HAC (Newey-West) SEs can be 3-8 times larger. Always check residual autocorrelation after estimating time series regressions and use HAC SEs or model the dynamics explicitly.
""")))

# --- Transition 2: Before cell 26 (17.6 Autocorrelation) ---
insertions.append((26, make_md("""*Now that we have visualized the time series patterns and estimated regressions in levels, let's formally examine autocorrelation in the residuals and its consequences for inference.*
""")))

# --- Key Concept 5: After cell 21 (time series data loaded) ---
insertions.append((22, make_md("""> **Key Concept: Time Series Stationarity and Spurious Regression**
>
> A time series is stationary if its statistical properties (mean, variance, autocorrelation) are constant over time. Many economic series are non-stationary (trending), which can produce spurious regressions: high $R^2$ and significant coefficients even when variables are unrelated. Solutions include first differencing (removing trends), detrending, and cointegration analysis. Always check whether your time series are stationary before interpreting regression results.
""")))

# --- Transition 1: Before cell 20 (17.5 Time Series) ---
insertions.append((20, make_md("""*Having explored panel data methods for cross-sectional units observed over time, we now turn to pure time series analysis where the focus shifts to temporal dynamics, autocorrelation, and stationarity.*
""")))

# --- Key Concept 4: After cell 17 (RE estimation) ---
insertions.append((18, make_md("""> **Key Concept: Fixed Effects vs. Random Effects**
>
> Fixed effects (FE) and random effects (RE) differ in a key assumption: RE requires that individual effects $\\alpha_i$ are uncorrelated with regressors, while FE allows arbitrary correlation. FE is consistent in either case but uses only within variation; RE is more efficient but inconsistent if the assumption fails. The Hausman test compares FE and RE estimates -- a significant difference indicates RE is inconsistent and FE should be preferred. In practice, FE is the safer choice for most observational studies.
""")))

# --- Key Concept 3: After cell 14 (FE estimation) ---
insertions.append((15, make_md("""> **Key Concept: Fixed Effects -- Controlling for Unobserved Heterogeneity**
>
> Fixed effects estimation controls for time-invariant individual characteristics by including individual-specific intercepts $\\alpha_i$. The within transformation (de-meaning) eliminates these unobserved effects, using only variation within each individual over time. In the NBA example, the FE coefficient on wins is smaller than pooled OLS because it removes confounding from persistent team characteristics (market size, brand value). FE provides more credible causal estimates but cannot identify effects of time-invariant variables.
""")))

# --- Key Concept 2: After cell 11 (pooled OLS with cluster SEs) ---
insertions.append((12, make_md("""> **Key Concept: Cluster-Robust Standard Errors for Panel Data**
>
> Observations within the same individual (team, firm, country) are correlated over time, violating the independence assumption. Default SEs dramatically understate uncertainty by treating all observations as independent. Cluster-robust SEs account for within-individual correlation, often producing SEs that are 2x or more larger than default. Always cluster by individual in panel data; with few clusters ($G < 30$), consider wild bootstrap refinements.
""")))

# --- Key Concept 1: After cell 5 (NBA data loaded) ---
insertions.append((6, make_md("""> **Key Concept: Panel Data Variation Decomposition**
>
> Panel data variation decomposes into two components: between variation (differences across individuals in their averages) and within variation (deviations from individual averages over time). In the NBA example, between variation in revenue is large (big-market vs. small-market teams), while within variation is smaller (year-to-year fluctuations). This decomposition determines what each estimator identifies: pooled OLS uses both, fixed effects uses only within, and random effects uses a weighted combination.
""")))

# Sort insertions bottom-to-top
insertions.sort(key=lambda x: x[0], reverse=True)

for idx, cell in insertions:
    cells.insert(idx, cell)

print(f"Phase 2-3: Inserted {len(insertions)} cells (8 Key Concepts + 3 Transitions)")

# ============================================================
# Phase 5: Append Practice Exercises
# ============================================================
practice = make_md("""## Practice Exercises

**Exercise 1: Panel Data Variance Decomposition**

A panel dataset of 50 firms over 5 years shows:
- Overall standard deviation of log revenue: 0.80
- Between standard deviation: 0.70
- Within standard deviation: 0.30

(a) Which source of variation dominates? What does this imply about the importance of firm-specific characteristics?

(b) If you run fixed effects, what proportion of the total variation are you using for estimation?

(c) Would you expect the FE coefficient to be larger or smaller than pooled OLS? Explain using the omitted variables bias formula.

**Exercise 2: Cluster-Robust Standard Errors**

You estimate a panel regression of test scores on class size using data from 100 schools over 3 years (300 observations). The coefficient on class size has:
- Default SE: 0.15 (t = 3.33)
- Cluster-robust SE (by school): 0.45 (t = 1.11)

(a) Why is the cluster SE three times larger than the default SE?

(b) Does your conclusion about the significance of class size change? At what significance level?

(c) What is the effective number of independent observations in this panel?

**Exercise 3: Fixed Effects vs. Random Effects**

You estimate a wage equation using panel data on 500 workers over 10 years. The Hausman test yields $\\chi^2 = 25.4$ with 3 degrees of freedom ($p < 0.001$).

(a) State the null and alternative hypotheses of the Hausman test.

(b) What do you conclude? Which estimator should you use?

(c) Give an economic reason why the RE assumption might fail in a wage equation (hint: think about unobserved ability).

**Exercise 4: Time Series Autocorrelation**

A regression of the 10-year interest rate on the 1-year rate using monthly data yields residuals with:
- Lag 1 autocorrelation: 0.95
- Lag 5 autocorrelation: 0.75
- Default SE on the 1-year rate coefficient: 0.022
- HAC SE (24 lags): 0.080

(a) Is there evidence of autocorrelation? What does the slowly decaying ACF pattern suggest about the data?

(b) By what factor do the HAC SEs differ from default SEs? What are the implications for hypothesis testing?

(c) Would first differencing help? What would you expect the lag 1 autocorrelation of the differenced residuals to be?

**Exercise 5: Spurious Regression**

You regress GDP on the number of mobile phone subscriptions over 30 years and find $R^2 = 0.97$ with a highly significant coefficient.

(a) Why might this be a spurious regression? What is the key characteristic of both series?

(b) Describe two methods to address this problem.

(c) If you first-difference both series, what economic relationship (if any) would the regression estimate?

**Exercise 6: Identifying Causal Effects**

For each scenario, identify the main threat to causal inference and suggest an appropriate method:

(a) Estimating the effect of police spending on crime rates across cities (cross-sectional data).

(b) Estimating the effect of a minimum wage increase on employment (state-level panel data with staggered adoption).

(c) Estimating the effect of class size on student achievement (students assigned to classes based on a cutoff rule).
""")

cells.append(practice)
print("Phase 5: Added 6 Practice Exercises")

# ============================================================
# Phase 6: Case Study (Mendez dataset)
# ============================================================
case_study = make_md("""## Case Studies

### Case Study: Panel Data Analysis of Cross-Country Productivity

In this case study, you will apply panel data methods from this chapter to analyze labor productivity dynamics across countries using the Mendez convergence clubs dataset.

**Dataset:** Mendez (2020) convergence clubs data
- **Source:** `https://raw.githubusercontent.com/quarcs-lab/mendez2020-convergence-clubs-code-data/master/assets/dat.csv`
- **Sample:** 108 countries, 1990-2014 (panel structure: country $\\times$ year)
- **Variables:** `lp` (labor productivity), `rk` (physical capital), `hc` (human capital), `rgdppc` (real GDP per capita), `tfp` (total factor productivity), `region`, `country`

**Research question:** How do physical and human capital affect labor productivity across countries, and does controlling for unobserved country characteristics change the estimates?

---

#### Task 1: Panel Data Structure (Guided)

Load the dataset and explore its panel structure. Calculate the within and between variation for log labor productivity.

```python
import pandas as pd
import numpy as np

url = "https://raw.githubusercontent.com/quarcs-lab/mendez2020-convergence-clubs-code-data/master/assets/dat.csv"
dat = pd.read_csv(url)
dat['ln_lp'] = np.log(dat['lp'])
dat['ln_rk'] = np.log(dat['rk'])

# Panel structure
print(f"Countries: {dat['country'].nunique()}")
print(f"Years: {dat['year'].nunique()}")
print(f"Total observations: {len(dat)}")

# Variance decomposition
overall_var = dat['ln_lp'].var()
between_var = dat.groupby('country')['ln_lp'].mean().var()
within_var = dat.groupby('country')['ln_lp'].apply(lambda x: x - x.mean()).var()
print(f"Overall variance: {overall_var:.4f}")
print(f"Between variance: {between_var:.4f}")
print(f"Within variance: {within_var:.4f}")
```

Which source of variation dominates? What does this imply for the choice between pooled OLS and fixed effects?

---

#### Task 2: Pooled OLS with Cluster-Robust SEs (Guided)

Estimate a pooled OLS regression of log productivity on log physical capital and human capital. Compare default and cluster-robust standard errors (clustered by country).

```python
from statsmodels.formula.api import ols

model_default = ols('ln_lp ~ ln_rk + hc', data=dat).fit()
model_cluster = ols('ln_lp ~ ln_rk + hc', data=dat).fit(
    cov_type='cluster', cov_kwds={'groups': dat['country']}
)

print("Default SE:", model_default.bse.round(4).to_dict())
print("Cluster SE:", model_cluster.bse.round(4).to_dict())
print("Ratio:", (model_cluster.bse / model_default.bse).round(2).to_dict())
```

How much larger are cluster SEs? What does this tell you about within-country correlation?

---

#### Task 3: Fixed Effects Estimation (Semi-guided)

Estimate a fixed effects model controlling for country-specific characteristics. Compare the FE coefficients with the pooled OLS coefficients.

*Hint:* Use `linearmodels.panel.PanelOLS` with `entity_effects=True`, or use the within transformation manually by de-meaning the variables by country.

Which coefficients change most? What unobserved country characteristics might be driving the difference?

---

#### Task 4: Time Trends in Productivity (Semi-guided)

Add a time trend or year fixed effects to the panel model. Test whether productivity growth rates differ across regions.

*Hint:* Use `time_effects=True` in PanelOLS for year fixed effects, or create region-year interaction terms.

Is there evidence of convergence (faster growth in initially poorer countries)?

---

#### Task 5: Regional Heterogeneity with Interactions (Independent)

Estimate models that allow the returns to physical and human capital to vary by region:
1. Add region dummy variables
2. Add region-capital interaction terms
3. Test the joint significance of regional interactions

Do returns to capital differ significantly across regions? Which regions show the highest returns to human capital?

---

#### Task 6: Policy Brief on Capital and Productivity (Independent)

Write a 200-300 word policy brief addressing: What are the most effective channels for increasing labor productivity across countries? Your brief should:

1. Compare pooled OLS and fixed effects estimates of capital returns
2. Discuss whether the relationship is causal (what are the threats to identification?)
3. Evaluate whether returns to capital differ by region
4. Recommend policies based on the relative importance of physical vs. human capital

> **Key Concept: Panel Data for Cross-Country Analysis**
>
> Cross-country panel data enables controlling for time-invariant country characteristics (institutions, geography, culture) that confound cross-sectional estimates. Fixed effects absorb these permanent differences, identifying the relationship between capital accumulation and productivity growth from within-country variation over time. The typical finding is that FE coefficients are smaller than pooled OLS, indicating positive omitted variable bias in cross-sectional estimates.

> **Key Concept: Choosing Between Panel Data Estimators**
>
> The choice between pooled OLS, fixed effects, and random effects depends on the research question and data structure. Use pooled OLS with cluster SEs for descriptive associations; use FE when unobserved individual heterogeneity is likely correlated with regressors (the common case); use RE only when individual effects are plausibly random and uncorrelated with regressors (e.g., randomized experiments). The Hausman test helps decide between FE and RE, but economic reasoning should guide the choice.

**What You've Learned:**
In this case study, you applied the complete panel data toolkit to cross-country productivity analysis. You decomposed variation into within and between components, compared pooled OLS with fixed effects, examined cluster-robust standard errors, and explored regional heterogeneity. These methods are essential for any empirical analysis using panel data.
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
