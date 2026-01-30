# Chapter 9: Models with Natural Logarithms

## Learning Objectives

By the end of this chapter, you will be able to:

- Understand the natural logarithm function and its basic properties
- Use logarithmic transformations to approximate proportionate and percentage changes
- Distinguish between semi-elasticity (percentage change in y per unit change in x) and elasticity (percentage change in y per percentage change in x)
- Interpret coefficients in log-linear, log-log, and linear-log regression models
- Apply logarithmic models to analyze the relationship between earnings and education
- Use the approximation ln of the quantity 1 plus x, approximately equals x, for small values of x
- Apply the Rule of 72 to calculate doubling times for compound growth
- Linearize exponential growth patterns using natural logarithms
- Understand the exponential function and its relationship to the natural logarithm

---

In Chapter 5, you learned that one more year of education is associated with a 5,021 dollar increase in earnings. But here's a better way to think about it: one more year of education is associated with a 13 percent increase in earnings. Why is percentage change more useful than dollar amounts? Because 5,021 dollars means very different things to someone earning 20,000 dollars versus someone earning 200,000 dollars. Logarithms let us work with percentage changes instead of absolute changes—and they unlock powerful techniques for analyzing growth rates, elasticities, and nonlinear relationships.

## 9.1 Natural Logarithm Function

- A logarithmic function is the reverse operation to raising a number to a power
- e.g. 10 to the power 2 equals 100 implies that log to the base 10 of 100 equals 2
- if 10 raised to the power 2 equals 100 then the logarithm to the base 10 of 100 is 2.
- More generally

a to the power b equals x implies that log to the base a of x equals b;

- the logarithm to the base a of x equals b.
- Most obvious choice of the base a is base 10 (decimal system).
- Economics often uses logarithm to base e, the natural logarithm
- where e is approximately 2.71828 dot-dot-dot, is a transcendental number like pi

The natural logarithm of x equals log to the base e of x, for x greater than zero.

> **Key Concept**: A logarithm is the reverse operation to exponentiation. If a to the power b equals x, then log to the base a of x equals b. The natural logarithm uses base e approximately 2.71828, a transcendental number. We write the natural logarithm of x as ln x, which equals log to the base e of x, defined only for x greater than zero. Natural logarithms are particularly useful in economics for analyzing growth rates and percentage changes.

### Approximating Proportionate Changes

- Delta x equals x-one minus x-zero is the change in x when x changes from x-zero to x-one.
- The proportionate change in x is

Delta x divided by x-zero equals the quantity x-one minus x-zero, divided by x-zero.

- Example: Change from x-zero equals 40 to x-one equals 40.4
- Delta x equals 40.4 minus 40 equals 0.4
- proportionate change in x is Delta x divided by x-zero equals 0.4 divided by 40 equals 0.01
- and percentage change is 100 times 0.01 equals 1 percent.

- We have

From calculus, the derivative d ln x by d x equals 1 over x. This implies that Delta ln x divided by Delta x is approximately 1 over x, for small Delta x divided by x. Rearranging, we get Delta ln x is approximately Delta x divided by x.

- For small proportionate changes we use the approximation

Delta ln x is approximately Delta x divided by x, for small Delta x divided by x (say Delta x divided by x less than 0.1).

- Multiplying by 100 yields percentage changes, so equivalently

100 times Delta ln x is approximately the percentage change in x.

- Example: Change from x-zero equals 40 to x-one equals 40.4
- approximation is ln of 40.4 minus ln of 40 equals 3.69883 minus 3.68888, which is approximately 0.00995
- exact is Delta x divided by x-zero equals the quantity 40.4 minus 40, divided by 40, equals 0.01.

> **Key Concept**: For small proportionate changes, the change in the natural logarithm approximates the proportionate change: Delta ln x is approximately Delta x divided by x. This relationship follows from calculus (d ln x by d x equals 1 over x). Multiplying by 100 converts this to percentage change: 100 times Delta ln x is approximately the percentage change in x. This approximation works well when Delta x divided by x is less than 0.1 (i.e., changes less than 10 percent).

## 9.2 Semi-elasticity and Elasticity

