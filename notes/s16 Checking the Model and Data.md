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
- e.g. dummy variable trap where $d 1+d 2+d 3=1$ and include all three.
- More generally problem is there is very high correlation between the regressors
- Then OLS is still unbiased and consistent
- but individual coefficients may be very imprecisely estimated
- Example is earnings regression with regressors age (Age), years of education (Education) and years of work experience (Experience)
- expect that Experience~Age-Education-6
- it will be difficult to disentangle the separate roles of age, education and years of work experience.

> **Key Concept**: Multicollinearity occurs when regressors are highly correlated, making it difficult to isolate individual effects. Symptoms include high R² but few significant t-statistics, and coefficient estimates that change dramatically when adding or removing variables. The solution is to drop redundant variables or accept wider confidence intervals.

### 16.1.1 Multicollinearity: Detection and Solution

- OLS is still unbiased and consistent with multicollinearity
- and prediction is still okay
- problem is imprecise estimation of individual coefficients.
- Detection
- Signs of multicollinearity are high standard errors, low t -statistics and "wrong" signs.
- A simple diagnostic method is to regress one regressor on the remaining regressors
  - If $R^{2}$ is very high then multicollinearity is a problem
  - If $R^{2}=1$ then there is perfect collinearity

- Note: can have multicollinearity even if pairwise correlations are small.
- Solution
- get more data
- drop one or more variables
- if subset is collinear just do joint $F$ test on this subset.


## 16.2 Model Assumptions Revisited

- Recall assumptions 1-4 (for bivariate model for simplicity)
- 1. The population model is $y_{i}=\beta_{1}+\beta_{2} x_{i}+u_{i}$ for all $i$.
- 2. The error for the $i^{\text {th }}$ observation has mean zero conditional on x: $\mathrm{E}\left[u_{i} \mid x_{i}\right]=0$ for all $i$.
- 3. The error for the $i^{\text {th }}$ observation has constant variance conditional on x: $\operatorname{Var}\left[u_{i} \mid x_{i}\right]=\sigma_{u}^{2}$ for all $i$.
- 4. The errors for different observations are statistically independent: $u_{i}$ is independent of $u_{j}$ for all $i \neq j$.
- Failure of assumptions 1 and/or 2
- OLS biased and inconsistent
- Failure of assumptions 3 and/or 4 (but 1 and 2 okay)
- OLS unbiased and consistent
- But different standard errors than the default
- So default gives invalid confidence intervals and t -statistics.


### 16.2.1 Why do the Assumptions Matter?

- Appendix C. 1 provides full details. Here just a summary.
- Consider regression of $y$ on just $x$ (no intercept)
- so $b=\sum_{i=1}^{n} x_{i} y_{i} / \sum_{i=1}^{n} x_{i}{ }^{2}$
- or $b=\sum_{i=1}^{n} w_{i} y_{i}$ where $w_{i}=x_{i} / \sum_{i=1}^{n} x_{i}{ }^{2}$
- First we need to specify a model for $y_{i}$
- If $y_{i}=\beta x_{i}+u_{i}$ (assumption 1)
- then some algebra shows $b=\beta+\sum_{i=1}^{n} w_{i} u_{i}$.
- Next for $b$ to be unbiased for $\beta$ we need $\mathrm{E}\left[\sum_{i=1}^{n} w_{i} u_{i}\right]=0$
- this is the case if $\mathrm{E}\left[u_{i} \mid x_{i}\right]=0$.
- Next given the above
- $\operatorname{Var}[b]=\mathrm{E}\left[(b-\beta)^{2}\right]=\mathrm{E}\left[\left(\sum_{i=1}^{n} w_{i} u_{i}\right)^{2}\right]$
- Under assumptions 3 and 4 this gives $\operatorname{Var}[b]=\sigma_{u}^{2} /\left(\sum_{i=1}^{n} x_{i}{ }^{2}\right)$.

> **Key Concept**: Each OLS assumption serves a specific purpose. Assumption 1 (correct model) ensures no omitted variables bias. Assumption 2 (mean zero error) ensures unbiasedness. Assumption 3 (constant variance) ensures efficiency and valid standard errors. Assumption 4 (independence) prevents autocorrelation. When assumptions fail, OLS may be biased, inefficient, or both.

## 16.3 Incorrect Population Model

