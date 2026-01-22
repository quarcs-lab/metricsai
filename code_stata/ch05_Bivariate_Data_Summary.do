* ch05_Bivariate_Data_Summary.do - January 2026 For Stata
* Updated for online execution portability

********** OVERVIEW OF ch05_Bivariate_Data_Summary.do **********

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

* This STATA program does analysis for Chapter 5
*  5.1 EXAMPLE: HOUSE PRICE AND SIZE
*  5.2 TWO-WAY TABULATION
*  5.3 TWOWAY SCATTER PLOT
*  5.4 CORRELATION
*  5.5 REGRESSION LINE
*  5.6 MEASURES OF MODEL FIT
*  5.7 COMPUTER OUTPUT FOLLOWING REGRESSION
*  5.8 PREDICTION AND OUTLYING OBSERVATIONS
*  5.9 REGRESSION AND CORRELATION
*  5.10 CAUSATION
*  5.11 COMPUTATIONS FOR CORRELATION AND REGRESSION 
*  5.12 NONPARAMETRIC REGRESSION

********** DATA DESCRIPTION

* House sale price for 29 houses in Central Davis in 1999
*     29 observations on 9 variables 

****  5.1 EXAMPLE: HOUSE PRICE AND SIZE

* Download and load data from GitHub
clear
copy "${github_data_url}AED_HOUSE.DTA" "temp_data.dta", replace
use "temp_data.dta", clear
erase "temp_data.dta"
describe
summarize
* Table 5.1
sort price
list, clean 
* Table 5.2
summarize price, detail
mean price
summarize size, detail
mean size

****  5.2 TWO-WAY TABULATION

* Create categorical variables
generate pricerange = price
recode pricerange(1/249999=1) (250000/400000=2)
generate sizerange = size
recode sizerange (1/1799=1) (1800/2399=2) (2400/4000=3)
* Table 5.3
tabulate pricerange sizerange, row
* Table 5.4 - with expected frequencies
tabulate pricerange sizerange, expected

****  5.3 TWOWAY SCATTER PLOT

* Figure 5.1 First panel
scatter price size
graph export "images/ch05_fig1.png", replace

****  5.4 CORRELATION

* Figure 5.1 Second panel
scatter price size, xline(1883) yline(253910) xlabel(0(1000)4000) ylabel(0(100000)500000)
* Covariance and correlation coefficient
correlate price size, covariance
display %20.1f r(cov_12)
* Figure 5.2: Plot of four cases of correlation - skip

****  5.5 REGRESSION

* Download and load data from GitHub
clear
copy "${github_data_url}AED_HOUSE.DTA" "temp_data.dta", replace
use "temp_data.dta", clear
erase "temp_data.dta"
* Linear regression
regress price size
* Figure 5.3 - drawn in Word
* Figure 5.4
scatter price size || lfit price size
* Intercept-only regression compared to the sample mean
regress price
mean price 

****  5.6 MEASURES OF GOODNESS OF FIT

* Figure 5.5 - skip

**** 5.7 COMPUTER OUTPUT FOLLOWING REGRESSION

* Table 5.5
regress price size

**** 5.8 PREDICTION AND OUTLYING OBSERVATIONS

* predict at size = 2000
display _b[_cons] + _b[size]*2000
* predict all observations in sample
predict double yhat
generate double resid = y - yhat
summarize price yhat resid

****  5.9 REGRESSION AND CORRELATION

* Nothing

****  5.10 CAUSATION

* Reverse regression
regress size price

****  5.11 REGRESSION COMPUTATION

* Example with artifical data
clear
input x y 
 1 1
 2 2
 3 2
 4 2
 5 3
end
list 
summarize
* Figure 5.6
graph twoway (scatter y x) (function y = 0.8 + 0.4*x, range(0 6)), legend(off)
* Check hand calculations
regress y x
correlate y x
display r(rho)^2

****  5.12 NONPARAMETRIC REGRESSION

* Download and load data from GitHub
clear
copy "${github_data_url}AED_HOUSE.DTA" "temp_data.dta", replace
use "temp_data.dta", clear
erase "temp_data.dta"
sort size
list price size
correlate price size
regress price size
* local linear regression
lpoly price size, degree(1) bw(300) generate(xlpoly ylpoly)
* lowess with default bandwidth
lowess price size, generate(ylowess)
* Figure 5.7
graph twoway (scatter price size) (line ylpoly xlpoly) (line ylowess size)
  
********** CLOSE OUTPUT

display ""
display "Chapter 05 analysis complete."
display "Figures saved to: images/"
display "Tables saved to: tables/"
