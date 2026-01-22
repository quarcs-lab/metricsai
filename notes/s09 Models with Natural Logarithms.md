# Analysis of Economics Data Chapter 9: Models with Natural Logarithms 

(C) A. Colin Cameron

Univ. of Calif. Davis

November 2022

## CHAPTER 9: Models with Natural Logarithms

- Economists are often interested in measuring proportionate changes
- e.g. price elasticity of demand
- e.g. percentage change in earnings with one more year of education
- natural logarithms are useful for this.
- Additional uses of the natural logarithm include
- eliminating right skewness in data (chapter 2 )
- compounding and the rule of 72
- linearizing exponential growth.


## Outline

(1) Natural Logarithm Function
(2) Semi-elasticities and elasticities
( ) Log-linear, Log-log and Linear-Log Models
(4) Example: Earnings and Education
(5) Further Uses of the Natural Logarithm
(6) Exponential Function

Dataset: EARNINGS

### 9.1 Natural Logarithm Function

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

## Approximating Proportionate Changes

- $\Delta x=x_{1}-x_{0}$ is the change in $x$ when $x$ changes from $x_{0}$ to $x_{1}$.
- The proportionate change in $x$ is

$$
\frac{\Delta x}{x_{0}}=\frac{x_{1}-x_{0}}{x_{0}} .
$$

- Example: Change from $x_{0}=40$ to $x_{1}=40.4$
- $\Delta x=40.4-40=0.4$
- proportionate change in $x$ is $\Delta x / x_{0}=0.4 / 40=0.01$
- and percentage change is $100 \times 0.01=1 \%$.


## Approximating Proportionate Changes (continued)

- We have

$$
\begin{array}{rlrl} 
& & \frac{d \ln x}{d x} & =\frac{1}{x} \\
\Rightarrow & & \text { from calculus } \\
\Rightarrow & \frac{\Delta \ln x}{\Delta x} & \simeq \frac{1}{x} & \text { for small } \frac{\Delta x}{x} \\
\Rightarrow & \Delta \ln x & \simeq \frac{\Delta x}{x} & \\
& \text { rearranging }
\end{array}
$$

- For small proportionate changes we use the approximation

$$
\Delta \ln \mathbf{x} \simeq \frac{\Delta \mathbf{x}}{\mathbf{x}} \quad \text { for small } \frac{\Delta x}{x}\left(\text { say } \frac{\Delta x}{x}<0.1\right) .
$$

- Multiplying by 100 yields percentage changes, so equivalently

$$
\mathbf{1 0 0} \times \Delta \ln \mathbf{x} \simeq \text { Percentage change in } x \text {. }
$$

- Example: Change from $x_{0}=40$ to $x_{1}=40.4$
- approximation is $\ln (40.4)-\ln (40)=3.69883-3.68888 \simeq 0.00995$
- exact is $\Delta x / x_{0}=(40.4-40) / 40=0.01$.


### 9.2 Semi-elasticity and Elasticity

- The semi-elasticity of $y$ with respect to $x$ is the ratio of the proportionate change in $y$ to the change in the level of $x$

$$
\text { Semi }- \text { elasticity }_{y x}=\frac{\Delta y / y}{\Delta x} .
$$

- Multiplying by 100 gives the percentage change in $y$ when $x$ changes by one unit.
- Example: semi-elasticity of earnings with respect to years of schooling is 0.08
- one more year of schooling is associated with a 0.08 proportionate change in earnings
- one more year of schooling is associated with an $8 \%$ change in earnings.


## Semi-elasticity and Elasticity (continued)

- The elasticity of $y$ with respect to $x$ is the proportionate change of $y$ for a given proportionate change in $x$

$$
\text { Elasticity }_{y x}=\frac{\Delta y / y}{\Delta x / x}=\frac{\Delta y}{\Delta x} \times \frac{x}{y} .
$$

- Example price elasticity of demand for a good is -2
- a one percent increase in price leads to a 2 percent decrease in demand.


## Approximation of Semi-Elasticity and Elasticity

- Since $\frac{\Delta y}{y} \simeq \Delta \ln y$ and $\frac{\Delta x}{x} \simeq \Delta \ln x$ we obtain the following.
- Semi-elasticities and elasticities can be approximated as following

$$
\begin{aligned}
\text { Semi }- \text { elasticity }_{y x} & =\frac{\Delta y / y}{\Delta x} \simeq \frac{\Delta \ln y}{\Delta x} \\
\text { Elasticity }_{y x} & =\frac{\Delta y / y}{\Delta x / x} \simeq \frac{\Delta \ln y}{\Delta \ln x}
\end{aligned}
$$

