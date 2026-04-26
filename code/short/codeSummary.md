# metricsAI: Code Summaries


A compilation of all chapter code cheat sheets — self-contained Python scripts covering the core workflow of each chapter.

---

## Chapter 01 Analysis of Economics Data

```python
# =============================================================================
# CHAPTER 1 CHEAT SHEET: Analysis of Economics Data
# =============================================================================

# --- Libraries ---
import pandas as pd                       # data loading and manipulation
import matplotlib.pyplot as plt           # creating plots and visualizations
import pyfixest as pf                     # OLS regression with R-style formulas
# !pip install pyfixest  # if not installed

# =============================================================================
# STEP 1: Load data directly from a URL
# =============================================================================
# pd.read_stata() reads Stata .dta files (pandas also supports CSV, Excel, etc.)
url = "https://raw.githubusercontent.com/quarcs-lab/data-open/master/AED/AED_HOUSE.DTA"
data_house = pd.read_stata(url)

print(f"Dataset: {data_house.shape[0]} observations, {data_house.shape[1]} variables")

# =============================================================================
# STEP 2: Descriptive statistics — summarize before modeling
# =============================================================================
# .head() shows the first rows; .describe() gives mean, std, min, quartiles, max
print(data_house[['price', 'size']].describe().round(2))

# =============================================================================
# STEP 3: Scatter plot — always visualize before fitting a regression
# =============================================================================
fig, ax = plt.subplots(figsize=(10, 6))
ax.scatter(data_house['size'], data_house['price'], s=50, alpha=0.7)
ax.set_xlabel('House Size (square feet)')
ax.set_ylabel('House Sale Price (dollars)')
ax.set_title('House Price vs Size')
ax.grid(True, alpha=0.3)
plt.tight_layout()
plt.show()

# =============================================================================
# STEP 4: OLS regression — fit the model
# =============================================================================
# Formula syntax: 'y ~ x' regresses y on x (intercept included automatically)
fit = pf.feols('price ~ size', data=data_house)

# Extract key results
slope     = fit.coef()['size']         # marginal effect: $/sq ft
intercept = fit.coef()['Intercept']    # predicted price when size = 0
r_squared = fit._r2                    # proportion of variation explained

print(f"Estimated equation: price = {intercept:,.0f} + {slope:.2f} × size")
print(f"Interpretation: each additional sq ft is associated with ${slope:,.2f} higher price")
print(f"R-squared: {r_squared:.4f} ({r_squared*100:.1f}% of variation explained)")

# Full regression table (coefficients, std errors, t-stats, p-values, R²)
fit.summary()

# =============================================================================
# STEP 5: Scatter plot with fitted regression line and R²
# =============================================================================
# fit.predict() contains the predicted y-values from the estimated equation
fig, ax = plt.subplots(figsize=(10, 6))
ax.scatter(data_house['size'], data_house['price'], s=50, alpha=0.7, label='Actual prices')
ax.plot(data_house['size'], fit.predict(), color='red', linewidth=2, label='Fitted line')
ax.set_xlabel('House Size (square feet)')
ax.set_ylabel('House Sale Price (dollars)')
ax.set_title(f'OLS Regression: price = {intercept:,.0f} + {slope:.2f} × size  (R² = {r_squared:.2%})')
ax.legend()
ax.grid(True, alpha=0.3)
plt.tight_layout()
plt.show()

# =============================================================================
# STEP 6: Compare predictors — association is NOT causation
# =============================================================================
# Running separate regressions with different x-variables shows that each tells
# a different story. High R² does not prove causation — omitted variables
# (location, condition, school district) can bias any single-variable slope.
predictors = {
    'size':      'Size (sq ft)',
    'bedrooms':  'Bedrooms',
    'bathrooms': 'Bathrooms',
    'lotsize':   'Lot size',
    'age':       'Age (years)',
}

print(f"{'Predictor':<18} {'Slope':>10} {'R²':>8}")
print("-" * 38)
for var, label in predictors.items():
    m = pf.feols(f'price ~ {var}', data=data_house)
    print(f"{label:<18} {m.coef()[var]:>10.2f} {m._r2:>8.4f}")

```

---

## Chapter 02 Univariate Data Summary

```python
# =============================================================================
# CHAPTER 2 CHEAT SHEET: Univariate Data Summary
# =============================================================================

# --- Libraries ---
import numpy as np                        # numerical operations (log, mean)
import pandas as pd                       # data loading and manipulation
import matplotlib.pyplot as plt           # creating plots and visualizations
from scipy import stats                   # skewness, kurtosis, distribution shape

# =============================================================================
# STEP 1: Load data directly from a URL
# =============================================================================
# pd.read_stata() reads Stata .dta files; this dataset has 171 observations
url_earnings = "https://raw.githubusercontent.com/quarcs-lab/data-open/master/AED/AED_EARNINGS.DTA"
data_earnings = pd.read_stata(url_earnings)

earnings = data_earnings['earnings']
print(f"Dataset: {data_earnings.shape[0]} observations, {data_earnings.shape[1]} variables")

# =============================================================================
# STEP 2: Summary statistics — mean vs median reveals skewness
# =============================================================================
# .describe() gives count, mean, std, min, quartiles, max in one call
print(data_earnings[['earnings']].describe().round(2))

# Skewness and kurtosis measure the shape of the distribution
print(f"\nSkewness:        {stats.skew(earnings):.2f}  (> 1 = strongly right-skewed)")
print(f"Excess kurtosis: {stats.kurtosis(earnings):.2f}  (> 0 = heavier tails than normal)")
print(f"Mean - Median:   ${earnings.mean() - earnings.median():,.0f}  (positive gap signals right skew)")

# =============================================================================
# STEP 3: Histogram with KDE overlay — see the distribution shape
# =============================================================================
# Bin width is a choice: narrower = more detail (and noise), wider = smoother
fig, ax = plt.subplots(figsize=(10, 6))
ax.hist(earnings, bins=20, edgecolor='black', alpha=0.7, density=True, label='Histogram')
earnings.plot.kde(ax=ax, linewidth=2, color='red', label='KDE')
ax.set_xlabel('Annual Earnings ($)')
ax.set_ylabel('Density')
ax.set_title('Earnings Distribution: Histogram + Kernel Density Estimate')
ax.legend()
ax.grid(True, alpha=0.3)
plt.tight_layout()
plt.show()

# =============================================================================
# STEP 4: Box plot — visualize quartiles and outliers
# =============================================================================
# The box spans Q1 to Q3 (IQR); whiskers extend 1.5×IQR; dots are outliers
fig, ax = plt.subplots(figsize=(10, 4))
ax.boxplot(earnings, vert=False, patch_artist=True,
           boxprops=dict(facecolor='lightblue', alpha=0.7),
           medianprops=dict(color='red', linewidth=2))
ax.set_xlabel('Annual Earnings ($)')
ax.set_title('Box Plot of Earnings — Median, Quartiles, and Outliers')
ax.grid(True, alpha=0.3)
plt.tight_layout()
plt.show()

# =============================================================================
# STEP 5: Log transformation — taming right skew
# =============================================================================
# np.log() compresses big values and stretches small ones, making skewed
# distributions more symmetric — a prerequisite for many statistical methods
data_earnings['lnearnings'] = np.log(earnings)

fig, axes = plt.subplots(1, 2, figsize=(14, 5))
axes[0].hist(earnings, bins=20, edgecolor='black', alpha=0.7, color='steelblue')
axes[0].set_title(f'Original  (skewness = {stats.skew(earnings):.2f})')
axes[0].set_xlabel('Earnings ($)')

axes[1].hist(data_earnings['lnearnings'], bins=20, edgecolor='black', alpha=0.7, color='coral')
axes[1].set_title(f'Log-transformed  (skewness = {stats.skew(data_earnings["lnearnings"]):.2f})')
axes[1].set_xlabel('ln(Earnings)')

plt.suptitle('Effect of Log Transformation on Skewness', fontweight='bold')
plt.tight_layout()
plt.show()

# =============================================================================
# STEP 6: Z-scores — how unusual is each observation?
# =============================================================================
# z = (x - mean) / std  puts every value on a common "standard deviations
# from the mean" scale: |z| > 2 is unusual, |z| > 3 is very unusual
z_scores = (earnings - earnings.mean()) / earnings.std()

print(f"Highest earner: ${earnings.max():,.0f}  →  z = {z_scores.max():.2f}")
print(f"Median earner:  ${earnings.median():,.0f}  →  z = {(earnings.median() - earnings.mean()) / earnings.std():.2f}")
print(f"Observations with |z| > 2: {(z_scores.abs() > 2).sum()} out of {len(z_scores)}")

# =============================================================================
# STEP 7: Time series — moving average smooths seasonal noise
# =============================================================================
# Monthly home sales zigzag with the seasons; an 11-month moving average
# cancels one full seasonal cycle, revealing the underlying trend
url_homesales = "https://raw.githubusercontent.com/quarcs-lab/data-open/master/AED/AED_MONTHLYHOMESALES.DTA"
data_hs = pd.read_stata(url_homesales)
data_hs = data_hs[data_hs['year'] >= 2005]

fig, ax = plt.subplots(figsize=(12, 6))
ax.plot(data_hs['daten'], data_hs['exsales'], linewidth=1, alpha=0.6, label='Original (monthly)')
ax.plot(data_hs['daten'], data_hs['exsales_ma11'], linewidth=2, color='red',
        linestyle='--', label='11-month Moving Average')
ax.set_xlabel('Year')
ax.set_ylabel('Monthly Home Sales')
ax.set_title('U.S. Home Sales: Raw Series vs. Moving Average (2005–2015)')
ax.legend()
ax.grid(True, alpha=0.3)
plt.tight_layout()
plt.show()

```

---

## Chapter 03 The Sample Mean

```python
# =============================================================================
# CHAPTER 3 CHEAT SHEET: The Sample Mean
# =============================================================================

# --- Libraries ---
import numpy as np                        # numerical operations and random sampling
import pandas as pd                       # data loading and manipulation
import matplotlib.pyplot as plt           # creating plots and visualizations
from scipy import stats                   # normal distribution PDF for overlays

# =============================================================================
# STEP 1: Load pre-computed sample means from coin toss experiments
# =============================================================================
# 400 samples of 30 coin tosses each — precomputed in the textbook dataset
url_coin = "https://raw.githubusercontent.com/quarcs-lab/data-open/master/AED/AED_COINTOSSMEANS.DTA"
data_coin = pd.read_stata(url_coin)
xbar_coin = data_coin['xbar']

print(f"Coin toss experiment: {len(xbar_coin)} sample means (each from n=30 tosses)")
print(f"Mean of sample means: {xbar_coin.mean():.4f}  (theoretical μ = 0.5)")
print(f"SD of sample means:   {xbar_coin.std():.4f}  (theoretical σ/√n = {np.sqrt(0.25/30):.4f})")

# =============================================================================
# STEP 2: Visualize the sampling distribution with normal overlay
# =============================================================================
# The histogram of 400 sample means approximates the sampling distribution of X̄
fig, ax = plt.subplots(figsize=(10, 6))
ax.hist(xbar_coin, bins=25, density=True, edgecolor='black', alpha=0.7,
        label='400 sample means')

# Overlay theoretical normal: N(μ, σ²/n)
theo_se = np.sqrt(0.25 / 30)
x_range = np.linspace(xbar_coin.min(), xbar_coin.max(), 100)
ax.plot(x_range, stats.norm.pdf(x_range, 0.5, theo_se),
        'r-', linewidth=2.5, label=f'N(0.5, {theo_se:.3f}²)')
ax.set_xlabel('Sample Mean (proportion of heads)')
ax.set_ylabel('Density')
ax.set_title('Sampling Distribution of X̄ from 400 Coin Toss Experiments (n=30)')
ax.legend()
ax.grid(True, alpha=0.3)
plt.tight_layout()
plt.show()

# =============================================================================
# STEP 3: Central Limit Theorem — non-normal population still gives normal X̄
# =============================================================================
# 1880 U.S. Census ages: highly skewed population, yet sample means are normal
url_census = "https://raw.githubusercontent.com/quarcs-lab/data-open/master/AED/AED_CENSUSAGEMEANS.DTA"
data_census = pd.read_stata(url_census)

# Identify the sample mean column
if 'mean' in data_census.columns:
    age_means = data_census['mean']
elif 'xmean' in data_census.columns:
    age_means = data_census['xmean']
else:
    age_means = data_census.iloc[:, 0]

print(f"\n1880 Census: {len(age_means)} sample means (each from n=25 people)")
print(f"Mean of sample means: {age_means.mean():.2f} years  (theoretical μ = 24.13)")
print(f"SD of sample means:   {age_means.std():.2f} years  (theoretical σ/√n = {18.61/np.sqrt(25):.2f})")

fig, ax = plt.subplots(figsize=(10, 6))
ax.hist(age_means, bins=20, density=True, edgecolor='black', alpha=0.7,
        label='100 sample means')
age_range = np.linspace(age_means.min(), age_means.max(), 100)
ax.plot(age_range, stats.norm.pdf(age_range, 24.13, 18.61 / np.sqrt(25)),
        'r-', linewidth=2.5, label=f'N(24.13, {18.61/np.sqrt(25):.2f}²)')
ax.set_xlabel('Sample Mean Age (years)')
ax.set_ylabel('Density')
ax.set_title('CLT in Action: Normal Sample Means from a Skewed Population')
ax.legend()
ax.grid(True, alpha=0.3)
plt.tight_layout()
plt.show()

# =============================================================================
# STEP 4: Standard error — how sample size affects precision
# =============================================================================
# SE = σ/√n: to halve the SE, you must quadruple the sample size
sigma = 0.5  # coin toss population std dev

print(f"\nStandard error vs sample size (σ = {sigma}):")
print(f"{'n':<10} {'SE = σ/√n':<15} {'Var(X̄) = σ²/n':<15}")
print("-" * 40)
for n in [10, 30, 100, 400, 1000]:
    se = sigma / np.sqrt(n)
    var_xbar = sigma**2 / n
    print(f"{n:<10} {se:<15.4f} {var_xbar:<15.6f}")

# =============================================================================
# STEP 5: Monte Carlo simulation — verify the theory computationally
# =============================================================================
# Simulate 1000 samples of 30 coin tosses to see the CLT converge
np.random.seed(10101)
n_sims = 1000
sample_size = 30
sim_means = np.array([np.random.binomial(1, 0.5, sample_size).mean()
                       for _ in range(n_sims)])

print(f"\nMonte Carlo simulation ({n_sims} samples, n={sample_size}):")
print(f"Mean of simulated means: {sim_means.mean():.4f}  (theoretical: 0.5)")
print(f"SD of simulated means:   {sim_means.std():.4f}  (theoretical: {np.sqrt(0.25/30):.4f})")

fig, ax = plt.subplots(figsize=(10, 6))
ax.hist(sim_means, bins=30, density=True, edgecolor='black', alpha=0.7,
        label=f'{n_sims} simulated means')
x_range = np.linspace(sim_means.min(), sim_means.max(), 100)
ax.plot(x_range, stats.norm.pdf(x_range, 0.5, np.sqrt(0.25/30)),
        'r-', linewidth=2.5, label='Theoretical N(0.5, 0.091²)')
ax.set_xlabel('Sample Mean')
ax.set_ylabel('Density')
ax.set_title('Monte Carlo Simulation vs Theoretical Sampling Distribution')
ax.legend()
ax.grid(True, alpha=0.3)
plt.tight_layout()
plt.show()

# =============================================================================
# STEP 6: Weighted means — correcting for nonrepresentative samples
# =============================================================================
# When inclusion probabilities differ, the unweighted mean is biased;
# inverse-probability weights w_i = 1/π_i recover the true population mean
np.random.seed(42)
income_men = np.random.normal(60000, 15000, 50)
income_women = np.random.normal(50000, 15000, 50)
true_pop_mean = (income_men.mean() + income_women.mean()) / 2

# Biased sample: oversample women (70% women, 30% men)
sample_men = np.random.choice(income_men, size=15, replace=False)
sample_women = np.random.choice(income_women, size=35, replace=False)
sample = np.concatenate([sample_men, sample_women])

# Unweighted mean is biased toward the oversampled group
unweighted = sample.mean()

# Weighted mean with IPW: w_i = 1/π_i corrects the imbalance
weights = np.concatenate([np.repeat(1/0.3, 15), np.repeat(1/0.7, 35)])
weighted = np.average(sample, weights=weights)

print(f"\nWeighted vs Unweighted Means:")
print(f"True population mean:  ${true_pop_mean:,.0f}")
print(f"Unweighted mean:       ${unweighted:,.0f}  (bias: ${unweighted - true_pop_mean:,.0f})")
print(f"Weighted mean (IPW):   ${weighted:,.0f}  (bias: ${weighted - true_pop_mean:,.0f})")

```

