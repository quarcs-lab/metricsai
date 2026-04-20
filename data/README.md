# metricsAI Data Dictionary

This directory contains all datasets used in the metricsAI course. Every dataset can be loaded directly from GitHub into Python — no downloads required.

## Quick Start

Copy any line below into a Python notebook and the dataset loads automatically:

```python
import pandas as pd
df = pd.read_stata("https://raw.githubusercontent.com/quarcs-lab/data-open/master/AED/AED_HOUSE.DTA")
df.head()
```

[Open an empty Google Colab notebook](https://colab.research.google.com/notebooks/empty.ipynb) to try it.

## Summary

| Dataset | Obs | Vars | Description | Chapters |
|---------|----:|-----:|-------------|----------|
| AED_HOUSE | 29 | 8 | House prices in Davis, CA | 1, 5, 7, 10-12 |
| AED_EARNINGS | 171 | 4 | Earnings, education, age, gender | 2, 4, 8, 9 |
| AED_EARNINGSMALE | 191 | 4 | Male earnings subset | 4 |
| AED_EARNINGS_COMPLETE | 872 | 45 | Full labor market survey | 14-17 |
| AED_HEALTH2009 | 34 | 13 | OECD health expenditures | 8 |
| AED_HEALTHINSEXP | 20,203 | 29 | RAND Health Insurance Experiment | 13 |
| AED_HEALTHACCESS | 1,071 | 26 | Healthcare access (South Africa) | 13 |
| AED_HEALTHCATEGORIES | 13 | 4 | U.S. health spending categories | 2 |
| AED_CAPM | 354 | 13 | Stock returns (CAPM) | 8 |
| AED_AUTOSMPG | 26,995 | 21 | Automobile fuel efficiency | 13 |
| AED_COBBDOUGLAS | 24 | 7 | Cobb-Douglas production data | 13 |
| AED_DEMOCRACY | 131 | 16 | Democracy and development | 16 |
| AED_INSTITUTIONS | 64 | 35 | Colonial institutions and GDP | 13 |
| AED_RETURNSTOSCHOOLING | 3,010 | 101 | Returns to education (IV) | 13 |
| AED_NBA | 286 | 65 | NBA team revenue panel | 17 |
| AED_INCUMBENCY | 1,390 | 9 | U.S. Senate incumbency (RDD) | 13 |
| AED_FISHING | 1,182 | 17 | Recreational fishing choices | 2 |
| AED_GDPUNEMPLOY | 59 | 5 | U.S. GDP and unemployment | 8 |
| AED_PHILLIPS | 66 | 14 | Phillips curve (inflation/unemployment) | 13 |
| AED_INTERESTRATES | 397 | 19 | U.S. interest rates and yield curves | 17 |
| AED_REALGDPPC | 245 | 12 | U.S. real GDP per capita | 2, 4, 8, 12 |
| AED_SP500INDEX | 93 | 3 | S&P 500 annual index | 9 |
| AED_GASPRICE | 32 | 2 | Gasoline prices (Yolo County) | 4 |
| AED_MONTHLYHOMESALES | 193 | 9 | U.S. monthly home sales | 2 |
| AED_GENERATEDDATA | 5 | 4 | Simulated regression example | 6 |
| AED_COINTOSSMEANS | 400 | 3 | Coin toss simulation means | 3 |
| AED_CENSUSAGEMEANS | 100 | 3 | 1880 Census age sample means | 3 |
| AED_CENSUSREGRESSIONS | 400 | 5 | 1880 Census regression samples | 3 |
| AED_API99 | 807 | 17 | California school performance | 13 |

---

## Detailed Data Dictionary

Each entry below includes the full self-contained load command, variable list, original source, and description.

---

### AED_HOUSE.DTA

**House prices in Central Davis, California (1999)**

```python
df = pd.read_stata("https://raw.githubusercontent.com/quarcs-lab/data-open/master/AED/AED_HOUSE.DTA")
```

- **Observations:** 29
- **Variables (8):** `price`, `size`, `bedrooms`, `bathrooms`, `lotsize`, `age`, `monthsold`, `list`
- **Source:** Author collection, Central Davis, CA
- **Used in:** Chapters 1, 5, 7, 10, 11, 12
- **Description:** Cross-section of 29 house sales. The primary teaching dataset for introducing regression analysis. Price is the sale price in dollars; size is square footage. Used to demonstrate scatter plots, OLS estimation, confidence intervals, hypothesis tests, and multiple regression.

---

### AED_EARNINGS.DTA

**Earnings, education, and demographics**

```python
df = pd.read_stata("https://raw.githubusercontent.com/quarcs-lab/data-open/master/AED/AED_EARNINGS.DTA")
```

- **Observations:** 171
- **Variables (4):** `earnings`, `education`, `age`, `gender`
- **Source:** 2010 American Community Survey via IPUMS USA
- **Used in:** Chapters 2, 4, 8, 9
- **Description:** Sample of individual earnings with education, age, and gender. Used for univariate summaries, hypothesis testing, and log-earnings models. Earnings are annual in dollars; education is years of schooling; gender is binary (0/1).

---

### AED_EARNINGSMALE.DTA

**Male earnings subset**

```python
df = pd.read_stata("https://raw.githubusercontent.com/quarcs-lab/data-open/master/AED/AED_EARNINGSMALE.DTA")
```

- **Observations:** 191
- **Variables (4):** `earnings`, `education`, `age`, `gender`
- **Source:** 2010 American Community Survey via IPUMS USA
- **Used in:** Chapter 4
- **Description:** Male-only subset for comparing inference results across gender subsamples.

---

### AED_EARNINGS_COMPLETE.DTA

**Complete labor market survey**

```python
df = pd.read_stata("https://raw.githubusercontent.com/quarcs-lab/data-open/master/AED/AED_EARNINGS_COMPLETE.DTA")
```

- **Observations:** 872
- **Variables (45):** `earnings`, `lnearnings`, `dearnings`, `gender`, `age`, `lnage`, `agesq`, `education`, `educsquared`, `agebyeduc`, `genderbyage`, `genderbyeduc`, `hours`, `lnhours`, `genderbyhours`, `dself`, `dprivate`, `dgovt`, `state`, `statefip`, `stateunemp`, `stateincomepc`, `year`, `pernum`, `perwt`, `relate`, `region`, `metro`, `marst`, `race`, `raced`, `hispan`, `racesing`, `hcovany`, `attainededuc`, `detailededuc`, `empstat`, `classwkr`, `classwkrd`, `wkswork2`, `workedyr`, `inctot`, `incwage`, `incbus00`, `incearn`
- **Source:** 2010 American Community Survey via IPUMS USA
- **Used in:** Chapters 14, 15, 16, 17
- **Description:** The most comprehensive earnings dataset. Includes pre-computed transformations (log earnings, age squared, interaction terms), employment type indicators (self-employed, private, government), geographic identifiers, and demographic controls. Central dataset for multiple regression, indicator variables, transformed variables, and model diagnostics.

---

### AED_HEALTH2009.DTA

**OECD health expenditure and outcomes (2009)**

```python
df = pd.read_stata("https://raw.githubusercontent.com/quarcs-lab/data-open/master/AED/AED_HEALTH2009.DTA")
```

- **Observations:** 34
- **Variables (13):** `country_name`, `year`, `hlthgdp`, `hlthpc`, `infmort`, `lifeexp`, `gdppc`, `code`, `hlthpcsq`, `lnhlthpc`, `lngdppc`, `lnlifeexp`, `lninfmort`
- **Source:** OECD Health Statistics 2022
- **Used in:** Chapter 8
- **Description:** Cross-country comparison of health spending, life expectancy, and infant mortality for 34 OECD countries. Includes per-capita health expenditure, GDP per capita, and their log transformations. Used to study income elasticity of health spending.

---

### AED_HEALTHINSEXP.DTA

**RAND Health Insurance Experiment**

```python
df = pd.read_stata("https://raw.githubusercontent.com/quarcs-lab/data-open/master/AED/AED_HEALTHINSEXP.DTA")
```

- **Observations:** 20,203
- **Variables (29):** `idperson`, `idfamily`, `year`, `site`, `plan`, `mde`, `coins0`, `coins25`, `coinsmixed`, `coins50`, `coinsindiv`, `coins95`, `coinsrate`, `spending`, `inpat`, `outpat`, `out_rand_infl`, `dental`, `mental`, `drugs`, `supplies`, `oop`, `age`, `famincome`, `gender`, `educ`, `badhealth`, `goodhealth`, `exchealth`
- **Source:** Aron-Dine, Einav, Finkelstein (2013); original RAND HIE data
- **Used in:** Chapter 13
- **Description:** The landmark randomized controlled trial in health economics. Families were randomly assigned to insurance plans with different coinsurance rates (0%, 25%, 50%, 95%). Spending is total medical expenditures. Used to demonstrate causal inference via RCT design and cluster-robust standard errors.

---

### AED_HEALTHACCESS.DTA

**Healthcare access in post-apartheid South Africa**

```python
df = pd.read_stata("https://raw.githubusercontent.com/quarcs-lab/data-open/master/AED/AED_HEALTHACCESS.DTA")
```

- **Observations:** 1,071
- **Variables (26):** `hhid93`, `pcode`, `idcommunity`, `year`, `hightreat`, `post`, `postXhigh`, `waz`, `whz`, `haz`, `fedu`, `medu`, `hhsizep`, `lntotminc`, `immuniz`, `nonclinic`, `male`, `age`, `age93_0`–`age93_3`, `age98_0`–`age98_3`
- **Source:** Tanaka (2014), *American Economic Journal: Economic Policy*
- **Used in:** Chapter 13
- **Description:** Difference-in-differences study of clinic construction in South Africa. Child health outcomes (weight-for-age, height-for-age z-scores) measured before and after treatment. `hightreat` indicates high-intensity treatment communities. Used to demonstrate the DiD estimator.

---

### AED_HEALTHCATEGORIES.DTA

**U.S. national health spending by category**

```python
df = pd.read_stata("https://raw.githubusercontent.com/quarcs-lab/data-open/master/AED/AED_HEALTHCATEGORIES.DTA")
```

- **Observations:** 13
- **Variables (4):** `category`, `expenditures`, `cat_short`, `exp_short`
- **Source:** Centers for Medicare & Medicaid Services (CMS), 1960-2021
- **Used in:** Chapter 2
- **Description:** Aggregate U.S. health expenditures broken down by category (hospital, physician, drugs, etc.). Used for bar charts and categorical data visualization.

---

### AED_CAPM.DTA

**Capital Asset Pricing Model — stock and market returns**

```python
df = pd.read_stata("https://raw.githubusercontent.com/quarcs-lab/data-open/master/AED/AED_CAPM.DTA")
```

- **Observations:** 354
- **Variables (13):** `date`, `rm`, `rf`, `rko`, `rtgt`, `rwmt`, `rm_rf`, `rko_rf`, `rtgt_rf`, `rwmt_rf`, `rm_rf_sq`, `smb`, `hml`
- **Source:** Ken French Data Library, Dartmouth Tuck School of Business
- **Used in:** Chapter 8
- **Description:** Monthly stock returns for three companies (Coca-Cola `rko`, Target `rtgt`, Walmart `rwmt`) alongside market returns and the risk-free rate. Excess returns (`_rf` suffix) are pre-computed. `smb` and `hml` are the Fama-French factors. Used to estimate stock betas and test the CAPM.

---

### AED_AUTOSMPG.DTA

**Automobile fuel efficiency**

```python
df = pd.read_stata("https://raw.githubusercontent.com/quarcs-lab/data-open/master/AED/AED_AUTOSMPG.DTA")
```

- **Observations:** 26,995
- **Variables (21):** `year`, `mfr`, `idmfr`, `nameplate`, `mpg`, `curbwt`, `hp`, `torque`, `fuel`, `d_truck`, `d_manual`, `time_d_manual`, `d_diesel`, `d_turbo`, `d_super`, `accel`, `base`, `lmpg`, `lcurbwt`, `lhp`, `ltorque`
- **Source:** Knittel (2011), *American Economic Review*
- **Used in:** Chapter 13
- **Description:** Panel of U.S. automobile models with fuel economy (MPG), weight, horsepower, and transmission type. Indicator variables for trucks, manual transmission, diesel, turbo, and supercharged engines. Log transformations pre-computed. Used for multiple regression case studies.

---

### AED_COBBDOUGLAS.DTA

**Cobb-Douglas production function**

```python
df = pd.read_stata("https://raw.githubusercontent.com/quarcs-lab/data-open/master/AED/AED_COBBDOUGLAS.DTA")
```

- **Observations:** 24
- **Variables (7):** `year`, `q`, `k`, `l`, `lnq`, `lnk`, `lnl`
- **Source:** Cobb & Douglas (1928), *American Economic Review*
- **Used in:** Chapter 13
- **Description:** The original 1928 data on U.S. manufacturing output (`q`), capital (`k`), and labor (`l`) with log transformations. Used to estimate returns to scale and test constant returns (alpha + beta = 1) via joint F-tests with HAC standard errors.

---

### AED_DEMOCRACY.DTA

**Democracy and economic development**

```python
df = pd.read_stata("https://raw.githubusercontent.com/quarcs-lab/data-open/master/AED/AED_DEMOCRACY.DTA")
```

- **Observations:** 131
- **Variables (16):** `code`, `country`, `democracy`, `growth`, `constraint`, `indcent`, `catholic`, `muslim`, `protestant`, `other`, `world`, `colony`, `indyear`, `logem4`, `lpd1500s`, `madid`
- **Source:** Acemoglu, Johnson, Robinson, Yared (2008)
- **Used in:** Chapter 16
- **Description:** Cross-country data on democracy scores, economic growth, colonial origins, religion shares, and institutional constraints. `logem4` is log settler mortality (instrumental variable). Used for model diagnostics, omitted variable bias, and influential observation analysis.

---

### AED_INSTITUTIONS.DTA

**Colonial institutions and economic development**

```python
df = pd.read_stata("https://raw.githubusercontent.com/quarcs-lab/data-open/master/AED/AED_INSTITUTIONS.DTA")
```

- **Observations:** 64
- **Variables (35):** `shortnam`, `logpgp95`, `avexpr`, `lat_abst`, `logem4`, `edes1975`, `avelf`, `temp1`–`temp5`, `humid1`–`humid4`, `steplow`, `deslow`, `stepmid`, `desmid`, `drystep`, `drywint`, `landlock`, `goldm`, `iron`, `silv`, `zinc`, `oilres`, `baseco`, `indtime`, `euro1900`, `democ1`, `cons1`, `democ00a`, `cons00a`
- **Source:** Acemoglu, Johnson, Robinson (2001), *American Economic Review*
- **Used in:** Chapter 13
- **Description:** The landmark AJR dataset linking colonial settler mortality (`logem4`) to current institutions (`avexpr` = expropriation risk) and GDP (`logpgp95`). Includes geographic, climate, and natural resource controls. Used for instrumental variables estimation (2SLS).

---

### AED_RETURNSTOSCHOOLING.DTA

**Returns to education — instrumental variables**

```python
df = pd.read_stata("https://raw.githubusercontent.com/quarcs-lab/data-open/master/AED/AED_RETURNSTOSCHOOLING.DTA")
```

- **Observations:** 3,010
- **Variables (101):** `id`, `black`, `imigrnt`, `hhead`, `mag_14`, `news_14`, `lib_14`, `num_sib`, `fgrade`, `mgrade`, `iq`, `bdate`, `grade76`, `grade66`, `age66`, `smsa66`, `region`, `smsa76`, `wage76`, `exp76`, `expsq76`, `age76`, and 79 additional controls and instruments
- **Source:** Kling (2001) citing Card (1995); National Longitudinal Survey of Young Men
- **Used in:** Chapter 13
- **Description:** Classic IV dataset for estimating the causal return to schooling. `wage76` is log hourly wage, `grade76` is years of schooling. College proximity indicators serve as instruments. Extensive controls for family background, ability (IQ), and geographic characteristics. The most variable-rich dataset in the course (101 variables).

---

### AED_NBA.DTA

**NBA team revenue and franchise values**

```python
df = pd.read_stata("https://raw.githubusercontent.com/quarcs-lab/data-open/master/AED/AED_NBA.DTA")
```

- **Observations:** 286
- **Variables (65):** `teamandyear`, `team`, `teamid`, `season`, `seasonsq`, `revenue`, `lnrevenue`, `value`, `lnvalue`, `wins`, `playoff`, `champ`, `allstars`, `relocated`, `newarenayr1`–`newarenayr4`, `cpi`, `realgdp`, `realgdppc`, `citypop`, `lncitypop`, `gdpmetro`, `lngdpmetro`, `season1`–`season10`, plus 20 team dummy variables
- **Source:** Forbes franchise valuations; Bang (2012)
- **Used in:** Chapter 17
- **Description:** Panel data of NBA teams across multiple seasons. Revenue and franchise value with team-level fixed effects dummies. Includes wins, playoff/championship indicators, city economic variables, and arena effects. The primary dataset for teaching panel data methods (pooled OLS, fixed effects, cluster-robust standard errors).

---

### AED_INCUMBENCY.DTA

**U.S. Senate election incumbency advantage (RDD)**

```python
df = pd.read_stata("https://raw.githubusercontent.com/quarcs-lab/data-open/master/AED/AED_INCUMBENCY.DTA")
```

- **Observations:** 1,390
- **Variables (9):** `state`, `year`, `vote`, `margin`, `class`, `termshouse`, `termssenate`, `population`, `win`
- **Source:** Calonico, Cattaneo, Farrell, Titiunik (2017)
- **Used in:** Chapter 13
- **Description:** U.S. Senate elections for regression discontinuity design. `margin` is the running variable (vote margin at the cutoff), `vote` is the outcome in the next election. Used to estimate the incumbency advantage at the margin = 0 threshold.

---

### AED_FISHING.DTA

**Recreational fishing site choices**

```python
df = pd.read_stata("https://raw.githubusercontent.com/quarcs-lab/data-open/master/AED/AED_FISHING.DTA")
```

- **Observations:** 1,182
- **Variables (17):** `mode`, `price`, `crate`, `dbeach`, `dpier`, `dprivate`, `dcharter`, `pbeach`, `ppier`, `pprivate`, `pcharter`, `qbeach`, `qpier`, `qprivate`, `qcharter`, `income`, `one`
- **Source:** Herriges & Kling (1999), *Review of Economics and Statistics*
- **Used in:** Chapter 2
- **Description:** Discrete choice data on fishing mode selection (beach, pier, private boat, charter). Prices, catch rates, and income for each individual. Used for categorical data analysis and random utility models.

---

### AED_GDPUNEMPLOY.DTA

**U.S. GDP growth and unemployment**

```python
df = pd.read_stata("https://raw.githubusercontent.com/quarcs-lab/data-open/master/AED/AED_GDPUNEMPLOY.DTA")
```

- **Observations:** 59
- **Variables (5):** `year`, `urate`, `rgdp`, `rgdpgrowth`, `uratechange`
- **Source:** FRED (Federal Reserve Economic Data)
- **Used in:** Chapter 8
- **Description:** Annual U.S. macroeconomic data for estimating Okun's Law (the relationship between GDP growth and changes in unemployment). Pre-computed first differences included.

---

### AED_PHILLIPS.DTA

**Phillips curve — inflation and unemployment**

```python
df = pd.read_stata("https://raw.githubusercontent.com/quarcs-lab/data-open/master/AED/AED_PHILLIPS.DTA")
```

- **Observations:** 66
- **Variables (14):** `year`, `urate`, `gdpdef`, `inflgdp`, `pastinflgdp`, `inflgdp1yr`, `cpi`, `inflcpi`, `pastinflcpi`, `infcpi1yr`, `infcpi10yr`, `mich`, `date`, `daten`
- **Source:** FRED + Federal Reserve Bank of Philadelphia
- **Used in:** Chapter 13
- **Description:** Annual U.S. inflation (GDP deflator and CPI) and unemployment for estimating the Phillips curve. Includes lagged inflation, 10-year inflation expectations, and Michigan survey expectations. Used to demonstrate omitted variable bias (pre vs. post-1970 structural break).

---

### AED_INTERESTRATES.DTA

**U.S. interest rates and yield curves**

```python
df = pd.read_stata("https://raw.githubusercontent.com/quarcs-lab/data-open/master/AED/AED_INTERESTRATES.DTA")
```

- **Observations:** 397
- **Variables (19):** `date`, `daten`, `gs3m`, `gs1`, `gs2`, `gs3`, `gs5`, `gs10`, `gs20`, `gs30`, `fii10`, `fedfunds`, `med1`, `aaa`, `baa`, `year`, `time`, `dgs1`, `dgs10`
- **Source:** FRED (Federal Reserve Economic Data)
- **Used in:** Chapter 17
- **Description:** Monthly U.S. Treasury yields at various maturities (3-month to 30-year), federal funds rate, and corporate bond rates (AAA, BAA). Pre-computed first differences for 1-year and 10-year rates. Used for time series analysis, unit roots, and spurious regression demonstrations.

---

### AED_REALGDPPC.DTA

**U.S. real GDP per capita (quarterly)**

```python
df = pd.read_stata("https://raw.githubusercontent.com/quarcs-lab/data-open/master/AED/AED_REALGDPPC.DTA")
```

- **Observations:** 245
- **Variables (12):** `gdpc1`, `gdp`, `gdpdef`, `date`, `daten`, `quarter`, `popthm`, `year`, `realgdp`, `gdppc`, `realgdppc`, `growth`
- **Source:** FRED (Federal Reserve Economic Data)
- **Used in:** Chapters 2, 4, 8, 12
- **Description:** Quarterly U.S. GDP data with nominal GDP, GDP deflator, population, and pre-computed real GDP per capita and growth rates. Used for time series visualization, hypothesis testing, and HAC standard errors.

---

### AED_SP500INDEX.DTA

**S&P 500 annual index**

```python
df = pd.read_stata("https://raw.githubusercontent.com/quarcs-lab/data-open/master/AED/AED_SP500INDEX.DTA")
```

- **Observations:** 93
- **Variables (3):** `year`, `sp500`, `lnsp500`
- **Source:** Yahoo Finance
- **Used in:** Chapter 9
- **Description:** Annual S&P 500 index values with log transformation. Used to demonstrate exponential growth, the Rule of 72, and log-linear time trends.

---

### AED_GASPRICE.DTA

**Gasoline prices in Yolo County, CA**

```python
df = pd.read_stata("https://raw.githubusercontent.com/quarcs-lab/data-open/master/AED/AED_GASPRICE.DTA")
```

- **Observations:** 32
- **Variables (2):** `city`, `price`
- **Source:** Author collection from web source, Yolo County gas stations
- **Used in:** Chapter 4
- **Description:** Cross-section of gasoline prices at 32 stations. Used to test whether the population mean price differs from a hypothesized value and to illustrate the distinction between statistical and practical significance.

---

### AED_MONTHLYHOMESALES.DTA

**U.S. monthly home sales**

```python
df = pd.read_stata("https://raw.githubusercontent.com/quarcs-lab/data-open/master/AED/AED_MONTHLYHOMESALES.DTA")
```

- **Observations:** 193
- **Variables (9):** `date`, `daten`, `year`, `month`, `exsales`, `exsales_sa`, `exsales_ma11`, `construct`, `construct_sa`
- **Source:** FRED (Federal Reserve Economic Data)
- **Used in:** Chapter 2
- **Description:** Monthly time series of existing home sales with seasonal adjustment and 11-month moving average. Also includes construction data. Used to demonstrate time series plots, seasonality, and moving average smoothing.

---

### AED_GENERATEDDATA.DTA

**Simulated regression data**

```python
df = pd.read_stata("https://raw.githubusercontent.com/quarcs-lab/data-open/master/AED/AED_GENERATEDDATA.DTA")
```

- **Observations:** 5
- **Variables (4):** `x`, `Eygivenx`, `u`, `y`
- **Source:** Author-generated
- **Used in:** Chapter 6
- **Description:** Five-observation dataset with known data-generating process. Shows the population regression function (`Eygivenx`), the error term (`u`), and the realized outcome (`y`). Used to illustrate the distinction between population and sample regression.

---

### AED_COINTOSSMEANS.DTA

**Coin toss simulation — sample means**

```python
df = pd.read_stata("https://raw.githubusercontent.com/quarcs-lab/data-open/master/AED/AED_COINTOSSMEANS.DTA")
```

- **Observations:** 400
- **Variables (3):** `xbar`, `stdev`, `numobs`
- **Source:** Author-generated simulation
- **Used in:** Chapter 3
- **Description:** 400 simulated sample means from coin toss experiments of varying sample sizes. Used to demonstrate the sampling distribution of the mean and the Central Limit Theorem.

---

### AED_CENSUSAGEMEANS.DTA

**1880 Census — age sample means**

```python
df = pd.read_stata("https://raw.githubusercontent.com/quarcs-lab/data-open/master/AED/AED_CENSUSAGEMEANS.DTA")
```

- **Observations:** 100
- **Variables (3):** `mean`, `stdev`, `numobs`
- **Source:** USA Full Count 1880 Census via IPUMS USA
- **Used in:** Chapter 3
- **Description:** 100 sample means of ages drawn from the 1880 Census. Demonstrates that sample means are approximately normal even when the population distribution (age) is right-skewed — the Central Limit Theorem in action.

---

### AED_CENSUSREGRESSIONS.DTA

**1880 Census — regression simulation**

```python
df = pd.read_stata("https://raw.githubusercontent.com/quarcs-lab/data-open/master/AED/AED_CENSUSREGRESSIONS.DTA")
```

- **Observations:** 400
- **Variables (5):** `slope`, `seslope`, `intercept`, `seintercept`, `numobs`
- **Source:** USA Full Count 1880 Census via IPUMS USA
- **Used in:** Chapter 3
- **Description:** 400 regression estimates from repeated samples of Census data. Used to demonstrate the sampling distribution of regression coefficients.

---

### AED_API99.DTA

**California Academic Performance Index (1999)**

```python
df = pd.read_stata("https://raw.githubusercontent.com/quarcs-lab/data-open/master/AED/AED_API99.DTA")
```

- **Observations:** 807
- **Variables (17):** `sch_code`, `api99`, `edparent`, `meals`, `englearn`, `yearround`, `credteach`, `emerteach`, `avg_ed_raw`, `pct_af_am`, `pct_am_ind`, `pct_asian`, `pct_fil`, `pct_hisp`, `pct_pac`, `pct_white`, `mobility`
- **Source:** California Department of Education API Data Files
- **Used in:** Chapter 13
- **Description:** School-level academic performance scores with demographics (% by race/ethnicity), % free meals (poverty proxy), % English learners, teacher credentials, and parent education. Used for multiple regression analysis of educational outcomes.

---

## Case Study Datasets

These datasets are used in the end-of-chapter case studies across multiple chapters.

### Mendez Convergence Clubs Dataset

```python
df = pd.read_csv("https://raw.githubusercontent.com/quarcs-lab/mendez2020-convergence-clubs-code-data/master/assets/dat.csv", index_col=["country", "year"]).sort_index()
```

- **Observations:** ~2,700 (108 countries, 1990-2014)
- **Variables:** `lp`, `rk`, `hc`, `rgdppc`, `tfp`, `region`
- **Source:** Mendez (2020), convergence clubs research data
- **Used in:** Chapters 1-7, 9-12, 14-17 (Case Study 1)
- **Description:** Country-year panel of labor productivity, physical capital, human capital, real GDP per capita, and total factor productivity across 108 countries. Used for cross-country convergence analysis.

### DS4Bolivia Dataset

```python
df = pd.read_csv("https://raw.githubusercontent.com/quarcs-lab/ds4bolivia/master/ds4bolivia_v20250523.csv")
```

- **Observations:** 339 municipalities
- **Variables:** `mun`, `dep`, `imds`, `ln_NTLpc2017`, `pop2017`, `index_sdg1`–`index_sdg17`, `sdg1_1_ubn`, `sdg7_1_ec`, `sdg4_6_lr`, plus 64 satellite embeddings (`A00`–`A63`)
- **Source:** DS4Bolivia project (satellite nighttime lights + SDG indices)
- **Used in:** Chapters 1-2, 4-5, 7, 10-12, 14-17 (Case Study 2)
- **Description:** Bolivian municipal-level data combining satellite nighttime lights per capita, sustainable development goal indices, and satellite image embeddings. Theme: "Can Satellites See Development?"

---

## Exercise Datasets

The `exercises/` subdirectory contains additional datasets for chapter exercises:

| Dataset | Description | Source |
|---------|-------------|--------|
| AED_ADVERTISING.DTA | Advertising and sales | James et al. (2014) *Intro to Statistical Learning* |
| AED_ANSCOMBE.DTA | Anscombe's quartet | Anscombe (1973) *American Statistician* |
| AED_AUSREGWEALTH.DTA | Australian regional wealth | Australian Bureau of Infrastructure |
| AED_COVIDFALL2020.DTA | COVID-19 statistics (Fall 2020) | New York Times compilation |
| AED_DIETOSS.DTA | Diet experiment simulation | Author-generated |
| AED_DOCTORVISITS.DTA | Doctor visit counts | Cameron & Trivedi (1986) |
| AED_ELECTRICITYPERCAP.DTA | Per-capita electricity use | Web-sourced |
| AED_ELECTRICITYPRICE.DTA | California electricity prices | Knittel (UC Davis) |
| AED_GDPAUSTRALIA.DTA | Australian GDP | Australian Bureau of Statistics |
| AED_HEALTH2018.DTA | OECD health data (2018) | OECD Health Statistics 2022 |
| AED_HOMEPRICEINDEX.DTA | Case-Shiller home price index | S&P Indices |
| AED_HOUSE2015.DTA | Davis house prices (2015) | Author collection |
| AED_KNEEREPLACE.DTA | Knee replacement costs | NY Health Department |
| AED_NAEP.DTA | National education achievement | NAEP |
| AED_ONETWOTHREE.DTA | Simple pedagogical data | Author-generated |
| AED_PHARVIS.DTA | Pharmaceutical visits | Cameron & Trivedi |
| AED_PRICEEARNINGSRATIO.DTA | Stock P/E ratios | Shiller (Yale) |
| AED_SALARYSAT.DTA | Youth employment | NLS Youth 1997 |
| AED_SPOTFORWARD.DTA | Energy market prices | Borenstein et al. (2008) |
| AED_STOCKINDEX.DTA | Russell 2000 index | Yahoo Finance |
| AED_SURVEYDATA.DTA | ACS survey extract | 2010 ACS via IPUMS |
| AED_TDIST4.DTA | t-distribution (df=4) | Author-generated |
| AED_TDIST25.DTA | t-distribution (df=25) | Author-generated |
| AED_USMANUFACTURING.DTA | Manufacturing statistics | U.S. Census Bureau |
| AED_API2006.csv | California API (2006) | CA Dept. of Education |
| AED_GALTON.csv | Galton height data | Harvard Dataverse |

---

## Data Source

All main text and exercise datasets are from Colin Cameron's textbook *Analysis of Economics Data: An Introduction to Econometrics* and are used with permission for educational purposes.

Original source: https://cameron.econ.ucdavis.edu/aed/

## Format Notes

- All `.DTA` files are Stata 13+ format, automatically converted to pandas DataFrames by `pd.read_stata()`
- All load commands above are self-contained — copy any single line into a notebook and it works
- No local downloads required when using Google Colab or any Python environment with internet access
- Duplicate files marked with `(1)`, `(2)` in the directory can be ignored
