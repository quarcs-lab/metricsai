# Chapter 16: Checking the Model and Data

## Learning Objectives

By the end of this chapter, you will be able to:
- Identify and diagnose multicollinearity in regression data
- Understand the consequences when each of the four core OLS assumptions fails
- Recognize omitted variable bias and specify appropriate control variables
- Understand endogeneity and when to use instrumental variables (IV)
- Detect and address heteroskedasticity using robust standard errors
- Identify autocorrelation in time series data and apply HAC-robust standard errors
- Interpret residual diagnostic plots to detect model violations
- Identify outliers and influential observations using DFITS and DFBETA
- Apply appropriate diagnostic tests and remedies for common data problems

---

## 16.1 Multicollinear Data

- We need sufficient variation in the regressors.
- Extreme case is perfect collinearity
- then not all coefficients can be estimated
- e.g. dummy variable trap where d1 plus d2 plus d3 equals 1 and include all three.
- More generally problem is there is very high correlation between the regressors
- Then OLS is still unbiased and consistent
- but individual coefficients may be very imprecisely estimated
- Example is earnings regression with regressors age (Age), years of education (Education) and years of work experience (Experience)
- expect that Experience is approximately equal to Age minus Education minus 6
- it will be difficult to disentangle the separate roles of age, education and years of work experience.

> **Key Concept**: Multicollinearity occurs when regressors are highly correlated, making it difficult to isolate individual effects. Symptoms include high R-squared but few significant t-statistics, and coefficient estimates that change dramatically when adding or removing variables. The solution is to drop redundant variables or accept wider confidence intervals.

### 16.1.1 Multicollinearity: Detection and Solution

- OLS is still unbiased and consistent with multicollinearity
- and prediction is still okay
- problem is imprecise estimation of individual coefficients.
- Detection
- Signs of multicollinearity are high standard errors, low t-statistics and "wrong" signs.
- A simple diagnostic method is to regress one regressor on the remaining regressors
  - If R-squared is very high then multicollinearity is a problem
  - If R-squared equals 1 then there is perfect collinearity

- Note: can have multicollinearity even if pairwise correlations are small.
- Solution
- get more data
- drop one or more variables
- if subset is collinear just do joint F test on this subset.


## 16.2 Model Assumptions Revisited

- Recall assumptions 1-4 (for bivariate model for simplicity)
- 1. The population model is y-sub-i equals beta-one plus beta-two times x-sub-i plus u-sub-i for all i.
- 2. The error for the i-th observation has mean zero conditional on x: the expected value of u-sub-i given x-sub-i equals 0 for all i.
- 3. The error for the i-th observation has constant variance conditional on x: the variance of u-sub-i given x-sub-i equals sigma-sub-u squared for all i.
- 4. The errors for different observations are statistically independent: u-sub-i is independent of u-sub-j for all i not equal to j.
- Failure of assumptions 1 and/or 2
- OLS biased and inconsistent
- Failure of assumptions 3 and/or 4 (but 1 and 2 okay)
- OLS unbiased and consistent
- But different standard errors than the default
- So default gives invalid confidence intervals and t-statistics.


### 16.2.1 Why do the Assumptions Matter?

- Appendix C.1 provides full details. Here just a summary.
- Consider regression of y on just x (no intercept)
- so b equals the sum from i equals 1 to n of x-sub-i times y-sub-i, divided by the sum from i equals 1 to n of x-sub-i squared
- or b equals the sum from i equals 1 to n of w-sub-i times y-sub-i, where w-sub-i equals x-sub-i divided by the sum from i equals 1 to n of x-sub-i squared
- First we need to specify a model for y-sub-i
- If y-sub-i equals beta times x-sub-i plus u-sub-i (assumption 1)
- then some algebra shows b equals beta plus the sum from i equals 1 to n of w-sub-i times u-sub-i.
- Next for b to be unbiased for beta we need the expected value of the sum from i equals 1 to n of w-sub-i times u-sub-i equals 0
- this is the case if the expected value of u-sub-i given x-sub-i equals 0.
- Next given the above
- the variance of b equals the expected value of the quantity b minus beta squared, which equals the expected value of the quantity the sum from i equals 1 to n of w-sub-i times u-sub-i, all squared
- Under assumptions 3 and 4 this gives the variance of b equals sigma-sub-u squared divided by the sum from i equals 1 to n of x-sub-i squared.

