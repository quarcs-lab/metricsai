* ch16_Checking_the_Model_and_Data.do - January 2026 For Stata
* Updated for online execution portability

********** OVERVIEW OF ch16_Checking_the_Model_and_Data.do **********

* STATA Program
* copyright C 2021 by A. Colin Cameron
* Used for "Analyis of Economics Data: An Introduction to Econometrics"
* by A. Colin Cameron (2021)

* To run you need file
*   AED_EARNINGS_COMPLETE.DTA
*   AED_DEMOCRACY.DTA
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

* This STATA does analysis for Chapter 16
*  16.1 MULTICOLLINEAR DATA
*  16.2 FAILURE OF MODEL ASSUMPTIONS
*  16.3 INCORRECT POPULATION MDOEL
*  16.4 REGRESSORS CORRELATED WITH ERRORS
*  16.5 HETEROSKEDASTIC ERRORS
*  16.6 CORRELATED ERRORS
*  16.7 EXAMPLE: DEMOCRACY AND GROWTH 
*  16.8 DIAGNOSTICS

************

**** 16.1 MULTICOLLINEARITY

* Download and load data from GitHub
clear
copy "${github_data_url}AED_EARNINGS_COMPLETE.DTA" "temp_data.dta", replace
use "temp_data.dta", clear
erase "temp_data.dta"
summarize
describe

regress earnings age education, vce(robust)
regress earnings age education agebyeduc, vce(robust)
test age agebyeduc
test education agebyeduc
correlate agebyeduc age education
regress agebyeduc age education

**** 16.2 MODEL ASSUMPTIONS REVISITED

* No computations done

**** 16.3 INCORRECT POPULATION MDOEL

* No computations done

**** 16.4 REGRESSORS CORRELATED WITH ERRORS

* No computations done

**** 16.5 HETEROSKEDASTIC ERRORS

* Generate data with autocorrelated error
clear all
set obs 1000
set seed 10101
* time period
gen t = _n
* e_t is underlying N(0,1) error
gen e=rnormal(0,1)
* Serially Correlated Errors u_t = 0.8*u_t-1 + e_t
gen u=rnormal(0,1)
replace u=0.8*u[_n-1]+e in 2/1000
* regressor
gen x = rnormal(0,1)
* y_1t with serially correlated error
gen y1 = 1 + 2*x + u
* y_2t is serially correlated but with i.i.d. error
* For this d.g.p. E[y2] = 1/(1-0.6) = 2.5 so initialize y2 = 2.5
gen y2 = 0
replace y2 = 1 + 0.6*y2[_n-1] + 2*x + e in 2/1000
* y_3t is serially correlated and the error is serially correlated
* For this d.g.p. E[y3] = 1/(1-0.6) = 2.5 so initialize y3 = 2.5
gen y3 = 0
replace y3 = 1 + 0.6*y3[_n-1] + 2*x + u in 2/1000
* If need to e.g. drop the first observation give command drop if t==1
summarize
correlate
* Some time series analysis requires tsset
tsset t
corrgram e, lags(10)
corrgram u, lags(10)
corrgram y1, lags(10)
corrgram y3, lags(10)
* Regressions
* y_1t with serially correlated error
reg y1 x, vce(robust)
estimates store y1rob
predict u1hat, resid
corrgram u1hat, lags(10)
newey y1 x, lag(10)
estimates store y1HAC
* y_2t is serially correlated but with i.i.d. error
reg y2 l.y2 x, vce(robust)
estimates store y2rob
predict u2hat, resid
corrgram u2hat, lags(10)
newey y2 l.y2 x, lag(10)
estimates store y2HAC
* y_3t is serially correlated and the error is serially correlated
reg y3 l.y3 x, vce(robust)
estimates store y3rob
predict u3hat, resid
corrgram u3hat, lags(10)
newey y3 l.y3 x, lag(10)
estimates store y3HAC
estimates table y1rob y1HAC y2rob y2HAC y3rob y3HAC, b(%8.4f) se stat(r2 N)