---

## Chapter 04 Statistical Inference for the Mean

```python
# =============================================================================
# CHAPTER 4 CHEAT SHEET: Statistical Inference for the Mean
# =============================================================================

# --- Libraries ---
import numpy as np                       # numerical operations (sqrt, linspace)
import pandas as pd                      # data loading and manipulation
import matplotlib.pyplot as plt          # creating plots and visualizations
from scipy import stats                  # t-distribution and normal distribution

# =============================================================================
# STEP 1: Load data directly from a URL
# =============================================================================
# pd.read_stata() reads Stata .dta files — this sample has 171 female workers
url = "https://raw.githubusercontent.com/quarcs-lab/data-open/master/AED/AED_EARNINGS.DTA"
data_earnings = pd.read_stata(url)
earnings = data_earnings['earnings']

print(f"Dataset: {len(earnings)} observations")

# =============================================================================
# STEP 2: Sample statistics and standard error
# =============================================================================
# The standard error measures the precision of the sample mean as an estimate
# of the population mean. It shrinks with sqrt(n), not n — so quadrupling the
# sample size is needed to halve the SE.
n             = len(earnings)
mean_earnings = earnings.mean()
std_earnings  = earnings.std(ddof=1)           # ddof=1 for sample std dev
se_earnings   = std_earnings / np.sqrt(n)      # standard error = s / sqrt(n)

print(f"Sample mean:        ${mean_earnings:,.2f}")
print(f"Standard deviation: ${std_earnings:,.2f}")
print(f"Standard error:     ${se_earnings:,.2f}")

# =============================================================================
# STEP 3: t-distribution vs standard normal
# =============================================================================
# When sigma is unknown (estimated by s), we use the t-distribution instead of
# the normal. It has fatter tails — more probability in the extremes — but
# approaches the normal as n grows (the "n >= 30" rule of thumb).
x = np.linspace(-4, 4, 200)

fig, ax = plt.subplots(figsize=(10, 6))
ax.plot(x, stats.norm.pdf(x), '--', linewidth=2, label='Standard Normal')
ax.plot(x, stats.t.pdf(x, df=4), linewidth=2, label='t(4) — fatter tails')
ax.plot(x, stats.t.pdf(x, df=30), linewidth=2, label='t(30) — nearly normal')
ax.set_xlabel('t value')
ax.set_ylabel('Density')
ax.set_title('t-Distribution Approaches Normal as Degrees of Freedom Increase')
ax.legend()
ax.grid(True, alpha=0.3)
plt.tight_layout()
plt.show()

# =============================================================================
# STEP 4: Confidence interval — a range of plausible values for mu
# =============================================================================
# A 95% CI means: if we repeatedly sampled and built CIs, about 95% would
# contain the true mu. Formula: x-bar +/- t_crit * SE
alpha  = 0.05
t_crit = stats.t.ppf(1 - alpha / 2, n - 1)    # critical value from t(n-1)
margin = t_crit * se_earnings

ci_lower = mean_earnings - margin
ci_upper = mean_earnings + margin

print(f"Critical value (t_170, 0.025): {t_crit:.4f}")
print(f"Margin of error:               ${margin:,.2f}")
print(f"95% CI: [${ci_lower:,.2f}, ${ci_upper:,.2f}]")

# Compare 90%, 95%, and 99% — higher confidence requires wider intervals
print(f"\n{'Level':<8} {'Lower':>12} {'Upper':>12} {'Width':>10}")
print("-" * 44)
for conf in [0.90, 0.95, 0.99]:
    tc = stats.t.ppf(1 - (1 - conf) / 2, n - 1)
    lo = mean_earnings - tc * se_earnings
    hi = mean_earnings + tc * se_earnings
    print(f"{conf*100:.0f}%{lo:>14,.2f}{hi:>14,.2f}{hi - lo:>12,.2f}")

# =============================================================================
# STEP 5: Two-sided hypothesis test — H0: mu = $40,000
# =============================================================================
# The t-statistic measures how many standard errors the estimate is from the
# hypothesized value. The p-value is the probability of a result at least as
# extreme as ours if H0 were true.
mu0    = 40000
t_stat = (mean_earnings - mu0) / se_earnings
p_val  = 2 * (1 - stats.t.cdf(abs(t_stat), n - 1))  # two-sided p-value

print(f"H0: mu = ${mu0:,}  vs  Ha: mu != ${mu0:,}")
print(f"t-statistic: {t_stat:.4f}")
print(f"p-value:     {p_val:.4f}")
print(f"Decision:    {'Reject H0' if p_val < 0.05 else 'Do not reject H0'} at alpha = 0.05")

# One-sided (upper-tailed): H0: mu <= 40000 vs Ha: mu > 40000
p_val_one = 1 - stats.t.cdf(t_stat, n - 1)            # upper tail only
t_crit_one = stats.t.ppf(0.95, n - 1)                  # one-sided critical value

print(f"\nOne-sided (upper): p-value = {p_val_one:.4f} (= two-sided / 2)")
print(f"One-sided critical value:    {t_crit_one:.4f} (vs two-sided {t_crit:.4f})")

# =============================================================================
# STEP 6: Statistical vs practical significance — gasoline prices
# =============================================================================
# A $0.14 price gap looks small, but the SE is tiny — so the t-statistic is
# huge and p < 0.0001. Statistical significance says "the difference is real";
# practical significance asks "does it matter?"
url_gas   = "https://raw.githubusercontent.com/quarcs-lab/data-open/master/AED/AED_GASPRICE.DTA"
data_gas  = pd.read_stata(url_gas)
price     = data_gas['price']

n_gas     = len(price)
mean_gas  = price.mean()
se_gas    = price.std(ddof=1) / np.sqrt(n_gas)
mu0_gas   = 3.81                                        # CA state average
t_gas     = (mean_gas - mu0_gas) / se_gas
p_gas     = 2 * (1 - stats.t.cdf(abs(t_gas), n_gas - 1))

print(f"Gas price test: H0: mu = ${mu0_gas}")
print(f"Sample mean: ${mean_gas:.4f}   SE: ${se_gas:.4f}")
print(f"t = {t_gas:.4f},  p = {p_gas:.6f}")
print(f"Decision: {'Reject H0' if p_gas < 0.05 else 'Do not reject H0'}")
print(f"Practical: ${mu0_gas - mean_gas:.2f}/gallon * 15 gal = ${(mu0_gas - mean_gas)*15:.2f} per tank")

# =============================================================================
# STEP 7: Inference for proportions — binary (0/1) data
# =============================================================================
# Proportions are just means of 0/1 variables. The same CI and hypothesis-test
# logic applies — only the SE formula changes: sqrt(p_hat*(1-p_hat)/n).
n_voters  = 921
n_dem     = 480
p_hat     = n_dem / n_voters
se_prop   = np.sqrt(p_hat * (1 - p_hat) / n_voters)

# 95% confidence interval (use z for large-sample proportions)
ci_lo = p_hat - 1.96 * se_prop
ci_hi = p_hat + 1.96 * se_prop

# Hypothesis test: H0: p = 0.50
p0        = 0.50
se_h0     = np.sqrt(p0 * (1 - p0) / n_voters)
z_stat    = (p_hat - p0) / se_h0
p_val_z   = 2 * (1 - stats.norm.cdf(abs(z_stat)))

print(f"Sample proportion: {p_hat:.4f} ({p_hat*100:.1f}%)")
print(f"SE: {se_prop:.4f}")
print(f"95% CI: [{ci_lo:.4f}, {ci_hi:.4f}]")
print(f"\nH0: p = {p0}  z = {z_stat:.4f}  p-value = {p_val_z:.4f}")
print(f"Decision: {'Reject H0' if abs(z_stat) > 1.96 else 'Do not reject H0'}")

```

---

## Chapter 05 Bivariate Data Summary

```python
# =============================================================================
# CHAPTER 5 CHEAT SHEET: Bivariate Data Summary
# =============================================================================

# --- Libraries ---
import pandas as pd                                         # data loading and manipulation
import matplotlib.pyplot as plt                              # creating plots and visualizations
import pyfixest as pf                                        # OLS regression with R-style formulas
# !pip install pyfixest  # if not installed
from statsmodels.nonparametric.smoothers_lowess import lowess  # LOWESS nonparametric smoothing

# =============================================================================
# STEP 1: Load data directly from a URL
# =============================================================================
# pd.read_stata() reads Stata .dta files — the dataset has 29 house sales
url = "https://raw.githubusercontent.com/quarcs-lab/data-open/master/AED/AED_HOUSE.DTA"
data_house = pd.read_stata(url)

print(f"Dataset: {data_house.shape[0]} observations, {data_house.shape[1]} variables")

# =============================================================================
# STEP 2: Descriptive statistics — summarize each variable before comparing
# =============================================================================
# .describe() gives mean, std, min, quartiles, max for both variables
print(data_house[['price', 'size']].describe().round(2))

# =============================================================================
# STEP 3: Scatter plot — visualize the relationship before quantifying it
# =============================================================================
fig, ax = plt.subplots(figsize=(10, 6))
ax.scatter(data_house['size'], data_house['price'], s=60, alpha=0.7)
ax.set_xlabel('House Size (square feet)')
ax.set_ylabel('House Sale Price (dollars)')
ax.set_title('House Price vs Size')
ax.grid(True, alpha=0.3)
plt.tight_layout()
plt.show()

# =============================================================================
# STEP 4: Correlation coefficient — one number for direction and strength
# =============================================================================
# .corr() computes the Pearson correlation matrix; r is unit-free and symmetric
corr_matrix = data_house[['price', 'size']].corr()
r = corr_matrix.loc['price', 'size']

print(f"Correlation coefficient: r = {r:.4f}")
print(f"Strength: {'Strong' if abs(r) > 0.7 else 'Moderate' if abs(r) > 0.4 else 'Weak'}")
print(f"r² = {r**2:.4f} ({r**2*100:.1f}% of variation shared)")

# =============================================================================
# STEP 5: OLS regression — fit the best-fitting line
# =============================================================================
# Formula syntax: 'y ~ x' regresses y on x (intercept included automatically)
fit = pf.feols('price ~ size', data=data_house)

slope     = fit.coef()['size']          # marginal effect: $/sq ft
intercept = fit.coef()['Intercept']     # predicted price when size = 0
r_squared = fit._r2                     # proportion of variation explained

print(f"Estimated equation: price = {intercept:,.0f} + {slope:.2f} × size")
print(f"Interpretation: each additional sq ft is associated with ${slope:,.2f} higher price")
print(f"R-squared: {r_squared:.4f} ({r_squared*100:.1f}% of variation explained)")

# Full regression table (coefficients, std errors, t-stats, p-values, R²)
fit.summary()

# =============================================================================
# STEP 6: Scatter plot with fitted line and R² — visualize model fit
# =============================================================================
# fit.predict() contains the predicted y-values from the estimated equation
fig, ax = plt.subplots(figsize=(10, 6))
ax.scatter(data_house['size'], data_house['price'], s=60, alpha=0.7, label='Actual prices')
ax.plot(data_house['size'], fit.predict(), color='red', linewidth=2, label='Fitted line')
ax.set_xlabel('House Size (square feet)')
ax.set_ylabel('House Sale Price (dollars)')
ax.set_title(f'OLS: price = {intercept:,.0f} + {slope:.2f} × size  (R² = {r_squared:.2%})')
ax.legend()
ax.grid(True, alpha=0.3)
plt.tight_layout()
plt.show()

# =============================================================================
# STEP 7: Reverse regression — association is NOT causation
# =============================================================================
# If regression = causation, the reverse slope would be 1/slope. It is not.
fit_reverse = pf.feols('size ~ price', data=data_house)

print(f"price ~ size  slope: {slope:.4f}")
print(f"size ~ price  slope: {fit_reverse.coef()['price']:.6f}")
print(f"1 / original slope:  {1/slope:.6f}")
print(f"Reciprocals match?   {1/slope:.6f} ≠ {fit_reverse.coef()['price']:.6f}")
print("→ Regression is asymmetric: association, not causation!")

# =============================================================================
# STEP 8: Nonparametric regression — check the linearity assumption
# =============================================================================
# LOWESS fits weighted local regressions; if the curve tracks the OLS line,
# the linear assumption is validated for this dataset
lowess_result = lowess(data_house['price'], data_house['size'], frac=0.6)

fig, ax = plt.subplots(figsize=(10, 6))
ax.scatter(data_house['size'], data_house['price'], s=60, alpha=0.6, label='Actual data')
ax.plot(data_house['size'], fit.predict(), color='red',
        linewidth=2, label='OLS (parametric)')
ax.plot(lowess_result[:, 0], lowess_result[:, 1], color='green',
        linewidth=2, linestyle='--', label='LOWESS (nonparametric)')
ax.set_xlabel('House Size (square feet)')
ax.set_ylabel('House Sale Price (dollars)')
ax.set_title('Parametric vs Nonparametric Regression')
ax.legend()
ax.grid(True, alpha=0.3)
plt.tight_layout()
plt.show()

```

