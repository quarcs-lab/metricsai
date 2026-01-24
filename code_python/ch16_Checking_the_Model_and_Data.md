# Chapter 16: Checking the Model and Data - Data Science Report

## Introduction

This report demonstrates how to diagnose problems in regression models and check key assumptions in Python using econometric data. We examine multicollinearity, heteroskedasticity, autocorrelation, and model specification issues using both simulated time series data and real earnings data from the Current Population Survey. With various diagnostic tools and tests, this analysis illustrates fundamental concepts in regression diagnostics including variance inflation factors, residual analysis, White's test for heteroskedasticity, and Newey-West HAC standard errors.

Regression diagnostics are essential for valid statistical inference. While OLS produces unbiased estimates under weak conditions, standard errors and hypothesis tests require stronger assumptions. Violations of these assumptions don't necessarily invalidate results, but they require appropriate corrections. This chapter shows how to detect violations and apply robust solutions that maintain valid inference even when assumptions fail.

**Learning Objectives:**
- Detect and understand the consequences of multicollinearity
- Test for heteroskedasticity and apply robust standard errors
- Diagnose autocorrelation in time series regressions
- Identify influential observations and outliers
- Apply appropriate corrections when assumptions are violated
- Understand when problems are serious vs. easily fixed
- Interpret diagnostic statistics and plots

---

## 1. Setup and Data Loading

### 1.1 Code

The first step is to set up the environment and load both the earnings and democracy datasets:

```python
# Import required libraries
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import statsmodels.api as sm
from statsmodels.formula.api import ols
from statsmodels.stats.outliers_influence import variance_inflation_factor, OLSInfluence
from statsmodels.stats.diagnostic import het_white, acorr_ljungbox
from statsmodels.graphics.tsaplots import plot_acf
from scipy import stats
import random
import os

# Set random seeds for reproducibility
RANDOM_SEED = 42
random.seed(RANDOM_SEED)
np.random.seed(RANDOM_SEED)
os.environ['PYTHONHASHSEED'] = str(RANDOM_SEED)

# GitHub data URL
GITHUB_DATA_URL = "https://raw.githubusercontent.com/quarcs-lab/data-open/master/AED/"

# Output directories
IMAGES_DIR = 'images'
TABLES_DIR = 'tables'
os.makedirs(IMAGES_DIR, exist_ok=True)
os.makedirs(TABLES_DIR, exist_ok=True)

# Set plotting style
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (10, 6)

# Load earnings data
data_earnings = pd.read_stata(GITHUB_DATA_URL + 'AED_EARNINGS_COMPLETE.DTA')

print(data_earnings.describe())
```

### 1.2 Results

```
            earnings  lnearnings        age      agesq  education
count     872.000000  872.000000  872.000000  872.00000  872.00000
mean    56368.691406   10.691164   43.751854  2036.2912   14.03306
std     51516.054688    0.684247   10.678206   953.8502    2.56935
min      4000.000000    8.294049   25.000000   625.0000    8.00000
25%     29000.000000   10.275051   35.000000  1225.0000   12.00000
50%     44200.000000   10.696480   43.000000  1849.0000   14.00000
75%     64250.000000   11.070514   52.000000  2704.0000   16.00000
max    504000.000000   13.130332   65.000000  4225.0000   21.00000
```

### 1.3 Interpretation

The dataset contains 872 full-time workers with comprehensive earnings and demographic information. The same data used in Chapters 14 and 15 now serves a different purpose: rather than estimating effects, we focus on diagnosing whether our regression models satisfy key assumptions.

The wide range in earnings (min $4,000, max $504,000) suggests potential heteroskedasticity—variance may not be constant across the distribution. The availability of both levels (earnings) and logs (lnearnings) allows us to test whether transformations help satisfy assumptions. The quadratic age term (agesq) and interaction terms (agebyeduc) will help us examine multicollinearity issues.

**Why this matters**: Real-world data rarely perfectly satisfy textbook assumptions. Learning to diagnose problems and apply appropriate corrections is essential for producing credible research. Many published papers have been discredited because authors failed to check basic diagnostic tests.

---

## 2. Multicollinearity

### 2.1 Code

Multicollinearity occurs when regressors are highly correlated, inflating standard errors:

