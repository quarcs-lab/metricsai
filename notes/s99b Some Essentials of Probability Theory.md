# Analysis of Economics Data Appendix B: Some Essentials of Probability 

(c) A. Colin Cameron Univ. of Calif. Davis

November 2022

## APPENDIX B: Some Essentials of Probability

- Appendix B considers properties of random variables.
- Probability theory for a single random variable
- chapter 3 focused on a discrete random variable

★ e.g. coin toss

- appendix also considers continuous random variables
$\star$ e.g. normal and $t$ distribution.
- Probability theory for the Sample Mean
- more detail than Chapter 3.
- Probability theory for two related random variables
- define formally concepts used in Chapter 6

★ conditional mean and conditional variance.

- define the population analogs of sample covariance and sample correlation.


## Outline

(1) Probability Theory for a Single Random Variable
(1) Discrete Random Variables, Bernoulli Distribution
(2) Linear Transformation of a Random Variable
(1) Continuous Random Variable
(1) Standard Normal Distribution, Other Continuous Distributions
(2) Probability Theory for the Sample Mean
(1) Statistical Independence
(2) Sums of Independent Random Variables
(1) Mean and Variance of the Sample Mean
(1) Law of Large Numbers, Central Limit Theorem
( ) Probability Theory for Two Related Random Variables
(1) Joint Probability
(2) Conditional Distribution, Mean, Variance
(1) Covariance and Correlation

## Appendix B.1: Single Random Variable

- We often use linear transformations of a random variable
- key result: $Y=a+b X$ has mean $a+b \mathrm{E}[X]$ and variance $a^{2} \operatorname{Var}[X]$.
- Linear transformations of a random variable $X$
- $\mathrm{E}[a]=a \quad$ expected value of a constant is a constant
- $\mathrm{E}[b X]=b \mathrm{E}[X] \quad$ mean of $b$ times $X$ is $b$ times the mean
- $\mathrm{E}[a+b X]=a+b \mathrm{E}[X] \quad$ combining
- $\operatorname{Var}[b X]=b \operatorname{Var}[X] \quad$ variance of $b$ times $X$ is $b^{2}$ times the variance

★ $\mathrm{E}\left[(b X-\mathrm{E}[b X])^{2}\right]=\mathrm{E}\left[\{b(X-\mathrm{E}[X])\}^{2}\right]$

$$
=b^{2} \mathrm{E}\left[(X-\mathrm{E}[X])^{2}\right]=b^{2} \operatorname{Var}[X]
$$

- $\operatorname{Var}[a+b X]=b^{2} \operatorname{Var}[X]$.
- Standardization for $X \sim\left(\mu, \sigma^{2}\right)$
- $\mathrm{E}[X-\mu]=\mathrm{E}[X]-\mu=\mu-\mu=0$.
- $\operatorname{Var}\left[\frac{X-\mu}{\sigma}\right]=\operatorname{Var}\left[\frac{X-\mu}{\sigma}\right]=\left(\frac{1}{\sigma}\right)^{2} \operatorname{Var}[X-\mu]=\left(\frac{1}{\sigma}\right)^{2} \sigma^{2}=1$.
- so $\frac{X-\mu}{\sigma} \sim(0,1)$
- standardize by subtract mean and divide by standard deviation.


## Continuous random variables use integration

- Discrete random variables take a limited number of values
- $\operatorname{Pr}[X=x]>0$ for all values that $x$ may take
- $\operatorname{Pr}[X \leq x]=\sum_{y \leq x} \operatorname{Pr}[X=y]=$ Sum of probabilities up to $x$
- $\mathrm{E}[X]=\sum_{x} x \cdot \operatorname{Pr}[X=x]$ weight $x$ by probabilities.
- Continuous random variables take uncountably infinite number of values, so individual probabilities do not exist.
- $\operatorname{Pr}[X=x]=0$ for all values that $x$ may take
- Continuous random variables replace summation with integration
- $\operatorname{Pr}[X \leq x]=\int_{-\infty}^{x} f(y) d y=$ Area under the density $f(\cdot)$ up to $x$
- $\mathrm{E}[X]=\int_{-\infty}^{\infty} x f(x) d x$. This weights $x$ by the density.
- Leading examples are normal, $t$ distribution, $F$ distribution.


## Standard Normal Distribution Probabilities