---

## Chapter 06 The Least Squares Estimator

```python
# =============================================================================
# CHAPTER 6 CHEAT SHEET: The Least Squares Estimator
# =============================================================================

# --- Libraries ---
import numpy as np                        # random sampling and numerical operations
import pandas as pd                       # data manipulation
import matplotlib.pyplot as plt           # creating plots and visualizations
import pyfixest as pf                     # OLS regression with R-style formulas
# !pip install pyfixest  # if not installed

# =============================================================================
# STEP 1: Define the Data-Generating Process (DGP)
# =============================================================================
# The DGP specifies the TRUE population relationship: y = β₁ + β₂x + u
# We know the true parameters — in real research, we never do!
beta_1_true = 1       # true intercept
beta_2_true = 2       # true slope
sigma_u     = 2       # error standard deviation

# Generate one sample of n observations
np.random.seed(42)
n = 30
x = np.random.normal(3, 1, n)
u = np.random.normal(0, sigma_u, n)
y = beta_1_true + beta_2_true * x + u

data = pd.DataFrame({'x': x, 'y': y})
print(f"Generated sample: {n} observations from y = {beta_1_true} + {beta_2_true}x + u")

# =============================================================================
# STEP 2: Fit OLS and compare sample vs. population parameters
# =============================================================================
# The sample regression estimates the unknown population line from data
fit = pf.feols('y ~ x', data=data)

b1 = fit.coef()['Intercept']
b2 = fit.coef()['x']

print(f"\nPopulation:  E[y|x] = {beta_1_true} + {beta_2_true}x")
print(f"Sample:      ŷ = {b1:.2f} + {b2:.2f}x")
print(f"Sampling error in slope: b₂ - β₂ = {b2 - beta_2_true:.4f}")

# Full regression table (coefficients, std errors, t-stats, p-values, R²)
fit.summary()

# =============================================================================
# STEP 3: Scatter plot — population line vs. sample line
# =============================================================================
# Visualizing the gap between the true line and our estimate
fig, ax = plt.subplots(figsize=(10, 6))
ax.scatter(data['x'], data['y'], s=50, alpha=0.7, label='Observed data')
ax.plot(data['x'], fit.predict(), color='red', linewidth=2,
        label=f'Sample: ŷ = {b1:.2f} + {b2:.2f}x')
x_range = np.linspace(data['x'].min(), data['x'].max(), 100)
ax.plot(x_range, beta_1_true + beta_2_true * x_range,
        color='green', linewidth=2, linestyle='--',
        label=f'Population: E[y|x] = {beta_1_true} + {beta_2_true}x')
ax.set_xlabel('x')
ax.set_ylabel('y')
ax.set_title('Population Regression vs. Sample Regression')
ax.legend()
ax.grid(True, alpha=0.3)
plt.tight_layout()
plt.show()

# =============================================================================
# STEP 4: Monte Carlo simulation — demonstrate unbiasedness
# =============================================================================
# Draw many samples from the SAME DGP to see how b₂ varies
# Unbiasedness: on average, b₂ equals the true β₂
n_simulations = 1000
b2_estimates = []

for i in range(n_simulations):
    x_sim = np.random.normal(3, 1, n)
    u_sim = np.random.normal(0, sigma_u, n)
    y_sim = beta_1_true + beta_2_true * x_sim + u_sim
    df_sim = pd.DataFrame({'x': x_sim, 'y': y_sim})
    m = pf.feols('y ~ x', data=df_sim)
    b2_estimates.append(m.coef()['x'])

print(f"\nMonte Carlo results ({n_simulations} simulations, n={n} each):")
print(f"  True β₂:              {beta_2_true}")
print(f"  Mean of b₂ estimates: {np.mean(b2_estimates):.4f}  (≈ β₂, confirming unbiasedness)")
print(f"  Std dev of estimates:  {np.std(b2_estimates):.4f}  (empirical standard error)")

# =============================================================================
# STEP 5: Visualize the sampling distribution of b₂
# =============================================================================
# The histogram should be centered on β₂ (unbiasedness) and bell-shaped (CLT)
fig, ax = plt.subplots(figsize=(10, 6))
ax.hist(b2_estimates, bins=40, density=True, alpha=0.7, edgecolor='white',
        label=f'{n_simulations} estimates of b₂')
ax.axvline(beta_2_true, color='green', linewidth=2, linestyle='--',
           label=f'True β₂ = {beta_2_true}')
ax.axvline(np.mean(b2_estimates), color='red', linewidth=2,
           label=f'Mean of estimates = {np.mean(b2_estimates):.4f}')
ax.set_xlabel('Slope estimate (b₂)')
ax.set_ylabel('Density')
ax.set_title('Sampling Distribution of b₂: Unbiasedness + CLT')
ax.legend()
ax.grid(True, alpha=0.3)
plt.tight_layout()
plt.show()

# =============================================================================
# STEP 6: Standard error — what controls precision?
# =============================================================================
# se(b₂) = sₑ / √[Σ(xᵢ - x̄)²]
# Smaller when: (1) model fits well, (2) large n, (3) x spread wide
se_b2       = fit.se()['x']                         # from regression output
s_e         = np.sqrt(np.mean(fit._u_hat**2))      # standard error of regression
x_variation = np.sum((data['x'] - data['x'].mean())**2)

print(f"\nStandard error anatomy (from the single-sample regression):")
print(f"  sₑ (root MSE):          {s_e:.4f}")
print(f"  Σ(xᵢ - x̄)²:            {x_variation:.4f}")
print(f"  se(b₂) = sₑ / √Σ(xᵢ-x̄)² = {s_e / np.sqrt(x_variation):.4f}")
print(f"  se(b₂) from output:     {se_b2:.4f}")

# =============================================================================
# STEP 7: Effect of sample size on precision
# =============================================================================
# Theory: se(b₂) ∝ 1/√n — doubling n cuts SE by ~30%, quadrupling halves it
sample_sizes = [20, 50, 100, 200]

print(f"\n{'n':>6}  {'Mean b₂':>10}  {'Std dev (empirical SE)':>22}")
print("-" * 42)
for ns in sample_sizes:
    estimates = []
    for _ in range(1000):
        xs = np.random.normal(3, 1, ns)
        us = np.random.normal(0, sigma_u, ns)
        ys = beta_1_true + beta_2_true * xs + us
        m = pf.feols('y ~ x', data=pd.DataFrame({'x': xs, 'y': ys}))
        estimates.append(m.coef()['x'])
    print(f"{ns:>6}  {np.mean(estimates):>10.4f}  {np.std(estimates):>22.4f}")

```

---

## Chapter 07 Statistical Inference for Bivariate Regression

```python
# =============================================================================
# CHAPTER 7 CHEAT SHEET: Statistical Inference for Bivariate Regression
# =============================================================================

# --- Libraries ---
import pandas as pd                       # data loading and manipulation
import matplotlib.pyplot as plt           # creating plots and visualizations
import pyfixest as pf                     # OLS regression with R-style formulas
# !pip install pyfixest  # if not installed
from scipy import stats                   # t-distribution and critical values

# =============================================================================
# STEP 1: Load data directly from a URL
# =============================================================================
# pd.read_stata() reads Stata .dta files — the house price dataset has 29 houses
url = "https://raw.githubusercontent.com/quarcs-lab/data-open/master/AED/AED_HOUSE.DTA"
data_house = pd.read_stata(url)

print(f"Dataset: {data_house.shape[0]} observations, {data_house.shape[1]} variables")

# =============================================================================
# STEP 2: Estimate the regression and extract key statistics
# =============================================================================
# The t-statistic measures how many standard errors the estimate is from zero
fit = pf.feols('price ~ size', data=data_house)

slope     = fit.coef()['size']         # marginal effect: $/sq ft
intercept = fit.coef()['Intercept']
se_slope  = fit.se()['size']           # standard error of the slope
t_stat    = fit.tstat()['size']        # t = b2 / se(b2)
p_value   = fit.pvalue()['size']         # two-sided p-value for H0: b2 = 0

print(f"Estimated equation: price = {intercept:,.0f} + {slope:.2f} × size")
print(f"Standard error of slope: {se_slope:.2f}")
print(f"t-statistic: {t_stat:.4f}")
print(f"p-value: {p_value:.6f}")

# Full regression table (coefficients, std errors, t-stats, p-values, R²)
fit.summary()

# =============================================================================
# STEP 3: Confidence interval — a range of plausible values for β₂
# =============================================================================
# CI = b2 ± t_crit × se(b2), using T(n-2) distribution
n  = len(data_house)
df = n - 2                                        # degrees of freedom
t_crit = stats.t.ppf(0.975, df)                   # critical value for 95% CI

ci_lower = slope - t_crit * se_slope
ci_upper = slope + t_crit * se_slope

print(f"Degrees of freedom: {df}")
print(f"Critical t-value (α=0.05, two-sided): {t_crit:.4f}")
print(f"95% CI for slope: [{ci_lower:.2f}, {ci_upper:.2f}]")
print(f"Interpretation: each sq ft adds between ${ci_lower:.0f} and ${ci_upper:.0f} to price")

# =============================================================================
# STEP 4: Hypothesis tests — does size matter? Is the effect $90/sq ft?
# =============================================================================
# Test 1: Statistical significance (H0: β₂ = 0)
print(f"Test H₀: β₂ = 0  →  t = {t_stat:.2f}, p = {p_value:.6f}  →  Reject H₀")

# Test 2: Two-sided test for a specific value (H0: β₂ = 90)
null_value = 90
t_90 = (slope - null_value) / se_slope
p_90 = 2 * (1 - stats.t.cdf(abs(t_90), df))

print(f"Test H₀: β₂ = 90  →  t = {t_90:.4f}, p = {p_90:.4f}  →  Fail to reject H₀")
print(f"  (90 is inside the 95% CI [{ci_lower:.2f}, {ci_upper:.2f}])")

# =============================================================================
# STEP 5: One-sided test — does size increase price by less than $90/sq ft?
# =============================================================================
# H0: β₂ ≥ 90  vs  Ha: β₂ < 90 (lower-tailed test)
p_lower = stats.t.cdf(t_90, df)                   # one-sided p-value (left tail)

print(f"One-sided test H₀: β₂ ≥ 90 vs Hₐ: β₂ < 90")
print(f"  t = {t_90:.4f}, one-sided p = {p_lower:.4f}")
print(f"  Fail to reject at 5% (p = {p_lower:.3f} > 0.05)")
print(f"  Would reject at 10% (p = {p_lower:.3f} < 0.10)")

# =============================================================================
# STEP 6: Robust standard errors — valid with or without heteroskedasticity
# =============================================================================
# HC1 robust SEs protect against non-constant variance in the errors
fit_robust = pf.feols('price ~ size', data=data_house, vcov='HC1')

print(f"{'':20s} {'Standard':>12s} {'Robust (HC1)':>12s}")
print("-" * 46)
print(f"{'SE(size)':<20s} {se_slope:>12.2f} {fit_robust.se()['size']:>12.2f}")
print(f"{'t-statistic':<20s} {t_stat:>12.2f} {fit_robust.tstat()['size']:>12.2f}")
print(f"{'p-value':<20s} {p_value:>12.6f} {fit_robust.pvalue()['size']:>12.6f}")

pct_change = ((fit_robust.se()['size'] - se_slope) / se_slope) * 100
print(f"\nRobust SE is {pct_change:+.1f}% different from standard SE")

# =============================================================================
# STEP 7: Scatter plot with regression line and inference summary
# =============================================================================
fig, ax = plt.subplots(figsize=(10, 6))
ax.scatter(data_house['size'], data_house['price'], s=50, alpha=0.7, label='Actual prices')
ax.plot(data_house['size'], fit.predict(), color='red', linewidth=2, label='Fitted line')
ax.set_xlabel('House Size (square feet)')
ax.set_ylabel('House Sale Price (dollars)')
ax.set_title(f'price = {intercept:,.0f} + {slope:.2f} × size    '
             f'95% CI for slope: [{ci_lower:.0f}, {ci_upper:.0f}]')
ax.legend()
ax.grid(True, alpha=0.3)
plt.tight_layout()
plt.show()

```

---

## Chapter 08 Case Studies for Bivariate Regression

