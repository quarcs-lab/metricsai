# Appendix C: Properties of OLS and IV Estimators

- Appendix C considers properties of OLS and related estimator.
- C. 1 OLS with Independent Homoskedastic Errors
- C. 2 Robust Standard errors
- C. 3 Instrumental Variables Estimation
- C. 4 OLS with Matrix Algebra
- C. 5 Maximum Likelihood Estimation


## C.1: OLS with Independent Homoskedastic Errors

- Simplify model to make algebra easier by dropping intercept

$$
y_{i}=\beta x+u_{i} .
$$

- Then OLS estimator is

$$
b=\left(\sum_{i} x_{i}^{2}\right)^{-1} \sum_{i} x_{i} y_{i}
$$

- Also simplify by assume $x_{i}$ is a fixed regressor. Then assume.
(1) Model: $y_{i}=\beta x_{i}+u_{i}$.
(2) Zero error mean: $\mathrm{E}\left[u_{i}\right]=0$.
(3) Constant error variance: $\operatorname{Var}\left[u_{i}\right]=\sigma_{u}^{2}$.
(4) Uncorrelated errors: $\operatorname{Cov}\left[u_{i}, u_{j}\right]=0, \quad i \neq j$.


## A key result

- Given assumption 1 it is always the case that

$$
b=\beta+\left(\sum_{i} x_{i}^{2}\right)^{-1}\left(\sum_{i} x_{i} u_{i}\right) .
$$

- To obtain this result, note that

$$
\begin{aligned}
b & =\left(\sum_{i} x_{i}^{2}\right)^{-1}\left(\sum_{i} x_{i} y_{i}\right) \\
& =\left(\sum_{i} x_{i}^{2}\right)^{-1}\left(\sum_{i} x_{i}\left(\beta x_{i}+u_{i}\right)\right) \\
& =\left(\sum_{i} x_{i}^{2}\right)^{-1}\left(\sum_{i} \beta x_{i}^{2}+x_{i} u_{i}\right) \\
& =\left(\sum_{i} x_{i}^{2}\right)^{-1}\left(\sum_{i} \beta x_{i}^{2}\right)+\left(\sum_{i} x_{i}^{2}\right)^{-1}\left(\sum_{i} x_{i} u_{i}\right) \\
& =\beta+\left(\sum_{i} x_{i}^{2}\right)^{-1}\left(\sum_{i} x_{i} u_{i}\right)
\end{aligned} \text { assuming } y_{i}=\beta x_{i}+u_{i} \text {. }
$$

- The mean and variance of $b$ will depend on assumptions about $u_{i}$.


## Mean of the OLS Estimator

- Since $b=\beta+\left(\sum_{i} x_{i}^{2}\right)^{-1}\left(\sum_{i} x_{i} u_{i}\right)$ we have

$$
\begin{aligned}
\mathrm{E}[b] & =\mathrm{E}\left[\beta+\left(\sum_{i} x_{i}^{2}\right)^{-1}\left(\sum_{i} x_{i} u_{i}\right)\right] \\
& =\mathrm{E}[\beta]+\mathrm{E}\left[\left(\sum_{i} x_{i}^{2}\right)^{-1}\left(\sum_{i} x_{i} u_{i}\right)\right] \\
& =\beta+\left(\sum_{i} x_{i}^{2}\right)^{-1} \times \mathrm{E}\left[\sum_{i} x_{i} u_{i}\right] \\
& =\beta+\left(\sum_{i} x_{i}^{2}\right)^{-1} \times \sum_{i} \mathrm{E}\left[x_{i} u_{i}\right] \\
& =\beta \quad \text { if } \mathrm{E}\left[x_{i} u_{i}\right]=0 .
\end{aligned}
$$

- $\mathrm{E}\left[x_{i} u_{i}\right]=0$ given assumption 2 that $\mathrm{E}\left[u_{i}\right]=0$
- since $x_{i}$ is fixed so $\mathrm{E}\left[x_{i} u_{i}\right]=x_{i} \mathrm{E}\left[u_{i}\right]=x_{i} \times 0=0$ assuming $\mathrm{E}\left[u_{i}\right]=0$.


## Variance of OLS with Independent Homoskedastic Errors