**** 16.6 CORRELATED ERRORS

* No computations done

**** 16.7 EXAMPLE: DEMOCRACY AND GROWTH 

* Download and load data from GitHub
clear
copy "${github_data_url}AED_DEMOCRACY.DTA" "temp_data.dta", replace
use "temp_data.dta", clear
erase "temp_data.dta"
summarize
describe

* Table 16.1
describe democracy growth constraint indcent catholic muslim protestant other
summarize democracy growth constraint indcent catholic muslim protestant other
correlate democracy growth constraint indcent catholic muslim protestant other

* Bivariate regression
regress democracy growth
regress democracy growth, vce(robust)

* Figure 16.1 - Simple version
twoway (scatter democracy growth, msymbol(none) mlabel(code) mlabsize(vsmall)) ///
  (lfit democ growth)

* Multiple regression
regress democracy growth constraint indcent catholic muslim protestant
regress democracy growth constraint indcent catholic muslim protestant, vce(robust)

**** 16.8 DIAGNOSTICS

quietly regress democracy growth constraint indcent catholic muslim protestant
predict yhat
predict uhat, resid

* Figure 16.2 - simple
twoway (scatter democ yhat) (lfit democ yhat) (lowess uhat yhat)
twoway (scatter uhat yhat) (lowess uhat yhat), yline(0)

* Figure 16.3 using Stata commands
quietly regress democracy growth constraint indcent catholic muslim protestant
* First panel: Residual versus regressor plot
rvpplot growth, yline(0)
* Second panel: Component plus residual plot
cprplot growth, lowess
* Third panel: Added variable plot
avplot growth

* Figure 16.3 done manually
* Residual versus Regressor
twoway (scatter uhat growth) (lfit uhat growth) (lowess uhat growth)
* Component plus residual plot: crplot done manually
generate prgrowth = _b[growth]*growth + uhat
twoway (scatter prgrowth growth) (lfit prgrowth growth) (lowess prgrowth growth)
* Added variable plot: avplot done manually
* growth is dropped
regress democracy constraint indcent catholic muslim protestant
predict uhat1democ, resid
* growth is dependent variable
regress growth constraint indcent catholic muslim protestant
predict uhat1growth, resid
twoway(scatter uhat1democ uhat1growth) (lfit uhat1democ uhat1growth) ///
    (lowess uhat1democ uhat1growth)
	
** Influential Observations

* Outliers that effect yhat
quietly regress democracy growth constraint indcent catholic muslim protestant
predict dfits, dfits
summarize dfits, d
scalar threshold = 2*sqrt((e(df_m)+1)/e(N))
display "dfits threshold = " %6.3f threshold
summarize dfits if abs(dfits) > threshold
generate dfitslarge = (abs(dfits) > threshold)
list country dfits democracy growth if abs(dfits) > threshold, clean

* Effect of dropping outliers
quietly regress democracy growth constraint indcent catholic muslim ///
    protestant, vce(robust)
estimates store all
quietly regress democracy growth constraint indcent catholic muslim ///
    protestant if abs(dfits) < threshold,  vce(robust)
estimates store some
estimates table all some, b se stat(r2 N rmse)

* Outliers that effect uhat
quietly regress democracy growth constraint indcent catholic muslim protestant
predict dfbgrowth, dfbeta(growth)
summarize dfbgrowth, d
scalar threshold = 2*sqrt(1/e(N))
display "dfbeta threshold = "  %6.3f threshold
list country dfbgrowth democracy growth if abs(dfbgrowth) > threshold, clean

* Effect of dropping outliers
quietly regress democracy growth constraint indcent catholic muslim ///
    protestant, vce(robust)
estimates store all
quietly regress democracy growth constraint indcent catholic muslim ///
    protestant if abs(dfbgrowth) < threshold,  vce(robust)
estimates store some
estimates table all some, b se stat(r2 N rmse)
	

********** CLOSE OUTPUT
display ""
display "Chapter 16 analysis complete."
display "Figures saved to: images/"
display "Tables saved to: tables/"