```python
# =============================================================================
# CHAPTER 8 CHEAT SHEET: Case Studies for Bivariate Regression
# =============================================================================

# --- Libraries ---
import pandas as pd                       # data loading and manipulation
import matplotlib.pyplot as plt           # creating plots and visualizations
import pyfixest as pf                     # OLS regression with R-style formulas
# !pip install pyfixest  # if not installed

# =============================================================================
# STEP 1: Load OECD health data from a URL
# =============================================================================
# pd.read_stata() reads Stata .dta files — this dataset covers 34 OECD countries
url_health = "https://raw.githubusercontent.com/quarcs-lab/data-open/master/AED/AED_HEALTH2009.DTA"
data_health = pd.read_stata(url_health)

print(f"Health dataset: {data_health.shape[0]} countries, {data_health.shape[1]} variables")

# =============================================================================
# STEP 2: Descriptive statistics — summarize before modeling
# =============================================================================
# .describe() gives mean, std, min, quartiles, max for each variable
print(data_health[['hlthpc', 'lifeexp', 'infmort', 'gdppc']].describe().round(2))

# =============================================================================
# STEP 3: Health outcomes regression with robust standard errors
# =============================================================================
# Does higher health spending improve life expectancy?
fit_life = pf.feols('lifeexp ~ hlthpc', data=data_health)

slope_life = fit_life.coef()['hlthpc']
r2_life    = fit_life._r2

print(f"Life expectancy: slope = {slope_life:.5f}, R² = {r2_life:.4f}")
print(f"Each extra $1,000 in spending → {slope_life*1000:.2f} more years of life expectancy")

# Robust standard errors adjust for non-constant error variance (heteroskedasticity)
fit_life_robust = pf.feols('lifeexp ~ hlthpc', data=data_health, vcov='HC1')
fit_life_robust.summary()

# =============================================================================
# STEP 4: Health spending vs GDP — income elasticity
# =============================================================================
# How much of health spending is driven by national income?
fit_gdp = pf.feols('hlthpc ~ gdppc', data=data_health)

slope_gdp = fit_gdp.coef()['gdppc']
r2_gdp    = fit_gdp._r2

# Income elasticity at the mean: (slope × mean_x) / mean_y
mean_gdp  = data_health['gdppc'].mean()
mean_hlth = data_health['hlthpc'].mean()
elasticity = (slope_gdp * mean_gdp) / mean_hlth

print(f"Health spending on GDP: slope = {slope_gdp:.4f}, R² = {r2_gdp:.4f}")
print(f"Income elasticity at the mean: {elasticity:.2f} (≈1.0 → normal good)")

# =============================================================================
# STEP 5: Outlier robustness — excluding USA and Luxembourg
# =============================================================================
# Two countries drive much of the model's "misfit" — test robustness by excluding them
data_subset = data_health[(data_health['code'] != 'USA') &
                          (data_health['code'] != 'LUX')]

fit_subset = pf.feols('hlthpc ~ gdppc', data=data_subset)

print(f"\nAll 34 countries:  slope = {slope_gdp:.4f}, R² = {r2_gdp:.4f}")
print(f"Excluding USA/LUX: slope = {fit_subset.coef()['gdppc']:.4f}, R² = {fit_subset._r2:.4f}")
print("Removing 2 of 34 countries transforms R² — always check for influential observations!")

fig, axes = plt.subplots(1, 2, figsize=(14, 5))
for ax, df, mdl, title in zip(
        axes,
        [data_health, data_subset],
        [fit_gdp, fit_subset],
        ['All 34 Countries', 'Excluding USA & Luxembourg']):
    ax.scatter(df['gdppc'], df['hlthpc'], s=50, alpha=0.7)
    ax.plot(df['gdppc'], mdl.predict(), color='red', linewidth=2)
    ax.set_xlabel('GDP per capita ($)')
    ax.set_ylabel('Health spending per capita ($)')
    ax.set_title(f'{title}  (R² = {mdl._r2:.2f})')
    ax.grid(True, alpha=0.3)
plt.tight_layout()
plt.show()

# =============================================================================
# STEP 6: CAPM — estimating Coca-Cola's beta (systematic risk)
# =============================================================================
# Beta measures how a stock's excess return co-moves with the market excess return
url_capm = "https://raw.githubusercontent.com/quarcs-lab/data-open/master/AED/AED_CAPM.DTA"
data_capm = pd.read_stata(url_capm)

fit_capm = pf.feols('rko_rf ~ rm_rf', data=data_capm)

alpha = fit_capm.coef()['Intercept']     # excess return beyond CAPM prediction
beta  = fit_capm.coef()['rm_rf']         # systematic risk
r2_capm = fit_capm._r2

print(f"Coca-Cola CAPM: alpha = {alpha:.4f}, beta = {beta:.4f}, R² = {r2_capm:.4f}")
print(f"Beta < 1 → defensive stock (moves less than the market)")
print(f"R² = {r2_capm:.2%} explained by market; {1-r2_capm:.2%} is idiosyncratic risk")

# Full regression table
fit_capm.summary()

# =============================================================================
# STEP 7: Okun's Law — GDP growth vs unemployment change
# =============================================================================
# Okun (1962): each +1 point in unemployment → ≈ -2 points in GDP growth
url_gdp = "https://raw.githubusercontent.com/quarcs-lab/data-open/master/AED/AED_GDPUNEMPLOY.DTA"
data_gdp = pd.read_stata(url_gdp)

fit_okun = pf.feols('rgdpgrowth ~ uratechange', data=data_gdp)

slope_okun = fit_okun.coef()['uratechange']
r2_okun    = fit_okun._r2

print(f"Okun's Law: slope = {slope_okun:.2f} (Okun's original: -2.0)")
print(f"R² = {r2_okun:.4f} — unemployment explains {r2_okun*100:.0f}% of GDP growth variation")

# Scatter plot with fitted line
fig, ax = plt.subplots(figsize=(10, 6))
ax.scatter(data_gdp['uratechange'], data_gdp['rgdpgrowth'], s=50, alpha=0.7)
ax.plot(data_gdp['uratechange'], fit_okun.predict(), color='red', linewidth=2,
        label=f'Fitted: slope = {slope_okun:.2f}')
ax.axhline(y=0, color='gray', linestyle=':', linewidth=1, alpha=0.5)
ax.set_xlabel('Change in unemployment rate (percentage points)')
ax.set_ylabel('Real GDP growth (%)')
ax.set_title(f"Okun's Law: GDP Growth vs Unemployment Change  (R² = {r2_okun:.2f})")
ax.legend()
ax.grid(True, alpha=0.3)
plt.tight_layout()
plt.show()

```

---

## Chapter 09 Models with Natural Logarithms

```python
# =============================================================================
# CHAPTER 9 CHEAT SHEET: Models with Natural Logarithms
# =============================================================================

# --- Libraries ---
import numpy as np                        # logarithms and exponentials
import pandas as pd                       # data loading and manipulation
import matplotlib.pyplot as plt           # creating plots and visualizations
import pyfixest as pf                     # OLS regression with R-style formulas
# !pip install pyfixest  # if not installed

# =============================================================================
# STEP 1: Load the earnings-education dataset
# =============================================================================
# pd.read_stata() reads Stata .dta files directly from a URL
url_earn = "https://raw.githubusercontent.com/quarcs-lab/data-open/master/AED/AED_EARNINGS.DTA"
data_earnings = pd.read_stata(url_earn)

print(f"Dataset: {data_earnings.shape[0]} observations, {data_earnings.shape[1]} variables")

# =============================================================================
# STEP 2: Logarithmic approximation — why economists use logs
# =============================================================================
# Key property: Δln(x) ≈ Δx/x (proportionate change)
# Multiplying by 100 gives the percentage change
x0, x1 = 40, 40.4
exact = (x1 - x0) / x0
approx = np.log(x1) - np.log(x0)
print(f"Change from {x0} to {x1}:")
print(f"  Exact proportionate change: {exact:.6f} ({exact*100:.2f}%)")
print(f"  Log approximation Δln(x):   {approx:.6f} ({approx*100:.2f}%)")

# =============================================================================
# STEP 3: Descriptive statistics and log transformations
# =============================================================================
# Create log-transformed variables for the regression models
data_earnings['lnearn'] = np.log(data_earnings['earnings'])
data_earnings['lneduc'] = np.log(data_earnings['education'])

print(data_earnings[['earnings', 'lnearn', 'education', 'lneduc']].describe().round(2))

# =============================================================================
# STEP 4: Estimate all four model specifications
# =============================================================================
# Each model answers a different economic question about earnings and education

# Model 1: Linear — Δy = β₁Δx (dollar change per year of education)
fit_linear = pf.feols('earnings ~ education', data=data_earnings)

# Model 2: Log-linear — 100β₁ ≈ % change in y per unit x (semi-elasticity)
fit_loglin = pf.feols('lnearn ~ education', data=data_earnings)

# Model 3: Log-log — β₁ ≈ % change in y per % change in x (elasticity)
fit_loglog = pf.feols('lnearn ~ lneduc', data=data_earnings)

# Model 4: Linear-log — β₁/100 ≈ dollar change per % change in x
fit_linlog = pf.feols('earnings ~ lneduc', data=data_earnings)

# Print the most important model: log-linear (semi-elasticity)
semi_elast = fit_loglin.coef()['education']
print(f"Log-linear: each year of education → {100*semi_elast:.1f}% higher earnings")
print(f"Log-log elasticity: {fit_loglog.coef()['lneduc']:.3f}")

# Full regression table for the log-linear model
fit_loglin.summary()

# =============================================================================
# STEP 5: Compare all four models side by side
# =============================================================================
# The comparison shows that model choice affects both R² and interpretation
models = {
    'Linear':     ('earnings ~ education',  fit_linear,  'education', '${:,.0f} per year'),
    'Log-linear': ('ln(y) ~ x',            fit_loglin,  'education', '{:.1f}% per year'),
    'Log-log':    ('ln(y) ~ ln(x)',         fit_loglog,  'lneduc',   '{:.2f}% per 1%'),
    'Linear-log': ('y ~ ln(x)',            fit_linlog,  'lneduc',   '${:,.0f} per 1%'),
}

print(f"{'Model':<12} {'Specification':<16} {'Slope':>10} {'R²':>8}  Interpretation")
print("-" * 75)
for name, (spec, m, var, fmt) in models.items():
    slope = m.coef()[var]
    interp = fmt.format(100*slope if 'per year' in fmt and 'Log' in name else slope/100 if 'per 1%' in fmt and name == 'Linear-log' else slope)
    print(f"{name:<12} {spec:<16} {slope:>10.4f} {m._r2:>8.3f}  {interp}")

# =============================================================================
# STEP 6: Scatter plot with the log-linear fitted line
# =============================================================================
# The log-linear model (semi-elasticity) provides the best fit for earnings data
fig, ax = plt.subplots(figsize=(10, 6))
ax.scatter(data_earnings['education'], data_earnings['lnearn'], s=50, alpha=0.7)
ax.plot(data_earnings['education'], fit_loglin.predict(),
        color='red', linewidth=2, label='Fitted line')
ax.set_xlabel('Education (years)')
ax.set_ylabel('ln(Earnings)')
ax.set_title(f'Log-Linear Model: semi-elasticity = {semi_elast:.4f}  (R² = {fit_loglin._r2:.3f})')
ax.legend()
ax.grid(True, alpha=0.3)
plt.tight_layout()
plt.show()

# =============================================================================
# STEP 7: Exponential growth — S&P 500 and the Rule of 72
# =============================================================================
# Exponential growth in levels becomes linear in logs:
# ln(x_t) ≈ ln(x₀) + r × t, where slope r = annual growth rate
url_sp500 = "https://raw.githubusercontent.com/quarcs-lab/data-open/master/AED/AED_SP500INDEX.DTA"
data_sp500 = pd.read_stata(url_sp500)

fit_sp500 = pf.feols('lnsp500 ~ year', data=data_sp500)
growth_rate = fit_sp500.coef()['year']

print(f"S&P 500 estimated growth rate: {100*growth_rate:.2f}% per year")
print(f"Rule of 72: doubles every {72/(100*growth_rate):.1f} years")
print(f"R-squared: {fit_sp500._r2:.4f}")

# Visualize: exponential in levels vs. linear in logs
fig, axes = plt.subplots(1, 2, figsize=(14, 5))
axes[0].plot(data_sp500['year'], data_sp500['sp500'], linewidth=2)
axes[0].set_xlabel('Year')
axes[0].set_ylabel('S&P 500 Index')
axes[0].set_title('Exponential Growth in Levels')
axes[0].grid(True, alpha=0.3)

axes[1].plot(data_sp500['year'], data_sp500['lnsp500'], linewidth=2)
axes[1].plot(data_sp500['year'], fit_sp500.predict(),
             color='red', linewidth=2, linestyle='--', label='Fitted (linear)')
axes[1].set_xlabel('Year')
axes[1].set_ylabel('ln(S&P 500 Index)')
axes[1].set_title(f'Linear in Logs: growth = {100*growth_rate:.2f}%/year')
axes[1].legend()
axes[1].grid(True, alpha=0.3)
plt.tight_layout()
plt.show()

```

---

## Chapter 10 Data Summary for Multiple Regression