- Since $b=\beta+\left(\sum_{i} x_{i}^{2}\right)^{-1}\left(\sum_{i} x_{i} u_{i}\right)$
the variance of $b$ is simply the variance of $\left(\sum_{i} x_{i}^{2}\right)^{-1}\left(\sum_{i} x_{i} u_{i}\right)$.
- Given independent and homoskedastic errors and fixed $x_{i}$

$$
\begin{aligned}
\operatorname{Var}[b] & =\operatorname{Var}\left[\left(\sum_{i} x_{i}^{2}\right)^{-1}\left(\sum_{i} x_{i} u_{i}\right)\right] \\
& =\left\{\left(\sum_{i} x_{i}^{2}\right)^{-1}\right\}^{2} \times \operatorname{Var}\left[\sum_{i} x_{i} u_{i}\right] \\
& =\left(\sum_{i} x_{i}^{2}\right)^{-2} \times \sum_{i} \operatorname{Var}\left[x_{i} u_{i}\right] \quad \text { by }[a Y]=a^{2} \operatorname{Var}[Y] \\
& =\left(\sum_{i} x_{i}^{2}\right)^{-2} \times \sum_{i} x_{i}^{2} \operatorname{Var}\left[u_{i}\right] \quad \text { as fixed } x_{i} \\
& =\left(\sum_{i} x_{i}^{2}\right)^{-2} \times \sum_{i} x_{i}^{2} \times \sigma_{u}^{2} \text { for homoskedastic errors. } \\
& =\sigma_{u}^{2}\left(\sum_{i} x_{i}^{2}\right)^{-1} \quad \text { simplifying. }
\end{aligned}
$$

- We estimate $\sigma_{u}^{2}$ using $s_{e}^{2}=\frac{1}{n-1} \sum_{i} e_{i}^{2}$ where $e_{i}=y_{i}-\widehat{y}_{i}$. Then

$$
\text { Estimated } \operatorname{Var}[b]=\frac{s_{e}^{2}}{\sum_{i} x_{i}^{2}} .
$$

- With an intercept $\widehat{\operatorname{Var}}[b]=\frac{s_{e}^{2}}{\sum_{i}\left(x_{i}-\bar{x}\right)^{2}}$ where $s_{e}^{2}=\frac{1}{n-2} \sum_{i} e_{i}^{2}$.


## C. 2 Robust Standard Errors Summary

- Since $b=\beta+\left(\sum_{i} x_{i}^{2}\right)^{-1}\left(\sum_{i} x_{i} u_{i}\right)$ some algebra yields

$$
\begin{aligned}
\operatorname{Var}[b] & =\left(\sum_{i} x_{i}^{2}\right)^{-2} \times \operatorname{Var}\left[\sum_{i} x_{i} u_{i}\right] \\
& =\left(\sum_{i} x_{i}^{2}\right)^{-2} \times \sum_{i} \operatorname{Var}\left[x_{i} u_{i}\right] \quad \text { if errors are independent } \\
& =\left(\sum_{i} x_{i}^{2}\right)^{-2} \times \sum_{i} \sum_{j} x_{i} x_{j} \mathrm{E}\left[u_{i} u_{j}\right] \quad \text { in general. }
\end{aligned}
$$

- This leads to robust standard error estimates where $e_{i}=y_{i}-\hat{y}_{i}$.
- Heteroskedastic independent errors

$$
\widehat{\operatorname{Var}}_{h e t}[b]=\left(\sum_{i} x_{i}^{2}\right)^{-2} x_{i}^{2} e_{i}^{2} .
$$

- Clustered (and heteroskedastic errors) where $\delta_{i j}=1$ if $i$ and $j$ in same cluster

$$
\widehat{\operatorname{Var}}_{c l u}[b]=\left(\sum_{i} x_{i}^{2}\right)^{-2} \times \sum_{i} \sum_{j} \delta_{i j} x_{i} x_{j} e_{i} e_{j} .
$$

- Autocorrelated errors (to $m$ periods apart)

$$
\begin{aligned}
\widehat{\operatorname{Var}}_{H A C}[b]= & \left(\sum_{t} x_{t}^{2}\right)^{-2} \times\left\{\sum_{t=1}^{T} x_{t}^{2} e_{t}^{2}+\frac{2 m}{m+1} \sum_{t=2}^{m} x_{t} x_{t-1} e_{t} e_{t-1}\right. \\
& \left.+\cdots+\frac{2}{m+1} \sum_{t=m}^{T} x_{t} x_{t-m} e_{t} e_{t-m}\right\}
\end{aligned}
$$

