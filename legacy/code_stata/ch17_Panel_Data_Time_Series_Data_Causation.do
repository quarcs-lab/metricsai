* ch17_Panel_Data_Time_Series_Data_Causation.do - January 2026 For Stata
* Updated for online execution portability
* old aed21.do has a lot more detail

********** OVERVIEW OF ch17_Panel_Data_Time_Series_Data_Causation.do **********

* STATA Program
* copyright C 2021 by A. Colin Cameron
* Used for "Analyis of Economics Data: An Introduction to Econometrics"
* by A. Colin Cameron (2021)

* To run you need file
*   AED_EARNINGS_COMPLETE
*   AED_NBA.DTA
*   AED_INTERESTRATES
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

* This STATA does analysis for Chapter 17
*   17.1 CROSS-SECTION DATA
*   17.2 PANEL DATA
*   17.3 PANEL DATA EXAMPLE: NBA TEAM REVENUE 
*   17.4 CAUSALITY: AN OVERVIEW
*   17.5 NONLINEAR REGRESSION MODELS
*   17.6 TIME SERIES DATA
*   17.7 TIME SERIES EXAMPLE: U.S. TREASURY SECURITY INTEREST RATES

********** DATA DESCRIPTION

* (1) Data on 29 NBA basketball teams over 10 seasons 2001-02 to 2010-11

**** 17.1 CROSS-SECTION DATA

* No computer analysis

**** 17.2 PANEL DATA

* No computer analysis

**** 17.3 PANEL DATA EXAMPLE: NBA TEAM REVENUE

* Download and load data from GitHub
clear
copy "${github_data_url}AED_NBA.DTA" "temp_data.dta", replace
use "temp_data.dta", clear
erase "temp_data.dta"
summarize

* Table 17.1
describe revenue lnrevenue wins season playoff champ allstars lncitypop teamid
summarize revenue lnrevenue wins season playoff champ allstars lncitypop teamid 
xtset teamid 
xtsum revenue lnrevenue wins season playoff champ allstars lncitypop teamid

* Manually compute within and between for lnrevenue
* team means
bysort teamid: egen meanlnrev = mean(lnrevenue)
* Number each observation for a team
bysort teamid: gen obsnum = _n
* Between standard deviation next
* Summary stats for the first team mean
sum meanlnrev if obsnum == 1
* Observation less team mean
gen mdifflnrev = lnrevenue - meanlnrev
* Between standard deviation next
sum lnrevenue mdifflnrev
* Check
xtsum lnrevenue

* Figure 17.1
graph twoway (scatter lnrevenue wins, msize(small))                    ///
    (lfit lnrevenue wins, lstyle(p1) lwidth(medthick))
graph export "images/ch17_fig1.png", replace

* OLS regression in Figure 17.1
regress lnrevenue wins

* Correlation
correlate revenue lnrevenue wins season playoff champ allstars lncitypop

* Declare the individual identifier and the time identifier
xtset teamid season
xtdescribe
xtsum lnrev wins season
xtsum revenue lnrevenue wins season playoff champ allstars lncitypop teamid

*** Pooled OLS estimation

* Table 17.2 - first column Pooled OLS with default standard errors
regress lnrev wins season
estimates store olsdef
* Table 17.2 - second column Pooled OLS with het-robust standard errors
regress lnrev wins season, vce(robust)
estimates store olshet
* Table 17.2 - third column Pooled OLS with cluster-robust standard errors
regress lnrev wins season, vce(cluster teamid)
estimates store olsclu
* Table 17.2
estimates table olsdef olshet olsclu, b(%10.5f) se(%10.5f) t(%10.2f) ///
    stfmt(%10.4f) stat(r2 r2_a)

*** Pooled, Random effects and Fixed effects estimation

global xlistlong wins season playoff champ allstars lncitypop

* Table 17.3 - First column OLS with default standard errors
reg lnrev $xlistlong, vce(robust)
estimates store olshet
* Table 17.3 - Second column OLS with cluster-robust standard errors
reg lnrev $xlistlong, vce(cluster teamid)
estimates store olsclu
* Table 17.3 - Third column Random effects with default standard errors
xtreg lnrev $xlistlong, re
estimates store redef
* Table 17.3 - Fourth column Random effects with cluster-robust standard errors
xtreg lnrev $xlistlong, re vce(robust)
estimates store rerob
* Table 17.3 - Fifth column Fixed effects with default standard errors
xtreg lnrev $xlistlong, fe
estimates store fedef
* Table 17.3 - Sixth column Fixed effects with cluster-robust standard errors
xtreg lnrev $xlistlong, fe vce(robust) 
estimates store feclu
* Table 17.3 
estimates table olshet olsclu redef rerob fedef feclu, ///
    b(%10.4f) se(%10.4f) t(%10.2f) stat(r2)

**** 17.4 CAUSALITY: AN OVERVIEW

* Figure 17.2 - created elsewhere