```python
# =============================================================================
# CHAPTER 10 CHEAT SHEET: Data Summary for Multiple Regression
# =============================================================================

# --- Libraries ---
import numpy as np                                          # numerical operations
import pandas as pd                                         # data loading and manipulation
import matplotlib.pyplot as plt                             # creating plots and visualizations
import seaborn as sns                                       # statistical visualization (heatmaps, pairplots)
import pyfixest as pf                                       # OLS regression with R-style formulas
# !pip install pyfixest  # if not installed
from statsmodels.stats.outliers_influence import variance_inflation_factor  # multicollinearity detection

# =============================================================================
# STEP 1: Load data and explore
# =============================================================================
# pd.read_stata() reads Stata .dta files directly from a URL
url = "https://raw.githubusercontent.com/quarcs-lab/data-open/master/AED/AED_HOUSE.DTA"
data_house = pd.read_stata(url)

print(f"Dataset: {data_house.shape[0]} observations, {data_house.shape[1]} variables")
print(data_house[['price', 'size', 'bedrooms', 'bathrooms', 'lotsize', 'age']].describe().round(2))

# =============================================================================
# STEP 2: Partial effects vs. total effects — why controls matter
# =============================================================================
# Bivariate regression captures TOTAL effect (direct + indirect through size)
fit_bivariate = pf.feols('price ~ bedrooms', data=data_house)

# Multiple regression isolates the PARTIAL effect (holding size constant)
fit_partial = pf.feols('price ~ bedrooms + size', data=data_house)

print(f"Bedrooms coefficient (bivariate):  ${fit_bivariate.coef()['bedrooms']:,.2f}")
print(f"Bedrooms coefficient (multiple):   ${fit_partial.coef()['bedrooms']:,.2f}")
print(f"Change: ${fit_partial.coef()['bedrooms'] - fit_bivariate.coef()['bedrooms']:,.2f}")
# The coefficient drops from ~$23,667 to ~$1,553 once we control for size

# =============================================================================
# STEP 3: Correlation matrix — check pairwise associations before modeling
# =============================================================================
# High correlations between regressors signal potential multicollinearity
corr_vars = ['price', 'size', 'bedrooms', 'bathrooms', 'lotsize', 'age']
corr_matrix = data_house[corr_vars].corr()

fig, ax = plt.subplots(figsize=(10, 8))
sns.heatmap(corr_matrix, annot=True, fmt='.3f', cmap='coolwarm', center=0,
            square=True, linewidths=1)
ax.set_title('Correlation Matrix Heatmap')
plt.tight_layout()
plt.show()

print(f"Price-Size correlation: {corr_matrix.loc['price', 'size']:.3f}")
print(f"Size-Bedrooms correlation: {corr_matrix.loc['size', 'bedrooms']:.3f}")

# =============================================================================
# STEP 4: Full multiple regression — estimate partial effects
# =============================================================================
# Each coefficient measures the change in price for a one-unit change in that
# variable, holding ALL other regressors constant
fit_full = pf.feols('price ~ size + bedrooms + bathrooms + lotsize + age + monthsold',
                    data=data_house)

size_coef = fit_full.coef()['size']
print(f"Size effect: each additional sq ft is associated with ${size_coef:,.2f} higher price")
print(f"R-squared: {fit_full._r2:.4f} ({fit_full._r2*100:.1f}% of variation explained)")
print(f"Adjusted R-squared: {fit_full._adj_r2:.4f}")

# Full regression table (coefficients, std errors, t-stats, p-values)
fit_full.summary()

# =============================================================================
# STEP 5: FWL theorem — how "holding constant" actually works
# =============================================================================
# Step A: Regress size on all other regressors, keep residuals
fit_size_on_others = pf.feols('size ~ bedrooms + bathrooms + lotsize + age + monthsold',
                              data=data_house)
resid_size = fit_size_on_others._u_hat

# Step B: Regress price on those residuals — the slope matches the full model
data_house['resid_size'] = resid_size
fit_fwl = pf.feols('price ~ resid_size', data=data_house)

print(f"Size coef from FULL regression:     {fit_full.coef()['size']:.10f}")
print(f"Coef from FWL residual regression:  {fit_fwl.coef()['resid_size']:.10f}")
# These are identical — the FWL theorem in action

# =============================================================================
# STEP 6: Model comparison — parsimony vs. complexity
# =============================================================================
# Compare simple (size only) vs. full model using fit statistics
fit_simple = pf.feols('price ~ size', data=data_house)

comparison = pd.DataFrame({
    'Model': ['Size only', 'Full (all variables)'],
    'R²':     [fit_simple._r2,     fit_full._r2],
    'Adj R²': [fit_simple._adj_r2, fit_full._adj_r2],
    'AIC':    [fit_simple._aic,    fit_full._aic],
    'BIC':    [fit_simple._bic,    fit_full._bic],
})
print(comparison.to_string(index=False))
# Adj R² DECREASES when adding 5 weak predictors — parsimony wins

# =============================================================================
# STEP 7: VIF — detect multicollinearity
# =============================================================================
# VIF_j = 1 / (1 - R²_j), where R²_j is from regressing x_j on all other x's
# VIF > 5: moderate concern; VIF > 10: severe multicollinearity
X = data_house[['size', 'bedrooms', 'bathrooms', 'lotsize', 'age', 'monthsold']]
vif_data = pd.DataFrame({
    'Variable': X.columns,
    'VIF': [variance_inflation_factor(X.values, i) for i in range(X.shape[1])]
})
print(vif_data.to_string(index=False))

# =============================================================================
# STEP 8: Diagnostics — actual vs. predicted and residual plots
# =============================================================================
# Good fit: points hug the 45° line; residuals scatter randomly around zero
fig, axes = plt.subplots(1, 2, figsize=(14, 6))

# Actual vs. predicted
axes[0].scatter(data_house['price'], fit_full.predict(), alpha=0.7, s=50)
axes[0].plot([data_house['price'].min(), data_house['price'].max()],
             [data_house['price'].min(), data_house['price'].max()],
             'r--', linewidth=2, label='Perfect prediction (45° line)')
axes[0].set_xlabel('Actual Price ($)')
axes[0].set_ylabel('Predicted Price ($)')
axes[0].set_title('Actual vs Predicted')
axes[0].legend()
axes[0].grid(True, alpha=0.3)

# Residual plot
axes[1].scatter(fit_full.predict(), fit_full._u_hat, alpha=0.7, s=50)
axes[1].axhline(y=0, color='red', linestyle='--', linewidth=2)
axes[1].set_xlabel('Fitted Values ($)')
axes[1].set_ylabel('Residuals ($)')
axes[1].set_title('Residual Plot')
axes[1].grid(True, alpha=0.3)

plt.tight_layout()
plt.show()

```

---

## Chapter 11 Statistical Inference for Multiple Regression

```python
# =============================================================================
# CHAPTER 11 CHEAT SHEET: Statistical Inference for Multiple Regression
# =============================================================================

# --- Libraries ---
import numpy as np                              # numerical operations
import pandas as pd                             # data loading and manipulation
import matplotlib.pyplot as plt                 # creating plots and visualizations
import pyfixest as pf                           # OLS regression with R-style formulas
# !pip install pyfixest  # if not installed
from scipy import stats                         # t and F distributions for inference
from statsmodels.formula.api import ols as sm_ols  # for ANOVA model comparison
from statsmodels.stats.anova import anova_lm    # ANOVA table for model comparison

# =============================================================================
# STEP 1: Load data directly from a URL
# =============================================================================
# pd.read_stata() reads Stata .dta files; the dataset has 29 houses from Davis, CA
url = "https://raw.githubusercontent.com/quarcs-lab/data-open/master/AED/AED_HOUSE.DTA"
data_house = pd.read_stata(url)

print(f"Dataset: {data_house.shape[0]} observations, {data_house.shape[1]} variables")
print(data_house[['price', 'size', 'bedrooms', 'bathrooms', 'lotsize', 'age']].describe().round(2))

# =============================================================================
# STEP 2: Estimate the full multiple regression model
# =============================================================================
# Formula syntax: 'y ~ x1 + x2 + ...' includes an intercept automatically
# pf.feols() estimates the model in one step (no separate .fit() needed)
fit_full = pf.feols('price ~ size + bedrooms + bathrooms + lotsize + age + monthsold',
                    data=data_house)

n = int(fit_full._N)
k = len(fit_full.coef())
df = n - k  # degrees of freedom for t and F tests

print(f"\nSize effect: ${fit_full.coef()['size']:,.2f} per sq ft (p = {fit_full.pvalue()['size']:.4f})")
print(f"R-squared: {fit_full._r2:.4f} ({fit_full._r2*100:.1f}% of variation explained)")
print(f"Degrees of freedom: n-k = {n}-{k} = {df}")

# Full regression table (coefficients, std errors, t-stats, p-values, R²)
fit_full.summary()

# =============================================================================
# STEP 3: Confidence intervals — does the CI exclude zero?
# =============================================================================
# 95% CI: b_j ± t_critical × se(b_j)
# If the interval excludes zero, the coefficient is statistically significant at 5%
conf_int = fit_full.confint()
print("\n95% Confidence Intervals:")
print(conf_int.round(2))

# Manual calculation for the size coefficient
coef_size = fit_full.coef()['size']
se_size   = fit_full.se()['size']
t_crit    = stats.t.ppf(0.975, df)  # 0.975 = upper tail for two-sided 95% CI

ci_lower = coef_size - t_crit * se_size
ci_upper = coef_size + t_crit * se_size
print(f"\nSize 95% CI: [${ci_lower:.2f}, ${ci_upper:.2f}]  (excludes zero → significant)")

# =============================================================================
# STEP 4: Hypothesis test on a single coefficient
# =============================================================================
# Test H₀: β_size = 50 vs H₁: β_size ≠ 50
# t = (b_j - hypothesized value) / se(b_j)
null_value = 50
t_stat = (coef_size - null_value) / se_size
p_value = 2 * (1 - stats.t.cdf(abs(t_stat), df))

print(f"\nTest H₀: β_size = {null_value}")
print(f"  t-statistic: {t_stat:.4f}")
print(f"  p-value: {p_value:.4f}")
print(f"  Decision: {'Reject' if p_value < 0.05 else 'Fail to reject'} H₀ at 5% level")

# Test of statistical significance: H₀: β_size = 0
t_stat_zero = coef_size / se_size
print(f"\nTest H₀: β_size = 0")
print(f"  t-statistic: {t_stat_zero:.4f}, p-value: {fit_full.pvalue()['size']:.6f}")
print(f"  Size IS statistically significant at 5% level")

# =============================================================================
# STEP 5: Joint F-test — are groups of coefficients jointly significant?
# =============================================================================
# Overall F-test: H₀: all slope coefficients = 0
# Use statsmodels for F-test functionality
sm_full = sm_ols('price ~ size + bedrooms + bathrooms + lotsize + age + monthsold',
                 data=data_house).fit()
print(f"\nOverall F-test: F = {sm_full.fvalue:.4f}, p = {sm_full.f_pvalue:.6e}")
print(f"  At least one variable matters → model is jointly significant")

# Subset F-test: are variables other than size jointly significant?
# H₀: β_bedrooms = β_bathrooms = β_lotsize = β_age = β_monthsold = 0
hypotheses = ['bedrooms = 0', 'bathrooms = 0', 'lotsize = 0',
              'age = 0', 'monthsold = 0']
f_test_result = sm_full.f_test(hypotheses)
print(f"\nSubset F-test (drop 5 vars, keep size):")
print(f"  F = {f_test_result.fvalue[0][0]:.4f}, p = {float(f_test_result.pvalue):.4f}")
print(f"  Extra variables are NOT jointly significant → simpler model preferred")

# =============================================================================
# STEP 6: Model comparison — restricted vs unrestricted
# =============================================================================
# Restricted model: only size as predictor
fit_restricted = pf.feols('price ~ size', data=data_house)
sm_restricted = sm_ols('price ~ size', data=data_house).fit()

# ANOVA table confirms the F-test result
anova_results = anova_lm(sm_restricted, sm_full)
print("\nANOVA: Restricted (size only) vs Full model:")
print(anova_results)

# Compare fit statistics
print(f"\n{'Model':<25} {'R²':>8} {'Adj. R²':>9}")
print("-" * 44)
for name, m in [('Size only', fit_restricted), ('Full model', fit_full)]:
    print(f"{name:<25} {m._r2:>8.4f} {m._adj_r2:>9.4f}")

# =============================================================================
# STEP 7: Robust standard errors — valid under heteroskedasticity
# =============================================================================
# HC1 (White's correction) provides valid inference without constant variance
fit_robust = pf.feols('price ~ size + bedrooms + bathrooms + lotsize + age + monthsold',
                      data=data_house, vcov='HC1')

print("\nStandard vs Robust SEs:")
print(f"{'Variable':<14} {'Coef':>10} {'Std SE':>10} {'Robust SE':>10} {'p (robust)':>10}")
print("-" * 56)
for var in fit_full.coef().index:
    print(f"{var:<14} {fit_full.coef()[var]:>10.2f} "
          f"{fit_full.se()[var]:>10.2f} {fit_robust.se()[var]:>10.2f} "
          f"{fit_robust.pvalue()[var]:>10.4f}")

# =============================================================================
# STEP 8: Coefficient plot — visual summary of significance
# =============================================================================
# Error bars crossing zero = not significant at 5%
params_plot = fit_full.coef()[1:]  # exclude intercept
ci_plot = conf_int.iloc[1:, :]

fig, ax = plt.subplots(figsize=(10, 6))
y_pos = np.arange(len(params_plot))
ax.errorbar(params_plot.values, y_pos,
            xerr=[params_plot.values - ci_plot.iloc[:, 0].values,
                  ci_plot.iloc[:, 1].values - params_plot.values],
            fmt='o', markersize=8, capsize=5, capthick=2, linewidth=2)
ax.axvline(x=0, color='red', linestyle='--', linewidth=1.5, alpha=0.7, label='H₀: β = 0')
ax.set_yticks(y_pos)
ax.set_yticklabels(params_plot.index)
ax.set_xlabel('Coefficient Value')
ax.set_title('Coefficient Estimates with 95% Confidence Intervals')
ax.legend()
ax.grid(True, alpha=0.3, axis='x')
plt.tight_layout()
plt.show()

```

---

## Chapter 12 Further Topics in Multiple Regression

