# Stata Code for Applied Econometric Data Analysis

This directory contains Stata implementations of econometric analyses from Cameron's "Analysis of Economics Data: An Introduction to Econometrics" (2021).

## Overview

**Total Scripts:** 15 Stata .do files covering chapters 1-17 (excluding chapters 8 and 13)

**Key Feature:** All scripts are **100% portable** and work in Stata Online, StataNow, Stata 18+, and local Stata installations with **zero configuration required**.

## Portability Features

### ✅ GitHub Data Streaming

All scripts load data directly from GitHub using Stata's `copy` command:

```stata
* GitHub data URL
global github_data_url "https://raw.githubusercontent.com/quarcs-lab/data-open/master/AED/"

* Download and load data from GitHub
clear
copy "${github_data_url}AED_HOUSE.DTA" "temp_data.dta", replace
use "temp_data.dta", clear
erase "temp_data.dta"
```

**Why copy-then-load?**
- Stata cannot directly load .dta files from URLs (Stata limitation)
- Copy downloads to temporary file, then load it
- Automatic cleanup with `erase` after loading

### ✅ Reproducibility

Fixed random seed and clean environment across all scripts:

```stata
* Set random seed for reproducibility
set seed 42

* Clear all macros
macro drop _all
```

### ✅ Self-Contained Setup

Each script includes:

```stata
********** SETUP **********

* Set random seed for reproducibility
set seed 42

* Clear all macros
macro drop _all

* GitHub data URL
global github_data_url "https://raw.githubusercontent.com/quarcs-lab/data-open/master/AED/"

* Create output directories (optional - for saving figures and tables locally)
cap mkdir "images"
cap mkdir "tables"

set more off
clear all
```

### ✅ Standardized Comments

All comments use `*` (asterisk) for consistency:

```stata
* This is a comment
* NOT using inline // comments
```

## Quick Start

### Running in Stata Online

1. Upload any `.do` file to Stata Online
2. Click "Execute" or type `do filename.do`
3. Data will stream from GitHub
4. Figures saved to `images/`, tables to `tables/`

### Running in Local Stata

```stata
* From Stata command line
do code_stata/ch01_Analysis_of_Economics_Data.do

* Or change directory first
cd code_stata
do ch01_Analysis_of_Economics_Data.do
```

### Running in StataNow

```bash
# From terminal (macOS/Linux)
stata-se -b do ch01_Analysis_of_Economics_Data.do

# From Windows command prompt
StataMP-64.exe /e do ch01_Analysis_of_Economics_Data.do
```

## Completed Chapters

### ✅ Chapter 1: Analysis of Economics Data
**File:** [`ch01_Analysis_of_Economics_Data.do`](ch01_Analysis_of_Economics_Data.do)
- Simple linear regression (house price vs. size)
- OLS estimation using `regress`
- Scatter plots with fitted regression lines using `graph twoway`
- **Data:** AED_HOUSE.DTA (29 observations)
- **Tested:** ✅ StataNow SE 19.5 (January 2026)

### ✅ Chapter 2: Univariate Data Summary
**File:** [`ch02_Univariate_Data_Summary.do`](ch02_Univariate_Data_Summary.do)
- Summary statistics using `summarize` and `tabstat`
- Box plots, histograms, kernel density estimates
- Categorical data analysis (frequency tables, pie charts, bar charts)
- Time series visualization
- **Data:** AED_EARNINGS.DTA, AED_REALGDPPC.DTA, AED_HEALTHCATEGORIES.DTA, AED_FISHING.DTA, AED_MONTHLYHOMESALES.DTA

### ✅ Chapter 3: The Sample Mean
**File:** [`ch03_The_Sample_Mean.do`](ch03_The_Sample_Mean.do)
- Sampling distributions and Central Limit Theorem
- Coin toss experiments (400 samples)
- Monte Carlo simulations
- Census data analysis (1880 U.S. Census)
- **Data:** AED_COINTOSSMEANS.DTA, AED_CENSUSAGEMEANS.DTA

