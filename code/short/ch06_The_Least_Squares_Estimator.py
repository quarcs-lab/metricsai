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