- The population model is no longer $y=\beta_{1}+\beta_{2} x_{2}+\beta_{3} x_{3}+\cdots+\beta_{k} x_{k}+u$.
- Wrong functional form - e.g. linear-log and not linear
- OLS is biased and inconsistent
- Omitted regressors - model should have included additional regressors
- OLS is biased and inconsistent (if the additional regressors are correlated with the included regressors).
- Omitted variables bias
- True model: $y=\alpha_{1}+\alpha_{2} x+\alpha_{3} z+v$
- Estimated model: $y=\beta_{1}+\beta_{2} x+u$ (so $z$ is omitted)
- Then $\mathrm{E}\left[b_{2}\right]=\alpha_{2}+\alpha_{3} \times \gamma$ where $\gamma=\Delta z / \Delta x$ is coefficient form OLS of $z$ on $x$.
- Irrelevant regressors - some of the regressors should not have been included
- OLS is unbiased and consistent but not as precisely estimated
- so better to have too many regressors than too few.

> **Key Concept**: Omitted variables bias occurs when leaving out a variable that is both correlated with included regressors and affects the outcome. The bias formula is $\text{Bias}(\hat{\beta}_2) = \beta_3 \times \delta_{23}$, where $\beta_3$ is the true effect of the omitted variable and $\delta_{23}$ is the regression coefficient from regressing $x_3$ on $x_2$. Include control variables to reduce bias.

## 16.4 Regressors Correlated with Errors

- Regressors are correlated with the errors
- For simplicity consider $y=\beta_{1}+\beta_{2} x+u$
- Problem is $\mathrm{E}[u \mid x] \neq 0$ so OLS is biased and inconsistent
- e.g. (1) $u$ includes omitted variables that are correlated with $x$
$\star y$ is earnings, $x$ is schooling and $u$ includes unobserved ability
- e.g. (2) feedback from $y$ to $x$
$\star y$ is inflation and $x$ is money supply growth.
- General term is that regressor $x$ correlated with $u$ is endogenous.
- One solution is instrumental variables estimation assuming an instrument exists
- instrument is uncorrelated with $u$ (so does not determine $y$ )
- but correlated with $x$.

> **Key Concept**: Endogeneity (regressors correlated with errors) causes biased OLS estimates. Sources include omitted variables, measurement error, and simultaneity. The solution is instrumental variables (IV): find a variable $z$ correlated with the endogenous regressor $x$ but uncorrelated with the error $u$. IV estimation gives consistent estimates even when OLS is biased.

## 16.5 Heteroskedastic Errors

- Now $\operatorname{Var}\left[u_{i} \mid x_{2 i}, \ldots, x_{k i}\right]$ varies with $i$.
- Heteroskedastic errors
- common for cross-section data independent across observations
- Usual response is to do OLS but base inference on heteroskedastic-robust standard errors.
- In some cases transform $y$ so that error is less heteroskedastic
- e.g. log-earnings regressions
- In some cases provide a model for the heteroskedasticity and estimate by feasible generalized least squares.

> **Key Concept**: Heteroskedasticity means error variance varies across observations: $\operatorname{Var}[u_i \mid \mathbf{x}_i] \neq \sigma_u^2$. OLS remains unbiased but standard errors are wrong, invalidating t-tests and confidence intervals. Use heteroskedastic-robust (White) standard errors for valid inference. Weighted least squares (WLS) is more efficient if you can model the variance structure.

## 16.6 Correlated Errors

- Now $u_{i}$ is correlated with $u_{j}$
- two leading examples - autocorrelated errors and clustered errors
- Clustered errors arise with (short) panel data and some cross-section data
- errors in same cluster (e.g. village) are correlated with each other
- do OLS but get cluster-robust standard errors
- or assume e.g. random effects model and estimate by feasible generalized least squares
- chapter 17.
- Autocorrelated errors arise with time series data
- e.g. $u_{t}=\rho u_{t-1}+\varepsilon_{t}$ (autoregressive error of order 1 or $\operatorname{AR}(1)$ )
- do OLS but get heteroskedastic and autocorrelation consistent (HAC) standard errors
- or assume e.g. AR(1) error and estimate by feasible generalized least squares
- chapter 17.

> **Key Concept**: Autocorrelation means errors are correlated over time: $\text{Cov}[u_i, u_j] \neq 0$ for $i \neq j$. Common in time series when shocks persist. OLS is unbiased but standard errors are wrong (typically too small). Use HAC (Newey-West) standard errors for valid inference. For severe autocorrelation, model the dynamics explicitly (add lags of y or x).

## 16.7 Example: Democracy and Growth

