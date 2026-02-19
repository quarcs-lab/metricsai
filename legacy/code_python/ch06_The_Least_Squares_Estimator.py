# %%
"""
ch06_The_Least_Squares_Estimator.py - January 2026 for Python

Chapter 6: THE LEAST SQUARES ESTIMATOR

To run you need files:
  AED_GENERATEDDATA.DTA
  AED_GENERATEDREGRESSION.DTA
  AED_CENSUSREGRESSIONS.DTA
in the data_stata/ directory

Sections covered:
  6.1 POPULATION AND SAMPLE
  6.2 EXAMPLES OF SAMPLING FROM A POPULATION
  6.3 PROPERTIES OF THE LEAST SQUARES ESTIMATOR
  6.4 ESTIMATORS OF MODEL PARAMETERS
"""

# %% =========== SETUP ==========

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

# Output directories (optional - for saving figures and tables locally)
IMAGES_DIR = 'images'
TABLES_DIR = 'tables'
os.makedirs(IMAGES_DIR, exist_ok=True)
os.makedirs(TABLES_DIR, exist_ok=True)

# Set plotting style
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (10, 6)

print("=" * 70)
print("CHAPTER 6: THE LEAST SQUARES ESTIMATOR")
print("=" * 70)

# %% =========== 6.2 EXAMPLES OF SAMPLING FROM A POPULATION ==========

print("\n" + "=" * 70)
print("6.2 EXAMPLES OF SAMPLING FROM A POPULATION")
print("=" * 70)

# Read in generated data
data_gen = pd.read_stata(GITHUB_DATA_URL + 'AED_GENERATEDDATA.DTA')

# %% Explore data structure

print("\nGenerated data summary:")
data_summary = data_gen.describe()

# %% Calculate statistics
print(data_summary)
print("\nFirst 10 observations (Table 6.1):")
print(data_gen.head(10))
data_summary.to_csv(os.path.join(TABLES_DIR, 'ch06_generated_data_descriptive_stats.csv'))
print(f"Table saved to: {os.path.join(TABLES_DIR, 'ch06_generated_data_descriptive_stats.csv')}")

# Figure 6.2: Panel A - Population regression line E[y|x] = 1 + 2x

# %% Estimate regression model

model_population = ols('Eygivenx ~ x', data=data_gen).fit()

fig, ax = plt.subplots(figsize=(10, 6))
ax.scatter(data_gen['x'], data_gen['y'], alpha=0.6, s=50, color='black', label='Actual')
ax.plot(data_gen['x'], model_population.fittedvalues,
        color='blue', linewidth=2, label='Population line E[y|x]')
ax.set_xlabel('Regressor x', fontsize=12)
ax.set_ylabel('Dependent variable y', fontsize=12)
# ax.set_title('Figure 6.2 Panel A: Population Line E[y|x] = 1 + 2x',
#              fontsize=14, fontweight='bold')  # Removed: redundant with LaTeX caption
ax.legend()
ax.grid(True, alpha=0.3)

output_file = os.path.join(IMAGES_DIR, 'ch06_fig2a_population_line.png')
plt.tight_layout()
plt.savefig(output_file, dpi=300, bbox_inches='tight')
print(f"\nFigure 6.2 Panel A saved to: {output_file}")
plt.close()

print("\nPopulation regression results:")

# %% Display regression results

print(model_population.summary())
# Save regression coefficients
coef_table = pd.DataFrame({
    'coefficient': model_population.params,
    'std_err': model_population.bse,
    't_value': model_population.tvalues,
    'p_value': model_population.pvalues
})
coef_table.to_csv(os.path.join(TABLES_DIR, 'ch06_population_regression_coefficients.csv'))
print(f"Coefficients saved to: {os.path.join(TABLES_DIR, 'ch06_population_regression_coefficients.csv')}")

# Figure 6.2: Panel B - Sample regression line

# %% Estimate regression model

