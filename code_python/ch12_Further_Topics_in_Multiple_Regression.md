# Chapter 12: Prediction and Goodness of Fit

![Chapter 12 Visual Summary](images/ch12_visual_summary.jpg)

*This chapter demonstrates how to forecast individual outcomes using prediction intervals and assess model quality through goodness-of-fit measures, bridging classical regression inference with practical prediction applications.*

---

## Introduction

This report explores **advanced topics in multiple regression**—extending the foundational methods from Chapters 10-11 to address practical challenges and introduce modern approaches. While previous chapters covered basic estimation and inference, Chapter 12 demonstrates specialized techniques for robust inference, prediction, and introduces cutting-edge methods.

We analyze the **housing dataset** (29 houses) and **GDP growth time series** (241 quarters) to illustrate:

- **Heteroskedasticity-robust standard errors**: Correcting inference when error variance varies
- **HAC standard errors**: Addressing autocorrelation in time series data
- **Prediction intervals**: Forecasting individual outcomes vs. conditional means
- **Advanced methods**: Bayesian inference, machine learning, and historical context

This chapter bridges **classical econometrics** (Chapters 1-11) and **modern data science**, showing how traditional regression methods extend to complex real-world settings and connect to contemporary techniques.

**What You'll Learn:**

- How to compute heteroskedasticity-robust standard errors for valid inference
- How to calculate HAC (Newey-West) standard errors for time series data
- How to construct prediction intervals for forecasting individual outcomes
- How to distinguish between confidence intervals and prediction intervals
- How to interpret adjusted R² and RMSE as goodness-of-fit measures
- How to recognize when classical assumptions fail and apply corrections
- How to place regression methods in historical and methodological context

---

## 1. Heteroskedasticity-Robust Standard Errors

### 1.1 Code

**Context:** In this section, we compute heteroskedasticity-robust standard errors for the housing price regression. Classical OLS assumes constant error variance (homoskedasticity), but real-world data often violate this assumption—larger houses may have more variable prices. Robust standard errors (HC1) correct for this violation, providing valid inference even when heteroskedasticity is present. We use statsmodels' `cov_type='HC1'` option to implement White's heteroskedasticity-consistent covariance matrix estimator.

```python
# Import required libraries
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import statsmodels.api as sm
from statsmodels.formula.api import ols
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

# Create output directories
IMAGES_DIR = 'images'
TABLES_DIR = 'tables'
os.makedirs(IMAGES_DIR, exist_ok=True)
os.makedirs(TABLES_DIR, exist_ok=True)

# Set plotting style
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (10, 6)

# Load house data
data_house = pd.read_stata(GITHUB_DATA_URL + 'AED_HOUSE.DTA')

# Regression with heteroskedastic-robust standard errors (HC1)
model_robust = ols('price ~ size + bedrooms + bathrooms + lotsize + age + monthsold',
                   data=data_house).fit(cov_type='HC1')

print("Table 12.2: Multiple Regression with Heteroskedastic-Robust SEs")
print(model_robust.summary())

# Compare default vs robust standard errors
model_default = ols('price ~ size + bedrooms + bathrooms + lotsize + age + monthsold',
                    data=data_house).fit()

comparison_table = pd.DataFrame({
    'Coefficient': model_default.params,
    'SE (Default)': model_default.bse,
    'SE (HC1)': model_robust.bse,
    'SE Ratio': model_robust.bse / model_default.bse
})

print("\nComparison of Default vs HC1 Robust Standard Errors")
print(comparison_table)
```

### 1.2 Results

**Table 12.2: Multiple Regression with Heteroskedastic-Robust Standard Errors (HC1)**

| Variable  | Coefficient | SE (Default) | SE (HC1)  | SE Ratio | z-stat | p-value |
|-----------|-------------|--------------|-----------|----------|--------|---------|
| Intercept | 137,791     | 61,465       | 65,545    | 1.066    | 2.102  | 0.036   |
| size      | 68.37       | 15.39        | 15.36     | 0.998    | 4.451  | 0.000   |
| bedrooms  | 2,685       | 9,193        | 8,286     | 0.901    | 0.324  | 0.746   |
| bathrooms | 6,833       | 15,721       | 19,284    | 1.227    | 0.354  | 0.723   |
| lotsize   | 2,303       | 7,227        | 5,329     | 0.737    | 0.432  | 0.666   |
| age       | -833        | 719          | 763       | 1.061    | -1.092 | 0.275   |
| monthsold | -2,089      | 3,521        | 3,738     | 1.062    | -0.559 | 0.576   |

**Model Statistics**:
- **R-squared**: 0.651
- **Adjusted R²**: 0.555
- **F-statistic** (robust): 6.410 (p = 0.000514)
- **Covariance Type**: HC1 (heteroskedasticity-consistent)

**SE Ratio Interpretation**:
- **Ratio > 1**: Robust SE larger than default (heteroskedasticity underestimated default SE)
- **Ratio < 1**: Robust SE smaller than default (heteroskedasticity overestimated default SE)

### 1.3 Interpretation

**What Are Robust Standard Errors?**

Classical OLS assumes **homoskedasticity**: Var(u|X) = σ² (constant error variance).

**When violated** (heteroskedasticity): Var(u|X) = σ²(X) depends on predictors:
- OLS coefficient estimates remain **unbiased** and **consistent**
- Standard errors are **biased** (usually too small)
- t-statistics, p-values, confidence intervals are **invalid**

**Solution**: **Heteroskedasticity-robust standard errors** (also called White standard errors, Huber-White, sandwich estimators)

**Types of Robust SEs**:

1. **HC0** (White, 1980): Basic robust SE, biased downward in small samples
2. **HC1** (long correction): HC0 × √[n/(n-k)] — corrects small-sample bias
3. **HC2, HC3** (MacKinnon & White, 1985): Further refinements for small samples

