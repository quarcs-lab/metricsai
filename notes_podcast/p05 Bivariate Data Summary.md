# Chapter 5: Bivariate Data Summary

## Learning Objectives

By the end of this chapter, you will be able to:
- Summarize bivariate relationships using two-way tabulations and scatterplots
- Calculate and interpret the correlation coefficient between two variables
- Estimate a regression line using the method of least squares
- Interpret regression slope and intercept coefficients
- Evaluate model fit using R-squared and standard error of regression
- Make predictions using estimated regression models
- Understand the relationship between correlation and regression
- Recognize the difference between association and causation

---

You've learned to summarize individual variables using means, standard deviations, and histograms. But economics is rarely about one variable in isolation. Does education increase earnings? Do larger houses sell for higher prices? Does inflation affect unemployment? These questions all involve relationships between two variables. This chapter introduces the tools for measuring and visualizing these relationships: scatterplots, correlation, and regression—the foundation of all econometric analysis.

## 5.1 Example: House Price and Size

- We examine house price and size for a sample of 29 houses
- We control for location by considering a homogeneous housing market in central Davis in 1999.
- Eyeballing the data, it seems that price is higher if size is larger

**Example 5.1**: House Price and Size Data (29 observations)

The dataset includes pairs of sale price and square feet for 29 houses. For example, the first house sold for 375,000 dollars with 3,300 square feet, the second for 340,000 dollars with 2,400 square feet, and so on. Prices range from 204,000 to 375,000 dollars, while sizes range from 1,400 to 3,300 square feet. The data show considerable variation in both price and size.

## Summary Statistics

- House sale prices range from 204,000 to 375,000 dollars, with mean 253,910 dollars and standard deviation 37,391 dollars.
- House sizes range from 1,400 to 3,300 square feet, with mean 1,883 square feet and standard deviation 398 square feet.

**Example 5.2**: Summary Statistics for House Price and Size

Looking at the summary statistics: For sale price, the mean is 253,910 dollars, standard deviation is 37,391 dollars, standard error is 6,943 dollars, maximum is 375,000 dollars, median is 244,000 dollars, minimum is 204,000 dollars, skewness is 1.56, and kurtosis is 5.61. For square feet, the mean is 1,883 square feet, standard deviation is 398 square feet, standard error is 74 square feet, maximum is 3,300 square feet, median is 1,800 square feet, minimum is 1,400 square feet, skewness is 1.73, and kurtosis is 6.74. Both variables show positive skewness, indicating right-skewed distributions.

**Why This Matters**: In real estate markets, buyers care about both price and size simultaneously. Summary statistics for each variable separately tell us the typical price (253,910 dollars) and typical size (1,883 square feet), but they don't tell us the crucial relationship: how much more you pay for each extra square foot. That's where bivariate analysis—studying two variables together—becomes essential.

## Key methods for measuring relationship (this chapter)

