# Chapter 14: Regression with Indicator Variables

## Learning Objectives

By the end of this chapter, you will be able to:
- Understand indicator (dummy) variables and their role in regression analysis
- Interpret regression coefficients when regressors are categorical variables
- Use indicator variables to compare group means and test for differences
- Understand the relationship between regression on indicators and t-tests/ANOVA
- Incorporate indicator variables alongside continuous regressors to control for categories
- Create and interpret interaction terms between indicators and continuous variables
- Apply the dummy variable trap rule when using sets of mutually exclusive indicators
- Choose appropriate base categories and interpret coefficients relative to the base
- Conduct joint F-tests for the significance of sets of indicator variables
- Apply indicator variable techniques to real earnings data

---

## 14.1 Example: Earnings, Education and Type of Worker

- Dataset EARNINGS_COMPLETE
- 872 female and male full-time workers aged 25-65 years in 2000
- indicators Gender, d1, d2, d3 and interactions such as Genderbyeduc.

**Table 14.1**: Variable Definitions and Summary Statistics for EARNINGS_COMPLETE Dataset

| Variable | Definition | Mean | Standard Deviation | Min | Max |
| :--- | :--- | :--- | :--- | :--- | :--- |
|  |  |  |  |  |  |
| Earnings | Annual earnings in \$ | 56369 | 51516 | 4000 | 504000 |
| Age | Age in years | 43.31 | 10.68 | 25 | 65 |
| Gender | $=1$ if female | 0.433 | 0.496 | 0 | 1 |
| Education | Years of schooling | 13.85 | 2.88 | 0 | 20 |
| Genderbyeduc | Gender times Education | 6.08 | 7.17 | 0 | 20 |
| Age | Age in years | 43.31 | 10.68 | 25 | 65 |
| Genderbyage | Gender times Age | 19.04 | 22.87 | 0 | 65 |
| Hours | Usual hours worked per week | 44.34 | 8.50 | 35 | 99 |
| Genderbyhours | Gender times Hours | 18.56 | 21.76 | 0 | 80 |
| d1 or dself | $=1$ if self-employed | 0.089 | 0.286 | 0 | 1 |
| d2 or dpriv | $=1$ if private sector employee | 0.760 | 0.427 | 0 | 1 |
| d3 or dgovt | $=1$ if govt. sector employee | 0.149 | 0.356 | 0 | 1 |

> **Key Concept**: Indicator variables (dummy variables) are binary variables that equal 1 if an observation is in a specific category and 0 otherwise. They allow regression models to incorporate categorical information such as gender, employment type, or region. The dataset EARNINGS_COMPLETE includes indicators for Gender (1=female), and three employment types: d1 (self-employed), d2 (private sector), d3 (government sector).

## 14.2 Regression on a Single Indicator Variable

**In this section:**
- 14.2.1 Example: Earnings and gender regression
- 14.2.2 Difference in means specialized methods (t-test equivalence)

- Indicator variable takes just two values, for simplicity 0 and 1

**Definition 14.1**: Indicator Variable

$$
d= \begin{cases}1 & \text { if in the category } \\ 0 & \text { otherwise }\end{cases}
$$

- Regress $y$ on just an intercept and the indicator variable

**Equation 14.1**: Fitted Model for Regression on a Single Indicator

$$
\widehat{y}=b+a d .
$$

- Then $\hat{y}_{i}$ takes one of only two possible values

$$
\widehat{y}_{i}= \begin{cases}b+a & \text { if } d_{i}=1 \\ b & \text { if } d_{i}=0 .\end{cases}
$$

- For OLS regression it can be shown that

**Result 14.1**: OLS Estimates for Regression on a Single Indicator

$$
\begin{array}{cl}
b=\bar{y}_{0} & \text { where } \bar{y}_{0} \text { is mean of } y \text { when } d=0 \\
a=\bar{y}_{1}-\bar{y}_{0} & \text { where } \bar{y}_{1} \text { is mean of } y \text { when } d=1
\end{array}
$$

