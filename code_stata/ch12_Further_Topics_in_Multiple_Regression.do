* ch12_Further_Topics_in_Multiple_Regression.do - January 2026 For Stata
* Updated for online execution portability

********** OVERVIEW OF ch12_Further_Topics_in_Multiple_Regression.do **********

* STATA Program
* copyright C 2021 by A. Colin Cameron
* Used for "Analyis of Economics Data: An Introduction to Econometrics"
* by A. Colin Cameron (2021)

* To run you need file
*   AED_HOUSE.DTA
*   AED_REALGDPPC
* in your directory

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

************

* This STATA program does analysis for Chapter 12
*  12.1 INFERENCE WITH ROBUST STANDARD ERRORS
*  12.2 PREDICTION 
*  12.3 NONREPRESENTATIVE SAMPLES
*  12.4 BEST ESTIMATION
*  12.5 BEST CONFIDENCE INTERVALS 
*  12.6 BEST TESTS
*  12.7 DATA SCIENCE AAND BIG DATA: AN OVERVIEW
*  12.8 BAYESIAN METHODS: AN OVERVIEW
*  12.9 A BRIEF HISTORY OF STATISTICS, REGRESSION AND ECONOMETRICS
 
********** DATA DESCRIPTION

* (1) House sale price for 29 houses in Central Davis in 1999
*     29 observations on 9 variables
* (2) U.S. quarterly GDP and related data from 1959Q1 to 2020Q1
*     245 Observations on 11 variables

****  12.1 INFERENCE WITH ROBUST STANDARD ERRORS

* Download and load data from GitHub
clear
copy "${github_data_url}AED_HOUSE.DTA" "temp_data.dta", replace
use "temp_data.dta", clear
erase "temp_data.dta"
describe
summarize

* Table 12.2
regress price size bedrooms bathroom lotsize age monthsold, vce(robust)

* HAC standard errors for the mean
* Download and load data from GitHub
clear
copy "${github_data_url}AED_REALGDPPC.DTA" "temp_data.dta", replace
use "temp_data.dta", clear
erase "temp_data.dta"
describe growth
summarize growth
mean growth
regress growth
* lag 1 autocorrelation manually
generate growthlag1 = growth[_n-1]
correlate growth growthlag1
* Autocorrelations using Stata commands
pwcorr growth l.growth l2.growth l3.growth l4.growth l5.growth
corrgram growth, lag(10)
* newey is the same as regress except HAC standard errors
newey growth, lag(0)
newey growth, lag(5)

****  12.2 PREDICTION

*** Predict conditional mean for house size = 2000 and get confidence interval
* This uses Stata command lincom
* Download and load data from GitHub
clear
copy "${github_data_url}AED_HOUSE.DTA" "temp_data.dta", replace
use "temp_data.dta", clear
erase "temp_data.dta"

*** Figure 12.1 Simple version
* First panel - Confidence Interval for Conditional Mean
twoway (lfitci price size, stdp) (scatter price size)
* Second panel - Confidence Interval for Actual Value
twoway (lfitci price size, stdf) (scatter price size)

*** Predict conditional mean for house size = 2000
regress price size
display _b[_cons] + _b[size]*2000
* Stata command lincom gives the standard error
lincom _cons + size*2000

*** Get confidence intervals for conditional mean and actual value
*   Do manually as was done in book
quietly summarize size
scalar xbar = r(mean)
scalar n = r(N)
scalar sumxminusxbarsq = (r(N)-1)*r(Var)
quietly regress price size
scalar b1 = _b[_cons]
scalar b2 = _b[size]
scalar s_e = e(rmse)
scalar y_cm = b1 + 2000*b2
scalar y_f = b1 + 2000*b2
scalar s_y_cm = s_e*sqrt(1/n+(2000-xbar)^2/sumxminusxbarsq)
scalar s_y_f = s_e*sqrt(1+1/n+(2000-xbar)^2/sumxminusxbarsq)
scalar tcrit = invttail(n-2,.025)

* Conditional mean at size = 2000
display "yhat = " y_cm _n "t critical value = " tcrit _n
display "Se for cond mean = " s_y_cm _n "CI width = " tcrit*s_y_cm _n
display "95% confidence interval: (" y_cm-tcrit*s_y_cm ", " y_cm+tcrit*s_y_cm ")"

* Actual value at size = 2000
display "yhat = " y_f _n "t critical value = " tcrit _n
display "Se for actual value = " s_y_f _n  "CI width = " tcrit*s_y_f
display "95% confidence interval: (" y_f-tcrit*s_y_f ", " y_f+tcrit*s_y_f ")"

*** Predict for multiple regression
quietly regress price size bedrooms bathroom lotsize age monthsold
scalar s_e = e(rmse)
scalar n = e(N)
scalar k = e(rank)
lincom _cons + size*2000 + bedrooms*4 + bathroom*2 + lotsize*2 + age*40 + monthsold*6
display "Se for conditional mean = " r(se)
scalar y_f = r(estimate)
scalar s_y_cm = r(se)
scalar s_y_f = sqrt(s_e^2 + s_y_cm^2)
scalar tcrit = invttail(n-k,.025)
display "y_f = " y_f _n "t critical value = " tcrit _n            ///
  "Se for actual value = " s_y_f _n  "CI width = " tcrit*s_y_f _n ///
  "95% confidence interval: (" y_f-tcrit*s_y_f ", " y_f+tcrit*s_y_f ")"

* Repeat for het robust se's
* Just confidence interval for fitted mean
quietly regress price size bedrooms bathroom lotsize age monthsold, vce(robust)
lincom _cons + size*2000 + bedrooms*4 + bathroom*2 + lotsize*2 + age*40 + monthsold*6
display "heteroskedastic-robust se for conditional mean = " r(se)
display "heteroskedastic-robust Se for actual value = " sqrt(s_e^2 + r(se)^2)

**** 12.3 NONREPRESENTATIVE SAMPLES

* No computation

**** 12.4 BEST ESTIMATION

* No computation

**** 12.5 BEST CONFIDENCE INTERVALS 

* No computation

**** 12.6 BEST TESTS

* No computation

**** 12.7 DATA SCIENCE AAND BIG DATA: AN OVERVIEW

* No computation

****  12.8 BAYESIAN METHODS: AN OVERVIEW

* Prior is uninformative here
generate pricenew = price/1000
bayes, rseed(10101): regress pricenew size

* Prior turns out to be informative here
bayes, rseed(10101): regress price size

********** CLOSE OUTPUT

display ""
display "Chapter 12 analysis complete."
display "Figures saved to: images/"
display "Tables saved to: tables/"
