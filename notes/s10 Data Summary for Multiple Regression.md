# Chapter 10: Data Summary for Multiple Regression

## Learning Objectives

By the end of this chapter, you will be able to:
- Extend bivariate regression concepts to multiple regression with several regressors
- Interpret pairwise correlations and use them for exploratory data analysis
- Understand the ordinary least squares (OLS) method for multiple regression
- Interpret partial effects: how one regressor affects y while holding others constant
- Distinguish between partial effects and total effects
- Evaluate model fit using R-squared and adjusted R-squared
- Understand information criteria (AIC, BIC) for model selection
- Recognize when regression coefficients cannot be estimated (perfect collinearity)

Multiple regression extends bivariate regression to include several regressors simultaneously. This chapter introduces the core concepts for understanding multiple regression:

**Data Exploration (Sections 10.1-10.3):** Example data on house prices, two-way scatterplots, and correlation matrices for exploratory analysis.

**Regression Estimation (Sections 10.4-10.5):** The regression line with multiple regressors, ordinary least squares (OLS) estimation, and interpretation of slope coefficients as partial effects.

**Model Evaluation (Section 10.6):** Measures of model fit including R-squared, adjusted R-squared, and information criteria for model selection.

**Technical Issues (Sections 10.7-10.8):** Reading computer output and understanding when models cannot be estimated due to perfect collinearity.

Multiple regression is the workhorse of applied econometrics. While visual methods become less useful with many variables, the interpretation of coefficients as partial effects (controlling for other variables) is central to empirical work.


## Outline

(1) Example: House price and characteristics
(2) Two-way Scatter Plots
(3) Correlation
(4) Regression line
(5) Interpretation of Slope Coefficients
(6) Model Fit
(7) Computer Output Following Multiple Regression
(8) Inestimable Models

### 10.1 Example: House Price

- HOUSE data: 29 houses sold in central Davis, California, in 1999.
- lot size is 1 for small, 2 for medium and 3 for large
- a half bathroom is a lavatory without bath or shower.

**Example 10.1**: House Price and Characteristics Data Summary

| Variable | Definition | Mean | Standard deviation | Min | Max |
| :--- | :--- | :--- | :--- | :--- | :--- |
| Price | Sale Price in dollars | 253910 | 37391 | 204000 | 375000 |
| Size | House size in square feet | 1883 | 398 | 1400 | 3300 |
| Bedrooms | Number of bedrooms | 3.79 | 0.68 | 3 | 6 |
| Bathrooms | Number of bathrooms | 2.21 | 0.34 | 2 | 3 |
| Lotsize | Size of lot (1, 2 or 3 ) | 2.14 | 0.69 | 1 | 3 |
| Age | House age in years | 36.4 | 7.12 | 23 | 51 |
| Month Sold | Month of year house was sold | 5.97 | 1.68 | 3 | 8 |

> **Key Concept**: Multiple regression requires examining relationships between many variables. Summary statistics and pairwise correlations provide initial insights, but regression coefficients measure the effect of each variable after controlling for the others.

## Example Regression

**Example 10.2**: Multiple Regression Results for House Price

| Variable | Coefficient | St. Error | t statistic | p value | 95\% conf. int. |  |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| Size | 68.37 | 15.39 | 4.44 | 0.000 | 36.45 | 101.29 |
| Bedrooms | 2685 | 9193 | 0.29 | 0.773 | -16379 | 21749 |
| Bathrooms | 6833 | 15721 | 0.43 | 0.668 | -25771 | 39437 |
| Lot Size | 2303 | 7227 | 0.32 | 0.753 | -12684 | 17290 |
| Age | -833 | 719 | -1.16 | 0.259 | -2325 | 659 |
| Month Sold | -2089 | 3521 | -0.59 | 0.559 | -9390 | 5213 |
| Intercept | 137791 | 61464 | 2.24 | 0.036 | 10321 | 265261 |
| n | 29 |  |  |  |  |  |
| F(6,22) | 6.83 |  |  |  |  |  |
| p -value for F | 0.0003 |  |  |  |  |  |
| $\mathrm{R}^{2}$ | 0.651 |  |  |  |  |  |
| Adjusted $\mathrm{R}^{2}$ | 0.555 |  |  |  |  |  |
| St. error | 24936 |  |  |  |  |  |

### 10.2 Two-way Scatterplots

- Can get multiple two-way scatterplots - next slide.
- Some programs provide three-way surface plots
- e.g. price against size and number of bedrooms
- these can be difficult to read.


## Two-way Scatterplots

