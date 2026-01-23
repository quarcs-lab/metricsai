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

Dataset API99 has data for 807 high schools in California in 1999 on
- API (Academic Performance Index) in range 200 to 1000
  - Goal is for API > 800
- Socioeconomics variables Edparent, Meals and Englearn
- school variable Yearround
- teacher variables Credteach and Emerteach.

| Variable | Definition | Mean | Standard deviation | Min | Max |
| :--- | :--- | :--- | :--- | :--- | :--- |
| Api | Academic Performance Index | 620.94 | 107.44 | 355 | 966 |
| Edparent | Average years schooling of parents | 12.84 | 1.23 | 9.62 | 16 |
| Meals | \% of students in lunch program | 21.92 | 23.67 | 0 | 98 |
| Englearn | \% of students English learners | 14.00 | 12.79 | 0 | 66 |
| Yearround | $=1$ if multi-track year-round school | 0.02 | 0.15 | 0 | 1 |
| Credteach | \% of teachers with full credentials | 89.84 | 8.44 | 33 | 100 |
| Emerteach | \% of teachers with emergency creds | 10.47 | 8.21 | 0 | 56 |

### 13.1.2 Univariate Analysis

Data are approximately normally distributed (by design)
![](https://cdn.mathpix.com/cropped/305edb9b-4075-41ef-9523-a058e126c526-05.jpg?height=415&width=546&top_left_y=325&top_left_x=78)
![](https://cdn.mathpix.com/cropped/305edb9b-4075-41ef-9523-a058e126c526-05.jpg?height=419&width=547&top_left_y=322&top_left_x=642)


### 13.1.3 Bivariate Analysis

**Example 13.1**: Bivariate Regression of API on Parent Education

$\widehat{A p i}=-400.31+79.53 \times$ Edparent, $s_{e}=43.674, R^{2}=0.835$, (15.99) (1.22)
$\bar{R}^{2}=0.834$ (heteroskedastic-robust se's in parentheses)
- One more year of parent education associated with 80 more points!
![](https://cdn.mathpix.com/cropped/305edb9b-4075-41ef-9523-a058e126c526-06.jpg?height=528&width=693&top_left_y=341&top_left_x=287)

> **Key Concept**: Parent education shows a strong positive association with school performance (API), with one additional year of parent education associated with approximately 80 more API points. However, this bivariate relationship doesn't account for other factors.


### 13.1.4 Correlations

- Pairwise correlations also moderate to high for several other variables

|  | Api | Edparent | Meals | Englearn | Yrrd | Cred | Emer |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| Api | 1 |  |  |  |  |  |  |
| Edparent | .91* | 1 |  |  |  |  |  |
| Meals | -.54* | -.60* | 1 |  |  |  |  |
| Englearn | -.66* | -.71* | .56* | 1 |  |  |  |
| Yearround | -.19* | -.25* | .29* | .22* | 1 |  |  |
| Credteach | .46* | .40* | -.27* | -.26* | -.18* | 1 |  |
| Emerteach | -.45* | -.37* | .22* | .20* | .09* | -.82* | 1 |

### 13.1.5 Multiple Regression Results

**Example 13.2**: Multiple Regression of API on All Factors

Regress API on other regressors with default se's
- Edparent coefficient little change from 79.53 to 73.94
- all six regressors jointly statistically significant $F=771.4$
- subset of five regressors other than Edparent statistically significant $F=14.80$ has $p=0.000$
- but $R^{2}$ only increases to 0.853 from 0.835 with just Edparent.

| Variable | Coefficient | St. Error | t-stat | p -value | 95\% conf. int. |  |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| Edparent | 73.942 | 1.835 | 40.29 | 0.000 | 70.339 | 77.545 |
| Meals | 0.079 | 0.092 | 0.86 | 0.390 | -0.102 | 0.260 |
| Englearn | -0.358 | 0.177 | -2.02 | 0.044 | -0.706 | -0.010 |
| Yearround | 25.956 | 10.752 | 2.41 | 0.016 | 4.850 | 47.062 |
| Credteach | 0.287 | 0.349 | 1.11 | 0.268 | -0.298 | 1.073 |
| Emerteach | -1.470 | 0.358 | -4.11 | 0.000 | -2.174 | -0.767 |
| Intercept | -345.328 | 44.027 | -7.84 | 0.000 | -431.750 | -268.905 |
| $n=$ | $F(6,22)=$ | $R^{2}=$ | $\bar{R}^{2}=$ | $s_{e}=$ |  |  |
| 807 | 771.4 | 853 | . 852 | 41.4 |  |  |

> **Key Concept**: In multiple regression, the coefficient for parent education remains strong (73.94) even after controlling for other factors. The high correlation between socioeconomic variables makes it difficult to isolate the separate effects of other educational inputs like teacher quality.


### 13.1.6 Conclusion and Implications

- Very strong association of API with socioeconomic characteristics
here parental education.
- Makes it difficult to calculate the separate role of other educational inputs
- such as teacher quality.
- California also produced a "similar schools" index
- this controls for socioeconomic characteristics.


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

- Important issue for determining market structure is whether or not returns to scale are constant, increasing or decreasing.
- e.g. with increasing returns to scale a natural monopoly may arise.
- A production function models output ( $Q$ ) as a function of capital ( $K$ ) and labor ( $L$ )
- plus possibly extra inputs such as land.
- The Cobb-Douglas production function specifies

$$
Q=\alpha K^{\beta_{2}} L^{\beta_{3}} .
$$

- With constant returns to scale doubling both inputs leads to exactly doubling output
- for Cobb-Douglas this is the case if $\beta_{2}+\beta_{3}=1$
- versus increasing if $\beta_{2}+\beta_{3}>1$ and decreasing if $\beta_{2}+\beta_{3}<1$.


### 13.2.1 Natural Logarithm Transformation

The model for $Q$ is nonlinear in $K$ and $L$
- so OLS multiple regression seems impossible.
- But OLS is possible once take logs

$$
\begin{aligned}
\ln Q & =\ln \left(A K^{\beta_{2}} L^{\beta_{3}}\right) \\
& =\ln A+\ln \left(K^{\beta_{2}}\right)+\ln \left(L^{\beta_{3}}\right) \\
& =\ln A+\beta_{2} \ln K+\beta_{3} \ln L \\
& =\beta_{1}+\beta_{2} \ln K+\beta_{3} \ln L,
\end{aligned}
$$

where $\beta_{1}=\ln \alpha$.

- This result uses the properties of natural logarithm that $\ln (a \times b)=\ln a+\ln b$ and $\ln a^{b}=b \ln a$.
- So do OLS regression of $\ln Q$ on an intercept, $\ln K$ and $\ln L$.

> **Key Concept**: Taking natural logarithms of the Cobb-Douglas production function transforms a nonlinear model into a linear model suitable for OLS regression. The resulting coefficients are elasticities that can be directly interpreted.


### 13.2.2 Original Cobb-Douglas Study Data

- Dataset COBBDOUGLAS has U.S. aggregate data on manufacturing for the 24 years from 1899 to 1922.
- From C.W. Cobb and P.H. Douglas (1928), "A Theory of Production," American Economic Review," pages 139-165.

| Year | Q | K | L | Year | Q | K | L |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 1899 | 100 | 100 | 100 | 1911 | 153 | 216 | 145 |
| 1900 | 101 | 107 | 105 | 1912 | 177 | 226 | 152 |
| 1901 | 112 | 114 | 110 | 1913 | 184 | 236 | 154 |
| 1902 | 122 | 122 | 118 | 1914 | 169 | 244 | 149 |
| 1903 | 124 | 131 | 123 | 1915 | 189 | 266 | 154 |
| 1904 | 122 | 138 | 116 | 1916 | 225 | 298 | 182 |
| 1905 | 143 | 149 | 125 | 1917 | 227 | 335 | 196 |
| 1906 | 152 | 163 | 133 | 1918 | 223 | 366 | 200 |
| 1907 | 151 | 176 | 138 | 1919 | 218 | 387 | 193 |
| 1908 | 126 | 185 | 121 | 1920 | 231 | 407 | 193 |
| 1909 | 155 | 198 | 140 | 1921 | 179 | 417 | 147 |
| 1910 | 159 | 208 | 144 | 1922 | 240 | 431 | 161 |

### 13.2.3 Regression Results

**Example 13.3**: Cobb-Douglas Production Function Estimation

Regression results
- HAC-robust standard errors (lag length 3 ) in parentheses

$$
\widehat{\ln Q}=-\underset{(.398)}{-.177}+\underset{(.062)}{.233} \times \ln K+\underset{(.134)}{.807} \times \ln K, s_{e}=0.0581, R^{2}=0.957 .
$$

- The model fits the data very well
- high $R^{2}$
- coefficients of $\ln K$ and $\ln L$ are reasonably precisely estimated and highly statistically significant at level 0.05 .
- The residuals are only slightly correlated with first three autocorrelations $0.11,-0.16$ and -0.16
- use lag length $m=3$ as $0.75 \times 24^{1 / 3}=2.16$.

> **Key Concept**: The estimated elasticities of capital (0.233) and labor (0.807) indicate that a 1% increase in capital increases output by 0.23%, while a 1% increase in labor increases output by 0.81%. Labor has a much stronger effect on production.


### 13.2.4 Testing Specified Parameter Values

- Cobb and Douglas did not estimate this model by linear regression
- instead set $\beta_{2}=.25$ and $\beta_{3}=.75$.
- Estimated coefficients are $b_{2}=0.233$ and $b_{3}=0.807$
- Test whether individually different from these values at $5 \%$
- e.g. test $H_{0}: \beta_{3}=.75$ against $H_{a}: \beta_{3} \neq 0$
$\star t=(.807-0.75) / .134=0.425$ with $p=0.675$
${ }^{\star}$ not statistically different from 0.75 at level $5 \%$.
- Joint test of $H_{0}: \beta_{2}=.25, \beta_{3}=.75$ against $H_{a}$ : at least one of $\beta_{2}, \beta_{3} \neq 0$
- $F=0.12$ with $p=\operatorname{Pr}\left[F_{2,21}>0.12\right]=0.889$.
- the restrictions are not rejected at significance level 0.05.


### 13.2.5 Testing Constant Returns to Scale

Constant returns to scale if $\beta_{2}+\beta_{3}=1$.
- $b_{2}+b_{3}=.233+.807=1.040$ is close to 1 .
- Formal test of $H_{0}: \beta_{2}+\beta_{3}=1$ against $H_{0}: \beta_{2}+\beta_{3} \neq 1$
- $F=0.23$ and $p=\operatorname{Pr}\left[F_{1,21}>0.23\right]=0.636$.
- restrictions are not rejected at significance level 0.05 .
- The data are consistent with constant returns to scale.

> **Key Concept**: The test for constant returns to scale examines whether β₂ + β₃ = 1. The estimated sum is 1.040, and formal testing fails to reject constant returns to scale (p = 0.636), consistent with the theoretical prediction for competitive markets.


### 13.2.6 Predicted Output

**Example 13.4**: Predicting Output with Retransformation

$-\widehat{\ln Q}=-.177+.233 \ln K+.807 \times \ln K$

- In prediction allow for retransformation bias (chapter 15.5)

$$
\begin{aligned}
\widehat{Q} & =\exp \left(s_{e}^{2} / 2\right) \times \exp (-.177+.233 \ln K+.807 \times \ln K) \\
& =\exp \left(.0581^{2} / 2\right) \times \exp (-.177) \times K^{.233} \times L^{.807} \\
& =.839 \times K^{.233} L^{.807}
\end{aligned}
$$

- Gives sample mean of $\widehat{Q}$ equal to 166.0 , quite close to mean of $Q$ of 165.9.
- First panel of next figure plots actual $Q$ and predicted $Q$ against time
- fit is quite good aside from final year.


### 13.2.7 Figures and Visualization

- First panel plots actual $Q$ and predicted $Q$ against time.
- Second panel gives isoquants obtained next.
![](https://cdn.mathpix.com/cropped/305edb9b-4075-41ef-9523-a058e126c526-17.jpg?height=437&width=549&top_left_y=356&top_left_x=74)
![](https://cdn.mathpix.com/cropped/305edb9b-4075-41ef-9523-a058e126c526-17.jpg?height=441&width=549&top_left_y=356&top_left_x=641)


### 13.2.8 Fitted Isoquants

Isoquants gives $K$ as function of $L$ for different values of $Q$

$$
\begin{aligned}
Q & =\alpha K^{\beta_{2}} L^{\beta_{3}} \\
\Rightarrow \quad K^{\beta_{2}} & =Q /\left(\alpha L^{\beta_{3}}\right) \\
\Rightarrow \quad K & =\alpha^{-1} Q L^{-\beta_{3}} \\
\Rightarrow \quad & =\alpha^{-1 / \beta_{2}} Q^{1 / \beta_{2}} L^{-\beta_{3} / \beta_{2}} .
\end{aligned}
$$

- Fitted values gives $K=2.140 \times Q^{4.29} \times L^{-3.46}$.
- ignores log transformation bias for simplicity
$\star$ small as $\exp \left(.0581^{2} / 2\right)=1.0017$ is close to 1.
- As expected isoquants do not cross.


### 13.2.9 HAC-Robust Standard Errors

- For time series data concern about serially correlated errors.
- Less of a problem here as residual autocorrelations $\widehat{\rho}_{1}=0.11$, $\widehat{\rho}_{2}=-0.16, \widehat{\rho}_{3}=-0.16$
- we nonetheless used them with $m=3$.
- Robust standard errors of $b_{1}$ and $b_{2}$ are
- default: 0.064 and 0.145 .
- heteroskedastic-robust: 0.105 and 0.216
- HAC $(m=3): 0.062$ and 0.134 .

> **Key Concept**: For time series data, HAC (Heteroskedasticity and Autocorrelation Consistent) standard errors account for both changing error variances and correlation over time. They provide more reliable inference than default standard errors when these issues are present.


## 13.3 Case Study 3: Phillips Curve

**In this case study:**
- 13.3.1 U.S. price inflation data
- 13.3.2 Phillips curve pre-1970
- 13.3.3 Phillips curve post-1970
- 13.3.4 Augmented Phillips curve
- 13.3.5 Figures and visualization
- 13.3.6 Omitted variables bias analysis

- Phillips curve plots price inflation against unemployment.
- A. W. Phillips (1958) found a negative relationship
- An increase in money supply may stimulate the economy in the short-run
  - Leading to lower unemployment
  - Accompanied by some increase in prices
- Importance
- can lower unemployment at the mild expense of somewhat higher price inflation.
- but fierce debate as to whether this relationship holds in the long-run.


### 13.3.1 U.S. Price Inflation Data

Dataset PHILLIPS has annual U.S. data from 1949 to 2014
- Inflation based on GDP implicit price deflator
- Later analysis uses expectations of future price inflation
- 1. Survey of Professional Forecasters from Federal Reserve Bank of Philadelphia
- 2. Ad hoc measure weighted average of inflation over past 4 years
  - $\dot{p}_{t}^{e}=0.4 \dot{p}_{t-1}+0.3 \dot{p}_{t-2}+0.2 \dot{p}_{t-3}+0.1 \dot{p}_{t-1}$, where $\dot{p}_{t}$ is inflation rate in year $t$

| Variable | Definition | Obs | Mean | St.Dev. | Min |
| :--- | :--- | :---: | :---: | :---: | :---: |
| Urate | Civilian unemployment rate (\%) | 66 | 5.87 | 1.63 | 2.70 |
| Inflation | Annual inflation rate | 66 | 3.20 | 2.32 | -1.97 |
| Expinflation | Forecast of one-year ahead Inflation | 45 | 3.31 | 2.05 | 1.14 |
| Pastinflation | Average of Inflation over past 4 years | 63 | 3.65 | 2.04 | 1.48 |

### 13.3.2 Phillips Curve Pre-1970

**Example 13.5**: Phillips Curve 1949-1969

OLS regression 1949 to 1969 looks good
- the predicted negative relationship between inflation and unemployment
- t-statistics in paranetheses based on HAC standard errors with $m=3$.

$$
\widehat{\text { Inflation }}=\underset{(4.49)}{7.111}-\underset{(-3.17)}{1.030} \times \text { Urate, } s_{e}=1.32, R^{2}=0.454, n=21 \text {, }
$$

![](https://cdn.mathpix.com/cropped/305edb9b-4075-41ef-9523-a058e126c526-22.jpg?height=427&width=539&top_left_y=423&top_left_x=81)
![](https://cdn.mathpix.com/cropped/305edb9b-4075-41ef-9523-a058e126c526-22.jpg?height=432&width=543&top_left_y=423&top_left_x=644)

> **Key Concept**: The original Phillips curve showed a negative relationship between unemployment and inflation pre-1970: higher unemployment was associated with lower inflation. This suggested a policy trade-off between unemployment and inflation.


### 13.3.3 Phillips Curve Post-1970

**Example 13.6**: Phillips Curve 1970-2014

- OLS regression 1970 to 2014 (HAC t-statistics with $m=5$ in parentheses) looks bad

$$
\widehat{\text { Inflation }}=\underset{(1.87)}{1.923}+\underset{(1.03)}{0.266} \times \text { Urate, } s_{e}=2.44, R^{2}=0.258, n=45 .
$$

- Positive though statistically insignificant relationship
- "breakdown" of the Phillips curve.

> **Key Concept**: The Phillips curve relationship broke down post-1970, showing a positive (though insignificant) relationship between unemployment and inflation. This breakdown suggests the simple model was misspecified.


### 13.3.4 Augmented Phillips Curve

**Example 13.7**: Augmented Phillips Curve 1970-2014

- The problem is that people's inflation expectations also matter
- add this as a regressor
- OLS regression 1970 to 2014 (HAC t-statistics with $m=5$ in parentheses) looks good

$$
\widehat{\text { Inflation }}=\underset{(0.43)}{0.270}-\underset{(1.54)}{0.128} \times \text { Urate }+\underset{(13.58)}{1.147} \times \text { Expinflation, } s_{e}=0.86, R^{2}
$$

- Urate now negative, though statistically insignificant at $5 \%$
- and Expinflation coefficient is close to 1 .
- Augmented Phillips curve relationship can be represented by a series of regular Phillips curves
- each curve is given for a different expected inflation rate
- e.g. for expected inflation rate of $2.0 \%$ we have

$$
\begin{aligned}
\widehat{\text { Inflation }} & =0.270-0.128 \times \text { Urate }+1.147 \times 2 \\
& =2.559-0.128 \times \text { Urate }
\end{aligned}
$$

> **Key Concept**: The augmented Phillips curve adds expected inflation as a regressor. With this addition, the unemployment coefficient returns to negative and inflation expectations have a coefficient near 1, resolving the apparent breakdown of the relationship.


### 13.3.5 Figures and Visualization

- First panel shows time series plot
- Second panel shows augmented curve for 3 expected inflation rates.
![](https://cdn.mathpix.com/cropped/305edb9b-4075-41ef-9523-a058e126c526-25.jpg?height=433&width=546&top_left_y=358&top_left_x=76)
![](https://cdn.mathpix.com/cropped/305edb9b-4075-41ef-9523-a058e126c526-25.jpg?height=436&width=547&top_left_y=358&top_left_x=641)


### 13.3.6 Omitted Variables Bias Analysis

- Observed sign reversal for the coefficient of Urate is a classic example of omitted variables bias.
- True model: Inflation $=\beta_{1}+\beta_{2} \times$ Urate $+\beta_{3} \times$ Expinflation $+u_{t}$.
- Incorrect bivariate model: Inflation $=b_{1}+b_{2} \times$ Urate.
- Omitted variables bias from chapter 16.3: $\mathrm{E}\left[b_{2}\right]=\beta_{2}+\beta_{3} \gamma$
- $\gamma$ is the coefficient of Urate in a regression of Expinflation on Urate.
- here bivariate regression of Expinflation on Urate has slope of . 343.
- Then $\widehat{\mathrm{E}\left[b_{2}\right]}=-.128+1.147 \times .343=0.266$
- equals estimated coefficient of Urate from bivariate regression of Inflation on Urate.

> **Key Concept**: The sign reversal for the unemployment coefficient is a classic example of omitted variables bias. When expected inflation is omitted, the unemployment coefficient captures both the true effect and a spurious correlation through expected inflation.


## 13.4 Automobile Efficiency

- Was better fuel efficiency of cars negated by switch to bigger more powerful cars?
- Dataset AUTOSMPG has annual data on most models of cars and light trucks on sale in the U.S. from 1980 to 2006 ( $n=27,871$ ).
- Model fuel efficiency (m.p.g.) which decreases with increased horsepower, car weight and torque.
- Estimate log-log model.
- Find that greatly increased fuel efficiency from 1980 to 1960 has been completely negated by heavier more powerful vehicles.
- Use cluster-robust standard errors with clustering on car manufacturer
- because errors are correlated within manufacturer.


## 13.5 Rand Health Insurance Experiment

- Does better health insurance increase consumption of health care?
- 1970's randomized control trial experiment (to give a causal estimate)
- randomly assign different levels of health insurance to different families.
- Dataset HEALTHINSEXP has 20,203 individual-year observations on 5,915 individuals in 2,205 families in experiment for 3 years or 5 years.
- Use data for the first year of experiment and only selected variables.
- $y=$ total annual spending on health
- $x$ includes six different insurance plans ranging from $0 \%$ coinsurance (free care) to $95 \%$ coinsurance.
- Find that spending increases with better health insurance
- joint F test finds statistically significant at $5 \%$
- use cluster-robust standard errors with clustering on family.


## 13.6 Access to Health Care and Health Status

- Does greater access to health care improve health status?
- 1994 South Africa policy change
- increase access to health care for children in communities with clinics.
- Use difference-in-differences method (to give a causal estimate)
- change over time for treated (children in communities with clinics) minus change over time for untreated (children in communities without clinics).
- Dataset HEALTHACCESS has data on children ages 0 to 4 .
- Outcome is a weight-for-age z-score
- so normed to have mean 0 and standard deviation 1 for a representative world-wide population.
- Estimate is a 0.522 increase in weight-for-age z -score
- and increase of 0.516 when controls variables are added.
- Use cluster-robust standard errors with clustering on community.


## 13.7 Gains to Political Incumbency

- Does being an incumbent increase the probability of winning the next election?
- Use regression discontinuity method (to give a causal estimate)
- compare party vote in subsequent election if party just won the senate seat to that if party just lost the senate seat.
- Dataset INCUMBENCY has data on 1,390 Senate seat elections from 1914 to 2010.
- Estimated effect is a $5 \%$ to $7 \%$ increase in the vote if win previous election.
- Use heteroskedastic-robust standard errors
- cluster-robust standard errors with clustering on state are similar.


## 13.8 Institutions and Country GDP

- Do better institutions lead to higher GDP?
- Use instrumental variables estimator (chapter 17.4) rather than OLS (to get a causal estimate).
- Dataset INSTITUTIONS has data on 64 countries settled by Europeans.
- outcome is log GDP per capita in 1995
- regressor is average protection against appropriation risk
- instrument is log settler mortality (many years in the past)
- Find that better institutions lead to higher GDP.


## 13.9 From Raw Data to Final Data

- Going from raw data to a final dataset for analysis can be difficult
- recently labelled as data carpentry or data wrangling.
- First task: read any sort of data into a statistical package
- Excel spreadsheets (with extension .xls or .xlsx)
- plain text file with character-separated values (with extension .csv)
- a data file formatted for a commonly-used statistical package
- a table in a PDF document (with extension .pdf)
- hardcopy data may be scanned and digitized using e.g. Adobe Acrobat
- web data obtained using a web scraping program. \}
- Second task: combine data from multiple sources
- merging data requires care.
- Third task: cleaning the data
- entails recoding data and detecting data that are in error.
- And in many places: check the data.

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
- **Regression discontinuity (13.7)**: Political incumbency provides 5-7% vote share advantage
- **Instrumental variables (13.8)**: Better institutions causally increase country GDP
- Each method addresses specific identification challenges for causal inference

**Data Preparation and Practical Workflow (Case Study 13.9):**
- Real data analysis requires extensive data carpentry/wrangling
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