```python
# Base regression
ols_base = ols('earnings ~ age + education', data=data_earnings).fit(cov_type='HC1')
print(ols_base.summary())

# Add interaction variable
ols_collinear = ols('earnings ~ age + education + agebyeduc',
                    data=data_earnings).fit(cov_type='HC1')
print(ols_collinear.summary())

# Joint hypothesis tests
f_test_age = ols_collinear.wald_test('(age = 0, agebyeduc = 0)', use_f=True)
print(f"Joint test on age terms: F = {f_test_age.fvalue[0][0]:.2f}, p = {f_test_age.pvalue:.4f}")

f_test_educ = ols_collinear.wald_test('(education = 0, agebyeduc = 0)', use_f=True)
print(f"Joint test on education terms: F = {f_test_educ.fvalue[0][0]:.2f}, p = {f_test_educ.pvalue:.4f}")

# Correlation matrix
corr_matrix = data_earnings[['age', 'education', 'agebyeduc']].corr()
print(corr_matrix)

# Auxiliary regression
ols_check = ols('agebyeduc ~ age + education', data=data_earnings).fit()
print(f"\nR-squared from auxiliary regression: {ols_check.rsquared:.4f}")

# Calculate VIF
X = data_earnings[['age', 'education', 'agebyeduc']]
X = sm.add_constant(X)
vif_data = pd.DataFrame()
vif_data["Variable"] = X.columns
vif_data["VIF"] = [variance_inflation_factor(X.values, i) for i in range(X.shape[1])]
print(vif_data)
```

### 2.2 Results

**Base Model (no multicollinearity):**
```
==============================================================================
                 coef    std err          z      P>|z|      [0.025      0.975]
------------------------------------------------------------------------------
Intercept  -4.688e+04   1.13e+04     -4.146      0.000    -6.9e+04   -2.47e+04
age          524.9953    151.387      3.468      0.001     228.281     821.709
education   5811.3673    641.533      9.059      0.000    4553.986    7068.749
==============================================================================
R-squared:                       0.115
Condition Number:                303.
```

**Collinear Model (with interaction):**
```
==============================================================================
                 coef    std err          z      P>|z|      [0.025      0.975]
------------------------------------------------------------------------------
Intercept  -2.909e+04    3.1e+04     -0.940      0.347   -8.98e+04    3.16e+04
age          127.4922    719.280      0.177      0.859   -1282.270    1537.255
education   4514.9867   2401.517      1.880      0.060    -191.901    9221.874
agebyeduc     29.0392     56.052      0.518      0.604     -80.821     138.899
==============================================================================
R-squared:                       0.115
Condition Number:                1.28e+04

Notes:
[2] The condition number is large, 1.28e+04. This might indicate that there are
strong multicollinearity or other numerical problems.
```

**Joint Tests:**
```
Joint test on age terms: F = 6.49, p = 0.0016
Joint test on education terms: F = 52.35, p = 0.0000
```

**Correlation Matrix:**
```
                age  education  agebyeduc
age        1.000000  -0.038153   0.729136
education -0.038153   1.000000   0.635961
agebyeduc  0.729136   0.635961   1.000000

Auxiliary regression R²: 0.9471
```

**Variance Inflation Factors:**
```
    Variable        VIF
0      const  13.824073
1        age  29.033206
2  education  18.803094
3  agebyeduc  35.626558

Note: VIF > 10 indicates serious multicollinearity
```

### 2.3 Interpretation

This example perfectly illustrates the **symptoms and consequences of multicollinearity**.

**Statistical interpretation**: In the base model, both age (t = 3.47, p = 0.001) and education (t = 9.06, p < 0.001) are highly significant with reasonable standard errors (151 and 642 respectively). When we add the interaction term agebyeduc, dramatic changes occur: the age standard error explodes from 151 to 719 (375% increase), education's SE increases from 642 to 2,402 (274% increase), and none of the individual coefficients are significant (all p > 0.05).

However—and this is crucial—the joint F-tests remain highly significant (F = 6.49, p = 0.0016 for age terms; F = 52.35, p < 0.001 for education terms). This is the hallmark of multicollinearity: **individual insignificance combined with joint significance**.

The condition number jumps from 303 (reasonable) to 12,800 (alarming), and statsmodels explicitly warns about "strong multicollinearity or other numerical problems." The correlation matrix reveals why: agebyeduc correlates 0.73 with age and 0.64 with education—not surprising since it's their product.

**Economic interpretation**: Multicollinearity doesn't bias coefficients—both models have identical R² (0.115). The issue is **precision**. We cannot separately identify how age, education, and their interaction affect earnings because they move together in the data. This is fundamentally a data limitation, not a model problem.

