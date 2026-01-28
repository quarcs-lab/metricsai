"""
ch04_Statistical_Inference_for_the_Mean.py - January 2026 for Python

Chapter 4: STATISTICAL INFERENCE FOR THE MEAN

To run you need files:
  AED_EARNINGS.DTA
  AED_GASPRICE.DTA
  AED_EARNINGSMALE.DTA
  AED_REALGDPPC.DTA
in the data_stata/ directory

Sections covered:
  4.1 EXAMPLE: MEAN ANNUAL EARNINGS
  4.2 t STATISTIC AND t DISTRIBUTION
  4.3 CONFIDENCE INTERVALS
  4.4 TWO-SIDED HYPOTHESIS TESTS
  4.5 TWO-SIDED HYPOTHESIS TEST EXAMPLES
  4.6 ONE-SIDED DIRECTIONAL HYPOTHESIS TESTS
  4.7 GENERALIZATIONS OF CONFIDENCE INTERVALS AND HYPOTHESIS TESTS
  4.8 PROPORTIONS DATA
"""

# ========== SETUP ==========

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
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

# Output directories (optional - for saving figures and tables locally)
IMAGES_DIR = 'images'
TABLES_DIR = 'tables'
os.makedirs(IMAGES_DIR, exist_ok=True)
os.makedirs(TABLES_DIR, exist_ok=True)

# Set plotting style
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (10, 6)

print("=" * 70)
print("CHAPTER 4: STATISTICAL INFERENCE FOR THE MEAN")
print("=" * 70)

# ========== 4.1 EXAMPLE: MEAN ANNUAL EARNINGS ==========

print("\n" + "=" * 70)
print("4.1 EXAMPLE: MEAN ANNUAL EARNINGS")
print("=" * 70)

# Read in earnings data
data_earnings = pd.read_stata(GITHUB_DATA_URL + 'AED_EARNINGS.DTA')

print("\nData summary:")
data_summary = data_earnings.describe()
print(data_summary)
data_summary.to_csv(os.path.join(TABLES_DIR, 'ch04_earnings_descriptive_stats.csv'))
print(f"Table saved to: {os.path.join(TABLES_DIR, 'ch04_earnings_descriptive_stats.csv')}")

earnings = data_earnings['earnings']

# Summary statistics
mean_earnings = earnings.mean()
std_earnings = earnings.std(ddof=1)
n = len(earnings)
se_earnings = std_earnings / np.sqrt(n)

print(f"\n{'='*50}")
print(f"Sample Statistics:")
print(f"{'='*50}")
print(f"Sample size (n):        {n}")
print(f"Mean:                   ${mean_earnings:,.2f}")
print(f"Standard deviation:     ${std_earnings:,.2f}")
print(f"Standard error:         ${se_earnings:,.2f}")

# 95% Confidence interval
conf_level = 0.95
alpha = 1 - conf_level
t_crit = stats.t.ppf(1 - alpha/2, n - 1)
ci_lower = mean_earnings - t_crit * se_earnings
ci_upper = mean_earnings + t_crit * se_earnings

print(f"\n95% Confidence Interval:")
print(f"  [{ci_lower:,.2f}, {ci_upper:,.2f}]")

# Save confidence interval
ci_df = pd.DataFrame({
    'Statistic': ['Mean', 'Std Dev', 'Std Error', 'CI Lower (95%)', 'CI Upper (95%)'],
    'Value': [mean_earnings, std_earnings, se_earnings, ci_lower, ci_upper]
})
ci_df.to_csv(os.path.join(TABLES_DIR, 'ch04_confidence_interval.csv'), index=False)
print(f"Table saved to: {os.path.join(TABLES_DIR, 'ch04_confidence_interval.csv')}")

# Hypothesis test: H0: μ = 40000
mu0 = 40000
t_stat = (mean_earnings - mu0) / se_earnings
p_value = 2 * (1 - stats.t.cdf(abs(t_stat), n - 1))

