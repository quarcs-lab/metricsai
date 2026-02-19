* ch07_Statistical_Inference_for_Bivariate_Regression.do - January 2026 For Stata
* Updated for online execution portability

********** OVERVIEW OF ch07_Statistical_Inference_for_Bivariate_Regression.do **********

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
clear all

************

* This STATA does analysis for Chapter 7
*   7.1 EXAMPLE: HOUSE PRICE AND SIZE
*   7.2 THE T STATISTIC
*   7.3 CONFIDENCE INTERVALS
*   7.4 TESTS OF STATISTICAL SIGNIFICANCE
*   7.5 TWO-SIDED HYPOTHESIS TESTS
*   7.6 ONE-SIDED DIRECTIONAL HYPOTHESIS TESTS
*   7.7 ROBUST STANDARD ERRORS

********** DATA DESCRIPTION

* House sale price for 29 houses in Central Davis in 1999
*     29 observations on 9 variables 

**** 7.1 EXAMPLE: HOUSE PRICE AND SIZE

* Download and load data from GitHub
clear
copy "${github_data_url}AED_HOUSE.DTA" "temp_data.dta", replace
use "temp_data.dta", clear
erase "temp_data.dta"
summarize

* Table 7.1
regress price size

**** 7.3 CONFIDENCE INTERVALS

* Example with artifical data
clear
input x y 
 1 1
 2 2
 3 2
 4 2
 5 3
end
regress y x

***** 7.4 TESTS OF STATISTICAL SIGNIFICNACE

* Download and load data from GitHub
clear
copy "${github_data_url}AED_HOUSE.DTA" "temp_data.dta", replace
use "temp_data.dta", clear
erase "temp_data.dta"
regress price size

**** 7.5 TWO-SIDED HYPOTHESIS TESTS

regress price size
test size = 90

* Compute manually
scalar t = (_b[size] - 90)/_se[size]
scalar pvalue = 2*ttail(27,abs(t))
scalar critvalue = invttail(27,.025)
display "t = " t "  p = " pvalue "  critical value = " critvalue

* Figure 7.1 - generated elsewhere is similar to Figure 4.3 

**** 7.6 ONE-SIDED HYPOTHESIS TESTS

* Download and load data from GitHub
clear
copy "${github_data_url}AED_HOUSE.DTA" "temp_data.dta", replace
use "temp_data.dta", clear
erase "temp_data.dta"
regress price size
ttest size = 90
* Halve the two-sided p-value provided
* t>0 for an upper one-tailed alternative
* t<0 for a lower one-tailed alternative

****  7.7 ROBUST STANDARD ERRORS

* Heteroskedastic robust
regress price size, vce(robust)

********** CLOSE OUTPUT

display ""
display "Chapter 07 analysis complete."
display "Figures saved to: images/"
display "Tables saved to: tables/"