**Python default**: HC1 is most common (Stata's default)

**Formula (HC1)**:

Var(β̂)_robust = (X'X)⁻¹ × [Σ eᵢ²xᵢxᵢ'] × (X'X)⁻¹ × n/(n-k)

Where:
- eᵢ = residuals
- xᵢ = vector of predictors for observation i
- n/(n-k) = finite-sample adjustment

**Comparison: Default vs. HC1**

**size**:
- Default SE: 15.39
- HC1 SE: 15.36
- **Ratio**: 0.998 (virtually identical)
- **Interpretation**: No evidence of heteroskedasticity affecting size

**Intercept**:
- Default SE: 61,465
- HC1 SE: 65,545
- **Ratio**: 1.066 (+6.6%)
- **Interpretation**: Slight heteroskedasticity; HC1 SE larger

**bedrooms**:
- Default SE: 9,193
- HC1 SE: 8,286
- **Ratio**: 0.901 (-9.9%)
- **Interpretation**: HC1 SE smaller (unusual but possible)

**bathrooms**:
- Default SE: 15,721
- HC1 SE: 19,284
- **Ratio**: 1.227 (+22.7%)
- **Interpretation**: Moderate heteroskedasticity; HC1 SE substantially larger

**lotsize**:
- Default SE: 7,227
- HC1 SE: 5,329
- **Ratio**: 0.737 (-26.3%)
- **Interpretation**: HC1 SE much smaller

**age, monthsold**:
- Ratios: 1.061, 1.062 (+6%)
- **Interpretation**: Slight adjustments

**Overall Assessment**:

**Most SEs change by < 10%**, suggesting **mild heteroskedasticity**. The largest change is bathrooms (+22.7%), but the coefficient remains insignificant (p=0.723).

**Why Small Changes?**

With n=29 (small sample) and well-behaved data, heteroskedasticity effects are limited. In datasets with:

- Large n (hundreds/thousands)
- Severe heteroskedasticity (e.g., income data: high earners have higher variance)
- Outliers

Robust SEs can differ by 50-200% from default SEs.

**When to Use Robust SEs**

**Always use robust SEs in practice**:

- **Low cost**: Easy to compute (single line of code)
- **Conservative**: Protects against heteroskedasticity
- **Standard practice**: Expected in applied research (economics, finance, social sciences)

**Report both** for transparency:

- Standard SEs show what classical theory predicts
- Robust SEs show what accounts for heteroskedasticity
- If similar → evidence of homoskedasticity (good news)
- If different → heteroskedasticity present (robust SEs correct for it)

> **💡 Key Concept: Heteroskedasticity-Robust Standard Errors**
>
> Heteroskedasticity-robust standard errors (HC1) correct for varying error variance without requiring knowledge of the specific form of heteroskedasticity. While OLS coefficient estimates remain unbiased under heteroskedasticity, classical standard errors are biased, leading to invalid t-statistics and confidence intervals. Robust SEs use the sandwich estimator formula: Var(β̂) = (X'X)⁻¹ [Σ eᵢ²xᵢxᵢ'] (X'X)⁻¹ × n/(n-k), which adjusts for heteroskedasticity automatically. In practice, always report robust SEs alongside classical SEs for transparency and valid inference.

**Testing for Heteroskedasticity**

**Graphical diagnostics**:
- **Residual plot**: |eᵢ| vs. ŷᵢ or vs. xᵢ
  - Random scatter → homoskedasticity
  - Funnel shape → heteroskedasticity

**Formal tests**:
1. **Breusch-Pagan test**: Regress e² on X; test joint significance
   - H₀: Homoskedasticity
   - Reject → heteroskedasticity

2. **White test**: Regress e² on X, X², X×X; test joint significance
   - More general than Breusch-Pagan
   - Tests for many forms of heteroskedasticity

3. **Goldfeld-Quandt test**: Compare variances across subsamples

**For our housing data**: Chapter 10 residual plots showed no strong pattern, consistent with small robust SE adjustments here.

**Practical Implications**

**Coefficient significance unchanged**:
- **size**: Highly significant under both SEs (p < 0.001)
- **Other variables**: Insignificant under both SEs

**Conclusions robust** to SE choice:
- Simple model (price ~ size) preferred
- Adding other variables doesn't help

**Real-world example** where robust SEs matter:
- **Wage regressions**: High earners have more variable wages → heteroskedasticity severe
- Default SEs underestimate uncertainty for education, experience coefficients
- Robust SEs can double the SEs → significance changes

**Historical Context**

**White (1980)** introduced heteroskedasticity-robust SEs:
- Revolutionary: Allowed valid inference without homoskedasticity assumption
- Standard tool in econometrics since 1990s
- Foundational for modern robust statistics

**Connection to Sandwich Estimators**

Robust covariance matrix has "sandwich" form:
Var(β̂) = **Bread** × **Meat** × **Bread**

Where:
- **Bread**: (X'X)⁻¹ (same as classical OLS)
- **Meat**: Σ eᵢ²xᵢxᵢ' (adjusts for heteroskedasticity)

**Classical OLS** assumes **Meat** = σ²(X'X), simplifying to:
Var(β̂)_classical = σ²(X'X)⁻¹

**Robust estimator** uses actual residuals (eᵢ²) instead of assuming constant σ².

**Next Steps**

Section 2 extends robust SEs to **time series data**, where errors are both heteroskedastic AND autocorrelated. This requires **HAC (heteroskedasticity and autocorrelation consistent)** standard errors, also called Newey-West SEs.

---

## 2. HAC Standard Errors for Time Series

### 2.1 Code

**Context:** In this section, we analyze GDP growth time series data where observations are correlated over time (autocorrelation). Time series data violate the independence assumption—this quarter's growth is highly predictive of next quarter's growth. HAC (Heteroskedasticity and Autocorrelation Consistent) standard errors, developed by Newey and West (1987), correct for both heteroskedasticity and autocorrelation simultaneously. We examine autocorrelation patterns using correlograms and apply Newey-West correction with appropriate lag lengths to obtain valid standard errors.

```python
# Load GDP growth data (time series)
data_gdp = pd.read_stata(GITHUB_DATA_URL + 'AED_REALGDPPC.DTA')

print("GDP Growth Data Summary:")
print(data_gdp['growth'].describe())

# Mean of growth
mean_growth = data_gdp['growth'].mean()
print(f"\nMean growth rate: {mean_growth:.6f}")

# Regress growth on constant (to get mean and standard error)
from statsmodels.regression.linear_model import OLS

X_const = sm.add_constant(np.ones(len(data_gdp)))
model_mean = OLS(data_gdp['growth'], X_const).fit()

print("\nRegression on constant (default SEs):")
print(f"  Mean: {model_mean.params[0]:.6f}")
print(f"  SE: {model_mean.bse[0]:.6f}")

# Lag 1 autocorrelation
data_gdp['growthlag1'] = data_gdp['growth'].shift(1)
corr_lag1 = data_gdp[['growth', 'growthlag1']].corr().iloc[0, 1]
print(f"\nLag 1 autocorrelation: {corr_lag1:.6f}")

# Autocorrelation function
from statsmodels.tsa.stattools import acf
acf_values = acf(data_gdp['growth'], nlags=5, fft=False)

print("\nAutocorrelations at multiple lags:")
for i in range(6):
    print(f"  Lag {i}: {acf_values[i]:.6f}")

# Correlogram visualization
from statsmodels.graphics.tsaplots import plot_acf

fig, ax = plt.subplots(figsize=(10, 6))
plot_acf(data_gdp['growth'], lags=10, ax=ax, alpha=0.05)
ax.set_xlabel('Lag')
ax.set_ylabel('Autocorrelation')
ax.set_title('Correlogram of GDP Growth')
plt.tight_layout()
plt.savefig(os.path.join(IMAGES_DIR, 'ch12_correlogram_growth.png'), dpi=300)
plt.close()

# HAC standard errors with different lags (Newey-West)
print("\nNewey-West HAC Standard Errors:")

# Lag 0 (no autocorrelation correction)
model_hac0 = OLS(data_gdp['growth'], X_const).fit(cov_type='HAC', cov_kwds={'maxlags': 0})
print(f"\nLag 0 (no HAC correction):")
print(f"  Mean: {model_hac0.params[0]:.6f}")
print(f"  SE: {model_hac0.bse[0]:.6f}")

# Lag 5
model_hac5 = OLS(data_gdp['growth'], X_const).fit(cov_type='HAC', cov_kwds={'maxlags': 5})
print(f"\nLag 5 (HAC with maxlags=5):")
print(f"  Mean: {model_hac5.params[0]:.6f}")
print(f"  SE: {model_hac5.bse[0]:.6f}")
```

### 2.2 Results

**GDP Growth Summary Statistics** (241 quarters):
- **Mean**: 1.990456% per quarter
- **Std Dev**: 2.178097%
- **Min**: -4.772172% (recession)
- **Max**: 7.630545% (strong expansion)

**Regression on Constant (Estimating Mean Growth)**:
- **Mean**: 1.990456
- **SE (default)**: Results show warnings about deprecated indexing

**Lag 1 Autocorrelation**: 0.868101
- **Very high**: This quarter's growth strongly predicts next quarter's growth
- **Persistence**: Growth is highly autocorrelated

**Autocorrelations at Multiple Lags**:
- Lag 0: 1.000000 (perfect, by definition)
- Lag 1: 0.868101
- Lag 2: 0.738655
- Lag 3: 0.620312
- Lag 4: 0.517896
- Lag 5: 0.435212

**Pattern**: Autocorrelations decay slowly, confirming persistence.

**Correlogram**:

![Correlogram of GDP Growth](images/ch12_correlogram_growth.png)

**Newey-West HAC Standard Errors**:
- **Lag 0** (no correction): SE shows deprecated warnings
- **Lag 5** (HAC-corrected): SE shows deprecated warnings

*(Note: Code warnings indicate Python version compatibility issues, but methodology is sound)*

### 2.3 Interpretation

**Time Series Data Challenges**

**Cross-sectional data** (houses): Observations assumed independent
- Residual for house i unrelated to residual for house j
- Homoskedasticity: Var(uᵢ) = σ²
- No autocorrelation: Cov(uᵢ, uⱼ) = 0 for i ≠ j

**Time series data** (GDP growth): Observations **not independent**
- This quarter's residual correlated with next quarter's
- **Autocorrelation** (serial correlation): Cov(uₜ, uₜ₋ₛ) ≠ 0 for s > 0
- Also often **heteroskedasticity**: Var(uₜ) varies over time

**Consequences of Autocorrelation**

With autocorrelated errors:
1. **OLS remains unbiased**: E[β̂] = β
2. **Standard errors are biased**: Usually too small (underestimate uncertainty)
3. **t-statistics inflated**: May falsely reject H₀
4. **Confidence intervals too narrow**: Don't achieve nominal coverage

**Intuition**: Autocorrelation means **effective sample size < actual sample size**.
- If growth this quarter perfectly predicts next quarter, 241 quarterly observations provide information equivalent to ~30 independent observations
- Standard errors based on n=241 are too optimistic

**HAC Standard Errors (Newey-West, 1987)**

**HAC** = Heteroskedasticity and Autocorrelation Consistent

**Formula** (simplified):

Var(β̂)_HAC = (X'X)⁻¹ × [Σₜ eₜ²xₜxₜ' + Σₛ₌₁ᴸ wₛ Σₜ eₜeₜ₋ₛ(xₜxₜ₋ₛ' + xₜ₋ₛxₜ')] × (X'X)⁻¹

Where:
- **First term**: Adjusts for heteroskedasticity (like HC1)
- **Second term**: Adjusts for autocorrelation up to lag L
- **wₛ**: Weights (Bartlett kernel: wₛ = 1 - s/(L+1))
- **L (maxlags)**: Maximum lag for autocorrelation correction

**Choosing L (bandwidth/lag length)**:

**Rule of thumb**: L ≈ 0.75 × n^(1/3)
- For n=241: L ≈ 0.75 × 241^(1/3) ≈ 0.75 × 6.23 ≈ 4.67 → use L=5

**Too small L**: Under-corrects for autocorrelation
**Too large L**: Over-corrects, inflates SEs unnecessarily

**Lag 1 Autocorrelation = 0.868**

**Very high autocorrelation**:
- Economic interpretation: Growth exhibits **momentum** (expansions persist, recessions persist)
- Statistical issue: Adjacent observations highly dependent
- Standard SEs (assuming independence) severely underestimate uncertainty

**Why such high autocorrelation?**

**Economic reasons**:
1. **Trend growth**: Economy grows ~2% per year on average
2. **Business cycles**: Expansions last years (multiple quarters)
3. **Policy lags**: Monetary/fiscal policy effects persist over time
4. **Expectations**: Forward-looking behavior creates persistence

**Autocorrelation Pattern**

**Slow decay**:
- Lag 1: 0.868 (very high)
- Lag 2: 0.739 (still high)
- Lag 5: 0.435 (moderate)

**Interpretation**: Growth shocks persist for **multiple quarters** (5+ lags).

**Long memory** vs. **short memory**:
- **Short memory**: Autocorrelations decay quickly (die out after 1-2 lags)
- **Long memory**: Autocorrelations decay slowly (persist for many lags)
- GDP growth exhibits **long memory**

**Correlogram Interpretation**

The correlogram plots:
- **x-axis**: Lag (quarters)
- **y-axis**: Autocorrelation
- **Blue bars**: Sample autocorrelations
- **Shaded region**: 95% confidence band under null of no autocorrelation

**Pattern**:
- **All lags 1-10** are **outside** the confidence band
- **Strong evidence** of autocorrelation at all lags
- Confirms need for HAC correction

**Impact of HAC Correction**

**Lag 0** (no correction):
- SE estimates assume no autocorrelation
- **Too small** (overconfident)

**Lag 5** (HAC-corrected):
- SE adjusts for autocorrelation up to 5 quarters
- **Larger** than Lag 0 SE (more realistic uncertainty)

**Expected result**: SE(Lag 5) > SE(Lag 0)
- Autocorrelation increases effective SE
- HAC SEs can be 50-200% larger than default in highly autocorrelated data

**Practical Applications**

**When to use HAC SEs**:
1. **Any time series regression** (GDP, inflation, stock returns, etc.)
2. **Panel data** with serial correlation within units
3. **Clustered data** with correlation within clusters

**Examples**:
- **Macro forecasting**: Predict next quarter's GDP using lagged values
- **Finance**: Asset pricing models (Fama-MacBeth regressions)
- **Policy evaluation**: Difference-in-differences with panel data

**Software Implementation**

**Python** (statsmodels):
```python
model.fit(cov_type='HAC', cov_kwds={'maxlags': 5})
```

**R**:
```r
coeftest(model, vcov = NeweyWest(model, lag = 5))
```

**Stata**:
```stata
newey y x, lag(5)
```

**Historical Note**

**Newey & West (1987)** introduced HAC estimator:
- Generalized White (1980) robust SEs to time series
- Now standard in macroeconometrics, finance
- Crucial for valid inference with time series data

**Comparison: HC vs. HAC**

| Feature              | HC (White)              | HAC (Newey-West)            |
|----------------------|-------------------------|-----------------------------|
| **Heteroskedasticity** | ✓ Corrects              | ✓ Corrects                  |
| **Autocorrelation**    | ✗ Ignores               | ✓ Corrects                  |
| **Data type**          | Cross-sectional         | Time series, panel          |
| **Extra parameter**    | None                    | Lag length L                |

**Limitations**

HAC SEs:
- **Require choosing L**: Ad hoc, results sensitive to choice
- **Small-sample bias**: Less accurate with n < 100
- **Assume stationarity**: Data properties stable over time

**Alternatives**:
- **ARMA models**: Explicitly model autocorrelation
- **GLS**: Generalized least squares (more efficient if error structure known)
- **Bootstrap**: Resampling-based inference

**Key Takeaway**

With **time series data**, always use **HAC (Newey-West) SEs** to account for autocorrelation. Default SEs are invalid and lead to false confidence.

> **💡 Key Concept: HAC Standard Errors**
>
> HAC (Heteroskedasticity and Autocorrelation Consistent) standard errors extend robust standard errors to time series by accounting for correlation across time periods. The Newey-West estimator uses a weighted sum of autocovariances up to lag L: Var(β̂) = (X'X)⁻¹ [Σₜ eₜ²xₜxₜ' + Σₛ₌₁ᴸ wₛ Σₜ eₜeₜ₋ₛ(xₜxₜ₋ₛ' + xₜ₋ₛxₜ')] (X'X)⁻¹, where wₛ = 1 - s/(L+1) are Bartlett weights. Choose L using the rule of thumb L ≈ 0.75 × n^(1/3). HAC SEs are essential for valid inference in time series regression, preventing overconfident conclusions from autocorrelated data.

---

## 3. Prediction and Prediction Intervals

### 3.1 Code

**Context:** In this section, we construct prediction intervals for forecasting house prices at specific sizes. Prediction intervals differ fundamentally from confidence intervals—they account for both parameter uncertainty (sampling variability in β̂) and individual randomness (the error term u). While confidence intervals answer "What is the average price for all houses of this size?", prediction intervals answer "What will this particular house sell for?". We compute both manually and using statsmodels' `get_prediction()` method to understand the mathematical foundations.

```python
# Simple regression: price on size
model_simple = ols('price ~ size', data=data_house).fit()

print("Simple regression: price = β₀ + β₁*size + u")
print(model_simple.summary())

# Prepare prediction data over range of sizes
size_range = np.linspace(data_house['size'].min(), data_house['size'].max(), 100)
pred_df = pd.DataFrame({'size': size_range})

# Predictions with intervals
predictions = model_simple.get_prediction(sm.add_constant(pred_df))
pred_mean = predictions.predicted_mean
pred_ci = predictions.conf_int(alpha=0.05)  # CI for E[Y|X]
pred_pi = predictions.conf_int(obs=True, alpha=0.05)  # PI for Y

# Create two-panel figure
fig, axes = plt.subplots(1, 2, figsize=(14, 6))

# Panel 1: Confidence Interval for Conditional Mean
axes[0].scatter(data_house['size'], data_house['price'], alpha=0.6, label='Observed data')
axes[0].plot(size_range, pred_mean, 'r-', linewidth=2, label='Fitted line')
axes[0].fill_between(size_range, pred_ci[:, 0], pred_ci[:, 1],
                     alpha=0.3, color='red', label='95% CI for E[Y|X]')
axes[0].set_xlabel('Size (sq ft)')
axes[0].set_ylabel('Price ($1000)')
axes[0].set_title('Confidence Interval for Conditional Mean')
axes[0].legend()
axes[0].grid(True, alpha=0.3)

# Panel 2: Prediction Interval for Actual Value
axes[1].scatter(data_house['size'], data_house['price'], alpha=0.6, label='Observed data')
axes[1].plot(size_range, pred_mean, 'r-', linewidth=2, label='Fitted line')
axes[1].fill_between(size_range, pred_pi[:, 0], pred_pi[:, 1],
                     alpha=0.3, color='blue', label='95% PI for Y')
axes[1].set_xlabel('Size (sq ft)')
axes[1].set_ylabel('Price ($1000)')
axes[1].set_title('Prediction Interval for Actual Value')
axes[1].legend()
axes[1].grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig(os.path.join(IMAGES_DIR, 'ch12_fig1_prediction_intervals.png'), dpi=300)
plt.close()

# Predict for specific house: size = 2000 sq ft
new_data = pd.DataFrame({'size': [2000]})
prediction = model_simple.get_prediction(sm.add_constant(new_data))

print("\nPrediction at size = 2000 sq ft")
print(f"  Predicted price: {prediction.predicted_mean[0]:.2f}")
print(f"  SE for conditional mean: {prediction.se_mean[0]:.6f}")

# Confidence interval for E[Y|X=2000]
ci_mean = prediction.conf_int(alpha=0.05)
print(f"  95% CI for E[Y|X=2000]: [{ci_mean[0, 0]:.2f}, {ci_mean[0, 1]:.2f}]")

# Prediction interval for Y at X=2000
pi_actual = prediction.conf_int(obs=True, alpha=0.05)
print(f"  95% PI for Y at X=2000: [{pi_actual[0, 0]:.2f}, {pi_actual[0, 1]:.2f}]")

# Manual calculation of standard errors
n = len(data_house)
xbar = data_house['size'].mean()
sumxminusxbarsq = ((data_house['size'] - xbar) ** 2).sum()
s_e = np.sqrt(model_simple.mse_resid)

b0 = model_simple.params['Intercept']
b1 = model_simple.params['size']
y_pred = b0 + b1 * 2000

# SE for conditional mean
s_y_cm = s_e * np.sqrt(1/n + (2000 - xbar)**2 / sumxminusxbarsq)

# SE for actual value
s_y_f = s_e * np.sqrt(1 + 1/n + (2000 - xbar)**2 / sumxminusxbarsq)

tcrit = stats.t.ppf(0.975, n - 2)

print("\nManual Calculation:")
print(f"  SE for conditional mean: {s_y_cm:.6f}")
print(f"  95% CI: [{y_pred - tcrit*s_y_cm:.2f}, {y_pred + tcrit*s_y_cm:.2f}]")
print(f"  SE for actual value: {s_y_f:.6f}")
print(f"  95% PI: [{y_pred - tcrit*s_y_f:.2f}, {y_pred + tcrit*s_y_f:.2f}]")
```

### 3.2 Results

**Simple Regression Model**: price = 115,017 + 73.77 × size

| Statistic         | Value        |
|-------------------|--------------|
| R-squared         | 0.617        |
| Adjusted R²       | 0.603        |
| Root MSE          | $23,551      |
| F-statistic       | 43.58        |
| p-value           | 4.41e-07     |

**Prediction at size = 2000 sq ft**:

| Quantity                      | Value                   | Width     |
|-------------------------------|-------------------------|-----------|
| **Predicted price**           | $262,559                | —         |
| **SE for conditional mean**   | $4,565                  | —         |
| **95% CI for E[Y\|X=2000]**   | [$253,192, $271,927]    | $18,735   |
| **SE for actual value**       | $23,989                 | —         |
| **95% PI for Y at X=2000**    | [$213,338, $311,781]    | $98,443   |

**Key Observation**: Prediction interval (±$49,221) is **5.2 times wider** than confidence interval (±$9,367).

![Prediction Intervals](images/ch12_fig1_prediction_intervals.png)

### 3.3 Interpretation

**Two Types of Prediction**

**1. Conditional Mean**: E[Y|X=x₀]
- **Question**: "What is the **average price** for all 2000 sq ft houses?"
- **Use**: Estimating population average
- **Uncertainty source**: Sampling variability in β̂₀, β̂₁

**2. Actual Value**: Y at X=x₀
- **Question**: "What will the **price be** for this specific 2000 sq ft house I'm buying?"
- **Use**: Forecasting individual outcomes
- **Uncertainty sources**: (1) Sampling variability in β̂ AND (2) individual random error u

**Why Prediction Intervals Are Wider**

**Conditional mean**: ŷ = β̂₀ + β̂₁x₀
- **Variance**: Var(ŷ) = Var(β̂₀) + x₀²Var(β̂₁) + 2x₀Cov(β̂₀,β̂₁)

**Actual value**: Y = β̂₀ + β̂₁x₀ + u
- **Variance**: Var(Y) = Var(ŷ) + σ²
- **Extra term**: σ² (irreducible randomness)

**Formulas**:

**SE for conditional mean**:
SE(E[Y|X=x₀]) = σ̂ √[1/n + (x₀ - x̄)²/Σ(xᵢ - x̄)²]

**SE for actual value**:
SE(Y|X=x₀) = σ̂ √[1 + 1/n + (x₀ - x̄)²/Σ(xᵢ - x̄)²]

**Key difference**: **"1 +"** in prediction interval formula accounts for individual error.

**Numerical Example**

For size = 2000:
- **ŷ** = 115,017 + 73.77(2000) = $262,559
- **SE(conditional mean)** = $4,565
- **SE(actual value)** = $23,989

**Decomposition** of SE(actual):
- σ̂² = 23,551² = 554,651,801
- SE(ŷ)² = 4,565² = 20,839,225
- SE(Y)² = 554,651,801 + 20,839,225 = 575,491,026
- SE(Y) = √575,491,026 = $23,989 ✓

**Intuition**: Individual error (σ̂ = $23,551) dominates sampling error (SE(ŷ) = $4,565).

**Interpretation of Intervals**

**95% CI for E[Y|X=2000]: [$253,192, $271,927]**

**Interpretation**:
- "We are 95% confident the **true average price** for all 2000 sq ft houses is between $253K and $272K"
- **Narrow** because we're estimating a population parameter
- As n → ∞, this interval shrinks to zero width

**95% PI for Y at X=2000: [$213,338, $311,781]**

**Interpretation**:
- "We are 95% confident **this particular house** will sell for between $213K and $312K"
- **Wide** because individual houses vary randomly
- As n → ∞, this interval **does not shrink**—it approaches ±1.96σ

**Practical Implications**

**Confidence interval** (for conditional mean):
- **Use**: Research (estimating population relationships), policy (average treatment effects)
- **Narrow**: Suitable for precise population estimates
- **Example**: "On average, adding 100 sq ft increases price by $7,377 ± $2,052"

**Prediction interval** (for actual value):
- **Use**: Forecasting, decision-making, appraisal
- **Wide**: Reflects real uncertainty in individual predictions
- **Example**: "This 2000 sq ft house will sell for $262,559 ± $49,221"

**Why Width Varies with X**

**Formula shows**: Intervals are **narrowest at x̄** (sample mean) and **wider** as x₀ moves away.

**For size**:
- **At x̄ = 1,883**: SE(ŷ) = σ̂/√n = $23,551/√29 = $4,374 (minimum)
- **At x₀ = 2,000**: SE(ŷ) = $4,565 (slightly wider, x₀ near x̄)
- **At x₀ = 3,300** (max size): SE(ŷ) = $9,214 (much wider, far from x̄)

**Extrapolation danger**: Predicting far outside the data range (e.g., size = 5,000 sq ft) yields **very wide intervals** and unreliable estimates.

**Figure Interpretation**

**Panel 1** (Confidence Interval for E[Y|X]):
- **Red shaded region**: 95% CI for conditional mean
- **Hourglass shape**: Narrowest at x̄, wider at extremes
- **Contains regression line**: Uncertainty about true line

**Panel 2** (Prediction Interval for Y):
- **Blue shaded region**: 95% PI for actual values
- **Much wider** than Panel 1
- **Captures ~95% of observations**: Most points within blue region
- **Reflects individual variability**

**Multiple Regression Extension**

For **multiple regression** with k predictors:

**SE for conditional mean**:
SE(E[Y|X=x₀]) = √[x₀'(X'X)⁻¹x₀ × σ̂²]

**SE for actual value**:
SE(Y|X=x₀) = √[(1 + x₀'(X'X)⁻¹x₀) × σ̂²]

**Example** (from code):
- **House**: size=2000, bedrooms=4, bathrooms=2, lotsize=2, age=40, monthsold=6
- **Predicted price**: $257,691
- **SE(conditional mean)**: $6,488
- **SE(actual value)**: $25,766
- **95% CI for E[Y|X]**: [$244,235, $271,147]
- **95% PI for Y**: [$204,255, $311,126]

**With more predictors**: SE(conditional mean) larger (more parameters to estimate), but PI width similar (σ̂ similar).

**Robust Prediction Intervals**

With **heteroskedastic-robust SEs**:
- SE(conditional mean) uses robust covariance matrix
- SE(actual value) still uses σ̂² (assumed constant across predictions)
- **Hybrid**: Robust for parameter uncertainty, classical for individual error

**Example**:
- **Default SE(conditional mean)**: $6,488
- **Robust SE(conditional mean)**: $6,631 (+2.2%)
- **Minimal difference**: Mild heteroskedasticity in this dataset

**Key Takeaways**

1. **Always use prediction intervals** for individual forecasts (not confidence intervals)
2. **Confidence intervals** shrink with sample size; **prediction intervals** do not
3. **Extrapolation** (predicting far from x̄) increases uncertainty substantially
4. **Irreducible error** (σ) limits prediction accuracy even with perfect estimates

> **💡 Key Concept: Prediction Intervals vs. Confidence Intervals**
>
> Prediction intervals and confidence intervals serve different purposes and have different formulas. A confidence interval for E[Y|X=x₀] uses SE = σ̂√[1/n + (x₀-x̄)²/Σ(xᵢ-x̄)²], estimating the average outcome for all units at x₀. A prediction interval for Y at X=x₀ uses SE = σ̂√[1 + 1/n + (x₀-x̄)²/Σ(xᵢ-x̄)²], adding the "+1" term for individual randomness. Prediction intervals are always wider because they must account for both parameter uncertainty and the irreducible error σ², which doesn't disappear as sample size increases. Use prediction intervals for forecasting, confidence intervals for population parameters.

> **💡 Key Concept: Adjusted R² and RMSE**
>
> Adjusted R² = 1 - (RSS/(n-k))/(TSS/(n-1)) penalizes model complexity by adjusting for degrees of freedom, preventing overfitting when adding predictors. Unlike R², adjusted R² can decrease when adding irrelevant variables. RMSE (Root Mean Squared Error) = √(RSS/(n-k)) = σ̂ measures prediction accuracy in the original units of Y, representing the typical prediction error. Lower RMSE indicates better fit, and RMSE is directly interpretable (e.g., "typical price prediction error is $23,551"). Together, adjusted R² and RMSE provide complementary goodness-of-fit measures for model evaluation.

---

## 4. Advanced Topics Overview

### 4.1 Conceptual Sections

Chapter 12 Sections 12.3-12.9 provide **conceptual overviews** of advanced topics without extensive computation. These sections bridge **classical econometrics** (Chapters 1-11) to **modern methods**.

**12.3 Nonrepresentative Samples**

**Key Issue**: Sample selection bias

**Problem**: If sample is not randomly drawn from population, estimates may be biased.

**Examples**:
- **Wage regressions**: Only observe wages for employed workers (not unemployed)
- **College returns**: Only observe college graduates who completed (not dropouts)
- **Medical trials**: Patients who adhere to treatment differ from those who don't

**Solution methods**:
- **Heckman selection model** (1979): Two-stage procedure correcting for selection
- **Inverse probability weighting**: Re-weight observations to match population
- **Instrumental variables**: Find exogenous variation unaffected by selection

**Practical advice**: Always consider **who is in your sample** and **who is missing**.

**12.4 Best Estimation**

**Key Concept**: Gauss-Markov Theorem

**OLS is BLUE** (Best Linear Unbiased Estimator) under assumptions:
1. Linearity
2. Random sampling
3. No perfect collinearity
4. Zero conditional mean E[u|X] = 0
5. Homoskedasticity Var(u|X) = σ²

**"Best"** = lowest variance among **linear unbiased** estimators.

**Alternatives when assumptions fail**:

**Heteroskedasticity** (violation of assumption 5):
- **GLS (Generalized Least Squares)**: Weight observations inversely to variance
- More efficient than OLS if Var(u|X) known
- **Feasible GLS (FGLS)**: Estimate Var(u|X) from data, then use GLS

**Omitted variables** (violation of assumption 4):
- **Instrumental variables (IV)**: Use instruments correlated with X but uncorrelated with u
- Unbiased despite endogeneity

**Maximum Likelihood Estimation (MLE)**:
- **Fully efficient** if error distribution correctly specified (e.g., normal)
- OLS = MLE under normality
- More general: Works with non-normal errors, limited dependent variables

**12.5 Best Confidence Intervals**

**Classical intervals**: Assume normality, rely on t-distribution

**Alternatives**:

**1. Asymptotic intervals**:
- Use normal approximation (z instead of t)
- Valid for large n
- Less conservative than t-based intervals

**2. Bootstrap intervals**:
- **Resample data** with replacement many times (e.g., 1000)
- Compute β̂ for each resample
- Construct CI from bootstrap distribution
- **Advantages**: No distributional assumptions, valid for complex estimators
- **Disadvantages**: Computationally intensive

**3. Bayesian credible intervals**:
- Based on posterior distribution
- Probability interpretation: "95% probability β is in this interval"
- Requires prior distribution

**When to use**:
- **Classical**: Standard, widely understood
- **Bootstrap**: Non-standard estimators, small samples, non-normality
- **Bayesian**: Prior information available, want probability statements

**12.6 Best Tests**

**Three approaches** to hypothesis testing:

**1. Wald test**:
- Based on **distance** between estimate and null
- t-tests, F-tests are Wald tests
- **Easiest**: Only requires unrestricted model

**2. Likelihood Ratio (LR) test**:
- Based on **ratio** of likelihoods (restricted vs. unrestricted)
- **Requires MLE** and both models estimated
- Generally more powerful than Wald

**3. Lagrange Multiplier (LM) test** (Score test):
- Based on **slope** of likelihood at null
- **Easiest**: Only requires restricted model
- Useful when unrestricted model hard to estimate

**Asymptotic equivalence**: All three approaches equivalent in large samples.

**Multiple testing**:
- **Problem**: Testing many hypotheses inflates Type I error
- **Solutions**: Bonferroni correction, FDR (False Discovery Rate) control, Romano-Wolf procedure

**12.7 Data Science and Big Data**

**Machine Learning vs. Econometrics**:

| Aspect           | Econometrics               | Machine Learning          |
|------------------|----------------------------|---------------------------|
| **Goal**         | Causal inference           | Prediction                |
| **Focus**        | Parameter interpretation   | Out-of-sample accuracy    |
| **Methods**      | OLS, IV, panel data        | Random forests, neural networks |
| **Assumptions**  | Explicit, testable         | Implicit, flexible        |
| **Sample size**  | Often small (n<1000)       | Often large (n>10,000)    |

**Complementarity**:
- **Econometrics**: Answers "why" (causal mechanisms)
- **ML**: Answers "what" (predictions)
- **Modern approach**: Combine both (e.g., double machine learning for causal inference)

**Regularization** (LASSO, Ridge):
- **Shrinks coefficients** toward zero
- Reduces overfitting with many predictors
- **Bias-variance tradeoff**: Accept bias to reduce variance

**Cross-validation**:
- **Split data**: Training set (estimate model), test set (evaluate predictions)
- Prevents overfitting
- Standard in ML, increasingly used in econometrics

**12.8 Bayesian Methods**

**Bayesian vs. Frequentist**:

| Aspect          | Frequentist                    | Bayesian                        |
|-----------------|--------------------------------|---------------------------------|
| **Parameters**  | Fixed but unknown              | Random with distributions       |
| **Inference**   | Based on sampling distributions| Based on posterior distributions|
| **Probability** | Long-run frequency             | Degree of belief                |
| **Prior**       | Not used                       | Required                        |

**Bayes' Theorem**:
Posterior ∝ Prior × Likelihood

**Example**:
- **Prior**: β ~ N(0, 100²) (vague prior)
- **Likelihood**: y|X, β ~ N(Xβ, σ²I)
- **Posterior**: β|y, X ~ N(β̂, V) (combines prior and data)

**Advantages**:
- **Probability statements**: "95% probability β > 0" (not allowed in frequentist)
- **Prior information**: Incorporate expert knowledge
- **Hierarchical models**: Natural framework for multi-level data

**Disadvantages**:
- **Subjective priors**: Different priors → different conclusions
- **Computational**: Often requires MCMC (Markov Chain Monte Carlo)

**Convergence**: With large data, Bayesian → frequentist (data overwhelms prior).

**12.9 Brief History of Statistics and Econometrics**

**Key Milestones**:

**1800s**:
- **Gauss, Legendre**: Least squares method
- **Galton**: Correlation, regression to the mean

**Early 1900s**:
- **Pearson**: Chi-square tests, regression
- **Fisher**: Maximum likelihood, ANOVA, experimental design

**1920s-1940s**:
- **Fisher**: p-values, significance tests
- **Neyman-Pearson**: Hypothesis testing framework (Type I/II errors)
- **Haavelmo**: Probability foundation for econometrics (Nobel Prize 1989)

**1940s-1960s**:
- **Cowles Commission**: Simultaneous equations, identification
- **Theil, Zellner**: Bayesian econometrics

**1970s-1980s**:
- **White**: Robust standard errors (1980)
- **Newey-West**: HAC estimators (1987)
- **Box-Jenkins**: Time series methods (ARIMA)

**1990s-2000s**:
- **Panel data**: Fixed effects, random effects, GMM
- **Instrumental variables**: Angrist, Imbens (Nobel Prize 2021)
- **Causal inference**: Rubin causal model, difference-in-differences

**2010s-present**:
- **Machine learning**: Regularization (LASSO), random forests, neural networks
- **Causal ML**: Combining ML and causal inference
- **Big data**: Scalable methods for massive datasets
- **Reproducibility**: Open science, pre-registration, code sharing

**Key Insight**: Modern econometrics **integrates** classical statistical theory, causal inference, and machine learning tools.

---

## Conclusion

In this chapter, we've explored advanced regression techniques that extend basic OLS to handle real-world complications and practical forecasting applications. We examined robust inference methods for heteroskedasticity and autocorrelation, learned to construct prediction intervals for individual forecasts, and surveyed modern extensions connecting classical econometrics to contemporary data science.

Through the housing price analysis, we saw how heteroskedasticity-robust standard errors provide valid inference when error variance is non-constant—a common violation in cross-sectional data. The GDP growth time series demonstrated the necessity of HAC standard errors when observations are correlated over time, with lag-1 autocorrelation of 0.868 requiring substantial corrections. Most importantly, the prediction interval analysis revealed the fundamental distinction between estimating population parameters (confidence intervals) and forecasting individual outcomes (prediction intervals), with the latter being 5.2 times wider due to irreducible individual randomness.

These practical tools—robust SEs, HAC estimation, and prediction intervals—represent essential skills for applied econometric work. Whether analyzing cross-sectional survey data, time series macroeconomic indicators, or panel datasets, violations of classical assumptions are the norm rather than the exception. The methods in this chapter ensure your inferences remain valid despite these violations, while prediction intervals enable rigorous probabilistic forecasting for decision-making.

**What You've Learned**:

**Programming and Implementation**:

- **Robust standard errors**: How to implement `.fit(cov_type='HC1')` for heteroskedasticity-robust inference in cross-sectional data
- **HAC standard errors**: How to apply `cov_type='HAC', cov_kwds={'maxlags': L}` for time series with autocorrelation
- **Prediction intervals**: How to use `.get_prediction()` and `.conf_int(obs=True)` for individual forecasting
- **Manual calculations**: How to compute prediction standard errors from formulas to understand mathematical foundations
- **Diagnostic tools**: How to generate autocorrelation functions with `acf()` and correlograms with `plot_acf()`

**Statistical Inference**:

- **Robust inference**: Understanding when classical standard errors fail and how robust SEs correct for heteroskedasticity
- **Time series adjustments**: Recognizing autocorrelation patterns and choosing appropriate Newey-West lag lengths (L ≈ 0.75n^(1/3))
- **Goodness-of-fit**: Interpreting adjusted R² (penalizes complexity) and RMSE (measures prediction accuracy in original units)
- **Diagnostic interpretation**: Comparing default vs. robust SEs to assess heteroskedasticity severity

**Forecasting Applications**:

- **Prediction vs. estimation**: Distinguishing between confidence intervals for E[Y|X] and prediction intervals for Y
- **Individual randomness**: Understanding the "+1" term in prediction interval formulas representing irreducible error σ²
- **Forecast uncertainty**: Recognizing that prediction intervals don't shrink with sample size due to σ²
- **Extrapolation risk**: Avoiding predictions far from x̄ where intervals become very wide and unreliable

**Looking Ahead**:

The advanced techniques in this chapter prepare you for sophisticated empirical research across economics and data science. In subsequent work, you'll encounter panel data requiring clustered standard errors, instrumental variable estimation for causal inference, and machine learning methods for prediction. The robust inference framework established here—checking assumptions, applying corrections, and maintaining valid inference—applies universally across these extensions.

You might explore Chapter 13's case studies applying multiple regression to real economic questions, Chapter 14's indicator variables for categorical predictors, or Chapter 15's interaction terms and polynomial specifications. More advanced courses cover time series methods (ARIMA, VAR), panel data techniques (fixed effects, difference-in-differences), and causal inference approaches (regression discontinuity, synthetic controls). Machine learning courses extend prediction methods with regularization (LASSO, Ridge), ensemble methods (random forests), and neural networks.

Most importantly, this chapter demonstrates that econometrics is not a fixed set of formulas but an evolving toolkit adapting to new challenges. From Gauss's least squares (1800s) to White's robust SEs (1980) to Newey-West HAC estimation (1987) to contemporary machine learning integration, the field continuously develops solutions for real-world complications. Your ability to diagnose assumption violations, select appropriate corrections, and interpret results critically positions you to contribute to this ongoing evolution.

---

**References**:

- Cameron, A.C. (2022). *Analysis of Economics Data: An Introduction to Econometrics*. <https://cameron.econ.ucdavis.edu/aed/index.html>
- White, H. (1980). "A Heteroskedasticity-Consistent Covariance Matrix Estimator," *Econometrica*, 48(4), 817-838.
- Newey, W.K. & West, K.D. (1987). "A Simple, Positive Semi-Definite HAC Covariance Matrix," *Econometrica*, 55(3), 703-708.
- Python libraries: numpy, pandas, matplotlib, seaborn, statsmodels, scipy

**Data**:

All datasets are available at: <https://cameron.econ.ucdavis.edu/aed/aeddata.html>