print(f"\nHypothesis Test: H0: μ = ${mu0:,}")
print(f"  t-statistic:  {t_stat:.4f}")
print(f"  p-value:      {p_value:.4f}")
print(f"  Decision:     {'Reject H0' if p_value < 0.05 else 'Fail to reject H0'} at α=0.05")

# ========== 4.2 t STATISTIC AND t DISTRIBUTION ==========

print("\n" + "=" * 70)
print("4.2 t STATISTIC AND t DISTRIBUTION")
print("=" * 70)

# Figure 4.1: Comparison of t and normal distributions
fig, axes = plt.subplots(1, 2, figsize=(16, 6))

x = np.linspace(-4, 4, 200)

# Panel A: t(4) vs standard normal
axes[0].plot(x, stats.norm.pdf(x), 'b--', linewidth=2, label='Standard Normal')
axes[0].plot(x, stats.t.pdf(x, df=4), 'r-', linewidth=2, label='t(4)')
axes[0].set_xlabel('x value', fontsize=12)
axes[0].set_ylabel('Density', fontsize=12)
# axes[0].set_title('Panel A: t(4)  # Removed: redundant with LaTeX caption and Standard Normal', fontsize=13, fontweight='bold')  # Removed: redundant with LaTeX caption
# axes[0].legend()  # Removed: redundant with LaTeX caption
axes[0].grid(True, alpha=0.3)

# Panel B: t(30) vs standard normal
axes[1].plot(x, stats.norm.pdf(x), 'b--', linewidth=2, label='Standard Normal')
axes[1].plot(x, stats.t.pdf(x, df=30), 'r-', linewidth=2, label='t(30)')
axes[1].set_xlabel('x value', fontsize=12)
axes[1].set_ylabel('Density', fontsize=12)
# axes[1].set_title('Panel B: t(30)  # Removed: redundant with LaTeX caption and Standard Normal', fontsize=13, fontweight='bold')  # Removed: redundant with LaTeX caption
# axes[1].legend()  # Removed: redundant with LaTeX caption
axes[1].grid(True, alpha=0.3)

# plt.suptitle('Figure 4.1: t Distribution vs Standard Normal',
#              fontsize=14, fontweight='bold', y=1.0)  # Removed: redundant with LaTeX caption  # Removed: redundant with LaTeX caption
output_file = os.path.join(IMAGES_DIR, 'ch04_fig1_t_vs_normal_distributions.png')
plt.tight_layout()
plt.savefig(output_file, dpi=300, bbox_inches='tight')
print(f"\nFigure 4.1 saved to: {output_file}")
plt.close()

# ========== 4.3 CONFIDENCE INTERVALS ==========

print("\n" + "=" * 70)
print("4.3 CONFIDENCE INTERVALS")
print("=" * 70)

# Different confidence levels
conf_levels = [0.90, 0.95, 0.99]

print(f"\nConfidence Intervals for Mean Earnings:")
print(f"{'Level':<10} {'Lower Bound':>15} {'Upper Bound':>15} {'Width':>15}")
print("-" * 60)

for conf in conf_levels:
    alpha = 1 - conf
    t_crit = stats.t.ppf(1 - alpha/2, n - 1)
    ci_lower = mean_earnings - t_crit * se_earnings
    ci_upper = mean_earnings + t_crit * se_earnings
    width = ci_upper - ci_lower
    print(f"{conf*100:.0f}%{ci_lower:>18,.2f}{ci_upper:>18,.2f}{width:>18,.2f}")

# Manual calculation for 95% CI (demonstration)
print(f"\nManual Calculation (95% CI):")
print(f"  Mean:              ${mean_earnings:,.2f}")
print(f"  Std Error:         ${se_earnings:,.2f}")
print(f"  Critical value:     {t_crit:.4f}")
print(f"  Margin of error:   ${t_crit * se_earnings:,.2f}")
print(f"  CI:                [${ci_lower:,.2f}, ${ci_upper:,.2f}]")

