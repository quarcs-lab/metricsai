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