## Robust Standard Errors Algebra

- Since $b=\beta+\left(\sum_{i} x_{i}^{2}\right)^{-1}\left(\sum_{i} x_{i} u_{i}\right)$
the variance of $b$ is simply the variance of $\left(\sum_{i} x_{i}^{2}\right)^{-1}\left(\sum_{i} x_{i} u_{i}\right)$.

$$
\begin{aligned}
\operatorname{Var}[b] & =\operatorname{Var}\left[\left\{\left(\sum_{i} x_{i}^{2}\right)^{-1} \sum_{i} x_{i} u_{i}\right\}\right] \\
& =\left\{\left(\sum_{i} x_{i}^{2}\right)^{-1}\right\}^{2} \times \operatorname{Var}\left[\sum_{i} x_{i} u_{i}\right] \\
& =\left(\sum_{i} x_{i}^{2}\right)^{-2} \times \operatorname{Var}\left[\sum_{i} x_{i} u_{i}\right]
\end{aligned}
$$

- In general $\operatorname{Var}\left[\sum_{i=1}^{n} Y_{i}\right]=\sum_{i} \sum_{j} \operatorname{Cov}\left[Y_{i}, Y_{j}\right]$. So

$$
\begin{aligned}
\operatorname{Var}\left[\sum_{i} x_{i} u_{i}\right] & =\sum_{i} \sum_{j} \operatorname{Cov}\left[x_{i} u_{i}, x_{j} u_{j}\right] \\
& =\sum_{i} \sum_{j} x_{i} x_{j} \operatorname{Cov}\left[u_{i}, u_{j}\right] \\
& =\sum_{i} \sum_{j} x_{i} x_{j} \mathrm{E}\left[u_{i} u_{j}\right] \text { using } \mathrm{E}\left[u_{i}\right]=0
\end{aligned}
$$

- So

$$
\begin{aligned}
\operatorname{Var}[b] & =\left(\sum_{i} x_{i}^{2}\right)^{-2} \times \operatorname{Var}\left[\sum_{i} x_{i} u_{i}\right] \\
& =\left(\sum_{i} x_{i}^{2}\right)^{-2} \times \sum_{i} \sum_{j} x_{i} x_{j} \mathrm{E}\left[u_{i} u_{j}\right] \quad \text { in general. }
\end{aligned}
$$

## Variance with Heteroskedastic Independent Errors

- Given independent and heteroskedastic errors and fixed $x_{i}$

$$
\begin{aligned}
\mathrm{E}\left[u_{i} u_{j}\right] & =\mathrm{E}\left[u_{i}^{2}\right] \text { if } i=j \\
& =0 \text { if } i \neq j
\end{aligned}
$$

- Then

$$
\begin{aligned}
\operatorname{Var}[b] & =\left(\sum_{i} x_{i}^{2}\right)^{-2} \times \sum_{i} \sum_{j} x_{i} x_{j} \mathrm{E}\left[u_{i} u_{j}\right] \quad \text { in general } \\
& =\left(\sum_{i} x_{i}^{2}\right)^{-2} \times \sum_{i} x_{i}^{2} \mathrm{E}\left[u_{i}^{2}\right] .
\end{aligned}
$$

- We estimate $\sum_{i} x_{i}^{2} \mathrm{E}\left[u_{i}^{2}\right]$ using $\sum_{i} x_{i}^{2} e_{i}^{2}$. Then

$$
\widehat{\operatorname{Var}}_{h e t}[b]=\frac{\sum_{i} x_{i}^{2} e_{i}^{2}}{\left(\sum_{i} x_{i}^{2}\right)^{2}}
$$

## Variance with Clustered Errors

- Define

$$
\begin{aligned}
& \delta_{i j}=1 \text { if observations } i \text { and } j \text { are in the same cluster } \\
& \delta_{i j}=0 \text { otherwise. }
\end{aligned}
$$

- Then with clustered errors we assume

$$
\begin{aligned}
\operatorname{Cov}\left[u_{i}, u_{j}\right] & =\mathrm{E}\left[u_{i}, u_{j}\right] \neq 0 \text { if } \delta_{i j}=1 \\
\operatorname{Cov}\left[u_{i}, u_{j}\right] & =0 \text { if } \delta_{i j}=0
\end{aligned}
$$

- So given clustered (and heteroskedastic) errors and fixed $x_{i}$