- So the slope is the difference in means across the two categories.
- Inference is based on the population model $y=\beta+\alpha d+u$.


### 14.2.1 Example: Earnings and Gender

- Earnings by gender (-1 if female)

**Table 14.2**: Earnings by Gender: Summary Statistics

| Gender | Sample size | Mean | Standard |  |  |
| :--- | :---: | :---: | :---: | :---: | :---: |
| Deviation | Min | Max |  |  |  |
| Male Earnings (Gender $=$ 0) | 494 | 63476 | 61713 | 5000 | 504000 |
| Female earnings (Gender $=1$ ) | 378 | 47080 | 31596 | 4000 | 322000 |

- OLS regression with heteroskedastic-robust standard errors

**Example 14.1**: Regression of Earnings on Gender Indicator

$$
\widehat{\text { Earnings }}=\underset{(2290)}{63476}-\underset{(3478)}{16396} \times \text { Gender } \quad R^{2}=0.025 .
$$

- Intercept $=$ mean male earnings $(d=0)=63,476$.
- Slope $=$ Difference in means $=47080-47080=-16396$
- women earn $\$ 16,396$ less on average
- statistically significant at $5 \%$ as $t=-16396 / 3478=-4.71$.

> **Key Concept**: When regressing $y$ on just an intercept and a single indicator $d$, the fitted model is $\hat{y} = b + ad$. The intercept $b$ equals the mean of $y$ when $d=0$, and the slope $a$ equals the difference in means $(\bar{y}_1 - \bar{y}_0)$. Thus, regression on an indicator variable is equivalent to a difference in means test. Here, women earn \$16,396 less on average ($t=-4.71$, statistically significant).

### 14.2.2 Difference in Means: Specialized Methods

- Many areas of statistics avoid regression
- instead use a specialized method for difference in means
- specialized t-tests yield same estimate but slightly different standard error.
- Two samples
- $d=1$ has mean $\bar{y}_{1}$, variance $s_{1}^{2}$ and $s e\left(\bar{y}_{1}\right)=s_{1} / \sqrt{n_{1}}$
- $d=0$ has mean $\bar{y}_{0}$, variance $s_{0}^{2}$ and $\operatorname{se}\left(\bar{y}_{0}\right)=s_{0} / \sqrt{n_{0}}$
- Estimate is $\bar{y}_{1}-\bar{y}_{0}=-16396$.
- Given independence of samples
- $\operatorname{Var}\left[\bar{y}_{1}-\bar{y}_{0}\right]=\operatorname{Var}\left[\bar{y}_{1}\right]+\operatorname{Var}\left[\bar{y}_{0}\right]$
- $s e^{2}\left(\bar{y}_{1}-\bar{y}_{0}\right)=s e^{2}\left(\bar{y}_{0}\right)+s e^{2}\left(\bar{y}_{0}\right)$
- $s e\left(\bar{y}_{1}-\bar{y}_{0}\right)=\sqrt{s e^{2}\left(\bar{y}_{0}\right)+s e^{2}\left(\bar{y}_{0}\right)}=\sqrt{\frac{s_{1}^{2}}{n_{1}}+\frac{s_{0}^{2}}{n 0}}$
- Here $\operatorname{se}\left(\bar{y}_{1}-\bar{y}_{0}\right)=\sqrt{\left(31596^{2} / 378\right)+\left(61713^{2} / 494\right)}=3217$.

> **Key Concept**: Specialized difference-in-means methods (like the t-test with `by(gender) unequal` option) and regression on an indicator give the same estimate but slightly different standard errors. Regression uses $se(\hat{a})$ from the regression model, while the t-test uses $se(\bar{y}_1 - \bar{y}_0) = \sqrt{s_1^2/n_1 + s_0^2/n_0}$. Both approaches are valid; regression is more flexible when adding control variables.

