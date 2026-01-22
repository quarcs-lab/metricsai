* ch15_Regression_with_transformed_Variables.do - January 2026 For Stata
* Updated for online execution portability

********** OVERVIEW OF ch15_Regression_with_transformed_Variables.do **********

* STATA Program
* copyright C 2021 by A. Colin Cameron
* Used for "Analyis of Economics Data: An Introduction to Econometrics"
* by A. Colin Cameron (2021)

* To run you need file
*   AED_EARNINGS_COMPLETE
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

*  15.1 EXAMPLE: EARNINGS, GENDER, EDUCATION and TYPE OF WORKER
*  15.2 MARGINAL EFFECTS FOR NONLINEAR MODELS
*  15.3 QUADRATIC MODEL AND POLYNOMIAL MODELS
*  15.4 INTERACTED REGRESSORS
*  15.5 LOG-LINEAR AND LOG-LOG MODELS
*  15.6 PREDICTION FROM LOG-LINEAR AND LOG-LOG MODELS
*  15.7 MODELS WITH A MIX OF REGRESSOR TYPES 

********** DATA DESCRIPTION

* Annual Earnings for 842 male and female full-time workers
* aged 25-65 years old in 2010

****  15.1 EXAMPLE: EARNINGS, GENDER, EDUCATION and TYPE OF WORKER

* Table 15.1
* Download and load data from GitHub
clear
copy "${github_data_url}AED_EARNINGS_COMPLETE.DTA" "temp_data.dta", replace
use "temp_data.dta", clear
erase "temp_data.dta"
describe earnings lnearnings age agesq education agebyeduc lnage gender ///
    dself dprivate dgovt hours lnhours 
summarize earnings lnearnings age agesq education agebyeduc lnage gender ///
    dself dprivate dgovt hours lnhours 

****  15.2 MARGINAL EFFECTS FOR NONLINEAR MODELS

** Figure 15.1 - created using generated data

****  15.3 QUADRATIC AND POLYNOMIAL MODELS

*** Figure 15.2 - generated data
clear
set obs 100
generate x = 1 + 3*_n/100
generate y1 = 1 + 4*(x-2.5)^2
generate y2 = 1 + (x-4)^2
generate y3 = 1 + (x-1)^2
generate y4 = 10 - 4*(x-2.5)^2
generate y5 = 10 - (x-4)^2
generate y6 = 10 - (x-1)^2
twoway (line y1 x), scale(1.5) legend(off) xtitle(" ") ytitle(" ") ylabel(, angle(0)) saving(graph1, replace)
twoway (line y2 x), scale(1.5) legend(off) xtitle(" ") ytitle(" ") ylabel(, angle(0)) saving(graph2, replace)
twoway (line y3 x), scale(1.5) legend(off) xtitle(" ") ytitle(" ") ylabel(, angle(0)) saving(graph3, replace)
twoway (line y4 x), scale(1.5) legend(off) xtitle(" ") ytitle(" ") ylabel(, angle(0)) saving(graph4, replace)
twoway (line y5 x), scale(1.5) legend(off) xtitle(" ") ytitle(" ") ylabel(, angle(0)) saving(graph5, replace)
twoway (line y6 x), scale(1.5) legend(off) xtitle(" ") ytitle(" ") ylabel(, angle(0)) saving(graph6, replace)

* Figure 15.2
graph combine graph1.gph graph2.gph graph3.gph graph4.gph graph5.gph graph6.gph, ///
  iscale(0.8) ysize(4) xsize(6) rows(2) ycommon xcommon title("Examples of Quadratic Model")

*** Quadratic Model for Earnings on Age with Education as a regressor as well

* Download and load data from GitHub
clear
copy "${github_data_url}AED_EARNINGS_COMPLETE.DTA" "temp_data.dta", replace
use "temp_data.dta", clear
erase "temp_data.dta"
describe
summarize

* Linear Model
regress earnings age education, vce(robust)
estimates store BASE

* Quadratic model
regress earnings age agesq education, vce(robust)
estimates store QUAD
display "Turning point is at " -_b[age]/(2*_b[agesq])
generate mequad = _b[age] + 2*_b[agesq]*age
summarize mequad
summarize mequad if age == 25
summarize mequad if age == 65
summarize age
display "MEM = " _b[age] + 2*_b[agesq]*r(mean)
display "MER at age 25 = " _b[age] + 2*_b[agesq]*25
test age agesq

