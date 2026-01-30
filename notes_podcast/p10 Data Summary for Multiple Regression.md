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

---

In [Chapter 5](s05%20Bivariate%20Data%20Summary.md), you learned that each extra square foot adds about 74 dollars to house price. But houses aren't just square footage—they also have bedrooms, bathrooms, lot size, and age. Does an extra bedroom increase price beyond what square footage alone predicts? This is the question multiple regression answers. By including many variables simultaneously, we can isolate each variable's effect while holding all others constant. This is the most important extension in all of econometrics—moving from bivariate to multivariate analysis.

## 10.1 Example: House Price

- HOUSE data: 29 houses sold in central Davis, California, in 1999.
- lot size is 1 for small, 2 for medium and 3 for large
- a half bathroom is a lavatory without bath or shower.

**Example 10.1**: House Price and Characteristics Data Summary

Examining the summary statistics: Price (Sale Price in dollars) has Mean 253,910, Standard deviation 37,391, Min 204,000, Max 375,000. Size (House size in square feet) has Mean 1,883, Standard deviation 398, Min 1,400, Max 3,300. Bedrooms (Number of bedrooms) has Mean 3.79, Standard deviation 0.68, Min 3, Max 6. Bathrooms (Number of bathrooms) has Mean 2.21, Standard deviation 0.34, Min 2, Max 3. Lotsize (Size of lot: 1, 2 or 3) has Mean 2.14, Standard deviation 0.69, Min 1, Max 3. Age (House age in years) has Mean 36.4, Standard deviation 7.12, Min 23, Max 51. Month Sold (Month of year house was sold) has Mean 5.97, Standard deviation 1.68, Min 3, Max 8.

> **Key Concept**: Multiple regression requires examining relationships between many variables. Summary statistics and pairwise correlations provide initial insights, but regression coefficients measure the effect of each variable after controlling for the others.

## Example Regression

**Example 10.2**: Multiple Regression Results for House Price

Looking at the regression results: Size has Coefficient 68.37, Standard Error 15.39, t statistic 4.44, p value 0.000, and 95 percent confidence interval from 36.45 to 101.29. Bedrooms has Coefficient 2,685, Standard Error 9,193, t statistic 0.29, p value 0.773, and 95 percent confidence interval from negative 16,379 to 21,749. Bathrooms has Coefficient 6,833, Standard Error 15,721, t statistic 0.43, p value 0.668, and 95 percent confidence interval from negative 25,771 to 39,437. Lot Size has Coefficient 2,303, Standard Error 7,227, t statistic 0.32, p value 0.753, and 95 percent confidence interval from negative 12,684 to 17,290. Age has Coefficient negative 833, Standard Error 719, t statistic negative 1.16, p value 0.259, and 95 percent confidence interval from negative 2,325 to 659. Month Sold has Coefficient negative 2,089, Standard Error 3,521, t statistic negative 0.59, p value 0.559, and 95 percent confidence interval from negative 9,390 to 5,213. Intercept has Coefficient 137,791, Standard Error 61,464, t statistic 2.24, p value 0.036, and 95 percent confidence interval from 10,321 to 265,261. Sample size n equals 29. F with 6 comma 22 degrees of freedom equals 6.83. p-value for F equals 0.0003. R-squared equals 0.651. Adjusted R-squared equals 0.555. Standard error equals 24,936.

> **Key Concept**: The multiple regression shows that only Size is statistically significant (t equals 4.44, p equals 0.000). Each additional square foot is associated with a 68.37 dollar increase in price, holding all other variables constant. The model explains 65.1 percent of price variation (R-squared equals 0.651), though adjusted R-squared is lower at 0.555 due to the penalty for including many regressors.

**Why This Matters**: Notice something surprising in the regression results—only Size is statistically significant! Bedrooms, bathrooms, lot size, age, and month sold all have p-values above 0.05. Why? Because once you control for square footage, these other features don't add much independent information. A larger house naturally has more bedrooms, so bedrooms don't matter beyond what size already tells us. This illustrates a key lesson: correlation doesn't equal causation, and simple bivariate relationships can be misleading.

Before jumping into the math, let's explore our data visually to understand the relationships we're trying to model.

## 10.2 Two-way Scatterplots

- Can get multiple two-way scatterplots - next slide.
- Some programs provide three-way surface plots
- e.g. price against size and number of bedrooms
- these can be difficult to read.