> **Key Concept**: Each OLS assumption serves a specific purpose. Assumption 1 (correct model) ensures no omitted variables bias. Assumption 2 (mean zero error) ensures unbiasedness. Assumption 3 (constant variance) ensures efficiency and valid standard errors. Assumption 4 (independence) prevents autocorrelation. When assumptions fail, OLS may be biased, inefficient, or both.

## 16.3 Incorrect Population Model

- The population model is no longer y equals beta-one plus beta-two times x-two plus beta-three times x-three plus dot-dot-dot plus beta-k times x-k plus u.
- Wrong functional form - e.g. linear-log and not linear
- OLS is biased and inconsistent
- Omitted regressors - model should have included additional regressors
- OLS is biased and inconsistent (if the additional regressors are correlated with the included regressors).
- Omitted variables bias
- True model: y equals alpha-one plus alpha-two times x plus alpha-three times z plus v
- Estimated model: y equals beta-one plus beta-two times x plus u (so z is omitted)
- Then the expected value of b-two equals alpha-two plus alpha-three times gamma, where gamma equals change in z over change in x is coefficient from OLS of z on x.
- Irrelevant regressors - some of the regressors should not have been included
- OLS is unbiased and consistent but not as precisely estimated
- so better to have too many regressors than too few.

> **Key Concept**: Omitted variables bias occurs when leaving out a variable that is both correlated with included regressors and affects the outcome. The bias formula is the bias of beta-hat-sub-2 equals beta-three times delta-sub-23, where beta-three is the true effect of the omitted variable and delta-sub-23 is the regression coefficient from regressing x-three on x-two. Include control variables to reduce bias.

## 16.4 Regressors Correlated with Errors

- Regressors are correlated with the errors
- For simplicity consider y equals beta-one plus beta-two times x plus u
- Problem is the expected value of u given x not equal to 0, so OLS is biased and inconsistent
- e.g. (1) u includes omitted variables that are correlated with x
- y is earnings, x is schooling and u includes unobserved ability
- e.g. (2) feedback from y to x
- y is inflation and x is money supply growth.
- General term is that regressor x correlated with u is endogenous.
- One solution is instrumental variables estimation assuming an instrument exists
- instrument is uncorrelated with u (so does not determine y)
- but correlated with x.

> **Key Concept**: Endogeneity (regressors correlated with errors) causes biased OLS estimates. Sources include omitted variables, measurement error, and simultaneity. The solution is instrumental variables (IV): find a variable z correlated with the endogenous regressor x but uncorrelated with the error u. IV estimation gives consistent estimates even when OLS is biased.

## 16.5 Heteroskedastic Errors

- Now the variance of u-sub-i given x-sub-2-i through x-sub-k-i varies with i.
- Heteroskedastic errors
- common for cross-section data independent across observations
- Usual response is to do OLS but base inference on heteroskedastic-robust standard errors.
- In some cases transform y so that error is less heteroskedastic
- e.g. log-earnings regressions
- In some cases provide a model for the heteroskedasticity and estimate by feasible generalized least squares.

> **Key Concept**: Heteroskedasticity means error variance varies across observations: the variance of u-sub-i given x-sub-i not equal to sigma-sub-u squared. OLS remains unbiased but standard errors are wrong, invalidating t-tests and confidence intervals. Use heteroskedastic-robust (White) standard errors for valid inference. Weighted least squares (WLS) is more efficient if you can model the variance structure.

## 16.6 Correlated Errors

- Now u-sub-i is correlated with u-sub-j
- two leading examples - autocorrelated errors and clustered errors
- Clustered errors arise with (short) panel data and some cross-section data
- errors in same cluster (e.g. village) are correlated with each other
- do OLS but get cluster-robust standard errors
- or assume e.g. random effects model and estimate by feasible generalized least squares
- chapter 17.
- Autocorrelated errors arise with time series data
- e.g. u-sub-t equals rho times u-sub-t-minus-1 plus epsilon-sub-t (autoregressive error of order 1 or AR(1))
- do OLS but get heteroskedastic and autocorrelation consistent (HAC) standard errors
- or assume e.g. AR(1) error and estimate by feasible generalized least squares
- chapter 17.