- The semi-elasticity of y with respect to x is the ratio of the proportionate change in y to the change in the level of x

Semi-elasticity of y with respect to x equals the quantity Delta y divided by y, all divided by Delta x.

- Multiplying by 100 gives the percentage change in y when x changes by one unit.
- Example: semi-elasticity of earnings with respect to years of schooling is 0.08
- one more year of schooling is associated with a 0.08 proportionate change in earnings
- one more year of schooling is associated with an 8 percent change in earnings.

- The elasticity of y with respect to x is the proportionate change of y for a given proportionate change in x

Elasticity of y with respect to x equals the quantity Delta y divided by y, all divided by the quantity Delta x divided by x. This equals Delta y divided by Delta x, times x divided by y.

- Example: price elasticity of demand for a good is negative 2
- a one percent increase in price leads to a 2 percent decrease in demand.

- Since Delta y divided by y is approximately Delta ln y, and Delta x divided by x is approximately Delta ln x, we obtain the following.
- Semi-elasticities and elasticities can be approximated as following

Semi-elasticity of y with respect to x equals the quantity Delta y divided by y, all divided by Delta x, which is approximately Delta ln y divided by Delta x. Elasticity of y with respect to x equals the quantity Delta y divided by y, all divided by the quantity Delta x divided by x, which is approximately Delta ln y divided by Delta ln x.

- OLS regression of models that first transform variables to natural logarithms can directly estimate semi-elasticities and elasticities.
- Example: if ln y equals a plus b times ln x, then the slope b equals Delta ln y divided by Delta ln x, which equals the elasticity.
- so we can obtain the semi-elasticity by regressing ln y on x.

> **Key Concept**: Semi-elasticity measures the percentage change in y per unit change in x: the quantity Delta y divided by y, all divided by Delta x. Elasticity measures the percentage change in y per percentage change in x: the quantity Delta y divided by y, all divided by the quantity Delta x divided by x. Using the logarithmic approximation, semi-elasticity is approximately Delta ln y divided by Delta x, and elasticity is approximately Delta ln y divided by Delta ln x. This means we can estimate semi-elasticities by regressing ln y on x, and elasticities by regressing ln y on ln x.

## 9.3 Log-linear Model

- The log-linear or log-level model regresses ln y on x
- with fitted value predicted ln y equals b-one plus b-two times x
- the slope coefficient b-two equals Delta predicted ln y divided by Delta x, is an estimate of the semi-elasticity of y with respect to x
- we need y greater than zero since only then is ln y defined.
- This is a very common model for right-skewed data such as individual earnings.

### Log-log Model

- The log-log model regresses ln y on ln x
- with fitted value predicted ln y equals b-one plus b-two times ln x
- the slope coefficient b-two equals Delta predicted ln y divided by Delta ln x, is an estimate of the elasticity of y with respect to x
- we need y greater than zero and x greater than zero since only then are ln y and ln x defined.

### Linear-log Model

- The linear-log model or level-log regresses y on ln x
- with fitted value predicted y equals b-one plus b-two times ln x
- b-two divided by 100 is an estimate of the change in y in response to a one percent change in x.
- we need x greater than zero since only then is ln x defined.

> **Key Concept**: The interpretation of regression coefficients depends on which variables are logged. Log-linear (ln y on x): coefficient b-two is the semi-elasticity (percentage change in y per unit change in x). Log-log (ln y on ln x): coefficient b-two is the elasticity (percentage change in y per percentage change in x). Linear-log (y on ln x): coefficient b-two divided by 100 is the change in y per one percent change in x.

- We have

Comparing the four models: The Linear model has specification predicted y equals b-one plus b-two times x, with interpretation of b-two as slope: Delta y divided by Delta x. The Log-Linear model has specification predicted ln y equals b-one plus b-two times x, with interpretation as semi-elasticity: the quantity Delta y divided by y, all divided by Delta x. The Log-log model has specification predicted ln y equals b-one plus b-two times ln x, with interpretation as elasticity: the quantity Delta y divided by y, all divided by the quantity Delta x divided by x. The Linear-log model has specification predicted y equals b-one plus b-two times ln x, with interpretation as Delta y divided by the quantity Delta x divided by x.