```python
# =============================================================================
# CHAPTER 12 CHEAT SHEET: Further Topics in Multiple Regression
# =============================================================================

# --- Libraries ---
import pandas as pd                       # data loading and manipulation
import numpy as np                        # numerical operations
import matplotlib.pyplot as plt           # creating plots and visualizations
import pyfixest as pf                     # OLS regression with R-style formulas
# !pip install pyfixest  # if not installed
from statsmodels.formula.api import ols as sm_ols  # for prediction intervals
from scipy import stats                   # statistical distributions for CIs and power
from statsmodels.graphics.tsaplots import plot_acf  # autocorrelation plots

# =============================================================================
# STEP 1: Load house price data from a URL
# =============================================================================
# pd.read_stata() reads Stata .dta files directly from the web
url_house = "https://raw.githubusercontent.com/quarcs-lab/data-open/master/AED/AED_HOUSE.DTA"
data_house = pd.read_stata(url_house)

print(f"Dataset: {data_house.shape[0]} observations, {data_house.shape[1]} variables")
print(data_house[['price', 'size', 'bedrooms', 'bathrooms', 'lotsize', 'age']].describe().round(2))

# =============================================================================
# STEP 2: OLS regression with default standard errors
# =============================================================================
# Default SEs assume homoskedasticity (constant error variance)
fit_default = pf.feols('price ~ size + bedrooms + bathrooms + lotsize + age + monthsold',
                       data=data_house)

print(f"\nR-squared: {fit_default._r2:.4f}")
print(f"Size effect (default): ${fit_default.coef()['size']:,.2f} per sq ft")
fit_default.summary()

# =============================================================================
# STEP 3: Robust (HC1) standard errors — compare with default
# =============================================================================
# HC1 SEs correct for heteroskedasticity without changing coefficient estimates
# Only the SEs, t-statistics, and confidence intervals change
fit_robust = pf.feols('price ~ size + bedrooms + bathrooms + lotsize + age + monthsold',
                      data=data_house, vcov='HC1')

# SE ratio: how much heteroskedasticity affects each coefficient's uncertainty
print(f"{'Variable':<14} {'Coef':>10} {'Default SE':>12} {'Robust SE':>12} {'Ratio':>8}")
print("-" * 58)
for var in fit_default.coef().index:
    coef  = fit_default.coef()[var]
    se_d  = fit_default.se()[var]
    se_r  = fit_robust.se()[var]
    ratio = se_r / se_d                   # ratio > 1 → default was too optimistic
    print(f"{var:<14} {coef:>10.2f} {se_d:>12.2f} {se_r:>12.2f} {ratio:>8.3f}")

# =============================================================================
# STEP 4: Prediction — conditional mean CI vs. individual forecast PI
# =============================================================================
# Predicting E[y|x*] is more precise than predicting an individual y|x*
fit_simple = pf.feols('price ~ size', data=data_house)
# Use statsmodels for prediction intervals (not available in pyfixest)
sm_simple = sm_ols('price ~ size', data=data_house).fit()

# Predict for a 2000 sq ft house
new_house = pd.DataFrame({'size': [2000]})
pred = sm_simple.get_prediction(new_house)
pred_frame = pred.summary_frame(alpha=0.05)

s_e = np.sqrt(np.mean(fit_simple._u_hat**2))  # RMSE — irreducible individual uncertainty

print(f"\nPredicted price (2000 sq ft): ${pred_frame['mean'].values[0]:,.0f}")
print(f"95% CI for E[Y|X=2000]: [${pred_frame['mean_ci_lower'].values[0]:,.0f}, "
      f"${pred_frame['mean_ci_upper'].values[0]:,.0f}]")
print(f"95% PI for individual Y:  [${pred_frame['obs_ci_lower'].values[0]:,.0f}, "
      f"${pred_frame['obs_ci_upper'].values[0]:,.0f}]")
print(f"\nRMSE (s_e): ${s_e:,.0f} — PI can never be narrower than ±1.96 × s_e")

# Visualize: CI (narrow) vs. PI (wide)
sizes_sorted = data_house[['size']].sort_values('size')
pred_all = sm_simple.get_prediction(sizes_sorted)
pred_f = pred_all.summary_frame(alpha=0.05)

fig, ax = plt.subplots(figsize=(10, 6))
ax.scatter(data_house['size'], data_house['price'], s=50, alpha=0.6, label='Actual')
ax.plot(sizes_sorted['size'], pred_f['mean'], color='red', linewidth=2, label='Fitted line')
ax.fill_between(sizes_sorted['size'], pred_f['mean_ci_lower'], pred_f['mean_ci_upper'],
                color='red', alpha=0.2, label='95% CI (conditional mean)')
ax.fill_between(sizes_sorted['size'], pred_f['obs_ci_lower'], pred_f['obs_ci_upper'],
                color='blue', alpha=0.1, label='95% PI (individual)')
ax.set_xlabel('House Size (sq ft)')
ax.set_ylabel('House Price ($)')
ax.set_title('Confidence Interval vs. Prediction Interval')
ax.legend()
ax.grid(True, alpha=0.3)
plt.tight_layout()
plt.show()

# =============================================================================
# STEP 5: HAC (Newey-West) standard errors for time series
# =============================================================================
# Time series errors are often autocorrelated — HAC SEs account for this
url_gdp = "https://raw.githubusercontent.com/quarcs-lab/data-open/master/AED/AED_REALGDPPC.DTA"
data_gdp = pd.read_stata(url_gdp)

mean_growth = data_gdp['growth'].mean()
n_gdp       = len(data_gdp)
lag_length   = int(0.75 * n_gdp**(1/3))  # rule of thumb: m = 0.75 × T^(1/3)

# Compare default SE vs. HAC SE for the mean
se_default = data_gdp['growth'].std() / np.sqrt(n_gdp)
data_gdp['_const'] = 1
data_gdp['_time'] = range(len(data_gdp))
fit_hac = pf.feols('growth ~ 1', data=data_gdp,
                   vcov='NW', vcov_kwargs={'time_id': '_time', 'lag': lag_length})

print(f"\nGDP Growth: mean = {mean_growth:.4f}")
print(f"Default SE (no autocorrelation): {se_default:.6f}")
print(f"HAC SE (lag = {lag_length}):            {fit_hac.se()['Intercept']:.6f}")
print(f"Ratio HAC/Default: {fit_hac.se()['Intercept'] / se_default:.3f}")

# Correlogram — visualize autocorrelation structure
fig, ax = plt.subplots(figsize=(10, 6))
plot_acf(data_gdp['growth'], lags=10, ax=ax, alpha=0.05)
ax.set_xlabel('Lag')
ax.set_ylabel('Autocorrelation')
ax.set_title('Correlogram of GDP Growth')
plt.tight_layout()
plt.show()

# =============================================================================
# STEP 6: Power curve — Type I vs. Type II error tradeoff
# =============================================================================
# Power = P(reject H₀ | H₀ is false) — depends on true effect size
alpha = 0.05
se_test = 15                              # hypothetical standard error
n_test  = 30
t_crit  = stats.t.ppf(1 - alpha / 2, df=n_test - 1)

# Power as a function of the true coefficient
beta_range = np.linspace(-60, 60, 500)
power = []
for beta_true in beta_range:
    ncp = beta_true / se_test             # non-centrality parameter
    # Two-sided test: reject if |t| > t_crit
    power_val = 1 - (stats.t.cdf(t_crit - ncp, df=n_test - 1)
                      - stats.t.cdf(-t_crit - ncp, df=n_test - 1))
    power.append(power_val)

fig, ax = plt.subplots(figsize=(10, 6))
ax.plot(beta_range, power, linewidth=2)
ax.axhline(0.05, color='gray', linestyle='--', alpha=0.5, label='α = 0.05 (Type I)')
ax.axhline(0.80, color='green', linestyle='--', alpha=0.5, label='Power = 0.80 target')
ax.axvline(0, color='gray', linestyle='-', alpha=0.3, label='H₀: β = 0')
ax.set_xlabel('True Coefficient Value (β)')
ax.set_ylabel('Power = P(Reject H₀)')
ax.set_title('Power Curve: Larger Effects Are Easier to Detect')
ax.legend()
ax.grid(True, alpha=0.3)
plt.tight_layout()
plt.show()

# =============================================================================
# STEP 7: Bootstrap confidence intervals — no distributional assumptions
# =============================================================================
# Resample data with replacement to estimate the sampling distribution of β
np.random.seed(42)
n_boot = 1000
boot_slopes = []

for _ in range(n_boot):
    boot_sample = data_house.sample(n=len(data_house), replace=True)
    boot_fit    = pf.feols('price ~ size', data=boot_sample)
    boot_slopes.append(boot_fit.coef()['size'])

# Percentile method: 95% CI = [2.5th, 97.5th percentile]
ci_lower = np.percentile(boot_slopes, 2.5)
ci_upper = np.percentile(boot_slopes, 97.5)
ols_slope = fit_simple.coef()['size']

print(f"\nOLS slope (size): {ols_slope:.4f}")
print(f"Bootstrap 95% CI: [{ci_lower:.4f}, {ci_upper:.4f}]")
print(f"Analytical 95% CI: [{fit_simple.confint().loc['size'].iloc[0]:.4f}, "
      f"{fit_simple.confint().loc['size'].iloc[1]:.4f}]")

fig, ax = plt.subplots(figsize=(10, 6))
ax.hist(boot_slopes, bins=40, edgecolor='black', alpha=0.7)
ax.axvline(ols_slope, color='red', linewidth=2, label=f'OLS estimate: {ols_slope:.4f}')
ax.axvline(ci_lower, color='green', linewidth=2, linestyle='--', label=f'2.5th pctl: {ci_lower:.4f}')
ax.axvline(ci_upper, color='green', linewidth=2, linestyle='--', label=f'97.5th pctl: {ci_upper:.4f}')
ax.set_xlabel('Bootstrap Slope Estimates')
ax.set_ylabel('Frequency')
ax.set_title('Bootstrap Distribution of Size Coefficient (1000 replications)')
ax.legend()
ax.grid(True, alpha=0.3)
plt.tight_layout()
plt.show()

```

---

## Chapter 13 Case Studies for Multiple Regression

```python
# =============================================================================
# CHAPTER 13 CHEAT SHEET: Case Studies for Multiple Regression
# =============================================================================

# --- Libraries ---
import numpy as np                        # numerical operations and log transforms
import pandas as pd                       # data loading and manipulation
import matplotlib.pyplot as plt           # creating plots and visualizations
import pyfixest as pf                     # OLS regression with R-style formulas
# !pip install pyfixest  # if not installed
from statsmodels.formula.api import ols as sm_ols  # for SSR-based F-tests and cluster SEs
from scipy import stats                   # F-distribution for hypothesis tests

# --- Data source ---
URL = "https://raw.githubusercontent.com/quarcs-lab/data-open/master/AED/"

# =============================================================================
# STEP 1: Cobb-Douglas Production Function — log-linearize and estimate
# =============================================================================
# Taking logs converts Q = A*K^alpha*L^beta into a linear model estimable by OLS
data_cobb = pd.read_stata(URL + "AED_COBBDOUGLAS.DTA")
data_cobb['lnq'] = np.log(data_cobb['q'])
data_cobb['lnk'] = np.log(data_cobb['k'])
data_cobb['lnl'] = np.log(data_cobb['l'])

# OLS with HAC standard errors (time series: autocorrelation + heteroskedasticity)
data_cobb['_time'] = range(len(data_cobb))
fit_cobb = pf.feols('lnq ~ lnk + lnl', data=data_cobb,
                    vcov='NW', vcov_kwargs={'time_id': '_time', 'lag': 3})

alpha = fit_cobb.coef()['lnk']    # capital elasticity
beta  = fit_cobb.coef()['lnl']    # labor elasticity

print(f"Capital elasticity α = {alpha:.3f}, Labor elasticity β = {beta:.3f}")
print(f"Sum α + β = {alpha + beta:.3f}  (≈1 → constant returns to scale)")
print(f"R² = {fit_cobb._r2:.4f}")
fit_cobb.summary()

# F-test for constant returns to scale: H0: α + β = 1
data_cobb['lnq_l'] = data_cobb['lnq'] - data_cobb['lnl']
data_cobb['lnk_l'] = data_cobb['lnk'] - data_cobb['lnl']
# Use statsmodels for SSR-based F-test
sm_cobb = sm_ols('lnq ~ lnk + lnl', data=data_cobb).fit()
sm_r = sm_ols('lnq_l ~ lnk_l', data=data_cobb).fit()
f_stat = ((sm_r.ssr - sm_cobb.ssr) / 1) / (sm_cobb.ssr / sm_cobb.df_resid)
p_val  = 1 - stats.f.cdf(f_stat, 1, sm_cobb.df_resid)
print(f"CRS test: F = {f_stat:.2f}, p = {p_val:.3f} → {'Fail to reject' if p_val > 0.05 else 'Reject'} CRS")

# =============================================================================
# STEP 2: Phillips Curve — omitted variables bias reverses the sign
# =============================================================================
# Pre-1970 the trade-off works; post-1970 it breaks because expected inflation
# is omitted — a textbook demonstration of OVB
data_phil = pd.read_stata(URL + "AED_PHILLIPS.DTA")

# Pre-1970: classic negative relationship
pre = data_phil[data_phil['year'] < 1970].copy()
pre['_time'] = range(len(pre))
fit_pre = pf.feols('inflgdp ~ urate', data=pre,
                   vcov='NW', vcov_kwargs={'time_id': '_time', 'lag': 3})
print(f"\nPre-1970 slope: {fit_pre.coef()['urate']:.3f}  (negative → classic Phillips curve)")

# Post-1970: sign flips due to omitted expected inflation
post = data_phil[data_phil['year'] >= 1970].copy()
post['_time'] = range(len(post))
fit_post = pf.feols('inflgdp ~ urate', data=post,
                    vcov='NW', vcov_kwargs={'time_id': '_time', 'lag': 5})
print(f"Post-1970 slope: {fit_post.coef()['urate']:.3f}  (positive → breakdown!)")

# Augmented model: adding expected inflation restores the negative sign
post_exp = post.dropna(subset=['inflgdp1yr']).copy()
post_exp['_time'] = range(len(post_exp))
fit_aug = pf.feols('inflgdp ~ urate + inflgdp1yr', data=post_exp,
                   vcov='NW', vcov_kwargs={'time_id': '_time', 'lag': 5})
print(f"Augmented slope on urate: {fit_aug.coef()['urate']:.3f}  (negative again!)")
print(f"Expected inflation coef:  {fit_aug.coef()['inflgdp1yr']:.3f}")

# OVB formula: E[b2] = β2 + β3*γ
fit_aux = pf.feols('inflgdp1yr ~ urate', data=post_exp)
predicted = fit_aug.coef()['urate'] + fit_aug.coef()['inflgdp1yr'] * fit_aux.coef()['urate']
print(f"OVB predicted bivariate slope: {predicted:.3f}  (actual: {fit_post.coef()['urate']:.3f})")

# =============================================================================
# STEP 3: RAND Health Insurance Experiment — RCT as the gold standard
# =============================================================================
# Random assignment to insurance plans eliminates selection bias
data_rand = pd.read_stata(URL + "AED_HEALTHINSEXP.DTA")
data_rand_y1 = data_rand[data_rand['year'] == 1]

# Mean spending by plan
print(f"\n{'Plan':<12} {'Mean $':>10} {'N':>8}")
for plan, grp in data_rand_y1.groupby('plan')['spending']:
    print(f"{plan:<12} {grp.mean():>10,.0f} {len(grp):>8,}")

# Regression with cluster-robust SEs by family
fit_rct = pf.feols('spending ~ coins25 + coins50 + coins95 + coinsmixed + coinsindiv',
                   data=data_rand_y1, vcov={'CRV1': 'idfamily'})
fit_rct.summary()

# Joint F-test: do insurance plans matter?
sm_rct = sm_ols('spending ~ coins25 + coins50 + coins95 + coinsmixed + coinsindiv',
                data=data_rand_y1).fit(
    cov_type='cluster', cov_kwds={'groups': data_rand_y1['idfamily']}
)
ftest = sm_rct.f_test('coins25 = coins50 = coins95 = coinsmixed = coinsindiv = 0')
print(f"Joint F-test: F = {ftest.fvalue:.2f}, p = {ftest.pvalue:.4f}")

# =============================================================================
# STEP 4: Difference-in-Differences — health clinic access in South Africa
# =============================================================================
# DiD removes both time-invariant confounders and common time trends
data_did = pd.read_stata(URL + "AED_HEALTHACCESS.DTA")

# Manual DiD calculation
pre_c  = data_did[(data_did['hightreat']==0) & (data_did['post']==0)]['waz'].mean()
post_c = data_did[(data_did['hightreat']==0) & (data_did['post']==1)]['waz'].mean()
pre_t  = data_did[(data_did['hightreat']==1) & (data_did['post']==0)]['waz'].mean()
post_t = data_did[(data_did['hightreat']==1) & (data_did['post']==1)]['waz'].mean()
did    = (post_t - pre_t) - (post_c - pre_c)
print(f"\nDiD estimate (manual): {did:.3f} SD improvement in child nutrition")

# DiD regression with cluster-robust SEs by community
fit_did = pf.feols('waz ~ hightreat + post + postXhigh', data=data_did,
                   vcov={'CRV1': 'idcommunity'})
print(f"DiD coefficient (regression): {fit_did.coef()['postXhigh']:.3f}")
print(f"p-value: {fit_did.pvalue()['postXhigh']:.4f}")

# =============================================================================
# STEP 5: Regression Discontinuity — incumbency advantage in U.S. Senate
# =============================================================================
# Candidates who barely win vs barely lose are quasi-randomly assigned to
# incumbent status — the jump at margin = 0 is the causal effect
data_rd = pd.read_stata(URL + "AED_INCUMBENCY.DTA")
data_rd = data_rd[data_rd['vote'].notna()].copy()

fit_rd = pf.feols('vote ~ win + margin', data=data_rd, vcov='HC1')
print(f"\nIncumbency advantage: {fit_rd.coef()['win']:.1f} percentage points")
print(f"95% CI: [{fit_rd.confint().loc['win'].iloc[0]:.1f}, {fit_rd.confint().loc['win'].iloc[1]:.1f}]")
print(f"p-value: {fit_rd.pvalue()['win']:.4f}")

# =============================================================================
# STEP 6: Instrumental Variables — do institutions cause growth?
# =============================================================================
# OLS is biased by reverse causation; settler mortality instruments for
# modern institutions (relevant + exogenous to modern GDP)
data_iv = pd.read_stata(URL + "AED_INSTITUTIONS.DTA")

# OLS (biased)
fit_ols_iv = pf.feols('logpgp95 ~ avexpr', data=data_iv, vcov='HC1')

# First stage: institutions ~ settler mortality
fit_1st = pf.feols('avexpr ~ logem4', data=data_iv, vcov='HC1')
sm_1st = sm_ols('avexpr ~ logem4', data=data_iv).fit(cov_type='HC1')
print(f"\nFirst-stage F = {sm_1st.fvalue:.1f}  ({'Strong' if sm_1st.fvalue > 10 else 'Weak'} instrument)")

# Second stage: GDP ~ predicted institutions
data_iv['avexpr_hat'] = fit_1st.predict()
fit_2nd = pf.feols('logpgp95 ~ avexpr_hat', data=data_iv, vcov='HC1')

print(f"OLS coefficient:  {fit_ols_iv.coef()['avexpr']:.3f}  (biased)")
print(f"IV/2SLS coefficient: {fit_2nd.coef()['avexpr_hat']:.3f}  (causal)")
print(f"Causal effect: 1-unit improvement in institutions → "
      f"{np.exp(fit_2nd.coef()['avexpr_hat']):.1f}x increase in GDP")

```