- OLS regression of models that first transform variables to natural logarithms can directly estimate semi-elasticities and elasticities.
- Example: if $\ln y=a+b \ln x$ then the slope $b=\frac{\Delta \ln y}{\Delta \ln x}=$ the elasticity.
- so we can obtain the semi-elasticity by regressing $\ln y$ on $x$.


### 9.3 Log-linear Model

- The log-linear or log-level model regresses $\ln y$ on $x$
- with fitted value $\widehat{\ln y}=b_{1}+b_{2} x$
- the slope coefficient $b_{2}=\Delta \widehat{\ln y} / \Delta x$ is an estimate of the semi-elasticity of $y$ with respect to $x$
- we need $y>0$ since only then is $\ln y$ defined.
- This is a very common model for right-skewed data such as individual earnings.


## Log-log Model

- The $\boldsymbol{\operatorname { l o g }} \boldsymbol{-} \boldsymbol{\operatorname { l o g }} \boldsymbol{m o d e l}$ regresses $\ln y$ on $\ln x$
- with fitted value $\widehat{\ln y}=b_{1}+b_{2} \ln x$
- the slope coefficient $b_{2}=b_{2}=\Delta \widehat{\ln y} / \Delta \ln x$ is an estimate of the elasticity of $y$ with respect to $x$
- we need $y>0$ and $x>0$ since only then are $\ln y$ and $\ln x$ defined.


## Linear-log Model

- The linear-log model or level-log regresses $\ln y$ on $\ln x$
- with fitted value $\widehat{y}=b_{1}+b_{2} \ln x$
- $b_{2} / 100$ is an estimate of the change in $y$ in response to a one percent change in $x$.
- we need $x>0$ since only then is $\ln x$ defined.


## Summary: Models with Logs

- We have

| Model | Specification | Interpretation of $b_{2}$ |
| :--- | :--- | :---: |
| Linear | $\widehat{y}=b_{1}+b_{2} x$ | Slope: $\Delta y / \Delta x$ |
| Log-Linear | $\ln y=b_{1}+b_{2} x$ | Semi-elasticity: $(\Delta y / y) / \Delta x$ |
| Log-log | $\widehat{\ln y}=b_{1}+b_{2} \ln x$ | Elasticity: $(\Delta y / y) /(\Delta x / x)$ |
| Linear-log | $\widehat{y}=b_{1}+b_{2} \ln x$ | $\Delta y /(\Delta x / x)$ |

### 9.4 Example: Earnings and Education

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

## Linear Model and Log-Linear Model