## Two-way Scatterplots

![](https://cdn.mathpix.com/cropped/87eb2a36-f476-4d35-b20d-3d6a18abe1e1-07.jpg?height=623&width=817&top_left_y=191&top_left_x=221)

## 10.3 Correlation

- Pairwise correlations are very useful for exploratory analysis
- Price is most highly correlated with square feet, then bedrooms and bathrooms.
- Asterisk means statistically significant correlation at significance level 0.05.

**Example 10.3**: Correlation Matrix for House Price Variables

Looking at the correlation matrix: Sale Price has correlation 1 with itself. Size has correlation 0.79 with asterisk (statistically significant) with Price, and correlation 1 with itself. Bedrooms has correlation 0.43 with asterisk with Price, correlation 0.52 with asterisk with Size, and correlation 1 with itself. Bathrooms has correlation 0.33 with Price, correlation 0.32 with Size, correlation 0.04 with Bedrooms, and correlation 1 with itself. Lot Size has correlation 0.15 with Price, correlation 0.11 with Size, correlation 0.29 with Bedrooms, correlation 0.10 with Bathrooms, and correlation 1 with itself. Age has correlation negative 0.07 with Price, correlation 0.08 with Size, correlation negative 0.03 with Bedrooms, correlation 0.03 with Bathrooms, correlation negative 0.02 with Lot Size, and correlation 1 with itself. Month Sold has correlation negative 0.21 with Price, correlation negative 0.21 with Size, correlation 0.18 with Bedrooms, correlation negative 0.39 with asterisk with Bathrooms, correlation negative 0.06 with Lot Size, correlation negative 0.37 with Age, and correlation 1 with itself.

- Bedrooms correlated with Price but this could merely be picking up the effect of Size (Bedrooms is correlated with Size).
- Multiple regression measures role of each variable in predicting price, after controlling for the other variables.

> **Key Concept**: Correlation matrices reveal bivariate relationships, but can be misleading. For example, bedrooms correlate with price, but this may simply reflect that larger houses (higher square footage) have more bedrooms. Multiple regression isolates the effect of each variable.

Now that we've explored correlations, let's formalize how multiple regression estimates the relationship between price and all these variables simultaneously.

## 10.4 Regression Line

**In this section:**
- 10.4.1 Least squares estimation
- 10.4.2 Computing OLS estimates

- Regression line from regression of y on several variables x-two, dot-dot-dot, x-k is

**Example 10.4**: Multiple Regression Model Specification

Predicted y equals b-one plus b-two times x-two, plus b-three times x-three, plus dot-dot-dot, plus b-k times x-k,

where

- predicted y equals predicted (or fitted) dependent variable
- x-two, dot-dot-dot, x-k are regressor variables
- b-one, b-two, dot-dot-dot, b-k are estimated intercept and estimated slope parameters.


### 10.4.1 Least Squares Estimation

- The residual is

Starting with e-sub-i equals y-sub-i minus predicted y-sub-i. This equals y-sub-i minus b-one, minus b-two times x-two-i, minus b-three times x-three-i, plus dot-dot-dot, minus b-k times x-k-i

- Estimate b-one, b-two, dot-dot-dot, b-k by least squares (OLS: ordinary least squares) that minimizes sum of squared residuals

Starting with the sum from i equals 1 to n of e-sub-i-squared equals the sum from i equals 1 to n of the quantity y-sub-i minus predicted y-sub-i, all squared. This equals the sum from i equals 1 to n of the quantity y-sub-i minus b-one, minus b-two times x-two-i, minus b-three times x-three-i, plus dot-dot-dot, minus b-k times x-k-i, all squared

- Estimates b-one, dot-dot-dot, b-k solve the k normal equations
- The sum from i equals 1 to n of x-sub-j-i times the quantity y-sub-i minus b-one, minus b-two times x-two-i, minus b-three times x-three-i, minus dot-dot-dot, minus b-k times x-k-i, equals zero, for j equals 1, dot-dot-dot, k,
- or the sum from i equals 1 to n of x-sub-j-i times e-sub-i equals zero, for j equals 1, dot-dot-dot, k
- each regressor is orthogonal to the regressor
- and the residuals sum to zero if an intercept is included.

> **Key Concept**: OLS estimates minimize the sum of squared residuals. The normal equations ensure that each regressor is orthogonal to the residuals: the sum of x-sub-j-i times e-sub-i equals zero for each regressor j. When an intercept is included, residuals sum to zero. These k equations uniquely determine the k coefficient estimates.

### 10.4.2 Computing OLS Estimates

- Consider the coefficient b-sub-j of the j-th regressor x-sub-j.
- The OLS coefficient b-sub-j can be calculated by
- bivariate regression of y on x-tilde-sub-j
- where x-tilde-sub-j equals x-sub-j minus predicted x-sub-j is the residual from regressing x-sub-j on an intercept and all regressors other than x-sub-j.
- Algebraically

b-sub-j equals the sum from i equals 1 to n of x-tilde-sub-j-i times the quantity y-sub-i minus y-bar, all divided by the sum from i equals 1 to n of x-tilde-sub-j-i-squared.

- So OLS coefficient measures the relationship between y and x-sub-j after the explanatory power of x-sub-j has been reduced by controlling for how the other regressors in the equation jointly predict x-sub-j.
- More generally matrix algebra is used - see Appendix C.4.

> **Key Concept**: The OLS coefficient for regressor x-sub-j measures the relationship between y and x-sub-j after controlling for how other regressors jointly predict x-sub-j. This "residualizing" interpretation is key to understanding partial effects.

## 10.5 Interpretation of Slope Coefficients

**In this section:**
- 10.5.1 Partial effects versus total effects
- 10.5.2 Further details on partial effects

- b-two measures the partial effect of changing x-two while holding all other regressors at their current values
- Reason: increase x-two by Delta x-two. Then

Starting with predicted y-sub-new equals b-one plus b-two times the quantity x-two plus Delta x-two, plus b-three times x-three, plus dot-dot-dot, plus b-k times x-k. This equals b-two times Delta x-two, plus b-one, plus b-two times x-two, plus b-three times x-three, plus dot-dot-dot, plus b-k times x-k. This equals b-two times Delta x-two, plus predicted y-sub-old

- So Delta predicted y equals b-two times Delta x-two and hence partial effect

The partial derivative of predicted y with respect to x-two, holding x-three through x-k constant, equals b-two.

> **Key Concept**: The regression coefficient b-two measures the partial effect of x-two on y, holding all other regressors constant. Mathematically, this is the partial derivative of predicted y with respect to x-two. If x-two increases by Delta x-two while other variables stay fixed, predicted y changes by b-two times Delta x-two.

### 10.5.1 Partial Effects Versus Total Effects

- The total effect on y-two lets other features of the house change as we change x-two.
- Suppose predicted y equals b-one plus b-two times x-two, plus b-three times x-three
- changing x-two by Delta x-two is associated with a change in x-three of Delta x-three
- then the total effect on y of changing x-two by Delta x-two equals Delta predicted y equals b-two times Delta x-two, plus b-three times Delta x-three
- Dividing by Delta x-two, the total effect on y-two of changing x-two equals

The total derivative of predicted y with respect to x-two equals b-two plus b-three times the quantity Delta x-three divided by Delta x-two

- Aside: Mechanical result for OLS
- When regression is by OLS, the total effect on the predicted value of y when x-two changes by one unit from a multivariate regression simply equals the slope coefficient from bivariate regression of y on x-two alone.

> **Key Concept**: Partial effects measure the impact of changing one regressor while holding all others constant (partial derivative of y with respect to x-sub-j). Total effects allow other regressors to change as well (total derivative of y with respect to x-sub-j). In most applications, we focus on partial effects to isolate the role of each variable.

**Why This Matters**: The distinction between partial and total effects is crucial for policy analysis. Suppose education increases earnings. The partial effect answers: "If we increase one person's education while everyone else stays the same, how much more do they earn?" The total effect answers: "If we increase everyone's education, accounting for equilibrium effects on labor markets, how much more does the average person earn?" These can be very different! Partial effects are what regression gives us—and they're what most policy questions require.

### 10.5.2 Further Details on Partial Effects

- Partial effect versus total effect
- Often interest lies in the partial effect of changing one key regressor after controlling for other variables
- e.g. size of change in earnings as education varies after controlling for age, gender, socioeconomic background.
- Calculus
- partial effect of regressor x-sub-j is partial derivative partial y by partial x-sub-j.
- total effect of regressor x-sub-j is total derivative d y by d x-sub-j.
- Causation
- OLS measures association but not necessarily causation.
- so say that a one unit change in x-sub-j is associated with a b-sub-j change in predicted y holding all other regressors constant.

> **Key Concept**: Multiple regression measures association, not causation. We say that a one-unit change in x-sub-j is associated with a b-sub-j change in predicted y holding other regressors constant. Causal claims require additional assumptions (addressed in [Chapter 17](s17%20Panel%20Data%2C%20Time%20Series%20Data%2C%20Causation.md)).

## 10.6 Model Fit: Standard Error of the Regression

**In this section:**
- 10.6.1 R-squared for multiple regression
- 10.6.2 Adjusted R-squared
- 10.6.3 Information criteria (AIC, BIC, HQIC)
- 10.6.4 Information criteria formulas

- For multiple regression the standard error of the regression is

s-e equals the square root of 1 over n minus k, times the sum from i equals 1 to n of the quantity y-sub-i minus predicted y-sub-i, all squared.

- Now division is by n minus k, rather than n minus 2 in the bivariate case, as k degrees of freedom are lost since computation of predicted y equals b-one plus b-two times x, plus dot-dot-dot, plus b-k times x-k is based on the k estimates b-one, dot-dot-dot, b-k.
- Another name for s-e is the root mean squared error (MSE) of the residual.
- It is also sometimes called the standard error of the residual.

> **Key Concept**: The standard error of the regression s-e measures the typical size of residuals. In multiple regression, we divide by n minus k degrees of freedom (not n minus 2) because we estimate k parameters. This degrees of freedom adjustment ensures s-e-squared is an unbiased estimator of the error variance.

### 10.6.1 R-Squared for Multiple Regression

- Again Total sum of squares equals Explained sum of squares plus Residual sum of squares.
- R-squared is same underlying formula as in bivariate case

Starting with R-squared equals Explained sum of squares divided by Total sum of squares, which equals the sum from i equals 1 to n of the quantity predicted y-sub-i minus y-bar, all squared, divided by the sum from i equals 1 to n of the quantity y-sub-i minus y-bar, all squared. Also, R-squared equals 1 minus Residual sum of squares divided by Total sum of squares, which equals 1 minus the sum from i equals 1 to n of the quantity y-sub-i minus predicted y-sub-i, all squared, divided by the sum from i equals 1 to n of the quantity y-sub-i minus y-bar, all squared.

- assuming the model includes an intercept term
- zero is less than or equal to R-squared, which is less than or equal to 1.
- R-squared equals the fraction of the variation in y (about y-bar) explained by the regressors x-one, dot-dot-dot, x-k.
- R-squared equals the squared correlation between y-sub-i and predicted y-sub-i
- i.e. between fitted and actual value of y.

> **Key Concept**: R-squared in multiple regression has the same interpretation as in bivariate regression: the fraction of variation in y explained by all regressors. It equals the squared correlation between y and predicted y (fitted values).

### 10.6.2 Adjusted R-Squared

- R-squared necessarily increases as add regressors, since residual sum of squares decreases.
- So also use adjusted R-squared, denoted R-bar-squared

Starting with R-bar-squared equals 1 minus Residual sum of squares divided by n minus k, all divided by Total sum of squares divided by n minus 1. This equals 1 minus the sum from i equals 1 to n of the quantity y-sub-i minus predicted y-sub-i, all squared, divided by n minus k, all divided by the sum from i equals 1 to n of the quantity y-sub-i minus y-bar, all squared, divided by n minus 1.

- Motivation is to divide residual and total sum of squares by their degrees of freedom
- this gives penalty to larger models (k increases)
- Compare smaller and larger model for house price
- with just square feet as regressor: R-squared equals 0.618 and R-bar-squared equals 0.603.
- with all regressors: R-squared equals 0.651 and R-bar-squared equals 0.555.
- only a modest increase in R-squared and R-bar-squared falls.

> **Key Concept**: Adjusted R-squared penalizes model complexity by dividing sums of squares by degrees of freedom. Unlike R-squared, adjusted R-squared can decrease when adding regressors if the new regressors add little explanatory power. Use adjusted R-squared to compare models with different numbers of regressors.

### 10.6.3 Information Criteria (AIC, BIC, HQIC)

- Information criteria are a more advanced method that penalizes larger models.

- Specifically, information criteria penalize sigma-hat-e-squared for larger model size
- sigma-hat-e-squared equals 1 over n times the sum from i equals 1 to n of the quantity y-sub-i minus predicted y-sub-i, all squared, is the sample average of the squared residuals
- similar to s-e-squared except there is no degrees of freedom correction, so division is by n rather than n minus k.

> **Key Concept**: Information criteria use sigma-hat-e-squared (average squared residual without degrees of freedom correction) rather than s-e-squared. They penalize this for model size to balance fit and parsimony. Smaller information criterion values indicate better models.

### 10.6.4 Information Criteria Formulas

Akaike IC
Bayesian IC
Hannan-Quinn IC

**General formula**

The formulas are: AIC equals n times ln of sigma-hat-e-squared, plus n times the quantity 1 plus ln of 2 pi, plus 2 times k. BIC equals n times ln of sigma-hat-e-squared, plus n times the quantity 1 plus ln of 2 pi, plus k times ln of n. HQIC equals n times ln of sigma-hat-e-squared, plus n times the quantity 1 plus ln of 2 pi, plus 2 times k times ln of the quantity ln of n.

- k is the number of regressors
- smaller values of each criterion are preferred
- BIC is preferred (AIC has too small a penalty for model size)
- some statistical packages divide the above formulas by n.

> **Key Concept**: Information criteria (AIC, BIC, HQIC) penalize larger models more heavily than adjusted R-squared. Smaller values are better. BIC is generally preferred as it has a stronger penalty for model size. These criteria are useful for model selection among non-nested models.

**Quick Check**: Before moving on, make sure you understand these core concepts: (1) What does the coefficient b-two equals 68.37 mean in the house price regression with multiple regressors? (2) Why did adjusted R-squared decrease from 0.603 to 0.555 when we added five regressors? (3) What's the difference between partial and total effects? (4) Why is only Size statistically significant in the full model? Understanding these points is essential for interpreting multiple regression results—and they'll be crucial when we learn statistical inference for multiple regression in [Chapter 11](s11%20Statistical%20Inference%20for%20Multiple%20Regression.md).

Now let's see how all these statistics appear in actual computer output when you run a multiple regression.

## 10.7 Computer Output Following Multiple Regression

- Computer output usually has three components
- 1. ANOVA table
- Gives explained, residual and total sum of squares
- Use to compute R-squared (and overall F-statistic given in next chapter).
- 2. Regression coefficient estimates
- and associated standard errors, t-statistics, p-values, confidence intervals
- 3. Regression summary statistics
- number of observations, R-squared, adjusted R-squared, Standard error of regression, overall F-statistic.

> **Key Concept**: Standard regression output includes three main components: the ANOVA table (sums of squares), coefficient estimates with inference statistics (standard errors, t-statistics, p-values, confidence intervals), and summary statistics (n, R-squared, adjusted R-squared, s-e, F-statistic). Understanding each component is essential for interpreting regression results.

## 10.8 Inestimable Models

- It is not always possible to estimate all k regression coefficients in the regression of y on an intercept and regressors x-two, dot-dot-dot, x-k.
- e.g. bivariate regression cannot estimate b-two if the sum from i equals 1 to n of the quantity x-sub-i minus x-bar, all squared, equals zero.
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

## Key Takeaways

**Data Exploration and Correlation:**

- Multiple regression extends bivariate regression to include several regressors simultaneously
- Summary statistics provide initial overview of variables (means, standard deviations, min and max values)
- Two-way scatterplots can show relationships but become unwieldy with many variables
- Correlation matrices reveal pairwise associations among all variables (e.g., price-size correlation of 0.79)
- Strong correlations between regressors (multicollinearity) can make it difficult to isolate individual effects
- Correlation can be misleading—bedrooms correlate with price but may reflect size, not independent bedroom effect
- Multiple regression isolates each regressor's effect after controlling for others

**Multiple Regression Model and OLS Estimation:**

- Multiple regression model: predicted y equals b-one plus b-two times x-two, plus b-three times x-three, plus dot-dot-dot, plus b-k times x-k
- OLS estimates minimize the sum of squared residuals: the sum of the quantity y-sub-i minus predicted y-sub-i, all squared
- Normal equations ensure each regressor is orthogonal to residuals: the sum of x-sub-j-i times e-sub-i equals zero
- Residuals sum to zero when an intercept is included
- The coefficient b-sub-j can be computed by bivariate regression of y on x-tilde-sub-j (residuals from regressing x-sub-j on other regressors)
- This "residualizing" interpretation shows how OLS controls for other variables
- Matrix algebra is typically used for computation (see Appendix C.4)

**Partial Effects and Coefficient Interpretation:**

- The coefficient b-sub-j measures the partial effect of x-sub-j: partial derivative of predicted y with respect to x-sub-j, holding other regressors constant
- Partial effects differ from total effects (which allow other regressors to vary simultaneously)
- Total effect: total derivative of y with respect to x-sub-j equals b-sub-j plus the sum of b-sub-k times d x-sub-k by d x-sub-j, when other variables change with x-sub-j
- For OLS, total effect from multivariate regression equals bivariate regression slope coefficient
- In most applications, we focus on partial effects to isolate each variable's role
- Example: Size coefficient of 68.37 means 68.37 dollars price increase per square foot, holding bedrooms, bathrooms, lot size, age, and month sold constant
- Multiple regression measures association, not necessarily causation—use careful language ("associated with")

**Model Fit and Evaluation:**

- R-squared measures the fraction of y variation explained by all regressors: R-squared equals Explained sum of squares divided by Total sum of squares
- R-squared equals 1 minus Residual sum of squares divided by Total sum of squares, equals squared correlation between y and predicted y (fitted values)
- R-squared necessarily increases when adding regressors (residual sum of squares cannot increase)
- Adjusted R-squared penalizes model complexity: R-bar-squared equals 1 minus Residual sum of squares divided by n minus k, all divided by Total sum of squares divided by n minus 1
- Adjusted R-squared can decrease when adding weak regressors, making it useful for model comparison
- Example: Adding 5 regressors to size-only model increased R-squared from 0.618 to 0.651 but decreased R-bar-squared from 0.603 to 0.555
- Standard error of regression s-e measures typical prediction error: s-e equals the square root of the sum of the quantity y-sub-i minus predicted y-sub-i, all squared, divided by n minus k

**Information Criteria and Model Selection:**

- Information criteria (AIC, BIC, HQIC) penalize larger models more heavily than adjusted R-squared
- Smaller values of each criterion are preferred (better models)
- BIC is generally preferred as it has a stronger penalty for model size than AIC
- BIC equals n times ln of sigma-hat-e-squared, plus n times the quantity 1 plus ln of 2 pi, plus k times ln of n, where k is number of regressors
- Information criteria are useful for model selection among non-nested models
- Different from hypothesis testing—focus on predictive performance rather than statistical significance

**Computer Output and Practical Issues:**

- Computer output typically includes three components: ANOVA table, coefficient estimates, and summary statistics
- ANOVA table provides sums of squares for computing R-squared and overall F-statistic
- Coefficient estimates include standard errors, t-statistics, p-values, and 95 percent confidence intervals
- Summary statistics include n, R-squared, adjusted R-squared, and standard error of regression
- Overall F-test evaluates joint significance of all regressors (covered in Chapter 11)

**Perfect Collinearity and Inestimable Models:**

- Perfect collinearity occurs when regressors have exact linear relationships
- With perfect collinearity, some coefficients cannot be estimated (not identified)
- Computer output will show "omitted" or blank entries for affected regressors
- Regressor data matrix is said to be of less than full rank
- Perfect collinearity can arise from inadequate data variation in well-specified models
- More commonly arises from model misspecification (e.g., including both a variable and its exact linear combination)
- Example: Including both temperature in Fahrenheit and Celsius, or income and log of income as separate regressors without interaction

---

## Some in-class Exercises

(1) Regression leads to fitted line predicted y equals 2 plus 3 times x-two, plus 4 times x-three. What is the residual for observation the triple x-two, x-three, y equals the triple 2, 1, 9?
(2) Suppose we know that y equals 8 plus 5 times x-two, plus 5 times x-three, plus u, where the expected value of u given x equals zero. Give the conditional mean of y given x and the error term for the observation the pair x, y equals the pair the pair 2, 3, 30.
(3) OLS regression on the same dataset leads to fitted models predicted y equals 6 plus 5 times x-two, and predicted y equals 2 plus 3 times x-two, plus 4 times x-three. Are you surprised by the different coefficients for x-two? Explain.
(4) OLS regression of y on x for a sample of size 53 leads to residual sum of squares 20 and total sum of squares 50. Compute the standard error of the regression.
(5) For the data of the previous example, compute R-squared and the correlation between y and predicted y.