$$
\begin{aligned}
\operatorname{Var}[b] & =\left(\sum_{i} x_{i}^{2}\right)^{-2} \times \sum_{i} \sum_{j} x_{i} x_{j} \mathrm{E}\left[u_{i} u_{j}\right] \quad \text { in general } \\
& =\left(\sum_{i} x_{i}^{2}\right)^{-2} \times \sum_{i} \sum_{j} \delta_{i j} x_{i} x_{j} \mathrm{E}\left[u_{i} u_{j}\right] .
\end{aligned}
$$

- We estimate $\sum_{i} \sum_{j} \delta_{i j} x_{i} x_{j} \mathrm{E}\left[u_{i} u_{j}\right]$ by $\sum_{i} \sum_{j} \delta_{i j} x_{i} x_{j} e_{i} e_{j}$.

$$
\widehat{\operatorname{Var}}_{c l u}[b]=\frac{\sum_{i} \sum_{j} \delta_{i j} x_{i} x_{j} e_{i} e_{j}}{\left(\sum_{i} x_{i}^{2}\right)^{2}}
$$

## Variance with Autocorrelated Errors

- Use subscript $t$ for time series (rather than subscript $i$ ).
- Assume that errors are uncorrelated after $m$ periods

$$
\begin{aligned}
\operatorname{Cov}\left[u_{t}, u_{s}\right] & \neq 0 \text { for }|t-s| \leq m \\
& =0 \text { for }|t-s|>m,
\end{aligned}
$$

- Then

$$
\begin{aligned}
& \operatorname{Var}\left[\sum_{t} x_{t} u_{t}\right]=\sum_{t} \sum_{t} x_{t} x_{s} \mathrm{E}\left[x_{t} u_{t} u_{t} u_{s}\right] \quad \text { in general } \\
= & \sum_{t} \mathrm{E}\left[x_{t} u_{t}\right]+2 \sum_{t} \mathrm{E}\left[x_{t} u_{t} x_{t-1} u_{t-1}\right] \\
& +\cdots+2 \sum_{t} \mathrm{E}\left[x_{t} u_{t}, x_{t-m} u_{t-m}\right] \text { as correlated up to } m \text { periods }
\end{aligned}
$$

- We estimate $\operatorname{Var}[b]=\left(\sum_{t} x_{t}^{2}\right)^{-2} \times \operatorname{Var}\left[\sum_{t} x_{t} u_{t}\right]$ with

$$
\begin{aligned}
\widehat{\operatorname{Var}}_{H A C}[b]= & \left(\sum_{t} x_{t}^{2}\right)^{-1} \times\left\{\sum_{t=1}^{T} x_{t}^{2} \widehat{u}_{t}^{2}+\frac{2 m}{m+1} \sum_{t=2}^{m} x_{t} x_{t-1} \widehat{u}_{t} \widehat{u}_{t-1}\right. \\
& \left.+\cdots+\frac{2}{m+1} \sum_{t=m}^{T} x_{t} x_{t-m} \widehat{u}_{t} \widehat{u}_{t-m}\right\} \times\left(\sum_{t} x_{t}^{2}\right)^{-1},
\end{aligned}
$$

## C. 3 Instrumental Variables

- Consider model without intercept: $y_{i}=\beta x_{i}+u_{i}$.
- Suppose $\operatorname{Cov}\left(x_{i}, u_{i}\right) \neq 0$. Then OLS is biased and inconsistent as

$$
\begin{aligned}
\mathrm{E}[b] & =\beta+\left(\sum_{i} x_{i}^{2}\right)^{-1} \times \sum_{i} \mathrm{E}\left[x_{i} u_{i}\right] \quad \text { from earlier OLS results } \\
& \neq \beta \quad \text { because } \mathrm{E}\left[x_{i} u_{i}\right] \neq 0 .
\end{aligned}
$$

- Instead assume there exists an instrument $z_{i}$ that is uncorrelated with the error. Specifically $\operatorname{Cov}\left(z_{i}, u_{i}\right)=0$ which implies the average $\left(\frac{1}{n} \sum_{i} z_{i} u_{i}\right) \rightarrow 0$ as $n \rightarrow \infty$.
- The instrumental variables estimator of $\beta$ is

$$
b_{I V}=\left(\sum_{i=1}^{n} z_{i} x_{i}\right)^{-1} \sum_{i=1}^{n} z_{i} y_{i} .
$$

- The instrumental variables estimator is consistent for $\beta$ since