# ========== 4.4 TWO-SIDED HYPOTHESIS TESTS ==========

print("\n" + "=" * 70)
print("4.4 TWO-SIDED HYPOTHESIS TESTS")
print("=" * 70)

# Test H0: μ = 40000 vs HA: μ ≠ 40000
mu0 = 40000
t_stat = (mean_earnings - mu0) / se_earnings
p_value = 2 * (1 - stats.t.cdf(abs(t_stat), n - 1))
t_crit_95 = stats.t.ppf(0.975, n - 1)

print(f"\nTwo-Sided Test: H0: μ = ${mu0:,} vs HA: μ ≠ ${mu0:,}")
print(f"  Sample mean:      ${mean_earnings:,.2f}")
print(f"  t-statistic:       {t_stat:.4f}")
print(f"  p-value:           {p_value:.4f}")
print(f"  Critical value:    ±{t_crit_95:.4f}")
print(f"  Decision:          {'Reject H0' if abs(t_stat) > t_crit_95 else 'Fail to reject H0'}")

# ========== 4.5 TWO-SIDED HYPOTHESIS TEST EXAMPLES ==========

print("\n" + "=" * 70)
print("4.5 TWO-SIDED HYPOTHESIS TEST EXAMPLES")
print("=" * 70)

# Example 1: Gasoline prices
print("\nExample 1: Gasoline Prices")
print("-" * 50)

data_gasprice = pd.read_stata(GITHUB_DATA_URL + 'AED_GASPRICE.DTA')
price = data_gasprice['price']

mean_price = price.mean()
std_price = price.std(ddof=1)
n_price = len(price)
se_price = std_price / np.sqrt(n_price)

mu0_price = 3.81
t_stat_price = (mean_price - mu0_price) / se_price
p_value_price = 2 * (1 - stats.t.cdf(abs(t_stat_price), n_price - 1))
t_crit_price = stats.t.ppf(0.975, n_price - 1)

print(f"H0: μ = ${mu0_price:.2f}")
print(f"  Sample size:       {n_price}")
print(f"  Sample mean:      ${mean_price:.4f}")
print(f"  Std error:        ${se_price:.4f}")
print(f"  t-statistic:       {t_stat_price:.4f}")
print(f"  p-value:           {p_value_price:.4f}")
print(f"  Critical value:    ±{t_crit_price:.4f}")

# Example 2: Male earnings
print("\nExample 2: Male Earnings")
print("-" * 50)

data_male = pd.read_stata(GITHUB_DATA_URL + 'AED_EARNINGSMALE.DTA')
earnings_male = data_male['earnings']

mean_male = earnings_male.mean()
std_male = earnings_male.std(ddof=1)
n_male = len(earnings_male)
se_male = std_male / np.sqrt(n_male)

mu0_male = 50000
t_stat_male = (mean_male - mu0_male) / se_male
p_value_male = 2 * (1 - stats.t.cdf(abs(t_stat_male), n_male - 1))
t_crit_male = stats.t.ppf(0.975, n_male - 1)

print(f"H0: μ = ${mu0_male:,}")
print(f"  Sample size:       {n_male}")
print(f"  Sample mean:      ${mean_male:,.2f}")
print(f"  Std error:        ${se_male:,.2f}")
print(f"  t-statistic:       {t_stat_male:.4f}")
print(f"  p-value:           {p_value_male:.4f}")
print(f"  Critical value:    ±{t_crit_male:.4f}")

# Example 3: GDP growth
print("\nExample 3: Real GDP per Capita Growth")
print("-" * 50)

data_gdp = pd.read_stata(GITHUB_DATA_URL + 'AED_REALGDPPC.DTA')
growth = data_gdp['growth']