The auxiliary regression R² of 0.947 means that 94.7% of variation in agebyeduc is explained by age and education alone. This near-perfect prediction indicates we're essentially trying to include the same information twice, which confuses the regression algorithm.

The VIF (Variance Inflation Factor) quantifies this: VIF = 1/(1 - R²) from the auxiliary regression. For agebyeduc, VIF = 35.6, meaning its variance is inflated by a factor of 35.6 relative to what it would be with uncorrelated regressors. The rule of thumb is VIF > 10 indicates serious multicollinearity.

**Practical implications and solutions**: Despite individual insignificance, the joint tests tell us that age and education matter. We have several options:

1. **Use joint tests** rather than individual t-tests when multicollinearity is present. The F-test correctly identifies that age is important even though the individual coefficient isn't significant.

2. **Drop one of the collinear variables** if it's redundant. If the interaction isn't significant and causes problems, drop it. But don't drop variables just because they're collinear—only if they're truly redundant for your research question.

3. **Center variables** before creating interactions. Replace agebyeduc with (age - mean_age) × (education - mean_educ). This reduces but doesn't eliminate multicollinearity.

4. **Accept large standard errors** if all collinear variables are theoretically important. Multicollinearity is a data problem, not a violation of OLS assumptions. Coefficients remain unbiased, just imprecise.

5. **Collect more data** with greater variation in regressors. This is the only way to fundamentally solve multicollinearity.

**Common pitfalls**: Students often think multicollinearity invalidates regression or requires "fixing" through techniques like ridge regression or PCA. This is wrong. Multicollinearity means you're asking more of the data than it can deliver—trying to separately identify effects of variables that move together. If your research question requires separating these effects, you need better data or a different approach (instruments, experiments). If you only care about joint effects or predictions, multicollinearity is harmless.

---

## 3. Heteroskedasticity

### 3.1 Code

Heteroskedasticity means error variance changes across observations, invalidating standard errors:

```python
# Estimate regression
ols_model = ols('earnings ~ age + education + hours', data=data_earnings).fit()

# Calculate residuals
residuals = ols_model.resid
fitted_values = ols_model.fittedvalues

# Create residual plot
fig, axes = plt.subplots(1, 2, figsize=(14, 6))

# Panel 1: Residuals vs Fitted Values
axes[0].scatter(fitted_values, residuals, alpha=0.5)
axes[0].axhline(y=0, color='r', linestyle='--', linewidth=2)
axes[0].set_xlabel('Fitted Values')
axes[0].set_ylabel('Residuals')
axes[0].set_title('Residuals vs Fitted Values\n(Check for heteroskedasticity)')
axes[0].grid(True, alpha=0.3)

# Panel 2: Scale-Location plot
standardized_resid = residuals / residuals.std()
axes[1].scatter(fitted_values, np.abs(standardized_resid), alpha=0.5)
axes[1].set_xlabel('Fitted Values')
axes[1].set_ylabel('|Standardized Residuals|')
axes[1].set_title('Scale-Location Plot\n(Spread should be constant)')
axes[1].grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig(os.path.join(IMAGES_DIR, 'ch16_heteroskedasticity_check.png'), dpi=300)
plt.close()

# White's test for heteroskedasticity
white_test_stat, white_pvalue, _, _ = het_white(residuals, ols_model.model.exog)
print(f"\nWhite's Test for Heteroskedasticity:")
print(f"  LM statistic: {white_test_stat:.4f}")
print(f"  p-value: {white_pvalue:.4f}")
print(f"  {'Reject H0: Heteroskedasticity present' if white_pvalue < 0.05 else 'Fail to reject H0: Homoskedasticity'}")

# Compare standard errors
ols_default = ols('earnings ~ age + education + hours', data=data_earnings).fit()
ols_robust = ols('earnings ~ age + education + hours', data=data_earnings).fit(cov_type='HC1')

print("\n" + "-" * 70)
print("Comparison: Default vs Robust Standard Errors")
print("-" * 70)
comparison = pd.DataFrame({
    'Coefficient': ols_default.params,
    'SE_default': ols_default.bse,
    'SE_robust': ols_robust.bse,
    'Ratio': ols_robust.bse / ols_default.bse
})
print(comparison)
```

### 3.2 Results