* No computer analysis
* See Chapter 13 for several applications

**** 17.5 NONLINEAR REGRESSION MODELS

* Table 17.4 - text table

* Figure 17.3 - created elsewhere

* Logit example
* Download and load data from GitHub
clear
copy "${github_data_url}AED_EARNINGS_COMPLETE.DTA" "temp_data.dta", replace
use "temp_data.dta", clear
erase "temp_data.dta"

generate dbigearn = earnings > 60000
summarize dbigearn
logit dbigearn age education, vce(robust)
margins, dydx(*)

regress dbigearn age education, vce(robust)

**** 17.6 TIME SERIES DATA

**** 17.7 EXAMPLE: U.S. TREASURY SECURITY INTEREST RATES

* Download and load data from GitHub
clear
copy "${github_data_url}AED_INTERESTRATES.DTA" "temp_data.dta", replace
use "temp_data.dta", clear
erase "temp_data.dta"
describe
summarize
list in 1, clean

* Table 17.5
summarize gs10 gs1 dgs10 dgs1

* Levels on levels with a time trend - HAC robust ses
regress gs10 gs1 time
predict uhatgs10, resid
corrgram uhatgs10
drop uhatgs10
newey gs10 gs1 time, lag(24)

* Figure 17.4 - simple
twoway (tsline gs10) (tsline gs1)
twoway (scatter gs10 gs1) (lfit gs10 gs1)

* Table 17.6 - rows 1 and 2 (levels)
corrgram gs10
corrgram gs1

* Table 17.6 - rows 3 and 4 (levels and time trend)
regress gs10 time
predict uhatgs10, resid
corrgram uhatgs10
drop uhatgs10
regress gs1 time
predict uhatgs1, resid
drop uhatgs1

* Table 17.6 - rows 5 and 6 (levels AR(1))
regress gs10 l.gs10
predict uhatgs10, resid
corrgram uhatgs10
estat bgodfrey, lags(12)
drop uhatgs10
regress gs1 l.gs1
predict uhatgs1, resid
corrgram uhatgs1
estat bgodfrey, lags(12)
drop uhatgs1

* Table 17.6 - rows 7 and 8 (changes)
corrgram dgs10
corrgram dgs1

* Levels on levels with a time trend
regress gs10 gs1 time
predict uhatgs10, resid
corrgram uhatgs10
drop uhatgs10

* Changes on changes
regress dgs10 dgs1
predict uhatdgs10, resid
corrgram uhatdgs10
drop uhatdgs10

* DL(2) model in changes
newey dgs10 dgs1 l.dgs1 l2.dgs1, lag(3)
* gives r2 and se
regress dgs10 dgs1 l.dgs1 l2.dgs1

* AR(2) model in changes
regress dgs10 l.dgs10 l2.dgs10
predict uhatgs10, resid
corrgram uhatgs10
estat bgodfrey, lags(12)
drop uhatgs10
regress gs1 l.gs1 l2.gs10
predict uhatgs1, resid
corrgram uhatgs1
estat bgodfrey, lags(12)
drop uhatgs1
regress dgs10 l.dgs10 l2.dgs10, vce(robust)

* ADL(2,2) model in changes
regress dgs10 l.dgs10 l2.dgs10 dgs1 l.dgs1 l2.dgs1, vce(robust)
* check that residuals are uncorrelated
predict uhat, resid
corrgram uhat
drop uhat

* Figure 17.5 - brief
twoway (tsline dgs10) (tsline dgs1)
twoway (scatter dgs10 dgs1) (lfit dgs10 dgs1)

*** Spurious Regression detection
* One way is to regress in changes - already done
* Second way is lags in levels included
regress gs10 gs1 l.gs10 l.gs1
newey gs10 gs1 l.gs10 l.gs1, lag(24)
estimates store SPUHAC
predict uhat, resid
corrgram uhat
drop uhat

* Impulse response function for ADL(2,2) model in changes
* regress dgs10 l.dgs10 l2.dgs10 dgs1 l.dgs1 l2.dgs1, vce(robust)
* First do two period ahead impulse response
* This just changes dependent variable to two periods forward
* The impulse response is the coefficient of dgs1
* Need to use newey with two lags as autocorrelation of two periods is induced
newey f2.dgs10 l.dgs10 l2.dgs10 dgs1 l.dgs1 l2.dgs1, lag(2)
display "Two-period impulse and standard error: " _b[dgs1] "  " _se[dgs1]

* The following code does a loop that gets impulse up to four periods ahead
forvalues h = 0/4 {
	newey f(`h').dgs10 l(1/2).dgs10 l(0/2).dgs1, lag(4)
	estimates store impulse`h'
	}
estimates table impulse0 impulse1 impulse2 impulse3 impulse4, keep(dgs1) b se t

********** CLOSE OUTPUT

display ""
display "Chapter 17 analysis complete."
display "Figures saved to: images/"
display "Tables saved to: tables/"
