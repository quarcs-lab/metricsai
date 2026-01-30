# Chapter 8: Case Studies for Bivariate Regression

## Learning Objectives

By the end of this chapter, you will be able to:
- Apply bivariate regression analysis to real-world economic and health data
- Interpret regression results in the context of health outcomes, health spending, and GDP
- Understand and apply the Capital Asset Pricing Model (CAPM) using regression
- Analyze the relationship between output and unemployment using Okun's Law
- Compute and interpret heteroskedastic-robust standard errors
- Make predictions using estimated regression models
- Evaluate model fit using R-squared and other diagnostic measures

---

You've learned the theory of regression—how to estimate coefficients, calculate standard errors, and test hypotheses. Now it's time to see these tools in action with real data from health economics, finance, and macroeconomics. This chapter presents four case studies that demonstrate how bivariate regression answers important questions: Does health spending improve life expectancy? How risky is Coca-Cola stock? What's the relationship between economic growth and unemployment? Each case study reveals both the power and limitations of regression analysis.

## 8.1 Case Study 1: Health Outcomes across Countries

**In this case study:**
- 8.1.1 Life expectancy and health spending relationship
- 8.1.2 Infant mortality and health spending relationship
- 8.1.3 Further details and interpretation

Dataset HEALTH2009 has 2009 data for the 34 wealthy and relatively wealthy nations in the Organization of Economic and Community Development (OECD).
- Australia, Austria, Belgium, Canada, Chile, Czech Republic, Denmark, Estonia, Finland, France, Germany, Greece, Hungary, Iceland, Ireland, Israel, Italy, Japan, Korea, Luxembourg, Mexico, Netherlands, New Zealand, Norway, Poland, Portugal, Slovak Republic, Slovenia, Spain, Sweden, Switzerland, Turkey, United Kingdom, and United States.
- There is wide variation in annual health expenditures per capita and also in infant mortality.

Looking at the key variables in the HEALTH2009 dataset: Annual health expenditure per capita averages 3,256 US dollars with substantial variation—the standard deviation is 1,494 dollars. Health spending ranges from a minimum of 923 dollars to a maximum of 7,990 dollars. Male life expectancy at birth averages 76.7 years with a standard deviation of 2.94 years, ranging from 69.8 to 79.9 years. Infant mortality averages 4.44 deaths per 1,000 live births with a standard deviation of 2.72, ranging from 1.8 to 14.7 deaths per 1,000 births. This considerable variation across OECD countries provides an ideal setting for regression analysis.

### 8.1.1 Life Expectancy and Health Spending

**Example 8.1**: Regression of Life Expectancy on Health Spending

OLS regression yields the following results: Life expectancy equals 73.08 plus 0.00111 times health spending per capita. The intercept has a t-statistic of 71.36, and the slope has a t-statistic of 3.88. The R-squared is 0.320, the standard error of the regression is 2.46, and the sample size is 34 countries. Here, t-statistics are based on default standard errors shown in parentheses.

- The relationship is economically significant
- A 1,000 dollar increase in per capita health spending, which represents about two-thirds of a standard deviation change, is associated with an increase in life expectancy of 1.11 years.
- The relationship is highly statistically significant, with a t-statistic of 3.88.
- Here our prior belief is that beta-two is positive, so we perform a one-sided test of the null hypothesis that beta-two is less than or equal to zero, against the alternative that beta-two is greater than zero.
- The critical value c equals t with 32 degrees of freedom at the 0.05 level, which is 1.69. We reject the null hypothesis at significance level 0.05 since the t-statistic of 3.88 is greater than the critical value.
- Alternatively, the p-value equals the probability that T with 32 degrees of freedom exceeds 3.88, which equals 0.000 to three decimal places.

> **Key Concept**: The positive relationship between health spending and life expectancy suggests that countries investing more in healthcare tend to have better health outcomes. However, correlation does not imply causation—other factors like income, education, and lifestyle also matter. A one-percentage-point increase in health spending is associated with a measurable improvement in life expectancy, but we must be cautious about attributing this relationship solely to healthcare investment without controlling for confounding variables.