- Compute $\operatorname{Pr}[a<X<b]$ as the area under the probability density function between $a$ and $b$ (this is an integral)
- we cannot compute $\operatorname{Pr}[X=a]$ as it equals 0 for a continuous random variable.
- Standard normal example
- $\operatorname{Pr}[X<1.5]=\int_{-\infty}^{1.5} f(x) d x=\int_{-\infty}^{1.5} \frac{1}{\sqrt{2 \pi}} \exp \left(-x^{2} / 2\right) d x$.
- $\operatorname{Pr}[X<1.5] \simeq 0.9332$ by numerical methods

★ as the integral has no closed form solution.

- $\operatorname{Pr}[0.5<X<1.5] \simeq 0.2317$ similarly.
![](https://cdn.mathpix.com/cropped/070e37de-18d9-475e-82a4-4f69e65ff8a3-06.jpg?height=280&width=443&top_left_y=594&top_left_x=261)
![](https://cdn.mathpix.com/cropped/070e37de-18d9-475e-82a4-4f69e65ff8a3-06.jpg?height=284&width=444&top_left_y=593&top_left_x=708)


## Appendix B.2: Probability Theory for the Sample Mean

- To get the properties of $\bar{X}$ we need results on sums of random variables.
- Statistical Independence
- The random variables $X$ and $Y$ are statistically independent if the value taken by $X$ is unaffected by the value taken by $Y$
- Formally the joint probability of observing $X=x$ and $Y=y$ equals the product of the individual probabilities $\operatorname{Pr}[X=x] \times \operatorname{Pr}[Y=y]$.
- Sums of Random Variables: $X+Y$ and more generally $a X+b Y$.
- Mean: $\mathrm{E}[a X+b Y]=\mathrm{E}[a X]+\mathrm{E}[b Y]=a \mathrm{E}[X]+b \mathrm{E}[Y]$.
- Variance: if $X$ and $Y$ are statistically independent then $\operatorname{Var}[a X+b Y]=\operatorname{Var}[a X]+\operatorname{Var}[b Y]=a^{2} \operatorname{Var}[X]+b^{2} \operatorname{Var}[Y]$.


## Appendix B.2: Probability Theory for the Sample Mean

- Sample mean is the random variable $\bar{X}=\frac{1}{n} X_{1}+\frac{1}{n} X_{2}+\cdots+\frac{1}{n} X_{n}$.
- Mean of the sample mean
- $\mathrm{E}[\bar{X}]=\frac{1}{n} \mu+\frac{1}{n} \mu+\cdots+\frac{1}{n} \mu=\mu$ if the $X_{i}$ have common mean $\mu$.
- Variance of the sample mean for statistically independent data

$$
\begin{aligned}
\operatorname{Var}[\bar{X}] & =\operatorname{Var}\left[\frac{1}{n} X_{1}+\frac{1}{n} X_{2}+\ldots+\frac{1}{n} X_{n}\right] \\
& =\operatorname{Var}\left[\frac{1}{n} X_{1}\right]+\operatorname{Var}\left[\frac{1}{n} X_{2}\right]+\cdots+\operatorname{Var}\left[\frac{1}{n} X_{n}\right] \\
& =\left(\frac{1}{n}\right)^{2} \operatorname{Var}\left[X_{1}\right]+\cdots+\left(\frac{1}{n}\right)^{2} \operatorname{Var}\left[X_{n}\right] \\
& =\left(\frac{1}{n}\right)^{2} \sigma^{2}+\cdots+\left(\frac{1}{n}\right)^{2} \sigma^{2} \text { if } X_{i} \text { have common variance } \sigma^{2} \\
& =\left(\frac{1}{n}\right) \sigma .
\end{aligned}
$$

## Behavior as sample size gets large

- Results can be obtained under weaker assumptions if the sample size is very large.
- Law of Large Numbers: $\bar{X} \rightarrow \mu$ as $n \rightarrow \infty$
- this just requires just that $X_{i}$ have common mean $\mu$.
- Central Limit Theorem: $Z=(\bar{X}-\mu) / \sigma \sim N(0,1)$ as $n \rightarrow \infty$
- this requires that $X_{i}$ have common mean $\mu$ and common variance $\sigma^{2}$.
- it can be generalized to $Z=(\bar{X}-\mathrm{E}[\bar{X}]) / \operatorname{Var}[\bar{X}]$.


## Appendix B.3: Probability Theory for two Related Variables

- Here we formally define conditional mean, conditional variance and correlation that are used in the main text.
- The conditional probability that event $A$ happens given that $B$ happens is the joint probability that both $A$ and $B$ happen divided by the probability that event $B$ happens

$$
\operatorname{Pr}[A \mid B]=\frac{\operatorname{Pr}[A \text { and } B]}{\operatorname{Pr}[B]}
$$

- Now translate to random variables $X$ and $Y$.


## Conditional probability

- $\operatorname{Pr}[X=x, Y=y]$ is the joint probability of $Y$ and $X$.
- $\operatorname{Pr}[X=x]$ is the marginal probability of $X$
- it is $\operatorname{Pr}[X=x]=\sum_{y} \operatorname{Pr}[X=x, Y=y]$ (sum over all $y$.values).
- Then the conditional probability of $Y$ given $X$ :

$$
\operatorname{Pr}[Y=y \mid X=x]=\frac{\operatorname{Pr}[Y=y, X=x]}{\operatorname{Pr}[X=x]}=\frac{\text { Joint probability }}{\text { Marginal probability of } X} .
$$

- Conditional mean and conditional variance (of $Y$ given $X$ )
- mean and variance with respect to conditional distribution
- e.g. $\mathrm{E}[Y \mid X=x]=\sum_{y} y \times \operatorname{Pr}[Y=y \mid X=x]$
- the probability weighted average of $y$ where the probability used is the conditional probability if $Y$ given $X=x$.


## Covariance and Correlation

- Covariance of $X$ and $Y$
- $\operatorname{Cov}[X, Y]=\mathrm{E}\left[\left(X-\mu_{x}\right)\left(Y-\mu_{y}\right)\right]$
- calculate as $=\sum_{x} \sum_{y}\left(x-\mu_{x}\right)\left(y-\mu_{y}\right) \times \operatorname{Pr}[X=x, Y=y]$.
- Correlation of $X$ and $Y$ is the population analog of $r_{x y}$

$$
\operatorname{Cor}[X, Y]=\frac{\operatorname{Cov}[X, Y]}{\sqrt{\operatorname{Var}[X]} \sqrt{\operatorname{Var}[Y]}} .
$$

- $X$ and $Y$ are independent if

$$
\operatorname{Pr}[X=x, Y=y]=\operatorname{Pr}[X=x] \times \operatorname{Pr}[Y=y] .
$$

- $X$ and $Y$ are uncorrelated if $\operatorname{Cor}[X, Y]=0$.
- Statistical independence implies uncorrelated.


## Variance of sum of correlated variables

- We consider variance of a sum when random variables are correlated.

$$
\begin{aligned}
\operatorname{Var}\left[Y_{1}+Y_{2}\right] & =\mathrm{E}\left[\left\{\left(Y_{1}+Y_{2}\right)-\mathrm{E}\left[\left(Y_{1}+Y_{2}\right)\right]\right\}^{2}\right] \\
& =\mathrm{E}\left[\left\{\left(Y_{1}+Y_{2}\right)-\left(\mu_{1}+\mu_{2}\right)\right\}^{2}\right] \\
& =\mathrm{E}\left[\left\{\left(Y_{1}-\mu_{1}\right)+\left(Y_{2}-\mu_{2}\right)\right\}^{2}\right] \\
& =\mathrm{E}\left[\left(Y_{1}-\mu_{1}\right)^{2}+\left(Y_{2}-\mu_{2}\right)^{2}+2\left(Y_{1}-\mu_{1}\right)\left(Y_{2}-\mu_{2}\right)\right] \\
& =\mathrm{E}\left[\left(Y_{1}-\mu_{1}\right)^{2}\right]+\mathrm{E}\left[\left(Y_{2}-\mu_{2}\right)^{2}\right] \\
& +2 \mathrm{E}\left[\left(Y_{1}-\mu_{1}\right)\left(Y_{2}-\mu_{2}\right)\right] \\
& =\operatorname{Var}\left[Y_{1}\right]+\operatorname{Var}\left[Y_{2}\right]+2 \operatorname{Cov}\left[Y_{1}, Y_{2}\right] .
\end{aligned}
$$

- More generally (using $\operatorname{Cov}\left[Y_{i}, Y_{i}\right]=\operatorname{Var}\left[Y_{i}\right]$ )

$$
\operatorname{Var}\left[\sum_{i=1}^{n} Y_{i}\right]=\sum_{i} \sum_{j} \operatorname{Cov}\left[Y_{i}, Y_{j}\right] .
$$