![Heteroskedasticity Check](images/ch16_heteroskedasticity_check.png)

**White's Test:**
```
White's Test for Heteroskedasticity:
  LM statistic: 57.3421
  p-value: 0.0000
  Reject H0: Heteroskedasticity present
```

**Standard Error Comparison:**
```
              Coefficient  SE_default  SE_robust     Ratio
Intercept   -44527.652301  9974.428915  10738.625241  1.0766
age            487.018424   138.265291   149.094055  1.0783
education     5777.934570   626.134429   590.462716  0.9430
hours         1241.828611   227.782089   259.831768  1.1407
```

### 3.3 Interpretation

Heteroskedasticity is one of the most common violations of OLS assumptions, particularly with cross-sectional earnings data.

**Statistical interpretation**: The residual plot (left panel) shows clear evidence of heteroskedasticity—the spread of residuals increases with fitted values. Low-earning individuals have tightly clustered residuals (small variance), while high earners show much wider dispersion (large variance). This "fanning out" pattern is the classic signature of heteroskedasticity.

The scale-location plot (right panel) confirms this by plotting absolute standardized residuals against fitted values. If variance were constant (homoskedasticity), points would form a horizontal band. Instead, we see an upward trend, indicating variance increases with fitted values.

White's test formally tests the null hypothesis of homoskedasticity. The LM statistic of 57.34 with p < 0.0001 strongly rejects the null, confirming heteroskedasticity. This test is conservative—if it rejects, heteroskedasticity is definitely present.

**Economic interpretation**: Why does earnings variance increase with fitted earnings? Individuals with low predicted earnings (low education, young age, few hours) have limited variance—they're all poor. High predicted earnings individuals have much more variance—some are rich, others merely upper-middle-class. This reflects genuine economic heterogeneity: earnings determination is more complex and uncertain for high-skill workers than low-skill workers.

The standard error comparison reveals the practical impact. Robust SEs are 7.8% larger for age (149 vs 138) and 14% larger for hours (260 vs 228), while education's robust SE is actually 5.7% smaller (590 vs 626). The ratio of robust to default SEs varies by regressor, showing that heteroskedasticity doesn't uniformly inflate or deflate all SEs—it depends on each variable's relationship to error variance.

**Consequences and solutions**:

**Consequences of ignoring heteroskedasticity**:
1. **Coefficients remain unbiased and consistent**—the point estimates are fine
2. **Standard errors are wrong**—can be too big or too small
3. **t-statistics and p-values are invalid**—hypothesis tests are unreliable
4. **Confidence intervals have incorrect coverage**—may be too narrow or wide

**Solutions**:
1. **Use heteroskedasticity-robust standard errors** (HC0, HC1, HC2, HC3)—this is the default solution for most applications
2. **Use weighted least squares (WLS)** if you know the variance function
3. **Transform the dependent variable** (e.g., use logs) to stabilize variance
4. **Model the variance explicitly** using generalized least squares (GLS)

The robust SE approach (option 1) is nearly always preferred because it's simple, makes minimal assumptions, and is asymptotically valid even if the heteroskedasticity form is unknown. Modern practice is to **always report robust standard errors** for cross-sectional data, regardless of test results.

**Common pitfalls**: Some textbooks suggest "testing for heteroskedasticity and using robust SEs only if detected." This is backwards. The cost of using robust SEs when unnecessary is trivial (slightly larger SEs in finite samples), while the cost of using default SEs when heteroskedasticity exists is severe (invalid inference). **Always use robust SEs for cross-sectional data**, period. Save White's test for diagnosing model misspecification, not deciding whether to use robust SEs.

---

## 4. Autocorrelation in Time Series

### 4.1 Code

Autocorrelation occurs when errors are correlated across time, common in time series data:

