# %%
"""
ch14_Regression_with_Indicator_Variables.py - January 2026 for Python

Chapter 14: REGRESSION WITH INDICATOR VARIABLES

To run you need file:
  AED_EARNINGS_COMPLETE.DTA
in the data/ directory

Sections covered:
  14.1 EXAMPLE: EARNINGS, GENDER, EDUCATION and TYPE OF WORKER
  14.2 REGRESSION ON JUST A SINGLE INDICATOR VARIABLE
  14.3 REGRESSION ON A SINGLE INDICATOR VARIABLE AND ADDITIONAL REGRESSORS
  14.4 REGRESSION ON SETS OF INDICATOR VARIABLES
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
print("CHAPTER 14: REGRESSION WITH INDICATOR VARIABLES")
print("=" * 70)

# %% =========== DATA PREPARATION ==========

# Load earnings data
data = pd.read_stata(GITHUB_DATA_URL + 'AED_EARNINGS_COMPLETE.DTA')

# %% Explore data structure

print("\nData description:")
data_summary = data.describe()

# %% Calculate statistics
print(data_summary)
data_summary.to_csv(os.path.join(TABLES_DIR, 'ch14_earnings_descriptive_stats.csv'))
print(f"Table saved to: {os.path.join(TABLES_DIR, 'ch14_earnings_descriptive_stats.csv')}")

# %% =========== 14.1 EXAMPLE: EARNINGS, GENDER, EDUCATION and TYPE OF WORKER ==========

print("\n" + "=" * 70)
print("14.1 EXAMPLE: EARNINGS, GENDER, EDUCATION and TYPE OF WORKER")
print("=" * 70)

# Table 14.1: Summary statistics
print("\n" + "-" * 70)
print("Table 14.1: Summary Statistics")
print("-" * 70)

variables = ['earnings', 'gender', 'education', 'genderbyeduc', 'age',
             'genderbyage', 'hours', 'genderbyhours', 'dself', 'dprivate', 'dgovt']

print("\nVariable descriptions:")
for var in variables:
    print(f"  {var}: {data[var].dtype}")

summary_stats = data[variables].describe()
print("\n", summary_stats)

# Additional info
print("\nNote on indicator variables:")
print(f"  gender: 1=female, 0=male")
print(f"  dself: 1=self-employed, 0=not")
print(f"  dprivate: 1=private sector, 0=not")
print(f"  dgovt: 1=government, 0=not")

# %% =========== 14.2 REGRESSION ON JUST A SINGLE INDICATOR VARIABLE ==========

print("\n" + "=" * 70)
print("14.2 REGRESSION ON JUST A SINGLE INDICATOR VARIABLE")
print("=" * 70)

# Table 14.2: Summary statistics by gender
print("\n" + "-" * 70)
print("Table 14.2: Summary Statistics by Gender")
print("-" * 70)

print("\nFemale (gender=1):")
print(data[data['gender'] == 1]['earnings'].describe())

# %% Calculate statistics

print("\nMale (gender=0):")
print(data[data['gender'] == 0]['earnings'].describe())

# %% Calculate statistics

# Difference in means
mean_female = data[data['gender'] == 1]['earnings'].mean()
mean_male = data[data['gender'] == 0]['earnings'].mean()
diff_means = mean_female - mean_male

print(f"\nMean earnings:")
print(f"  Female: ${mean_female:.2f}")
print(f"  Male: ${mean_male:.2f}")
print(f"  Difference: ${diff_means:.2f}")

# OLS for difference in means - heteroskedastic-robust standard errors
print("\n" + "-" * 70)
print("OLS Regression: earnings on gender indicator")
print("-" * 70)


# %% Estimate regression model

model_gender = ols('earnings ~ gender', data=data).fit(cov_type='HC1')

# %% Display regression results

print(model_gender.summary())
# Save regression coefficients
coef_table = pd.DataFrame({
    'coefficient': model_gender.params,
    'std_err': model_gender.bse,
    't_value': model_gender.tvalues,
    'p_value': model_gender.pvalues
})
coef_table.to_csv(os.path.join(TABLES_DIR, 'ch14_gender_regression_coefficients.csv'))
print(f"Coefficients saved to: {os.path.join(TABLES_DIR, 'ch14_gender_regression_coefficients.csv')}")

print("\nInterpretation:")
print(f"  Intercept = Mean earnings for males (gender=0): ${model_gender.params['Intercept']:.2f}")
print(f"  Coefficient on gender = Difference in means: ${model_gender.params['gender']:.2f}")
print(f"  Females earn ${model_gender.params['gender']:.2f} less than males on average")

# Compare with t-test (unequal variances)
print("\n" + "-" * 70)
print("Independent t-test (Welch's, unequal variances)")
print("-" * 70)

female_earnings = data[data['gender'] == 1]['earnings']
male_earnings = data[data['gender'] == 0]['earnings']

t_stat, p_value = stats.ttest_ind(female_earnings, male_earnings, equal_var=False)
print(f"\nt-statistic: {t_stat:.4f}")
print(f"p-value: {p_value:.6f}")
print("\nNote: Similar results to regression with robust SEs")

# With equal variances (classical assumptions)
print("\n" + "-" * 70)
print("Comparison: Default SEs vs Robust SEs")
print("-" * 70)


# %% Estimate regression model

model_gender_default = ols('earnings ~ gender', data=data).fit()
print("\nDefault (homoskedastic) SEs:")

# %% Display regression results

print(model_gender_default.summary())

# Classical t-test (equal variances)
t_stat_eq, p_value_eq = stats.ttest_ind(female_earnings, male_earnings, equal_var=True)
print(f"\nClassical t-test (equal variances):")
print(f"  t-statistic: {t_stat_eq:.4f}")
print(f"  p-value: {p_value_eq:.6f}")
print("\nNote: With equal variance assumption, regression and t-test give identical results")

# %% =========== 14.3 REGRESSION ON A SINGLE INDICATOR VARIABLE AND ADDITIONAL REGRESSORS ==========

print("\n" + "=" * 70)
print("14.3 REGRESSION ON A SINGLE INDICATOR VARIABLE AND ADDITIONAL REGRESSORS")
print("=" * 70)

# Estimate multiple models
print("\n" + "-" * 70)
print("Table 14.3: Multiple Model Comparison")
print("-" * 70)

# Model 1: Gender indicator only

# %% Estimate regression model

model1 = ols('earnings ~ gender', data=data).fit(cov_type='HC1')
print("\nModel 1: Gender only")
print(f"  Gender coefficient: {model1.params['gender']:.0f}")
print(f"  Robust SE: {model1.bse['gender']:.0f}")
print(f"  t-statistic: {model1.tvalues['gender']:.2f}")
print(f"  p-value: {model1.pvalues['gender']:.4f}")
print(f"  R²: {model1.rsquared:.4f}")

# Test on gender
print(f"\nF-test on gender: F = {model1.tvalues['gender']**2:.2f}, p = {model1.pvalues['gender']:.4f}")

# Model 2: Add education

# %% Estimate regression model

model2 = ols('earnings ~ gender + education', data=data).fit(cov_type='HC1')
print("\nModel 2: Gender + Education")
print(f"  Gender coefficient: {model2.params['gender']:.0f}")
print(f"  Education coefficient: {model2.params['education']:.0f}")
print(f"  R²: {model2.rsquared:.4f}")

# Model 3: Interact education and gender

# %% Estimate regression model

model3 = ols('earnings ~ gender + education + genderbyeduc', data=data).fit(cov_type='HC1')
print("\nModel 3: Gender + Education + Interaction")
print(f"  Gender coefficient: {model3.params['gender']:.0f}")
print(f"  Education coefficient: {model3.params['education']:.0f}")
print(f"  Gender×Education coefficient: {model3.params['genderbyeduc']:.0f}")
print(f"  R²: {model3.rsquared:.4f}")

# Joint test on gender and interaction
f_test_3 = model3.f_test('gender = 0, genderbyeduc = 0')
f_val_3 = f_test_3.fvalue[0][0] if hasattr(f_test_3.fvalue, '__getitem__') else f_test_3.fvalue
print(f"\nJoint F-test (gender, genderbyeduc): F = {f_val_3:.2f}, p = {f_test_3.pvalue:.4f}")

# Model 4: Add additional controls

# %% Estimate regression model

model4 = ols('earnings ~ gender + education + genderbyeduc + age + hours',
             data=data).fit(cov_type='HC1')
print("\nModel 4: Add age and hours controls")
print(f"  Gender coefficient: {model4.params['gender']:.0f}")
print(f"  Education coefficient: {model4.params['education']:.0f}")
print(f"  Gender×Education coefficient: {model4.params['genderbyeduc']:.0f}")
print(f"  Age coefficient: {model4.params['age']:.0f}")
print(f"  Hours coefficient: {model4.params['hours']:.0f}")
print(f"  R²: {model4.rsquared:.4f}")

# Joint test
f_test_4 = model4.f_test('gender = 0, genderbyeduc = 0')
f_val_4 = f_test_4.fvalue[0][0] if hasattr(f_test_4.fvalue, '__getitem__') else f_test_4.fvalue
print(f"\nJoint F-test (gender, genderbyeduc): F = {f_val_4:.2f}, p = {f_test_4.pvalue:.4f}")

# Model 5: Fully interact all variables with gender

# %% Estimate regression model

model5 = ols('earnings ~ gender + education + genderbyeduc + age + hours + genderbyage + genderbyhours',
             data=data).fit(cov_type='HC1')
print("\nModel 5: Full interactions with gender")
print(f"  Gender coefficient: {model5.params['gender']:.0f}")
print(f"  Education coefficient: {model5.params['education']:.0f}")
print(f"  Gender×Education coefficient: {model5.params['genderbyeduc']:.0f}")
print(f"  Age coefficient: {model5.params['age']:.0f}")
print(f"  Gender×Age coefficient: {model5.params['genderbyage']:.0f}")
print(f"  Hours coefficient: {model5.params['hours']:.0f}")
print(f"  Gender×Hours coefficient: {model5.params['genderbyhours']:.0f}")
print(f"  R²: {model5.rsquared:.4f}")

# Joint test on all gender terms
f_test_5 = model5.f_test('gender = 0, genderbyeduc = 0, genderbyage = 0, genderbyhours = 0')
f_val_5 = f_test_5.fvalue[0][0] if hasattr(f_test_5.fvalue, '__getitem__') else f_test_5.fvalue
print(f"\nJoint F-test (all gender terms): F = {f_val_5:.2f}, p = {f_test_5.pvalue:.4f}")

# Summary table of all models
print("\n" + "-" * 70)
print("Summary Table: All Five Models")
print("-" * 70)

summary_df = pd.DataFrame({
    'Model 1': ['Gender only', model1.params.get('gender', np.nan),
                model1.bse.get('gender', np.nan), model1.tvalues.get('gender', np.nan),
                model1.nobs, model1.rsquared, model1.rsquared_adj, np.sqrt(model1.mse_resid)],
    'Model 2': ['+ Education', model2.params.get('gender', np.nan),
                model2.bse.get('gender', np.nan), model2.tvalues.get('gender', np.nan),
                model2.nobs, model2.rsquared, model2.rsquared_adj, np.sqrt(model2.mse_resid)],
    'Model 3': ['+ Gender×Educ', model3.params.get('gender', np.nan),
                model3.bse.get('gender', np.nan), model3.tvalues.get('gender', np.nan),
                model3.nobs, model3.rsquared, model3.rsquared_adj, np.sqrt(model3.mse_resid)],
    'Model 4': ['+ Age, Hours', model4.params.get('gender', np.nan),
                model4.bse.get('gender', np.nan), model4.tvalues.get('gender', np.nan),
                model4.nobs, model4.rsquared, model4.rsquared_adj, np.sqrt(model4.mse_resid)],
    'Model 5': ['Full Interact', model5.params.get('gender', np.nan),
                model5.bse.get('gender', np.nan), model5.tvalues.get('gender', np.nan),
                model5.nobs, model5.rsquared, model5.rsquared_adj, np.sqrt(model5.mse_resid)]
}, index=['Description', 'Gender Coef', 'Robust SE', 't-stat', 'N', 'R²', 'Adj R²', 'RMSE'])

print(summary_df.to_string())

# Separate regressions by gender
print("\n" + "-" * 70)
print("Separate Regressions by Gender")
print("-" * 70)

# Female regression

# %% Estimate regression model

model_female = ols('earnings ~ education + age + hours',
                   data=data[data['gender'] == 1]).fit(cov_type='HC1')
print("\nFemale subsample:")

# %% Display regression results

print(model_female.summary())

# Male regression

# %% Estimate regression model

model_male = ols('earnings ~ education + age + hours',
                 data=data[data['gender'] == 0]).fit(cov_type='HC1')
print("\nMale subsample:")

# %% Display regression results

print(model_male.summary())

# Compare coefficients
print("\n" + "-" * 70)
print("Comparison of Coefficients by Gender")
print("-" * 70)

comparison = pd.DataFrame({
    'Female': model_female.params,
    'Male': model_male.params,
    'Difference': model_female.params - model_male.params
})
print(comparison)

# %% =========== 14.4 REGRESSION ON SETS OF INDICATOR VARIABLES ==========

print("\n" + "=" * 70)
print("14.4 REGRESSION ON SETS OF INDICATOR VARIABLES")
print("=" * 70)

# Regression on indicators with no intercept
print("\n" + "-" * 70)
print("Regression with Indicator Variables (No Intercept)")
print("-" * 70)

# Model with no constant gives means for each group

# %% Estimate regression model

model_noconstant = ols('earnings ~ dself + dprivate + dgovt - 1', data=data).fit(cov_type='HC1')

# %% Display regression results

print(model_noconstant.summary())

print("\nInterpretation:")
print(f"  dself coefficient = Mean earnings for self-employed: ${model_noconstant.params['dself']:.2f}")
print(f"  dprivate coefficient = Mean earnings for private sector: ${model_noconstant.params['dprivate']:.2f}")
print(f"  dgovt coefficient = Mean earnings for government: ${model_noconstant.params['dgovt']:.2f}")

# Verify with direct means
print("\nVerification with direct means:")
print(f"  Self-employed: ${data[data['dself'] == 1]['earnings'].mean():.2f}")
print(f"  Private sector: ${data[data['dprivate'] == 1]['earnings'].mean():.2f}")
print(f"  Government: ${data[data['dgovt'] == 1]['earnings'].mean():.2f}")

# Different reference categories
print("\n" + "-" * 70)
print("Table 14.4: Different Reference Categories")
print("-" * 70)

# Base model with no indicator variables (for comparison)

# %% Estimate regression model

model_noindic = ols('earnings ~ age + education', data=data).fit(cov_type='HC1')
print("\nModel with no type of worker indicators:")
print(f"  R²: {model_noindic.rsquared:.4f}")
print(f"  RMSE: {np.sqrt(model_noindic.mse_resid):.2f}")

# Reference group: self-employed (omit dself)

# %% Estimate regression model

model_ref_self = ols('earnings ~ age + education + dprivate + dgovt',
                     data=data).fit(cov_type='HC1')
print("\nReference: Self-employed")

# %% Display regression results

print(model_ref_self.summary())
f_test_self = model_ref_self.f_test('dprivate = 0, dgovt = 0')
f_val_self = f_test_self.fvalue[0][0] if hasattr(f_test_self.fvalue, '__getitem__') else f_test_self.fvalue
print(f"Joint F-test (dprivate, dgovt): F = {f_val_self:.2f}, p = {f_test_self.pvalue:.4f}")

# Reference group: private sector (omit dprivate)

# %% Estimate regression model

model_ref_private = ols('earnings ~ age + education + dself + dgovt',
                        data=data).fit(cov_type='HC1')
print("\nReference: Private sector")

# %% Display regression results

print(model_ref_private.summary())
f_test_private = model_ref_private.f_test('dself = 0, dgovt = 0')
f_val_private = f_test_private.fvalue[0][0] if hasattr(f_test_private.fvalue, '__getitem__') else f_test_private.fvalue
print(f"Joint F-test (dself, dgovt): F = {f_val_private:.2f}, p = {f_test_private.pvalue:.4f}")

# Reference group: government (omit dgovt)

# %% Estimate regression model

model_ref_govt = ols('earnings ~ age + education + dself + dprivate',
                     data=data).fit(cov_type='HC1')
print("\nReference: Government")

# %% Display regression results

print(model_ref_govt.summary())
f_test_govt = model_ref_govt.f_test('dself = 0, dprivate = 0')
f_val_govt = f_test_govt.fvalue[0][0] if hasattr(f_test_govt.fvalue, '__getitem__') else f_test_govt.fvalue
print(f"Joint F-test (dself, dprivate): F = {f_val_govt:.2f}, p = {f_test_govt.pvalue:.4f}")

# No intercept (include all indicators)

# %% Estimate regression model

model_noint = ols('earnings ~ age + education + dself + dprivate + dgovt - 1',
                  data=data).fit(cov_type='HC1')
print("\nNo intercept (all indicators included):")

# %% Display regression results

print(model_noint.summary())

# Multiple F-tests with no intercept model
# Test 1: dself = dprivate and dself = dgovt
f_test_noint1 = model_noint.f_test('dself = dprivate, dself = dgovt')
f_val_noint1 = f_test_noint1.fvalue[0][0] if hasattr(f_test_noint1.fvalue, '__getitem__') else f_test_noint1.fvalue
print(f"\nF-test (dself=dprivate, dself=dgovt): F = {f_val_noint1:.2f}, p = {f_test_noint1.pvalue:.4f}")

# Test 2: dself = dprivate and dprivate = dgovt
f_test_noint2 = model_noint.f_test('dself = dprivate, dprivate = dgovt')
f_val_noint2 = f_test_noint2.fvalue[0][0] if hasattr(f_test_noint2.fvalue, '__getitem__') else f_test_noint2.fvalue
print(f"F-test (dself=dprivate, dprivate=dgovt): F = {f_val_noint2:.2f}, p = {f_test_noint2.pvalue:.4f}")

# Summary comparison table
print("\n" + "-" * 70)
print("Comparison of Different Specifications")
print("-" * 70)

spec_comparison = pd.DataFrame({
    'No Indicators': [model_noindic.rsquared, model_noindic.rsquared_adj,
                      np.sqrt(model_noindic.mse_resid), model_noindic.nobs],
    'Ref: Self': [model_ref_self.rsquared, model_ref_self.rsquared_adj,
                  np.sqrt(model_ref_self.mse_resid), model_ref_self.nobs],
    'Ref: Private': [model_ref_private.rsquared, model_ref_private.rsquared_adj,
                     np.sqrt(model_ref_private.mse_resid), model_ref_private.nobs],
    'Ref: Govt': [model_ref_govt.rsquared, model_ref_govt.rsquared_adj,
                  np.sqrt(model_ref_govt.mse_resid), model_ref_govt.nobs],
    'No Intercept': [model_noint.rsquared, model_noint.rsquared_adj,
                     np.sqrt(model_noint.mse_resid), model_noint.nobs]
}, index=['R²', 'Adj R²', 'RMSE', 'N'])

print(spec_comparison.to_string())

# Difference in several means (no other regressors)
print("\n" + "-" * 70)
print("Testing Differences in Means Across Groups")
print("-" * 70)

# Model 1: Drop self-employed as reference

# %% Estimate regression model

model_means1 = ols('earnings ~ dprivate + dgovt', data=data).fit(cov_type='HC1')
print("\nReference: Self-employed")
print(f"  Private sector effect: {model_means1.params['dprivate']:.2f} (SE: {model_means1.bse['dprivate']:.2f})")
print(f"  Government effect: {model_means1.params['dgovt']:.2f} (SE: {model_means1.bse['dgovt']:.2f})")

# Model 2: No intercept

# %% Estimate regression model

model_means2 = ols('earnings ~ dself + dprivate + dgovt - 1', data=data).fit(cov_type='HC1')
print("\nNo intercept (group means):")
print(f"  Self-employed: {model_means2.params['dself']:.2f} (SE: {model_means2.bse['dself']:.2f})")
print(f"  Private sector: {model_means2.params['dprivate']:.2f} (SE: {model_means2.bse['dprivate']:.2f})")
print(f"  Government: {model_means2.params['dgovt']:.2f} (SE: {model_means2.bse['dgovt']:.2f})")

# ANOVA
print("\n" + "-" * 70)
print("ANOVA: Testing Equality of Means Across Worker Types")
print("-" * 70)

# Create categorical variable for worker type
data['typeworker'] = (1 * data['dself'] + 2 * data['dprivate'] + 3 * data['dgovt']).astype(int)

print("\nMeans by worker type:")
means_by_type = data.groupby('typeworker')['earnings'].agg(['mean', 'std', 'count'])
means_by_type.index = ['Self-employed', 'Private', 'Government']
print(means_by_type)

# One-way ANOVA
from scipy.stats import f_oneway

group1 = data[data['typeworker'] == 1]['earnings']
group2 = data[data['typeworker'] == 2]['earnings']
group3 = data[data['typeworker'] == 3]['earnings']

f_stat_anova, p_value_anova = f_oneway(group1, group2, group3)

print(f"\nOne-way ANOVA:")
print(f"  F-statistic: {f_stat_anova:.2f}")
print(f"  p-value: {p_value_anova:.6f}")

# Using statsmodels for detailed ANOVA table

# %% Estimate regression model

model_anova = ols('earnings ~ C(typeworker)', data=data).fit()
from statsmodels.stats.anova import anova_lm
anova_table = anova_lm(model_anova, typ=2)
print("\nDetailed ANOVA table:")
print(anova_table)

print("\nNote: ANOVA F-statistic matches the joint test from regression (with default SEs)")

# Visualization
print("\n" + "-" * 70)
print("Visualizations")
print("-" * 70)

# Figure: Earnings by gender
fig, axes = plt.subplots(1, 2, figsize=(14, 6))

# Panel 1: Box plot by gender
data['Gender'] = data['gender'].map({0: 'Male', 1: 'Female'})
sns.boxplot(x='Gender', y='earnings', data=data, ax=axes[0])
axes[0].set_ylabel('Earnings ($)')
# axes[0].set_title('Earnings Distribution by Gender')  # Removed: redundant with LaTeX caption
# axes[0].grid(True, alpha=0.3)  # Removed: redundant with LaTeX caption

# Panel 2: Box plot by worker type
data['Worker Type'] = data['typeworker'].map({1: 'Self-employed', 2: 'Private', 3: 'Government'})
sns.boxplot(x='Worker Type', y='earnings', data=data, ax=axes[1])
axes[1].set_ylabel('Earnings ($)')
# axes[1].set_title('Earnings Distribution by Worker Type')  # Removed: redundant with LaTeX caption
# axes[1].tick_params(axis='x', rotation=45)  # Removed: redundant with LaTeX caption
axes[1].grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig(os.path.join(IMAGES_DIR, 'ch14_earnings_by_groups.png'), dpi=300, bbox_inches='tight')
print(f"Saved: {os.path.join(IMAGES_DIR, 'ch14_earnings_by_groups.png')}")
plt.close()

# %% Continue analysis

# Figure: Earnings vs education by gender
fig, ax = plt.subplots(figsize=(10, 6))
for gender, label in [(0, 'Male'), (1, 'Female')]:
    subset = data[data['gender'] == gender]
    ax.scatter(subset['education'], subset['earnings'], alpha=0.5, label=label)

    # Add regression line
    z = np.polyfit(subset['education'], subset['earnings'], 1)
    p = np.poly1d(z)
    edu_range = np.linspace(subset['education'].min(), subset['education'].max(), 100)
    ax.plot(edu_range, p(edu_range), linewidth=2)

ax.set_xlabel('Years of Education')
ax.set_ylabel('Earnings ($)')
# ax.set_title('Earnings vs Education by Gender')  # Removed: redundant with LaTeX caption
ax.legend()
ax.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig(os.path.join(IMAGES_DIR, 'ch14_earnings_education_gender.png'), dpi=300, bbox_inches='tight')
print(f"Saved: {os.path.join(IMAGES_DIR, 'ch14_earnings_education_gender.png')}")
plt.close()

# %% Continue analysis

# %% =========== SUMMARY ==========

print("\n" + "=" * 70)
print("CHAPTER 14 SUMMARY")
print("=" * 70)
print("\nKey topics covered:")
print("  1. Single indicator variable regression (difference in means)")
print("  2. Multiple indicator variables with different reference categories")
print("  3. Interaction terms between indicators and continuous variables")
print("  4. Fully interacted models")
print("  5. Separate regressions by groups")
print("  6. ANOVA for testing equality of means")
print("  7. Interpretation of coefficients with indicators")
print("\nKey findings:")
print(f"  - Gender earnings gap: ${diff_means:.2f} (females earn less)")
print(f"  - Returns to education vary by gender (interaction effects)")
print(f"  - Earnings differ significantly across worker types (ANOVA F={f_stat_anova:.2f})")
print("\nAll figures saved to:", IMAGES_DIR)

print("\n" + "=" * 70)
print("END OF CHAPTER 14")
print("=" * 70)