## 9.4 Example: Earnings and Education

- Dataset EARNINGS on 172 full-time male workers in 2010 aged 30 years (same dataset as Chapter 5, now with logarithmic transformations).

Looking at the summary statistics: The Earnings variable is Annual earnings in dollars, with Mean 41,413, Standard Deviation 25,527, Min 1,050, Max 172,000. Lnearn is the Natural logarithm of Earnings, with Mean 10.46, Standard Deviation 0.62, Min 6.96, Max 12.05. Education is Years of completed schooling, with Mean 14.43, Standard Deviation 2.73, Min 3, Max 20. Lneduc is the Natural logarithm of Education, with Mean 2.65, Standard Deviation 0.22, Min 1.10, Max 3.00. The sample size n equals 171.

- OLS regression of Earnings (y) on Education (x) yields (t-statistics in parentheses)

Predicted y equals negative 31,056 with t-statistic negative 3.49 in parentheses, plus 5,021 with t-statistic 8.30 in parentheses, times x. R-squared equals 0.290.

> **Key Concept**: The earnings and education data provides an ideal context for comparing linear and logarithmic models. Mean earnings are 41,413 dollars with substantial variation (standard deviation 25,527). Mean education is 14.43 years. The linear model shows that one more year of education is associated with 5,021 dollars higher earnings, with R-squared of 0.290. The high t-statistic (8.30) indicates this relationship is statistically significant.

### Linear Model and Log-Linear Model