* ME for age using margins and Stata's factor variable notation
regress earnings c.age##c.age education, vce(robust)
* AME
margins, dydx(*)
* MEM
margins, dydx(*) atmean
* MER marginal effect at a representative value e.g. age=25
margins, dydx(*) at(age=25)

****  15.4 INTERACTED REGRESSORS

* Regression with interactions
regress earnings age education agebyeduc, vce(robust)
estimates store INTERACT

* Joint test for statistical significance of age
test age agebyeduc
* Joint test for statistical significance of education
test education agebyeduc

* The regressors are highly correlated
correlate age education agebyeduc

* ME for education using margins and Stata's factor variable notation
regress earnings c.education##c.age, vce(robust)
* AME
margins, dydx(*)
* MEM
margins, dydx(*) atmean
* MER marginal effect at a representative value e.g. age=25
margins, dydx(*) at(age=25)

* ME for education done manually
quietly regress earnings age education agebyeduc, vce(robust)
* MEM
quietly summarize age
scalar meanage = r(mean)
lincom _b[education] + meanage*_b[agebyeduc]
display "MEM = " _b[education] + meanage*_b[agebyeduc]
* AME
generate ME_Ed = _b[education] + age*_b[agebyeduc]
mean ME_Ed
* MER
quietly regress earnings age education agebyeduc
display "ME of education at age 25 = " _b[education] + 25*_b[agebyeduc]
display "ME of education at age 65 = " _b[education] + 65*_b[agebyeduc]

estimates table BASE QUAD INTERACT, ///
    b(%11.0f) se(%11.0f) t(%11.2f) stfmt(%11.3f) stat(N r2 r2_a rmse F) 

****  15.5 LOG-LINEAR AND LOG-LOG MODELS

* Levels model
regress earnings age education, vce(robust)
predict pearnings

* Log-linear model
regress lnearnings age education, vce(robust)

* Log-log model
regress lnearnings lnage education, vce(robust)

****  15.6 PREDICTION FROM LOG-LINEAR AND LOG-LOG MODELS

* Retransformation bias in log-linear model
regress lnearnings age education, vce(robust)
predict plnearnings
display "s_e = " e(rmse) " and exp(s_e^2/2) = " exp(e(rmse)^2/2)
generate biasedpearnings = exp(plnearnings)
generate correctedpearnings = exp(e(rmse)^2/2)*biasedpearnings
summarize earnings pearnings biasedpearnings correctedpearnings
correlate earnings pearnings correctedpearnings
drop plnearnings biasedpearnings correctedpearnings

* Retransformation bias in log-log model
regress lnearnings lnage education, vce(robust)
predict plnearnings
display "s_e = " e(rmse) " and exp(s_e^2/2) = " exp(e(rmse)^2/2)
generate biasedpearnings = exp(plnearnings)
generate correctedpearnings = exp(e(rmse)^2/2)*biasedpearnings
summarize earnings pearnings biasedpearnings correctedpearnings
correlate earnings pearnings biasedpearnings correctedpearnings
drop pearnings plnearnings biasedpearnings correctedpearnings

****  15.7 MODELS WITH A MIX OF REGRESSOR TYPES

* Linear dependent variable
regress earnings gender age agesq education dself dgovt lnhours, vce(robust)
predict pearnings

* Log-transformed dependent variable
regress lnearnings gender age agesq education dself dgovt lnhours, vce(robust)
predict plnearnings
display "s_e = " e(rmse) " and exp(s_e^2/2) = " exp(e(rmse)^2/2)
generate biasedpearnings = exp(plnearnings)
generate correctedpearnings = exp(e(rmse)^2/2)*biasedpearnings
summarize earnings pearnings biasedpearnings correctedpearnings
correlate earnings pearnings biasedpearnings correctedpearnings

* Levels dependent variable and standardized coefficients - option beta
regress earnings gender age agesq education dself dgovt lnhours, beta vce(robust)

********** CLOSE OUTPUT

display ""
display "Chapter 15 analysis complete."
display "Figures saved to: images/"
display "Tables saved to: tables/"