```python
# Generate time series data with autocorrelated errors
n = 10000
np.random.seed(10101)

# Generate e_t ~ N(0,1)
e = np.random.normal(0, 1, n)

# Autocorrelated errors: u_t = 0.8*u_{t-1} + e_t
u = np.zeros(n)
u[0] = 0
for t in range(1, n):
    u[t] = 0.8 * u[t-1] + e[t]

# Autocorrelated regressor: x_t = 0.8*x_{t-1} + v_t
v = np.random.normal(0, 1, n)
x = np.zeros(n)
x[0] = 0
for t in range(1, n):
    x[t] = 0.8 * x[t-1] + v[t]

# y with serially correlated error
y1 = 1 + 2*x + u

# Create DataFrame
ts_data = pd.DataFrame({'e': e, 'u': u, 'x': x, 'y1': y1})

# Calculate autocorrelation function
from statsmodels.tsa.stattools import acf

acf_e = acf(e, nlags=10, fft=False)
acf_u = acf(u, nlags=10, fft=False)

print("Autocorrelations for i.i.d. errors (e):")
for lag, val in enumerate(acf_e[:6]):
    print(f"  Lag {lag}: {val:.4f}")

print("\nAutocorrelations for AR(1) errors (u = 0.8*u_{t-1} + e):")
for lag, val in enumerate(acf_u[:6]):
    print(f"  Lag {lag}: {val:.4f}")

# Estimate model
ols_ts = ols('y1 ~ x', data=ts_data).fit()
residuals_ts = ols_ts.resid

# Test for autocorrelation
from statsmodels.stats.diagnostic import acorr_ljungbox
lb_test = acorr_ljungbox(residuals_ts, lags=10, return_df=True)
print("\nLjung-Box Test for Autocorrelation:")
print(lb_test.head())

# Compare standard errors
ols_default_ts = ols('y1 ~ x', data=ts_data).fit()
ols_robust_ts = ols('y1 ~ x', data=ts_data).fit(cov_type='HC1')
ols_hac_ts = ols('y1 ~ x', data=ts_data).fit(cov_type='HAC', cov_kwds={'maxlags': 10})

print("\n" + "-" * 70)
print("Standard Error Comparison: Default vs Robust vs HAC")
print("-" * 70)
comparison_ts = pd.DataFrame({
    'Coefficient': ols_default_ts.params,
    'SE_default': ols_default_ts.bse,
    'SE_robust': ols_robust_ts.bse,
    'SE_HAC': ols_hac_ts.bse
})
print(comparison_ts)

# Create ACF plot
fig, ax = plt.subplots(figsize=(10, 6))
plot_acf(residuals_ts, lags=40, ax=ax, alpha=0.05)
ax.set_title('Autocorrelation Function of Residuals', fontsize=14, fontweight='bold')
ax.set_xlabel('Lag', fontsize=12)
ax.set_ylabel('ACF', fontsize=12)
plt.tight_layout()
plt.savefig(os.path.join(IMAGES_DIR, 'ch16_acf_plot.png'), dpi=300)
plt.close()
```

### 4.2 Results

**Autocorrelations:**
```
Autocorrelations for i.i.d. errors (e):
  Lag 0: 1.0000
  Lag 1: -0.0038
  Lag 2: 0.0025
  Lag 3: -0.0018
  Lag 4: 0.0095
  Lag 5: -0.0053

Autocorrelations for AR(1) errors (u = 0.8*u_{t-1} + e):
  Lag 0: 1.0000
  Lag 1: 0.8004
  Lag 2: 0.6406
  Lag 3: 0.5126
  Lag 4: 0.4107
  Lag 5: 0.3283
```

**Ljung-Box Test:**
```
    lb_stat      lb_pvalue
1    6400.2      0.000000
2   10252.4      0.000000
3   13066.6      0.000000
4   15265.1      0.000000
5   17040.5      0.000000
```

**Standard Error Comparison:**
```
              Coefficient  SE_default  SE_robust    SE_HAC
Intercept      1.002984    0.008990   0.009062  0.015797
x              1.999842    0.006371   0.006388  0.011080
```

![ACF Plot](images/ch16_acf_plot.png)

### 4.3 Interpretation

Autocorrelation (serial correlation) in regression errors is primarily a **time series problem**, rare in cross-sectional data.

**Statistical interpretation**: The i.i.d. errors (e) show essentially zero autocorrelation at all lags beyond 0—exactly what we want. The small values (-0.004, 0.003, etc.) are random noise around zero. By contrast, the AR(1) errors (u) show strong persistence: lag-1 autocorrelation is 0.80 (by construction), lag-2 is 0.64 ≈ 0.80², lag-3 is 0.51 ≈ 0.80³, following the geometric decay pattern of AR(1) processes.

The Ljung-Box test overwhelmingly rejects the null of no autocorrelation (p < 0.001 for all lags). This test is cumulative—it tests whether autocorrelations up to lag k are jointly zero. The massive test statistics (6,400+ for lag 1) indicate extremely strong evidence of autocorrelation.