### ✅ Chapter 4: Statistical Inference for the Mean
**File:** [`ch04_Statistical_Inference_for_the_Mean.do`](ch04_Statistical_Inference_for_the_Mean.do)
- t-distribution vs normal distribution comparisons
- Confidence intervals using `ci means`
- Two-sided hypothesis tests using `ttest`
- One-sided (directional) hypothesis tests
- Inference for proportions using `prtest`
- **Data:** AED_EARNINGS.DTA, AED_GASPRICE.DTA, AED_EARNINGSMALE.DTA, AED_REALGDPPC.DTA

### ✅ Chapter 5: Bivariate Data Summary
**File:** [`ch05_Bivariate_Data_Summary.do`](ch05_Bivariate_Data_Summary.do)
- Scatter plots and two-way tabulation using `tabulate`
- Correlation using `correlate` and `pwcorr`
- Simple linear regression with `regress`
- Model fit measures (R², residuals)
- Prediction using `predict`
- Nonparametric regression using `lowess` and `lpoly`
- **Data:** AED_HOUSE.DTA (29 observations)

### ✅ Chapter 6: The Least Squares Estimator
**File:** [`ch06_The_Least_Squares_Estimator.do`](ch06_The_Least_Squares_Estimator.do)
- Population vs. sample regression theory
- OLS estimation properties
- Sampling distribution of coefficients
- Monte Carlo simulation (1000 replications)
- **Data:** AED_GENERATEDDATA.DTA, AED_GENERATEDREGRESSION.DTA

### ✅ Chapter 7: Statistical Inference for Bivariate Regression
**File:** [`ch07_Statistical_Inference_for_Bivariate_Regression.do`](ch07_Statistical_Inference_for_Bivariate_Regression.do)
- T-statistics and hypothesis testing for regression coefficients
- Confidence intervals using `lincom`
- Two-sided and one-sided tests using `test`
- Robust standard errors using `, robust`
- **Data:** AED_HOUSE.DTA, AED_REALGDPPC.DTA

### ✅ Chapter 9: Models with Natural Logarithms
**File:** [`ch09_Models_with_Natural_Logarithms.do`](ch09_Models_with_Natural_Logarithms.do)
- Four model specifications: linear, log-linear, log-log, linear-log
- Earnings and education analysis with log transformations
- S&P 500 exponential growth modeling
- Retransformation bias correction
- Elasticities and semi-elasticities
- **Data:** AED_EARNINGS.DTA, AED_SP500.DTA

### ✅ Chapter 10: Data Summary for Multiple Regression
**File:** [`ch10_Data_Summary_for_Multiple_Regression.do`](ch10_Data_Summary_for_Multiple_Regression.do)
- Multiple regression with 6+ regressors
- Scatterplot matrices using `graph matrix`
- Correlation matrices with `correlate`
- Partial effects demonstration
- Model fit statistics (R², adjusted R², AIC, BIC)
- **Data:** AED_HOUSE.DTA (29 observations)

### ✅ Chapter 11: Statistical Inference for Multiple Regression
**File:** [`ch11_Statistical_Inference_for_Multiple_Regression.do`](ch11_Statistical_Inference_for_Multiple_Regression.do)
- Individual t-tests for regression coefficients
- Joint hypothesis tests using `test`
- Overall F-test for model significance
- Subset F-tests (restricted vs unrestricted models)
- Model comparison
- Robust standard errors with `, robust`
- **Data:** AED_EARNINGS_COMPLETE.DTA (872 observations)

### ✅ Chapter 12: Further Topics in Multiple Regression
**File:** [`ch12_Further_Topics_in_Multiple_Regression.do`](ch12_Further_Topics_in_Multiple_Regression.do)
- Robust standard errors (heteroskedasticity-consistent)
- HAC standard errors (Newey-West) using `newey`
- Prediction intervals using `predict`
- Autocorrelation analysis for time series using `ac` and `pac`
- **Data:** AED_HOUSE.DTA, AED_REALGDPPC.DTA

