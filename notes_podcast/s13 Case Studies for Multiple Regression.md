# Chapter 13: Case Studies for Multiple Regression

## Learning Objectives

By the end of this chapter, you will be able to:
- Apply multiple regression to analyze school performance and socioeconomic factors
- Use logarithmic transformations to estimate production functions
- Understand and test for constant returns to scale
- Identify and correct for omitted variables bias
- Apply cluster-robust standard errors for grouped data
- Understand randomized control trials and difference-in-differences methods
- Apply regression discontinuity design to causal questions
- Use instrumental variables to estimate causal effects
- Navigate the data cleaning and preparation process

---

## 13.1 Case Study 1: School Performance Index

**In this case study:**
- 13.1.1 California Academic Performance Index data
- 13.1.2 Univariate analysis
- 13.1.3 Bivariate analysis
- 13.1.4 Correlations among variables
- 13.1.5 Multiple regression results
- 13.1.6 Conclusion and implications

How do we encourage schools to become better?
- Many U.S. states score schools based on student performance on standardized tests
- in key subjects such as math and English conducted each year.
- Schools are expected to improve their scores over time.
- failure to do so can lead to intervention by state authorities.


### 13.1.1 California Academic Performance Index

Dataset API99 has data for 807 high schools in California in 1999 on the Academic Performance Index (API), which ranges from 200 to 1000 with a goal for schools to achieve API greater than 800. The dataset also includes socioeconomic variables like Edparent (average years of parent schooling), Meals (percentage of students in the lunch program), and Englearn (percentage of English learners), a school variable Yearround (indicating year-round schools), and teacher variables Credteach and Emerteach (percentages of teachers with full credentials and emergency credentials).

Looking at the key variables: The Academic Performance Index averages 620.94 with a standard deviation of 107.44, ranging from 355 to 966. Average years of schooling of parents averages 12.84 years with a standard deviation of 1.23, ranging from 9.62 to 16 years. The percentage of students in the lunch program averages 21.92 percent with a standard deviation of 23.67, ranging from 0 to 98 percent. The percentage of students who are English learners averages 14.00 percent with a standard deviation of 12.79, ranging from 0 to 66 percent. Year-round schools represent only 2 percent of the sample. The percentage of teachers with full credentials averages 89.84 percent with a standard deviation of 8.44, ranging from 33 to 100 percent. The percentage of teachers with emergency credentials averages 10.47 percent with a standard deviation of 8.21, ranging from 0 to 56 percent.

### 13.1.2 Univariate Analysis