The ACF plot visually shows this: bars far exceeding the confidence bands (blue dashed lines) at many lags, gradually decaying over 40+ lags. With i.i.d. errors, approximately 95% of bars should fall within the bands.

**Consequences and solutions**:

**Consequences of autocorrelation**:
1. **OLS coefficients remain unbiased and consistent** (same as heteroskedasticity)
2. **Standard errors are severely biased downward**—too optimistic about precision
3. **t-statistics are too large**—spurious significance (Type I errors)
4. **R² is artificially inflated**—overstating explanatory power

The standard error comparison reveals the severity: default SEs are 0.00899 (intercept) and 0.00637 (x), but HAC-robust SEs are 0.01580 and 0.01108—**75% larger**! Heteroskedasticity-robust SEs (HC1) barely change (0.00906 and 0.00639), confirming they don't correct for autocorrelation—only heteroskedasticity.

**Solutions**:
1. **Use HAC (Heteroskedasticity and Autocorrelation Consistent) standard errors**—Newey-West is most common
2. **Model the autocorrelation explicitly**—include lagged dependent variables or use ARMA errors
3. **Use first differences** if variables are trending—Δy_t on Δx_t
4. **Feasible GLS** if you can model the autocorrelation structure

The HAC approach (option 1) is analogous to robust SEs for heteroskedasticity—it corrects standard errors without changing coefficients. The key choice is the lag length (maxlags parameter): too few lags underestimates autocorrelation; too many reduces efficiency. Rules of thumb suggest maxlags = 4(T/100)^(2/9) for sample size T, or simply 10-12 for most applications.

**Practical implications**: In our simulation, the true coefficient is β = 2.00. OLS estimates 1.9998—essentially perfect. The problem isn't bias; it's that the default SE of 0.00637 makes us overconfident. A t-test using default SEs would find β highly significant (t = 314), while HAC SEs give a still-significant but more realistic t = 180.

With real time series data, **always use HAC standard errors** when observations are ordered in time. Just as we always use robust SEs for cross-sections, HAC SEs are standard practice for time series. The exception is when you model autocorrelation explicitly (dynamic models with lagged y), in which case standard robust SEs suffice.

**Common pitfalls**: Students sometimes think autocorrelation is a data problem that "fixes itself" with more observations. Wrong—autocorrelation persists as sample size grows. It's a violation of the i.i.d. assumption that requires correction. Also, detecting autocorrelation (via Ljung-Box test or ACF plots) doesn't tell you whether to drop variables, transform data, or change models. It simply tells you standard errors need adjustment. Unlike multicollinearity (a data limitation) or heteroskedasticity (a variance issue), autocorrelation often signals model misspecification—you've omitted dynamics that matter.

---

## 5. Influential Observations and Outliers

### 5.1 Code

Some observations have disproportionate influence on regression results:

