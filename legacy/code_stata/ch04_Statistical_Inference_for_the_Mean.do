* ch04_Statistical_Inference_for_the_Mean.do - January 2026 For Stata
* Updated for online execution portability

********** OVERVIEW OF ch04_Statistical_Inference_for_the_Mean.do **********

* STATA Program
* copyright C 2021 by A. Colin Cameron
* Used for "Analyis of Economics Data: An Introduction to Econometrics"
* by A. Colin Cameron (2021)

* To run you need file
*   AED_EARNINGS.DTA
*   AED_GASPRICE.DTA
*   AED_EARNINGSMALE.DTA
*   AED_REALGDPPC.DTA
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

* This STATA program does analysis for Chapter 4
*   4.1 EXAMPLE: MEAN ANNUAL EARNINGS
*   4.2 t STATISTIC AND t DISTRIBUTION
*   4.3 CONFIDENCE INTERVALS
*   4.4 TWO-SIDED HYPOTHESIS TESTS
*   4.5 TWO-SIDED HYPOTHESIS TEST EXAMPLES
*   4.6 ONE-SIDED DIRECTIONAL HYPOTHESIS TESTS
*   4.7 GENERALIZATIONS OF CONFIDENCE INTERVALS AND HYPOTHESIS TESTS
*   4.8 PROPORTIONS DATA

********** DATA DESCRIPTION

*  (1) Annual Earnings for 171 women age 30 years in 2010 Full-time workers
*  (2) Gasloine price per gallon at 32 service stations
*  (3) Annual Earnings for 191 men age 30 years in 2010 Full-time workers
*  (4) Quarterly data on U.S. real GDP per capita from 1959Q1 to 2020Q1

**** 4.1 EXAMPLE: MEAN ANNUAL EARNINGS

* Download and load data from GitHub
clear
copy "${github_data_url}AED_EARNINGS.DTA" "temp_data.dta", replace
use "temp_data.dta", clear
erase "temp_data.dta"
describe
summarize

* Summary statisitcs
summarize earnings

* 95% Confidence interval
mean earnings

* Hypothesis test
ttest earnings = 40000

****  4.2 t Statistic and t DISTRIBUTION

* Plot densities of standard normal and t distributions with 4 and 30 degrees of freedom

* Figure 4.1 - use twoway function
graph twoway (function t5 = tden(5,x), range(-3.5 3.5)) ///
    (function z = normalden(x), range(-3.5 3.5) lpattern(dash))
graph twoway (function t50 = tden(50,x), range(-3.5 3.5)) ///
    (function z = normalden(x), range(-3.5 3.5) lpattern(dash))
graph export "images/ch04_fig1.png", replace

* Figure 4.2 requires generating a variable first in order to use area graph1

* Generate t(170) data
clear
global nobs = 1000
set obs $nobs
generate x = -3.5 + _n/($nobs/7)
generate t170 = tden(170,x)

* Obtain the critical values
scalar tpoint05 = invttail(170,.05)
display "Critical value= " tpoint05
scalar tpoint025 = invttail(170,.025)
display "Critical value= " tpoint025

graph twoway (area t170 x if (x>tpoint05), color(gs9))  ///
    (line t170 x, lwidth(thick) lstyle(p1))
graph twoway (area t170 x if (x>tpoint025), color(gs9)) ///
    (area t170 x if (x<-tpoint025), color(gs9))         ///
    (line t170 x, lwidth(thick) lstyle(p1)), legend(off)
graph export "images/ch04_fig2.png", replace

**** 4.3 CONFIDENCE INTERVALS

* Download and load data from GitHub
clear
copy "${github_data_url}AED_EARNINGS.DTA" "temp_data.dta", replace
use "temp_data.dta", clear
erase "temp_data.dta"
summarize

* 95% Confidence interval
mean earnings

* 90% and 99% confidence intervals
mean earnings, level(90)
mean earnings, level(99)

* Confidence interval manually
* This uses command summarize stores the number of observations in r(N)
* the mean in r(mean), and the standard deviation in r(sd)
quietly summarize earnings
scalar mean = r(mean)
scalar tcrit = invttail(r(N)-1,.025)
scalar sterror = r(sd)/sqrt(r(N))
scalar intwidth = tcrit*sterror
display "mean = " mean _n "t_.025;n-1 = " tcrit _n "standard error = " ///
    sterror _n "interval width = " intwidth ///
    " 95% confidence interval = (" mean-intwidth ", "  mean+intwidth ")"

* 90% and 99% critical values
display "t_.05;n-1 = " invttail(r(N)-1,.05)
display "t_.005;n-1 = " invttail(r(N)-1,.005)

**** 4.4 TWO-SIDED HYPOTHESIS TEST

* Test H0: mu = 40000 against HA: mu not = 40000 using Stata command ttest
* This also does one-sided tests - in both directions.
ttest earnings = 40000