![](https://cdn.mathpix.com/cropped/87eb2a36-f476-4d35-b20d-3d6a18abe1e1-07.jpg?height=623&width=817&top_left_y=191&top_left_x=221)

### 10.3 Correlation

- Pairwise correlations are very useful for exploratory analysis
- Price is most highly correlated with square feet, then bedrooms and bathrooms.
- Asterisk means statistically significant correlation at significance level 0.05.

**Example 10.3**: Correlation Matrix for House Price Variables

| Correlation | Price | Size | Bed | Bath | Lot | Age | Mth Sold |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| Sale Price | 1 |  |  |  |  |  |  |
| Size | $.79^{*}$ | 1 |  |  |  |  |  |
| Bedrooms | $.43^{*}$ | $.52^{*}$ | 1 |  |  |  |  |
| Bathrooms | .33 | .32 | .04 | 1 |  |  |  |
| Lot Size | .15 | .11 | .29 | .10 | 1 |  |  |
| Age | -.07 | .08 | -.03 | .03 | -.02 | 1 |  |
| Month Sold | -.21 | -.21 | .18 | $-.39^{*}$ | -.06 | -.37 | 1 |

- Bedrooms correlated with Price but this could merely be picking up the effect of Size (Bedrooms is correlated with Size).
- Multiple regression measures role of each variable in predicting price, after controlling for the other variables.

> **Key Concept**: Correlation matrices reveal bivariate relationships, but can be misleading. For example, bedrooms correlate with price, but this may simply reflect that larger houses (higher square footage) have more bedrooms. Multiple regression isolates the effect of each variable.

---

**Key Takeaways from Sections 10.1-10.3 (Data Exploration):**
- Multiple regression extends bivariate regression to include several regressors simultaneously
- Two-way scatterplots can show relationships but become unwieldy with many variables
- Correlation matrices reveal pairwise associations among all variables
- Strong correlations between regressors (multicollinearity) can make it difficult to isolate individual effects
- Multiple regression measures each regressor's effect after controlling for other regressors

---

### 10.4 Regression Line

**In this section:**
- 10.4.1 Least squares estimation
- 10.4.2 Computing OLS estimates

- Regression line from regression of $y$ on several variables $x_{2}, \ldots, x_{k}$ is

**Example 10.4**: Multiple Regression Model Specification

$$
\widehat{y}=b_{1}+b_{2} x_{2}+b_{3} x_{3}+\cdots+b_{k} x_{k},
$$

where

- $\widehat{y}=$ predicted (or fitted) dependent variable
- $x_{2}, \ldots, x_{k}$ are regressor variables
- $b_{1}, b_{2}, \ldots, b_{k}$ are estimated intercept and estimated slope parameters.


#### 10.4.1 Least Squares Estimation

- The residual is

$$
\begin{aligned}
e_{i} & =y_{i}-\widehat{y}_{i} \\
& =y_{i}-b_{1}-b_{2} x_{2 i}-b_{3} x_{3 i}+\cdots-b_{k} x_{k i}
\end{aligned}
$$

- Estimate $b_{1}, b_{2}, \ldots, b_{k}$ by least squares (OLS: ordinary least squares) that minimizes sum of squared residuals

$$
\begin{aligned}
\sum_{i=1}^{n} e_{i}^{2} & =\sum_{i=1}^{n}\left(y_{i}-\widehat{y}_{i}\right)^{2} \\
& =\sum_{i=1}^{n}\left(y_{i}-b_{1}-b_{2} x_{2 i}-b_{3} x_{3 i}+\cdots-b_{k} x_{k i}\right)^{2}
\end{aligned}
$$

- Estimates $b_{1}, \ldots, b_{k}$ solve the $k$ normal equations
- $\sum_{i=1}^{n} x_{j i}\left(y_{i}-b_{1}-b_{2} x_{2 i}-b_{3} x_{3 i}-\cdots-b_{k} x_{k i}\right)=0, \quad j=1, \ldots, k$,
- or $\sum_{i=1}^{n} x_{j i} e_{i}=0, \quad j=1, \ldots, k$
- each regressor is orthogonal to the regressor
- and the residuals sum to zero if an intercept is included.


#### 10.4.2 Computing OLS Estimates

- Consider the coefficient $b_{j}$ of the $j^{t h}$ regressor $x_{j}$.
- The OLS coefficient $b_{j}$ can be calculated by
- bivariate regression of $y$ on $\widetilde{x}_{j}$
- where $\widetilde{x}_{j}=x_{j}-\widehat{x}_{j}$ is the residual from regressing $x_{j}$ on an intercept and all regressors other than $x_{j}$.
- Algebraically

$$
b_{j}=\frac{\sum_{i=1}^{n} \widetilde{x}_{j i}\left(y_{i}-\bar{y}\right)}{\sum_{i=1}^{n} \widetilde{x}_{j i}^{2}} .
$$

- So OLS coefficient measures the relationship between $y$ and $x_{j}$ after the explanatory power of $x_{j}$ has been reduced by controlling for how the other regressors in the equation jointly predict $x_{j}$.
- More generally matrix algebra is used - see Appendix C.4.

> **Key Concept**: The OLS coefficient for regressor xⱼ measures the relationship between y and xⱼ after controlling for how other regressors jointly predict xⱼ. This "residualizing" interpretation is key to understanding partial effects.

### 10.5 Interpretation of Slope Coefficients

**In this section:**
- 10.5.1 Partial effects versus total effects
- 10.5.2 Further details on partial effects

- $b_{2}$ measures the partial effect of changing $x_{2}$ while holding all other regressors at their current values
- Reason: increase $x_{2}$ by $\Delta x_{2}$. Then

$$
\begin{aligned}
\hat{y}_{\text {new }} & =b_{1}+b_{2}\left(x_{2}+\Delta x_{2}\right)+b_{3} x_{3}+\cdots+b_{k} x_{k} \\
& =b_{2} \Delta x_{2}+b_{1}+b_{2} x_{2}+b_{3} x_{3}+\cdots+b_{k} x_{k} \\
& =b_{2} \Delta x_{2}+\hat{y}_{\text {old }}
\end{aligned}
$$

- So $\Delta \hat{y}=b_{2} \Delta x_{2}$ and hence partial effect

$$
\left.\frac{\Delta \widehat{y}}{\Delta x_{2}}\right|_{x_{3}, \ldots, x_{k}}=b_{2} .
$$

#### 10.5.1 Partial Effects Versus Total Effects

- The total effect on $y_{2}$ lets other features of the house change as we change $x_{2}$.
- Suppose $\widehat{y}=b_{1}+b_{2} x_{2}+b_{3} x_{3}$
- changing $x_{2}$ by $\Delta x_{2}$ is associated with a change in $x_{3}$ of $\Delta x_{3}$
- then the total effect on $y$ of changing $x_{2}$ by $\Delta x_{2}$ equals $\Delta \hat{y}=b_{2} \Delta x_{2}+b_{3} \Delta x_{3}$
- Dividing by $\Delta x_{2}$, the total effect on $y_{2}$ of changing $x_{2}$ equals

$$
\left.\frac{\Delta \widehat{y}}{\Delta x_{2}}\right|_{\text {Total }}=b_{2}+b_{3} \frac{\Delta x_{3}}{\Delta x_{2}}
$$

- Aside: Mechanical result for OLS
- When regression is by OLS, the total effect on the predicted value of $y$ when $x_{2}$ changes by one unit from a multivariate regression simply equals the slope coefficient from bivariate regression of $y$ on $x_{2}$ alone.

> **Key Concept**: Partial effects measure the impact of changing one regressor while holding all others constant (∂y/∂xⱼ). Total effects allow other regressors to change as well (dy/dxⱼ). In most applications, we focus on partial effects to isolate the role of each variable.

#### 10.5.2 Further Details on Partial Effects

- Partial effect versus total effect
- Often interest lies in the partial effect of changing one key regressor after controlling for other variables
- e.g. size of change in earnings as education varies after controlling for age, gender, socioeconomic background.
- Calculus
- partial effect of regressor $x_{j}$ is partial derivative $\partial y / \partial x_{j}$.
- total effect of regressor $x_{j}$ is total derivative $d y / d x_{j}$.
- Causation
- OLS measures association but not necessarily causation.
- so say that a one unit change in $x_{j}$ is associated with a $b_{j}$ change in $\hat{y}$ holding all other regressors constant.

> **Key Concept**: Multiple regression measures association, not causation. We say that a one-unit change in xⱼ is associated with a bⱼ change in ŷ holding other regressors constant. Causal claims require additional assumptions (addressed in Chapter 17).

---

**Key Takeaways from Sections 10.4-10.5 (Regression Estimation and Interpretation):**
- Multiple regression: ŷ = b₁ + b₂x₂ + b₃x₃ + ... + bₖxₖ
- OLS estimates minimize the sum of squared residuals
- The coefficient bⱼ measures the partial effect of xⱼ: ∂ŷ/∂xⱼ holding other regressors constant
- Partial effects differ from total effects (which allow other regressors to vary)
- In most applications, we focus on partial effects to isolate each variable's role
- Multiple regression measures association, not necessarily causation

---

### 10.6 Model Fit: Standard Error of the Regression

**In this section:**
- 10.6.1 R-squared for multiple regression
- 10.6.2 Adjusted R-squared
- 10.6.3 Information criteria (AIC, BIC, HQIC)
- 10.6.4 Information criteria formulas

- For multiple regression the standard error of the regression is

$$
s_{e}=\sqrt{\frac{1}{n-k} \sum_{i=1}^{n}\left(y_{i}-\widehat{y}_{i}\right)^{2}} .
$$

- Now division is by $n-k$, rather than $n-2$ in the bivariate case, as $k$ degrees of freedom are lost since computation of $\widehat{y}=b_{1}+b_{2} x+\cdots+b_{k} x_{k}$ is based on the $k$ estimates $b_{1}, \ldots, b_{k}$.
- Another name for $s_{e}$ is the root mean squared error (MSE) of the residual.
- It is also sometimes called the standard error of the residual.


#### 10.6.1 R-Squared for Multiple Regression

- Again Total $S S=$ Explained $S S+$ Residual $S S$.
- $\mathbf{R}$-squared is same underlying formula as in bivariate case

$$
\begin{aligned}
& R^{2}=\frac{\text { Explained SS }}{\text { Total SS }}=\frac{\sum_{i=1}^{n}\left(\widehat{y}_{i}-\bar{y}\right)^{2}}{\sum_{i=1}^{n}\left(y_{i}-\bar{y}\right)^{2}} . \\
& R^{2}=1-\frac{\text { Residual SS }}{\text { Total SS }}=1-\frac{\sum_{i=1}^{n}\left(y_{i}-\widehat{y}_{i}\right)^{2}}{\sum_{i=1}^{n}\left(y_{i}-\bar{y}\right)^{2}} .
\end{aligned}
$$

- assuming the model includes an intercept term
- $0 \leq R^{2} \leq 1$.
- $R^{2}$ equals the fraction of the variation in $y$ (about $\bar{y}$ ) explained by the regressors $x_{1}, \ldots, x_{k}$.
- $R^{2}$ equals the squared correlation between $y_{i}$ and $\hat{y}_{i}$
- i.e. between fitted and actual value of $y$.

> **Key Concept**: R-squared in multiple regression has the same interpretation as in bivariate regression: the fraction of variation in y explained by all regressors. It equals the squared correlation between y and ŷ (fitted values).

#### 10.6.2 Adjusted R-Squared

- $R^{2}$ necessarily increases as add regressors, since residual sum of squares decreases.
- So also use adjusted $\mathbf{R}$-squared, denoted $\bar{R}^{2}$

$$
\begin{aligned}
\bar{R}^{2} & =1-\frac{\text { Residual SS } /(n-k)}{\text { Total SS } /(n-1)} \\
& =1-\frac{\sum_{i=1}^{n}\left(y_{i}-\widehat{y}_{i}\right)^{2} /(n-k)}{\sum_{i=1}^{n}\left(y_{i}-\bar{y}\right)^{2} /(n-1)} .
\end{aligned}
$$

- Motivation is to divide residual and total sum of squares by their degrees of freedom
- this gives penalty to larger models ( $k \uparrow$ )
- Compare smaller and larger model for house price
- with just square feet as regressor: $R^{2}=0.618$ and $\bar{R}^{2}=0.603$.
- with all regressors: $R^{2}=0.651$ and $\bar{R}^{2}=0.555$.
- only a modest increase in $R^{2}$ and $\bar{R}^{2}$ falls.

> **Key Concept**: Adjusted R-squared penalizes model complexity by dividing sums of squares by degrees of freedom. Unlike R², adjusted R² can decrease when adding regressors if the new regressors add little explanatory power. Use adjusted R² to compare models with different numbers of regressors.

#### 10.6.3 Information Criteria (AIC, BIC, HQIC)

- Information criteria are a more advanced method that penalizes larger models.

- Specifically, information criteria penalize $\widehat{\sigma}_{e}^{2}$ for larger model size
- $\widehat{\sigma}_{e}^{2}=\frac{1}{n} \sum_{i=1}^{n}\left(y_{i}-\widehat{y}_{i}\right)^{2}$ is the sample average of the squared residuals
- similar to $s_{e}^{2}$ except there is no degrees of freedom correction, so division is by $n$ rather than $n-k$.


#### 10.6.4 Information Criteria Formulas

Akaike IC
Bayesian IC
Hannan-Quinn IC

**General formula**

$$
\begin{aligned}
A I C & =n \times \ln \widehat{\sigma}_{e}^{2}+n(1+\ln 2 \pi)+2 k \\
B I C & =n \times \ln \widehat{\sigma}_{e}^{2}+n(1+\ln 2 \pi)+k \times \ln (n) \\
H Q I C & =n \times \ln \widehat{\sigma}_{e}^{2}+n(1+\ln 2 \pi)+2 k \times \ln (\ln (n))
\end{aligned}
$$

- $k$ is the number of regressors
- smaller values of each criterion are preferred
- BIC is preferred (AIC has too small a penalty for model size)
- some statistical packages divide the above formulas by $n$.

> **Key Concept**: Information criteria (AIC, BIC, HQIC) penalize larger models more heavily than adjusted R². Smaller values are better. BIC is generally preferred as it has a stronger penalty for model size. These criteria are useful for model selection among non-nested models.

---

**Key Takeaways from Section 10.6 (Model Fit):**
- R-squared measures the fraction of y variation explained by all regressors
- R² necessarily increases when adding regressors (residual SS decreases)
- Adjusted R-squared penalizes model complexity using degrees of freedom
- Adjusted R² can decrease when adding weak regressors, making it useful for model comparison
- Information criteria (AIC, BIC, HQIC) provide alternative model selection tools
- BIC is generally preferred (stronger penalty for model size than AIC)
- Standard error of regression (sₑ) measures typical prediction error

---

### 10.7 Computer Output Following Multiple Regression

- Computer output usually has three components
- 1. ANOVA table
- Gives explained, residual and total sum of squares
- Use to compute R-squared (and overall F-statistic given in next chapter).
- 2. Regression coefficient estimates
- and associated standard errors, t-statistics, p-values, Cl's
- 3. Regression summary statistics
- number of observations, R-squared, adjusted R-squared, Standard error of regression, overall F-statistic.


### 10.8 Inestimable Models

- It is not always possible to estimate all $k$ regression coefficients in the regression of $y$ on an intercept and regressors $x_{2}, \ldots, x_{k}$.
- e.g. bivariate regression cannot estimate $b_{2}$ if $\sum_{i=1}^{n}\left(x_{i}-\bar{x}\right)^{2}=0$.
- Then computer regression output will have no entries for one or more regressors, and may include the word omitted.
- When not all coefficients can be estimated
- the coefficients are said to be not identified
- the regressors are said to be perfectly collinear
- the regressor data matrix is said to of less than full rank.
- This situation may arise due to
- inadequate variation in the data in a well-specified model
- or due to a poorly specified model.

> **Key Concept**: Perfect collinearity (exact linear relationships among regressors) makes some coefficients inestimable. This can arise from inadequate data variation or model misspecification (e.g., including both a variable and its exact linear combination). Computer output will show "omitted" for affected regressors.

---

**Key Takeaways from Sections 10.7-10.8 (Computer Output and Estimation Issues):**
- Computer output typically includes: ANOVA table, coefficient estimates with inference, and summary statistics
- ANOVA table provides sums of squares for computing R²
- Coefficient estimates include standard errors, t-statistics, p-values, and confidence intervals
- Perfect collinearity occurs when regressors have exact linear relationships
- With perfect collinearity, some coefficients cannot be estimated (shown as "omitted")
- Perfect collinearity can arise from inadequate data variation or model misspecification

---

## Key Stata Commands

clear
use AED_HOUSE.DTA
correlate price size bedrooms bathroom lotsize age monthsold
regress price size bedrooms bathroom lotsize age monthsold

## Some in-class Exercises

(1) Regression leads to fitted line $\widehat{y}=2+3 x_{2}+4 x_{3}$. What is the residual for observation $\left(x_{2}, x_{3}, y\right)=(2,1,9)$ ?
(2) Suppose we know that $y=8+5 x_{2}+5 x_{3}+u$ where $E[u \mid x]=0$. Give the conditional mean of $y$ given $x$ and the error term for the observation $(x, y)=(2,3,30)$.
(3) OLS regression on the same dataset leads to fitted models $\widehat{y}=6+5 x_{2}$ and $\widehat{y}=2+3 x_{2}+4 x_{3}$. Are you surprised by the different coefficients for $x_{2}$ ? Explain.
(4) OLS regression of $y$ on $x$ for a sample of size 53 leads to residual sum of squares 20 and total sum of squares 50 . Compute the standard error of the regression.
(5) For the data of the previous example, compute $R^{2}$ and the correlation between $y$. and $\widehat{y}$.

