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

## 15.1 Example: Earnings, Gender, Education, Worker Type

- Dataset EARNINGS_COMPLETE
- 872 female and male full-time workers aged 25-65 years in 2000.

| Variable | Definition | Mean | Standard Deviation | Min | Max |
| :--- | :--- | :--- | :--- | :--- | :--- |
| Earnings | Annual earnings in \$ | 56369 | 51516 | 4000 | 504000 |
| Age | Age in years | 43.31 | 10.68 | 25 | 65 |
| Gender | $=1$ if female | 0.433 | 0.496 | 0 | 1 |
| Education | Years of schooling | 13.85 | 2.88 | 0 | 20 |
| d1 or dself | $=1$ if self-employed | 0.089 | 0.286 | 0 | 1 |
| d2 or dpriv | $=1$ if private sector employee | 0.760 | 0.427 | 0 | 1 |
| d3 or dgovt | $=1$ if government sector employee | 0.149 | 0.356 | 0 | 1 |
| Agesq | Age squared | 1989.7 | 935.7 | 625 | 4225 |
| Educbyage | Education times Age | 598.8 | 193.69 | 0 | 1260 |
| Hours | Usual hours worked per week | 44.34 | 8.50 | 35 | 99 |
| Lnhours | Natural logarithm of Hours | 3.78 | 0.16 | 3.56 | 4.60 |
| Lnearnings | Natural logarithm of Earnings | 10.69 | 0.68 | 8.29 | 13.13 |
| n | 872 |  |  |  |  |

## 15.2 Marginal Effects for Nonlinear Models

- Examples of nonlinear models
- Quadratic: $\hat{y}=b_{1}+b_{2} x+b_{3} x^{2}$
- Interactions: $\hat{y}=b_{1}+b_{2} x+b_{3} z+b_{3}(x \times z)$
- Natural logarithms: $\ln \hat{y}=b_{1}+b_{2} x+b_{3} z$.
- The marginal effect (ME) on the predicted value of $y$ of a change in a regressor is

$$
\mathrm{ME}_{x}=\frac{\Delta \widehat{y}}{\Delta x}
$$

- In nonlinear models we get different results depending on method
- calculus method: use the derivative $d \widehat{y} / d x$ (for very small $\Delta x$ )
- finite difference methods: such as $\Delta x=1$.


## Calculus method versus Finite Difference Method

- Plotted curve is $y=12-2 \times(x-3)^{2}$
- calculus method at $x=2: \frac{d y}{d x}=12-4 x=4$ at $x=2$.
- finite difference for $x=2$ to $x=3: \Delta y=12-10=2$.

