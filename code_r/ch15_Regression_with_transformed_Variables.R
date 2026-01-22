# ch15_Regression_with_transformed_Variables.R - January 2026 For R
# Updated for online execution portability

########## OVERVIEW ##########

# R Program
# copyright C 2021 by A. Colin Cameron (original code)
# Updated: 2026 for portability
# Used for "Analysis of Economics Data: An Introduction to Econometrics"
# by A. Colin Cameron (2021)

# Data is streamed directly from GitHub - no local files needed
# Works in RStudio Cloud, Posit Cloud, and any online R environment

########## SETUP ##########

# Clear the workspace
rm(list=ls())

# Set random seed for reproducibility
set.seed(42)

# GitHub data URL
github_data_url <- "https://raw.githubusercontent.com/quarcs-lab/data-open/master/AED/"

# Create output directories (optional - for saving figures and tables locally)
images_dir <- "images"
tables_dir <- "tables"
dir.create(images_dir, showWarnings = FALSE, recursive = TRUE)
dir.create(tables_dir, showWarnings = FALSE, recursive = TRUE)

# Load required libraries (install if needed)
if (!require("haven")) install.packages("haven")
if (!require("car")) install.packages("car")
if (!require("sandwich")) install.packages("sandwich")
if (!require("jtools")) install.packages("jtools")
if (!require("huxtable")) install.packages("huxtable")
if (!require("margins")) install.packages("margins")
if (!require("QuantPsyc")) install.packages("QuantPsyc")

library(haven)
library(car)
library(sandwich)
library(jtools)
library(huxtable)
library(margins)
library(QuantPsyc)

# Function to load data from GitHub
load_data <- function(filename) {
  url <- paste0(github_data_url, filename)
  tryCatch({
    read_dta(url)
  }, error = function(e) {
    message("Error loading from GitHub: ", e$message)
    message("Attempting to load from local directory...")
    read_dta(file.path("../data_stata", filename))
  })
}

############
    
# This R program covers Chapter 15 of "Analysis of Economics Data"
#  15.1 EXAMPLE: EARNINGS, GENDER, EDUCATION and TYPE OF WORKER
#  15.2 MARGINAL EFFECTS FOR NONLINEAR MODELS
#  15.3 QUADRATIC MODEL AND POLYNOMIAL MODELS
#  15.4 INTERACTED REGRESSORS
#  15.5 LOG-LINEAR AND LOG-LOG MODELS
#  15.6 PREDICTION FROM LOG-LINEAR AND LOG-LOG MODELS
#  15.7 MODELS WITH A MIX OF REGRESSOR TYPES 

############ DATA DESCRIPTION

# Annual Earnings for 842 male and female full-time workers
# aged 25-65 years old in 2010

####  15.1 EXAMPLE: EARNINGS, GENDER, EDUCATION and TYPE OF WORKER

# Read in the Stata data set from GitHub
data.EARNINGS_COMPLETE = load_data("AED_EARNINGS_COMPLETE.DTA")

# Allow variables in database to be accessed simply by giving names
attach(data.EARNINGS_COMPLETE)

# Summarize the data set
summary(data.EARNINGS_COMPLETE)

# Table 15.1
table151vars = c("earnings", "lnearnings", "age", "agesq", "education", "agebyeduc",  
   "lnage", "gender", "dself", "dprivate", "dgovt", "hours", "lnhours")
summary(data.EARNINGS_COMPLETE[table151vars])

####  15.2 MARGINAL EFFECTS FOR NONLINEAR MODELS

## Figure 15.1 - created using generated data

####  15.3 QUADRATIC AND POLYNOMIAL MODELS

## Figure 15.2 - generated data

## Quadratic Model for Earnings on Age with Education as a regressor as well

# Use function summ in jtools package which also requires sandwich
# Linear Model
library(sandwich)
library(jtools)
ols.linear = lm(earnings ~ age+education)
summ(ols.linear, digits=3, robust = "HC1")

# Quadratic model
ols.quad = lm(earnings ~ age+agesq+education)
summ(ols.quad, digits=3, robust = "HC1")

# Turning point
bage = summary(ols.quad)$coefficients["age",1]
bagesq = summary(ols.quad)$coefficients["agesq",1]
turning.point = -bage/(2*bagesq)
turning.point

# Marginal effects
mequad = bage + 2*bagesq*age
summary(mequad)
AME.age = mean(mequad)
AME.age
MEM.age = bage + 2*bagesq*mean(age)
MEM.age
MER.age25 = bage + 2*bagesq*25
MER.age25

# Joint hypothesis test requires packages car and sandwich
library(car)
robvar = vcovHC(ols.quad, type="HC1")
linearHypothesis(ols.quad,c("age=0", "agesq=0"), vcov=robvar)

# ME for age using margins package
# and R's factor variable notation - age*age gives age and age^2
# and use heteroskedastic-robust standard errors which uses sandwich package
library(margins)
library(sandwich)
ols.factor.quad = lm(earnings ~ age*age + education)
summ(ols.factor.quad, digits=3, robust = "HC1")
# AMEs only
margins(ols.factor.quad)
# AMES with standard errors, z-statistic, confidence interval                
summary(margins(ols.factor.quad, vcov = vcovHC(ols.factor.quad, type="HC1")))
# AME for a single regressor
summary(margins(ols.factor.quad, variables = "age",
            vcov = vcovHC(ols.factor.quad, type="HC1")))
# MEM is not given by margins
# MER for a single regressor at two values
summary(margins(ols.factor.quad, variables = "age", 
            at=list(age=c(25,65)), vcov = vcovHC(ols.factor.quad, type="HC1")))

