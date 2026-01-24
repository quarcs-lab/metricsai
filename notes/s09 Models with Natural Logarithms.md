# Chapter 9: Models with Natural Logarithms

## Learning Objectives

By the end of this chapter, you will be able to:

- Understand the natural logarithm function and its basic properties
- Use logarithmic transformations to approximate proportionate and percentage changes
- Distinguish between semi-elasticity (percentage change in y per unit change in x) and elasticity (percentage change in y per percentage change in x)
- Interpret coefficients in log-linear, log-log, and linear-log regression models
- Apply logarithmic models to analyze the relationship between earnings and education
- Use the approximation ln(1+x) ≈ x for small values of x
- Apply the Rule of 72 to calculate doubling times for compound growth
- Linearize exponential growth patterns using natural logarithms
- Understand the exponential function and its relationship to the natural logarithm

---

## 9.1 Natural Logarithm Function

- A logarithmic function is the reverse operation to raising a number to a power
- e.g. $10^{2}=100$ implies that $\log _{10} 100=2$
- if 10 raised to the power 2 equals 100 then the logarithm to the base 10 of 100 is 2 .
- More generally

$$
a^{b}=x \quad \Rightarrow \quad \log _{a} x=b ;
$$

- the logarithm to the base $a$ of $x$ equals $b$.
- Most obvious choice of the base $a$ is base 10 (decimal system).
- Economics often uses logarithm to base $e$, the natural logarithm
- where $e \simeq 2.71828 \ldots$. is a transcendental number like $\pi$

$$
\ln x=\log _{e}(x), \quad x>0 .
$$

### Approximating Proportionate Changes

- $\Delta x=x_{1}-x_{0}$ is the change in $x$ when $x$ changes from $x_{0}$ to $x_{1}$.
- The proportionate change in $x$ is

$$
\frac{\Delta x}{x_{0}}=\frac{x_{1}-x_{0}}{x_{0}} .
$$

- Example: Change from $x_{0}=40$ to $x_{1}=40.4$
- $\Delta x=40.4-40=0.4$
- proportionate change in $x$ is $\Delta x / x_{0}=0.4 / 40=0.01$
- and percentage change is $100 \times 0.01=1 \%$.

- We have

$$
\begin{aligned}
& \frac{d \ln x}{d x} = \frac{1}{x} && \text{from calculus} \\
\Rightarrow \quad & \frac{\Delta \ln x}{\Delta x} \simeq \frac{1}{x} && \text{for small } \frac{\Delta x}{x} \\
\Rightarrow \quad & \Delta \ln x \simeq \frac{\Delta x}{x} && \text{rearranging}
\end{aligned}
$$

- For small proportionate changes we use the approximation

$$
\Delta \ln \mathbf{x} \simeq \frac{\Delta \mathbf{x}}{\mathbf{x}} \quad \text{for small } \frac{\Delta x}{x}\left(\text{say } \frac{\Delta x}{x}<0.1\right) .
$$

- Multiplying by 100 yields percentage changes, so equivalently

$$
\mathbf{1 0 0} \times \Delta \ln \mathbf{x} \simeq \text{Percentage change in } x \text{.}
$$

- Example: Change from $x_{0}=40$ to $x_{1}=40.4$
- approximation is $\ln (40.4)-\ln (40)=3.69883-3.68888 \simeq 0.00995$
- exact is $\Delta x / x_{0}=(40.4-40) / 40=0.01$.

**Key Concept: Logarithmic Approximation of Proportionate Change**

For small proportionate changes, the change in the natural logarithm approximates the proportionate change: Δln x ≈ Δx/x. This relationship follows from calculus (d ln x / dx = 1/x). Multiplying by 100 converts this to percentage change: 100 × Δln x ≈ Percentage change in x. This approximation works well when Δx/x < 0.1 (i.e., changes less than 10%).

## 9.2 Semi-elasticity and Elasticity

- The semi-elasticity of $y$ with respect to $x$ is the ratio of the proportionate change in $y$ to the change in the level of $x$

$$
\text{Semi}- \text{elasticity}_{y x}=\frac{\Delta y / y}{\Delta x} .
$$