- Linear model: Earnings $=-31056+5021$ Education
- Log-linear model: $\ln ($ Earnings $)=8.561+0.131$ Education
![](https://cdn.mathpix.com/cropped/7c64b055-6220-4bbe-a4f4-67774edc6d98-15.jpg?height=421&width=529&top_left_y=368&top_left_x=86)
![](https://cdn.mathpix.com/cropped/7c64b055-6220-4bbe-a4f4-67774edc6d98-15.jpg?height=423&width=534&top_left_y=368&top_left_x=646)


## Comparison of Models with Earnings Data

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


### 9.5 Approximating Natural Logarithm

- $\ln (1+x)=x-\frac{x^{2}}{2}+\frac{x^{3}}{3}-\frac{x^{4}}{4}+\frac{x^{5}}{5}-\cdots$
-e.g. $\ln (1.1)=1-0.1+\frac{0.01}{2}-\frac{0.001}{3}+\cdots \simeq 1-0.1+0.005-0.00033 \simeq 0.0953$.
- So for small $x$ we have the approximation

$$
\ln (1+x) \simeq x, \quad \text { for, say, } x<0.1
$$

- Approximation good for small $x$, but $x$ increasingly overestimates $\ln (1+x)$
- for $x<0.10$ the approximation is within five percent of $\ln (1+x)$
- for $x=0.2$, for example, the approximation is ten percent larger than $\ln 1.2=0.1823$.

|  |  | "Small" $\mathbf{x}$ |  | "'Larger" $\mathbf{x}$ |  |  |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
|  |  | $\mathrm{x}=0.05$ | $\mathrm{x}=0.10$ | $\mathrm{x}=0.15$ | $\mathrm{x}=0.20$ | $\mathrm{x}=0.50$ |
| True Value | $\ln (1+\mathrm{x})$ | 0.0488 | 0.0953 | 0.1398 | 0.1823 | 0.4055 |
| Approximation | x | 0.05 | 0.10 | 0.15 | 0.20 | 0.50 |

## Compounding and the Rule of 72

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


## Linearizing Exponential Growth

- Many data series grow according to a power law, or exponentially, over time, rather than linearly.

$$
x_{t}=x_{0} \times(1+r)^{t}
$$

- Here $x_{0}$ is value at time 0
- $x_{t}$ is value at time $t$
- $r$ is the constant growth rate (or decay rate if $r<0$ ).
- Example: $\$ 100$ invested at $3 \%$ annual interest rate for 10 years.
- annual growth rate is $r=3 / 100=0.03$
- investment worth $100 \times(1.03)^{10}$ or $\$ 134.39$ after ten years.


## Linearizing Exponential Growth (continued)

- Taking the natural logarithm of $x_{t}=x_{0} \times(1+r)^{t}$ yields

$$
\begin{aligned}
\ln x_{t} & =\ln \left(x_{0}(1+r)^{t}\right) \\
& =\ln x_{0}+\ln (1+r)^{t} \\
& =\ln x_{0}+\ln (1+r) \times t \\
& \simeq \ln x_{0}+r \times t \text { for small } r .
\end{aligned}
$$

- Exponential growth is linear growth in logs!


## Example: S\&P 500

- Standard and Poor 500 Index 1927-2019
- no inflation adjustment and no dividends
- left panel: exponential growth in level
- right panel: linear growth in logs
${ }^{\star}$ growth rate $\simeq \frac{7.8-1.8}{2019-1927}=\frac{6.0}{92}=0.065$ or $6.5 \%$ per annum
![](https://cdn.mathpix.com/cropped/7c64b055-6220-4bbe-a4f4-67774edc6d98-21.jpg?height=429&width=548&top_left_y=416&top_left_x=82)
![](https://cdn.mathpix.com/cropped/7c64b055-6220-4bbe-a4f4-67774edc6d98-21.jpg?height=429&width=550&top_left_y=416&top_left_x=644)


### 9.6 Exponential Function

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


## Approximating Exponential

- $\exp (x)=1+x+\frac{x^{2}}{2!}+\frac{x^{3}}{3!}+\frac{x^{4}}{4!}+\frac{x^{5}}{5!}+\cdots$
- e.g. $\exp (1.1)=1+0.1+\frac{0.01}{2}+\frac{0.001}{6}+\cdots$
$\simeq 1+0.1+0.005+0.00016 \simeq 1.1052$.
- So for small $x$

$$
e^{x} \simeq 1+x, \quad \text { for, say, } x<0.1 .
$$

- Approximation good for small $x$, but increasingly underestimates $e^{x}$ as $x$ increases.

Table: Approximating $\exp (\mathrm{x})$ by $1+\mathrm{x}$.
|  |  | "Small" $\mathbf{x}$ |  | "Larger" $\mathbf{x}$ |  |  |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
|  |  | $\mathrm{x}=0.05$ | $\mathrm{x}=0.10$ | $\mathrm{x}=0.15$ | $\mathrm{x}=0.20$ | $\mathrm{x}=0.50$ |
| True Value | $\exp (\mathrm{x})$ | 1.0513 | 1.1052 | 1.1618 | 1.2214 | 1.6487 |
| Approximation | $1+\mathrm{x}$ | 1.05 | 1.10 | 1.15 | 1.20 | 1.50 |


## Compound Interest Rates

- Consider compound for a year and find the annual percentage yield (APY).
- Suppose have $12 \%$ per annum then $\mathrm{APY}=12 \%$.
- Suppose compound monthly at $12 / 12=1 \%$ per month

$$
(1+0.01)^{12}=1.12683 \text { so APY }=12.683 \%
$$

- Suppose compound daily at $12 / 365 \%$ per day

$$
(1+0.12 / 365)^{365}=1.127547 \text { so } \mathrm{APY}=12.747 \%
$$

- If continuously compound for progressively smaller intervals at rate $r$

$$
(1+r / n)^{n} \rightarrow e^{r} \text { as } n \rightarrow \infty
$$

- Here $(1+0.12 / n)^{n} \rightarrow \exp (0.12)=1.12750$ or $12.750 \%$.


## Key Stata Commands

```
clear
use AED_EARNINGS.DTA
generate lnearn = ln(earnings)
generate lneduc = ln(education)
* Linear Model
regress earnings education, vce(robust)
* Log-linear Model
regress lnearn education
* Log-log Model
regress lnearn lneduc
* Linear-log Model
regress earnings lneduc
```


## Some in-class Exercises

(1) Consider numbers $a$ and $b$ with $\ln a=3.20$ and $\ln b=3.25$. Using only this information, what is the approximate percentage change in going from $a$ to $b$ ?
(2) Demand for a good falls from 100 to 90 when the price increases from 20 to 21 . Compute the price elasticity of demand.
(3) We estimate $\ln y=3+0.5 \ln x$. Give the elasticity of $y$ with respect to $x$.
(4) We estimate $\ln y=6+0.2 x$. Give the response of $y$ when $x$ changes by one unit.
(5) How long does it take for prices to double given $4 \%$ annual inflation?
(6) Suppose $y=\alpha \times(1+\beta)^{x}$. Explain how to estimate $\alpha$ and $\beta$ using OLS.

