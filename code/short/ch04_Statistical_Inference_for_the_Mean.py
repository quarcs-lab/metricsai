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