- Multiplying by 100 gives the percentage change in $y$ when $x$ changes by one unit.
- Example: semi-elasticity of earnings with respect to years of schooling is 0.08
- one more year of schooling is associated with a 0.08 proportionate change in earnings
- one more year of schooling is associated with an $8 \%$ change in earnings.

- The elasticity of $y$ with respect to $x$ is the proportionate change of $y$ for a given proportionate change in $x$

$$
\text{Elasticity}_{y x}=\frac{\Delta y / y}{\Delta x / x}=\frac{\Delta y}{\Delta x} \times \frac{x}{y} .
$$

- Example price elasticity of demand for a good is -2
- a one percent increase in price leads to a 2 percent decrease in demand.

- Since $\frac{\Delta y}{y} \simeq \Delta \ln y$ and $\frac{\Delta x}{x} \simeq \Delta \ln x$ we obtain the following.
- Semi-elasticities and elasticities can be approximated as following

$$
\begin{aligned}
\text{Semi}- \text{elasticity}_{y x} & =\frac{\Delta y / y}{\Delta x} \simeq \frac{\Delta \ln y}{\Delta x} \\
\text{Elasticity}_{y x} & =\frac{\Delta y / y}{\Delta x / x} \simeq \frac{\Delta \ln y}{\Delta \ln x}
\end{aligned}
$$

- OLS regression of models that first transform variables to natural logarithms can directly estimate semi-elasticities and elasticities.
- Example: if $\ln y=a+b \ln x$ then the slope $b=\frac{\Delta \ln y}{\Delta \ln x}=$ the elasticity.
- so we can obtain the semi-elasticity by regressing $\ln y$ on $x$.

**Key Concept: Semi-elasticity vs. Elasticity**

Semi-elasticity measures the percentage change in y per unit change in x: (Δy/y)/Δx. Elasticity measures the percentage change in y per percentage change in x: (Δy/y)/(Δx/x). Using the logarithmic approximation, semi-elasticity ≈ Δln y/Δx and elasticity ≈ Δln y/Δln x. This means we can estimate semi-elasticities by regressing ln y on x, and elasticities by regressing ln y on ln x.

## 9.3 Log-linear Model

- The log-linear or log-level model regresses $\ln y$ on $x$
- with fitted value $\widehat{\ln y}=b_{1}+b_{2} x$
- the slope coefficient $b_{2}=\Delta \widehat{\ln y} / \Delta x$ is an estimate of the semi-elasticity of $y$ with respect to $x$
- we need $y>0$ since only then is $\ln y$ defined.
- This is a very common model for right-skewed data such as individual earnings.

### Log-log Model

- The $\boldsymbol{\operatorname { l o g }} \boldsymbol{-} \boldsymbol{\operatorname { l o g }} \boldsymbol{m o d e l}$ regresses $\ln y$ on $\ln x$
- with fitted value $\widehat{\ln y}=b_{1}+b_{2} \ln x$
- the slope coefficient $b_{2}=b_{2}=\Delta \widehat{\ln y} / \Delta \ln x$ is an estimate of the elasticity of $y$ with respect to $x$
- we need $y>0$ and $x>0$ since only then are $\ln y$ and $\ln x$ defined.

### Linear-log Model

- The linear-log model or level-log regresses $\ln y$ on $\ln x$
- with fitted value $\widehat{y}=b_{1}+b_{2} \ln x$
- $b_{2} / 100$ is an estimate of the change in $y$ in response to a one percent change in $x$.
- we need $x>0$ since only then is $\ln x$ defined.

**Key Concept: Interpreting Coefficients in Log Models**

The interpretation of regression coefficients depends on which variables are logged. Log-linear (ln y on x): coefficient b₂ is the semi-elasticity (percentage change in y per unit change in x). Log-log (ln y on ln x): coefficient b₂ is the elasticity (percentage change in y per percentage change in x). Linear-log (y on ln x): coefficient b₂/100 is the change in y per one percent change in x.

- We have