model_sample = ols('y ~ x', data=data_gen).fit()

fig, ax = plt.subplots(figsize=(10, 6))
ax.scatter(data_gen['x'], data_gen['y'], alpha=0.6, s=50, color='black', label='Actual')
ax.plot(data_gen['x'], model_sample.fittedvalues,
        color='red', linewidth=2, label=f'Sample line ŷ = {model_sample.params[0]:.2f} + {model_sample.params[1]:.2f}x')
ax.set_xlabel('Regressor x', fontsize=12)
ax.set_ylabel('Dependent variable y', fontsize=12)
# ax.set_title('Figure 6.2 Panel B: Sample Regression Line',
#              fontsize=14, fontweight='bold')  # Removed: redundant with LaTeX caption
ax.legend()
ax.grid(True, alpha=0.3)

output_file = os.path.join(IMAGES_DIR, 'ch06_fig2b_sample_regression.png')
plt.tight_layout()
plt.savefig(output_file, dpi=300, bbox_inches='tight')
print(f"Figure 6.2 Panel B saved to: {output_file}")
plt.close()

print("\nSample regression results:")

# %% Display regression results

print(model_sample.summary())

# %% =========== THREE REGRESSIONS FROM THE SAME MODEL ==========

print("\n" + "=" * 70)
print("DEMONSTRATION: Three Regressions from the Same DGP")
print("=" * 70)

# Generate three samples from the same data generating process
np.random.seed(12345)
n = 30

# Sample 1
x1 = np.random.normal(3, 1, n)
u1 = np.random.normal(0, 2, n)
y1 = 1 + 2*x1 + u1

# Sample 2
x2 = np.random.normal(3, 1, n)
u2 = np.random.normal(0, 2, n)
y2 = 1 + 2*x2 + u2

# Sample 3
x3 = np.random.normal(3, 1, n)
u3 = np.random.normal(0, 2, n)
y3 = 1 + 2*x3 + u3

# Create dataframes
df1 = pd.DataFrame({'x': x1, 'y': y1})
df2 = pd.DataFrame({'x': x2, 'y': y2})
df3 = pd.DataFrame({'x': x3, 'y': y3})

# Fit regressions

# %% Estimate regression model

model1 = ols('y ~ x', data=df1).fit()

# %% Estimate regression model

model2 = ols('y ~ x', data=df2).fit()

# %% Estimate regression model

model3 = ols('y ~ x', data=df3).fit()

print("\nSample 1 - Regression coefficients:")
print(f"  Intercept: {model1.params[0]:.4f}, Slope: {model1.params[1]:.4f}")

print("\nSample 2 - Regression coefficients:")
print(f"  Intercept: {model2.params[0]:.4f}, Slope: {model2.params[1]:.4f}")

print("\nSample 3 - Regression coefficients:")
print(f"  Intercept: {model3.params[0]:.4f}, Slope: {model3.params[1]:.4f}")

print(f"\nTrue population parameters: Intercept = 1.0, Slope = 2.0")

# Visualize all three regressions
fig, axes = plt.subplots(1, 3, figsize=(18, 5))

for idx, (ax, df, model, title) in enumerate(zip(axes,
                                                   [df1, df2, df3],
                                                   [model1, model2, model3],
                                                   ['Sample 1', 'Sample 2', 'Sample 3'])):
    ax.scatter(df['x'], df['y'], alpha=0.6, s=50, color='black', label='Actual')
    ax.plot(df['x'], model.fittedvalues, color='red', linewidth=2,
            label=f'ŷ = {model.params[0]:.2f} + {model.params[1]:.2f}x')
    # Add population line
    x_range = np.linspace(df['x'].min(), df['x'].max(), 100)
    y_pop = 1 + 2*x_range
    ax.plot(x_range, y_pop, color='blue', linewidth=2, linestyle='--',
            label='Population: y = 1 + 2x', alpha=0.7)
    ax.set_xlabel('x', fontsize=11)
    ax.set_ylabel('y', fontsize=11)
    # ax.set_title(title, fontsize=12, fontweight='bold')  # Removed: redundant with LaTeX caption
