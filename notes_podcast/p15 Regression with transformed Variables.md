# Chapter 15: Regression with Transformed Variables

## Learning Objectives

By the end of this chapter, you will be able to:

- Understand how variable transformations affect regression interpretation
- Compute and interpret marginal effects for nonlinear models using calculus and finite difference methods
- Distinguish between average marginal effects (AME), marginal effects at the mean (MEM), and marginal effects at representative values (MER)
- Estimate and interpret quadratic and polynomial regression models
- Work with interaction terms and test their joint significance
- Apply natural logarithm transformations to create log-linear and log-log models
- Make predictions from models with transformed dependent variables, avoiding retransformation bias
- Combine multiple types of variable transformations in a single model

---

Do earnings increase linearly with age, or do they peak in mid-career and then decline? Does an extra year of education have the same payoff whether you're 25 or 55? Can we use our regression to predict someone's salary and not just the logarithm of their salary? Real economic relationships are rarely linear—they bend, interact, and often work better on percentage scales than dollar scales. In this chapter, we'll learn how to capture these nonlinear patterns using transformations: quadratic terms, interactions, and natural logarithms (building on Chapter 9). The key challenge? Coefficients no longer equal marginal effects, prediction requires care to avoid bias, and interpretation demands attention to whether we're working with levels, logs, or both.

## 15.1 Example: Earnings, Gender, Education, Worker Type

- Dataset EARNINGS_COMPLETE
- 872 female and male full-time workers aged 25-65 years in 2000.

| Variable | Definition | Mean | Standard Deviation | Min | Max |
| :--- | :--- | :--- | :--- | :--- | :--- |
| Earnings | Annual earnings in \$ | 56369 | 51516 | 4000 | 504000 |
| Age | Age in years | 43.31 | 10.68 | 25 | 65 |
| Gender | equals 1 if female | 0.433 | 0.496 | 0 | 1 |
| Education | Years of schooling | 13.85 | 2.88 | 0 | 20 |
| d1 or dself | equals 1 if self-employed | 0.089 | 0.286 | 0 | 1 |
| d2 or dpriv | equals 1 if private sector employee | 0.760 | 0.427 | 0 | 1 |
| d3 or dgovt | equals 1 if government sector employee | 0.149 | 0.356 | 0 | 1 |
| Agesq | Age squared | 1989.7 | 935.7 | 625 | 4225 |
| Educbyage | Education times Age | 598.8 | 193.69 | 0 | 1260 |
| Hours | Usual hours worked per week | 44.34 | 8.50 | 35 | 99 |
| Lnhours | Natural logarithm of Hours | 3.78 | 0.16 | 3.56 | 4.60 |
| Lnearnings | Natural logarithm of Earnings | 10.69 | 0.68 | 8.29 | 13.13 |
| n | 872 |  |  |  |  |

## 15.2 Marginal Effects for Nonlinear Models

- Examples of nonlinear models
- Quadratic: predicted y equals b-one plus b-two times x plus b-three times x-squared
- Interactions: predicted y equals b-one plus b-two times x plus b-three times z plus b-four times the quantity x times z
- Natural logarithms: ln of predicted y equals b-one plus b-two times x plus b-three times z.
- The marginal effect (ME) on the predicted value of y of a change in a regressor is

ME-sub-x equals change in predicted y divided by change in x

- In nonlinear models we get different results depending on method
- calculus method: use the derivative d predicted y over d x (for very small change in x)
- finite difference methods: such as change in x equals 1.


## Calculus method versus Finite Difference Method

- Plotted curve is y equals 12 minus 2 times the quantity x minus 3, all squared
- calculus method at x equals 2: dy over dx equals 12 minus 4 times x equals 4 at x equals 2.
- finite difference for x equals 2 to x equals 3: change in y equals 12 minus 10 equals 2.