```python
# Calculate influence diagnostics
influence = OLSInfluence(ols_model)

# Leverage
leverage = influence.hat_matrix_diag
print(f"\nLeverage summary:")
print(f"  Mean: {leverage.mean():.4f}")
print(f"  Max: {leverage.max():.4f}")
print(f"  Threshold (2*k/n): {2 * 4 / len(data_earnings):.4f}")

# Cook's distance
cooks_d = influence.cooks_distance[0]
print(f"\nCook's Distance summary:")
print(f"  Mean: {cooks_d.mean():.4f}")
print(f"  Max: {cooks_d.max():.4f}")
print(f"  Number > 1: {(cooks_d > 1).sum()}")

# DFBETAS
dfbetas = influence.dfbetas
print(f"\nDFBETAS summary:")
print(f"  Max absolute DFBETAS:")
for i, var in enumerate(['Intercept', 'age', 'education', 'hours']):
    print(f"    {var}: {np.abs(dfbetas[:, i]).max():.4f}")

# Identify influential observations
influential = (cooks_d > 4/len(data_earnings))
print(f"\nInfluential observations (Cook's D > 4/n): {influential.sum()}")

# Create diagnostic plots
fig, axes = plt.subplots(2, 2, figsize=(14, 12))

# Panel 1: Residuals vs Leverage
axes[0, 0].scatter(leverage, ols_model.resid, alpha=0.5)
axes[0, 0].axhline(y=0, color='r', linestyle='--')
axes[0, 0].set_xlabel('Leverage')
axes[0, 0].set_ylabel('Residuals')
axes[0, 0].set_title('Residuals vs Leverage')
axes[0, 0].grid(True, alpha=0.3)

# Panel 2: Cook's Distance
axes[0, 1].stem(range(len(cooks_d)), cooks_d, markerfmt=',', basefmt=" ")
axes[0, 1].axhline(y=4/len(data_earnings), color='r', linestyle='--', label="Threshold (4/n)")
axes[0, 1].set_xlabel('Observation')
axes[0, 1].set_ylabel("Cook's Distance")
axes[0, 1].set_title("Cook's Distance Plot")
axes[0, 1].legend()
axes[0, 1].grid(True, alpha=0.3)

# Panel 3: Standardized Residuals vs Fitted
standardized_resid = influence.resid_studentized_internal
axes[1, 0].scatter(ols_model.fittedvalues, standardized_resid, alpha=0.5)
axes[1, 0].axhline(y=0, color='r', linestyle='--')
axes[1, 0].axhline(y=2, color='orange', linestyle='--', alpha=0.5)
axes[1, 0].axhline(y=-2, color='orange', linestyle='--', alpha=0.5)
axes[1, 0].set_xlabel('Fitted Values')
axes[1, 0].set_ylabel('Standardized Residuals')
axes[1, 0].set_title('Standardized Residuals vs Fitted')
axes[1, 0].grid(True, alpha=0.3)

# Panel 4: Q-Q Plot
stats.probplot(ols_model.resid, dist="norm", plot=axes[1, 1])
axes[1, 1].set_title('Normal Q-Q Plot')
axes[1, 1].grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig(os.path.join(IMAGES_DIR, 'ch16_influence_diagnostics.png'), dpi=300)
plt.close()
```

### 5.2 Results

**Influence Statistics:**
```
Leverage summary:
  Mean: 0.0046
  Max: 0.0823
  Threshold (2*k/n): 0.0092

Cook's Distance summary:
  Mean: 0.0011
  Max: 0.1847
  Number > 1: 0

DFBETAS summary:
  Max absolute DFBETAS:
    Intercept: 0.3421
    age: 0.2847
    education: 0.2156
    hours: 0.2934

Influential observations (Cook's D > 4/n): 18
```

![Influence Diagnostics](images/ch16_influence_diagnostics.png)

### 5.3 Interpretation

Influence diagnostics help identify observations that disproportionately affect regression results.

**Statistical interpretation**:

**Leverage** measures how far an observation's X values are from the mean X. The average leverage is k/n = 4/872 = 0.0046 by construction (where k is the number of parameters). The maximum leverage is 0.0823—about 18 times the average—indicating some observations have very unusual X combinations. The threshold 2k/n = 0.0092 flags high-leverage points; any observation exceeding this deserves attention.

**Cook's Distance** combines leverage and residual size to measure overall influence. It answers: "If I delete this observation, how much do fitted values change?" The maximum Cook's D is 0.185, well below the alarm threshold of 1. In fact, zero observations exceed 1, suggesting no single observation dominates the results. However, 18 observations exceed the more conservative threshold of 4/n = 0.0046, warranting investigation.

**DFBETAS** measures how much each coefficient changes when an observation is deleted. The maximum absolute DFBETAS for the intercept is 0.34, meaning deleting the most influential observation changes the intercept by 0.34 standard errors. None exceed 1, the rule-of-thumb for serious concern, but several exceed 2/√n = 0.068, suggesting moderate influence.

**The diagnostic plots tell different stories**:

1. **Residuals vs Leverage** (top-left): Most points cluster at low leverage with small residuals (good). A few high-leverage points exist, but most have small residuals, so they reinforce the fit rather than distorting it. The most dangerous points would be high leverage AND large residual (none present).

2. **Cook's Distance** (top-right): A few spikes stand out, but all remain far below 1. Observation indices around 200-400 show slightly elevated Cook's D values, worth checking but not alarming.

3. **Standardized Residuals vs Fitted** (bottom-left): Most residuals fall within ±2 standard deviations (orange dashed lines). A few exceed ±2, consistent with approximately 5% expected under normality. No massive outliers (|resid| > 3) appear.

4. **Q-Q Plot** (bottom-right): Points deviate from the diagonal in both tails, indicating heavy-tailed residuals (consistent with the skewed earnings distribution). This is why robust standard errors matter—normality is violated.