## 14.3 Regression on an Indicator Variable and Additional Regressors

**In this section:**
- 14.3.1 Interacted indicator variables (indicator × continuous regressor)
- 14.3.2 Indicator variable versus indicator plus interaction (graphical comparison)
- 14.3.3 Example: Earnings, gender, and education with interaction
- 14.3.4 Indicator variable as a dependent variable (logit/probit preview)

- The difference in $y$ across the two categories may be partly explained by other variables
- e.g. earnings difference by gender is partly due to hours worked.
- Now bring in additional regressors (for simplicity just one)

**Equation 14.2**: Population Model with Indicator and Additional Regressors

$$
y=\beta_{1}+\beta_{2} x+\alpha d+u .
$$

- In the fitted model $\widehat{y}=b_{1}+b_{2} x+a d$

$$
\widehat{y}_{i}= \begin{cases}b_{1}+b_{2} x_{i}+a & \text { if } d_{i}=1 \\ b_{1}+b_{2} x_{i} & \text { if } d_{i}=0 .\end{cases}
$$

- Now a measures the difference in $y$ across categories after controlling for the additional variables.


### 14.3.1 Interacted Indicator Variables

- An interacted indicator variable is a regressor that is the product of an indicator variable and another regressor.
- Consider the model that adds the term $d \times x$.

**Equation 14.3**: Model with Interacted Indicator Variable

$$
y=\beta_{1}+\beta_{2} x+\alpha_{1} d+\alpha_{2} d \times x+u
$$

- In the fitted model $\widehat{y}=b_{1}+b_{2} x+a_{1} d+a_{2} d \times x$

$$
\widehat{y}= \begin{cases}\left(b_{1}+a_{1}\right)+\left(b_{2}+a_{2}\right) x & \text { if } d=1 \\ b_{1}+b_{2} x & \text { if } d=0\end{cases}
$$

- An interacted indicator variable is a regressor that is the product of an indicator variable and another regressor.
- This enables slope coefficients to vary according to the value of the indicator variable.

> **Key Concept**: An **interacted indicator variable** is the product of an indicator and another regressor, such as $d \times x$. In the model $y = \beta_1 + \beta_2 x + \alpha_1 d + \alpha_2(d \times x) + u$, the coefficient $\alpha_2$ measures how the slope on $x$ differs between the two groups. If $d=1$, the slope is $(\beta_2 + \alpha_2)$; if $d=0$, the slope is $\beta_2$. This enables the relationship between $y$ and $x$ to vary by category.

### 14.3.2 Indicator Variable versus Indicator plus Interaction

- First panel: $\widehat{y}=b_{1}+b_{2} x+a d$
- indicator variable shifts intercept
- Second panel: $\hat{y}=b_{1}+b_{2} x+a_{1} d+a_{2} d \times x$
- additional interacted regressor $d \times x$ additionally shifts slope.

**Figure 14.1a**: Indicator Variable (Intercept Shift Only)