$$
\begin{aligned}
b_{I V} & =\beta+\left(\sum_{i} z_{i} x_{i}\right)^{-1}\left(\sum_{i} z_{i} u_{i}\right) \quad \text { by algebra similar to OLS } \\
& =\beta+\left(\frac{1}{n} \sum_{i} z_{i} x_{i}\right)^{-1}\left(\frac{1}{n} \sum_{i} z_{i} u_{i}\right) \\
& \rightarrow \beta+\left(\frac{1}{n} \sum_{i} z_{i} x_{i}\right)^{-1} \times 0 \text { as } n \rightarrow \infty \text { as } \operatorname{Cov}\left(z_{i}, u_{i}\right)=0 \\
& \rightarrow \beta .
\end{aligned}
$$

## C. 4 OLS with Matrix Algebra

- Let $y_{i}=\beta_{1}+\beta_{2} x_{2 i}+\beta_{3} x_{3 i}+\cdots+\beta_{k} x_{k i}+u_{i}$.
- In vector notation this can be written as

$$
y_{i}=\left[\begin{array}{llll}
1 & x_{2 i} & \cdots & x_{k i}
\end{array}\right]\left[\begin{array}{c}
\beta_{1} \\
\beta_{2} \\
\vdots \\
\beta_{k}
\end{array}\right]+u_{i}
$$

- Stacking all $n$ equations for the $n$ observations into vectors and matrices yields

$$
\left[\begin{array}{c}
y_{1} \\
\vdots \\
y_{i} \\
\vdots \\
y_{n}
\end{array}\right]=\left[\begin{array}{cccc}
1 & x_{21} & \cdots & x_{k 1} \\
\vdots & \vdots & \vdots & \vdots \\
1 & x_{2 i} & \cdots & x_{k i} \\
\vdots & \vdots & \vdots & \vdots \\
1 & x_{2 n} & \cdots & x_{k n}
\end{array}\right]\left[\begin{array}{c}
\beta_{1} \\
\beta_{2} \\
\vdots \\
\beta_{k}
\end{array}\right]+\left[\begin{array}{c}
u_{1} \\
\vdots \\
u_{i} \\
\vdots \\
u_{n}
\end{array}\right] .
$$

## OLS with Matrix Algebra (continued)

- The stacked model can be written as

$$
\underset{(n \times 1)}{\mathbf{y}}=\underset{(n \times k)}{\mathbf{X}} \underset{(k \times 1)}{\boldsymbol{\beta}}+\underset{(n \times 1)}{\mathbf{u}}
$$

for $n \times 1$ vectors $\mathbf{y}$ and $\mathbf{u}, n \times k$ matrix $\mathbf{X}$, and $k \times 1$ vector $\boldsymbol{\beta}$.

- The OLS estimator that minimizes the sum of squared residuals $\mathbf{u}^{\prime} \mathbf{u}$ solves the so-called normal equations $\mathbf{X}^{\prime} \mathbf{u}=\mathbf{0}$ or

$$
\mathbf{X}^{\prime}(\mathbf{y}-\mathbf{X} \beta)=\mathbf{0}
$$

- Solving for $\boldsymbol{\beta}$ yields the the OLS estimator:

$$
\mathbf{b}=\left(\mathbf{X}^{\prime} \mathbf{X}\right)^{-1} \mathbf{X}^{\prime} \mathbf{y}
$$

where $\mathbf{b}$ is a $k \times 1$ vector with entries $b_{1}, b_{2}, \ldots, b_{k}$.

- Under assumptions 1-4

$$
\operatorname{Var}[\mathbf{b}]=\sigma_{u}^{2}\left(\mathbf{X}^{\prime} \mathbf{X}\right)^{-1} \text { and } \widehat{\operatorname{Var}}[\mathbf{b}]=s_{e}^{2}\left(\mathbf{X}^{\prime} \mathbf{X}\right)^{-1}
$$

where $s_{e}^{2}=\frac{1}{n-k} \sum_{i=1}^{n} \widehat{u}_{i}^{2}=\frac{1}{n-k} \widehat{\mathbf{u}}^{\prime} \widehat{\mathbf{u}}$ where $\widehat{\mathbf{u}}=\mathbf{y}-\mathbf{X b}$.

## C. 5 Maximum Likelihood Estimation