### 8.1.2 Infant Mortality and Health Spending

**Example 8.2**: Regression of Infant Mortality on Health Spending

- The second panel additionally studies infant mortality.
- The U.S. has much worse outcomes than predicted by the model.
![](https://cdn.mathpix.com/cropped/9d60cd7c-b37f-404c-8b9c-5eb8fb867709-05.jpg?height=431&width=541&top_left_y=360&top_left_x=77)
![](https://cdn.mathpix.com/cropped/9d60cd7c-b37f-404c-8b9c-5eb8fb867709-05.jpg?height=431&width=539&top_left_y=360&top_left_x=644)

> **Key Concept**: The negative relationship between health spending and infant mortality (higher spending leads to lower mortality) demonstrates the protective effect of healthcare investment on vulnerable populations. The strength of this relationship varies across income levels, with some countries achieving better health outcomes than others at similar spending levels.


### 8.1.3 Further Details and Interpretation

- For these cross-section data with independence across observations it is standard to use heteroskedastic-robust standard errors.
- For the life expectancy slope we obtain a heteroskedastic-robust standard error of 0.0004637 compared to the default of 0.000287
- The t-statistic falls to 2.40 from 3.88, but is still statistically significant at 5 percent.
- The plotted relationships appear to be nonlinear rather than linear
- Log-linear and log-log models are presented in Chapter 9.
- Bottom line: Country health outcomes improve on average with higher health spending
- The U.S. performs substantially worse than predicted.

**Why This Matters**: Healthcare policy debates often center on whether spending more money actually improves health. This regression provides evidence that it does—countries spending more tend to have longer life expectancies and lower infant mortality. But the U.S. spends far more than any other country yet achieves worse outcomes than predicted, suggesting that how money is spent matters as much as how much is spent. This is a puzzle that requires deeper multivariate analysis to understand.

The first case study examined health outcomes (life expectancy, infant mortality). Now let's flip the question: what drives health spending itself? Do wealthier countries simply spend more on healthcare because they can afford to?

## 8.2 Case Study 2: Health Expenditures across Countries

**In this case study:**
- 8.2.1 Health spending and GDP relationship
- 8.2.2 Heteroskedastic-robust standard errors

- Again use dataset HEALTH2009.
- Health expenditure is measured per capita, and income is measured using GDP per capita.
- There is considerable variation in GDP per capita, measured in current US dollars at current exchange rates, ranging from 13,807 dollars for Mexico to 82,901 dollars for Luxembourg, a small European country with population of half a million.

Looking at the relationship between GDP and health spending: GDP per capita averages 33,054 US dollars with a standard deviation of 12,918 dollars, ranging from 13,807 to 82,901 dollars. Health expenditure per capita averages 3,256 US dollars with a standard deviation of 1,494 dollars, ranging from 923 to 7,990 dollars. This wide variation in both income and health spending across OECD countries allows us to examine how healthcare investment responds to national wealth.

### 8.2.1 Health Spending and GDP Relationship

**Example 8.3**: Regression of Health Spending on GDP per Capita

OLS regression yields the following results: Health spending per capita equals 285 plus 0.0899 times GDP per capita. The intercept has a t-statistic of 0.63, and the slope has a t-statistic of 6.99. The R-squared is 0.604, the standard error of the regression is 954, and the sample size is 34 countries. Here, t-statistics are based on default standard errors shown in parentheses.

- The slope coefficient estimate implies that an extra 1,000 dollars in GDP per capita is associated with an 89.90 dollar increase in per capita health expenditures.
- The relationship is highly statistically significant, with a t-statistic of 6.99.
- Here our prior belief is that beta-two is positive, so we perform a one-sided test of the null hypothesis that beta-two is less than or equal to zero against the alternative that beta-two is greater than zero.
- We again reject the null hypothesis.
- The U.S. has unusually high health expenditures, much higher than other countries and roughly 4,000 dollars more than predicted by the regression line.
- Similarly Luxembourg seems to be an outlier.
- The second panel drops the U.S. and Luxembourg, and the slope coefficient increases from 0.0809 to 0.01267 and R-squared increases to 0.928.
![](https://cdn.mathpix.com/cropped/9d60cd7c-b37f-404c-8b9c-5eb8fb867709-09.jpg?height=431&width=537&top_left_y=416&top_left_x=81)
![](https://cdn.mathpix.com/cropped/9d60cd7c-b37f-404c-8b9c-5eb8fb867709-09.jpg?height=432&width=541&top_left_y=416&top_left_x=644)

> **Key Concept**: Health spending rises with GDP, but the relationship is not proportional across all income levels. Wealthier countries tend to spend a larger share of their GDP on healthcare, reflecting both increased demand for health services and the ability to pay. The presence of outliers like the United States, which spends far more than predicted, highlights the importance of examining individual observations and understanding country-specific factors.


### 8.2.2 Heteroskedastic-Robust Standard Errors

- For these cross-section data with independence across observations it is standard to use heteroskedastic-robust standard errors
- For the life expectancy slope we obtain a heteroskedastic-robust standard error of 0.0293 compared to the default of 0.0129
- The t-statistic then falls to 3.08 from 6.99, but is still statistically significant at 5 percent.
- The large change is due to large residuals for the U.S. and Luxembourg.

> **Key Concept**: Heteroskedastic-robust standard errors adjust for the fact that prediction errors may vary across observations. When heteroskedasticity is present—meaning the variance of errors differs across observations—robust standard errors provide more reliable inference than conventional standard errors. This adjustment is particularly important when dealing with outliers or when error variance increases with the level of the explanatory variable.

We've seen regression applied to health economics with cross-sectional country data. Now let's shift to finance, where regression is used with time series data to measure risk. The Capital Asset Pricing Model (CAPM) is one of the most widely used applications of bivariate regression in finance—it appears in virtually every finance textbook and is used daily by investors worldwide.

## 8.3 Case Study 3: Capital Asset Pricing Model

**In this case study:**
- 8.3.1 Theory of CAPM
- 8.3.2 Estimated CAPM model
- 8.3.3 Robust standard errors for CAPM

- Dataset CAPM has monthly data from May 1983 to October 2013 on returns to holding stock in Coca-Cola, Target and Walmart, the one-month U.S. Treasury bill rate, and the market return, which is the value-weighted return on all stocks listed on the NYSE, AMEX and NASDAQ.

Examining the CAPM dataset: The market return averages 0.0091 (or 0.91 percent) per month with a standard deviation of 0.0456, ranging from negative 0.2254 to positive 0.1285. The one-month U.S. Treasury bill rate averages 0.0035 (or 0.35 percent) with a standard deviation of 0.0022, ranging from 0.0000 to 0.0100. For individual stocks, Coca-Cola's return averages 0.0137 with a standard deviation of 0.0618, ranging from negative 0.1909 to positive 0.2266. Target's return averages 0.0138 with a standard deviation of 0.0842, ranging from negative 0.4781 to positive 0.2673. Walmart's return averages 0.0156 with a standard deviation of 0.0703, ranging from negative 0.2698 to positive 0.2644. The excess market return (market return minus risk-free rate) averages 0.0055 with a standard deviation of 0.0456. Similarly, excess returns for Coca-Cola, Target, and Walmart average 0.0102, 0.0103, and 0.0121 respectively, with their own patterns of variation.

### 8.3.1 Theory of CAPM

RF is the risk-free interest rate, specifically the one-month U.S. Treasury bill rate.
- RM is the overall market return on stocks.
- The difference (RM minus RF) is the market excess return or the equity market premium.
- RA is the return on investment asset A—in this case, Coca-Cola.
- CAPM links the excess returns on individual investments to the market excess return.

The theoretical CAPM equation states that the expected value of the excess return on asset A (which is RA-sub-t minus RF-sub-t) equals beta-A times the expected value of the market excess return (which is RM-sub-t minus RF-sub-t).

- Beta-A is called the "beta" and is on average one across the market.
- We estimate this relationship by OLS using the regression equation: The excess return on asset A equals alpha-A plus beta-A times the market excess return, plus an error term u-sub-t.

> **Key Concept**: CAPM posits that a stock's expected return depends on its systematic risk, measured by beta, which quantifies how much the stock moves with the overall market. A beta greater than 1 means the stock is more volatile than the market; a beta less than 1 means less volatile. This framework allows investors to understand the risk-return tradeoff and to evaluate whether a stock's return is appropriate given its level of systematic risk.


### 8.3.2 Estimated CAPM Model

**Example 8.4**: CAPM Beta Estimation

- OLS regression gives the fitted CAPM model for Coca-Cola, where the excess return on Coca-Cola equals 0.00681 plus 0.6063 times the market excess return. The intercept has a standard error of 0.00295, and the slope has a standard error of 0.0644. The R-squared is 0.201. Here, default standard errors are given in parentheses.

- The slope coefficient is the stock's beta
- It is statistically different from zero, as shown by the calculation: t equals 0.6063 divided by 0.0644, which equals 9.41. This exceeds the critical value t with 0.025 significance and 352 degrees of freedom, which is 1.967.

- The beta is also statistically different from one: t equals the quantity 0.6063 minus 1, divided by 0.0644, which equals negative 6.11.
- This classifies Coca-Cola as a value stock since beta lies between 0 and 1.
- Large companies such as Coca-Cola generally move less than the market as a whole, leading to beta less than 1.
- The intercept coefficient is the stock's alpha, which is a risk-adjusted measure of stock performance that measures the return in excess of that expected given the riskiness of the stock.
- The CAPM model in its purest form restricts alpha to equal zero.
- This restriction is rejected: t equals 0.00681 divided by 0.00295, which equals 2.31, and this exceeds 1.967.
- Furthermore, the alpha is large in magnitude.
- For readability the first panel uses only the last 20 percent of the sample.
- The second panel uses all data from 1983 to 2013.
![](https://cdn.mathpix.com/cropped/9d60cd7c-b37f-404c-8b9c-5eb8fb867709-14.jpg?height=413&width=535&top_left_y=314&top_left_x=82)
![](https://cdn.mathpix.com/cropped/9d60cd7c-b37f-404c-8b9c-5eb8fb867709-14.jpg?height=431&width=540&top_left_y=312&top_left_x=644)

> **Key Concept**: The estimated beta coefficient quantifies systematic risk. For example, a beta of 1.2 means that when the market return increases by 1 percent, the stock's return is expected to increase by 1.2 percent on average. Similarly, a beta of 0.6 means the stock moves only 60 percent as much as the market. Investors use beta to assess how much market risk they're taking on when buying a particular stock.


### 8.3.3 Robust Standard Errors for CAPM

- Default standard errors assume error independence over time and homoskedasticity.
- For time series in general, model errors may be correlated over time.
- For financial returns data, however, excess returns are intrinsically not forecastable if markets are efficient. So the error term should be uncorrelated.
- Here, the correlation between the current error and the lagged error (Corr of e-sub-t and e-sub-t-minus-1) equals negative 0.039, which is close to zero.
- The heteroskedastic-robust standard error of the slope coefficient is 0.0770, compared to the default standard error of 0.0644.
- A HAC standard error that additionally controls for error correlation (see Chapter 12.1) is 0.0885.

> **Key Concept**: For time series data, heteroskedastic and autocorrelation consistent (HAC) standard errors account for both changing variance over time and correlation between observations. These robust standard errors provide more reliable inference than conventional standard errors for financial and macroeconomic data, where volatility clustering and persistence are common features.

**Why This Matters**: Every time you invest in a stock, you face a fundamental tradeoff between risk and return. CAPM quantifies this tradeoff using regression. The beta coefficient tells you how risky the stock is relative to the market—crucial information for portfolio construction. A portfolio manager might combine high-beta stocks (riskier, higher expected returns) with low-beta stocks (safer, lower expected returns) to achieve a desired risk profile. Without regression, measuring this risk would be impossible.

From finance, we turn to macroeconomics. Our final case study examines Okun's Law, which links GDP growth to unemployment—one of the most important relationships in macroeconomic policy.

## 8.4 Case Study 4: Output and Unemployment in the U.S.

**In this case study:**
- 8.4.1 Okun's Law: theory and background
- 8.4.2 Estimated Okun's Law model
- 8.4.3 Prediction and forecasting
- 8.4.4 Robust standard errors for Okun's Law

- Dataset GDPUNEMPLOY has annual U.S. data from 1961 to 2019.
- Growth is the annual percentage growth in real GDP.
- URATEchange is the annual change in the percentage unemployment rate for the civilian population aged 16 years and older.
- For example, if the unemployment rate increases from 5.3 percent to 6.5 percent, then URATEchange equals 1.2.

Looking at the key variables in the GDPUNEMPLOY dataset: Annual percentage growth in real GDP averages 3.059 percent with a standard deviation of 2.038 percent, ranging from negative 2.537 to positive 7.237 percent. The annual change in the unemployment rate averages negative 0.032 percentage points (indicating a slight downward trend) with a standard deviation of 0.987 percentage points, ranging from negative 2.143 to positive 3.530 percentage points. This variation in both GDP growth and unemployment changes provides the data needed to estimate Okun's Law.

### 8.4.1 Okun's Law: Theory and Background

Okun's law is that each percentage point increase in the unemployment rate is associated with an approximate two percentage point decrease in the GDP growth rate.
- It's called Okun's law after Arthur Okun who first proposed it in a 1962 journal article.
- A better term is "Okun's rule-of-thumb" as it is an empirical relationship rather than an ironclad law.


### 8.4.2 Estimated Okun's Law Model

**Example 8.5**: Okun's Law Estimation

- OLS regression yields the following results: GDP growth equals 3.008 minus 1.589 times the change in unemployment rate. The intercept has a standard error of 0.162, and the slope has a standard error of 0.175. The R-squared is 0.592, and the standard error of the regression is 1.313. Here, default standard errors are given in parentheses.

- The slope coefficient is highly statistically significant with t equals negative 1.589 divided by 0.175, which equals negative 9.09.
- A test of Okun's law is a test of the null hypothesis that beta-two equals negative 2.0 against the alternative that beta-two does not equal negative 2.0.
- The t-statistic equals the quantity 1.589 minus 2.0, divided by 0.175, which equals negative 2.35. So the p-value equals the probability that the absolute value of T with 23 degrees of freedom is greater than or equal to 2.35, which equals 0.022.
- The null hypothesis is rejected at significance level 0.05.
- So Okun's law is rejected by the data at 5 percent, though negative 1.59 is reasonably close to negative 2.0.

> **Key Concept**: Okun's Law states that when economic growth (GDP) increases, unemployment tends to fall. The estimated coefficient tells us by how much: typically, a 1 percentage point increase in GDP growth is associated with about a 0.5 percentage point decrease in unemployment. This relationship is fundamental to macroeconomic policy, as it links output growth to labor market conditions and helps policymakers understand the employment consequences of economic fluctuations.


### 8.4.3 Prediction and Forecasting

**Example 8.6**: Predicting Unemployment from GDP Growth

From the second panel, output recovery from the 2008 global financial crisis is not as strong as predicted by the model.

![](https://cdn.mathpix.com/cropped/9d60cd7c-b37f-404c-8b9c-5eb8fb867709-19.jpg?height=446&width=1131&top_left_y=348&top_left_x=69)

> **Key Concept**: Regression models can be used for prediction, but predictions come with uncertainty captured by prediction intervals. These intervals account for both uncertainty in the estimated coefficients and the inherent variability in the data. When actual outcomes fall outside prediction intervals, as occurred during the 2008 financial crisis recovery, it suggests that the relationship may have changed or that unusual factors are at play.


### 8.4.4 Robust Standard Errors for Okun's Law

- Default standard errors assume error independence over time and homoskedasticity.
- For time series such as this, the model error is in general correlated over time.
- A HAC standard error that additionally controls for error correlation (see Chapter 12.1) is 0.207 compared to the default standard error of 0.175.

> **Key Concept**: Time series data often exhibits autocorrelation, meaning errors are correlated over time. For annual macroeconomic data like Okun's Law, HAC standard errors that account for this autocorrelation provide more reliable statistical inference than conventional standard errors. The increase from 0.175 to 0.207 reflects the adjustment needed to account for the persistence in economic shocks over time.

**Quick Check**: Before moving on, reflect on these case studies: (1) Why does the U.S. spend so much on healthcare yet achieve worse outcomes than predicted? (2) What does a stock beta of 0.6 tell an investor about risk? (3) Why did Okun's Law predict coefficient negative 2.0, but we estimated negative 1.59? (4) Which type of robust standard errors should you use for cross-sectional data versus time series data? These questions highlight that regression is more than formulas—it's about understanding real-world relationships.

---

## Key Takeaways

**Health Economics Applications:**
- Health spending is positively associated with life expectancy and negatively associated with infant mortality across countries
- The relationships are economically and statistically significant, though causation requires multivariate analysis
- Heteroskedastic-robust standard errors are essential for cross-country regressions due to varying error variances
- The U.S. performs substantially worse than predicted on health outcomes despite high spending
- Health expenditures increase with GDP per capita, but not proportionally across all income levels
- Outliers (U.S. and Luxembourg) can strongly influence regression results and should be investigated
- Log transformations may better capture nonlinear relationships in health data

**Financial Applications (CAPM):**
- The Capital Asset Pricing Model links individual stock returns to market returns through the beta coefficient
- Beta measures systematic risk: beta greater than 1 means more volatile than market, beta less than 1 means less volatile
- Large companies like Coca-Cola typically have beta less than 1, moving less than the overall market
- Alpha measures risk-adjusted performance; the CAPM model predicts alpha equals 0
- For financial returns data, heteroskedastic-robust standard errors account for time-varying volatility
- HAC standard errors additionally control for potential autocorrelation in returns
- R-squared in CAPM regressions indicates how much stock return variation is explained by market movements

**Macroeconomic Applications (Okun's Law):**
- Okun's Law describes the negative relationship between GDP growth and unemployment changes
- The estimated coefficient (negative 1.59) is close to but statistically different from Okun's original negative 2.0 prediction
- Each percentage point increase in GDP growth is associated with about a 0.5 percentage point decrease in unemployment
- The model can forecast unemployment based on GDP growth, with prediction intervals capturing uncertainty
- Time series data requires HAC standard errors to account for autocorrelation in macroeconomic variables
- The 2008 financial crisis recovery showed weaker GDP-unemployment relationship than historical patterns
- Okun's Law is better described as a "rule of thumb" than an ironclad economic law

**General Lessons from Case Studies:**
- Bivariate regression provides initial evidence of relationships, but multivariate analysis is needed for causal claims
- Robust standard errors (heteroskedastic-robust or HAC) are crucial for reliable inference with real-world data
- Model fit (R-squared) varies widely across applications: health (0.32 to 0.93), CAPM (0.20), Okun's Law (0.59)
- Scatterplots help identify outliers, nonlinearity, and heteroskedasticity before formal estimation
- Predictions from regression models come with uncertainty that should be quantified
- Context matters: cross-sectional, time series, and financial data each require different inferential approaches
- Economic significance (magnitude of coefficients) is as important as statistical significance

---
