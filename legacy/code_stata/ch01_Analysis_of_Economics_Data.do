* ch01_Analysis_of_Economics_Data.do - January 2026 For Stata
* Updated for online execution portability

********** OVERVIEW OF ch01_Analysis_of_Economics_Data.do **********

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

* This STATA program does analysis for Chapter 1
*  1.3 REGRESSION ANALYSIS

********** DATA DESCRIPTION

* House sale price for 29 houses in Central Davis in 1999
*     29 observations on 9 variables 

****  1.3 REGRESSION ANALYSIS

* Download and load data from GitHub
clear
copy "${github_data_url}AED_HOUSE.DTA" "temp_data.dta", replace
use "temp_data.dta", clear
erase "temp_data.dta"
summarize

* Figure 1.1
label variable price "House price (in dollars)"
label variable size "House size (in square feet)"
graph twoway (scatter price size) (lfit price size, lstyle(p1))
graph export "images/ch01_fig1.png", replace


********** CLOSE OUTPUT

display ""
display "Chapter 01 analysis complete."
display "Figures saved to: images/"
display "Tables saved to: tables/"