####  15.4 INTERACTED REGRESSORS

# Regression with interactions
ols.interact = lm(earnings ~ age+education+agebyeduc)
summ(ols.interact, digits=3, robust = "HC1")

# Joint test for statistical significance of age
robvar = vcovHC(ols.interact, type="HC1")
linearHypothesis(ols.interact,c("age=0", "agebyeduc=0"), vcov=robvar)

# The regressors are highly correlated
cor(cbind(age, education, agebyeduc))

# Marginal effects manually
beducation = summary(ols.interact)$coefficients["education",1]
bagebyeduc = summary(ols.interact)$coefficients["agebyeduc",1]
meinteract = beducation + bagebyeduc*age
AME.educ = summary(meinteract)
AME.educ
MEM.educ = beducation + bagebyeduc*summary(age)
MEM.educ
MER.educ.25 = beducation + bagebyeduc*25
MER.educ.25
     
# ME for education using margins package
# and R's factor variable notation - age*educ gives age, educ and age*educ
# and use heteroskedastic-robust standard errors which uses sandwich package
ols.factor.interact = lm(earnings ~ age*education)
summ(ols.factor.interact, digits=3, robust = "HC1")
# AMEs only
margins(ols.factor.interact)
# AMES with standard errors, z-statistic, confidence interval                
summary(margins(ols.factor.interact, vcov = vcovHC(ols.factor.interact, type="HC1")))
# AME for a single regressor
summary(margins(ols.factor.interact, variables = "education",
                vcov = vcovHC(ols.factor.interact, type="HC1")))
# MEM is not given by margins
# MER for a single regressor at two values
summary(margins(ols.factor.interact, variables = "education",
        vcov = vcovHC(ols.factor.interact, type="HC1")))
summary(margins(ols.factor.interact, variables = "education", 
        at=list(age=c(25,65)), vcov = vcovHC(ols.factor.interact, type="HC1")))

# Use package jtools which also needs huxtable for tables
library(huxtable)
export_summs(ols.linear, ols.quad, ols.interact, scale = TRUE, 
             error_format = "({statistic})", robust = "HC1")

####  15.5 LOG-LINEAR AND LOG-LOG MODELS

# Levels model
ols.linear2 <- lm(earnings ~ age+education)
summ(ols.linear, digits=3, robust = "HC1") 

# Log-linear model
ols.loglin2 <- lm(lnearnings ~ age+education)
summ(ols.loglin2, digits=3, robust = "HC1") 

# Log-log model
ols.loglog2 <- lm(lnearnings ~ lnage+education)
summ(ols.loglog2, digits=3, robust = "HC1")

# Use package jtools which also needs huxtable for tables
# For some reason gives wrong results
export_summs(ols.linear2, ols.loglin2, ols.loglog2, scale = TRUE, 
             error_format = "({statistic})", robust = "HC1")

####  15.6 PREDICTION FROM LOG-LINEAR AND LOG-LOG MODELS

# Levels model
ols.linear <- lm(earnings ~ age+education)
linear.predict = predict(ols.linear)

# Retransformation bias in log-linear model
ols.loglin = lm(lnearnings ~ age+education)
summary(ols.loglin)
predict.log = predict(ols.loglin)
biased.predict = exp(predict.log)
rmse = summary(ols.loglin)$sigma
rmse
exp(rmse^2/2)
adjusted.predict = exp(rmse^2/2)*biased.predict
summary(cbind(earnings, linear.predict, biased.predict, adjusted.predict))
cor(cbind(earnings, linear.predict, biased.predict, adjusted.predict)) 

# Retransformation bias in log-log model
ols.loglog <- lm(lnearnings ~ lnage+education)
summary(ols.loglog)
predict.loglog = predict(ols.loglog)
biased.predict = exp(predict.loglog)
rmse = summary(ols.loglog)$sigma
rmse
exp(rmse^2/2)
adjusted.predict = exp(rmse^2/2)*biased.predict
summary(cbind(earnings, linear.predict, biased.predict, adjusted.predict))
cor(cbind(earnings, linear.predict, biased.predict, adjusted.predict)) 

####  15.7 MODELS WITH A MIX OF REGRESSOR TYPES 

# Linear dependent variable
ols.linear <- lm(earnings ~ gender+age+agesq+education+dself+dgovt+lnhours)
summ(ols.linear, digits=3, robust = "HC1") 
linear.predict = predict(ols.linear)

# Log-transformed dependent variable
ols.log <- lm(lnearnings ~ gender+age+agesq+education+dself+dgovt+lnhours)
summ(ols.log, digits=3, robust = "HC1") 
predict.log = predict(ols.log)
biased.predict = exp(predict.log)
rmse = summary(ols.log)$sigma
rmse
exp(rmse^2/2)
adjusted.predict = exp(rmse^2/2)*biased.predict
summary(cbind(earnings, linear.predict, biased.predict, adjusted.predict))
cor(cbind(earnings, linear.predict, biased.predict, adjusted.predict))

# Levels dependent variable and standardized coefficients
library(QuantPsyc)
ols.linear <- lm(earnings ~ gender+age+agesq+education+dself+dgovt+lnhours)
lm.beta(ols.linear)

########## ANALYSIS COMPLETE ##########

cat("\n", rep("=", 70), "\n")
cat("ANALYSIS COMPLETE\n")
cat(rep("=", 70), "\n")
cat("\nFigures saved to:", images_dir, "\n")
cat("Tables saved to:", tables_dir, "\n")

# Detach database
detach(data.EARNINGS_COMPLETE)