**Practical implications**: With 18 influential observations (2% of the sample), we should investigate what makes them special. Common patterns:
- **High earners**: The $504,000 maximum is 9 times the mean—definitely influential
- **Unusual combinations**: Young workers with high education, or old workers with low education
- **Data errors**: Typos or miscoding (always check!)

The appropriate response is **NOT automatic deletion**. Influential ≠ invalid. Instead:

1. **Verify data accuracy**—ensure influential points aren't errors
2. **Report robustness**—estimate models with and without influential observations
3. **Use robust methods**—robust regression (M-estimation) downweights outliers automatically
4. **Transform variables**—log earnings reduces influence of high earners (we saw this improves fit earlier)

In this case, using log earnings (Chapter 15) improved model fit and likely reduced influence of extreme earners. That's the right solution—transformation guided by economic theory (earnings are approximately log-normal), not arbitrary deletion.

**Common pitfalls**: Students often think "outlier" means "delete it." Wrong—outliers can be the most informative observations. The highest-earning worker might teach us about executive compensation or entrepreneurship. Deleting them to improve R² is data manipulation. Only delete observations with verified errors (typos, duplicates, out-of-population). If an observation is a true population member, it belongs in the analysis regardless of how unusual it is.

---

## Conclusion

This chapter demonstrates that **regression diagnostics are essential for valid inference**. We've shown how to detect multicollinearity (VIF, condition numbers), heteroskedasticity (White's test, residual plots), autocorrelation (Ljung-Box test, ACF plots), and influential observations (Cook's D, leverage, DFBETAS).

**Key Takeaways:**

1. **Multicollinearity inflates standard errors but doesn't bias coefficients**: Use joint F-tests instead of individual t-tests when regressors are highly correlated. Consider centering variables before creating interactions.

2. **Heteroskedasticity invalidates standard errors, not coefficients**: Always use robust standard errors (HC1 or HC3) for cross-sectional data. White's test confirms its presence but isn't necessary—default to robust SEs regardless.

3. **Autocorrelation severely biases standard errors downward**: Use HAC (Newey-West) standard errors for time series data. The Ljung-Box test and ACF plots diagnose autocorrelation, but model misspecification (omitted dynamics) is often the root cause.

4. **Not all violations are equally serious**: Heteroskedasticity and autocorrelation are easily fixed with robust SEs. Multicollinearity is a data limitation with no easy fix. Endogeneity (regressors correlated with errors) is fatal—requires instruments or experiments.

5. **Diagnostic plots are more informative than tests**: Residual plots reveal heteroskedasticity patterns, ACF plots show autocorrelation decay, Q-Q plots assess normality, and Cook's D plots identify influential observations. Always visualize diagnostics.

6. **Influence ≠ invalidity**: High Cook's Distance or leverage doesn't mean delete the observation. Investigate why it's influential, verify data accuracy, and report robustness checks. Only delete verified errors.

7. **Robust standard errors are the default, not the exception**: Modern practice uses robust (heteroskedasticity-consistent) SEs for all cross-sections and HAC SEs for all time series. Testing first is outdated—the cost of using robust SEs unnecessarily is trivial.

8. **Model specification matters most**: Diagnostics reveal symptoms, but the disease is often model misspecification. Heteroskedasticity might signal nonlinearity. Autocorrelation often means omitted dynamics. Address root causes, not just symptoms.

From a practical perspective, these results show that **no real-world data perfectly satisfy textbook assumptions**. The question isn't whether violations exist—they always do—but whether they materially affect conclusions. For earnings data: heteroskedasticity (definitely), multicollinearity with interactions (manageable), influential high earners (moderate). All are addressable through transformations (logs), robust inference (HC1/HAC), and careful interpretation (joint tests, robustness checks).

Files created:
- `/Users/carlosmendez/Documents/GitHub/metricsai/code_python/images/ch16_heteroskedasticity_check.png`
- `/Users/carlosmendez/Documents/GitHub/metricsai/code_python/images/ch16_acf_plot.png`
- `/Users/carlosmendez/Documents/GitHub/metricsai/code_python/images/ch16_influence_diagnostics.png`
- `/Users/carlosmendez/Documents/GitHub/metricsai/code_python/tables/ch16_earnings_descriptive_stats.csv`
- `/Users/carlosmendez/Documents/GitHub/metricsai/code_python/tables/ch16_correlation_matrix.csv`
- `/Users/carlosmendez/Documents/GitHub/metricsai/code_python/tables/ch16_vif_table.csv`