* Same two-sided test done manually
* This uses command summarize stores the number of observations in r(N)
* the mean in r(mean), and the standard deviation in r(sd)
scalar mu0 = 40000
summarize earnings
scalar t = (r(mean)-mu0)/(r(sd)/sqrt(r(N)))
display "t = " t
* Compute the p-value
display "p value = " 2*ttail(r(N)-1,abs(t))
* Compute the critical value at 5%
display invttail(r(N)-1,.025)

* Figure 4.3 shows graphically
* Generate t(170) data
clear
global nobs = 1000
set obs $nobs
generate x = -3.5 + _n/($nobs/7)
generate t = tden(170,x)
scalar tpoint025 = invttail(170,.025)
display "Case t=.723 and p=.470"
* P value approach
graph twoway (area t x if (x<-.723), color(gs9))              ///
    (area t x if (x>.724), color(gs9)) (line t x), legend(off)
* Critical value approach
graph twoway (area t x if (x>tpoint025), color(gs9))                ///
    (area t x if (x<-tpoint025), color(gs9)) (line t x), legend(off)
	
****   4.5 TWO-SIDED HYPOTHESIS TEST EXAMPLES

* Gasoline data collected September 3 2013 good for September 2 2013
* from sactogasprices.com part of GasBuddy.com
* Download and load data from GitHub
clear
copy "${github_data_url}AED_GASPRICE.DTA" "temp_data.dta", replace
use "temp_data.dta", clear
erase "temp_data.dta"
describe
summarize
ttest price = 3.81
scalar t = (3.6697-3.81)/(0.1510/sqrt(32))
display "t = " t " p = " 2*ttail(32,abs(t))
display invttail(31,.025)

* Male Earnings
* Download and load data from GitHub
clear
copy "${github_data_url}AED_EARNINGSMALE.DTA" "temp_data.dta", replace
use "temp_data.dta", clear
erase "temp_data.dta"
describe
summarize
summarize, detail

* Test H0: mu = 50000 against HA: mu not = 50000
ttest earnings = 50000
scalar t = (52353.93-50000)/(65034.74/sqrt(191))
display "t = " t " p = " 2*ttail(191,abs(t))
display invttail(190,.025)

* Growth per capita
* Download and load data from GitHub
clear
copy "${github_data_url}AED_REALGDPPC.DTA" "temp_data.dta", replace
use "temp_data.dta", clear
erase "temp_data.dta"
describe
sum

* Test H0: mu = 2.0 against HA: mu not = 2.0
ttest growth = 2.0
scalar t = (1.9904-2.0)/(2.1781/sqrt(241))
display "t = " t " p = " 2*ttail(241,abs(t))
display invttail(240,.025)

* For HAC standard errors see code for chapter 12.1 

**** 4.6 ONE-SIDED DIRECTIONAL HYPOTHESIS TESTS

* Figure 4.4 shows graphically one-sided test
* Generate t(170) data
clear
global nobs = 1000
set obs $nobs
generate x = -3.5 + _n/($nobs/7)
generate t = tden(170,x)
scalar tpoint05 = invttail(170,.05)
display "Case t=.723 and p=.235"
* P value approach
graph twoway (area t x if (x>.724), color(gs9)) (line t x)
* Critical value approach
graph twoway (area t x if (x>tpoint05), color(gs9)) (line t x)

* One-sided test example

* Download and load data from GitHub
clear
copy "${github_data_url}AED_EARNINGS.DTA" "temp_data.dta", replace
use "temp_data.dta", clear
erase "temp_data.dta"

* Test H0: mu < 40000 against HA: mu >= 40000 using Stata command ttest
ttest earnings = 40000

* Same one-sided test done manually
scalar mu0 = 40000
summarize earnings 
scalar t = (r(mean)-mu0)/(r(sd)/sqrt(r(N)))
display "t = " t
* Compute the p-value
display "p value = " ttail(r(N)-1,t)
* Compute the critical value at 5% 
display invttail(r(N)-1,.05)

*** 4.7 GENERALIZATIONS OF CONFIDENCE INTERVALS AND HYPOTHESIS TESTS

**** 4.8 PROPORTIONS DATA

clear
scalar mean = (480*1+441*0)/921
scalar sterror = sqrt( (mean*(1-mean)) / 921)
display "mean = " mean "  standard error = " sterror
display "95% CI = " mean-1.964*sterror " , " mean+1.964*sterror

scalar sterrorH0 = sqrt( (0.5*(1-0.5)) / 921)
scalar t = (mean - 0.5) / sterrorH0
scalar p = 2*(1-normal(abs(t)))
display "t = " t " p = " p

********** CLOSE OUTPUT

display ""
display "Chapter 04 analysis complete."
display "Figures saved to: images/"
display "Tables saved to: tables/"
