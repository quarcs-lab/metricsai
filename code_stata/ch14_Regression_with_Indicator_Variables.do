* ch14_Regression_with_Indicator_Variables.do - January 2026 For Stata
* Updated for online execution portability

********** OVERVIEW OF ch14_Regression_with_Indicator_Variables.do **********

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

* This STATA does analysis for Chapter 14
*  14.1 EXAMPLE: EARNINGS, GENDER, EDUCATION and TYPE OF WORKER
*  14.2 REGRESSION ON JUST A SINGLE INDICATOR VARIABLE
*  14.3 REGRESSION ON A SINGLE INDICATOR VARIABLE AND ADDITIONAL REGERESSORS
*  14.4 REGRESSION ON SETS OF INDICATOR VARIABLES

********** DATA DESCRIPTION

* Annual Earnings for 842 male and female full-time workers
* aged 25-65 years old in 2010


****  14.1 EXAMPLE: EARNINGS, GENDER, EDUCATION and TYPE OF WORKER

* Download and load data from GitHub
clear
copy "${github_data_url}AED_EARNINGS_COMPLETE.DTA" "temp_data.dta", replace
use "temp_data.dta", clear
erase "temp_data.dta"
describe
summarize

* Table 14.1
describe earnings gender education genderbyeduc age genderbyage hours ///
   genderbyhours dself dprivate dgovt 
summarize earnings gender education genderbyeduc age genderbyage hours ///
   genderbyhours dself dprivate dgovt 
   
****  14.2 REGRESSION ON JUST A SINGLE INDICATOR VARIABLE

* Figure 14.1 code not included as for illustration

* Table 14.2 Summary statistics by gender
* female
summarize earnings if gender == 1
* male
summarize earnings if gender == 0

* OLS for difference in means - heteroskedastic-robust standard errors
regress earnings gender, vce(robust)
* Similar test using ttest and unequal variances
ttest earnings, by(gender) unequal

* Aside: with equal variances regress and ttest give exactly same results
regress earnings gender
ttest earnings, by(gender)

****  14.3 REGRESSION ON A SINGLE INDICATOR VARIABLE AND ADDITIONAL REGERESSORS

* Gender indicator only 
regress earnings gender, vce(robust)
estimates store D_ONLY
test gender 

* Add education 
regress earnings gender education, vce(robust)
estimates store D_ED
test gender

* Interact education and gender  
regress earnings gender education genderbyeduc, vce(robust)
estimates store D_ED_DBYED
test gender genderbyeduc

* Add additional controls education and gender  
regress earnings gender education genderbyeduc age hours, vce(robust)
estimates store D_CONTROLS
test gender genderbyeduc

* Fully interact
regress earnings gender genderbyeduc education age hours genderbyage ///
    genderbyhours, vce(robust)
estimates store D_FULL_INT
test gender genderbyeduc genderbyage genderbyhours

* Table 14.3
estimates table D_ONLY D_ED D_ED_DBYED D_CONTROLS D_FULL_INT, ///
    b(%11.0f) se(%11.0f) t(%11.2f) stfmt(%11.3f) stat(N r2 r2_a rmse F)

* Joint regression
regress earnings gender genderbyeduc education age hours genderbyage ///
    genderbyhours, vce(robust) noheader
* Separate regressions by gender
regress earnings gender education age hours if gender==1, vce(robust) noheader
regress earnings gender education age hours if gender==0, vce(robust) noheader

****  14.4 REGRESSION ON SETS OF INDICATOR VARIABLES

* regress on indicators with no intercept
regress earnings dself dprivate dgovt, noconstant vce(robust)
regress earnings dself dprivate dgovt, noconstant
mean earnings if dself==1
mean earnings if dprivate==1
mean earnings if dgovt==1

* Base with no indicator variables
regress earnings age education, vce(robust)
estimates store NOINDIC

* Reference group is self-employed
regress earnings age education dprivate dgovt, vce(robust)
estimates store NOSELF
test dprivate dgovt

* Reference group is private
regress earnings age education dself dgovt, vce(robust) 
estimates store NOPRIVATE
test dself dgovt

* Reference group is government
regress earnings age education dself dprivate, vce(robust) 
estimates store NOGOVT
test dself dprivate

* No intercept
regress earnings age education dself dprivate dgovt, noconstant vce(robust)
estimates store NOINT
test (dself=dprivate) (dself=dgovt)
test (dself=dprivate) (dprivate=dgovt)

* Table 14.4
estimates table NOINDIC NOSELF NOPRIVATE NOGOVT NOINT, ///
    keep(age education dself dprivate dgovt _cons)     ///
    b(%11.0f) se(%11.0f) t(%11.2f) stfmt(%11.3f) stat(N r2 r2_a rmse F) 

** Difference in several means

* No regressors and drop self-employed
regress earnings dprivate dgovt, vce(robust)
estimates store NOREG1

* No regressors and drop intercept 
regress earnings dself dprivate dgovt, noconstant vce(robust)
estimates store NOREG2

estimates table NOREG1 NOREG2, keep(dself dprivate dgovt _cons) ///
    b(%11.0f) se(%11.0f) t(%11.2f) stfmt(%11.3f) stat(N r2 r2_a rmse F) 

* ANOVA gives the same F statistic as with default standard errors
generate typeworker = 1*dself + 2*dprivate + 3*dgovt
bysort typeworker: summarize earnings
anova earnings typeworker

********** CLOSE OUTPUT
display ""
display "Chapter 14 analysis complete."
display "Figures saved to: images/"
display "Tables saved to: tables/"