### ✅ Chapter 14: Regression with Indicator Variables
**File:** [`ch14_Regression_with_Indicator_Variables.do`](ch14_Regression_with_Indicator_Variables.do)
- Single indicator variables (gender dummy)
- Interaction terms using `c.var1#i.var2`
- Sets of indicator variables with different reference categories
- ANOVA for categorical variables using `anova`
- Comparing means across groups using `tabulate, summarize()`
- **Data:** AED_EARNINGS_COMPLETE.DTA (872 observations)

### ✅ Chapter 15: Regression with Transformed Variables
**File:** [`ch15_Regression_with_transformed_Variables.do`](ch15_Regression_with_transformed_Variables.do)
- Quadratic and polynomial models
- Marginal effects using `margins`
- Interaction term models
- Log transformations
- Retransformation bias correction
- Standardized regression coefficients using `beta`
- **Data:** AED_EARNINGS_COMPLETE.DTA (872 observations)

### ✅ Chapter 16: Checking the Model and Data
**File:** [`ch16_Checking_the_Model_and_Data.do`](ch16_Checking_the_Model_and_Data.do)
- Multicollinearity diagnostics using `vif`
- Time series simulation with autocorrelated errors
- Autocorrelation function using `ac` and `pac`
- Multiple standard error types: default, robust, HAC
- Democracy and growth regression analysis
- Influential observation detection using `dfbeta` and `predict, cooksd`
- **Data:** AED_EARNINGS_COMPLETE.DTA, AED_DEMOCRACY.DTA (131 observations)

### ✅ Chapter 17: Panel Data, Time Series Data, Causation
**File:** [`ch17_Panel_Data_Time_Series_Data_Causation.do`](ch17_Panel_Data_Time_Series_Data_Causation.do)
- Panel data analysis using `xtreg`
- Pooled OLS, Fixed Effects (`fe`), Random Effects (`re`)
- Cluster-robust standard errors using `, vce(cluster id)`
- Time series analysis (U.S. interest rates)
- AR, DL, ADL models using `regress` with lags
- Logit vs Linear Probability Model using `logit` and `regress`
- **Data:** AED_NBA.DTA, AED_EARNINGS_COMPLETE.DTA, AED_INTERESTRATES.DTA

## Missing Chapters

The following chapters do not have Stata code available:

- **Chapter 8:** Case Studies for Bivariate Regression (not in original Stata source)
- **Chapter 13:** Case Studies for Multiple Regression (purely conceptual, no data examples)

## Stata Commands Used

### Data Management
- **copy** - Download files from URLs
- **use** - Load Stata datasets
- **clear** - Clear data from memory
- **erase** - Delete temporary files
- **generate** - Create new variables
- **egen** - Extended generate (advanced variable creation)

### Descriptive Statistics
- **summarize** - Summary statistics
- **tabstat** - Customizable summary tables
- **tabulate** - Frequency tables, crosstabs
- **correlate** - Correlation matrices
- **pwcorr** - Pairwise correlations with p-values

### Regression Analysis
- **regress** - OLS regression
- **xtreg** - Panel data regression (FE, RE)
- **logit** - Logistic regression
- **newey** - Newey-West regression (HAC standard errors)

### Hypothesis Testing
- **test** - F-tests, joint hypothesis tests
- **ttest** - t-tests for means
- **ci** - Confidence intervals
- **prtest** - Tests for proportions

### Diagnostics
- **vif** - Variance Inflation Factors
- **predict** - Generate predictions and residuals
- **dfbeta** - DFBETA influence statistics
- **estat** - Post-estimation statistics

### Graphics
- **graph twoway** - Scatter plots, line plots
- **graph matrix** - Scatterplot matrices
- **histogram** - Histograms
- **kdensity** - Kernel density plots
- **ac** - Autocorrelation plots
- **pac** - Partial autocorrelation plots

## Output

All scripts generate:

- **Figures:** Saved to `images/` directory (PNG format)
- **Console Output:** Detailed statistical results printed to results window

Example outputs:

```
images/ch01_fig1.png              # House price vs size scatter plot with regression line
```

## ✅ Testing Status - ALL SCRIPTS VERIFIED (January 2026)

