"""
ch15_Regression_with_Transformed_Variables.py - January 2026 for Python

Chapter 15: REGRESSION WITH TRANSFORMED VARIABLES

To run you need file:
  AED_EARNINGS_COMPLETE.DTA
in the data/ directory

Sections covered:
  15.1 EXAMPLE: EARNINGS, GENDER, EDUCATION and TYPE OF WORKER
  15.2 MARGINAL EFFECTS FOR NONLINEAR MODELS
  15.3 QUADRATIC MODEL AND POLYNOMIAL MODELS
  15.4 INTERACTED REGRESSORS
  15.5 LOG-LINEAR AND LOG-LOG MODELS
  15.6 PREDICTION FROM LOG-LINEAR AND LOG-LOG MODELS
  15.7 MODELS WITH A MIX OF REGRESSOR TYPES
"""

# ========== SETUP ==========

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import statsmodels.api as sm
from statsmodels.formula.api import ols
from statsmodels.stats.outliers_influence import variance_inflation_factor
from statsmodels.stats.diagnostic import het_white
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
print("CHAPTER 15: REGRESSION WITH TRANSFORMED VARIABLES")
print("=" * 70)

# ========== DATA DESCRIPTION ==========

# Annual Earnings for 842 male and female full-time workers
# aged 25-65 years old in 2010

# ========== 15.1 EXAMPLE: EARNINGS, GENDER, EDUCATION and TYPE OF WORKER ==========

print("\n" + "=" * 70)
print("15.1 EXAMPLE: EARNINGS, GENDER, EDUCATION and TYPE OF WORKER")
print("=" * 70)

# Read in the Stata data set
data_earnings = pd.read_stata(GITHUB_DATA_URL + 'AED_EARNINGS_COMPLETE.DTA')

print("\nData structure:")
print(data_earnings.info())

print("\nData summary:")
data_summary = data_earnings.describe()
print(data_summary)
data_summary.to_csv(os.path.join(TABLES_DIR, 'ch15_earnings_descriptive_stats.csv'))
print(f"Table saved to: {os.path.join(TABLES_DIR, 'ch15_earnings_descriptive_stats.csv')}")

# Table 15.1 - Selected variables
print("\n" + "-" * 70)
print("Table 15.1: Summary Statistics for Key Variables")
print("-" * 70)
table151vars = ["earnings", "lnearnings", "age", "agesq", "education", "agebyeduc",
                "lnage", "gender", "dself", "dprivate", "dgovt", "hours", "lnhours"]
print(data_earnings[table151vars].describe())

# ========== 15.2 MARGINAL EFFECTS FOR NONLINEAR MODELS ==========

print("\n" + "=" * 70)
print("15.2 MARGINAL EFFECTS FOR NONLINEAR MODELS")
print("=" * 70)
print("\nNote: Figures 15.1 and 15.2 use generated data (not reproduced here)")
print("Marginal effects calculations are demonstrated in sections 15.3 and 15.4")

# ========== 15.3 QUADRATIC AND POLYNOMIAL MODELS ==========

print("\n" + "=" * 70)
print("15.3 QUADRATIC AND POLYNOMIAL MODELS")
print("=" * 70)

# Linear Model
print("\n" + "-" * 70)
print("Linear Model: earnings ~ age + education")
print("-" * 70)
ols_linear = ols('earnings ~ age + education', data=data_earnings).fit(cov_type='HC1')
print(ols_linear.summary())

# Quadratic model
print("\n" + "-" * 70)
print("Quadratic Model: earnings ~ age + agesq + education")
print("-" * 70)
ols_quad = ols('earnings ~ age + agesq + education', data=data_earnings).fit(cov_type='HC1')
print(ols_quad.summary())

# Turning point
bage = ols_quad.params['age']
bagesq = ols_quad.params['agesq']
turning_point = -bage / (2 * bagesq)
print(f"\nTurning point for age: {turning_point:.2f} years")

# Marginal effects
print("\n" + "-" * 70)
print("Marginal Effects for Age in Quadratic Model")
print("-" * 70)
mequad = bage + 2 * bagesq * data_earnings['age']
print(f"\nMarginal effect summary statistics:")
print(mequad.describe())

AME_age = mequad.mean()
print(f"\nAverage Marginal Effect (AME) for age: {AME_age:.4f}")