---

## Chapter 14 Regression with Indicator Variables

```python
# =============================================================================
# CHAPTER 14 CHEAT SHEET: Regression with Indicator Variables
# =============================================================================

# --- Libraries ---
import pandas as pd                       # data loading and manipulation
import numpy as np                        # numerical operations
import matplotlib.pyplot as plt           # creating plots and visualizations
import pyfixest as pf                     # OLS regression with R-style formulas
# !pip install pyfixest  # if not installed
from scipy import stats                   # t-tests for group comparisons
from scipy.stats import f_oneway          # one-way ANOVA F-test

# =============================================================================
# STEP 1: Load data directly from a URL
# =============================================================================
# pd.read_stata() reads Stata .dta files — 872 full-time workers aged 25-65
url = "https://raw.githubusercontent.com/quarcs-lab/data-open/master/AED/AED_EARNINGS_COMPLETE.DTA"
data = pd.read_stata(url)

print(f"Dataset: {data.shape[0]} observations, {data.shape[1]} variables")

# =============================================================================
# STEP 2: Descriptive statistics — compare earnings by gender
# =============================================================================
# Indicator variable: gender = 1 (female), gender = 0 (male)
mean_male   = data[data['gender'] == 0]['earnings'].mean()
mean_female = data[data['gender'] == 1]['earnings'].mean()
diff_means  = mean_female - mean_male

print(f"Mean earnings (Male):   ${mean_male:,.2f}")
print(f"Mean earnings (Female): ${mean_female:,.2f}")
print(f"Difference (F - M):     ${diff_means:,.2f}")

# =============================================================================
# STEP 3: Regression on a single indicator — equivalent to difference in means
# =============================================================================
# The intercept = mean for d=0 (males); the gender coefficient = mean difference
# IMPORTANT: vcov='HC1' uses robust standard errors
fit1 = pf.feols('earnings ~ gender', data=data, vcov='HC1')

intercept = fit1.coef()['Intercept']      # mean earnings for males
gap       = fit1.coef()['gender']         # earnings gap (females - males)
r2        = fit1._r2

print(f"\nModel 1: earnings = {intercept:,.0f} + ({gap:,.0f}) × gender")
print(f"Raw gender gap: ${gap:,.0f} (females earn ${abs(gap):,.0f} less)")
print(f"R-squared: {r2:.4f} ({r2*100:.1f}% of variation explained)")

fit1.summary()

# =============================================================================
# STEP 4: Add controls and interaction — how the gap changes
# =============================================================================
# Adding education as a control measures the gap AFTER accounting for education
fit2 = pf.feols('earnings ~ gender + education', data=data, vcov='HC1')

# Adding gender×education interaction allows returns to education to differ by gender
fit3 = pf.feols('earnings ~ gender + education + genderbyeduc', data=data, vcov='HC1')

# Full model with additional controls
fit4 = pf.feols('earnings ~ gender + education + genderbyeduc + age + hours',
                data=data, vcov='HC1')

# Compare how the gender coefficient evolves across models
print(f"{'Model':<12} {'Gender Coef':>14} {'R²':>8}")
print("-" * 36)
for name, m in [('Gender only', fit1), ('+ Education', fit2),
                ('+ Interact', fit3), ('+ Age,Hours', fit4)]:
    g = m.coef()['gender']
    print(f"{name:<12} {g:>14,.0f} {m._r2:>8.4f}")

# =============================================================================
# STEP 5: Scatter plot — visualize separate regression lines by gender
# =============================================================================
# Non-parallel lines indicate different slopes = interaction term is needed
fig, ax = plt.subplots(figsize=(10, 6))

for g, label, color in [(0, 'Male', 'tab:blue'), (1, 'Female', 'tab:red')]:
    subset = data[data['gender'] == g]
    ax.scatter(subset['education'], subset['earnings'], alpha=0.3, s=25,
               label=label, color=color)
    # Fit and plot regression line for each group
    z = np.polyfit(subset['education'], subset['earnings'], 1)
    edu_range = np.linspace(subset['education'].min(), subset['education'].max(), 100)
    ax.plot(edu_range, np.poly1d(z)(edu_range), linewidth=2, color=color,
            label=f'{label} slope: ${z[0]:,.0f}/yr')

ax.set_xlabel('Years of Education')
ax.set_ylabel('Earnings ($)')
ax.set_title('Earnings vs Education by Gender (non-parallel = interaction needed)')
ax.legend()
ax.grid(True, alpha=0.3)
plt.tight_layout()
plt.show()

# =============================================================================
# STEP 6: Sets of indicators — worker type and the dummy variable trap
# =============================================================================
# Three mutually exclusive categories: dself, dprivate, dgovt (sum to 1)
# Drop one (dprivate = base) to avoid perfect multicollinearity
fit_worker = pf.feols('earnings ~ dself + dgovt + education + age',
                      data=data, vcov='HC1')

print(f"Base category: Private sector")
print(f"Self-employed vs Private: ${fit_worker.coef()['dself']:,.0f}")
print(f"Government vs Private:   ${fit_worker.coef()['dgovt']:,.0f}")
print(f"R-squared: {fit_worker._r2:.4f}")

fit_worker.summary()

# =============================================================================
# STEP 7: ANOVA — test if earnings differ across worker types
# =============================================================================
# Regression on mutually exclusive indicators = analysis of variance (ANOVA)
group_self = data[data['dself'] == 1]['earnings']
group_priv = data[data['dprivate'] == 1]['earnings']
group_govt = data[data['dgovt'] == 1]['earnings']

f_stat, p_value = f_oneway(group_self, group_priv, group_govt)
print(f"\nANOVA F-statistic: {f_stat:.2f}, p-value: {p_value:.4f}")

# Group means with counts
data['worker_type'] = np.where(data['dself'] == 1, 'Self-employed',
                      np.where(data['dprivate'] == 1, 'Private', 'Government'))
print(data.groupby('worker_type')['earnings'].agg(['mean', 'count']).round(0))

```

---

## Chapter 15 Regression with Transformed Variables

```python
# =============================================================================
# CHAPTER 15 CHEAT SHEET: Regression with Transformed Variables
# =============================================================================

# --- Libraries ---
import numpy as np                        # numerical operations (log, exp, sqrt)
import pandas as pd                       # data loading and manipulation
import matplotlib.pyplot as plt           # creating plots and visualizations
import pyfixest as pf                     # OLS regression with R-style formulas
# !pip install pyfixest  # if not installed
from statsmodels.formula.api import ols as sm_ols  # for Wald test

# =============================================================================
# STEP 1: Load data directly from a URL
# =============================================================================
# 872 full-time workers aged 25-65 with earnings, education, age, and hours
url = "https://raw.githubusercontent.com/quarcs-lab/data-open/master/AED/AED_EARNINGS_COMPLETE.DTA"
data_earnings = pd.read_stata(url)

# Create log and squared variables for transformations
data_earnings['lnage'] = np.log(data_earnings['age'])

print(f"Dataset: {data_earnings.shape[0]} observations, {data_earnings.shape[1]} variables")
print(data_earnings[['earnings', 'lnearnings', 'age', 'education']].describe().round(2))

# =============================================================================
# STEP 2: Log transformations — levels vs log-linear vs log-log
# =============================================================================
# Three specifications of the same relationship reveal different stories
fit_levels = pf.feols('earnings ~ age + education', data=data_earnings, vcov='HC1')
fit_loglin = pf.feols('lnearnings ~ age + education', data=data_earnings, vcov='HC1')
fit_loglog = pf.feols('lnearnings ~ lnage + education', data=data_earnings, vcov='HC1')

print("=== Levels: absolute dollar effects ===")
print(f"  Education: +${fit_levels.coef()['education']:,.0f} per year")

print("\n=== Log-Linear: semi-elasticity (% change per unit) ===")
print(f"  Education: +{100*fit_loglin.coef()['education']:.1f}% per year (Mincer return)")

print("\n=== Log-Log: elasticity (% change per % change) ===")
print(f"  Age elasticity: {fit_loglog.coef()['lnage']:.4f}")

# =============================================================================
# STEP 3: Quadratic model — turning point and varying marginal effects
# =============================================================================
# A quadratic in age captures the inverted-U life-cycle earnings profile
fit_quad = pf.feols('earnings ~ age + agesq + education', data=data_earnings, vcov='HC1')

bage    = fit_quad.coef()['age']
bagesq  = fit_quad.coef()['agesq']
turning_point = -bage / (2 * bagesq)        # age where earnings peak

print(f"Turning point: {turning_point:.1f} years")
for a in [25, 40, 55]:
    me = bage + 2 * bagesq * a              # ME varies with age
    print(f"  ME at age {a}: ${me:,.0f}/year")

# Joint F-test: H0: age and age² are jointly zero
sm_quad = sm_ols('earnings ~ age + agesq + education', data=data_earnings).fit(cov_type='HC1')
f_test = sm_quad.wald_test('(age = 0, agesq = 0)', use_f=True)
print(f"Joint F-test p-value: {f_test.pvalue:.4f}")

# =============================================================================
# STEP 4: Standardized coefficients — compare variable importance
# =============================================================================
# Raw coefficients can't be compared across different units; beta* can
fit_mix = pf.feols('earnings ~ gender + age + agesq + education + dself + dgovt + lnhours',
                   data=data_earnings, vcov='HC1')

sd_y = data_earnings['earnings'].std()
predictors = ['gender', 'age', 'agesq', 'education', 'dself', 'dgovt', 'lnhours']

print(f"\n{'Variable':<12} {'Raw coef':>12} {'Beta*':>8}")
print("-" * 34)
for var in sorted(predictors, key=lambda v: abs(fit_mix.coef()[v] * data_earnings[v].std() / sd_y), reverse=True):
    raw  = fit_mix.coef()[var]
    beta_star = raw * data_earnings[var].std() / sd_y
    print(f"{var:<12} {raw:>12.2f} {beta_star:>8.4f}")

# =============================================================================
# STEP 5: Interaction terms — education returns that vary with age
# =============================================================================
# Does one more year of schooling pay the same at 25 as at 55?
fit_inter = pf.feols('earnings ~ age + education + agebyeduc', data=data_earnings, vcov='HC1')

b_educ  = fit_inter.coef()['education']
b_inter = fit_inter.coef()['agebyeduc']

print(f"\nME of education = {b_educ:,.0f} + {b_inter:.1f} × age")
for a in [25, 40, 55]:
    me = b_educ + b_inter * a               # ME depends on age
    print(f"  At age {a}: ${me:,.0f} per year of education")

# =============================================================================
# STEP 6: Retransformation bias — naive exp() underpredicts
# =============================================================================
# Jensen's inequality: E[exp(u)] > exp(E[u]), so naive predictions are biased
rmse_log = np.sqrt(np.mean(fit_loglin._u_hat**2))
correction = np.exp(rmse_log**2 / 2)        # normal-based smearing factor

naive_pred    = np.exp(fit_loglin.predict())
adjusted_pred = correction * naive_pred

print(f"\nSmearing factor: {correction:.4f}")
print(f"Actual mean:     ${data_earnings['earnings'].mean():,.0f}")
print(f"Naive mean:      ${naive_pred.mean():,.0f}  (underpredicts)")
print(f"Corrected mean:  ${adjusted_pred.mean():,.0f}  (bias removed)")

# =============================================================================
# STEP 7: Comprehensive model — combine all transformation types
# =============================================================================
# A single model mixing logs, quadratics, dummies, and continuous regressors
fit_full = pf.feols('lnearnings ~ gender + age + agesq + education + dself + dgovt + lnhours',
                    data=data_earnings, vcov='HC1')

print(f"\nR²: {fit_full._r2:.4f}")
print(f"Education return: ~{100*fit_full.coef()['education']:.1f}% per year (semi-elasticity)")
print(f"Gender gap: ~{100*fit_full.coef()['gender']:.1f}%")
print(f"Hours elasticity: {fit_full.coef()['lnhours']:.3f} (log-log coefficient)")

# Full regression table
fit_full.summary()

```