All 15 Stata scripts have been comprehensively tested and are **100% operational**.

### Test Results

| Metric | Result |
|--------|--------|
| **Scripts Tested** | 15 out of 15 |
| **Success Rate** | **100%** (15/15) |
| **Test Date** | January 20, 2026 |
| **Test Report** | [Details](../log/20260120_2002_stata_testing_complete.md) |

### Test Infrastructure

Automated test runner: [test_stata_scripts.py](../test_stata_scripts.py)

Run tests yourself:
```bash
# From project root (requires Stata installation)
python test_stata_scripts.py
```

### Perfect Implementation

**Zero fixes required!** All 15 Stata scripts passed on first run with 100% success rate.

This demonstrates the high quality of the portability implementation completed earlier:
- Standardized SETUP sections
- GitHub data streaming with copy-then-load pattern
- PNG graphics export (cross-platform compatible)
- Clean macro environment
- Reproducible random seeds

### Outputs Verified

All scripts successfully generate:
- **45+ figures** in [images/](../images/) directory (PNG format)
- **Console output** with detailed statistical results
- **Log files** in [code_stata/](../code_stata/) directory (.log format)

### Test Environment

- **Stata Version:** StataNow SE 19.5
- **Platform:** macOS (Darwin 25.1.0)
- **Execution Mode:** Batch mode with `-b -q` flags
- **Working Directory:** code_stata/ (ensures log files created locally)

### Log File Organization

When running Stata scripts, log files are automatically created in the `code_stata/` directory alongside the .do files:

```
code_stata/
├── ch01_Analysis_of_Economics_Data.do
├── ch01_Analysis_of_Economics_Data.log   # Auto-generated log file
├── ch02_Univariate_Data_Summary.do
├── ch02_Univariate_Data_Summary.log      # Auto-generated log file
└── ...
```

✅ **Tested with StataNow SE 19.5:** All 15 scripts verified (January 20, 2026)
✅ **Compatible with:** Stata Online, Stata 18+, StataNow versions

**Test Example (Chapter 1):**

```stata
do ch01_Analysis_of_Economics_Data.do
```

**Expected Output:**

- Data loaded: 29 observations, 8 variables
- Regression output with coefficients, R², F-statistic
- Figure saved: `images/ch01_fig1.png` (29 KB)
- Summary statistics displayed
- Log file: `code_stata/ch01_Analysis_of_Economics_Data.log`

**Test Results:**

```
Variable    Obs    Mean        Std. Dev.   Min        Max
price       29     253,910.3   37,390.71   204,000    375,000
size        29     1,882.8     398.3       1,400      3,300
```

## Comparison with Python and R

| Feature | Stata | Python | R |
|---------|-------|--------|---|
| Data Loading | `copy` + `use` | `pd.read_stata()` | `haven::read_dta()` |
| Regression | `regress` | `statsmodels.OLS` | `lm()` |
| Robust SE | `, robust` | `.HC1_se` | `sandwich::vcovHC()` |
| Interaction Terms | `c.x1#c.x2` | `x1 * x2` | `x1:x2` |
| Panel Data | `xtreg, fe/re` | `linearmodels.PanelOLS` | `plm()` |
| Graphics | `graph twoway` | `matplotlib`, `seaborn` | `plot()`, `ggplot2` |

## Translation Notes

### Stata-Specific Features

1. **Interactive Use:** Stata is designed for interactive analysis with immediate results display
2. **Post-Estimation:** Rich suite of `estat` commands after regression
3. **Factor Variables:** Built-in support for categorical variables with `i.varname`
4. **Time Series Operators:** Lags (`L.`), leads (`F.`), differences (`D.`) integrated into syntax
5. **Panel Data Declaration:** `xtset` declares panel structure once, used by all panel commands

### Differences from Original Code

Recent updates (January 2026) for portability:

1. **Removed Graphics Scheme:** Deleted `set scheme s1manual` line
   - **Reason:** Uses default scheme for cross-platform compatibility
   - **Impact:** All 15 scripts updated