MEM_age = bage + 2 * bagesq * data_earnings['age'].mean()
print(f"Marginal Effect at Mean (MEM) for age: {MEM_age:.4f}")

MER_age25 = bage + 2 * bagesq * 25
print(f"Marginal Effect at Representative value (MER) for age=25: {MER_age25:.4f}")

# Joint hypothesis test for age coefficients
print("\n" + "-" * 70)
print("Joint Hypothesis Test: H0: age = 0 and agesq = 0")
print("-" * 70)
hypotheses = '(age = 0, agesq = 0)'
f_test = ols_quad.wald_test(hypotheses, use_f=True)
print(f_test)

# Alternative using I() notation for squared term
print("\n" + "-" * 70)
print("Alternative: Using I(age**2) notation")
print("-" * 70)
ols_factor_quad = ols('earnings ~ age + I(age**2) + education', data=data_earnings).fit(cov_type='HC1')
print(ols_factor_quad.summary())

# ========== 15.4 INTERACTED REGRESSORS ==========

print("\n" + "=" * 70)
print("15.4 INTERACTED REGRESSORS")
print("=" * 70)

# Regression with interactions
print("\n" + "-" * 70)
print("Interaction Model: earnings ~ age + education + agebyeduc")
print("-" * 70)
ols_interact = ols('earnings ~ age + education + agebyeduc', data=data_earnings).fit(cov_type='HC1')
print(ols_interact.summary())

# Joint test for statistical significance of age
print("\n" + "-" * 70)
print("Joint Hypothesis Test: H0: age = 0 and agebyeduc = 0")
print("-" * 70)
hypotheses = '(age = 0, agebyeduc = 0)'
f_test = ols_interact.wald_test(hypotheses, use_f=True)
print(f_test)

# The regressors are highly correlated
print("\n" + "-" * 70)
print("Correlation Matrix of Regressors")
print("-" * 70)
corr_matrix = data_earnings[['age', 'education', 'agebyeduc']].corr()
print(corr_matrix)
corr_matrix.to_csv(os.path.join(TABLES_DIR, 'ch15_correlation_matrix.csv'))
print(f"Table saved to: {os.path.join(TABLES_DIR, 'ch15_correlation_matrix.csv')}")

# Marginal effects manually
print("\n" + "-" * 70)
print("Marginal Effects for Education in Interaction Model")
print("-" * 70)
beducation = ols_interact.params['education']
bagebyeduc = ols_interact.params['agebyeduc']
meinteract = beducation + bagebyeduc * data_earnings['age']
print(f"\nMarginal effect summary statistics:")
print(meinteract.describe())

AME_educ = meinteract.mean()
print(f"\nAverage Marginal Effect (AME) for education: {AME_educ:.4f}")

MEM_educ = beducation + bagebyeduc * data_earnings['age'].mean()
print(f"Marginal Effect at Mean (MEM) for education: {MEM_educ:.4f}")

MER_educ_25 = beducation + bagebyeduc * 25
print(f"Marginal Effect at Representative value (MER) for age=25: {MER_educ_25:.4f}")

# Alternative using * notation for interaction
print("\n" + "-" * 70)
print("Alternative: Using age*education notation")
print("-" * 70)
ols_factor_interact = ols('earnings ~ age * education', data=data_earnings).fit(cov_type='HC1')
print(ols_factor_interact.summary())

# ========== 15.5 LOG-LINEAR AND LOG-LOG MODELS ==========

print("\n" + "=" * 70)
print("15.5 LOG-LINEAR AND LOG-LOG MODELS")
print("=" * 70)

# Levels model
print("\n" + "-" * 70)
print("Levels Model: earnings ~ age + education")
print("-" * 70)
ols_linear2 = ols('earnings ~ age + education', data=data_earnings).fit(cov_type='HC1')
print(ols_linear2.summary())

# Log-linear model
print("\n" + "-" * 70)
print("Log-Linear Model: lnearnings ~ age + education")
print("-" * 70)
ols_loglin = ols('lnearnings ~ age + education', data=data_earnings).fit(cov_type='HC1')
print(ols_loglin.summary())

# Log-log model
print("\n" + "-" * 70)
print("Log-Log Model: lnearnings ~ lnage + education")
print("-" * 70)
ols_loglog = ols('lnearnings ~ lnage + education', data=data_earnings).fit(cov_type='HC1')
print(ols_loglog.summary())