#     ax.legend(fontsize=9)  # Removed: redundant with LaTeX caption
    ax.grid(True, alpha=0.3)

# plt.suptitle('Three Different Samples from the Same DGP: y = 1 + 2x + u',
#              fontsize=14, fontweight='bold', y=1.02)  # Removed: redundant with LaTeX caption
output_file = os.path.join(IMAGES_DIR, 'ch06_three_samples_same_dgp.png')
plt.tight_layout()
plt.savefig(output_file, dpi=300, bbox_inches='tight')
print(f"\nThree samples figure saved to: {output_file}")
plt.close()

# %% Continue analysis

# %% =========== 6.3 PROPERTIES OF THE LEAST SQUARES ESTIMATOR ==========

print("\n" + "=" * 70)
print("6.3 PROPERTIES OF THE LEAST SQUARES ESTIMATOR")
print("=" * 70)

# Read in regression data (if available)
try:
    data_reg = pd.read_stata(GITHUB_DATA_URL + 'AED_GENERATEDREGRESSION.DTA')

# %% Explore data structure

    print("\nGenerated regression data summary:")
    print(data_reg.describe())

    # If the data contains regression coefficients from multiple samples
    if 'beta1' in data_reg.columns:
        print("\n" + "-" * 70)
        print("Distribution of OLS estimates across samples:")
        print("-" * 70)
        print(f"Mean of β̂₁: {data_reg['beta1'].mean():.4f}")
        print(f"Std dev of β̂₁: {data_reg['beta1'].std():.4f}")

        # Histogram of slope estimates
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.hist(data_reg['beta1'], bins=30, density=True,
                edgecolor='black', alpha=0.7, color='steelblue',
                label='OLS estimates')

        # Overlay normal distribution
        x_range = np.linspace(data_reg['beta1'].min(), data_reg['beta1'].max(), 100)
        normal_pdf = stats.norm.pdf(x_range, data_reg['beta1'].mean(), data_reg['beta1'].std())
        ax.plot(x_range, normal_pdf, 'r-', linewidth=2, label='Normal fit')

        # Add vertical line at true parameter value
        ax.axvline(x=2.0, color='green', linewidth=2, linestyle='--', label='True β₁ = 2.0')

        ax.set_xlabel('Estimated slope coefficient β̂₁', fontsize=12)
        ax.set_ylabel('Density', fontsize=12)
        # ax.set_title('Sampling Distribution of OLS Slope Estimator',
#                      fontsize=14, fontweight='bold')  # Removed: redundant with LaTeX caption
        ax.legend()
        ax.grid(True, alpha=0.3)

        output_file = os.path.join(IMAGES_DIR, 'ch06_sampling_distribution_ols.png')
        plt.tight_layout()
        plt.savefig(output_file, dpi=300, bbox_inches='tight')
        print(f"\nSampling distribution figure saved to: {output_file}")
        plt.close()

except (FileNotFoundError, Exception) as e:
    print("\nNote: AED_GENERATEDREGRESSION.DTA not found, skipping this section")

# %% =========== SIMULATION: SAMPLING DISTRIBUTION OF OLS ==========

print("\n" + "=" * 70)
print("SIMULATION: Sampling Distribution of OLS Estimator")
print("=" * 70)

# Simulate many regressions to demonstrate sampling distribution
np.random.seed(42)
n_simulations = 1000
sample_size = 30

beta0_estimates = np.zeros(n_simulations)
beta1_estimates = np.zeros(n_simulations)

for i in range(n_simulations):
    # Generate data from DGP: y = 1 + 2x + u
    x = np.random.normal(3, 1, sample_size)
    u = np.random.normal(0, 2, sample_size)
    y = 1 + 2*x + u

    # Fit OLS
    df = pd.DataFrame({'x': x, 'y': y})