---

## Chapter 16 Checking the Model and Data

```python
# =============================================================================
# CHAPTER 16 CHEAT SHEET: Checking the Model and Data
# =============================================================================

# --- Libraries ---
import numpy as np                                          # numerical operations
import pandas as pd                                         # data loading and manipulation
import matplotlib.pyplot as plt                             # creating plots and visualizations
import pyfixest as pf                                       # OLS regression with R-style formulas
# !pip install pyfixest  # if not installed
import statsmodels.api as sm                                # add_constant for VIF calculation
from statsmodels.formula.api import ols as sm_ols           # for OLSInfluence diagnostics
from statsmodels.stats.outliers_influence import (          # diagnostic tools:
    variance_inflation_factor, OLSInfluence)                #   VIF and influence measures
from statsmodels.nonparametric.smoothers_lowess import lowess  # LOWESS smooth for residual plots

# =============================================================================
# STEP 1: Load data
# =============================================================================
# Two datasets: earnings (cross-section) and democracy (cross-country)
url_base = "https://raw.githubusercontent.com/quarcs-lab/data-open/master/AED/"

data_earnings  = pd.read_stata(url_base + "AED_EARNINGS_COMPLETE.DTA")
data_democracy = pd.read_stata(url_base + "AED_DEMOCRACY.DTA")

print(f"Earnings:  {data_earnings.shape[0]} workers, {data_earnings.shape[1]} variables")
print(f"Democracy: {data_democracy.shape[0]} countries, {data_democracy.shape[1]} variables")

# =============================================================================
# STEP 2: Detect multicollinearity with VIF
# =============================================================================
# VIF_j = 1/(1 - R_j^2): measures how much SE inflates due to collinearity
# VIF > 10 = serious problem; VIF > 5 = investigate further

X_vif = data_earnings[['age', 'education', 'agebyeduc']].copy()
X_vif = sm.add_constant(X_vif)

vif_data = pd.DataFrame({
    'Variable': X_vif.columns,
    'VIF': [variance_inflation_factor(X_vif.values, i) for i in range(X_vif.shape[1])]
})
print("\nVariance Inflation Factors (with interaction term):")
print(vif_data.to_string(index=False))

# =============================================================================
# STEP 3: Compare standard vs robust standard errors
# =============================================================================
# Heteroskedasticity makes default SEs too small -> use HC1 (White) robust SEs
fit_std    = pf.feols('earnings ~ age + education', data=data_earnings)
fit_robust = pf.feols('earnings ~ age + education', data=data_earnings, vcov='HC1')

se_comparison = pd.DataFrame({
    'Variable':    fit_std.coef().index,
    'Standard SE': fit_std.se().values.round(2),
    'Robust SE':   fit_robust.se().values.round(2),
    'Ratio':       (fit_robust.se() / fit_std.se()).values.round(3)
})
print("\nSE Comparison (ratio > 1 signals heteroskedasticity):")
print(se_comparison.to_string(index=False))

# =============================================================================
# STEP 4: Omitted variable bias — democracy and growth
# =============================================================================
# Adding controls reveals how much the bivariate estimate was biased upward
fit_bivariate = pf.feols('democracy ~ growth', data=data_democracy, vcov='HC1')
fit_multiple  = pf.feols('democracy ~ growth + constraint + indcent + catholic + muslim + protestant',
                         data=data_democracy, vcov='HC1')

b_biv  = fit_bivariate.coef()['growth']
b_mult = fit_multiple.coef()['growth']
print(f"\nGrowth coefficient (bivariate):       {b_biv:.4f}")
print(f"Growth coefficient (with controls):   {b_mult:.4f}")
print(f"Reduction: {(1 - b_mult/b_biv)*100:.0f}% — institutional controls absorb the bias")

# =============================================================================
# STEP 5: Diagnostic plots — residual vs fitted
# =============================================================================
# Random scatter around zero = assumptions OK; fan shape = heteroskedasticity
uhat = fit_multiple._u_hat
yhat = fit_multiple.predict()

fig, axes = plt.subplots(1, 2, figsize=(14, 5))

# Panel A: Actual vs Fitted
axes[0].scatter(yhat, data_democracy['democracy'], s=50, alpha=0.6)
axes[0].plot([yhat.min(), yhat.max()], [yhat.min(), yhat.max()],
             'r-', linewidth=2, label='45° line')
axes[0].set_xlabel('Fitted Democracy')
axes[0].set_ylabel('Actual Democracy')
axes[0].set_title('Actual vs Fitted')
axes[0].legend()
axes[0].grid(True, alpha=0.3)

# Panel B: Residual vs Fitted (with LOWESS smooth)
axes[1].scatter(yhat, uhat, s=50, alpha=0.6)
axes[1].axhline(y=0, color='gray', linewidth=1)
lw = lowess(uhat, yhat, frac=0.3)          # LOWESS reveals hidden patterns
axes[1].plot(lw[:, 0], lw[:, 1], 'r--', linewidth=2, label='LOWESS smooth')
axes[1].set_xlabel('Fitted Democracy')
axes[1].set_ylabel('Residual')
axes[1].set_title('Residual vs Fitted')
axes[1].legend()
axes[1].grid(True, alpha=0.3)

plt.tight_layout()
plt.show()

# =============================================================================
# STEP 6: Influential observations — DFITS
# =============================================================================
# DFITS_i measures how much prediction i changes when observation i is excluded
# Threshold: |DFITS| > 2*sqrt(k/n)
# OLSInfluence requires statsmodels model object
sm_multiple = sm_ols('democracy ~ growth + constraint + indcent + catholic + muslim + protestant',
                     data=data_democracy).fit(cov_type='HC1')
influence = OLSInfluence(sm_multiple)
dfits     = influence.dffits[0]
n = len(data_democracy)
k = len(fit_multiple.coef())
threshold = 2 * np.sqrt(k / n)

print(f"\nDFITS threshold: {threshold:.4f}")
print(f"Observations exceeding threshold: {np.sum(np.abs(dfits) > threshold)} out of {n}")

fig, ax = plt.subplots(figsize=(10, 6))
colors = ['red' if abs(d) > threshold else 'steelblue' for d in dfits]
ax.scatter(range(n), dfits, c=colors, s=40, alpha=0.7)
ax.axhline(y=threshold,  color='red', linestyle='--', label=f'Threshold ±{threshold:.3f}')
ax.axhline(y=-threshold, color='red', linestyle='--')
ax.axhline(y=0, color='gray', linewidth=0.5)
ax.set_xlabel('Observation Index')
ax.set_ylabel('DFITS')
ax.set_title('Influential Observations (DFITS)')
ax.legend()
ax.grid(True, alpha=0.3)
plt.tight_layout()
plt.show()

```

---

## Chapter 17 Panel Data Time Series Data Causation

```python
# =============================================================================
# CHAPTER 17 CHEAT SHEET: Panel Data, Time Series Data, Causation
# =============================================================================

# --- Libraries ---
import pandas as pd                       # data loading and manipulation
import numpy as np                         # numerical operations
import matplotlib.pyplot as plt            # creating plots and visualizations
import pyfixest as pf                      # OLS and FE regression with R-style formulas
# !pip install pyfixest  # if not installed
from statsmodels.tsa.stattools import acf  # autocorrelation function

# =============================================================================
# STEP 1: Load panel data (NBA teams across seasons)
# =============================================================================
# Panel data: multiple individuals (teams) observed over multiple time periods
url_nba = "https://raw.githubusercontent.com/quarcs-lab/data-open/master/AED/AED_NBA.DTA"
data_nba = pd.read_stata(url_nba)

print(f"Panel: {data_nba['teamid'].nunique()} teams × {data_nba['season'].nunique()} seasons = {len(data_nba)} obs")

# =============================================================================
# STEP 2: Variance decomposition — between vs within variation
# =============================================================================
# Understanding which variation your estimator uses is the first step in panel analysis
overall_sd = data_nba['lnrevenue'].std()
between_sd = data_nba.groupby('teamid')['lnrevenue'].mean().std()
within_sd  = data_nba.groupby('teamid')['lnrevenue'].apply(lambda x: x - x.mean()).std()

print(f"\nVariance Decomposition of Log Revenue:")
print(f"  Overall SD:  {overall_sd:.4f}")
print(f"  Between SD:  {between_sd:.4f} (across teams)")
print(f"  Within SD:   {within_sd:.4f} (over time)")
print(f"  Between > Within → team characteristics dominate year-to-year swings")

# =============================================================================
# STEP 3: Pooled OLS with cluster-robust SEs
# =============================================================================
# Observations within the same team are correlated over time — default SEs
# dramatically understate uncertainty. Always cluster by individual in panel data.
fit_pool = pf.feols('lnrevenue ~ wins', data=data_nba)
fit_cluster = pf.feols('lnrevenue ~ wins', data=data_nba, vcov={'CRV1': 'teamid'})

print(f"\nPooled OLS — wins coefficient: {fit_pool.coef()['wins']:.6f}")
print(f"  Default SE:  {fit_pool.se()['wins']:.6f}")
print(f"  Cluster SE:  {fit_cluster.se()['wins']:.6f}")
print(f"  Ratio:       {fit_cluster.se()['wins'] / fit_pool.se()['wins']:.2f}x larger")

# =============================================================================
# STEP 4: Fixed effects — control for unobserved team characteristics
# =============================================================================
# FE uses only within-team variation (de-meaning), eliminating bias from
# persistent traits like market size, brand value, and arena quality.
fit_fe = pf.feols('lnrevenue ~ wins | teamid', data=data_nba, vcov={'CRV1': 'teamid'})

print(f"\nFixed Effects — wins coefficient: {fit_fe.coef()['wins']:.6f}")
print(f"  Cluster SE:  {fit_fe.se()['wins']:.6f}")
print(f"  R² (within): {fit_fe._r2_within:.4f}")

print(f"\nComparison:")
print(f"  Pooled OLS coef: {fit_pool.coef()['wins']:.6f}")
print(f"  Fixed Effects:   {fit_fe.coef()['wins']:.6f}")
print(f"  FE is smaller → pooled OLS had positive omitted variable bias")

# =============================================================================
# STEP 5: Time series — levels vs first differences
# =============================================================================
# Non-stationary (trending) series produce spurious regressions with misleading R².
# First differencing removes trends and restores valid inference.
url_rates = "https://raw.githubusercontent.com/quarcs-lab/data-open/master/AED/AED_INTERESTRATES.DTA"
data_rates = pd.read_stata(url_rates)

# Regression in levels (potentially spurious)
fit_levels = pf.feols('gs10 ~ gs1', data=data_rates)

# Regression in first differences (removes trends)
fit_changes = pf.feols('dgs10 ~ dgs1', data=data_rates)

print(f"\nLevels regression:  gs1 coef = {fit_levels.coef()['gs1']:.4f}, R² = {fit_levels._r2:.4f}")
print(f"Changes regression: dgs1 coef = {fit_changes.coef()['dgs1']:.4f}, R² = {fit_changes._r2:.4f}")
print(f"R² drops after differencing — lower but honest (no spurious trend inflation)")

# =============================================================================
# STEP 6: Autocorrelation diagnostics — the smoking gun
# =============================================================================
# Slowly decaying ACF in residuals signals non-stationarity and invalid SEs.
# After differencing, autocorrelation should drop dramatically.
acf_levels  = acf(pd.Series(fit_levels._u_hat).dropna(), nlags=5)
acf_changes = acf(pd.Series(fit_changes._u_hat).dropna(), nlags=5)

print(f"\nResidual autocorrelation (lag 1):")
print(f"  Levels regression:  {acf_levels[1]:.4f} (high → non-stationary residuals)")
print(f"  Changes regression: {acf_changes[1]:.4f} (much lower → differencing worked)")

# HAC (Newey-West) SEs correct for autocorrelation without differencing
fit_hac = pf.feols('gs10 ~ gs1', data=data_rates,
                   vcov='NW', vcov_kwargs={'time_id': 'time', 'lag': 24})
print(f"\nDefault SE on gs1:   {fit_levels.se()['gs1']:.4f}")
print(f"HAC SE on gs1:       {fit_hac.se()['gs1']:.4f}")
print(f"HAC is {fit_hac.se()['gs1'] / fit_levels.se()['gs1']:.1f}x larger — default SEs are too small")

# =============================================================================
# STEP 7: ADL model — dynamic multipliers
# =============================================================================
# Autoregressive distributed lag models capture how effects build over time.
# Lagged dependent and independent variables model persistence and transmission.
data_rates['dgs10_lag1'] = data_rates['dgs10'].shift(1)
data_rates['dgs10_lag2'] = data_rates['dgs10'].shift(2)
data_rates['dgs1_lag1']  = data_rates['dgs1'].shift(1)
data_rates['dgs1_lag2']  = data_rates['dgs1'].shift(2)

fit_adl = pf.feols('dgs10 ~ dgs10_lag1 + dgs10_lag2 + dgs1 + dgs1_lag1 + dgs1_lag2',
                   data=data_rates)

print(f"\nADL(2,2) Model:")
print(f"  Impact multiplier (dgs1):       {fit_adl.coef()['dgs1']:.4f}")
print(f"  1-month cumulative:             {fit_adl.coef()['dgs1'] + fit_adl.coef()['dgs1_lag1']:.4f}")
print(f"  2-month cumulative:             {fit_adl.coef()['dgs1'] + fit_adl.coef()['dgs1_lag1'] + fit_adl.coef()['dgs1_lag2']:.4f}")
print(f"  R²: {fit_adl._r2:.4f} (much higher than static model)")

# Check residual autocorrelation — should be near zero if well-specified
acf_adl = acf(pd.Series(fit_adl._u_hat).dropna(), nlags=5)
print(f"  Residual ACF(1): {acf_adl[1]:.4f} (near zero → dynamics captured)")

```