mean_growth = growth.mean()
std_growth = growth.std(ddof=1)
n_growth = len(growth)
se_growth = std_growth / np.sqrt(n_growth)

mu0_growth = 2.0
t_stat_growth = (mean_growth - mu0_growth) / se_growth
p_value_growth = 2 * (1 - stats.t.cdf(abs(t_stat_growth), n_growth - 1))
t_crit_growth = stats.t.ppf(0.975, n_growth - 1)

print(f"H0: μ = {mu0_growth:.1f}%")
print(f"  Sample size:       {n_growth}")
print(f"  Sample mean:       {mean_growth:.4f}%")
print(f"  Std error:         {se_growth:.4f}%")
print(f"  t-statistic:       {t_stat_growth:.4f}")
print(f"  p-value:           {p_value_growth:.4f}")
print(f"  Critical value:    ±{t_crit_growth:.4f}")

# ========== 4.6 ONE-SIDED DIRECTIONAL HYPOTHESIS TESTS ==========

print("\n" + "=" * 70)
print("4.6 ONE-SIDED DIRECTIONAL HYPOTHESIS TESTS")
print("=" * 70)

# Test H0: μ ≥ 40000 vs HA: μ < 40000
mu0 = 40000
t_stat = (mean_earnings - mu0) / se_earnings
p_value_one_sided = stats.t.cdf(t_stat, n - 1)
t_crit_one_sided = stats.t.ppf(0.05, n - 1)

print(f"\nOne-Sided Test (Lower-tailed): H0: μ ≥ ${mu0:,} vs HA: μ < ${mu0:,}")
print(f"  t-statistic:       {t_stat:.4f}")
print(f"  p-value:           {p_value_one_sided:.4f}")
print(f"  Critical value:    {t_crit_one_sided:.4f}")
print(f"  Decision:          {'Reject H0' if t_stat < t_crit_one_sided else 'Fail to reject H0'}")

# Test H0: μ ≤ 40000 vs HA: μ > 40000
p_value_upper = 1 - stats.t.cdf(t_stat, n - 1)
t_crit_upper = stats.t.ppf(0.95, n - 1)

print(f"\nOne-Sided Test (Upper-tailed): H0: μ ≤ ${mu0:,} vs HA: μ > ${mu0:,}")
print(f"  t-statistic:       {t_stat:.4f}")
print(f"  p-value:           {p_value_upper:.4f}")
print(f"  Critical value:    {t_crit_upper:.4f}")
print(f"  Decision:          {'Reject H0' if t_stat > t_crit_upper else 'Fail to reject H0'}")

# ========== 4.8 PROPORTIONS DATA ==========

print("\n" + "=" * 70)
print("4.8 PROPORTIONS DATA")
print("=" * 70)

# Example: proportion data
n_total = 921
n_success = 480
p_hat = n_success / n_total
se_prop = np.sqrt(p_hat * (1 - p_hat) / n_total)

# Confidence interval
z_crit = 1.96  # For 95% CI
ci_lower_prop = p_hat - z_crit * se_prop
ci_upper_prop = p_hat + z_crit * se_prop

print(f"\nProportion Analysis:")
print(f"  Sample size:       {n_total}")
print(f"  Number of successes: {n_success}")
print(f"  Sample proportion: {p_hat:.4f}")
print(f"  Standard error:    {se_prop:.4f}")
print(f"  95% CI:            [{ci_lower_prop:.4f}, {ci_upper_prop:.4f}]")

# Test H0: p = 0.50
p0 = 0.50
se_under_h0 = np.sqrt(p0 * (1 - p0) / n_total)
z_stat = (p_hat - p0) / se_under_h0
p_value_prop = 2 * (1 - stats.norm.cdf(abs(z_stat)))