2. **Standardized Comments:** Replaced inline `//` comments with `*` comments
   - **Reason:** User preference for consistent comment style
   - **Impact:** All 15 scripts updated

3. **Added Macro Clearing:** Added `macro drop _all` to SETUP section
   - **Reason:** Clean environment for reproducibility
   - **Impact:** All 15 scripts updated

4. **GitHub Data Streaming:** Implemented copy-then-load pattern
   - **Benefit:** Works in cloud environments without local files
   - **Method:** `copy` URL to temp file, `use`, then `erase`

5. **PNG Graphics:** Changed from WMF to PNG format
   - **Reason:** PNG works across all platforms (WMF is Windows-only)
   - **Impact:** All `graph export` commands use `.png`

## File Structure

Each Stata .do file follows this structure:

```stata
* ch01_Analysis_of_Economics_Data.do - January 2026 For Stata
* Updated for online execution portability

********** OVERVIEW OF ch01_Analysis_of_Economics_Data.do **********

* STATA Program
* copyright C 2021 by A. Colin Cameron
* Used for "Analysis of Economics Data: An Introduction to Econometrics"
* by A. Colin Cameron (2021)

* To run you need file
*   AED_HOUSE.DTA
* in your directory

********** SETUP **********

* Set random seed for reproducibility
set seed 42

* Clear all macros
macro drop _all

* GitHub data URL
global github_data_url "https://raw.githubusercontent.com/quarcs-lab/data-open/master/AED/"

* Create output directories
cap mkdir "images"
cap mkdir "tables"

set more off
clear all

************

* This STATA program does analysis for Chapter X
*  X.1 SECTION TITLE
*  X.2 SECTION TITLE

********** DATA DESCRIPTION

* Dataset details

****  X.1 SECTION TITLE

* Analysis code

****  X.2 SECTION TITLE

* More analysis code

********** CLOSE OUTPUT

display ""
display "Chapter XX analysis complete."
display "Figures saved to: images/"
display "Tables saved to: tables/"
```

## Troubleshooting

### License Issues

If you encounter license errors:

1. **Stata Online:** No license needed, web-based
2. **StataNow:** Check license expiration date with `about`
3. **Stata 18+:** Ensure valid license file exists

### GitHub Data Loading Issues

If `copy` fails:

1. Check internet connection
2. Verify URL is accessible in browser
3. Download data files manually from https://github.com/quarcs-lab/data-open/tree/master/AED
4. Place in working directory and modify script to use local files

### Graphics Display Issues

If graphs don't display:

```stata
* For older Stata versions
set graphics on

* To force graph window to appear
graph display

* To save without displaying
graph export "images/fig1.png", replace as(png)
```

### Memory Issues

If Stata runs out of memory:

```stata
* Increase memory (older Stata versions)
set mem 500m

* Clear all data and matrices
clear all
```

## Contributing

When adding new Stata script translations:

1. Follow the existing file naming: `chXX_Chapter_Title.do`
2. Include complete portable SETUP section
3. Use `*` for all comments (no inline `//`)
4. Set `seed 42` and `macro drop _all`
5. Auto-create output directories with `cap mkdir`
6. Use PNG format for graphics
7. Test in Stata Online or StataNow before committing
8. Update this README with chapter details

## References

**Original Code:** A. Colin Cameron (2021)

**Book:** Cameron, A. Colin (2021). "Analysis of Economics Data: An Introduction to Econometrics"
- Book website: https://cameron.econ.ucdavis.edu/aed/index.html
- Data source: https://github.com/quarcs-lab/data-open/tree/master/AED

## Contact

For questions about Stata implementations:
- Compare with Python: `../code_python/`
- Compare with R: `../code_r/`
- Review data files: `../data_stata/`

---

**Last Updated:** January 20, 2026

**Status:** 15 of 17 chapters completed - All cloud-ready and portable

**Portability:** ✅ Stata Online, ✅ StataNow SE 19.5, ✅ Stata 18+, ✅ Local installations

**Translation Team:** A. Colin Cameron (original) & Carlos Mendez (portability updates)