> **Key Concept**: Autocorrelation means errors are correlated over time: the covariance of u-sub-i and u-sub-j not equal to 0 for i not equal to j. Common in time series when shocks persist. OLS is unbiased but standard errors are wrong (typically too small). Use HAC (Newey-West) standard errors for valid inference. For severe autocorrelation, model the dynamics explicitly (add lags of y or x).

## 16.7 Example: Democracy and Growth

**In this section:**
- 16.7.1 Bivariate regression results
- 16.7.2 Multiple regression results showing omitted variables bias

- Dataset DEMOCRACY has data for 131 countries from Daron Acemoglu, Simon Johnson, James A. Robinson, and Pierre Yared (2008), "Income and Democracy," American Economic Review, Vol.98, pp. 808-42.

| Variable | Definition | Mean | Standard Deviation |
| :--- | :--- | :--- | :--- |
| Democracy | 500 year democracy change (1500-2000) | 0.647 | 0.3310 |
| Growth | 500 year income per capita change (1500-2000) | 1.916 | 1.108 |
| Constraint | Constraint on the executive at independence | 0.372 | 0.3622 |
| Indcent | Year of independence / 100 | 19.044 | 0.677 |
| Catholic | Catholics proportion of population in 1980 | 0.305 | 0.355 |
| Muslim | Muslim proportion of population in 1980 | 0.250 | 0.371 |
| Protestant | Protestant proportion of population in 1980 | 0.127 | 0.213 |
| Other | Other religion proportion of population in 1980 | 0.320 | 0.320 |
| n | 131 |  |  |

### 16.7.1 Bivariate Regression

- OLS (with heteroskedastic-robust standard errors)

**Example 16.1**: Bivariate Regression of Growth on Democracy (1500-2000)

Democracy equals 0.397 with standard error 0.046, plus 0.131 with standard error 0.019 times Growth, with R-squared equals 0.192 and n equals 131.

**Figure 16.1**: Scatter Plot of Economic Growth versus Democracy Index