- The correlation between house price and house size is 0.786.
- A scatterplot of house price against house size yields a clear positive pattern.
![](https://cdn.mathpix.com/cropped/b9128ba4-0753-416f-b579-a2696694bddc-06.jpg?height=369&width=500&top_left_y=257&top_left_x=386)
- Regression of house price against house size yields:

**Example 5.3**: Regression of House Price on House Size

Predicted Price equals 115,017 plus 73.77 times Size. The R-squared is 0.6175.

- An extra square foot of house is associated with a 73.77 dollar increase in house price.

> **Key Concept**: Visual inspection of data is the first step in bivariate analysis. The house price and size data show a clear positive relationship: larger houses tend to sell for higher prices. The correlation of 0.786 confirms this strong positive association, and the scatterplot reveals no obvious outliers or nonlinear patterns.


## 5.2 Two-way Tabulation

**In this section:**
- 5.2.1 Two-way tabulation with row and column percentages
- 5.2.2 Expected frequencies and chi-squared test

- A two-way tabulation or cross tabulation of variables x and y lists the number (or fraction) of observations equal to each of the distinct values taken by the pair (x, y).
- This is useful if the variables x and y take relatively few values: categorical data with few categories, discrete numerical data taking a few values, or for continuous numerical data converted to a few ranges.
- For the house price and size data, we create pricerange: low (price less than 249,000 dollars) or high (price greater than or equal to 250,000 dollars), and sizerange: small (size less than 1,800), medium (1,800 less than or equal to size less than 2,400) or large (size greater than or equal to 2,400).


### 5.2.1 Two-Way Tabulation with Row and Column Percentages

- Main entry: number of observations with a given price-size combination - for example, there were 11 houses of low price and small size.

**Example 5.4**: Two-Way Tabulation of Price Range and Size Range

Looking at the two-way tabulation: For low-priced houses, 11 are small, 6 are medium, and 0 are large, totaling 17 low-priced houses. For high-priced houses, 2 are small, 7 are medium, and 3 are large, totaling 12 high-priced houses. Column totals show 13 small houses, 13 medium houses, and 3 large houses, for a grand total of 29 houses.

- The table also includes row sums and column sums. For example, the total in the row for low price range is 11 plus 6 plus 0, which equals 17 observations.
- The table includes a second optional entry, a row percentage. For each value of pricerange, this gives the percentage of observations in each of the size ranges. For example, for low-priced houses: small equals 11 out of 17, which is 100 times 11 divided by 17, which equals 64.71 percent.
- We can also include similarly constructed column percentages.


### 5.2.2 Expected Frequencies and Chi-Squared Test

- A two-way tabulation can also include expected frequencies, assuming that the two variables are statistically independent.
- Expected frequency equals row total times column total, divided by number of observations.
- For example, the low-price small-size cell has expected frequency 17 times 13 divided by 29, which equals 7.62.

**Example 5.5**: Expected Frequencies Under Independence

The table presents both observed and expected frequencies. In each cell, the top number is the observed frequency and the bottom number is the expected frequency. For example, in the low-price small-size cell, we observe 11 houses but expect only 7.62 under independence. We see that more low-price houses are small than would be expected if price and size were independent (11 versus 7.62). This difference forms the basis for Pearson's chi-squared goodness-of-fit test of statistical independence of two categorical variables.

> **Key Concept**: Two-way tabulations show the joint distribution of two categorical variables. Expected frequencies (calculated assuming independence) provide the basis for Pearson's chi-squared test of statistical independence. If observed frequencies differ substantially from expected frequencies, we have evidence that the variables are related.

Two-way tabulations work well for categorical data with a few distinct values. But what about continuous variables like house price and size, which can take hundreds of different values? Tabulating every unique price-size combination would create an enormous, unreadable table. For continuous data, we need a visual approach: the scatterplot.

## 5.3 Two-way Scatterplot

- The standard visual method is a two-way scatter plot. The first panel shows house price increases with house size.
![](https://cdn.mathpix.com/cropped/b9128ba4-0753-416f-b579-a2696694bddc-10.jpg?height=455&width=576&top_left_y=387&top_left_x=64)
![](https://cdn.mathpix.com/cropped/b9128ba4-0753-416f-b579-a2696694bddc-10.jpg?height=449&width=576&top_left_y=389&top_left_x=646)

> **Key Concept**: Scatterplots provide visual evidence of relationships between two variables. The house price-size scatterplot shows a clear positive relationship: as size increases, price tends to increase. Scatterplots should always be examined before computing correlation or regression to check for outliers, nonlinearity, and the strength of the relationship.

Scatterplots let us see relationships visually. But we also need a numerical measure—a single number that summarizes the strength and direction of the relationship. This is where the correlation coefficient comes in. Correlation quantifies what the scatterplot shows qualitatively.

## 5.4 Sample Correlation

**In this section:**
- 5.4.1 Sample covariance
- 5.4.2 Sample correlation coefficient
- 5.4.3 Interpreting correlation strength
- 5.4.4 Autocorrelations for time series data

- The correlation coefficient is a standard way to measure association between x and y
- The sample correlation coefficient is a unit-free measure ranging from negative 1 to 1, where: r-sub-x-y equals 1 means perfect positive correlation, 0 less than r-sub-x-y less than 1 means positive correlation, r-sub-x-y equals 0 means no correlation, negative 1 less than r-sub-x-y less than 0 means negative correlation, and r-sub-x-y equals negative 1 means perfect negative correlation.

- For the house price and size data: r-sub-x-y equals 0.786.


### 5.4.1 Sample Covariance

- Recall the sample variance: s-sub-x-squared equals one over n minus 1, times the sum from i equals 1 to n of the quantity x-sub-i minus x-bar, all squared.
- The sample covariance between x and y is similarly defined: s-sub-x-y equals one over n minus 1, times the sum from i equals 1 to n of the quantity x-sub-i minus x-bar, times the quantity y-sub-i minus y-bar.

**Understanding the sign of covariance:**

Suppose on average y increases as x increases. Consider what happens with each observation.

When x-sub-i is greater than x-bar, y-sub-i is typically greater than y-bar. This gives positive times positive, which equals positive.

When x-sub-i is less than x-bar, y-sub-i is typically less than y-bar. This gives negative times negative, which equals positive.

It follows that s-sub-x-y is greater than zero when variables move together.

An example is shown in the second panel on the earlier slide. Most observations are in quadrants where the product is positive. The data are positively correlated (s-sub-x-y equals 11,701,613.3).

Similarly, s-sub-x-y is less than zero if y decreases as x increases.

Thus the sign of covariance is easily interpreted. Positive covariance means positive association. Negative covariance means negative association.


### 5.4.2 Sample Correlation Coefficient

The sample correlation coefficient is defined as: r-sub-x-y equals the covariance divided by the product of standard deviations.

That is, r-sub-x-y equals s-sub-x-y divided by s-sub-x times s-sub-y.

Equivalently, r-sub-x-y equals the sum of products of deviations, divided by the square root of the sum of x-deviations squared times the sum of y-deviations squared.

**Key insight:** The correlation coefficient is the covariance between standardized versions of x and y. That is, r-sub-x-y equals the covariance of the quantity x minus x-bar divided by s-sub-x, and the quantity y minus y-bar divided by s-sub-y.

> **Key Concept**: The correlation coefficient is a scale-free measure of linear association ranging from negative 1 (perfect negative correlation) to positive 1 (perfect positive correlation). A correlation of 0 indicates no linear relationship. For house price and size, r equals 0.786 indicates strong positive correlation—as size increases, price tends to increase proportionally.


### 5.4.3 Interpreting Correlation Strength

- The four panels show: (1) strong positive correlation; (2) moderate positive correlation; (3) almost zero correlation, and (4) moderate negative correlation.
- Though there are no clear cutoffs for "weak", "moderate", or "strong" correlation.
![](https://cdn.mathpix.com/cropped/b9128ba4-0753-416f-b579-a2696694bddc-14.jpg?height=253&width=408&top_left_y=328&top_left_x=208)
![](https://cdn.mathpix.com/cropped/b9128ba4-0753-416f-b579-a2696694bddc-14.jpg?height=253&width=407&top_left_y=328&top_left_x=656)
![](https://cdn.mathpix.com/cropped/b9128ba4-0753-416f-b579-a2696694bddc-14.jpg?height=258&width=412&top_left_y=619&top_left_x=206)
![](https://cdn.mathpix.com/cropped/b9128ba4-0753-416f-b579-a2696694bddc-14.jpg?height=253&width=409&top_left_y=622&top_left_x=654)


### 5.4.4 Autocorrelations for Time Series Data

- For time series data, the autocorrelation at lag j is the correlation between current data and the data lagged j periods.
- For example, the correlation between y-sub-t and y-sub-t-minus-j.

> **Key Concept**: Correlation measures the strength and direction of linear association between two variables. It is scale-free (ranging from negative 1 to positive 1), making it useful for comparing relationships across different units. Autocorrelation extends correlation to time series, measuring how a variable relates to its own past values—important for detecting patterns and persistence over time.

Correlation tells us that house price and size are related (r equals 0.786). But it doesn't tell us how much price changes for each additional square foot. For that, we need regression—the most important tool in econometrics. Regression goes beyond correlation by giving us a formula: predicted price equals 115,017 plus 73.77 times size. This formula lets us make specific predictions and quantify the relationship.

## 5.5 Regression Line

**In this section:**
- 5.5.1 The residual
- 5.5.2 Least squares estimation
- 5.5.3 Interpretation of the slope coefficient
- 5.5.4 Example: house price regression
- 5.5.5 Intercept-only regression and the sample mean

- This is the key method in the analysis of economics data.
- The regression line from regression of y on x is denoted: y-hat equals b-one plus b-two times x

where:
- y is called the dependent variable
- y-hat is the predicted value or fitted value of the dependent variable
- x is the independent variable or explanatory variable or regressor variable or covariate
- b-one is the estimated y-axis intercept
- b-two is the estimated slope coefficient.


### 5.5.1 The Residual

- The residual e is the difference between the actual value of y and the predicted value y-hat: e equals y minus y-hat
- This is also denoted u-hat equals y minus y-hat.
![](https://cdn.mathpix.com/cropped/b9128ba4-0753-416f-b579-a2696694bddc-17.jpg?height=523&width=733&top_left_y=373&top_left_x=247)


### 5.5.2 Least Squares Estimation

**Step 1: Define the residuals**

For the first observation, the residual is e-one equals y-one minus y-hat-one.

For the second observation, the residual is e-two equals y-two minus y-hat-two.

For the i-th observation: e-sub-i equals y-sub-i minus y-hat-sub-i.

This can be written as e-sub-i equals y-sub-i minus b-one minus b-two times x-sub-i.

**Step 2: Choose the criterion**

The least squares method chooses b-one and b-two to minimize the sum of squared residuals.

That is, minimize e-one squared plus e-two squared plus dot-dot-dot plus e-n squared.

Equivalently, minimize the sum from i equals 1 to n of the quantity y-sub-i minus b-one minus b-two times x-sub-i, all squared.

**Step 3: Solve the minimization problem**

This is a calculus problem. Differentiate with respect to b-one and b-two.

Set both derivatives equal to zero. Solve the two equations for b-one and b-two.

The algebra is skipped here, but the solution is straightforward.

**The resulting formulas:**

The least squares slope is: b-two equals the sum of products of deviations, divided by the sum of x-deviations squared.

The least squares intercept is: b-one equals y-bar minus b-two times x-bar.

> **Key Concept**: The method of least squares chooses the regression line to minimize the sum of squared residuals. This yields formulas for the slope (b-two) and intercept (b-one) that can be computed from the data. The slope equals the covariance divided by the variance of x. This is the most widely used estimation method in econometrics.

**Why This Matters**: Among infinitely many possible lines through a scatterplot, least squares gives us one definitive "best fit" line—the one that makes prediction errors as small as possible in the squared error sense. This objective criterion means two economists analyzing the same data will always get the same regression line, making results reproducible and comparable across studies. This is why OLS (ordinary least squares) is the foundation of applied econometrics. Chapter 6 explores the statistical properties of the OLS estimator in greater depth.

### 5.5.3 Interpretation of the Slope Coefficient

- The slope coefficient b-two gives the slope: delta y-hat divided by delta x equals b-two.

- Reason: If the regressor changes by delta-x from x to x plus delta-x, then the fitted value y-hat changes from b-one plus b-two times x to b-one plus b-two times the quantity x plus delta-x, which equals b-one plus b-two times x plus b-two times delta-x, a change of b-two times delta-x.
- It follows that delta y-hat equals b-two times delta-x.
- The slope coefficient b-two is therefore easily interpreted as the change in the predicted value of y when x increases by one unit.
- The same result can be obtained using calculus methods, since y-hat equals b-one plus b-two times x has derivative d y-hat by d-x equals b-two.

> **Key Concept**: The slope coefficient measures the change in y associated with a one-unit change in x. For house prices, b-two equals 73.77 means each additional square foot of size is associated with a 73.77 dollar increase in price. This is the most important interpretable quantity in regression analysis—it tells us the magnitude of the relationship between the variables.


### 5.5.4 Example: House Price Regression

- Fitted regression

**Example 5.6**: Fitted Regression Line for House Price

Predicted Price equals 115,017 plus 73.77 times Size.

- The slope coefficient equals 73.77
- One more square foot in size is associated with a 73.77 dollar increase in the house price
- Equivalently, an additional small room of size ten feet by ten feet, or 100 square feet, is associated with a 100 times 73.77 equals 7,377 dollar increase in house price.
- The figure shows the scatterplot and least squares regression line.
![](https://cdn.mathpix.com/cropped/b9128ba4-0753-416f-b579-a2696694bddc-22.jpg?height=645&width=876&top_left_y=186&top_left_x=206)


### 5.5.5 Intercept-Only Regression and the Sample Mean

- OLS regression of y on just an intercept—that is, minimizing the sum from i equals 1 to n of the quantity y-sub-i minus b-one, all squared—yields b-one equals y-bar.
- So regression of y on only an intercept yields the sample mean y-bar
- OLS regression is a natural extension of univariate statistics based on the sample mean (see Chapter 3)
- And univariate statistics based on the sample mean is just a special case of OLS regression.

> **Key Concept**: The regression line y-hat equals b-one plus b-two times x is the foundation of econometric analysis. It summarizes the linear relationship between two variables and provides predictions. The slope b-two is the most important parameter, measuring how much y changes for a one-unit change in x. The intercept b-one is often less meaningful, representing the predicted y when x equals 0, which may be outside the data range.

We now have a regression line with slope 73.77 and intercept 115,017. But how good is this fit? Does size explain most of the variation in price, or only a small fraction? To answer these questions, we need measures of model fit—statistics that tell us how well the regression line captures the data.

## 5.6 Measures of Model Fit

**In this section:**
- 5.6.1 Standard error of the regression
- 5.6.2 Definition of R-squared
- 5.6.3 Visual example of total and explained variation
- 5.6.4 Computing R-squared from sums of squares
- 5.6.5 Alternative R-squared formula
- 5.6.6 R-squared equals squared correlation
- 5.6.7 Interpreting R-squared values
- 5.6.8 When low R-squared is acceptable
- 5.6.9 Computing R-squared for house price data

- Two standard measures assess model fit.
- The standard error of the regression measures the standard deviation of the residuals.
- R-squared (R-squared) measures the fraction of the variation of y (around the sample mean y-bar) that is explained by the regressors.
- Provided the regression includes an intercept: 0 is less than or equal to R-squared, which is less than or equal to 1. R-squared equals 0 implies no relationship between y and x, as y-hat-sub-i equals y-bar for all i. R-squared equals 1 implies the regression line perfectly fits y, as y-hat-sub-i equals y-sub-i for all i.
- R-squared equals r-sub-x-y squared, meaning R-squared equals the squared correlation coefficient
- R-squared equals the squared correlation between y and x (that is, R-squared equals r-sub-x-y squared)
- R-squared also equals the squared correlation between y and fitted values y-hat.


### 5.6.1 Standard Error of the Regression

The standard error of the regression is: s-sub-e-squared equals one over n minus 2, times the sum from i equals 1 to n of the quantity y-sub-i minus y-hat-sub-i, all squared.

- This is also called the root mean squared error of the residual.
- This measures the closeness of the fitted values y-hat-sub-i to the actual values y-sub-i
- It is essentially the average of the squared residuals, except that division is by n minus 2 rather than n.
- Lower values of s-sub-e mean fitted values are closer to actual values, but s-sub-e is not scale-free.


### 5.6.2 Definition of R-Squared

R-squared measures the fraction of variation in y that is explained by the regression.

**Step 1: Measure total variation in y**

Total sum of squares measures variability in y around its mean.

Total SS equals the sum from i equals 1 to n of the quantity y-sub-i minus y-bar, all squared.

**Step 2: Measure explained variation**

Explained sum of squares measures variability in fitted values around y-bar.

Explained SS equals the sum from i equals 1 to n of the quantity y-hat-sub-i minus y-bar, all squared.

This is also called regression sum of squares or model sum of squares.

**Step 3: Calculate the fraction**

R-squared equals Explained SS divided by Total SS.

This gives the fraction of total variation explained by the regression.

> **Key Concept**: R-squared measures the fraction of variation in y explained by the regression on x. It ranges from 0 (no explanatory power) to 1 (perfect fit). R-squared equals 0.62 means 62 percent of house price variation is explained by size variation—the remaining 38 percent is due to other factors not captured by size alone.

### 5.6.3 Visual Example of Total and Explained Variation

- The left panel shows Total SS: the deviations of y-sub-i minus y-bar for five data points. The right panel shows Explained SS: the deviations of y-hat-sub-i minus y-bar for five data points.
![](https://cdn.mathpix.com/cropped/b9128ba4-0753-416f-b579-a2696694bddc-27.jpg?height=446&width=558&top_left_y=368&top_left_x=62)
![](https://cdn.mathpix.com/cropped/b9128ba4-0753-416f-b579-a2696694bddc-27.jpg?height=446&width=553&top_left_y=368&top_left_x=649)


### 5.6.4 Computing R-Squared from Sums of Squares

- For the data in the previous figure: Total SS is approximately negative 1.3 squared plus negative 1.3 squared plus negative 1.5 squared plus 1.4 squared plus 2.7 squared, which equals 14.8. Explained SS is approximately negative 2.1 squared plus negative 1.1 squared plus 0.0 squared plus 1.0 squared plus 2.2 squared, which equals 11.46. R-squared is approximately 11.46 divided by 14.88, which equals 0.77.

- R-squared equals 0.77 means 77 percent of the variation in y is explained by regression on x.


### 5.6.5 Alternative R-Squared Formula

- Residual sum of squares measures variability in fitted value y-hat around y: Residual SS equals the sum from i equals 1 to n of the quantity y-sub-i minus y-hat-sub-i, all squared.

- For regression including an intercept, it can be shown that: Total SS equals Explained SS plus Residual SS.

- As a result, R-squared can be equivalently defined as: R-squared equals 1 minus the fraction Residual SS divided by Total SS, which equals 1 minus the sum from i equals 1 to n of the quantity y-sub-i minus y-hat-sub-i, all squared, divided by the sum from i equals 1 to n of the quantity y-sub-i minus y-bar, all squared.

- So least squares maximizes R-squared as it minimizes Residual SS.


### 5.6.6 R-Squared Equals Squared Correlation

- For regression of y on x that includes an intercept, we have the following two results.
- R-squared equals the squared correlation coefficient between y and x: R-squared equals r-sub-y-x squared.

- R-squared also equals the squared correlation coefficient between y and the fitted value y-hat: R-squared equals r-sub-y-y-hat squared.

- The second result extends to regression with additional regressors.

> **Key Concept**: For bivariate regression, R-squared equals the squared correlation coefficient (R-squared equals r-sub-x-y squared). This connects the two main measures of association: correlation (scale-free association) and R-squared (fraction of variance explained). Both measure the same underlying relationship but express it differently.


### 5.6.7 Interpreting R-Squared Values

- Clearly R-squared approximately 0 is poor fit and R-squared approximately 1 is an excellent fit, but there is no rule for where R-squared becomes large enough that the fit moves from poor to good.
- The value of R-squared varies with the level of aggregation of data: R-squared is low for individual-level regression of earnings on education, but R-squared is higher using aggregated data, such as state-level regression of state-average earnings on state-average schooling.
- The value of R-squared also depends on the choice of dependent variable: transforming y to a more symmetric distribution may increase R-squared, and regression of levels y-sub-t has higher R-squared than regression of changes delta y-sub-t.
- For bivariate regression, use R-squared to compare models with the same dependent variable y, but not to compare models with different dependent variables.


### 5.6.8 When Low R-Squared Is Acceptable

- Low values of R-squared do not mean that regression analysis is without merit.
- Example: Regression of earnings on education usually indicates a substantial effect of education—for example, one more year of education is associated with a 6 percent increase in annual earnings—yet R-squared in regressions using individual-level data is very low, such as R-squared equals 0.10.
- Explanation: On average there is a large effect of schooling on earnings. At the individual level, however, there is considerable variability in earnings even for people with the same level of education. On average, society's earnings may increase with more education, but there is great uncertainty as to whether any one given individual will necessarily see increased earnings.

> **Key Concept**: Low R-squared does not mean regression is uninformative. Individual-level data often have low R-squared, yet the regression coefficient may be statistically significant and economically important. What matters is whether the coefficient accurately measures the average relationship and is precisely estimated relative to its standard error.


### 5.6.9 Computing R-Squared for House Price Data

- Regression output will automatically include R-squared, and often adjusted R-squared.
- Here we compute from formulas, using sums of squares that are given in the "analysis of variance" table often included with regression output.

The calculations are: Explained SS equals 24,170,725,242, Residual SS equals 14,975,101,655, Total SS equals 39,145,826,897. R-squared is approximately 24,170,725,242 divided by 39,145,826,897, which equals 0.6175. Alternatively, R-squared is approximately 1 minus the fraction 14,975,101,655 divided by 39,145,826,897, which also equals 0.6175.

- Thus 61.75 percent of the variation in house price is associated with variation in house size. This is viewed as a good fit, though still with room for improvement.

**Quick Check**: Before moving forward, make sure you can answer these questions: (1) What does R-squared equal 0.62 mean in plain English? (2) If two variables have correlation r equals 0.8, what is R-squared? (3) Can R-squared be negative? These connections between correlation and R-squared will appear repeatedly in econometrics.

## 5.7 Computer Output following OLS Regression

**Example 5.7**: Computer Output from OLS Regression

Computer output typically includes an ANOVA table, coefficient table, and summary statistics. The ANOVA table shows: Explained source with SS equals 2.4171 times 10 to the 10th, df equals 1, MS equals 2.4171 times 10 to the 10th, F equals 43.58, p equals 0.000. Residual source with SS equals 1.4975 times 10 to the 10th, df equals 27, MS equals 5.546 times 10 to the 8th. Total source with SS equals 3.9146 times 10 to the 10th, df equals 28, MS equals 1.3981 times 10 to the 9th.

The coefficient table shows: Size regressor with coefficient 73.77, standard error 11.17, t-statistic 6.60, p-value 0.000, 95 percent confidence interval from 50.84 to 96.70. Intercept with coefficient 115,017, standard error 21,489, t-statistic 5.35, p-value 0.000, 95 percent confidence interval from 70,925 to 159,110.

Summary statistics include: 29 observations, F with 1 and 27 degrees of freedom equals 43.58, p-value for F equals 0.0000, R-squared equals 0.618, Adjusted R-squared equals 0.603, Standard error of regression equals 23,551.

> **Key Concept**: Computer output from regression provides comprehensive information: coefficients and their standard errors, t-statistics and p-values for hypothesis testing, R-squared and adjusted R-squared for model fit, F-statistic for overall significance, and the ANOVA decomposition showing explained and residual variation. Understanding how to read regression output is essential for applied econometrics. Chapter 7 covers how to use these statistics for formal statistical inference about regression coefficients.


## 5.8 Prediction

- For x equals x-star, the prediction of y is: y-hat equals b-one plus b-two times x-star.

- Example: A house of size 2000 square feet has predicted price of 263,000 dollars, since y-hat equals 115,000 plus 74 times 2000, which equals 263,000.
- In-sample prediction uses the sample x-sub-i values, and then y-hat-sub-i is called the fitted value.
- Out-of-sample prediction: predictions can be poor if we extrapolate to values x-star outside the sample range of x.
- We distinguish between two different uses of a prediction:
  - **Prediction of an average outcome** - for example, average price for a house of 2000 square feet
  - **Prediction of an individual outcome** - for example, price for a particular house of 2000 square feet

**Why This Matters**: Regression isn't just an academic exercise—it's a prediction machine. Real estate agents use regressions like this to price homes. Banks use them to estimate property values for mortgages. City planners use them to forecast tax revenue. But the key limitation is extrapolation: predicting the price of a 5,000 square foot mansion based on data from 1,400-3,300 square foot homes is unreliable. Always check whether your prediction falls within the range of your data.

### 5.8.1 Outlying Observations and Influential Points

- An outlier or outlying observation is one that is a relatively large distance from the bulk of the data.
- A scatter plot is a useful visual tool.
- An observation with a large value for the product of x-sub-i minus x-bar, times y-sub-i minus y-bar, can have a big influence on b-two. This is the case for observations that are a long way from both x-bar and y-bar.
- An outlier may be due to miscoded data.

> **Key Concept**: Predictions extrapolate the regression line to new values of x. In-sample predictions use observed x values (fitted values). Out-of-sample predictions use new x values, but can be unreliable if extrapolating far beyond the sample range. Outliers can strongly influence regression estimates, especially if they are far from both means, and should be examined via scatterplots and investigated for possible data errors.


## 5.9 Regression and Correlation

- Note: The sum from i equals 1 to n of the quantity x-sub-i minus x-bar, times y-sub-i minus y-bar, appears in definitions of both b-two and r-sub-x-y.
- In fact, the slope coefficient b-two equals r-sub-x-y times s-sub-y divided by s-sub-x.

- Reason: r-sub-x-y times s-sub-y divided by s-sub-x equals the quantity s-sub-x-y divided by s-sub-x times s-sub-y, times s-sub-y divided by s-sub-x, which equals s-sub-x-y divided by s-sub-x squared, which equals b-two.
- So r-sub-x-y greater than 0 implies b-two greater than 0, and r-sub-x-y less than 0 implies b-two less than 0.
- Also, b-two from regressing the quantity y-sub-i minus y-bar divided by s-sub-y on the quantity x-sub-i minus x-bar divided by s-sub-x equals r-sub-x-y.
- So r-sub-x-y measures the number of standard deviations that y changes by as x changes by one standard deviation.
- For example, if r-sub-x-y equals 0.5, s-sub-x equals 2 and s-sub-y equals 10, then a one standard deviation change in x is associated with a 0.5 standard deviations change in y.

> **Key Concept**: The regression slope equals the correlation times the ratio of standard deviations: b-two equals r-sub-x-y times s-sub-y divided by s-sub-x. This formula connects regression and correlation—they measure the same relationship but in different units. Regression assigns a direction (y depends on x), while correlation is symmetric and doesn't assign direction.


## 5.10 Causation

**In this section:**
- 5.10.1 Association versus causation
- 5.10.2 Reverse regression and asymmetry

- The correlation coefficient always treats x and y neutrally
- Regression does not: The slope b-two from regressing y on x does not equal the inverse of slope c-two from reverse regressing x on y. This is explained below.

- The data alone cannot tell us which direction, if any, is appropriate
- If we estimate y equals b-one plus b-two times x, without further information, we can say that a one unit increase in x is associated with a b-two increase in y, but we cannot say that a one unit increase in x causes a b-two increase in y.


### 5.10.1 Association Versus Causation

- For example: a medical study might find that alcohol consumption is associated with depression, but is it alcohol consumption that causes depression, or is it depression that leads to alcohol consumption?
- Many examples exist where the direction of causation is questionable.
- Often it is due to a third variable that may be driving both y and x.
- For example: higher education is positively associated with higher earnings, but this may be due solely to unobserved innate ability that leads to both higher earnings due to higher productivity and to higher education due to ability to study more advanced material.
- Establishing causation requires careful thinking about confounding variables, reverse causality, and selection bias—topics covered extensively in Chapter 17.

> **Key Concept**: Regression measures association, not causation. A regression coefficient shows how much y changes when x changes, but does not prove that x causes y. Causation requires additional assumptions or experimental design (covered in Chapter 17). Correlation does not imply causation—it only tells us that variables move together.


### 5.10.2 Reverse Regression and Asymmetry

- Regression of y on x: y-hat equals b-one plus b-two times x
- Reverse regression (of x on y): x-hat equals c-one plus c-two times y.
- Then c-two does not equal 1 divided by b-one!
- In fact, c-two equals b-two times the quantity s-sub-x squared divided by s-sub-y squared.
- For the house data: Regression of house price on house size gives b-two equals 73.77. Reverse regression of house size on house price gives c-two equals 0.0084. Whereas 1 divided by b-two equals 1 divided by 73.77, which equals 0.0136, which does not equal 0.0084.

> **Key Concept**: Causation requires more than association. Regression shows that x and y are related, but doesn't prove x causes y. Confounding variables, reverse causality, or selection bias can create associations without causation. Establishing causation requires experimental design, natural experiments, or advanced techniques (Chapter 17). Regression is directional and asymmetric: regressing y on x gives a different slope than regressing x on y, and the two slopes are not reciprocals.


## 5.11 Computations for Correlation and Regression

**In this section:**
- 5.11.1 Computing the fitted line
- 5.11.2 Computing R-squared
- 5.11.3 Computing the correlation coefficient

- We use artificial data on number of vehicles per household (y) and household size (x)
- n equals 5, with the pairs: (x-one, y-one) equals (1, 1), (x-two, y-two) equals (2, 2), (x-three, y-three) equals (3, 2), (x-four, y-four) equals (4, 2), and (x-five, y-five) equals (5, 3).
- Recall we want b-two equals the sum from i equals 1 to n of the quantity x-sub-i minus x-bar, times y-sub-i minus y-bar, divided by the sum from i equals 1 to n of the quantity x-sub-i minus x-bar, all squared.

**Example 5.8**: Manual Computation of Regression Coefficients

The computation table shows: For i equals 1, x-sub-i equals 1, y-sub-i equals 1, x-sub-i minus x-bar equals negative 2, y-sub-i minus y-bar equals negative 1, their product equals 2, and x-sub-i minus x-bar squared equals 4. For i equals 2 through 5, we continue similarly. The sums are: sum of x-sub-i equals 15, sum of y-sub-i equals 10, sum of x-sub-i minus x-bar equals 0, sum of y-sub-i minus y-bar equals 0, sum of products equals 4, sum of x-sub-i minus x-bar squared equals 10. The means are x-bar equals 3 and y-bar equals 2.

### 5.11.1 Computing the Fitted Line

The slope, intercept and line are computed as follows: b-two equals the sum from i equals 1 to n of the quantity x-sub-i minus x-bar, times y-sub-i minus y-bar, divided by the sum from i equals 1 to n of the quantity x-sub-i minus x-bar, all squared, which equals 4 divided by 10, which equals 0.4. b-one equals y-bar minus b-two times x-bar, which equals 2 minus 0.4 times 3, which equals 0.8. Therefore, y-hat equals 0.8 plus 0.4 times x.

- The fitted values of y-hat equals 0.8 plus 0.4 times x for the five observations are: 1.2, 1.6, 2, 2.4, and 2.8.


### 5.11.2 Computing R-Squared

The sum of squared residuals is: the sum from i equals 1 to n of the quantity y-sub-i minus y-hat-sub-i, all squared, which equals 1 minus 1.2, all squared, plus 2 minus 1.6, all squared, plus 2 minus 2, all squared, plus 2 minus 2.4, all squared, plus 3 minus 2.8, all squared, which equals 0.4.

The total sum of squares is: the sum from i equals 1 to n of the quantity y-sub-i minus y-bar, all squared, which equals 1 minus 2, all squared, plus 2 minus 2, all squared, plus 2 minus 2, all squared, plus 2 minus 2, all squared, plus 3 minus 2, all squared, which equals 2.0.

R-squared equals 1 minus 0.4 divided by 2.0, which equals 0.8.

- So 80 percent of the variation in number of cars is explained by household size.
- Note that the explained sum of squares is 2.0 minus 0.4, which equals 1.6.


### 5.11.3 Computing the Correlation Coefficient

The sample correlation coefficient is: r-sub-x-y equals the sum from i equals 1 to n of the quantity x-sub-i minus x-bar, times y-sub-i minus y-bar, divided by the square root of the sum from i equals 1 to n of the quantity x-sub-i minus x-bar, all squared, times the sum from i equals 1 to n of the quantity y-sub-i minus y-bar, all squared, which equals 4 divided by the square root of 10 times 2, which equals 2 divided by the square root of 5, which equals 0.894.

- This is close to one, so there is strong positive association between cars and household size.
- As expected, r-sub-x-y squared equals 2 divided by the square root of 5, all squared, which equals 4 divided by 5, which equals 0.8, which equals R-squared.

> **Key Concept**: The formulas for b-two, b-one, R-squared, and r can be computed manually for small datasets, helping build intuition for how least squares works. In practice, statistical software performs these calculations. The key insight is that all quantities are based on sums of products and sums of squares of deviations from means.


## 5.12 Nonparametric Regression

- A flexible method for exploratory data analysis is nonparametric regression. Here the relationship appears to be linear.
- Local linear and lowess are two commonly-used methods.

Nonparametric regression
![](https://cdn.mathpix.com/cropped/b9128ba4-0753-416f-b579-a2696694bddc-45.jpg?height=473&width=703&top_left_y=372&top_left_x=365)

> **Key Concept**: Nonparametric regression (local linear, lowess) provides flexible alternatives to linear regression by not assuming a specific functional form. These methods are useful for exploratory analysis, checking whether the linear model is appropriate, and identifying nonlinear patterns in the data.

---

## Key Takeaways

**Visualization and Correlation:**
- Two-way tabulations, scatterplots, and correlation are essential first steps in bivariate analysis
- Scatterplots provide visual evidence of relationships and help identify outliers and nonlinear patterns
- Two-way tabulations with expected frequencies enable chi-squared tests of independence for categorical data
- The correlation coefficient (r) is a scale-free measure of linear association ranging from negative 1 to positive 1
- Covariance measures the direction of association but depends on the units of measurement
- For house price and size, r equals 0.786 indicates strong positive linear association
- Autocorrelation extends correlation to time series, measuring how a variable relates to its own past values

**Regression Analysis and Interpretation:**
- The regression line y-hat equals b-one plus b-two times x is estimated by ordinary least squares (OLS), which minimizes the sum of squared residuals
- The slope b-two measures the change in y for a one-unit change in x and is the most important interpretable quantity
- For house prices, b-two equals 73.77 means each additional square foot is associated with a 73.77 dollar price increase
- The intercept b-one represents the predicted y when x equals 0 (often not meaningful if x equals 0 is outside the data range)
- Residuals (e equals y minus y-hat) measure prediction errors; OLS makes the sum of squared residuals as small as possible
- Regression of y on only an intercept yields the sample mean as the fitted value, showing OLS generalizes univariate statistics
- The formulas b-two equals the sum of products divided by the sum of x-deviations squared, and b-one equals y-bar minus b-two times x-bar, enable manual computation
- The regression slope equals b-two equals r-sub-x-y times s-sub-y divided by s-sub-x, connecting regression and correlation

**Model Fit and Evaluation:**
- R-squared measures the fraction of variation in y explained by x, ranging from 0 (no fit) to 1 (perfect fit)
- R-squared equals Explained SS divided by Total SS, which equals 1 minus Residual SS divided by Total SS
- For bivariate regression, R-squared equals r-sub-x-y squared (squared correlation coefficient)
- For house prices, R-squared equals 0.618 means 62 percent of price variation is explained by size variation
- Standard error of regression (s-sub-e) measures the typical size of residuals in the units of y
- Low R-squared doesn't mean regression is uninformative—the coefficient can still be statistically significant and economically important
- R-squared depends on data aggregation and choice of dependent variable; use it to compare models with the same dependent variable
- Computer regression output provides coefficients, standard errors, t-statistics, p-values, F-statistics, and ANOVA decomposition

**Prediction, Causation, and Extensions:**
- Predictions use y-hat equals b-one plus b-two times x-star to forecast y for a given x-star
- In-sample predictions use observed x values (fitted values); out-of-sample predictions use new x values
- Extrapolation beyond the sample range of x can be unreliable
- Outliers can strongly influence regression estimates, especially if far from both x-bar and y-bar
- Association does not imply causation—regression measures correlation, not causal effects
- Confounding variables, reverse causality, or selection bias can create associations without causation
- Establishing causation requires experimental design, natural experiments, or advanced econometric techniques (Chapter 17)
- Regression is directional and asymmetric: regressing y on x gives a different slope than regressing x on y
- The two slopes are NOT reciprocals, reflecting that regression treats y and x differently
- Nonparametric regression (local linear, lowess) provides flexible alternatives without assuming linearity
- Nonparametric methods are useful for exploratory analysis and checking the appropriateness of linear models

---

## Some in-class Exercises

(1) Suppose we have a sample with three observations with (x, y) equal to (1, 5), (2, 2) and (3, 2). Calculate the sum from i equals 1 to 3 of the quantity x-sub-i minus x-bar, times y-sub-i minus y-bar.
(2) Variables x and y have sample variances of, respectively, 100 and 25, and their sample covariance is 8. What is the sample correlation between the two variables?
(3) The sum from i equals 1 to 50 of the quantity x-sub-i minus x-bar, all squared, equals 100. The sum from i equals 1 to 50 of the quantity x-sub-i minus x-bar, times y-sub-i minus y-bar, equals 10. The sum from i equals 1 to 50 of the quantity y-sub-i minus y-bar, all squared, equals 25. Give the sample correlation between x and y.
(4) For the data of the previous example, what is the slope coefficient from regression of y on an intercept and x?
(5) Regression leads to fitted line y-hat equals 2 plus 3 times x. What is the residual for observation (x, y) equals (2, 9)?
(6) OLS regression of y on x for a sample of size 52 leads to residual sum of squares 20 and total sum of squares 50. Compute the standard error of the regression.
(7) For the data of the previous example, compute R-squared.
