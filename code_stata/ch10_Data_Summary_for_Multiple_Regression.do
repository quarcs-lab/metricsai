* ch10_Data_Summary_for_Multiple_Regression.do - January 2026 For Stata
* Updated for online execution portability

********** OVERVIEW OF ch10_Data_Summary_for_Multiple_Regression.do **********

* STATA Program
* copyright C 2021 by A. Colin Cameron
* Used for "Analyis of Economics Data: An Introduction to Econometrics"
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

* Create output directories (optional - for saving figures and tables locally)
cap mkdir "images"
cap mkdir "tables"

set more off
clear all

************

* This STATA does analysis for Chapter 10
*  10.1 EXAMPLE: HOUSE PRICE AND CHARACTERISTICS
*  10.2 TWO-WAY SCATTERPLOTS
*  10.3 CORRELATION
*  10.4 REGRESSION LINE
*  10.5 ESTIMATED PARTIAL EFFECTS 
*  10.6 MODEL FIT
*  10.7 COMPUTER OUTPUT FOLLOWING MULTIPLE REGRESSION
*  10.8 INESTIMABLE MODELS

********** DATA DESCRIPTION

* House sale price for 29 houses in Central Davis in 1999
*     29 observations on 9 variables 

****  10.1 EXAMPLE: HOUSE PRICE AND CHARACTERISTICS

* Download and load data from GitHub
copy "${github_data_url}AED_HOUSE.DTA" "temp_data.dta", replace
use "temp_data.dta", clear
erase "temp_data.dta"
describe

* Table 10.1
summarize price size bedrooms bathroom lotsize age monthsold

* Table 10.2
list price size bedrooms bathroom lotsize age monthsold, clean

* Regression with and without control
regress price bedrooms
regress price bedrooms size

****   10.2 TWO-WAY SCATTERPLOTS

* Figure 10.1
graph matrix price size bedrooms age
graph export "images/ch10_fig1.png", replace

****  10.3 CORRELATION

* Table 10.3
correlate price size bedrooms bathroom lotsize age monthsold
pwcorr price size bedrooms bathroom lotsize age monthsold, sig star(.05)
set textsize 150

****  10.4 REGRESSION LINE

* Multivariate regression
regress price size bedrooms bathroom lotsize age monthsold

* Demonstrate that can get from bivariate regression on a residual
regress size bedrooms bathroom lotsize age monthsold
predict res_size, resid
regress price res_size

****  10.5 ESTIMATED PARTIAL EFFECTS 

*****  10.6 MODEL FIT

regress price size bedrooms bathroom lotsize age monthsold

* R-squared is squared correlation between yhat and y
regress price size bedrooms bathroom lotsize age monthsold
display e(r2)
predict pprice
correlate price pprice
display r(rho)^2

* Compute adjusted R-squared
display "Adjusted R-squared = " e(r2) - (e(df_m)/e(df_r))*(1-e(r2))

* Information criteria
estat ic

* Information criteria manually
display "AIC = " e(N)*ln(e(rss)/e(N)) + e(N)*(1+ln(2*_pi)) + 2*e(rank)
display "BIC = " e(N)*ln(e(rss)/e(N)) + e(N)*(1+ln(2*_pi)) + e(rank)*ln(e(N))

*****  10.7 COMPUTER OUTPUT FOLLOWING REGRESSION

* Table 10.4
regress price size bedrooms
estimates store OUTPUT
estimates table OUTPUT, b(%11.2f) se(%11.2f) stats(r2 N)
estimates table OUTPUT, b(%11.2f) t(%11.2f) stats(r2 N)
estimates table OUTPUT, b(%11.2f) p(%11.3f) stats(r2 N)
estimates table OUTPUT, b(%11.2f) star(.10 .05 .01) stats(r2 N)

*****  10.8 INESTIMABLE MODELS

********** CLOSE OUTPUT

display ""
display "Chapter 10 analysis complete."
display "Figures saved to: images/"
display "Tables saved to: tables/"