| Model | Specification | Interpretation of $b_{2}$ |
| :--- | :--- | :---: |
| Linear | $\widehat{y}=b_{1}+b_{2} x$ | Slope: $\Delta y / \Delta x$ |
| Log-Linear | $\ln y=b_{1}+b_{2} x$ | Semi-elasticity: $(\Delta y / y) / \Delta x$ |
| Log-log | $\widehat{\ln y}=b_{1}+b_{2} \ln x$ | Elasticity: $(\Delta y / y) /(\Delta x / x)$ |
| Linear-log | $\widehat{y}=b_{1}+b_{2} \ln x$ | $\Delta y /(\Delta x / x)$ |

## 9.4 Example: Earnings and Education

- Dataset EARNINGS on 172 full-time male workers in 2010 aged 30 years.

| Variable | Definition | Mean | Standard Deviation | Min | Max |
| :--- | :--- | :--- | :--- | :--- | :--- |
| Earnings | Annual earnings in \$ | 41413 | 25527 | 1050 | 172000 |
| Lnearn | Natural logarithm of Earnings | 10.46 | 0.62 | 6.96 | 12.05 |
| Education | Years of completed schooling | 14.43 | 2.73 | 3 | 20 |
| Lneduc | Natural logarithm of Education | 2.65 | 0.22 | 1.10 | 3.00 |
| n | 171 |  |  |  |  |

- OLS regression of Earnings ( $y$ ) on Education ( $x$ ) yields ( t -statistics in parentheses)

$$
\widehat{y}=\underset{(-3.49)}{-31056}+\underset{(8.30)}{5021} x, \quad R^{2}=.290
$$

### Linear Model and Log-Linear Model