# %% Estimate regression model

    model = ols('y ~ x', data=df).fit()

    beta0_estimates[i] = model.params[0]
    beta1_estimates[i] = model.params[1]

print(f"\nSimulation results ({n_simulations} replications):")
print(f"\nIntercept β₀:")
print(f"  Mean: {beta0_estimates.mean():.4f} (True value: 1.0)")
print(f"  Std dev: {beta0_estimates.std():.4f}")

print(f"\nSlope β₁:")
print(f"  Mean: {beta1_estimates.mean():.4f} (True value: 2.0)")
print(f"  Std dev: {beta1_estimates.std():.4f}")

# Visualize sampling distributions
fig, axes = plt.subplots(1, 2, figsize=(16, 6))

# Beta0 distribution
axes[0].hist(beta0_estimates, bins=40, density=True,
             edgecolor='black', alpha=0.7, color='coral', label='Simulated')
x_range = np.linspace(beta0_estimates.min(), beta0_estimates.max(), 100)
axes[0].plot(x_range, stats.norm.pdf(x_range, beta0_estimates.mean(), beta0_estimates.std()),
             'b-', linewidth=2, label='Normal fit')
axes[0].axvline(x=1.0, color='green', linewidth=2, linestyle='--', label='True β₀ = 1.0')
axes[0].set_xlabel('Estimated intercept β̂₀', fontsize=11)
axes[0].set_ylabel('Density', fontsize=11)
# axes[0].set_title('Sampling Distribution of Intercept', fontsize=12, fontweight='bold')  # Removed: redundant with LaTeX caption
# axes[0].legend()  # Removed: redundant with LaTeX caption
axes[0].grid(True, alpha=0.3)

# Beta1 distribution
axes[1].hist(beta1_estimates, bins=40, density=True,
             edgecolor='black', alpha=0.7, color='steelblue', label='Simulated')
x_range = np.linspace(beta1_estimates.min(), beta1_estimates.max(), 100)
axes[1].plot(x_range, stats.norm.pdf(x_range, beta1_estimates.mean(), beta1_estimates.std()),
             'r-', linewidth=2, label='Normal fit')
axes[1].axvline(x=2.0, color='green', linewidth=2, linestyle='--', label='True β₁ = 2.0')
axes[1].set_xlabel('Estimated slope β̂₁', fontsize=11)
axes[1].set_ylabel('Density', fontsize=11)
# axes[1].set_title('Sampling Distribution of Slope', fontsize=12, fontweight='bold')  # Removed: redundant with LaTeX caption
# axes[1].legend()  # Removed: redundant with LaTeX caption
axes[1].grid(True, alpha=0.3)

# plt.suptitle(f'Simulation of OLS Sampling Distributions ({n_simulations} replications)  # Removed: redundant with LaTeX caption',
#              fontsize=14, fontweight='bold', y=1.0)  # Removed: redundant with LaTeX caption
output_file = os.path.join(IMAGES_DIR, 'ch06_simulation_ols_sampling_distributions.png')
plt.tight_layout()
plt.savefig(output_file, dpi=300, bbox_inches='tight')
print(f"\nSimulation figure saved to: {output_file}")
plt.close()

# %% Continue analysis

# %% =========== SUMMARY ==========

print("\n" + "=" * 70)
print("CHAPTER 6 ANALYSIS COMPLETE")
print("=" * 70)
print("\nKey concepts demonstrated:")
print("  - Population vs. sample regression")
print("  - Ordinary Least Squares (OLS) estimation")
print("  - Properties of OLS estimators (unbiasedness, consistency)")
print("  - Sampling distribution of regression coefficients")
print("  - Monte Carlo simulation to verify theoretical properties")
print("\nAll figures saved to:", IMAGES_DIR)