Calculus method
![](https://cdn.mathpix.com/cropped/45e8e6db-1a23-4d8f-893d-5c4838b4b8e1-06.jpg?height=392&width=527&top_left_y=426&top_left_x=91)

Finite difference method
![](https://cdn.mathpix.com/cropped/45e8e6db-1a23-4d8f-893d-5c4838b4b8e1-06.jpg?height=395&width=533&top_left_y=426&top_left_x=654)

## AME, MEM and MER

- Marginal effect ME-sub-x equals change in predicted y over change in x varies with the level of x.
- So what value of x do we evaluate at?
- 1. Average marginal effect (AME): evaluate for each i and average

AME equals one over n times the sum from i equals 1 to n of ME-sub-i, which equals one over n times the sum from i equals 1 to n of the quantity change in predicted y-sub-i over change in x-sub-i.

- 2. Marginal effect at the mean (MEM): evaluate ME at x equals x-bar

MEM equals ME evaluated at x equals x-bar, which equals the quantity change in predicted y over change in x, evaluated at x equals x-bar.

- 3. Marginal effect at a representative value (MER): evaluate ME at a representative value of x, say x equals x-star

MER equals ME evaluated at x equals x-star, which equals the quantity change in predicted y over change in x, evaluated at x equals x-star

- Most often use AME, with ME-sub-i evaluated using calculus methods.

> **Key Concept**: For nonlinear models, marginal effects vary across observations. The average marginal effect (AME) averages ME across all observations, the marginal effect at the mean (MEM) evaluates at sample means, and marginal effect at a representative value (MER) evaluates at a chosen point. AME is most commonly used.

> **Why This Matters**: The choice between AME, MEM, and MER affects your policy conclusions. Suppose you're estimating how a minimum wage hike affects employment. MEM evaluates at the average wage and average employment level—but most workers aren't "average." AME captures the effect for low-wage workers (most affected), middle-wage workers (somewhat affected), and high-wage workers (unaffected), then averages them. This gives a more realistic picture. For nonlinear models, AME is the gold standard because it respects that a \$1 wage increase affects a \$10/hour worker differently than a \$50/hour worker.

## Computation of Marginal Effects

- Suppose ME-sub-x equals 2 times x-squared plus 3 times z-squared, so also depends on z.
- For AME evaluate for each individual and average
- AME-sub-x equals one over n times the sum from i equals 1 to n of the quantity 2 times x-sub-i squared plus 3 times z-sub-i squared.
- For the MEM set all variables at their means
- MEM-sub-x equals 2 times x-bar squared plus 3 times z-bar squared.
- For MER evaluate at a particular value x-star of x
- with z taking the values for each individual

MER-sub-x equals 2 times x-star squared plus one over n times the sum from i equals 1 to n of 3 times z-sub-i squared

- or additionally specify a particular value z-star of z, so

MER-sub-x equals 2 times x-star squared plus 3 times z-star squared.

- Some statistical packages provide post-estimation commands to calculate AME, MEM and MER
- these additionally provide standard errors and confidence intervals for these estimates.


## Nonlinear Models in Practice

- Several issues arise when the relationship is nonlinear.
- Estimation by OLS is possible if the coefficients in the model still appear linearly
- e.g. the expected value of y given x equals beta-one plus beta-two times ln x is okay as linear in beta-one and beta-two
- e.g. the expected value of y given x equals the exponential of beta-one plus beta-two times x is not okay as not linear in beta-one and beta-two
- Direct interpretation of slope coefficients may not be possible
- use marginal effects.
- Prediction of y problematic when y is transformed before regression
- e.g. if the expected value of ln y given x equals beta-one plus beta-two times x.
- Difficult to choose the appropriate nonlinear model
- when can't do a scatter plot of several regressors.


## 15.3 Quadratic Model and Polynomial Models

- A quadratic model is the model y equals beta-one plus beta-two times x plus beta-three times x-squared plus u.
- The figure gives various examples
- top row has beta-two less than 0 and bottom row has beta-two greater than 0.

Examples of Quadratic Model
![](https://cdn.mathpix.com/cropped/45e8e6db-1a23-4d8f-893d-5c4838b4b8e1-10.jpg?height=226&width=238&top_left_y=368&top_left_x=221)

Examples of Quadratic Model
![](https://cdn.mathpix.com/cropped/45e8e6db-1a23-4d8f-893d-5c4838b4b8e1-10.jpg?height=226&width=243&top_left_y=368&top_left_x=531)

![](https://cdn.mathpix.com/cropped/45e8e6db-1a23-4d8f-893d-5c4838b4b8e1-10.jpg?height=226&width=243&top_left_y=368&top_left_x=842)
![](https://cdn.mathpix.com/cropped/45e8e6db-1a23-4d8f-893d-5c4838b4b8e1-10.jpg?height=226&width=241&top_left_y=656&top_left_x=221)
![](https://cdn.mathpix.com/cropped/45e8e6db-1a23-4d8f-893d-5c4838b4b8e1-10.jpg?height=226&width=243&top_left_y=656&top_left_x=531)
![](https://cdn.mathpix.com/cropped/45e8e6db-1a23-4d8f-893d-5c4838b4b8e1-10.jpg?height=230&width=244&top_left_y=654&top_left_x=841)

## Marginal Effects for Quadratic Model

- Fitted quadratic model predicted y equals b-one plus b-two times x plus b-three times x-squared

ME-sub-x equals b-two plus 2 times b-three times x (using calculus methods).

- The average marginal effect is

AME equals one over n times the sum from i equals 1 to n of the quantity b-two plus 2 times b-three times x-sub-i, which equals b-two plus 2 times b-three times one over n times the sum from i equals 1 to n of x-sub-i, which equals b-two plus 2 times b-three times x-bar

## Quadratic Example: Earnings and Age

- Regress Earnings (y) on Age (x), Agesq (x-squared), and Education (z), with heteroskedastic-robust t-statistics in parentheses

Predicted y equals negative 98,620 with t-statistic negative 4.02, plus 3105 with t-statistic 2.86 times x, minus 29.66 with t-statistic negative 2.38 times x-squared, plus 5740 with t-statistic 8.94 times z, with R-squared equals 0.1196 and n equals 872.

- Quadratic term is warranted as for x-squared we have

the absolute value of t equals 2.38, which is greater than t-sub-868-semicolon-0.025 equals negative 1.963.

- The turning point for the quadratic is at x equals negative b-two divided by 2 times b-three
- here at Age equals 3105 divided by the quantity 2 times negative 29.66, which equals 52.3 years.
- earnings on average increase to 52.3 years and then decline.
- ME equals 3105 minus 29.66 times x minus 29.66 times change in x by finite difference method
- ME equals 3105 minus 59.32 times x using calculus method
- AME equals one over n times the sum from i equals 1 to n of the quantity 3105 minus 59.32 times x-sub-i, which equals 3105 minus 59.32 times x-bar, which equals 3105 minus 59.32 times 43.31, which equals 536

> **Key Concept**: Quadratic models capture nonlinear relationships with a turning point at x equals negative b-sub-2 divided by 2 times b-sub-3. The marginal effect is ME equals b-sub-2 plus 2 times b-sub-3 times x (calculus method), which varies with x. Always test whether the quadratic term is statistically significant before interpreting the nonlinear relationship.

## Polynomial Model

- A polynomial model of degree p includes powers of x up to x to the power p.
- The fitted model is

Predicted y equals b-one plus b-two times x plus b-three times x-squared plus dot-dot-dot plus b-sub-p-plus-1 times x to the power p.

- This model has up to p minus 1 turning points.
- Determine polynomial order by progressively adding terms x-squared, x-cubed, and so on
- until additional terms are no longer statistically significant.
- By calculus methods the marginal effect is

ME equals b-two plus 2 times b-three times x plus 3 times b-four times x-squared plus dot-dot-dot plus p times b-sub-p-plus-1 times x to the power p minus 1

which again will vary with the point of evaluation x.

Quadratic models let one variable's effect change with its own level—earnings rise with age, then fall. But what if we want one variable's effect to change with the level of a different variable? For example, does the payoff to education depend on how old you are? Do younger workers benefit more from schooling, or do older workers? To answer questions like these, we need interaction terms—and they'll reappear throughout econometrics (recall Chapter 14's gender-education interactions).

## 15.4 Interacted Regressors

- Example with x times z an interacted regressor is

y equals beta-one plus beta-two times x plus beta-three times z plus beta-four times x times z, plus u.

- Estimation is straightforward
- create a variable xz, say, that equals x times z
- run OLS regression of y on an intercept, x, z and xz.
- the fitted model (with xz equals x times z) is

Predicted y equals b-one plus b-two times x plus b-three times z plus b-four times xz

- Interpretation of regressors is more difficult.
- The marginal effect (ME) on predicted y of a change in x, holding z constant, depends on coefficients of both x and xz

ME-sub-x equals change in predicted y over change in x equals b-two plus b-four times z.

- To test statistical significance of x do joint F-test on variables x and xz: H-sub-0: beta-two equals 0 and beta-four equals 0.


## Interactions Example: Earnings, Education and Age

- OLS regression of Earnings on Age (x) and Education (z)
- both variables are statistically significant at 5 percent (t stats in parentheses)

Predicted y equals negative 46,875 with t-statistic negative 4.15, plus 525 with t-statistic 3.47 times x, plus 5811 with t-statistic 9.06 times z, with R-squared equals 0.115 and n equals 872

- Add AgebyEduc (x times z) as a regressor
- now no regressors are statistically significant at 5 percent

Predicted y equals negative 29,089 with t-statistic negative 0.94, plus 127 with t-statistic 0.18 times x, plus 4515 with t-statistic 1.88 times z, plus 29.0 with t-statistic 0.52 times x times z, with R-squared equals 0.115 and n equals 872

- The marginal effect of one more year of schooling is

ME-sub-Ed equals 4515 plus 29 times Age.

- So the returns to education increase as one ages.

> **Key Concept**: With interaction terms (x times z), the marginal effect of x depends on z: ME-sub-x equals b-two plus b-four times z. Individual coefficients may be insignificant due to collinearity with the interaction term, so use joint F-tests to assess the overall significance of a variable and its interactions.

**Quick Check**: You regress earnings on Age, Education, and Age times Education. The coefficient on Age is 127 (t equals 0.18, insignificant). Does this mean age doesn't matter for earnings? (Pause and think.) Answer: No! The marginal effect of age is 127 plus 29 times Education (if the interaction coefficient is 29). At Education equals 14 years, the age effect is 127 plus 29 times 14 equals 533 dollars per year—economically meaningful. The t-test on Age alone is misleading because Age is highly correlated with the interaction term. Always use a joint F-test on Age and Age times Education together (recall Chapter 11). Here, F equals 6.49 with p equals 0.002, confirming age is highly significant.

## Joint Hypothesis tests

- Individual coefficients are statistically insignificant at 5 percent
- But a joint test on Age (x) and AgebyEduc (x times z)
- a test of H-sub-0: beta-sub-x equals 0 and beta-sub-xz equals 0, yields F equals 6.49 with p equals 0.002
- so age remains highly statistically significant
- similarly F-test for the two education regressors is F equals 43.00 with p equals 0.000.
- Why the difference between individual and joint tests?
- The interaction variable AgebyEduc is
- quite highly correlated with Age (rho-hat equals 0.72)
- quite highly correlated with Education (rho-hat equals 0.64).
- When regressors are highly correlated with each other
- individual contributions are measured much less precisely
- here standard errors of Age and Education more than triple from 151 and 641 to 719 with inclusion of variable AgebyEduc.

We've now seen how quadratics and interactions capture different types of nonlinearity—curvature within one variable, and relationships that vary across variables. But there's another powerful transformation we introduced in Chapter 9: natural logarithms. Logs are especially useful for variables that vary widely (like earnings from \$4,000 to \$504,000) or when we care about percentage changes rather than level changes. Let's revisit log transformations, now with a focus on computing marginal effects and making predictions in original units.

## 15.5 Natural Logarithm Transformations

We introduced log transformations in Chapter 9, where we learned two key interpretations:
- In **log-linear models** (ln y equals beta-one plus beta-two times x), beta-two is a semi-elasticity
- In **log-log models** (ln y equals beta-one plus beta-two times ln x), beta-two is an elasticity

Now we'll go deeper. We'll compute marginal effects ME-sub-x equals change in y over change in x in original units, not just percentage changes.
- For log-linear model ln y equals b-one plus b-two times x, use ME-sub-x equals b-two times predicted y
- reason: change in ln y over change in x equals b-two, but change in ln y is approximately equal to change in y over y, so the quantity change in y over y, all divided by change in x equals b-two, and on solving, change in y over change in x equals b-two times y
- Similarly for log-log model ln y equals b-one plus b-two times ln x, use ME-sub-x equals b-two times predicted y over x.


## Log-linear Model

- OLS regression of ln of Earnings on Age (x) and Education (z)
- both variables are statistically significant at 5 percent (t stats in parentheses)

Predicted ln y equals 8.96 with t-statistic 59.63, plus 0.0078 with t-statistic 3.83 times x, plus 0.101 with t-statistic 11.68 times z, with R-squared equals 0.190

- One year of aging, controlling for education, is associated with a 0.78 percent (equals 100 times 0.0078) increase in earnings.
- The marginal effect of aging is 0.0078 times predicted y
- always positive and increases with age since predicted y increases with age.
- simplest to evaluate at y-bar, then MEM of a year of aging is a \$440 increase in earnings (equals 0.0078 times 56,369).

> **Key Concept**: In log-linear models (ln y equals beta-one plus beta-two times x), the coefficient beta-two is a semi-elasticity: a one-unit change in x is associated with a 100 times beta-two percent change in y. The marginal effect in levels is ME-sub-x equals beta-two times predicted y, which increases with the level of y.

## Log-log Models

- OLS regression of ln of Earnings on ln of Age (x) and Education (z)
- both variables are statistically significant at 5 percent (t stats in parentheses)

Predicted ln y equals 8.01 with t-statistic 24.23, plus 0.346 with t-statistic 4.21 times ln x, plus 0.100 with t-statistic 11.67 times z, with R-squared equals 0.193

- A one percent increase in age, controlling for education, is associated with a 0.346 percent increase in earnings.
- The marginal effect of aging is 0.346 times predicted y over x
- always positive and increases with age since predicted y increases with age.
- simplest to evaluate at y-bar and x-bar, then MEM of a year of aging is a \$450 increase in earnings (equals 0.346 times 56,369 divided by 43.41).

> **Key Concept**: In log-log models (ln y equals beta-one plus beta-two times ln x), the coefficient beta-two is an elasticity: a 1 percent change in x is associated with a beta-two percent change in y. The marginal effect in levels is ME-sub-x equals beta-two times predicted y over x, which varies with both x and y.

## 15.6 Prediction from Log-linear and Log-log Models

- Consider log-linear model: predicted ln y equals b-one plus b-two times x plus b-three times z.
- A naive prediction in level is predicted y equals the exponential of predicted ln y, which equals the exponential of the quantity b-one plus b-two times x plus b-three times z.
- But this underpredicts due to retransformation bias (next page).
- Instead if errors were normal and homoskedastic predict y using

y-tilde equals the exponential of the quantity s-sub-e squared divided by 2, all times the exponential of predicted ln y.

- Here s-sub-e is standard error of the regression for the ln y regression.
- Example: s-sub-e equals 0.4 (which is large for data on a log scale)
- need to rescale by the exponential of the quantity s-sub-e squared divided by 2, which equals 1.215


## Retransformation Bias Correction

**The setup**: Our log-linear population model assumes

ln y equals beta-one plus beta-two times x plus u, where the expected value of u given x equals 0.

**Taking exponentials**: Exponentiate both sides to get

y equals exp of the quantity beta-one plus beta-two times x plus u.

**Computing the conditional mean**: What's the expected value of y given x? Taking expectations:

The expected value of y given x equals the expected value of exp of the quantity beta-one plus beta-two times x plus u, given x.

We can pull out constants, giving:

The expected value of y given x equals exp of the quantity beta-one plus beta-two times x, times the expected value of exp of u, given x.

**The problem**: We need the expected value of exp of u given x. In general, this is greater than 1, even though the expected value of u given x equals 0.

**The solution** (when errors are normal and homoskedastic): If u given x is distributed as normal with mean 0 and variance sigma-sub-u squared, then

The expected value of exp of u given x equals exp of sigma-sub-u squared divided by 2.

**Putting it together**: The expected value of y given x equals exp of sigma-sub-u squared divided by 2, times exp of the quantity beta-one plus beta-two times x.

> **Key Concept**: Predicting y from a log-linear model requires accounting for retransformation bias. The naive prediction exp(ln predicted y) underestimates the expected value of y given x. With normal homoskedastic errors, multiply by the exponential of s-sub-e squared divided by 2, where s-sub-e is the standard error from the log regression.

> **Why This Matters**: Retransformation bias is one of the most common mistakes in applied economics. If you regress log earnings on education and naively exponentiate to predict someone's salary, you'll systematically underpredict—sometimes by 10-20 percent or more. This matters for policy: if you're designing a wage subsidy program and underestimate earnings by 15 percent, you'll underfund the program. Banks making loan decisions, governments projecting tax revenue, and researchers forecasting GDP all need to get this right. The fix is simple—multiply by exp of s-sub-e squared over 2—but forgetting it is costly.

## R-squared with Transformed Dependent Variable

- R-squared in regress y on x measures the fraction of the variation in y around y-bar that is explained by the regressors.
- R-squared in regress g of y on x instead measures the fraction of the variation in g of y around g of y-bar that is explained by the regressors.
- So meaningless to compare R-squared across models with different transformations of the dependent variable.
- For right-skewed data R-squared is usually higher in models for ln y rather than y.
- For persistent time series right-skewed data R-squared is usually higher in models for y than for change in y.


## 15.7 Models with a Mix of Regressor Types

- Levels example with R-squared equals 0.206 and n equals 872 is

Predicted Earnings equals negative 356,631 with t-statistic negative 5.38, minus 14,330 with t-statistic negative 5.31 times Gender, plus 3283 with t-statistic 3.08 times Age, minus 31.58 with t-statistic negative 2.59 times Agesq, plus 5399 with t-statistic 8.85 times Education, plus 9360 with t-statistic 1.07 times Dself, minus 291 with t-statistic negative 0.10 times Dgovt, plus 69,964 with t-statistic 4.34 times Lnhours.

- Interpretation controlling for other regressors
- ME of aging is 3283 minus 63.16 times Age
- Self-employed workers on average earn \$9,360 more than private sector workers (the omitted category)
  - Though this comparison is statistically insignificant at 5 percent
- A 1 percent change in hours worked is associated with a \$699 increase in earnings


## Dependent Variable in Natural Logarithms

- Natural logarithms example with R-squared equals 0.206 and n equals 872 is


## Ln of Predicted Earnings

Predicted ln of Earnings equals 4.459 with t-statistic 6.89, minus 0.193 with t-statistic negative 4.88 times Gender, plus 0.0560 with t-statistic 3.55 times Age, minus 0.000549 with t-statistic negative 2.99 times Agesq, plus 0.0934 with t-statistic 11.17 times Education, minus 0.118 with t-statistic negative 1.17 times Dself, plus 0.070 with t-statistic 1.53 times Dgovt, plus 0.975 with t-statistic 6.88 times Lnhours

- Interpretation controlling for other regressors
- women on average earn 19.3 percent less than men
- earnings increase with age to 51.0 years (equals negative 0.0560 divided by 2 times negative 0.000549) and then decrease
- Self-employed workers on average earn 11.8 percent less than private sector workers (the omitted category)
  - Though this comparison is statistically insignificant at 5 percent
- A 1 percent change in hours worked is associated with a 0.975 percent increase in earnings

---

## Key Takeaways

**Marginal Effects for Nonlinear Models:**
- In nonlinear models, the marginal effect ME-sub-x equals change in predicted y over change in x is no longer equal to the slope coefficient
- Marginal effects can be computed using calculus methods (derivatives, for very small change in x) or finite difference methods (change in x equals 1)
- Calculus method at x: ME equals d predicted y over d x; finite difference method: ME equals the quantity predicted y at x plus 1 minus predicted y at x, all divided by 1
- Three common approaches for summarizing marginal effects across observations:
- **AME (Average Marginal Effect)**: Compute ME for each observation and average: AME equals one over n times the sum of ME-sub-i
- **MEM (Marginal Effect at the Mean)**: Evaluate ME at sample means: MEM equals ME evaluated at x equals x-bar
- **MER (Marginal Effect at Representative value)**: Evaluate ME at a chosen representative value x-star
- AME is most commonly used in practice, typically with ME-sub-i evaluated using calculus methods
- Statistical packages often provide post-estimation commands to calculate AME, MEM, MER with standard errors

**Quadratic and Polynomial Models:**
- Quadratic model: y equals beta-one plus beta-two times x plus beta-three times x-squared plus u captures U-shaped or inverted U-shaped relationships
- The turning point occurs at x equals negative beta-two divided by 2 times beta-three
- Marginal effect using calculus: ME-sub-x equals b-two plus 2 times b-three times x, which varies with x
- Average marginal effect: AME equals b-two plus 2 times b-three times x-bar (simplifies nicely for quadratic models)
- Always test whether quadratic term is statistically significant before interpreting nonlinearity
- Polynomial models of degree p include powers up to x to the power p, allowing up to p minus 1 turning points
- Determine polynomial order progressively by adding terms until they become statistically insignificant
- For polynomial of degree p, marginal effect: ME equals b-two plus 2 times b-three times x plus 3 times b-four times x-squared plus dot-dot-dot plus p times b-sub-p-plus-1 times x to the power p minus 1
- Example: Earnings peak at age 52.3 years in quadratic model with Age and Age-squared

**Interaction Terms (Interacted Regressors):**
- Model with interaction: y equals beta-one plus beta-two times x plus beta-three times z plus beta-four times the quantity x times z, plus u
- Create interaction variable xz equals x times z and include as additional regressor in OLS
- The marginal effect of x depends on the level of z: ME-sub-x equals b-two plus b-four times z
- Similarly, marginal effect of z depends on x: ME-sub-z equals b-three plus b-four times x
- Individual coefficients on x, z, and x times z may be statistically insignificant due to high collinearity
- Use joint F-test to assess overall significance: H-sub-0: beta-two equals 0 and beta-four equals 0 tests significance of x
- Interaction terms are often highly correlated with their component variables (e.g., rho-hat equals 0.72, 0.64)
- This multicollinearity inflates standard errors but doesn't invalidate the model
- Example: Returns to education increase with age when Education times Age interaction is included

**Natural Logarithm Transformations:**
- OLS estimation works if model is linear in coefficients (e.g., ln y equals beta-one plus beta-two times x is okay)
- **Log-linear model**: ln y equals beta-one plus beta-two times x plus u
  - Coefficient beta-two is a semi-elasticity: one-unit change in x leads to 100 times beta-two percent change in y
  - Marginal effect in levels: ME-sub-x equals beta-two times predicted y (increases with level of y)
  - Example: b-two equals 0.0078 means one year of aging leads to 0.78 percent increase in earnings
- **Log-log model**: ln y equals beta-one plus beta-two times ln x plus u
  - Coefficient beta-two is an elasticity: 1 percent change in x leads to beta-two percent change in y
  - Marginal effect in levels: ME-sub-x equals beta-two times predicted y over x
  - Example: b-two equals 0.346 means 1 percent increase in age leads to 0.346 percent increase in earnings
- **Linear-log model**: y equals beta-one plus beta-two times ln x plus u (less common)
  - Marginal effect: ME-sub-x equals beta-two over x
- Log transformations often improve model fit for right-skewed data (higher R-squared)

**Prediction from Log Models and Retransformation Bias:**
- Naive prediction from ln y equals beta-one plus beta-two times x: predicted y equals exp of the quantity b-one plus b-two times x **underestimates** the expected value of y given x
- Problem: the expected value of exp of u given x is greater than 1 in general, so the expected value of y given x equals exp of the quantity beta-one plus beta-two times x, all times the expected value of exp of u given x
- **Retransformation bias correction** with normal homoskedastic errors:
  - y-tilde equals exp of the quantity s-sub-e squared over 2, all times exp of predicted ln y, where s-sub-e is standard error from log regression
  - The expected value of exp of u given x equals exp of sigma-sub-u squared over 2, when u given x is distributed as normal with mean 0 and variance sigma-sub-u squared
- Example: s-sub-e equals 0.4 requires rescaling by exp of the quantity 0.4 squared over 2 equals exp of 0.08 equals 1.083 (8.3 percent adjustment)
- Even small s-sub-e can matter: s-sub-e equals 0.2 leads to exp of 0.02 equals 1.020 (2 percent adjustment)
- Retransformation bias correction applies to log-linear, log-log, and other log-transformed models
- Alternative: Duan's smearing estimator uses one over n times the sum of exp of e-sub-i when errors not normal

**R-squared with Transformed Dependent Variables:**
- R-squared measures fraction of variation in the dependent variable explained by regressors
- R-squared from regress y on x measures variation in y; R-squared from regress g of y on x measures variation in g of y
- **Cannot compare R-squared across models with different dependent variable transformations**
- For right-skewed data, R-squared usually higher for ln y than for y (better fit on log scale)
- For time series, R-squared usually higher for y than for change in y (levels vs. changes)
- Model selection based on R-squared only valid when dependent variable transformation is identical

**Models with Mixed Regressor Types:**
- Can combine levels, quadratics, interactions, dummies, and log transformations in one model
- Example: Earnings equals f of Gender, Age, Age-squared, Education, Worker type dummies, ln Hours
- Interpretation requires care when mixing transformation types:
  - Binary regressor (Gender): women earn \$14,330 less (levels model) or 19.3 percent less (log model)
  - Quadratic (Age, Age-squared): earnings peak at specific age, then decline
  - Log regressor (ln Hours): 1 percent change in hours leads to 0.975 percent change in earnings (log model)
  - Dummy variables: compare to omitted category (private sector workers)
- Always control for other regressors when interpreting any single coefficient
- Statistical significance patterns may differ between levels and log models
- Choose transformation based on economic theory, data characteristics, and model diagnostics

---

## Some in-class Exercises

(1) For predicted y equals 2 plus 3 times x plus 4 times x-squared for a dataset with y-bar equals 30 and x-bar equals 2, give the marginal effect of a one unit change in x. Hence give the AME.
(2) For predicted y equals 1 plus 2 times x plus 4 times d plus 7 times d times x for a dataset with y-bar equals 22, x-bar equals 3 and d-bar equals 0.5, give the marginal effect of a one unit change in x. Hence give the AME.
(3) For model ln y equals beta-one plus beta-two plus u we obtain predicted ln y equals 1 plus 2 times x, n equals 100, s-sub-e equals 0.3. Give an estimate of the expected value of y given x.