- Linear model: Earnings $=-31056+5021$ Education
- Log-linear model: $\ln ($ Earnings $)=8.561+0.131$ Education
![](https://cdn.mathpix.com/cropped/7c64b055-6220-4bbe-a4f4-67774edc6d98-15.jpg?height=421&width=529&top_left_y=368&top_left_x=86)
![](https://cdn.mathpix.com/cropped/7c64b055-6220-4bbe-a4f4-67774edc6d98-15.jpg?height=423&width=534&top_left_y=368&top_left_x=646)

### Comparison of Models with Earnings Data

- $y$ is earnings and $x$ is education (with $t$-statistics in parentheses).

| Model | Estimates | $R^{2}$ | Slope | Semi-elasticity | Elasticity |
| :--- | :--- | :--- | :--- | :--- | :--- |
| Linear | $\widehat{y}=\underset{(-3.49)}{-31056}+\underset{(8.30)}{5021 x}$ | 0.289 | 5021 |  |  |
| Log-linear | $\widehat{\ln y}=\underset{(40.83)}{8.561}+\underset{(9.21)}{0.131 x}$ | 0.334 | - | 0.131 |  |
| Log-log | $\ln y=\underset{(13.70)}{6.543}+\underset{(8.23)}{1.478} \ln x$ | 0.286 | - | - | 1.478 |
| Linear-log | $\hat{y}=\underset{(-5.05)}{-102767}+\underset{(7.11)}{54452} \ln x$ | 0.230 | - | - | - |

- Linear: one year more of education is associated with a \$5,021 increase in earnings
- Log-linear: one year more of education is associated with a $13.1 \%$ increase in earnings
- Log-log: $1 \%$ increase in education is associated with a $1.478 \%$ increase in earnings
- Linear-log: $1 \%$ increase in education is associated with a \$544 (= 54452/100) increase in earnings.

**Key Concept: Comparing Model Interpretations with Earnings Data**

Different logarithmic transformations provide different insights. In the earnings-education example: the log-linear model (R²=0.334) suggests one more year of education is associated with a 13.1% increase in earnings. The log-log model (R²=0.286) suggests a 1% increase in education is associated with a 1.478% increase in earnings. The linear model gives absolute dollar changes (\$5,021 per year), while log models give relative percentage changes.

## 9.5 Approximating Natural Logarithm

- $\ln (1+x)=x-\frac{x^{2}}{2}+\frac{x^{3}}{3}-\frac{x^{4}}{4}+\frac{x^{5}}{5}-\cdots$
-e.g. $\ln (1.1)=1-0.1+\frac{0.01}{2}-\frac{0.001}{3}+\cdots \simeq 1-0.1+0.005-0.00033 \simeq 0.0953$.
- So for small $x$ we have the approximation

$$
\ln (1+x) \simeq x, \quad \text{for, say, } x<0.1
$$

- Approximation good for small $x$, but $x$ increasingly overestimates $\ln (1+x)$
- for $x<0.10$ the approximation is within five percent of $\ln (1+x)$
- for $x=0.2$, for example, the approximation is ten percent larger than $\ln 1.2=0.1823$.

|  |  | "Small" $\mathbf{x}$ |  | "'Larger" $\mathbf{x}$ |  |  |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
|  |  | $\mathrm{x}=0.05$ | $\mathrm{x}=0.10$ | $\mathrm{x}=0.15$ | $\mathrm{x}=0.20$ | $\mathrm{x}=0.50$ |
| True Value | $\ln (1+\mathrm{x})$ | 0.0488 | 0.0953 | 0.1398 | 0.1823 | 0.4055 |
| Approximation | x | 0.05 | 0.10 | 0.15 | 0.20 | 0.50 |

**Key Concept: The Rule of 72**

The Rule of 72 provides a quick way to estimate doubling time for compound growth: doubling time ≈ 72/r, where r is the percentage growth rate. For example, at 4% annual growth, an investment doubles in approximately 72/4 = 18 years. This rule works because it approximates the exact formula n = ln 2/ln(1+r), using the approximations ln(1+r) ≈ r and ln 2 ≈ 0.72.

### Compounding and the Rule of 72

- Rule of 72: a series growing at percentage rate $r$ takes approximately 72/ $r$ periods to double.
- Example: Invest at $4 \%$ per annum doubles in $72 / 4=18$ years.
- Reason:
- After $n$ periods at rate $r$ investment is $(1+r)^{n}$ times larger.
- Money doubles if $n$ solves $(1+r)^{n}=2$
- Solution is $n=\ln 2 /[\ln (1+r)]$.
- Approximate: $\ln (1+r) \simeq r$ for small $r$.
- Approximate: $\ln 2=0.6931 \simeq 0.72$.
- So $n=\ln 2 /[\ln (1+r)] \simeq \mathbf{0 . 7 2} / \mathbf{r}$.
- Example: $r=0.04$ (so $4 \%$ )
- true value: $\ln 2 /[\ln (1+0.04)]=17.67$ so doubles in 17.67 years
- rule of 72 : $72 / 4=18$ so doubles in 18 years.
- More precisely can have rule of 70 , or 69 , or 69.3 .

### Linearizing Exponential Growth

- Many data series grow according to a power law, or exponentially, over time, rather than linearly.

$$
x_{t}=x_{0} \times(1+r)^{t}
$$

- Here $x_{0}$ is value at time 0
- $x_{t}$ is value at time $t$
- $r$ is the constant growth rate (or decay rate if $r<0$ ).
- Example: \$100 invested at $3 \%$ annual interest rate for 10 years.
- annual growth rate is $r=3 / 100=0.03$
- investment worth $100 \times(1.03)^{10}$ or \$134.39 after ten years.

- Taking the natural logarithm of $x_{t}=x_{0} \times(1+r)^{t}$ yields

$$
\begin{aligned}
\ln x_{t} & =\ln \left(x_{0}(1+r)^{t}\right) \\
& =\ln x_{0}+\ln (1+r)^{t} \\
& =\ln x_{0}+\ln (1+r) \times t \\
& \simeq \ln x_{0}+r \times t \text{for small } r .
\end{aligned}
$$

- Exponential growth is linear growth in logs!

**Key Concept: Linearizing Exponential Growth**

Data that grows exponentially according to x_t = x₀(1+r)^t becomes linear when transformed to logarithms: ln x_t ≈ ln x₀ + r×t. This means exponential growth in levels appears as linear growth in logs. Taking logs allows us to estimate growth rates using simple linear regression and makes it easier to visualize long-term trends that would otherwise appear curved.

### Example: S\&P 500

- Standard and Poor 500 Index 1927-2019
- no inflation adjustment and no dividends
- Left panel: exponential growth in level
- Right panel: linear growth in logs
  - Growth rate $\simeq \frac{7.8-1.8}{2019-1927}=\frac{6.0}{92}=0.065$ or $6.5 \%$ per annum
![](https://cdn.mathpix.com/cropped/7c64b055-6220-4bbe-a4f4-67774edc6d98-21.jpg?height=429&width=548&top_left_y=416&top_left_x=82)
![](https://cdn.mathpix.com/cropped/7c64b055-6220-4bbe-a4f4-67774edc6d98-21.jpg?height=429&width=550&top_left_y=416&top_left_x=644)

## 9.6 Exponential Function

- What is $e$ ?
- $e$ is an irrational number that is approximately 2.7182818
- $e$ is a transcendental number, like $\pi \simeq 3.142$
- unlike for $\pi$, there is no simple physical interpretation for $e$.
- The exponential function is denoted

$$
\exp (x)=e^{x}
$$

- The natural logarithm is the reverse operation to exponentiation.
- Then

$$
y=e^{x} \quad \Rightarrow \quad x=\ln y .
$$

- For example, $e^{2} \simeq 7.38906$ so $\ln 7.38906 \simeq 2.0$.

### Approximating Exponential

- $\exp (x)=1+x+\frac{x^{2}}{2!}+\frac{x^{3}}{3!}+\frac{x^{4}}{4!}+\frac{x^{5}}{5!}+\cdots$
- e.g. $\exp (1.1)=1+0.1+\frac{0.01}{2}+\frac{0.001}{6}+\cdots$
$\simeq 1+0.1+0.005+0.00016 \simeq 1.1052$.
- So for small $x$

$$
e^{x} \simeq 1+x, \quad \text{for, say, } x<0.1 .
$$

- Approximation good for small $x$, but increasingly underestimates $e^{x}$ as $x$ increases.

Table: Approximating $\exp (\mathrm{x})$ by $1+\mathrm{x}$.
|  |  | "Small" $\mathbf{x}$ |  | "Larger" $\mathbf{x}$ |  |  |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
|  |  | $\mathrm{x}=0.05$ | $\mathrm{x}=0.10$ | $\mathrm{x}=0.15$ | $\mathrm{x}=0.20$ | $\mathrm{x}=0.50$ |
| True Value | $\exp (\mathrm{x})$ | 1.0513 | 1.1052 | 1.1618 | 1.2214 | 1.6487 |
| Approximation | $1+\mathrm{x}$ | 1.05 | 1.10 | 1.15 | 1.20 | 1.50 |

**Key Concept: Exponential Function and Continuous Compounding**

The exponential function e^x is the inverse operation to the natural logarithm: if y = e^x then x = ln y. For small values, e^x ≈ 1 + x. The exponential function naturally arises in continuous compounding: as the compounding frequency increases, (1 + r/n)^n approaches e^r. For example, 12% compounded continuously gives an annual yield of e^0.12 = 1.12750 or 12.750%.

### Compound Interest Rates

- Consider compound for a year and find the annual percentage yield (APY).
- Suppose have $12 \%$ per annum then $\mathrm{APY}=12 \%$.
- Suppose compound monthly at $12 / 12=1 \%$ per month

$$
(1+0.01)^{12}=1.12683 \text{so APY }=12.683 \%
$$

- Suppose compound daily at $12 / 365 \%$ per day

$$
(1+0.12 / 365)^{365}=1.127547 \text{so } \mathrm{APY}=12.747 \%
$$

- If continuously compound for progressively smaller intervals at rate $r$

$$
(1+r / n)^{n} \rightarrow e^{r} \text{as } n \rightarrow \infty
$$

- Here $(1+0.12 / n)^{n} \rightarrow \exp (0.12)=1.12750$ or $12.750 \%$.


## Some in-class Exercises

(1) Consider numbers $a$ and $b$ with $\ln a=3.20$ and $\ln b=3.25$. Using only this information, what is the approximate percentage change in going from $a$ to $b$ ?
(2) Demand for a good falls from 100 to 90 when the price increases from 20 to 21 . Compute the price elasticity of demand.
(3) We estimate $\ln y=3+0.5 \ln x$. Give the elasticity of $y$ with respect to $x$.
(4) We estimate $\ln y=6+0.2 x$. Give the response of $y$ when $x$ changes by one unit.
(5) How long does it take for prices to double given $4 \%$ annual inflation?
(6) Suppose $y=\alpha \times(1+\beta)^{x}$. Explain how to estimate $\alpha$ and $\beta$ using OLS.

---

## Key Takeaways

**Natural Logarithm Basics (Section 9.1):**
- A logarithm is the reverse operation to raising a number to a power: if a^b = x then log_a(x) = b
- The natural logarithm uses base e ≈ 2.71828: ln x = log_e(x) for x > 0
- The natural logarithm is particularly useful in economics for measuring proportionate and percentage changes
- The derivative relationship d ln x / dx = 1/x provides the foundation for logarithmic approximations
- For small proportionate changes (Δx/x < 0.1), we have the approximation: Δln x ≈ Δx/x
- Multiplying by 100 converts the logarithmic change to percentage change: 100 × Δln x ≈ Percentage change in x
- This approximation allows us to interpret changes in log-transformed variables as percentage changes
- Example: if ln x changes from 3.6889 to 3.6988, this represents approximately a 1% change in x
- The approximation becomes less accurate as the proportionate change increases beyond 10%

**Semi-elasticity and Elasticity (Section 9.2):**
- Semi-elasticity measures the percentage change in y per unit change in x: (Δy/y)/Δx
- Multiplying semi-elasticity by 100 gives the percentage change in y when x changes by one unit
- Example: if semi-elasticity is 0.08, one unit increase in x is associated with an 8% increase in y
- Elasticity measures the percentage change in y per percentage change in x: (Δy/y)/(Δx/x)
- Elasticity can also be expressed as (Δy/Δx) × (x/y), the ratio of marginal to average
- Example: if price elasticity of demand is -2, a 1% price increase leads to a 2% decrease in quantity demanded
- Using logarithmic approximations: semi-elasticity ≈ Δln y/Δx and elasticity ≈ Δln y/Δln x
- OLS regression with log transformations can directly estimate semi-elasticities and elasticities
- If ln y = a + b ln x, then the slope coefficient b estimates the elasticity
- If ln y = a + b x, then the slope coefficient b estimates the semi-elasticity

**Log-linear, Log-log, and Linear-log Models (Section 9.3):**
- The log-linear (or log-level) model regresses ln y on x: ln y = b₁ + b₂x
- In the log-linear model, b₂ estimates the semi-elasticity: percentage change in y per unit change in x
- Log-linear models are commonly used for right-skewed data like earnings, house prices, or firm sizes
- The log-log model regresses ln y on ln x: ln y = b₁ + b₂ ln x
- In the log-log model, b₂ estimates the elasticity: percentage change in y per percentage change in x
- Log-log models are common for demand curves, production functions, and other relationships involving elasticities
- The linear-log (or level-log) model regresses y on ln x: y = b₁ + b₂ ln x
- In the linear-log model, b₂/100 estimates the change in y from a one percent change in x
- For log-linear and log-log models, we need y > 0 since ln y must be defined
- For log-log and linear-log models, we need x > 0 since ln x must be defined
- The choice of model depends on the theoretical relationship and the units in which results should be interpreted
- Linear model gives absolute changes (Δy/Δx), log models give relative/percentage changes

**Earnings and Education Example (Section 9.4):**
- The EARNINGS dataset contains 171 full-time male workers aged 30 in 2010
- Mean earnings: $41,413, mean education: 14.43 years
- Linear model: one more year of education → $5,021 increase in earnings (R² = 0.289)
- Log-linear model: one more year of education → 13.1% increase in earnings (R² = 0.334)
- Log-log model: 1% increase in education → 1.478% increase in earnings (R² = 0.286)
- Linear-log model: 1% increase in education → $544 increase in earnings (R² = 0.230)
- The log-linear model has the highest R², suggesting it fits the data best
- The log-linear model interpretation (13.1% per year) is more meaningful than absolute dollar amounts for policy discussions
- Different models provide different insights: absolute dollar effects vs. percentage effects
- The convex relationship between earnings and education is better captured by log transformations
- All models show statistically significant positive relationships (high t-statistics)
- The choice between models depends on whether we want to interpret results in dollar terms or percentage terms

**Approximating ln(1+x) and the Rule of 72 (Section 9.5):**
- The Taylor series expansion: ln(1+x) = x - x²/2 + x³/3 - x⁴/4 + ...
- For small x (say x < 0.1), we have the simple approximation: ln(1+x) ≈ x
- This approximation is within 5% of the true value when x < 0.10
- For larger x values, the simple approximation x increasingly overestimates ln(1+x)
- Example: when x = 0.20, the approximation 0.20 is 10% larger than ln(1.2) = 0.1823
- The Rule of 72: a series growing at rate r% takes approximately 72/r periods to double
- Example: at 4% annual growth, an investment doubles in approximately 72/4 = 18 years
- The true doubling time is n = ln 2 / ln(1+r), which uses both logarithmic concepts
- The Rule of 72 works because ln 2 ≈ 0.693 ≈ 0.72 and ln(1+r) ≈ r for small r
- More precise variants include the Rule of 70 (using 70 instead of 72) or Rule of 69.3 (using ln 2 directly)
- The Rule of 72 is particularly useful for quick mental calculations of compound growth

**Linearizing Exponential Growth (Section 9.5 continued):**
- Many economic series grow exponentially over time: x_t = x₀(1+r)^t
- Here x₀ is the initial value, x_t is the value at time t, and r is the constant growth rate
- Taking natural logarithms: ln x_t = ln x₀ + ln(1+r) × t ≈ ln x₀ + r × t for small r
- Exponential growth in levels becomes linear growth in logs
- This linearization allows us to estimate growth rates using simple linear regression
- Regressing ln x_t on t gives slope ≈ r (the growth rate) and intercept ≈ ln x₀
- Example: S&P 500 Index (1927-2019) shows exponential growth in levels but linear growth in logs
- From the S&P 500 log chart, estimated growth rate ≈ (7.8 - 1.8)/(2019 - 1927) = 6.5% per annum
- The log transformation makes it easier to visualize long-term trends that would otherwise appear highly curved
- Exponential decay (r < 0) also becomes linear in logs, with negative slope

**Exponential Function (Section 9.6):**
- The exponential function exp(x) = e^x is the inverse of the natural logarithm
- If y = e^x then x = ln y, and vice versa
- The number e ≈ 2.71828 is a transcendental number (like π) with no simple physical interpretation
- The Taylor series expansion: e^x = 1 + x + x²/2! + x³/3! + x⁴/4! + ...
- For small x (x < 0.1), we have the approximation: e^x ≈ 1 + x
- This approximation increasingly underestimates e^x as x increases
- The exponential function naturally arises in continuous compounding problems
- With rate r compounded n times per period: (1 + r/n)^n → e^r as n → ∞
- Example: 12% compounded continuously gives annual yield e^0.12 = 1.12750 or 12.750%
- Compounding more frequently increases the effective annual yield
- The exponential function grows faster than any polynomial function as x → ∞

**General Principles:**
- Logarithmic transformations are essential tools for analyzing percentage changes and growth rates in economics
- Log transformations can reduce right skewness in data distributions (making them more normally distributed)
- The choice between using levels or logs depends on whether absolute or relative changes are more meaningful
- Log models require that transformed variables are strictly positive
- Interpretation of coefficients differs fundamentally between linear and log models
- The approximations (Δln x ≈ Δx/x and e^x ≈ 1+x) only work well for small values
- Natural logarithms and exponentials are inverse operations: they undo each other
- These tools are widely applicable: returns on investments, demand elasticities, growth accounting, income distributions, etc.

---