Data are approximately normally distributed (by design)
![](https://cdn.mathpix.com/cropped/305edb9b-4075-41ef-9523-a058e126c526-05.jpg?height=415&width=546&top_left_y=325&top_left_x=78)
![](https://cdn.mathpix.com/cropped/305edb9b-4075-41ef-9523-a058e126c526-05.jpg?height=419&width=547&top_left_y=322&top_left_x=642)


### 13.1.3 Bivariate Analysis

**Example 13.1**: Bivariate Regression of API on Parent Education

The estimated API equals negative 400.31 plus 79.53 times Edparent. The standard error of the regression is 43.674, R-squared is 0.835, and adjusted R-squared is 0.834. Heteroskedastic-robust standard errors are shown in parentheses: 15.99 for the intercept and 1.22 for the slope.
- One more year of parent education is associated with 80 more points!
![](https://cdn.mathpix.com/cropped/305edb9b-4075-41ef-9523-a058e126c526-06.jpg?height=528&width=693&top_left_y=341&top_left_x=287)

> **Key Concept**: Parent education shows a strong positive association with school performance (API), with one additional year of parent education associated with approximately 80 more API points. However, this bivariate relationship doesn't account for other factors that might also influence school performance, such as student poverty levels or teacher quality.


### 13.1.4 Correlations

- Pairwise correlations are also moderate to high for several other variables

Examining the correlation matrix: API has a correlation of 0.91 with Edparent (extremely high), negative 0.54 with Meals, negative 0.66 with Englearn, negative 0.19 with Yearround, positive 0.46 with Credteach, and negative 0.45 with Emerteach. Edparent correlates negative 0.60 with Meals, negative 0.71 with Englearn, negative 0.25 with Yearround, positive 0.40 with Credteach, and negative 0.37 with Emerteach. Meals correlates positive 0.56 with Englearn, positive 0.29 with Yearround, negative 0.27 with Credteach, and positive 0.22 with Emerteach. Englearn correlates positive 0.22 with Yearround, negative 0.26 with Credteach, and positive 0.20 with Emerteach. Yearround correlates negative 0.18 with Credteach and positive 0.09 with Emerteach. Finally, Credteach correlates negative 0.82 with Emerteach (very strong negative correlation). Note that asterisks indicate statistical significance, and all these correlations are statistically significant.

### 13.1.5 Multiple Regression Results

**Example 13.2**: Multiple Regression of API on All Factors

When we regress API on all other regressors using default standard errors, the Edparent coefficient shows little change from 79.53 to 73.94. All six regressors are jointly statistically significant with an F-statistic of 771.4. The subset of five regressors other than Edparent is also statistically significant, with F equals 14.80 and p-value of 0.000. However, R-squared only increases to 0.853 from 0.835 with just Edparent alone.

Looking at individual coefficients: Edparent has a coefficient of 73.942 with a standard error of 1.835, giving a t-statistic of 40.29 and a p-value of 0.000. The 95 percent confidence interval runs from 70.339 to 77.545. Meals has a coefficient of 0.079 with standard error 0.092, t-statistic 0.86, and p-value 0.390, indicating it's not statistically significant. Englearn has a coefficient of negative 0.358 with standard error 0.177, t-statistic negative 2.02, and p-value 0.044—just barely significant. Yearround has a coefficient of 25.956 with standard error 10.752, t-statistic 2.41, and p-value 0.016—statistically significant. Credteach has a coefficient of 0.287 with standard error 0.349, t-statistic 1.11, and p-value 0.268—not significant. Emerteach has a coefficient of negative 1.470 with standard error 0.358, t-statistic negative 4.11, and p-value 0.000—highly significant. The intercept is negative 345.328 with standard error 44.027, t-statistic negative 7.84, and p-value 0.000.

For the overall model: n equals 807, F-statistic with 6 and 22 degrees of freedom equals 771.4, R-squared equals 0.853, adjusted R-squared equals 0.852, and the standard error of the regression equals 41.4.

> **Key Concept**: In multiple regression, the coefficient for parent education remains strong (73.94) even after controlling for other factors. The high correlation between socioeconomic variables makes it difficult to isolate the separate effects of other educational inputs like teacher quality. Some variables that appeared important in bivariate analysis become insignificant once we control for parent education.


### 13.1.6 Conclusion and Implications

- There is a very strong association of API with socioeconomic characteristics, particularly parental education.
- This makes it difficult to calculate the separate role of other educational inputs such as teacher quality.
- California also produced a "similar schools" index which controls for socioeconomic characteristics.


## 13.2 Cobb-Douglas Production Function

**In this case study:**
- 13.2.1 Natural logarithm transformation
- 13.2.2 Original Cobb-Douglas study data
- 13.2.3 Regression results
- 13.2.4 Testing specified parameter values
- 13.2.5 Testing constant returns to scale
- 13.2.6 Predicted output
- 13.2.7 Figures and visualization
- 13.2.8 Fitted isoquants
- 13.2.9 HAC-robust standard errors

- An important issue for determining market structure is whether or not returns to scale are constant, increasing or decreasing.
- For example, with increasing returns to scale a natural monopoly may arise.
- A production function models output (Q) as a function of capital (K) and labor (L), plus possibly extra inputs such as land.
- The Cobb-Douglas production function specifies that Q equals alpha times K to the power beta-two, times L to the power beta-three.

- With constant returns to scale, doubling both inputs leads to exactly doubling output. For Cobb-Douglas, this is the case if beta-two plus beta-three equals 1, versus increasing returns if the sum is greater than 1, and decreasing returns if the sum is less than 1.


### 13.2.1 Natural Logarithm Transformation

The model for Q is nonlinear in K and L, so OLS multiple regression seems impossible. But OLS is possible once we take logs.

Taking the natural logarithm of both sides: ln of Q equals ln of the quantity alpha times K to the beta-two times L to the beta-three. Using logarithm properties, this becomes ln of alpha plus ln of K to the beta-two, plus ln of L to the beta-three. This simplifies to ln alpha plus beta-two times ln K, plus beta-three times ln L. We can write this as beta-one plus beta-two times ln K, plus beta-three times ln L, where beta-one equals ln alpha.

- This result uses the properties of natural logarithm that ln of a times b equals ln a plus ln b, and ln of a to the power b equals b times ln a.
- So we do OLS regression of ln Q on an intercept, ln K and ln L.

> **Key Concept**: Taking natural logarithms of the Cobb-Douglas production function transforms a nonlinear model into a linear model suitable for OLS regression. The resulting coefficients are elasticities that can be directly interpreted: beta-two is the capital elasticity (percentage change in output from a 1 percent change in capital), and beta-three is the labor elasticity.


### 13.2.2 Original Cobb-Douglas Study Data

- Dataset COBBDOUGLAS has U.S. aggregate data on manufacturing for the 24 years from 1899 to 1922.
- From C.W. Cobb and P.H. Douglas (1928), "A Theory of Production," American Economic Review," pages 139-165.

Looking at the historical data from 1899 to 1922: In 1899, the baseline year, output (Q), capital (K), and labor (L) are all indexed at 100. Over the following years, all three variables generally trend upward. By 1911, output reached 153, capital 216, and labor 145. The peak output year was 1922 with Q at 240, capital at 431, and labor at 161. There was variability throughout the period, with a notable dip during 1914 when output fell to 169. The data show that capital grew more rapidly than labor over this period—capital more than quadrupled from 100 to 431, while labor increased by about 60 percent from 100 to 161. This differential growth allows us to estimate separate capital and labor effects on production.

### 13.2.3 Regression Results

**Example 13.3**: Cobb-Douglas Production Function Estimation

The regression results using HAC-robust standard errors with lag length 3 (shown in parentheses): The natural log of Q-hat equals negative 0.177 (standard error 0.398) plus 0.233 (standard error 0.062) times ln K, plus 0.807 (standard error 0.134) times ln L. The standard error of the regression is 0.0581, and R-squared is 0.957.

- The model fits the data very well with high R-squared.
- The coefficients of ln K and ln L are reasonably precisely estimated and highly statistically significant at level 0.05.
- The residuals are only slightly correlated, with first three autocorrelations of 0.11, negative 0.16, and negative 0.16.
- We use lag length m equals 3 based on the formula 0.75 times 24 to the power one-third, which equals 2.16.

> **Key Concept**: The estimated elasticities of capital (0.233) and labor (0.807) indicate that a 1 percent increase in capital increases output by 0.23 percent, while a 1 percent increase in labor increases output by 0.81 percent. Labor has a much stronger effect on production than capital in U.S. manufacturing during this historical period.


### 13.2.4 Testing Specified Parameter Values

- Cobb and Douglas did not estimate this model by linear regression. Instead, they set beta-two equal to 0.25 and beta-three equal to 0.75.
- Our estimated coefficients are b-two equals 0.233 and b-three equals 0.807.
- We test whether these are individually different from Cobb and Douglas's values at 5 percent significance.
- For example, testing the null hypothesis that beta-three equals 0.75 against the alternative that beta-three does not equal 0.75: the t-statistic equals the quantity 0.807 minus 0.75, divided by 0.134, which equals 0.425, with p-value 0.675. So the coefficient is not statistically different from 0.75 at level 5 percent.
- A joint test of the null hypothesis that beta-two equals 0.25 and beta-three equals 0.75, against the alternative that at least one differs: F equals 0.12 with p-value equal to the probability that F with 2 and 21 degrees of freedom exceeds 0.12, which is 0.889.
- The restrictions are not rejected at significance level 0.05.


### 13.2.5 Testing Constant Returns to Scale

Constant returns to scale holds if beta-two plus beta-three equals 1.
- Our sum b-two plus b-three equals 0.233 plus 0.807, which equals 1.040—quite close to 1.
- A formal test of the null hypothesis that beta-two plus beta-three equals 1 against the alternative that the sum does not equal 1: F equals 0.23 and p-value equals the probability that F with 1 and 21 degrees of freedom exceeds 0.23, which is 0.636.
- The restrictions are not rejected at significance level 0.05.
- The data are consistent with constant returns to scale.

> **Key Concept**: The test for constant returns to scale examines whether beta-two plus beta-three equals 1. The estimated sum is 1.040, and formal testing fails to reject constant returns to scale with p-value 0.636. This is consistent with the theoretical prediction for competitive markets where firms operate at efficient scale.


### 13.2.6 Predicted Output

**Example 13.4**: Predicting Output with Retransformation

The fitted log equation is: ln Q-hat equals negative 0.177 plus 0.233 times ln K, plus 0.807 times ln L.

- When predicting Q rather than ln Q, we need to allow for retransformation bias (covered in chapter 15.5).

To get Q-hat, we use the exponential function: Q-hat equals the exponential of s-e squared divided by 2, times the exponential of the quantity negative 0.177 plus 0.233 times ln K, plus 0.807 times ln L. This simplifies to the exponential of 0.0581 squared divided by 2, times the exponential of negative 0.177, times K to the 0.233, times L to the 0.807. Computing this gives Q-hat equals 0.839 times K to the 0.233, times L to the 0.807.

- This gives a sample mean of Q-hat equal to 166.0, quite close to the mean of Q of 165.9.
- The first panel of the next figure plots actual Q and predicted Q against time, and the fit is quite good aside from the final year.


### 13.2.7 Figures and Visualization

- The first panel plots actual Q and predicted Q against time.
- The second panel gives isoquants obtained next.
![](https://cdn.mathpix.com/cropped/305edb9b-4075-41ef-9523-a058e126c526-17.jpg?height=437&width=549&top_left_y=356&top_left_x=74)
![](https://cdn.mathpix.com/cropped/305edb9b-4075-41ef-9523-a058e126c526-17.jpg?height=441&width=549&top_left_y=356&top_left_x=641)


### 13.2.8 Fitted Isoquants

Isoquants give K as a function of L for different values of Q.

Starting from Q equals alpha times K to the beta-two times L to the beta-three, we can solve for K. First, K to the beta-two equals Q divided by the quantity alpha times L to the beta-three. Taking both sides to the power one over beta-two gives K equals alpha to the negative one over beta-two, times Q to the one over beta-two, times L to the negative beta-three over beta-two.

- Using our fitted values gives K equals 2.140 times Q to the 4.29, times L to the negative 3.46.
- This ignores log transformation bias for simplicity, which is small since the exponential of 0.0581 squared divided by 2 equals 1.0017, very close to 1.
- As expected, isoquants do not cross.


### 13.2.9 HAC-Robust Standard Errors

- For time series data, there is concern about serially correlated errors.
- This is less of a problem here as residual autocorrelations are relatively small: rho-hat-one equals 0.11, rho-hat-two equals negative 0.16, and rho-hat-three equals negative 0.16.
- We nonetheless used HAC standard errors with m equals 3.
- Comparing robust standard errors for b-one and b-two: default standard errors are 0.064 and 0.145, heteroskedastic-robust are 0.105 and 0.216, and HAC with m equals 3 are 0.062 and 0.134.

> **Key Concept**: For time series data, HAC (Heteroskedasticity and Autocorrelation Consistent) standard errors account for both changing error variances and correlation over time. They provide more reliable inference than default standard errors when these issues are present. In this case, the HAC standard errors are similar to default, suggesting serial correlation is not a major concern.


## 13.3 Case Study 3: Phillips Curve

**In this case study:**
- 13.3.1 U.S. price inflation data
- 13.3.2 Phillips curve pre-1970
- 13.3.3 Phillips curve post-1970
- 13.3.4 Augmented Phillips curve
- 13.3.5 Figures and visualization
- 13.3.6 Omitted variables bias analysis

- The Phillips curve plots price inflation against unemployment.
- A. W. Phillips (1958) found a negative relationship.
- An increase in money supply may stimulate the economy in the short-run, leading to lower unemployment, accompanied by some increase in prices.
- The importance is that policymakers could potentially lower unemployment at the mild expense of somewhat higher price inflation.
- But there is fierce debate as to whether this relationship holds in the long-run.


### 13.3.1 U.S. Price Inflation Data

Dataset PHILLIPS has annual U.S. data from 1949 to 2014. Inflation is based on the GDP implicit price deflator. Later analysis uses expectations of future price inflation from two sources: 1) Survey of Professional Forecasters from the Federal Reserve Bank of Philadelphia, and 2) an ad hoc measure as a weighted average of inflation over the past 4 years: p-dot-sub-t-expected equals 0.4 times p-dot-sub-t-minus-1, plus 0.3 times p-dot-sub-t-minus-2, plus 0.2 times p-dot-sub-t-minus-3, plus 0.1 times p-dot-sub-t-minus-4, where p-dot-sub-t is the inflation rate in year t.

Looking at the key variables: The civilian unemployment rate averages 5.87 percent over 66 observations, with a standard deviation of 1.63, ranging from 2.70 percent to a maximum not shown. Annual inflation rate averages 3.20 percent over 66 observations, with a standard deviation of 2.32, ranging from negative 1.97 to a maximum not shown. Expected inflation (forecast of one-year ahead inflation) averages 3.31 percent over 45 observations, with a standard deviation of 2.05, ranging from 1.14 to a maximum not shown. Past inflation (average over past 4 years) averages 3.65 percent over 63 observations, with a standard deviation of 2.04, ranging from 1.48 to a maximum not shown.

### 13.3.2 Phillips Curve Pre-1970

**Example 13.5**: Phillips Curve 1949-1969

The OLS regression from 1949 to 1969 looks good, showing the predicted negative relationship between inflation and unemployment. t-statistics in parentheses are based on HAC standard errors with m equals 3.

Inflation-hat equals 7.111 (t-statistic 4.49) minus 1.030 (t-statistic negative 3.17) times Urate. The standard error of the regression is 1.32, R-squared is 0.454, and n equals 21.

![](https://cdn.mathpix.com/cropped/305edb9b-4075-41ef-9523-a058e126c526-22.jpg?height=427&width=539&top_left_y=423&top_left_x=81)
![](https://cdn.mathpix.com/cropped/305edb9b-4075-41ef-9523-a058e126c526-22.jpg?height=432&width=543&top_left_y=423&top_left_x=644)

> **Key Concept**: The original Phillips curve showed a negative relationship between unemployment and inflation pre-1970: higher unemployment was associated with lower inflation. This suggested a policy trade-off between unemployment and inflation—policymakers could reduce unemployment by accepting higher inflation, or reduce inflation by accepting higher unemployment.


### 13.3.3 Phillips Curve Post-1970

**Example 13.6**: Phillips Curve 1970-2014

- The OLS regression from 1970 to 2014, with HAC t-statistics (m equals 5) in parentheses, looks bad.

Inflation-hat equals 1.923 (t-statistic 1.87) plus 0.266 (t-statistic 1.03) times Urate. The standard error of the regression is 2.44, R-squared is 0.258, and n equals 45.

- The relationship is now positive though statistically insignificant—the apparent "breakdown" of the Phillips curve.

> **Key Concept**: The Phillips curve relationship broke down post-1970, showing a positive (though insignificant) relationship between unemployment and inflation. This breakdown was a major challenge to macroeconomic theory and policy, suggesting the simple model was misspecified and that some important variable was being omitted.


### 13.3.4 Augmented Phillips Curve

**Example 13.7**: Augmented Phillips Curve 1970-2014

- The problem is that people's inflation expectations also matter. We add this as a regressor.
- The OLS regression from 1970 to 2014, with HAC t-statistics (m equals 5) in parentheses, now looks good.

Inflation-hat equals 0.270 (t-statistic 0.43) minus 0.128 (t-statistic negative 1.54) times Urate, plus 1.147 (t-statistic 13.58) times Expinflation. The standard error of the regression is 0.86, and R-squared is not shown but is presumably much higher.

- Urate is now negative, though statistically insignificant at 5 percent, and the Expinflation coefficient is close to 1.
- The augmented Phillips curve relationship can be represented by a series of regular Phillips curves, where each curve is given for a different expected inflation rate.
- For example, for an expected inflation rate of 2.0 percent, we have: Inflation-hat equals 0.270 minus 0.128 times Urate, plus 1.147 times 2, which simplifies to 2.559 minus 0.128 times Urate.

> **Key Concept**: The augmented Phillips curve adds expected inflation as a regressor. With this addition, the unemployment coefficient returns to negative and inflation expectations have a coefficient near 1, resolving the apparent breakdown of the relationship. This suggests that the Phillips curve exists conditional on inflation expectations, but expectations adjust over time.


### 13.3.5 Figures and Visualization

- The first panel shows a time series plot
- The second panel shows the augmented curve for 3 different expected inflation rates.
![](https://cdn.mathpix.com/cropped/305edb9b-4075-41ef-9523-a058e126c526-25.jpg?height=433&width=546&top_left_y=358&top_left_x=76)
![](https://cdn.mathpix.com/cropped/305edb9b-4075-41ef-9523-a058e126c526-25.jpg?height=436&width=547&top_left_y=358&top_left_x=641)


### 13.3.6 Omitted Variables Bias Analysis

- The observed sign reversal for the coefficient of Urate is a classic example of omitted variables bias.
- The true model is: Inflation equals beta-one plus beta-two times Urate, plus beta-three times Expinflation, plus u-sub-t.
- The incorrect bivariate model is: Inflation equals b-one plus b-two times Urate.
- From chapter 16.3, omitted variables bias formula: the expected value of b-two equals beta-two plus beta-three times gamma.
- Gamma is the coefficient of Urate in a regression of Expinflation on Urate.
- Here, a bivariate regression of Expinflation on Urate has slope of 0.343.
- Then the estimated expected value of b-two equals negative 0.128 plus 1.147 times 0.343, which equals 0.266.
- This exactly equals the estimated coefficient of Urate from the bivariate regression of Inflation on Urate.

> **Key Concept**: The sign reversal for the unemployment coefficient is a classic example of omitted variables bias. When expected inflation is omitted from the regression, the unemployment coefficient captures both the true negative effect of unemployment on inflation and a spurious positive correlation through expected inflation. The omitted variables bias formula perfectly predicts the magnitude of the biased coefficient.


## 13.4 Automobile Efficiency

- Was better fuel efficiency of cars negated by a switch to bigger more powerful cars?
- Dataset AUTOSMPG has annual data on most models of cars and light trucks on sale in the U.S. from 1980 to 2006, with n equals 27,871 observations.
- We model fuel efficiency (miles per gallon) which decreases with increased horsepower, car weight and torque.
- We estimate a log-log model.
- We find that greatly increased fuel efficiency from 1980 to 2006 has been completely negated by heavier more powerful vehicles.
- We use cluster-robust standard errors with clustering on car manufacturer because errors are correlated within manufacturer.


## 13.5 Rand Health Insurance Experiment

- Does better health insurance increase consumption of health care?
- This was a 1970s randomized control trial experiment designed to give a causal estimate by randomly assigning different levels of health insurance to different families.
- Dataset HEALTHINSEXP has 20,203 individual-year observations on 5,915 individuals in 2,205 families in the experiment for either 3 years or 5 years.
- We use data for the first year of the experiment and only selected variables.
- y equals total annual spending on health
- x includes six different insurance plans ranging from 0 percent coinsurance (free care) to 95 percent coinsurance.
- We find that spending increases with better health insurance.
- A joint F test finds this is statistically significant at 5 percent.
- We use cluster-robust standard errors with clustering on family.


## 13.6 Access to Health Care and Health Status

- Does greater access to health care improve health status?
- A 1994 South Africa policy change increased access to health care for children in communities with clinics.
- We use the difference-in-differences method to give a causal estimate: the change over time for treated children (those in communities with clinics) minus the change over time for untreated children (those in communities without clinics).
- Dataset HEALTHACCESS has data on children ages 0 to 4.
- The outcome is a weight-for-age z-score, normed to have mean 0 and standard deviation 1 for a representative worldwide population.
- The estimate is a 0.522 increase in weight-for-age z-score, and an increase of 0.516 when control variables are added.
- We use cluster-robust standard errors with clustering on community.


## 13.7 Gains to Political Incumbency

- Does being an incumbent increase the probability of winning the next election?
- We use the regression discontinuity method to give a causal estimate: compare party vote in the subsequent election if the party just won the senate seat versus if the party just lost the senate seat.
- Dataset INCUMBENCY has data on 1,390 Senate seat elections from 1914 to 2010.
- The estimated effect is a 5 percent to 7 percent increase in the vote if you win the previous election.
- We use heteroskedastic-robust standard errors. Cluster-robust standard errors with clustering on state are similar.


## 13.8 Institutions and Country GDP

- Do better institutions lead to higher GDP?
- We use the instrumental variables estimator (chapter 17.4) rather than OLS to get a causal estimate.
- Dataset INSTITUTIONS has data on 64 countries settled by Europeans.
- The outcome is log GDP per capita in 1995.
- The regressor is average protection against appropriation risk.
- The instrument is log settler mortality many years in the past.
- We find that better institutions lead to higher GDP.


## 13.9 From Raw Data to Final Data

- Going from raw data to a final dataset for analysis can be difficult—recently labelled as data carpentry or data wrangling.
- The first task is reading any sort of data into a statistical package: Excel spreadsheets (with extension xls or xlsx), plain text files with character-separated values (with extension csv), data files formatted for commonly-used statistical packages, tables in PDF documents (with extension pdf)—where hardcopy data may be scanned and digitized using programs like Adobe Acrobat—and web data obtained using web scraping programs.
- The second task is combining data from multiple sources. Merging data requires care.
- The third task is cleaning the data, which entails recoding data and detecting data that are in error.
- And in many places throughout this process: check the data.

---

## Key Takeaways

**School Performance and Socioeconomic Factors (Case Study 13.1):**
- School performance (API) is strongly associated with socioeconomic factors, particularly parent education
- Bivariate analysis shows 80 API points per year of parent education
- Multiple regression maintains strong effect (74 points) after controlling for other factors
- High correlations among socioeconomic variables make isolating individual effects challenging
- Teacher quality measures show mixed significance when socioeconomic factors are controlled
- California's "similar schools" index controls for socioeconomic characteristics

**Cobb-Douglas Production Function and Returns to Scale (Case Study 13.2):**
- Natural logarithm transformation converts nonlinear Cobb-Douglas model to linear OLS form
- Estimated capital elasticity is 0.233 and labor elasticity is 0.807
- Labor has much stronger effect on production than capital in U.S. manufacturing (1899-1922)
- Data support constant returns to scale (elasticities sum to 1.040, not significantly different from 1)
- HAC-robust standard errors account for time series correlation in error terms
- Model provides good predictions after accounting for retransformation bias
- Isoquants can be derived from estimated production function

**Phillips Curve and Omitted Variables Bias (Case Study 13.3):**
- Original Phillips curve showed negative relationship between unemployment and inflation pre-1970
- Simple Phillips curve broke down post-1970, showing positive (insignificant) relationship
- Augmented Phillips curve adding expected inflation resolves the breakdown
- Expected inflation coefficient near 1 in augmented model
- Sign reversal is classic example of omitted variables bias
- Omitted variables bias formula correctly predicts the biased coefficient
- Policy implications: augmented curve suggests limited long-run unemployment-inflation trade-off

**Advanced Causal Methods Overview (Case Studies 13.4-13.8):**
- **Log-log models (13.4)**: Automobile efficiency gains offset by larger vehicles; cluster-robust SE by manufacturer
- **Randomized control trials (13.5)**: Rand Health Insurance Experiment shows better insurance increases health spending
- **Difference-in-differences (13.6)**: South Africa clinic access improved child health outcomes
- **Regression discontinuity (13.7)**: Political incumbency provides 5-7 percent vote share advantage
- **Instrumental variables (13.8)**: Better institutions causally increase country GDP
- Each method addresses specific identification challenges for causal inference

**Data Preparation and Practical Workflow (Case Study 13.9):**
- Real data analysis requires extensive data carpentry or data wrangling
- Reading data from multiple sources: Excel, CSV, statistical formats, PDF, web scraping
- Merging data from multiple sources requires careful attention
- Data cleaning includes recoding and detecting errors
- Validation and checking at multiple stages essential
- Data preparation often most time-consuming phase of analysis

**General Lessons from Multiple Regression Case Studies:**
- Multiple regression isolates partial effects while controlling for other variables
- Choice of standard errors critical: heteroskedastic-robust, cluster-robust, or HAC-robust
- Log transformations enable estimation of elasticities and nonlinear relationships
- Omitted variables bias can reverse coefficient signs and lead to incorrect conclusions
- Causal inference requires additional identification strategies beyond OLS
- Data quality and preparation foundational to reliable analysis

---