- For some types of data OLS is not appropriate.
- Then the maximum likelihood (ML) method is often used.
- This specifies a particular model for the conditional probability of the dependent variable given the regressors.
- Let $f\left(y_{i} \mid x_{i}, \theta\right)$ denote the model for the ith observation.
- The probability of observing the $n$ independent observations is then

$$
f\left(y_{1}, \ldots, y_{n} \mid x_{1}, \ldots, x_{n}, \theta\right)=f\left(y_{1} \mid x_{1}, \theta\right) \times \cdots \times f\left(y_{n} \mid x_{n}, \theta\right) .
$$

- The likelihood function reframes this probability as a function of the parameter $(s) \theta$ given the data $\left(y_{1}, x_{1}\right), \ldots,\left(x_{1}, x_{n}\right)$. Then

$$
L(\theta)=L\left(\theta \mid\left(y_{1}, x_{1}\right), \ldots,\left(y_{n}, x_{n}\right)\right)=f\left(y_{1} \mid x_{1}, \theta\right) \times \cdots \times f\left(y_{n} \mid x_{n}, \theta\right) .
$$

- We estimate $\theta$ by the value that is most likely given the data; i.e. the maximum likelihood estimator maximizes $L(\theta)$.
- Equivalently use $\theta$ that maximizes the natural logarithm of $L(\theta)$

$$
\ln L(\theta)=\ln f\left(y_{1} \mid x_{1}, \theta\right)+\cdots+\ln f\left(y_{n} \mid x_{n}, \theta\right)=\sum_{i=1}^{n} \ln f\left(y_{i} \mid x_{i}, \theta\right) .
$$

## Maximum Likelihood Estimation Properties

- The maximum likelihood estimator (MLE) of $\theta$, denoted $\widehat{\theta}_{\mathrm{ML}}$, maximizes $\ln L(\theta)=\sum_{i=1}^{n} \ln f\left(y_{i} \mid x_{i}, \theta\right)$.
- For standard problems the MLE has very desirable properties.
- Assuming $f\left(y_{i} \mid x_{i}, \theta\right)$ is correctly specified the MLE is consistent, has asymptotic distribution that is normal, and has the smallest variance among consistent and asymptotically normal estimators.
- If inference is relaxed to allow for the possibility that $f\left(y_{i} \mid x_{i}, \theta\right)$ is incorrectly specified then the MLE is called the quasi-MLE. Then inference must be based on appropriate robust standard errors.
- In general the quasi-MLE is inconsistent for $\theta$, though in the leading cases of logit, probit and Poisson regression, and the linear model with independent normally distributed errors, the quasi-MLE is still consistent for $\theta$ provided that the functional form for the conditional mean $\mathrm{E}\left[y_{i} \mid x_{i}\right]$ is correctly specified.


## Maximum Likelihood Estimation Example

- Consider regression where $y_{i}$ is a binary outcome with probability

$$
f\left(y_{i} \mid p_{i}\right)=\left\{\begin{array}{cc}
p_{i} & \text { if } y_{i}=1 \\
1-p_{i} & \text { if } y_{i}=0
\end{array}\right.
$$

- This can be rewritten as

$$
f\left(y_{i} \mid p_{i}\right)=p_{i}^{y_{i}}\left(1-p_{i}\right)^{1-y_{i}} .
$$

- The logit regression model specifies

$$
p_{i}=\Lambda\left(\beta_{1}+\beta_{2} x_{i}\right)=\exp \left(\beta_{1}+\beta_{2} x_{i}\right) /\left\{1+\exp \left(\beta_{1}+\beta_{2} x_{i}\right)\right\} .
$$

- The log-likelihood function given independent observations is then

$$
\begin{aligned}
\ln L\left(\beta_{1}, \beta_{2}\right) & =\prod_{i=1}^{n} p_{i}^{y_{i}}\left(1-p_{i}\right)^{1-y_{i}} \\
& =\sum_{i=1}^{n}\left\{y_{i} \ln p_{i}+\left(1-y_{i}\right) \ln \left(1-p_{i}\right)\right\} \\
& =\sum_{i=1}^{n}\left\{y_{i} \ln \Lambda\left(\beta_{1}+\beta_{2} x_{i}\right)+\left(1-y_{i}\right) \ln \left(1-\Lambda\left(\beta_{1}+\beta_{2}\right.\right.\right.
\end{aligned}
$$

- The ML estimates of $\beta_{1}$ and $\beta_{2}$ maximize this function.