# Comparison table
print("\n" + "-" * 70)
print("Model Comparison: Levels, Log-Linear, and Log-Log")
print("-" * 70)
print(f"{'Model':<15} {'R-squared':<12} {'Adj R-squared':<15}")
print("-" * 70)
print(f"{'Levels':<15} {ols_linear2.rsquared:<12.4f} {ols_linear2.rsquared_adj:<15.4f}")
print(f"{'Log-Linear':<15} {ols_loglin.rsquared:<12.4f} {ols_loglin.rsquared_adj:<15.4f}")
print(f"{'Log-Log':<15} {ols_loglog.rsquared:<12.4f} {ols_loglog.rsquared_adj:<15.4f}")

# ========== 15.6 PREDICTION FROM LOG-LINEAR AND LOG-LOG MODELS ==========

print("\n" + "=" * 70)
print("15.6 PREDICTION FROM LOG-LINEAR AND LOG-LOG MODELS")
print("=" * 70)

# Levels model predictions
print("\n" + "-" * 70)
print("Predictions from Levels Model")
print("-" * 70)
ols_linear_pred = ols('earnings ~ age + education', data=data_earnings).fit(cov_type='HC1')
linear_predict = ols_linear_pred.predict()

# Retransformation bias in log-linear model
print("\n" + "-" * 70)
print("Retransformation Bias in Log-Linear Model")
print("-" * 70)
ols_loglin_pred = ols('lnearnings ~ age + education', data=data_earnings).fit(cov_type='HC1')
predict_log = ols_loglin_pred.predict()
biased_predict = np.exp(predict_log)
rmse = np.sqrt(ols_loglin_pred.mse_resid)
print(f"\nRoot MSE: {rmse:.4f}")

adjustment_factor = np.exp(rmse**2 / 2)
print(f"Adjustment factor: exp(RMSE²/2) = {adjustment_factor:.4f}")

adjusted_predict = adjustment_factor * biased_predict

# Compare predictions
print("\n" + "-" * 70)
print("Comparison of Predictions: Log-Linear Model")
print("-" * 70)
comparison_df = pd.DataFrame({
    'earnings': data_earnings['earnings'],
    'linear_predict': linear_predict,
    'biased_predict': biased_predict,
    'adjusted_predict': adjusted_predict
})
print(comparison_df.describe())

# Correlations
print("\n" + "-" * 70)
print("Correlations Between Actual and Predicted Values")
print("-" * 70)
print(comparison_df.corr())

# Retransformation bias in log-log model
print("\n" + "-" * 70)
print("Retransformation Bias in Log-Log Model")
print("-" * 70)
ols_loglog_pred = ols('lnearnings ~ lnage + education', data=data_earnings).fit(cov_type='HC1')
predict_loglog = ols_loglog_pred.predict()
biased_predict_loglog = np.exp(predict_loglog)
rmse_loglog = np.sqrt(ols_loglog_pred.mse_resid)
print(f"\nRoot MSE: {rmse_loglog:.4f}")

adjustment_factor_loglog = np.exp(rmse_loglog**2 / 2)
print(f"Adjustment factor: exp(RMSE²/2) = {adjustment_factor_loglog:.4f}")

adjusted_predict_loglog = adjustment_factor_loglog * biased_predict_loglog

# Compare predictions
print("\n" + "-" * 70)
print("Comparison of Predictions: Log-Log Model")
print("-" * 70)
comparison_df_loglog = pd.DataFrame({
    'earnings': data_earnings['earnings'],
    'linear_predict': linear_predict,
    'biased_predict': biased_predict_loglog,
    'adjusted_predict': adjusted_predict_loglog
})
print(comparison_df_loglog.describe())

# Correlations
print("\n" + "-" * 70)
print("Correlations Between Actual and Predicted Values")
print("-" * 70)
print(comparison_df_loglog.corr())

# ========== 15.7 MODELS WITH A MIX OF REGRESSOR TYPES ==========

print("\n" + "=" * 70)
print("15.7 MODELS WITH A MIX OF REGRESSOR TYPES")
print("=" * 70)

# Linear dependent variable
print("\n" + "-" * 70)
print("Linear Model with Mixed Regressors:")
print("earnings ~ gender + age + agesq + education + dself + dgovt + lnhours")
print("-" * 70)
ols_linear_mix = ols('earnings ~ gender + age + agesq + education + dself + dgovt + lnhours',
                     data=data_earnings).fit(cov_type='HC1')