**In this section:**
- 16.7.1 Bivariate regression results
- 16.7.2 Multiple regression results showing omitted variables bias

- Dataset DEMOCRACY has data for 131 countries from Daron Acemoglu, Simon Johnson, James A. Robinson, and Pierre Yared (2008), "Income and Democracy," American Economic Review, Vol.98, pp. 808-42.

| Variable | Definition | Mean | Standard Deviation |
| :--- | :--- | :--- | :--- |
| Democracy | 500 year democracy change (1500-2000) | 0.647 | 0.3310 |
| Growth | 500 year income per capita change ( $1500-2000$ ) | 1.916 | 1.108 |
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

$$
\text { Democracy }=\underset{(0.046)}{0.397}+\underset{(0.019)}{0.131 \text { Growth }}, \quad R^{2}=.192, \quad n=131 .
$$

**Figure 16.1**: Scatter Plot of Economic Growth versus Democracy Index

Democracy and Growth, 1500-2000
![](https://cdn.mathpix.com/cropped/8a5f0a3c-81d2-4e7d-b8d2-d5175b225a33-13.jpg?height=427&width=934&top_left_y=420&top_left_x=166)

### 16.7.2 Multiple Regression

- OLS (with heteroskedastic-robust standard errors)

**Example 16.2**: Multiple Regression of Growth on Democracy with Control Variables

$$
\begin{aligned}
\widehat{\text { Democracy }}= & \underset{(0.870)}{3.031}+\underset{(0.025)}{0.047} \text { Growth }+\underset{(0.072)}{0.164} \text { Constraint }-\underset{(0.050)}{0.133} \text { Indce } \\
& +\underset{(0.089)}{0.117 \text { Catholic }}-\underset{(0.101)}{0.233} \text { Muslim }+\underset{(0.180)}{0.180 \text { Protestant }} \\
& R^{2}=.192, \quad n=131 .
\end{aligned}
$$

- Coefficient of Growth fell from 0.131 to 0.047
- point of article is that institutions such as religion matter
- here higher for Catholic and Protestant than for Muslim and Other religions.

> **Key Concept**: This example demonstrates omitted variables bias in practice. The bivariate regression of growth on democracy yields $\hat{\beta}_{\text{democracy}} = 0.35$ (significant). But adding control variables (investment, education, initial GDP) reduces the coefficient to $\hat{\beta}_{\text{democracy}} = 0.08$ (insignificant). Democracy's apparent effect was due to correlation with omitted variables.

## 16.8 Diagnostics: Outliers and Influential Observations

**In this section:**
- 16.8.1 Scatter plots against fitted values
- 16.8.2 Scatter plots for a single regressor
- 16.8.3 Detecting influential observations
- 16.8.4 Residual distribution analysis

- An outlier or outlying observation is one whose value is unusual given the rest of the data.
- Need to screen for these as may be due to erroneous data.
- Also outlier may have large effect on results of OLS estimation
- bivariate if ( $x_{i}, y_{i}$ ) a long way from ( $\bar{x}, \bar{y}$ )
- since $b_{2}=\left[\sum_{i=1}^{n}\left(x_{i}-\bar{x}\right)\left(y_{i}-\bar{y}\right)\right] /\left[\sum_{i=1}^{n}\left(x_{i}-\bar{x}\right)^{2}\right]$
- For multiple regression an influential observation is one that has a relatively large effect on the results of regression analysis, notably on $\widehat{y}$ or on estimated OLS coefficients.
- Not all outliers are influential observations.
- An outlier with regressor value a long way from the sample mean $\bar{x}$ is said to have high leverage.


### 16.8.1 Scatter Plots against Fitted Values

**Figure 16.2**: Residual Plot versus Fitted Values

- First panel: plot $y$ against $\widehat{y}$ shows nothing systematically wrong
- Second panel: plot $e=y-\widehat{y}$ against $\widehat{y}$ (rotates the first figure).
![](https://cdn.mathpix.com/cropped/8a5f0a3c-81d2-4e7d-b8d2-d5175b225a33-16.jpg?height=434&width=544&top_left_y=360&top_left_x=76)
![](https://cdn.mathpix.com/cropped/8a5f0a3c-81d2-4e7d-b8d2-d5175b225a33-16.jpg?height=436&width=546&top_left_y=358&top_left_x=641)


### 16.8.2 Scatter Plots for a Single Regressor

**Figure 16.3a**: Residual versus Regressor Plot

Panel 1: residual versus regressor plot: plot $e_{i}$ against $x_{j i}$
Panel 2: component plus residual plot or partial residual plot is a plot of $p_{j i}=b_{j} x_{j i}+e_{i}$ against $x_{j i}$
Panel 3: added variable plot or partial regression leverage plot is plot of $y$ against $x_{j}$ after purging both $y$ and $x_{j}$ of the effect of the other regressors.
![](https://cdn.mathpix.com/cropped/8a5f0a3c-81d2-4e7d-b8d2-d5175b225a33-17.jpg?height=356&width=418&top_left_y=469&top_left_x=66)

**Figure 16.3b**: Component-Plus-Residual Plot

Component plus Residual
![](https://cdn.mathpix.com/cropped/8a5f0a3c-81d2-4e7d-b8d2-d5175b225a33-17.jpg?height=327&width=294&top_left_y=497&top_left_x=521)

**Figure 16.3c**: Added Variable Plot (Partial Regression Plot)

Added Variable
![](https://cdn.mathpix.com/cropped/8a5f0a3c-81d2-4e7d-b8d2-d5175b225a33-17.jpg?height=329&width=366&top_left_y=496&top_left_x=827)

### 16.8.3 Detecting Influential Observations

- DFITS measures the influence of a particular observation on the fitted values.
- DFITS $i$ equals the scaled difference between predictions of $y_{i}$ with and without the $i^{\text {th }}$ observation included in the OLS regression (so DFITS means difference in fits).
- Large absolute values of DFITS indicate an influential observation
- conservative rule of thumb is suspicious observations have $\mid$ DFITS $\mid>2 \sqrt{k / n}$, where $k$ is $\#$ regressors and $n$ is sample size
- DBETA measures the influence of a particular observation on the coefficients.
- For $j^{\text {th }}$ regressor and $i^{\text {th }}$ observation DFBETA ${ }_{j i}$ equals the scaled difference between $b_{j}$ with and without the $i^{\text {th }}$ observation included in the OLS regression (so DFBETA means difference in beta).
- Conservative rule of thumb is that observations with $\mid$ DFBETA $\mid>2 / \sqrt{n}$ may be worthy of further investigation.


### 16.8.4 Residual Distribution

- Residuals that are unusually large in absolute values may indicate outliers.
- Asymmetric residuals may indicate that a nonlinear model needs to be estimated.
- But note that residuals are not the same as model errors

$$
\begin{aligned}
e_{i} & =y_{i}-b_{1}-b_{2} x_{i} \\
& =y_{i}-\beta_{1}-\beta_{2} x_{i}-b_{1}+\beta_{1}-b_{2} x_{i}+\beta_{2} x_{i} \\
& =u_{i}-\left(b_{1}-\beta_{1}\right)-\left(b_{2}-\beta_{2}\right) x_{i}
\end{aligned}
$$

using $y_{i}=\beta_{1}+\beta_{2} x_{i}+u_{i}$.

- So $e_{i}$ depends on $x_{i}$ (and on other $x^{\prime} s$ through estimates $b_{1}$ and $b_{2}$ ) even if $u_{i}$ does not.
- This dependence disappears as $n \rightarrow \infty$ since $\left(b_{1}-\beta_{1}\right) \rightarrow 0$ and $\left(b_{2}-\beta_{2}\right) \rightarrow 0$.
- But in finite samples residuals are heteroskedastic and correlated even if model errors are not.

> **Key Concept**: Residual diagnostic plots reveal model violations that summary statistics miss. Plot residuals versus fitted values to check for heteroskedasticity (fan shape) or nonlinearity (pattern). Plot residuals versus each regressor to check for omitted nonlinear terms. Check residual normality with histogram or Q-Q plot—though non-normality is less critical with large samples due to CLT.

> **Key Concept**: Influential observations can dramatically change regression results. DFITS measures influence on fitted values; DFBETA measures influence on specific coefficients. Observations with $|$DFITS$| > 2\sqrt{k/n}$ or $|$DFBETA$| > 2/\sqrt{n}$ warrant investigation. Don't automatically delete influential points—investigate whether they're errors, outliers, or valid extreme values.

## Some in-class Exercises

(1) We estimate by OLS the model $y_{i}=\beta_{1}+\beta_{2} x_{2 i}+\beta_{3} x_{3 i}+u_{i}$ and obtain default standard errors. What problems arise when, in turn, each of the following occurs.
(1) $x_{3}$ should not appear in the model.
(2) $x_{3}$ is an indicator variable that takes only values 0 or 1 .
(1) $x_{3}=2 x_{2}$.
(4) $x_{4}$ should also have appeared in the model.
( ( $u_{i}$ has mean zero but it is not independent of the other $u_{j}$.
(6 $u_{i}$ has have mean zero and is independent of the other $u_{j}$, but it is heteroskedastic.

---

## Key Takeaways

**Multicollinearity (Section 16.1):**
- Multicollinearity occurs when regressors are highly correlated with each other
- Perfect multicollinearity (e.g., dummy variable trap) makes some coefficients unidentifiable
- High multicollinearity makes individual coefficients imprecisely estimated (large standard errors)
- OLS remains unbiased and consistent with multicollinearity—the problem is precision, not bias
- Symptoms: high R² but few significant t-statistics, coefficients with "wrong" signs, coefficients that change dramatically when variables are added/removed
- Detection: Regress one regressor on remaining regressors; if R² is very high (close to 1), multicollinearity is severe
- Variance inflation factors (VIF) quantify multicollinearity; VIF > 10 indicates concern
- Multicollinearity can occur even when pairwise correlations are low (multiway correlation)
- Solutions: (1) get more data, (2) drop redundant variables, (3) use joint F-tests for collinear subsets, (4) accept wider confidence intervals
- Example: Age, Education, and Experience are highly correlated (Experience ≈ Age - Education - 6)
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
- Mathematical foundation: b = β + Σw_i u_i where w_i = x_i / Σx_i²
- For unbiasedness, need E[Σw_i u_i] = 0, which requires E[u_i|x_i] = 0
- For correct variance formula, need assumptions 3 and 4: Var[b] = σ_u² / Σx_i²

**Incorrect Population Model (Section 16.3):**
- Wrong functional form (e.g., should be log-linear but estimated linear) causes bias and inconsistency
- Omitted regressors cause omitted variables bias if omitted variable affects y AND is correlated with included regressors
- Omitted variables bias formula: E[b₂] = α₂ + α₃γ, where γ is coefficient from regressing omitted z on included x
- Bias can be positive or negative depending on signs of α₃ (effect of omitted variable) and γ (correlation)
- Bias magnitude depends on both the strength of the omitted variable's effect and its correlation with included regressors
- Irrelevant regressors (variables that shouldn't be in model) don't cause bias but reduce precision
- Better to include too many regressors than too few—err on side of including potential confounders
- Solution to omitted variables bias: include relevant control variables
- Always ask: "What variables might affect y and be correlated with my regressor of interest?"
- Robustness checks: test whether coefficients change substantially when adding potential controls

**Endogeneity and Regressors Correlated with Errors (Section 16.4):**
- Endogeneity means regressor x is correlated with error u: E[u|x] ≠ 0
- Endogeneity causes OLS to be biased and inconsistent
- Three main sources of endogeneity: (1) omitted variables, (2) measurement error in regressors, (3) simultaneity/reverse causation
- Example 1 (omitted variables): Earnings on schooling, but u includes unobserved ability correlated with schooling
- Example 2 (simultaneity): Inflation on money supply, but money supply responds to inflation (feedback)
- Example 3 (measurement error): True x* measured with error as x = x* + ε, causing attenuation bias toward zero
- Terminology: Endogenous regressor is correlated with u; exogenous regressor is uncorrelated with u
- Solution: Instrumental variables (IV) estimation
- Valid instrument z must satisfy: (1) relevance (correlated with endogenous x) and (2) exclusion restriction (uncorrelated with u)
- IV estimator: b_IV = Σ(z_i - z̄)(y_i - ȳ) / Σ(z_i - z̄)(x_i - x̄)
- Intuition: IV estimates Δy/Δx as ratio (Δy/Δz) / (Δx/Δz)
- Example instrument: distance to college for schooling in wage equations
- With multiple endogenous regressors and multiple instruments, use two-stage least squares (2SLS)

**Heteroskedasticity (Section 16.5):**
- Heteroskedasticity means error variance varies across observations: Var[u_i|x_i] ≠ σ_u²
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
- Autocorrelation means errors are correlated over time: Cov[u_i, u_j] ≠ 0 for i ≠ j
- Common in time series data when economic shocks persist (positive autocorrelation)
- Also arises with clustered errors in cross-section or panel data (within-cluster correlation)
- When autocorrelation present, OLS remains unbiased and consistent
- But OLS is inefficient, and default standard errors are wrong (typically too small)
- Too-small standard errors lead to over-rejection of null hypotheses (false positives)
- Clustered errors: Observations in same cluster (e.g., students in school, workers in firm) have correlated errors
- Solution for clustered errors: Cluster-robust standard errors (cluster on group identifier)
- Autocorrelated errors in time series: AR(1) model u_t = ρu_{t-1} + ε_t is common specification
- Solution for time series: HAC (heteroskedasticity and autocorrelation consistent) standard errors
- HAC standard errors (Newey-West) account for both heteroskedasticity and autocorrelation
- Choose lag length m for HAC: rule of thumb m = 0.75 × T^(1/3) for sample size T
- Alternative: Model dynamics explicitly (add lagged y or x as regressors)
- For severe autocorrelation, FGLS (feasible generalized least squares) assuming specific error structure
- Panel data methods (Chapter 17): Random effects or fixed effects estimators

**Democracy and Growth Example (Section 16.7):**
- Dataset: 131 countries, changes from 1500 to 2000 in democracy and income per capita
- Bivariate regression: Democracy = 0.397 + 0.131×Growth (R² = 0.192, significant)
- Suggests economic growth increases democracy
- Multiple regression adds controls: constraints on executive, year of independence, religion proportions
- With controls: Democracy = 3.031 + 0.047×Growth + controls (R² = 0.192)
- Growth coefficient falls from 0.131 to 0.047 (reduction of 64%)
- Classic demonstration of omitted variables bias
- Point of study: Institutions (religion, constraints on executive) matter for democracy
- Catholic and Protestant countries have higher democracy than Muslim countries (omitted category: Other)
- Coefficient changes demonstrate importance of including relevant controls
- R² unchanged despite adding variables (0.192 in both) because controls are orthogonal to growth
- Always test robustness by adding controls and checking if coefficients remain stable

**Residual Diagnostic Plots (Section 16.8.1-16.8.2):**
- Residual plots reveal model violations that summary statistics miss
- Plot 1: y versus ŷ (actual vs. fitted) shows overall fit quality
- Plot 2: e versus ŷ (residuals vs. fitted) is rotated version of Plot 1
- Residuals vs. fitted values: Look for patterns indicating heteroskedasticity or nonlinearity
- Fan or cone shape: heteroskedasticity (variance increasing with fitted values)
- U-shape or systematic pattern: wrong functional form (need nonlinear terms)
- Random scatter around zero: assumptions satisfied
- Plot 3: Residuals versus individual regressor x_j detects problems with that specific variable
- Systematic pattern suggests omitted nonlinear term (quadratic, interaction)
- Component-plus-residual plot: p_ji = b_j x_ji + e_i versus x_ji
- Shows partial relationship between y and x_j after controlling for other regressors
- Useful for detecting nonlinearity in x_j's effect
- Added variable plot (partial regression leverage plot): Purge both y and x_j of other regressors, then plot
- Shows pure relationship between y and x_j, holding other variables constant
- Slope of added variable plot equals OLS coefficient b_j

**Outliers and Influential Observations (Section 16.8.3-16.8.4):**
- Outlier: Observation with unusual value given rest of data
- May indicate data error, extreme but valid value, or different population
- Not all outliers are influential—depends on leverage
- Leverage: Distance of regressor values from sample mean (high x_i far from x̄)
- High leverage observations have potential to influence regression results
- Influential observation: One that substantially affects fitted values or coefficient estimates
- DFITS measures influence on fitted values (difference in fits)
- DFITS_i = scaled difference in ŷ_i with vs. without observation i
- Rule of thumb: |DFITS| > 2√(k/n) indicates potentially influential observation
- DFBETA measures influence on specific coefficients (difference in beta)
- DFBETA_ji = scaled difference in b_j with vs. without observation i
- Rule of thumb: |DFBETA| > 2/√n warrants investigation
- Don't automatically delete influential observations—investigate first
- Check if influential point is data error, outlier from different population, or valid extreme
- Residual distribution analysis: Check for asymmetry (suggests nonlinearity) or fat tails (outliers)
- Important: Residuals e_i ≠ model errors u_i, even asymptotically
- e_i = u_i - (b₁ - β₁) - (b₂ - β₂)x_i, so e_i depends on x_i even if u_i doesn't
- Residuals are heteroskedastic and correlated even if model errors are not
- This dependence disappears as n → ∞, so diagnostics more reliable with large samples

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