Calculus method
![](https://cdn.mathpix.com/cropped/45e8e6db-1a23-4d8f-893d-5c4838b4b8e1-06.jpg?height=392&width=527&top_left_y=426&top_left_x=91)

Finite difference method
![](https://cdn.mathpix.com/cropped/45e8e6db-1a23-4d8f-893d-5c4838b4b8e1-06.jpg?height=395&width=533&top_left_y=426&top_left_x=654)

## AME, MEM and MER

- Marginal effect $M E_{x}=\Delta \hat{y} / \Delta x$ varies with the level of $x$.
- So what value of $x$ do we evaluate at?
- 1. Average marginal effect (AME): evaluate for each $i$ and average

$$
\mathrm{AME}=\frac{1}{n} \sum_{i=1}^{n} \mathrm{ME}_{i}=\frac{1}{n} \sum_{i=1}^{n} \frac{\Delta \widehat{y}_{i}}{\Delta x_{i}} .
$$

- 2. Marginal effect at the mean (MEM): evaluate ME at $x=\bar{x}$

$$
\mathrm{MEM}=\left.\mathrm{ME}\right|_{x=\bar{x}}=\left.\frac{\Delta \widehat{y}}{\Delta x}\right|_{x=\bar{x}} .
$$

- 3. Marginal effect at a representative value (MER): evaluate ME at a representative value of $x$, say $x=x^{*}$

$$
\mathrm{MER}=\left.\mathrm{ME}\right|_{x=x^{*}}=\left.\frac{\Delta \widehat{y}}{\Delta x}\right|_{x=x^{*}}
$$

- Most often use AME, with ME ${ }_{i}$ evaluated using calculus methods.

> **Key Concept**: For nonlinear models, marginal effects vary across observations. The average marginal effect (AME) averages ME across all observations, the marginal effect at the mean (MEM) evaluates at sample means, and marginal effect at a representative value (MER) evaluates at a chosen point. AME is most commonly used.

## Computation of Marginal Effects

- Suppose $\mathrm{ME}_{x}=2 x^{2}+3 z^{2}$ so also depends on $z$.
- For AME evaluate for each individual and average
- $\mathrm{AME}_{x}=\frac{1}{n} \sum_{i=1}^{n}\left(2 x_{i}^{2}+3 z_{i}^{2}\right)$.
- For the MEM set all variables at their means
- $\mathrm{MEM}_{x}=2 \bar{x}^{2}+3 \bar{z}^{2}$.
- For MER evaluate at a particular value $x^{*}$ of $x$
- with $z$ taking the values for each individual

$$
\mathrm{MER}_{x}=2\left(x^{*}\right)^{2}+\frac{1}{n} \sum_{i=1}^{n} 3 z_{i}^{2}
$$

- or additionally specify a particular value $z^{*}$ of $z$, so

$$
\mathrm{MER}_{x}=2\left(x^{*}\right)^{2}+3\left(z^{*}\right)^{2} .
$$

- Some statistical packages provide post-estimation commands to calculate AME, MEM and MER
- these additionally provide standard errors and confidence intervals for these estimates.


## Nonlinear Models in Practice

- Several issues arise when the relationship is nonlinear.
- Estimation by OLS is possible if the coefficients in the model still appear linearly
- e.g. $\mathrm{E}[y \mid x]=\beta_{1}+\beta_{2} \ln x$ is okay as linear in $\beta_{1}$ and $\beta_{2}$
- e.g. $\mathrm{E}[y \mid x]=\exp \left(\beta_{1}+\beta_{2} x\right)$ is not okay as not linear in $\beta_{1}$ and $\beta_{2}$
- Direct interpretation of slope coefficients may not be possible
- use marginal effects.
- Prediction of $y$ problematic when $y$ is transformed before regression
- e.g. if $\mathrm{E}[\ln y \mid x]=\beta_{1}+\beta_{2} x$.
- Difficult to choose the appropriate nonlinear model
- when can't do a scatter plot of several regressors.


## 15.3 Quadratic Model and Polynomial Models

- A quadratic model is the model $y=\beta_{1}+\beta_{2} x+\beta_{3} x^{2}+u$.
- The figure gives various examples
- top row has $\beta_{2}<0$ and bottom row has $\beta_{2}>0$.

Examples of Quadratic Model
![](https://cdn.mathpix.com/cropped/45e8e6db-1a23-4d8f-893d-5c4838b4b8e1-10.jpg?height=226&width=238&top_left_y=368&top_left_x=221)

Examples of Quadratic Model
![](https://cdn.mathpix.com/cropped/45e8e6db-1a23-4d8f-893d-5c4838b4b8e1-10.jpg?height=226&width=243&top_left_y=368&top_left_x=531)

![](https://cdn.mathpix.com/cropped/45e8e6db-1a23-4d8f-893d-5c4838b4b8e1-10.jpg?height=226&width=243&top_left_y=368&top_left_x=842)
![](https://cdn.mathpix.com/cropped/45e8e6db-1a23-4d8f-893d-5c4838b4b8e1-10.jpg?height=226&width=241&top_left_y=656&top_left_x=221)
![](https://cdn.mathpix.com/cropped/45e8e6db-1a23-4d8f-893d-5c4838b4b8e1-10.jpg?height=226&width=243&top_left_y=656&top_left_x=531)
![](https://cdn.mathpix.com/cropped/45e8e6db-1a23-4d8f-893d-5c4838b4b8e1-10.jpg?height=230&width=244&top_left_y=654&top_left_x=841)

## Marginal Effects for Quadratic Model

- Fitted quadratic model $\widehat{y}=b_{1}+b_{2} x+b_{3} x^{2}$

$$
\mathrm{ME}_{x}=b_{2}+2 b_{3 x} \text { (using calculus methods). }
$$

- The average marginal effect is

$$
\begin{aligned}
\mathrm{AME} & =\frac{1}{n} \sum_{i=1}^{n}\left(b_{2}+2 b_{3} x_{i}\right) \\
& =b_{2}+2 b_{3} \times \frac{1}{n} \sum_{i=1}^{n} x_{i} \\
& =b_{2}+2 b_{3} \bar{x}
\end{aligned}
$$

## Quadratic Example: Earnings and Age

- Regress Earnings ( $y$ ) on Age ( $x$ ), Agesq ( $x^{2}$ ), and Education ( $z$ ), with heteroskedastic-robust $t$-statistics in parentheses

$$
\widehat{y}=-\underset{(-4.02)}{98620}+\underset{(2.86)}{3105} x-\underset{(-2.38)}{29.66} x^{2}+\underset{(8.94)}{5740 z}, \quad R^{2}=.1196, \quad n=872,
$$

- Quadratic term is warranted as for $x^{2}$ we have

$$
|t|=2.38>t_{868 ; .025}=-1.963 .
$$

- The turning point for the quadratic is at $x=-b_{2} / 2 b_{3}$
- here at Age $=3105 /(2 \times(-29.66))=52.3$ years.
- earnings on average increase to 52.3 years and then decline.
- $\mathrm{ME}=3105-29.66 x-29.66 \Delta x$ by finite difference method
- ME $=3105-59.32 x$ using calculus method
- $\mathrm{AME}=\frac{1}{n} \sum_{i=1}^{n}\left(3105-59.32 x_{i}\right)=3105-59.32 \bar{x}= 3105-59.32 \times 43.31=536$

> **Key Concept**: Quadratic models capture nonlinear relationships with a turning point at x = -b₂/(2b₃). The marginal effect is ME = b₂ + 2b₃x (calculus method), which varies with x. Always test whether the quadratic term is statistically significant before interpreting the nonlinear relationship.

## Polynomial Model

- A polynomial model of degree $p$ includes powers of $x$ up to $x^{p}$.
- The fitted model is

$$
\widehat{y}=b_{1}+b_{2} x+b_{3} x^{2}+\cdots+b_{p+1} x^{p} .
$$

- This model has up to $p-1$ turning points.
- Determine polynomial order by progressively adding terms $x^{2}, x^{3}, \ldots$
- until additional terms are no longer statistically significant.
- By calculus methods the marginal effect is

$$
\mathrm{ME}=b_{2}+2 b_{3} x+3 b_{4} x^{2}+\cdots+p b_{p+1} x^{p-1}
$$

which again will vary with the point of evaluation $x$.

## 15.4 Interacted Regressors

- Example with $x \times z$ an interacted regressor is

$$
y=\beta_{1}+\beta_{2} x+\beta_{3} z+\beta_{4} x \times z+u .
$$

- Estimation is straightforward
- create a variable $x z$, say, that equals $x \times z$
- run OLS regression of $y$ on an intercept, $x, z$ and $x z$.
- the fitted model (with $x z=x \times z$ ) is

$$
\widehat{y}=b_{1}+b_{2} x+b_{3} z+b_{4} x z
$$

- Interpretation of regressors is more difficult.
- The marginal effect (ME) on $\hat{y}$ of a change in $x$, holding $z$ constant, depends on coefficients of both $x$ and $x z$

$$
\mathrm{ME}_{x}=\frac{\Delta \widehat{y}}{\Delta x}=b_{2}+b_{4} z .
$$

- To test statistical significance of $x$ do joint $F$-test on variables $x$ and $x z: H_{0}: \beta_{2}=0, \beta_{4}=0$.


## Interactions Example: Earnings, Education and Age

- OLS regression of Earnings on Age ( $x$ ) and Education ( $z$ )
- both variables are statistically significant at $5 \%$ ( $t$ stats in parentheses)

$$
\widehat{y}=\underset{(-4.15)}{-46875}+\underset{(3.47)}{525} x+\underset{(9.06)}{5811} z, \quad R^{2}=.115, \quad n=872
$$

- Add AgebyEduc ( $x \times z$ ) as a regressor
- now no regressors are statistically significant at $5 \%$

$$
\widehat{y}=\underset{(-0.94)}{-29089}+\underset{(0.18)}{127} x+\underset{(1.88)}{4515} z+\underset{(0.52)}{29.0} x \times z, \quad R^{2}=.115, \quad n=872
$$

- The marginal effect of one more year of schooling is

$$
\mathrm{ME}_{E d}=4515+29 \times \text { Age } .
$$

- So the returns to education increase as one ages.

> **Key Concept**: With interaction terms (x×z), the marginal effect of x depends on z: ME_x = b₂ + b₄z. Individual coefficients may be insignificant due to collinearity with the interaction term, so use joint F-tests to assess the overall significance of a variable and its interactions.

## Joint Hypothesis tests

- Individual coefficients are statistically insignificant at $5 \%$
- But a joint test on Age ( $x$ ) and AgebyEduc ( $x \times z$ )
- a test of $H_{0}: \beta_{x}=0, \beta_{x z}=0$ yields $F=6.49$ with $p=0.002$
- so age remains highly statistically significant
- similarly $F$-test for the two education regressors is $F=43.00$ with $p=0.000$.
- Why the difference between individual and joint tests?
- The interaction variable AgebyEduc is
- quite highly correlated with Age ( $\widehat{\rho}=0.72$ )
- quite highly correlated with Education ( $\widehat{\rho}=0.64$ ).
- When regressors are highly correlated with each other
- individual contributions are measured much less precisely
- here standard errors of Age and Education more than triple from 151 and 641 to 719 with inclusion of variable AgebyEduc.


## 15.5 Natural Logarithm Transformations

- Consider models with $\ln y$ and/or $\ln x$.
- Chapter 9 gave interpretation of coefficients
- semi-elasticity in log-linear model
- elasticity in log-log model.
- Now additionally consider marginal effects $\mathrm{ME}_{x}=\Delta y / \Delta x$.
- For log-linear model $\ln y=b_{1}+b_{2} x$ use $\mathrm{ME}_{x}=b_{2} \widehat{y}$
- reason: $\Delta \ln y / \Delta x=b_{2}$ but $\Delta \ln y \simeq \Delta y / y$ so $(\Delta y / y) / \Delta x=b_{2}$ and on solving $\Delta y / \Delta x=b_{2} y$
- Similarly for $\log$-log model $\ln y=b_{1}+b_{2} \ln x$ use $\mathrm{ME}_{x}=b_{2} \widehat{y} / x$.


## Log-linear Model

- OLS regression of $\ln$ (Earnings) on Age ( $x$ ) and Education ( $z$ )
- both variables are statistically significant at $5 \%$ ( $t$ stats in parentheses)

$$
\widehat{\ln y}=\underset{(59.63)}{8.96}+\underset{(3.83)}{0.0078 x}+\underset{(11.68)}{0.101 z}, \quad R^{2}=.190
$$

- One year of aging, controlling for education, is associated with a 0.78 percent ( $=100 \times 0.0078$ ) increase in earnings.
- The marginal effect of aging is $0.0078 \widehat{y}$
- always positive and increases with age since $\widehat{y} \uparrow$ with age.
- simplest to evaluate at $\bar{y}$, then MEM of a year of aging is a \$440 increase in earnings $(=0.0078 \times 56369)$.

> **Key Concept**: In log-linear models (ln y = β₁ + β₂x), the coefficient β₂ is a semi-elasticity: a one-unit change in x is associated with a 100×β₂ percent change in y. The marginal effect in levels is ME_x = β₂ŷ, which increases with the level of y.

## Log-log Models

- OLS regression of $\ln$ (Earnings) on $\ln ($ Age $)(x)$ and Education ( $z$ )
- both variables are statistically significant at $5 \%$ ( $t$ stats in parentheses)

$$
\widehat{\ln y}=\underset{(24.23)}{8.01}+\underset{(4.21)}{0.346 \ln x}+\underset{(11.67)}{0.100} z, \quad R^{2}=.193
$$

- A one percent increase in age, controlling for education, is associated with a 0.346 percent increase in earnings.
- The marginal effect of aging is $0.346 \hat{y} / x$
- always positive and increases with age since $\widehat{y} \uparrow$ with age.
- simplest to evaluate at $\bar{y}$ and $\bar{x}$, then MEM of a year of aging is a \$450 increase in earnings $(=0.346 \times 56369 / 43.41)$.

> **Key Concept**: In log-log models (ln y = β₁ + β₂ ln x), the coefficient β₂ is an elasticity: a 1% change in x is associated with a β₂% change in y. The marginal effect in levels is ME_x = β₂ŷ/x, which varies with both x and y.

## 15.6 Prediction from Log-linear and Log-log Models

- Consider log-linear model: $\widehat{\ln y}=b_{1}+b_{2} x+b_{3} z$.
- A naive prediction in level is $\hat{y}=\exp (\widehat{\ln y})=\exp \left(b_{1}+b_{2} x+b_{3} z\right)$.
- But this underpredicts due to retransformation bias (next page).
- Instead if errors were normal and homoskedastic predict $y$ using

$$
\widetilde{y}=\exp \left(s_{e}^{2} / 2\right) \times \exp (\widehat{\ln y}) .
$$

- Here $s_{e}$ is standard error of the regression for the $\ln y$ regression.
- Example: $s_{e}=0.4$ (which is large for data on a log scale)
- need to rescale by $\exp \left(s_{e}^{2} / 2\right)=1.215$


## Retransformation Bias Correction

- Log-linear population model assumes $\mathrm{E}[u \mid x]=0$ in

$$
\ln y=\beta_{1}+\beta_{2} x+u
$$

- Taking the exponential on both sides: $y=\exp \left(\beta_{1}+\beta_{2} x+u\right)$.
- So the conditional mean of $y$ given $x$ is

$$
\begin{aligned}
\mathrm{E}[y \mid x] & =\mathrm{E}\left[\exp \left(\beta_{1}+\beta_{2} x+u\right) \mid x\right] \\
& =\exp \left(\beta_{1}+\beta_{2} x\right) \times \mathrm{E}[\exp (u) \mid x] .
\end{aligned}
$$

- Problem: We need to know $\mathrm{E}[\exp (u) \mid x]$.
- in general $\mathrm{E}[\exp (u) \mid x]>1$
- $\mathrm{E}[\exp (u) \mid x]=\exp \left(\sigma_{u}^{2} / 2\right)$ if $u \mid x \sim N\left(0, \sigma_{u}^{2}\right)$
  - i.e. normal homoskedastic errors

- then $\mathrm{E}[y \mid x]=\exp \left(\sigma_{u}^{2} / 2\right) \exp \left(\beta_{1}+\beta_{2} x\right)$.

> **Key Concept**: Predicting y from a log-linear model requires accounting for retransformation bias. The naive prediction exp(ln ŷ) underestimates E[y|x]. With normal homoskedastic errors, multiply by exp(s_e²/2) where s_e is the standard error from the log regression.

## R-squared with Transformed Dependent Variable

- $R^{2}$ in regress $y$ on $x$ measures the fraction of the variation in $y$ around $\bar{y}$ that is explained by the regressors.
- $R^{2}$ in regress $g(y)$ on $x$ instead measures the fraction of the variation in $g(y)$ around $\overline{g(y)}$ that is explained by the regressors.
- So meaningless to compare $R^{2}$ across models with different transformations of the dependent variable.
- For right-skewed data $R^{2}$ is usually higher in models for $\ln y$ rather than $y$.
- For persistent time series right-skewed data $R^{2}$ is usually higher in models for $y$ than for $\Delta y$.


## 15.7 Models with a Mix of Regressor Types

- Levels example with $R^{2}=.206, n=872$ is

$$
\begin{aligned}
& \widehat{\text { Earning }} \text { s } \\
= & \underset{(-5.38)}{-356631}-\underset{(-5.31)}{14330} \times \text { Gender }+\underset{(3.08)}{3283} \times \text { Age }-\underset{(-2.59)}{31.58} \times \text { Agesq } \\
& +\underset{(8.85)}{5399} \times \text { Education }+\underset{(1.07)}{9360} \times \text { Dself }-\underset{(-0.10)}{291} \times \text { Dgovt } \\
& +\underset{(4.34)}{69964} \times \text { Lnhours },
\end{aligned}
$$

- Interpretation controlling for other regressors
- ME of aging is $3283-63.16 \times$ Age
- Self-employed workers on average earn \$9,360 more than private sector workers (the omitted category)
  - Though this comparison is statistically insignificant at $5 \%$
- A $1 \%$ change in hours worked is associated with a \$699 increase in earnings


## Dependent Variable in Natural Logarithms

- Natural logarithms example with $R^{2}=.206, n=872$ is


## Ln $\widehat{\text { Earnings }}$

$$
\begin{aligned}
= & \underset{(6.89)}{4.459-\underset{(-4.88)}{0.193} \times \text { Gender }+\underset{(3.55)}{0.0560} \times \text { Age }-\underset{(-2.99)}{0.000549} \times \text { Agesq }} \\
& +\underset{(11.17)}{0.0934} \times \text { Education }-\underset{(-1.17)}{0.118} \times \text { Dself }+\underset{(1.53)}{0.070} \times \text { Dgovt } \\
& +\underset{(6.88)}{0.975} \times \text { Lnhours }
\end{aligned}
$$

- Interpretation controlling for other regressors
- women on average earn $19.3 \%$ less than men
- earnings increase with age to 51.0 years $(=-.560 /(2 \times(-.000549))$ and then decrease
- Self-employed workers on average earn $11.8 \%$ less than private sector workers (the omitted category)
  - Though this comparison is statistically insignificant at $5 \%$
- A $1 \%$ change in hours worked is associated with a $0.975 \%$ increase in earnings

---

## Key Takeaways

**Marginal Effects for Nonlinear Models:**
- In nonlinear models, the marginal effect ME_x = Δŷ/Δx is no longer equal to the slope coefficient
- Marginal effects can be computed using calculus methods (derivatives, for very small Δx) or finite difference methods (Δx = 1)
- Calculus method at x: ME = dŷ/dx; finite difference method: ME = [ŷ(x+1) - ŷ(x)]/1
- Three common approaches for summarizing marginal effects across observations:
- **AME (Average Marginal Effect)**: Compute ME for each observation and average: AME = (1/n)Σ ME_i
- **MEM (Marginal Effect at the Mean)**: Evaluate ME at sample means: MEM = ME|_{x=x̄}
- **MER (Marginal Effect at Representative value)**: Evaluate ME at a chosen representative value x*
- AME is most commonly used in practice, typically with ME_i evaluated using calculus methods
- Statistical packages often provide post-estimation commands to calculate AME, MEM, MER with standard errors

**Quadratic and Polynomial Models:**
- Quadratic model: y = β₁ + β₂x + β₃x² + u captures U-shaped or inverted U-shaped relationships
- The turning point occurs at x = -β₂/(2β₃)
- Marginal effect using calculus: ME_x = b₂ + 2b₃x, which varies with x
- Average marginal effect: AME = b₂ + 2b₃x̄ (simplifies nicely for quadratic models)
- Always test whether quadratic term is statistically significant before interpreting nonlinearity
- Polynomial models of degree p include powers up to x^p, allowing up to p-1 turning points
- Determine polynomial order progressively by adding terms until they become statistically insignificant
- For polynomial of degree p, marginal effect: ME = b₂ + 2b₃x + 3b₄x² + ... + pb_{p+1}x^{p-1}
- Example: Earnings peak at age 52.3 years in quadratic model with Age and Age²

**Interaction Terms (Interacted Regressors):**
- Model with interaction: y = β₁ + β₂x + β₃z + β₄(x×z) + u
- Create interaction variable xz = x × z and include as additional regressor in OLS
- The marginal effect of x depends on the level of z: ME_x = b₂ + b₄z
- Similarly, marginal effect of z depends on x: ME_z = b₃ + b₄x
- Individual coefficients on x, z, and x×z may be statistically insignificant due to high collinearity
- Use joint F-test to assess overall significance: H₀: β₂ = 0, β₄ = 0 tests significance of x
- Interaction terms are often highly correlated with their component variables (e.g., ρ̂ = 0.72, 0.64)
- This multicollinearity inflates standard errors but doesn't invalidate the model
- Example: Returns to education increase with age when Education×Age interaction is included

**Natural Logarithm Transformations:**
- OLS estimation works if model is linear in coefficients (e.g., ln y = β₁ + β₂x is okay)
- **Log-linear model**: ln y = β₁ + β₂x + u
  - Coefficient β₂ is a semi-elasticity: one-unit change in x → 100×β₂ percent change in y
  - Marginal effect in levels: ME_x = β₂ŷ (increases with level of y)
  - Example: b₂ = 0.0078 means one year of aging → 0.78% increase in earnings
- **Log-log model**: ln y = β₁ + β₂ ln x + u
  - Coefficient β₂ is an elasticity: 1% change in x → β₂% change in y
  - Marginal effect in levels: ME_x = β₂ŷ/x
  - Example: b₂ = 0.346 means 1% increase in age → 0.346% increase in earnings
- **Linear-log model**: y = β₁ + β₂ ln x + u (less common)
  - Marginal effect: ME_x = β₂/x
- Log transformations often improve model fit for right-skewed data (higher R²)

**Prediction from Log Models and Retransformation Bias:**
- Naive prediction from ln y = β₁ + β₂x: ŷ = exp(b₁ + b₂x) **underestimates** E[y|x]
- Problem: E[exp(u)|x] > 1 in general, so E[y|x] = exp(β₁ + β₂x) × E[exp(u)|x]
- **Retransformation bias correction** with normal homoskedastic errors:
  - ỹ = exp(s_e²/2) × exp(ln ŷ), where s_e is standard error from log regression
  - E[exp(u)|x] = exp(σ_u²/2) when u|x ~ N(0, σ_u²)
- Example: s_e = 0.4 requires rescaling by exp(0.4²/2) = exp(0.08) = 1.083 (8.3% adjustment)
- Even small s_e can matter: s_e = 0.2 → exp(0.02) = 1.020 (2% adjustment)
- Retransformation bias correction applies to log-linear, log-log, and other log-transformed models
- Alternative: Duan's smearing estimator uses (1/n)Σexp(e_i) when errors not normal

**R-squared with Transformed Dependent Variables:**
- R² measures fraction of variation in the dependent variable explained by regressors
- R² from regress y on x measures variation in y; R² from regress g(y) on x measures variation in g(y)
- **Cannot compare R² across models with different dependent variable transformations**
- For right-skewed data, R² usually higher for ln y than for y (better fit on log scale)
- For time series, R² usually higher for y than for Δy (levels vs. changes)
- Model selection based on R² only valid when dependent variable transformation is identical

**Models with Mixed Regressor Types:**
- Can combine levels, quadratics, interactions, dummies, and log transformations in one model
- Example: Earnings = f(Gender, Age, Age², Education, Worker type dummies, ln Hours)
- Interpretation requires care when mixing transformation types:
  - Binary regressor (Gender): women earn $14,330 less (levels model) or 19.3% less (log model)
  - Quadratic (Age, Age²): earnings peak at specific age, then decline
  - Log regressor (ln Hours): 1% change in hours → 0.975% change in earnings (log model)
  - Dummy variables: compare to omitted category (private sector workers)
- Always control for other regressors when interpreting any single coefficient
- Statistical significance patterns may differ between levels and log models
- Choose transformation based on economic theory, data characteristics, and model diagnostics

---

## Some in-class Exercises

(1) For $\hat{y}=2+3 x+4 x^{2}$ for a dataset with $\bar{y}=30$ and $\bar{x}=2$ give the marginal effect of a one unit change in $x$. Hence give the AME.
(2) For $\hat{y}=1+2 x+4 d+7 d \times x$ for a dataset with $\bar{y}=22, \bar{x}=3$ and $\bar{d}=0.5$ give the marginal effect of a one unit change in $x$. Hence give the AME.
(3) For model $\ln y=\beta_{1}+\beta_{2}+u$ we obtain $\widehat{\ln y}=1+2 x, n=100$, $s_{e}=0.3$. Give an estimate of $\mathrm{E}[y \mid x]$.