print(f"\nHypothesis Test: H0: p = {p0:.2f}")
print(f"  z-statistic:       {z_stat:.4f}")
print(f"  p-value:           {p_value_prop:.4f}")
print(f"  Decision:          {'Reject H0' if abs(z_stat) > 1.96 else 'Fail to reject H0'}")

# ========== VISUALIZATION: HYPOTHESIS TESTING ==========

fig, axes = plt.subplots(1, 2, figsize=(16, 6))

# Panel A: Two-sided test
x = np.linspace(-4, 4, 500)
y = stats.t.pdf(x, n - 1)

axes[0].plot(x, y, 'b-', linewidth=2, label=f't({n-1}) distribution')
axes[0].axvline(x=t_stat, color='red', linewidth=2, linestyle='--',
                label=f't-statistic = {t_stat:.2f}')
axes[0].axvline(x=t_crit_95, color='green', linewidth=1.5, linestyle=':',
                label=f'Critical value = ±{t_crit_95:.2f}')
axes[0].axvline(x=-t_crit_95, color='green', linewidth=1.5, linestyle=':')

# Shade rejection regions
x_reject_lower = x[x < -t_crit_95]
x_reject_upper = x[x > t_crit_95]
axes[0].fill_between(x_reject_lower, 0, stats.t.pdf(x_reject_lower, n-1),
                      alpha=0.3, color='red', label='Rejection region')
axes[0].fill_between(x_reject_upper, 0, stats.t.pdf(x_reject_upper, n-1),
                      alpha=0.3, color='red')

axes[0].set_xlabel('t-statistic', fontsize=12)
axes[0].set_ylabel('Density', fontsize=12)
# axes[0].set_title('Panel A: Two-Sided Hypothesis Test', fontsize=13, fontweight='bold')  # Removed: redundant with LaTeX caption
# axes[0].legend(fontsize=9)  # Removed: redundant with LaTeX caption
axes[0].grid(True, alpha=0.3)

# Panel B: One-sided test
axes[1].plot(x, y, 'b-', linewidth=2, label=f't({n-1}) distribution')
axes[1].axvline(x=t_stat, color='red', linewidth=2, linestyle='--',
                label=f't-statistic = {t_stat:.2f}')
axes[1].axvline(x=t_crit_upper, color='green', linewidth=1.5, linestyle=':',
                label=f'Critical value = {t_crit_upper:.2f}')

# Shade rejection region (upper tail)
x_reject = x[x > t_crit_upper]
axes[1].fill_between(x_reject, 0, stats.t.pdf(x_reject, n-1),
                      alpha=0.3, color='red', label='Rejection region')

axes[1].set_xlabel('t-statistic', fontsize=12)
axes[1].set_ylabel('Density', fontsize=12)
# axes[1].set_title('Panel B: One-Sided Hypothesis Test (Upper-tailed)  # Removed: redundant with LaTeX caption',
#                   fontsize=13, fontweight='bold')  # Removed: redundant with LaTeX caption
axes[1].legend(fontsize=9)
axes[1].grid(True, alpha=0.3)

# plt.suptitle('Hypothesis Testing Visualization', fontsize=14, fontweight='bold', y=1.0)  # Removed: redundant with LaTeX caption
output_file = os.path.join(IMAGES_DIR, 'ch04_hypothesis_testing_visualization.png')
plt.tight_layout()
plt.savefig(output_file, dpi=300, bbox_inches='tight')
print(f"\nHypothesis testing visualization saved to: {output_file}")
plt.close()

# ========== SUMMARY ==========

print("\n" + "=" * 70)
print("CHAPTER 4 ANALYSIS COMPLETE")
print("=" * 70)
print("\nKey concepts demonstrated:")
print("  - t-distribution vs normal distribution")
print("  - Confidence intervals for population mean")
print("  - Two-sided hypothesis tests")
print("  - One-sided (directional) hypothesis tests")
print("  - Inference for proportions")
print("  - Critical values and p-values")
print("\nAll figures saved to:", IMAGES_DIR)