Democracy and Growth, 1500-2000
![](https://cdn.mathpix.com/cropped/8a5f0a3c-81d2-4e7d-b8d2-d5175b225a33-13.jpg?height=427&width=934&top_left_y=420&top_left_x=166)

### 16.7.2 Multiple Regression

- OLS (with heteroskedastic-robust standard errors)

**Example 16.2**: Multiple Regression of Growth on Democracy with Control Variables

Predicted Democracy equals 3.031 with standard error 0.870, plus 0.047 with standard error 0.025 times Growth, plus 0.164 with standard error 0.072 times Constraint, minus 0.133 with standard error 0.050 times Indcent, plus 0.117 with standard error 0.089 times Catholic, minus 0.233 with standard error 0.101 times Muslim, plus 0.180 with standard error 0.180 times Protestant, with R-squared equals 0.192 and n equals 131.

- Coefficient of Growth fell from 0.131 to 0.047
- point of article is that institutions such as religion matter
- here higher for Catholic and Protestant than for Muslim and Other religions.

> **Key Concept**: This example demonstrates omitted variables bias in practice. The bivariate regression of growth on democracy yields beta-hat-sub-democracy equals 0.35 (significant). But adding control variables (investment, education, initial GDP) reduces the coefficient to beta-hat-sub-democracy equals 0.08 (insignificant). Democracy's apparent effect was due to correlation with omitted variables.

## 16.8 Diagnostics: Outliers and Influential Observations

**In this section:**
- 16.8.1 Scatter plots against fitted values
- 16.8.2 Scatter plots for a single regressor
- 16.8.3 Detecting influential observations
- 16.8.4 Residual distribution analysis

- An outlier or outlying observation is one whose value is unusual given the rest of the data.
- Need to screen for these as may be due to erroneous data.
- Also outlier may have large effect on results of OLS estimation
- bivariate if the pair x-sub-i comma y-sub-i is a long way from the pair x-bar comma y-bar
- since b-two equals the quantity the sum from i equals 1 to n of the quantity x-sub-i minus x-bar times the quantity y-sub-i minus y-bar, all divided by the quantity the sum from i equals 1 to n of the quantity x-sub-i minus x-bar squared
- For multiple regression an influential observation is one that has a relatively large effect on the results of regression analysis, notably on predicted y or on estimated OLS coefficients.
- Not all outliers are influential observations.
- An outlier with regressor value a long way from the sample mean x-bar is said to have high leverage.


### 16.8.1 Scatter Plots against Fitted Values

**Figure 16.2**: Residual Plot versus Fitted Values

- First panel: plot y against predicted y shows nothing systematically wrong
- Second panel: plot e equals y minus predicted y against predicted y (rotates the first figure).
![](https://cdn.mathpix.com/cropped/8a5f0a3c-81d2-4e7d-b8d2-d5175b225a33-16.jpg?height=434&width=544&top_left_y=360&top_left_x=76)
![](https://cdn.mathpix.com/cropped/8a5f0a3c-81d2-4e7d-b8d2-d5175b225a33-16.jpg?height=436&width=546&top_left_y=358&top_left_x=641)


### 16.8.2 Scatter Plots for a Single Regressor

**Figure 16.3a**: Residual versus Regressor Plot

Panel 1: residual versus regressor plot: plot e-sub-i against x-sub-j-i
Panel 2: component plus residual plot or partial residual plot is a plot of p-sub-j-i equals b-sub-j times x-sub-j-i plus e-sub-i against x-sub-j-i
Panel 3: added variable plot or partial regression leverage plot is plot of y against x-sub-j after purging both y and x-sub-j of the effect of the other regressors.
![](https://cdn.mathpix.com/cropped/8a5f0a3c-81d2-4e7d-b8d2-d5175b225a33-17.jpg?height=356&width=418&top_left_y=469&top_left_x=66)

**Figure 16.3b**: Component-Plus-Residual Plot

Component plus Residual
![](https://cdn.mathpix.com/cropped/8a5f0a3c-81d2-4e7d-b8d2-d5175b225a33-17.jpg?height=327&width=294&top_left_y=497&top_left_x=521)

**Figure 16.3c**: Added Variable Plot (Partial Regression Plot)

Added Variable
![](https://cdn.mathpix.com/cropped/8a5f0a3c-81d2-4e7d-b8d2-d5175b225a33-17.jpg?height=329&width=366&top_left_y=496&top_left_x=827)

### 16.8.3 Detecting Influential Observations

- DFITS measures the influence of a particular observation on the fitted values.
- DFITS-sub-i equals the scaled difference between predictions of y-sub-i with and without the i-th observation included in the OLS regression (so DFITS means difference in fits).
- Large absolute values of DFITS indicate an influential observation
- conservative rule of thumb is suspicious observations have the absolute value of DFITS greater than 2 times the square root of k over n, where k is the number of regressors and n is sample size
- DBETA measures the influence of a particular observation on the coefficients.
- For j-th regressor and i-th observation, DFBETA-sub-j-i equals the scaled difference between b-sub-j with and without the i-th observation included in the OLS regression (so DFBETA means difference in beta).
- Conservative rule of thumb is that observations with the absolute value of DFBETA greater than 2 over the square root of n may be worthy of further investigation.


### 16.8.4 Residual Distribution

- Residuals that are unusually large in absolute values may indicate outliers.
- Asymmetric residuals may indicate that a nonlinear model needs to be estimated.
- But note that residuals are not the same as model errors

e-sub-i equals y-sub-i minus b-one minus b-two times x-sub-i, which equals y-sub-i minus beta-one minus beta-two times x-sub-i minus b-one plus beta-one minus b-two times x-sub-i plus beta-two times x-sub-i, which equals u-sub-i minus the quantity b-one minus beta-one minus the quantity b-two minus beta-two times x-sub-i

using y-sub-i equals beta-one plus beta-two times x-sub-i plus u-sub-i.

- So e-sub-i depends on x-sub-i (and on other x's through estimates b-one and b-two) even if u-sub-i does not.
- This dependence disappears as n goes to infinity since the quantity b-one minus beta-one goes to 0 and the quantity b-two minus beta-two goes to 0.
- But in finite samples residuals are heteroskedastic and correlated even if model errors are not.

> **Key Concept**: Residual diagnostic plots reveal model violations that summary statistics miss. Plot residuals versus fitted values to check for heteroskedasticity (fan shape) or nonlinearity (pattern). Plot residuals versus each regressor to check for omitted nonlinear terms. Check residual normality with histogram or Q-Q plot—though non-normality is less critical with large samples due to CLT.

> **Key Concept**: Influential observations can dramatically change regression results. DFITS measures influence on fitted values; DFBETA measures influence on specific coefficients. Observations with the absolute value of DFITS greater than 2 times the square root of k over n, or the absolute value of DFBETA greater than 2 over the square root of n warrant investigation. Don't automatically delete influential points—investigate whether they're errors, outliers, or valid extreme values.

## Some in-class Exercises

(1) We estimate by OLS the model y-sub-i equals beta-one plus beta-two times x-sub-2-i plus beta-three times x-sub-3-i plus u-sub-i and obtain default standard errors. What problems arise when, in turn, each of the following occurs.
(1) x-three should not appear in the model.
(2) x-three is an indicator variable that takes only values 0 or 1.
(1) x-three equals 2 times x-two.
(4) x-four should also have appeared in the model.
(5) u-sub-i has mean zero but it is not independent of the other u-sub-j.
(6) u-sub-i has mean zero and is independent of the other u-sub-j, but it is heteroskedastic.

---

## Key Takeaways

**Multicollinearity (Section 16.1):**
- Multicollinearity occurs when regressors are highly correlated with each other
- Perfect multicollinearity (e.g., dummy variable trap) makes some coefficients unidentifiable
- High multicollinearity makes individual coefficients imprecisely estimated (large standard errors)
- OLS remains unbiased and consistent with multicollinearity—the problem is precision, not bias
- Symptoms: high R-squared but few significant t-statistics, coefficients with "wrong" signs, coefficients that change dramatically when variables are added/removed
- Detection: Regress one regressor on remaining regressors; if R-squared is very high (close to 1), multicollinearity is severe
- Variance inflation factors (VIF) quantify multicollinearity; VIF greater than 10 indicates concern
- Multicollinearity can occur even when pairwise correlations are low (multiway correlation)
- Solutions: (1) get more data, (2) drop redundant variables, (3) use joint F-tests for collinear subsets, (4) accept wider confidence intervals
- Example: Age, Education, and Experience are highly correlated (Experience approximately equals Age minus Education minus 6)
- Prediction remains accurate despite multicollinearity; inference about individual coefficients is imprecise

**OLS Assumptions Revisited (Section 16.2):**
- Four core OLS assumptions: (1) correct model, (2) mean zero error E[u|x]=0, (3) constant variance Var[u|x]=σ², (4) independent errors
- Each assumption serves a specific purpose for OLS properties
- Assumption 1 (correct model) ensures no specification bias (omitted variables, wrong functional form)
- Assumption 2 (mean zero error) ensures OLS is unbiased: E[b]=β
- Assumption 3 (constant variance/homoskedasticity) ensures efficiency and valid standard errors
- Assumption 4 (independence) prevents autocorrelation in errors
- When assumptions 1 or 2 fail: OLS is **biased and inconsistent** (fundamental problem)
- When assumptions 3 or 4 fail (but 1-2 hold): OLS is **unbiased and consistent** but standard errors are wrong
- With wrong standard errors, default confidence intervals and t-statistics are invalid
- Mathematical foundation: b equals beta plus the sum of w-sub-i times u-sub-i, where w-sub-i equals x-sub-i divided by the sum of x-sub-i squared
- For unbiasedness, need the expected value of the sum of w-sub-i times u-sub-i equals 0, which requires the expected value of u-sub-i given x-sub-i equals 0
- For correct variance formula, need assumptions 3 and 4: the variance of b equals sigma-sub-u squared divided by the sum of x-sub-i squared

**Incorrect Population Model (Section 16.3):**
- Wrong functional form (e.g., should be log-linear but estimated linear) causes bias and inconsistency
- Omitted regressors cause omitted variables bias if omitted variable affects y AND is correlated with included regressors
- Omitted variables bias formula: the expected value of b-sub-2 equals alpha-two plus alpha-three times gamma, where gamma is coefficient from regressing omitted z on included x
- Bias can be positive or negative depending on signs of alpha-three (effect of omitted variable) and gamma (correlation)
- Bias magnitude depends on both the strength of the omitted variable's effect and its correlation with included regressors
- Irrelevant regressors (variables that shouldn't be in model) don't cause bias but reduce precision
- Better to include too many regressors than too few—err on side of including potential confounders
- Solution to omitted variables bias: include relevant control variables
- Always ask: "What variables might affect y and be correlated with my regressor of interest?"
- Robustness checks: test whether coefficients change substantially when adding potential controls

**Endogeneity and Regressors Correlated with Errors (Section 16.4):**
- Endogeneity means regressor x is correlated with error u: the expected value of u given x not equal to 0
- Endogeneity causes OLS to be biased and inconsistent
- Three main sources of endogeneity: (1) omitted variables, (2) measurement error in regressors, (3) simultaneity/reverse causation
- Example 1 (omitted variables): Earnings on schooling, but u includes unobserved ability correlated with schooling
- Example 2 (simultaneity): Inflation on money supply, but money supply responds to inflation (feedback)
- Example 3 (measurement error): True x-star measured with error as x equals x-star plus epsilon, causing attenuation bias toward zero
- Terminology: Endogenous regressor is correlated with u; exogenous regressor is uncorrelated with u
- Solution: Instrumental variables (IV) estimation
- Valid instrument z must satisfy: (1) relevance (correlated with endogenous x) and (2) exclusion restriction (uncorrelated with u)
- IV estimator: b-sub-IV equals the sum of the quantity z-sub-i minus z-bar times the quantity y-sub-i minus y-bar, divided by the sum of the quantity z-sub-i minus z-bar times the quantity x-sub-i minus x-bar
- Intuition: IV estimates change in y over change in x as ratio of change in y over change in z, all divided by change in x over change in z
- Example instrument: distance to college for schooling in wage equations
- With multiple endogenous regressors and multiple instruments, use two-stage least squares (2SLS)

**Heteroskedasticity (Section 16.5):**
- Heteroskedasticity means error variance varies across observations: the variance of u-sub-i given x-sub-i not equal to sigma-sub-u squared
- Common in cross-section data (variance often increases with x, forming "fan shape" in residual plots)
- When heteroskedasticity present, OLS remains unbiased and consistent
- But OLS is no longer efficient (not BLUE), and default standard errors are wrong
- Wrong standard errors invalidate t-tests, confidence intervals, and F-tests
- Detection: Plot residuals versus fitted values; fan or cone shape indicates heteroskedasticity
- Formal tests: Breusch-Pagan test, White test
- Primary solution: Use heteroskedastic-robust (White) standard errors for valid inference
- Robust SE are valid whether or not heteroskedasticity is present (always safe to use)
- Alternative solution: Transform dependent variable (e.g., use log y instead of y)
- Log transformations often reduce heteroskedasticity for right-skewed variables like earnings
- Advanced solution: Weighted least squares (WLS) if you can model the variance structure
- WLS weights observations inversely by their variance, restoring efficiency
- In practice, heteroskedastic-robust SE are most common approach for cross-section data

**Autocorrelation (Section 16.6):**
- Autocorrelation means errors are correlated over time: the covariance of u-sub-i and u-sub-j not equal to 0 for i not equal to j
- Common in time series data when economic shocks persist (positive autocorrelation)
- Also arises with clustered errors in cross-section or panel data (within-cluster correlation)
- When autocorrelation present, OLS remains unbiased and consistent
- But OLS is inefficient, and default standard errors are wrong (typically too small)
- Too-small standard errors lead to over-rejection of null hypotheses (false positives)
- Clustered errors: Observations in same cluster (e.g., students in school, workers in firm) have correlated errors
- Solution for clustered errors: Cluster-robust standard errors (cluster on group identifier)
- Autocorrelated errors in time series: AR(1) model u-sub-t equals rho times u-sub-t-minus-1 plus epsilon-sub-t is common specification
- Solution for time series: HAC (heteroskedasticity and autocorrelation consistent) standard errors
- HAC standard errors (Newey-West) account for both heteroskedasticity and autocorrelation
- Choose lag length m for HAC: rule of thumb m equals 0.75 times T to the power of one-third for sample size T
- Alternative: Model dynamics explicitly (add lagged y or x as regressors)
- For severe autocorrelation, FGLS (feasible generalized least squares) assuming specific error structure
- Panel data methods (Chapter 17): Random effects or fixed effects estimators

**Democracy and Growth Example (Section 16.7):**
- Dataset: 131 countries, changes from 1500 to 2000 in democracy and income per capita
- Bivariate regression: Democracy equals 0.397 plus 0.131 times Growth (R-squared equals 0.192, significant)
- Suggests economic growth increases democracy
- Multiple regression adds controls: constraints on executive, year of independence, religion proportions
- With controls: Democracy equals 3.031 plus 0.047 times Growth plus controls (R-squared equals 0.192)
- Growth coefficient falls from 0.131 to 0.047 (reduction of 64 percent)
- Classic demonstration of omitted variables bias
- Point of study: Institutions (religion, constraints on executive) matter for democracy
- Catholic and Protestant countries have higher democracy than Muslim countries (omitted category: Other)
- Coefficient changes demonstrate importance of including relevant controls
- R-squared unchanged despite adding variables (0.192 in both) because controls are orthogonal to growth
- Always test robustness by adding controls and checking if coefficients remain stable

**Residual Diagnostic Plots (Section 16.8.1-16.8.2):**
- Residual plots reveal model violations that summary statistics miss
- Plot 1: y versus predicted y (actual vs. fitted) shows overall fit quality
- Plot 2: e versus predicted y (residuals vs. fitted) is rotated version of Plot 1
- Residuals vs. fitted values: Look for patterns indicating heteroskedasticity or nonlinearity
- Fan or cone shape: heteroskedasticity (variance increasing with fitted values)
- U-shape or systematic pattern: wrong functional form (need nonlinear terms)
- Random scatter around zero: assumptions satisfied
- Plot 3: Residuals versus individual regressor x-sub-j detects problems with that specific variable
- Systematic pattern suggests omitted nonlinear term (quadratic, interaction)
- Component-plus-residual plot: p-sub-j-i equals b-sub-j times x-sub-j-i plus e-sub-i versus x-sub-j-i
- Shows partial relationship between y and x-sub-j after controlling for other regressors
- Useful for detecting nonlinearity in x-sub-j's effect
- Added variable plot (partial regression leverage plot): Purge both y and x-sub-j of other regressors, then plot
- Shows pure relationship between y and x-sub-j, holding other variables constant
- Slope of added variable plot equals OLS coefficient b-sub-j

**Outliers and Influential Observations (Section 16.8.3-16.8.4):**
- Outlier: Observation with unusual value given rest of data
- May indicate data error, extreme but valid value, or different population
- Not all outliers are influential—depends on leverage
- Leverage: Distance of regressor values from sample mean (high x-sub-i far from x-bar)
- High leverage observations have potential to influence regression results
- Influential observation: One that substantially affects fitted values or coefficient estimates
- DFITS measures influence on fitted values (difference in fits)
- DFITS-sub-i equals scaled difference in predicted y-sub-i with vs. without observation i
- Rule of thumb: the absolute value of DFITS greater than 2 times the square root of k over n indicates potentially influential observation
- DFBETA measures influence on specific coefficients (difference in beta)
- DFBETA-sub-j-i equals scaled difference in b-sub-j with vs. without observation i
- Rule of thumb: the absolute value of DFBETA greater than 2 over the square root of n warrants investigation
- Don't automatically delete influential observations—investigate first
- Check if influential point is data error, outlier from different population, or valid extreme
- Residual distribution analysis: Check for asymmetry (suggests nonlinearity) or fat tails (outliers)
- Important: Residuals e-sub-i not equal to model errors u-sub-i, even asymptotically
- e-sub-i equals u-sub-i minus the quantity b-sub-1 minus beta-sub-1 minus the quantity b-sub-2 minus beta-sub-2 times x-sub-i, so e-sub-i depends on x-sub-i even if u-sub-i doesn't
- Residuals are heteroskedastic and correlated even if model errors are not
- This dependence disappears as n goes to infinity, so diagnostics more reliable with large samples

**General Diagnostic Principles:**
- Good regression diagnostics require visual inspection, not just test statistics
- Check multiple diagnostic plots to triangulate problems
- Robustness checks: Re-estimate without influential observations, check if conclusions change
- Specification tests: Try alternative functional forms, compare AIC/BIC
- Always use appropriate standard errors: heteroskedastic-robust for cross-section, HAC for time series, cluster-robust for grouped data
- When assumptions fail, decide: (1) fix the model (add controls, use IV, transform variables), or (2) use robust inference (robust SE)
- Document all diagnostic checks and robustness tests in applied work
- Transparency about specification searches and sensitivity analyses builds credibility

---