print(ols_linear_mix.summary())
linear_predict_mix = ols_linear_mix.predict()

# Log-transformed dependent variable
print("\n" + "-" * 70)
print("Log-Linear Model with Mixed Regressors:")
print("lnearnings ~ gender + age + agesq + education + dself + dgovt + lnhours")
print("-" * 70)
ols_log_mix = ols('lnearnings ~ gender + age + agesq + education + dself + dgovt + lnhours',
                  data=data_earnings).fit(cov_type='HC1')
print(ols_log_mix.summary())

# Predictions with retransformation adjustment
predict_log_mix = ols_log_mix.predict()
biased_predict_mix = np.exp(predict_log_mix)
rmse_mix = np.sqrt(ols_log_mix.mse_resid)
print(f"\nRoot MSE: {rmse_mix:.4f}")

adjustment_factor_mix = np.exp(rmse_mix**2 / 2)
print(f"Adjustment factor: exp(RMSE²/2) = {adjustment_factor_mix:.4f}")

adjusted_predict_mix = adjustment_factor_mix * biased_predict_mix

# Compare predictions
print("\n" + "-" * 70)
print("Comparison of Predictions: Mixed Regressor Models")
print("-" * 70)
comparison_df_mix = pd.DataFrame({
    'earnings': data_earnings['earnings'],
    'linear_predict': linear_predict_mix,
    'biased_predict': biased_predict_mix,
    'adjusted_predict': adjusted_predict_mix
})
print(comparison_df_mix.describe())

# Correlations
print("\n" + "-" * 70)
print("Correlations Between Actual and Predicted Values")
print("-" * 70)
print(comparison_df_mix.corr())

# Standardized coefficients
print("\n" + "-" * 70)
print("Standardized Regression Coefficients (Beta Coefficients)")
print("-" * 70)
print("Note: Standardized coefficients show the effect of one standard deviation")
print("change in each regressor on the dependent variable (in standard deviations)")

# Calculate standardized coefficients manually
# Beta = b * (sd_x / sd_y)
y_std = data_earnings['earnings'].std()
regressors = ['gender', 'age', 'agesq', 'education', 'dself', 'dgovt', 'lnhours']
standardized_coefs = {}

for var in regressors:
    x_std = data_earnings[var].std()
    beta = ols_linear_mix.params[var] * (x_std / y_std)
    standardized_coefs[var] = beta

print("\nStandardized Coefficients:")
for var, beta in standardized_coefs.items():
    print(f"  {var:<12}: {beta:>10.4f}")

# Create visualization comparing standardized coefficients
fig, ax = plt.subplots(figsize=(10, 6))
vars_plot = list(standardized_coefs.keys())
betas_plot = list(standardized_coefs.values())

colors = ['red' if b < 0 else 'blue' for b in betas_plot]
bars = ax.barh(vars_plot, betas_plot, color=colors, alpha=0.7)

ax.axvline(x=0, color='black', linestyle='-', linewidth=0.8)
ax.set_xlabel('Standardized Coefficient', fontsize=12)
ax.set_ylabel('Variable', fontsize=12)
ax.set_title('Standardized Regression Coefficients\n(Effect of 1 SD change in X on Y, in SD units)',
             fontsize=14, fontweight='bold')
ax.grid(True, alpha=0.3, axis='x')

output_file = os.path.join(IMAGES_DIR, 'ch15_standardized_coefficients.png')
plt.tight_layout()
plt.savefig(output_file, dpi=300, bbox_inches='tight')
print(f"\nFigure saved to: {output_file}")
plt.close()

# ========== SUMMARY ==========

print("\n" + "=" * 70)
print("CHAPTER 15 ANALYSIS COMPLETE")
print("=" * 70)
print("\nKey concepts demonstrated:")
print("  - Quadratic and polynomial models")
print("  - Marginal effects (AME, MEM, MER)")
print("  - Interaction terms and their interpretation")
print("  - Log-linear and log-log transformations")
print("  - Retransformation bias and adjustment")
print("  - Models with mixed regressor types")
print("  - Standardized regression coefficients")
print("\nAll figures saved to:", IMAGES_DIR)