- Linear model: Earnings equals negative 31,056 plus 5,021 times Education
- Log-linear model: ln of Earnings equals 8.561 plus 0.131 times Education
![](https://cdn.mathpix.com/cropped/7c64b055-6220-4bbe-a4f4-67774edc6d98-15.jpg?height=421&width=529&top_left_y=368&top_left_x=86)
![](https://cdn.mathpix.com/cropped/7c64b055-6220-4bbe-a4f4-67774edc6d98-15.jpg?height=423&width=534&top_left_y=368&top_left_x=646)

> **Key Concept**: The scatter plots illustrate the difference between linear and log-linear models. The left panel shows earnings versus education with a linear fit, revealing right-skewed earnings data with outliers at high values. The right panel shows natural log of earnings versus education with a linear fit, which better captures the relationship and reduces the influence of extreme values. The log transformation makes the earnings distribution more symmetric and the relationship more linear.

### Comparison of Models with Earnings Data

- y is earnings and x is education (with t-statistics in parentheses).

Comparing four model specifications: The Linear model has estimates predicted y equals negative 31,056 with t-statistic negative 3.49, plus 5,021 with t-statistic 8.30, times x. R-squared 0.289. The slope is 5,021. The Log-linear model has estimates predicted ln y equals 8.561 with t-statistic 40.83, plus 0.131 with t-statistic 9.21, times x. R-squared 0.334. The semi-elasticity is 0.131. The Log-log model has estimates predicted ln y equals 6.543 with t-statistic 13.70, plus 1.478 with t-statistic 8.23, times ln x. R-squared 0.286. The elasticity is 1.478. The Linear-log model has estimates predicted y equals negative 102,767 with t-statistic negative 5.05, plus 54,452 with t-statistic 7.11, times ln x. R-squared 0.230.

- Linear: one year more of education is associated with a 5,021 dollars increase in earnings
- Log-linear: one year more of education is associated with a 13.1 percent increase in earnings
- Log-log: 1 percent increase in education is associated with a 1.478 percent increase in earnings
- Linear-log: 1 percent increase in education is associated with a 544 dollars (equals 54,452 divided by 100) increase in earnings.

> **Key Concept**: Different logarithmic transformations provide different insights. In the earnings-education example: the log-linear model (R-squared 0.334) suggests one more year of education is associated with a 13.1 percent increase in earnings. The log-log model (R-squared 0.286) suggests a 1 percent increase in education is associated with a 1.478 percent increase in earnings. The linear model gives absolute dollar changes (5,021 dollars per year), while log models give relative percentage changes.

**Why This Matters**: Policy debates about education often focus on percentage returns. Telling policymakers that an extra year of education increases earnings by "13 percent" is far more compelling than saying it increases earnings by "5,021 dollars"—because the percentage applies regardless of your current earnings level. A 13 percent return is comparable to returns on other investments (stocks, bonds, real estate), helping policymakers decide whether education spending is worthwhile. This is why economists overwhelmingly prefer log models for analyzing earnings.

We've seen how logs help us interpret regression coefficients as percentages. But there's more to the story. Logarithms have useful mathematical properties that make calculations easier and provide shortcuts for everyday problems like compound interest.

## 9.5 Approximating Natural Logarithm

- ln of the quantity 1 plus x equals x minus x-squared divided by 2, plus x-cubed divided by 3, minus x to the fourth power divided by 4, plus x to the fifth power divided by 5, minus and so on
- e.g. ln of 1.1 equals 1 minus 0.1 plus 0.01 divided by 2, minus 0.001 divided by 3, plus dot-dot-dot, which is approximately 1 minus 0.1 plus 0.005 minus 0.00033, which is approximately 0.0953.
- So for small x we have the approximation

ln of the quantity 1 plus x is approximately x, for, say, x less than 0.1

- Approximation good for small x, but x increasingly overestimates ln of the quantity 1 plus x
- for x less than 0.10 the approximation is within five percent of ln of the quantity 1 plus x
- for x equals 0.2, for example, the approximation is ten percent larger than ln of 1.2 equals 0.1823.

Looking at the approximation table: For "Small" x: when x equals 0.05, the True Value ln of the quantity 1 plus x equals 0.0488, and the Approximation x equals 0.05. When x equals 0.10, True Value equals 0.0953, Approximation equals 0.10. For "Larger" x: when x equals 0.15, True Value equals 0.1398, Approximation equals 0.15. When x equals 0.20, True Value equals 0.1823, Approximation equals 0.20. When x equals 0.50, True Value equals 0.4055, Approximation equals 0.50.

> **Key Concept**: For small values of x (say x less than 0.1), the natural logarithm can be approximated as ln of the quantity 1 plus x is approximately x. This comes from the Taylor series expansion. The approximation is within 5 percent of the true value when x is less than 0.10, but becomes increasingly inaccurate for larger x. For example, when x equals 0.20, the simple approximation overestimates the true value by about 10 percent.

### Compounding and the Rule of 72

- Rule of 72: a series growing at percentage rate r takes approximately 72 divided by r periods to double.
- Example: Invest at 4 percent per annum doubles in 72 divided by 4 equals 18 years.
- Reason:
- After n periods at rate r investment is the quantity 1 plus r, raised to the power n, times larger.
- Money doubles if n solves the equation the quantity 1 plus r, raised to the power n, equals 2
- Solution is n equals ln of 2, divided by ln of the quantity 1 plus r.
- Approximate: ln of the quantity 1 plus r is approximately r for small r.
- Approximate: ln of 2 equals 0.6931, which is approximately 0.72.
- So n equals ln of 2, divided by ln of the quantity 1 plus r, is approximately 0.72 divided by r.
- Example: r equals 0.04 (so 4 percent)
- true value: ln of 2, divided by ln of the quantity 1 plus 0.04, equals 17.67, so doubles in 17.67 years
- rule of 72: 72 divided by 4 equals 18, so doubles in 18 years.
- More precisely can have rule of 70, or 69, or 69.3.

> **Key Concept**: The Rule of 72 provides a quick way to estimate doubling time for compound growth: doubling time is approximately 72 divided by r, where r is the percentage growth rate. For example, at 4 percent annual growth, an investment doubles in approximately 72 divided by 4 equals 18 years. This rule works because it approximates the exact formula n equals ln of 2, divided by ln of the quantity 1 plus r, using the approximations ln of the quantity 1 plus r is approximately r and ln of 2 is approximately 0.72.

**Why This Matters**: The Rule of 72 is one of the most practical applications of logarithms. Investors use it to compare investment options. At 8 percent annual return, your money doubles every 9 years (72 divided by 8). At 2 percent inflation, prices double every 36 years (72 divided by 2). Policy makers use it to assess economic growth: if GDP grows 3 percent annually, the economy doubles every 24 years. This simple rule—rooted in logarithms—helps you make quick mental calculations about compound growth without reaching for a calculator.

### Linearizing Exponential Growth

- Many data series grow according to a power law, or exponentially, over time, rather than linearly.

x-sub-t equals x-sub-zero times the quantity 1 plus r, raised to the power t

- Here x-sub-zero is value at time 0
- x-sub-t is value at time t
- r is the constant growth rate (or decay rate if r is less than zero).
- Example: 100 dollars invested at 3 percent annual interest rate for 10 years.
- annual growth rate is r equals 3 divided by 100 equals 0.03
- investment worth 100 times the quantity 1.03, raised to the power 10, or 134.39 dollars after ten years.

- Taking the natural logarithm of x-sub-t equals x-sub-zero times the quantity 1 plus r, raised to the power t, yields

Starting with ln of x-sub-t equals ln of the quantity x-sub-zero times the quantity 1 plus r, raised to the power t. This equals ln of x-sub-zero, plus ln of the quantity the quantity 1 plus r, raised to the power t. This equals ln of x-sub-zero, plus ln of the quantity 1 plus r, times t. This is approximately ln of x-sub-zero, plus r times t, for small r.

- Exponential growth is linear growth in logs!

> **Key Concept**: Data that grows exponentially according to x-sub-t equals x-sub-zero times the quantity 1 plus r, raised to the power t, becomes linear when transformed to logarithms: ln of x-sub-t is approximately ln of x-sub-zero, plus r times t. This means exponential growth in levels appears as linear growth in logs. Taking logs allows us to estimate growth rates using simple linear regression and makes it easier to visualize long-term trends that would otherwise appear curved.

### Example: S&P 500

- Standard and Poor 500 Index 1927 to 2019
- no inflation adjustment and no dividends
- Left panel: exponential growth in level
- Right panel: linear growth in logs
  - Growth rate is approximately the quantity 7.8 minus 1.8, divided by the quantity 2019 minus 1927, which equals 6.0 divided by 92, which equals 0.065 or 6.5 percent per annum
![](https://cdn.mathpix.com/cropped/7c64b055-6220-4bbe-a4f4-67774edc6d98-21.jpg?height=429&width=548&top_left_y=416&top_left_x=82)
![](https://cdn.mathpix.com/cropped/7c64b055-6220-4bbe-a4f4-67774edc6d98-21.jpg?height=429&width=550&top_left_y=416&top_left_x=644)

> **Key Concept**: The S&P 500 example from 1927 to 2019 illustrates exponential growth linearization. The left panel shows the index level growing exponentially, making it difficult to assess long-term trends. The right panel plots the natural logarithm of the index, revealing an approximately linear upward trend. The slope of this log-linear trend estimates the annual growth rate as approximately 6.5 percent. This log transformation makes complex growth patterns much easier to visualize and analyze.

## 9.6 Exponential Function

- What is e?
- e is an irrational number that is approximately 2.7182818
- e is a transcendental number, like pi which is approximately 3.142
- unlike for pi, there is no simple physical interpretation for e.
- The exponential function is denoted

exp of x equals e to the power x

- The natural logarithm is the reverse operation to exponentiation.
- Then

y equals e to the power x implies that x equals ln of y.

- For example, e to the power 2 is approximately 7.38906, so ln of 7.38906 is approximately 2.0.

> **Key Concept**: The exponential function exp of x equals e to the power x is the inverse operation to the natural logarithm. If y equals e to the power x, then x equals ln of y, and vice versa. The number e approximately 2.71828 is a transcendental number with no simple physical interpretation, yet it naturally arises in continuous compounding and many mathematical contexts. The exponential and natural logarithm functions undo each other.

### Approximating Exponential

- exp of x equals 1 plus x plus x-squared divided by 2 factorial, plus x-cubed divided by 3 factorial, plus x to the fourth power divided by 4 factorial, plus x to the fifth power divided by 5 factorial, plus and so on
- e.g. exp of 1.1 equals 1 plus 0.1 plus 0.01 divided by 2, plus 0.001 divided by 6, plus dot-dot-dot, which is approximately 1 plus 0.1 plus 0.005 plus 0.00016, which is approximately 1.1052.
- So for small x

e to the power x is approximately 1 plus x, for, say, x less than 0.1.

- Approximation good for small x, but increasingly underestimates e to the power x as x increases.

Looking at the approximation table for exp of x: For "Small" x: when x equals 0.05, the True Value exp of x equals 1.0513, and the Approximation 1 plus x equals 1.05. When x equals 0.10, True Value equals 1.1052, Approximation equals 1.10. For "Larger" x: when x equals 0.15, True Value equals 1.1618, Approximation equals 1.15. When x equals 0.20, True Value equals 1.2214, Approximation equals 1.20. When x equals 0.50, True Value equals 1.6487, Approximation equals 1.50.

> **Key Concept**: For small values of x, the exponential function can be approximated as e to the power x is approximately 1 plus x. This comes from the Taylor series expansion. The approximation works reasonably well for x less than 0.1, but increasingly underestimates the true value as x grows larger. For example, when x equals 0.50, the simple approximation 1.50 significantly underestimates the true value 1.6487.

### Compound Interest Rates

- Consider compound for a year and find the annual percentage yield, or APY.
- Suppose have 12 percent per annum then APY equals 12 percent.
- Suppose compound monthly at 12 divided by 12 equals 1 percent per month

The quantity 1 plus 0.01, raised to the power 12, equals 1.12683, so APY equals 12.683 percent

- Suppose compound daily at 12 divided by 365 percent per day

The quantity 1 plus 0.12 divided by 365, raised to the power 365, equals 1.127547, so APY equals 12.747 percent

- If continuously compound for progressively smaller intervals at rate r

The quantity 1 plus r divided by n, raised to the power n, approaches e to the power r as n approaches infinity

- Here the quantity 1 plus 0.12 divided by n, raised to the power n, approaches exp of 0.12 equals 1.12750 or 12.750 percent.

> **Key Concept**: The exponential function naturally arises in continuous compounding. As the compounding frequency increases, the quantity 1 plus r divided by n, raised to the power n, approaches e to the power r as n approaches infinity. For example, 12 percent compounded continuously gives an annual yield of e to the power 0.12 equals 1.12750 or 12.750 percent. Compounding more frequently increases the effective annual yield, with continuous compounding providing the mathematical limit.

**Quick Check**: Before moving on, test your understanding: (1) If ln of y increases by 0.10, what's the approximate percentage change in y? (2) In a log-linear model (ln of y on x), what does the slope coefficient b-two measure? (3) In a log-log model (ln of y on ln of x), what does b-two measure? (4) Using the Rule of 72, how long does it take for GDP to double at 6 percent annual growth? (5) Why do we prefer log models over linear models for earnings data? If you can answer these, you've mastered the core concepts of logarithmic regression.

## Some in-class Exercises

(1) Consider numbers a and b with ln of a equals 3.20 and ln of b equals 3.25. Using only this information, what is the approximate percentage change in going from a to b?
(2) Demand for a good falls from 100 to 90 when the price increases from 20 to 21. Compute the price elasticity of demand.
(3) We estimate ln of y equals 3 plus 0.5 times ln of x. Give the elasticity of y with respect to x.
(4) We estimate ln of y equals 6 plus 0.2 times x. Give the response of y when x changes by one unit.
(5) How long does it take for prices to double given 4 percent annual inflation?
(6) Suppose y equals alpha times the quantity 1 plus beta, raised to the power x. Explain how to estimate alpha and beta using OLS.

---

## Key Takeaways

**Natural Logarithm Basics (Section 9.1):**
- A logarithm is the reverse operation to raising a number to a power: if a to the power b equals x, then log to the base a of x equals b
- The natural logarithm uses base e approximately 2.71828: ln of x equals log to the base e of x, for x greater than zero
- The natural logarithm is particularly useful in economics for measuring proportionate and percentage changes
- The derivative relationship d ln x by d x equals 1 over x provides the foundation for logarithmic approximations
- For small proportionate changes (Delta x divided by x less than 0.1), we have the approximation: Delta ln x is approximately Delta x divided by x
- Multiplying by 100 converts the logarithmic change to percentage change: 100 times Delta ln x is approximately the percentage change in x
- This approximation allows us to interpret changes in log-transformed variables as percentage changes
- Example: if ln of x changes from 3.6889 to 3.6988, this represents approximately a 1 percent change in x
- The approximation becomes less accurate as the proportionate change increases beyond 10 percent

**Semi-elasticity and Elasticity (Section 9.2):**
- Semi-elasticity measures the percentage change in y per unit change in x: the quantity Delta y divided by y, all divided by Delta x
- Multiplying semi-elasticity by 100 gives the percentage change in y when x changes by one unit
- Example: if semi-elasticity is 0.08, one unit increase in x is associated with an 8 percent increase in y
- Elasticity measures the percentage change in y per percentage change in x: the quantity Delta y divided by y, all divided by the quantity Delta x divided by x
- Elasticity can also be expressed as the quantity Delta y divided by Delta x, times x divided by y, the ratio of marginal to average
- Example: if price elasticity of demand is negative 2, a 1 percent price increase leads to a 2 percent decrease in quantity demanded
- Using logarithmic approximations: semi-elasticity is approximately Delta ln y divided by Delta x, and elasticity is approximately Delta ln y divided by Delta ln x
- OLS regression with log transformations can directly estimate semi-elasticities and elasticities
- If ln of y equals a plus b times ln of x, then the slope coefficient b estimates the elasticity
- If ln of y equals a plus b times x, then the slope coefficient b estimates the semi-elasticity

**Log-linear, Log-log, and Linear-log Models (Section 9.3):**
- The log-linear (or log-level) model regresses ln of y on x: predicted ln of y equals b-one plus b-two times x
- In the log-linear model, b-two estimates the semi-elasticity: percentage change in y per unit change in x
- Log-linear models are commonly used for right-skewed data like earnings, house prices, or firm sizes
- The log-log model regresses ln of y on ln of x: predicted ln of y equals b-one plus b-two times ln of x
- In the log-log model, b-two estimates the elasticity: percentage change in y per percentage change in x
- Log-log models are common for demand curves, production functions, and other relationships involving elasticities
- The linear-log (or level-log) model regresses y on ln of x: predicted y equals b-one plus b-two times ln of x
- In the linear-log model, b-two divided by 100 estimates the change in y from a one percent change in x
- For log-linear and log-log models, we need y greater than zero since ln of y must be defined
- For log-log and linear-log models, we need x greater than zero since ln of x must be defined
- The choice of model depends on the theoretical relationship and the units in which results should be interpreted
- Linear model gives absolute changes (Delta y divided by Delta x), log models give relative or percentage changes

**Earnings and Education Example (Section 9.4):**
- The EARNINGS dataset contains 171 full-time male workers aged 30 in 2010
- Mean earnings: 41,413 dollars, mean education: 14.43 years
- Linear model: one more year of education leads to 5,021 dollars increase in earnings (R-squared equals 0.289)
- Log-linear model: one more year of education leads to 13.1 percent increase in earnings (R-squared equals 0.334)
- Log-log model: 1 percent increase in education leads to 1.478 percent increase in earnings (R-squared equals 0.286)
- Linear-log model: 1 percent increase in education leads to 544 dollars increase in earnings (R-squared equals 0.230)
- The log-linear model has the highest R-squared, suggesting it fits the data best
- The log-linear model interpretation (13.1 percent per year) is more meaningful than absolute dollar amounts for policy discussions
- Different models provide different insights: absolute dollar effects versus percentage effects
- The convex relationship between earnings and education is better captured by log transformations
- All models show statistically significant positive relationships (high t-statistics)
- The choice between models depends on whether we want to interpret results in dollar terms or percentage terms

**Approximating ln of the quantity 1 plus x and the Rule of 72 (Section 9.5):**
- The Taylor series expansion: ln of the quantity 1 plus x equals x minus x-squared divided by 2, plus x-cubed divided by 3, minus x to the fourth power divided by 4, plus and so on
- For small x (say x less than 0.1), we have the simple approximation: ln of the quantity 1 plus x is approximately x
- This approximation is within 5 percent of the true value when x is less than 0.10
- For larger x values, the simple approximation x increasingly overestimates ln of the quantity 1 plus x
- Example: when x equals 0.20, the approximation 0.20 is 10 percent larger than ln of 1.2 equals 0.1823
- The Rule of 72: a series growing at rate r percent takes approximately 72 divided by r periods to double
- Example: at 4 percent annual growth, an investment doubles in approximately 72 divided by 4 equals 18 years
- The true doubling time is n equals ln of 2, divided by ln of the quantity 1 plus r, which uses both logarithmic concepts
- The Rule of 72 works because ln of 2 is approximately 0.693, which is approximately 0.72, and ln of the quantity 1 plus r is approximately r for small r
- More precise variants include the Rule of 70 (using 70 instead of 72) or Rule of 69.3 (using ln of 2 directly)
- The Rule of 72 is particularly useful for quick mental calculations of compound growth

**Linearizing Exponential Growth (Section 9.5 continued):**
- Many economic series grow exponentially over time: x-sub-t equals x-sub-zero times the quantity 1 plus r, raised to the power t
- Here x-sub-zero is the initial value, x-sub-t is the value at time t, and r is the constant growth rate
- Taking natural logarithms: ln of x-sub-t equals ln of x-sub-zero plus ln of the quantity 1 plus r, times t, which is approximately ln of x-sub-zero plus r times t for small r
- Exponential growth in levels becomes linear growth in logs
- This linearization allows us to estimate growth rates using simple linear regression
- Regressing ln of x-sub-t on t gives slope approximately r (the growth rate) and intercept approximately ln of x-sub-zero
- Example: S&P 500 Index (1927 to 2019) shows exponential growth in levels but linear growth in logs
- From the S&P 500 log chart, estimated growth rate is approximately the quantity 7.8 minus 1.8, divided by the quantity 2019 minus 1927, equals 6.5 percent per annum
- The log transformation makes it easier to visualize long-term trends that would otherwise appear highly curved
- Exponential decay (r less than zero) also becomes linear in logs, with negative slope

**Exponential Function (Section 9.6):**
- The exponential function exp of x equals e to the power x is the inverse of the natural logarithm
- If y equals e to the power x, then x equals ln of y, and vice versa
- The number e approximately 2.71828 is a transcendental number (like pi) with no simple physical interpretation
- The Taylor series expansion: e to the power x equals 1 plus x plus x-squared divided by 2 factorial, plus x-cubed divided by 3 factorial, plus x to the fourth power divided by 4 factorial, plus and so on
- For small x (x less than 0.1), we have the approximation: e to the power x is approximately 1 plus x
- This approximation increasingly underestimates e to the power x as x increases
- The exponential function naturally arises in continuous compounding problems
- With rate r compounded n times per period: the quantity 1 plus r divided by n, raised to the power n, approaches e to the power r as n approaches infinity
- Example: 12 percent compounded continuously gives annual yield e to the power 0.12 equals 1.12750 or 12.750 percent
- Compounding more frequently increases the effective annual yield
- The exponential function grows faster than any polynomial function as x approaches infinity

**General Principles:**
- Logarithmic transformations are essential tools for analyzing percentage changes and growth rates in economics
- Log transformations can reduce right skewness in data distributions (making them more normally distributed)
- The choice between using levels or logs depends on whether absolute or relative changes are more meaningful
- Log models require that transformed variables are strictly positive
- Interpretation of coefficients differs fundamentally between linear and log models
- The approximations (Delta ln x is approximately Delta x divided by x, and e to the power x is approximately 1 plus x) only work well for small values
- Natural logarithms and exponentials are inverse operations: they undo each other
- These tools are widely applicable: returns on investments, demand elasticities, growth accounting, income distributions, etc.

---