![](https://cdn.mathpix.com/cropped/5767ee8c-1c99-4217-b73d-65d27c8e144b-10.jpg?height=430&width=551&top_left_y=412&top_left_x=84)

**Figure 14.1b**: Indicator Plus Interaction (Intercept and Slope Shift)

![](https://cdn.mathpix.com/cropped/5767ee8c-1c99-4217-b73d-65d27c8e144b-10.jpg?height=430&width=566&top_left_y=412&top_left_x=646)

> **Key Concept**: Including only an indicator variable $d$ (without interaction) shifts the intercept but keeps slopes parallel across groups. Adding an interaction term $d \times x$ additionally allows slopes to differ. The first panel shows parallel lines (same slope, different intercepts). The second panel shows non-parallel lines (different slopes and intercepts). Use joint F-tests to test whether the interaction is statistically significant.

### 14.3.3 Example: Earnings, Gender, and Education with Interaction

- Earnings on gender and education (with heteroskedastic-robust $t$ statistics)

**Example 14.2**: Earnings on Gender and Education (No Interaction)

$$
\widehat{\text { Earnings }}=\underset{(-2.20)}{-17552}-\underset{(-5.82)}{18258} \times \text { Gender }+\underset{(-5.82)}{5907} \times \text { Education, } R^{2}=.134
$$

- Add interaction between gender and education

**Example 14.3**: Earnings on Gender and Education (With Interaction)

$$
\begin{aligned}
\widehat{\text { Earnings }}= & \underset{(-2.66)}{-31451}+\underset{(1.32)}{20219} \times \text { Gender }+\underset{(7.31)}{6921} \times \text { Education } \\
& -\underset{(-2.37)}{2765} \times \text { Gender × Education, } R^{2}=.140 .
\end{aligned}
$$

- To test whether gender is statistically significant need a joint test
- $H_{0}: \beta_{\text {gender }}=0, \beta_{\text {genderxeducation }}=0$ versus $H_{a}$ : at least one $\neq 0$
- here $F=31.92$ with $p=0.000$ so statistically significant at $5 \%$.

> **Key Concept**: When an indicator and its interaction with another variable are both included, test their **joint significance** using an F-test. Here, testing $H_0: \beta_{\text{gender}}=0, \beta_{\text{gender×education}}=0$ yields $F=31.92$ ($p=0.000$), strongly rejecting the null. Gender's effect on earnings varies with education level—the gender earnings gap is larger at lower education levels (coefficient on interaction is negative).

### 14.3.4 Indicator Variable as a Dependent Variable

- For example model employment decision
- $y=1$ if person works and $y=0$ if does not work.
- Can still do OLS
- but use heteroskedastic-robust standard errors.
- It is better to use models specific to such data
- logit model or probit model.

> **Key Concept**: When the dependent variable $y$ is an indicator (e.g., $y=1$ if employed, $y=0$ if not), you can still use OLS, but heteroskedastic-robust standard errors are essential. However, specialized models like **logit** or **probit** are preferred because they ensure predicted probabilities lie between 0 and 1, unlike OLS which can predict values outside this range.

## 14.4 Regression with Sets of Indicator Variables

**In this section:**
- 14.4.1 Example: Type of worker categories (3 mutually exclusive groups)
- 14.4.2 Dummy variable trap (why you can't include all indicators)
- 14.4.3 Base category interpretation
- 14.4.4 Hypothesis testing with indicator sets (joint F-tests)
- 14.4.5 Example: Earnings and type of worker regression results
- 14.4.6 Difference in means across multiple groups (ANOVA equivalence)

- A set of indicator variables is mutually exclusive if any individual in the sample falls into exactly one of the categories.
- then for any individual observation only one indicator variables takes value 1
- while the remaining indicator variables take value 0
- so the indicator variables sum to one: $d 1+d 2+d 3=1$.
- Indicators could be formed from categorical data that is
- unordered: such as blue, red or orange
- ordered: such as small, medium, large.


### 14.4.1 Example: Type of Worker Categories

- Type of worker that has three categories - self-employed, employed in the private sector and employed in the government sector.
- Then three mutually exclusive indicator variables are defined as

**Definition 14.2**: Three Mutually Exclusive Indicator Variables for Worker Type

$$
\begin{aligned}
& d 1= \begin{cases}1 & \text { if self-employed } \\
0 & \text { otherwise }\end{cases} \\
& d 2= \begin{cases}1 & \text { if employed in private sector } \\
0 & \text { otherwise. }\end{cases} \\
& d 3= \begin{cases}1 & \text { if employed in government sector } \\
0 & \text { otherwise. }\end{cases}
\end{aligned}
$$

### 14.4.2 Dummy Variable Trap

- Not all three indicators and an intercept can be included in the regression
- erroneous inclusion of all is called the dummy variable trap.
- Since $d 1+d 2+d 3=1$ we have $d 1=1-d 2-d 3$, so

**Derivation 14.1**: Why the Dummy Variable Trap Occurs

$$
\begin{aligned}
y & =\beta_{1}+\beta_{2} x+\alpha_{1} d 1+\alpha_{2} d 2+\alpha_{3} d 3+u \\
& =\beta_{1}+\beta_{2} x+\alpha_{1}(1-d 2-d 3)+\alpha_{2} d 2+\alpha_{3} d 3+u \\
& =\left(\beta_{1}+\alpha_{1}\right)+\beta_{2} x+\left(\alpha_{2}-\alpha_{1}\right) d 2+\left(\alpha_{3}-\alpha_{1}\right) d 3+u
\end{aligned}
$$

- We can only identify four coefficients (of intercept, $x, d 2, d 3$ )
- but have five parameters to estimate $\left(\beta_{1}, \beta_{2}, \alpha_{1}, \alpha_{2}\right.$ and $\left.\alpha_{2}\right)$.
- Solution: drop one of the indicator variables or the intercept.

> **Key Concept**: The **dummy variable trap** occurs when including all $C$ indicators from a set of mutually exclusive categories plus an intercept. Since $d_1 + d_2 + \cdots + d_C = 1$, perfect multicollinearity arises—you have $C+1$ parameters but can only identify $C$ coefficients. **Solution**: Drop one indicator (the "base category") or drop the intercept. Typically, we keep the intercept and drop one indicator.

### 14.4.3 Base Category Interpretation

- In current example $d 1$ is dropped
- coefficient $\left(\alpha_{2}-\alpha_{1}\right)$ of $d 2$ measures difference between earnings for a private sector worker $(d 2=1)$ and a self-employed worker $(d 1=1)$ after controlling for the other regressors.
- Suppose a categorical variable has C categories
- Form a set of C mutually exclusive indicator variables $\mathrm{d} 1, \mathrm{~d} 2, \ldots, \mathrm{dC}$.
- To avoid the dummy variable trap drop one of the indicator variables

  - called the omitted category or base category.

- The coefficient of an included indicator variable measures the marginal effect of being in that category compared to the base category, after controlling for the other regressors.

> **Key Concept**: The **base category** (omitted category) is the reference group. Coefficients on included indicators measure the difference in $y$ between that category and the base category, **after controlling for other regressors**. For example, if self-employed ($d_1$) is the base, the coefficient on $d_2$ (private sector) is $(\alpha_2 - \alpha_1)$, the earnings difference between private sector and self-employed workers.

### 14.4.4 Hypothesis Testing with Indicator Sets

- Care is needed in interpreting hypothesis tests.
- e.g. when $d 1$ is the omitted category the coefficient of $d 2$ measures $\left(\alpha_{2}-\alpha_{1}\right)$, so a test of statistical significance of $d 2$ is a test of $H_{0}: \alpha_{2}=\alpha_{1}$ against $H_{a}: \alpha_{2} \neq \alpha_{1}$
$\star$ it is not a test of $H_{0}: \alpha_{2}=0$ against $H_{a}: \alpha_{2} \neq 0$.
- A $t$ test of the statistical significance of a single indicator variable tests whether the ME of that category differs from that for the base category.
- It is not a test of whether the ME effect of that category is zero.
- An $F$ test of the joint statistical significance of the $\mathrm{C}-1$ included indicator variables tests whether the set of indicator variables is statistically significant.
- This joint $F$ test leads to the same result regardless of the category that is dropped.

> **Key Concept**: A **t-test on a single indicator** tests whether that category differs from the base category: $H_0: \alpha_j = \alpha_{\text{base}}$. An **F-test on all $C-1$ included indicators** tests whether the categorical variable matters at all: $H_0: \alpha_1 = \alpha_2 = \cdots = \alpha_C$. The F-test result is the same regardless of which category is dropped. Always use F-tests to evaluate the overall significance of a categorical variable.

### 14.4.5 Example: Earnings and Type of Worker Regression

- Regress earnings on all 3 categorical variables for type of worker and excluding the constant;

**Example 14.4**: Regression on All Three Worker Type Indicators (No Intercept)

$$
\widehat{y}=\underset{(9636)}{72306} d 1+\underset{(1897)}{54521} d 2-\underset{(2825)}{56105} d 3 \quad R^{2}=0.550
$$

where heteroskedastic-robust standard errors are given in parentheses.

- For OLS estimation with all three mutually exclusive categories
- the coefficients are just the sample averages for each category
- e.g. average earnings for the self-employed are $\$ 72,306$ with a standard error of \$9,636.


## Example: Earnings and Type of Worker

- Same results for $F$ test and coefficients of Age and Education regardless of what is dropped (heteroskedastic-robust $t^{\prime} s$ in [ ])

**Table 14.3**: Comparison of Regression Results for Different Base Categories

| Variable | No Indicators | Drop d1 | Drop d2 | Drop d3 | Drop intercept |
| :--- | :--- | :--- | :--- | :--- | :--- |
| Age | 525 [3.47] | 488 [3.26] | 488 [3.26] | 488 [3.26] | 488 [3.26] |
| Education | 5811 [9.06] | 5865 [8.99] | 5865 [8.99] | 5865 [8.99] | 5865 [8.99] |
| d1 (self-employed) | - <br> - |  | 17098 [1.83] | 19123 [1.99] | -30151 [-2.29] |
| $d 2$ (private sector) | - <br> - | -17098 [-2.99] | - | 2025 [0.65] | -47249 [-4.15] |
| d3 (government sector) | -- | -19123 [-1.99] | -2025 [-0.65] | -- | -49274 [-4.00] |
| Intercept | -46875 [-4.40] | -30151 [-2.29] | -47249 [-4.15] | -49274 [-4.00] | -- |
|  | - | 2.01 | 2.01 | 2.01 | 2.01 |
| $\mathrm{F}(2, \mathrm{n}-\mathrm{k})$ for indicators $\mathrm{R}^{2}$ | . 115 | . 125 | . 125 | 125 | . 601 (!) |
| Overall F | 42.85 | 22.12 | 22.12 | 22.12 | 313.06 |

### 14.4.6 Difference in Means Across Multiple Groups

- Test whether earnings vary across the type of worker, without inclusion of any controls.
- In areas of applied statistics that do not use regression
- test using analysis of variance (ANOVA) methods that extend $t$ test for difference in two means.
- Equivalently test by regress earnings on an intercept, $d 2$ and $d 3$

**Example 14.5**: Difference in Means Across Worker Types (No Controls)

$$
\widehat{y}=\underset{(7.50)}{72306}-\underset{(-1.81)}{17785} d 2-\underset{(-1.61)}{16201} d 3 \quad R^{2}=0.010
$$

where heteroskedastic-robust $t$ statistics are given in parentheses.

- Then earnings
- \$72,306 for self-employed workers, the omitted category
- $\$ 17,785$ less than this for private sector workers
- \$16,201 lower for government sector workers.
- $F$-statistic for joint statistical significance of $d 2$ and $d 3$ equals 1.68
- since $p=0.188$ there is not a statistically significant difference in earnings across the three types of workers at significance level 0.05 .

> **Key Concept**: Regressing $y$ on a set of mutually exclusive indicators (with no other controls) is equivalent to ANOVA (analysis of variance). Coefficients give group means or differences from the base mean. Here, the F-statistic $F=1.68$ ($p=0.188$) indicates no statistically significant difference in earnings across the three worker types at the 5% level—without controlling for age and education.

## 14.6 Exercises

(1) OLS regression using all data yields $\widehat{y}=3+5 d$. Give $\bar{y}$ for the subsample with $d=0$ and $\bar{y}$ for the subsample with $d=1$.
(2) Suppose $\bar{y}=30$ for the subsample with $d=1$ and $\bar{y}=20$ for the subsample with $d=0$. Give the fitted model from OLS regression of $y$ on an intercept and $d$ using the full sample.
(3) Suppose we have three mutually exclusive indicator variables $d 1, d 2$ and $d 3$. OLS yields $\hat{y}=1+3 d 2+5 d 3$. What is the estimated difference between $y$ those in category $2(d 2=1)$ and those in category $1(d 1=1)$.
(4) For the preceding fitted model, give the coefficient estimates if instead we regressed $y$ on an intercept, $d 1$ and $d 2$.

---

## Key Takeaways

**Indicator Variables Basics:**
- Indicator variables (dummy variables) are binary variables that equal 1 for observations in a specific category and 0 otherwise
- They allow regression models to incorporate categorical information (gender, employment type, region, etc.)
- Categorical variables can be unordered (colors, regions) or ordered (education levels, firm size categories)
- EARNINGS_COMPLETE dataset includes Gender (1=female, 0=male) and three worker type indicators: d1 (self-employed), d2 (private sector), d3 (government sector)
- Indicator variables are ubiquitous in applied econometrics—nearly every empirical study uses them
- Interpretation differs from continuous variables—coefficients represent group differences rather than marginal effects

**Regression on a Single Indicator and Difference in Means:**
- When regressing $y$ on just an intercept and a single indicator $d$, the fitted model is $\hat{y} = b + ad$
- The intercept $b$ equals the mean of $y$ when $d=0$ (the reference group): $b = \bar{y}_0$
- The slope $a$ equals the difference in means: $a = \bar{y}_1 - \bar{y}_0$
- Regression on an indicator is mathematically equivalent to a two-sample difference-in-means test
- The t-statistic on the slope coefficient tests whether the two group means differ significantly
- Specialized t-test methods give same estimate but slightly different standard error
- Regression uses $se(\hat{a})$ from the model; t-test uses $se(\bar{y}_1 - \bar{y}_0) = \sqrt{s_1^2/n_1 + s_0^2/n_0}$
- Example: Women earn \$16,396 less than men on average ($t=-4.71$, highly significant)
- Both approaches are valid; regression is more flexible when adding control variables

**Indicators with Continuous Regressors:**
- Adding an indicator $d$ to a regression with continuous variables: $y = \beta_1 + \beta_2 x + \alpha d + u$
- The indicator coefficient $\alpha$ measures the difference in $y$ across categories **after controlling for** $x$
- This enables testing whether group differences persist after accounting for other factors
- Example: Gender earnings gap falls from -\$16,396 (bivariate) to -\$18,258 (after controlling for education)
- Including only $d$ (without interaction) shifts the intercept but keeps slopes parallel across groups
- Fitted values: $\hat{y} = b_1 + b_2 x + a$ if $d=1$, and $\hat{y} = b_1 + b_2 x$ if $d=0$
- Parallel lines assumption: the effect of $x$ on $y$ is the same in both groups

**Interaction Terms Between Indicators and Continuous Variables:**
- An **interacted indicator** is the product of an indicator and another regressor: $d \times x$
- Model with interaction: $y = \beta_1 + \beta_2 x + \alpha_1 d + \alpha_2(d \times x) + u$
- The interaction coefficient $\alpha_2$ measures how the slope on $x$ differs between groups
- If $d=1$, the slope on $x$ is $(\beta_2 + \alpha_2)$; if $d=0$, the slope is $\beta_2$
- Adding interaction terms allows both intercepts and slopes to vary by category (non-parallel lines)
- Example: Gender earnings gap varies with education—larger at lower education levels (interaction coefficient = -2,765, $t=-2.37$)
- Always use **joint F-tests** to test significance of both the indicator and its interaction: $H_0: \beta_{\text{gender}}=0, \beta_{\text{gender×education}}=0$
- Joint F-test for gender: $F=31.92$ ($p=0.000$), strongly rejecting the null
- If the dependent variable $y$ is an indicator (e.g., $y=1$ if employed), OLS can be used but specialized models (logit, probit) are preferred

**Sets of Mutually Exclusive Indicators:**
- A set of indicators is **mutually exclusive** if each observation falls into exactly one category
- For any individual, only one indicator equals 1 while all others equal 0: $d_1 + d_2 + d_3 = 1$
- Examples: worker type (self-employed, private, government), region (Northeast, South, Midwest, West), education level
- Indicators can be formed from categorical variables that are unordered or ordered
- When including mutually exclusive indicators, must avoid the **dummy variable trap**

**Dummy Variable Trap and Base Category:**
- The **dummy variable trap** occurs when including all $C$ indicators from a mutually exclusive set plus an intercept
- Since $d_1 + d_2 + \cdots + d_C = 1$, this creates perfect multicollinearity
- You have $C+1$ parameters ($\beta_1, \alpha_1, \alpha_2, \ldots, \alpha_C$) but can only identify $C$ coefficients
- **Solution**: Drop one indicator (the "base category" or "omitted category") or drop the intercept
- Standard practice: Keep the intercept and drop one indicator
- The **base category** is the reference group—coefficients on included indicators measure differences from the base
- If self-employed ($d_1$) is omitted, coefficient on $d_2$ (private sector) is $(\alpha_2 - \alpha_1)$, the earnings difference between private sector and self-employed workers **after controlling for other regressors**
- Choice of base category is arbitrary—it doesn't affect statistical conclusions, only interpretation
- Example: Average earnings are \$72,306 for self-employed, \$17,785 less for private sector, \$16,201 less for government workers (without controls)

**Hypothesis Testing with Indicator Sets:**
- A **t-test on a single indicator** tests whether that category differs from the base category: $H_0: \alpha_j = \alpha_{\text{base}}$
- It is NOT a test of whether $\alpha_j = 0$ (unless you drop the intercept instead of an indicator)
- An **F-test on all $C-1$ included indicators** tests whether the categorical variable is significant overall: $H_0: \alpha_1 = \alpha_2 = \cdots = \alpha_C$
- The F-test result is the same regardless of which category is dropped (invariant to base category choice)
- Always use F-tests to evaluate the overall significance of a categorical variable
- Example: F-test for worker type indicators (controlling for age and education): $F=2.01$
- Regressing $y$ on a set of mutually exclusive indicators (with no other controls) is equivalent to ANOVA (analysis of variance)
- Example: Without controls, no significant earnings differences across worker types ($F=1.68$, $p=0.188$)
- Adding controls (age, education) reveals significant differences ($F=2.01$), showing importance of controlling for confounders

**Regression Results Invariance:**
- Coefficients on continuous variables (Age, Education) remain unchanged regardless of which indicator is dropped
- F-statistic for joint significance of indicator set is identical across all base category choices
- Only the indicator coefficients and intercept change interpretation when base category changes
- $R^2$ is slightly different when regressing without intercept (not directly comparable)
- Table 14.3 demonstrates this invariance across five specifications (dropping d1, d2, d3, intercept, or no indicators)

**General Lessons from Indicator Variable Regressions:**
- Indicators enable comparison of group means while controlling for other factors
- They provide flexibility to model categorical relationships in regression frameworks
- Proper interpretation requires understanding which category is the base
- Joint F-tests are essential for testing significance of multi-category variables
- Interactions with continuous variables allow relationships to vary by group
- Always use heteroskedastic-robust standard errors for valid inference
- Regression on indicators unifies many statistical tests (t-tests, ANOVA) in a single framework
- EARNINGS_COMPLETE dataset: 872 workers, showing significant gender earnings gaps that vary with education

---

