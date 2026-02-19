# ch16_Checking_the_Model_and_Data.R - January 2026 For R
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
if (!require("dplyr")) install.packages("dplyr")
if (!require("olsrr")) install.packages("olsrr")

library(haven)
library(car)
library(sandwich)
library(jtools)
library(huxtable)
library(dplyr)
library(olsrr)

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

# This R program does analysis for Chapter 16
#  16.1 MULTICOLLINEAR DATA
#  16.2 FAILURE OF MODEL ASSUMPTIONS
#  16.3 INCORRECT POPULATION MDOEL
#  16.4 REGRESSORS CORRELATED WITH ERRORS
#  16.5 HETEROSKEDASTIC ERRORS
#  16.6 CORRELATED ERRORS
#  16.7 EXAMPLE: DEMOCRACY AND GROWTH 
#  16.8 DIAGNOSTICS

############ DATA DESCRIPTION

# Annual Earnings for 842 male and female full-time workers
# aged 25-65 years old in 2010

##### 16.1 MULTICOLLINEARITY

# Read in the Stata data set from GitHub
data.EARNINGS_COMPLETE = load_data("AED_EARNINGS_COMPLETE.DTA")

# Allow variables in database to be accessed simply by giving names
attach(data.EARNINGS_COMPLETE)

# Summarize the data set
summary(data.EARNINGS_COMPLETE)

# Regression - uses jtools package which needs sandwich package
library(sandwich)
library(jtools)
ols.base = lm(earnings ~ age+education)
summ(ols.base, digits=3, robust = "HC1")

# Add interacgtion variable
ols.collinear = lm(earnings ~ age+education+agebyeduc)
summ(ols.collinear, digits=3, robust = "HC1")

# Joint hypothesis test requires packages car and sandwich
library(car)
robvar = vcovHC(ols.collinear, type="HC1")
linearHypothesis(ols.collinear,c("age=0", "agebyeduc=0"), vcov=robvar)
linearHypothesis(ols.collinear,c("education=0", "agebyeduc=0"), vcov=robvar)

# The regressors are highly correlated
cor(cbind(age, education, agebyeduc))
ols.check = lm(agebyeduc ~ age+education)
summary(ols.check)

#### 16.2 MODEL ASSUMPTIONS REVISITED

# No computations done

#### 16.3 INCORRECT POPULATION MDOEL

# No computations done

#### 16.4 REGRESSOTS CORRELATED WITH ERRORS

# No computations done

#### 16.5 HETEROSKEDASTIC ERRORS

# No computations done

#### 16.6 CORRELATED ERRORS

## Time series generated data
# Generate data
n <- 10000                # Sample size
set.seed(10101)
e = rnorm(n,0,1)  # e_t is underlying N(0,1) error
u <- numeric(n)
# Autocorrelated Errors u_t = 0.8*u_t-1 + e_t
u[1] <- 0
for( t in 2:n ) {
   u[t] <- 0.8*u[t-1] + e[t]
}
# Autocorrelated regressor x_t = 0.8*x_t-1 + v_t where v_t ~ N(0,1)
v = rnorm(n,0,1)
x <- numeric(n)
x[1] <- 0
for( t in 2:n ) {
    x[t] <- 0.8*x[t-1] + v[t]
}
# y_1t with serially correlated error
y1 = 1 + 2*x + u    
# y_2t is serially correlated but with i.i.d. error
# For this d.g.p. E[y2] = 1/(1-0.6) = 2.5 so initialize y2 = 2.5
y2 <- numeric(n)
y2[1] <- 2.5
for( t in 2:n ) {
    y2[t] <- 1 + 0.6*y2[t-1] + 2*x[t] + e[t]
}
# y_3t is serially correlated and the error is serially correlated
# For this d.g.p. E[y3] = 1/(1-0.6) = 2.5 so initialize y3 = 2.5
y3 <- numeric(n)
y3[1] = 2.5
for( t in 2:n ) {
    y3[t] <- 1 + 0.6*y3[t-1] + 2*x[t] + u[t]
}
# Create variables lagged one period using package dplyr
library(dplyr)
y2lag <- lag(y2,n=1)
head(cbind(y2,y2lag))    # Check
y3lag <- lag(y3,n=1)
summary(y3lag)

# Declare data as time series data so can use acf
# setobs 1 1 --time-series
# Correlograms
acf(e, plot=FALSE, lag.max=10)
acf(u, plot=FALSE, lag.max=10)
acf(y1, plot=FALSE, lag.max=10)
acf(y2, plot=FALSE, lag.max=10)
acf(y3, plot=FALSE, lag.max=10)

# For heteroskedastic-robust and HAC-robust 
library(jtools)
library(sandwich)
# Regressions with heteroskedastic-robust standard errors
# y_1t with serially correlated error
ols.y1 <- lm(y1 ~ x)
u1hat = resid(ols.y1)
acf(u1hat, plot=FALSE, lag.max=10)
# Default standard errors
summ(ols.y1, digits=4)
# Heteroskedastic-robust standard errors
summ(ols.y1, digits=4, robust = "HC1")
# Newey-west HAC-robust
HACvar <- NeweyWest(ols.y1,lag=10)
HACse <- diag(HACvar)^0.5
HACse
# y_2t is serially correlated but with i.i.d. error
ols.y2 <- lm(y2 ~ y2lag+x, na.action=na.omit)
u2hat = resid(ols.y2)
acf(u2hat, plot=FALSE, lag.max=10)
# Heteroskedastic-robust results
summ(ols.y2, digits=4, robust = "HC1")
# Newey-west HAC-robust
HACvar <- NeweyWest(ols.y2,lag=10)
HACse <- diag(HACvar)^0.5
HACse
# y_3t is serially correlated and the error is serially correlated
ols.y3 <- lm(y3 ~ y3lag+x, na.action=na.omit)
u3hat = resid(ols.y3)
acf(u3hat, plot=FALSE, lag.max=10)
# Heteroskedastic-robust results
summ(ols.y3, digits=4, robust = "HC1")
# Newey-west HAC-robust
HACvar <- NeweyWest(ols.y3,lag=10)
HACse <- diag(HACvar)^0.5
HACse

# The following tries to drop the first observation manually
# Create data frame
gen.data <- data.frame(t,e,u,x,y1,y2,y3,y2lag,y3lag)
summary(gen.data)
head(gen.data)
# Drop first observation
new.data <- gen.data[2:100,]
head(new.data)
summary(new.data)
ols.y3alt <- lm(y3 ~ y3lag+x, data=new.data)
summ(ols.y3alt, digits=3, robust = "HC1")
summ(ols.y3, digits=3, robust = "HC1")

#### 16.7 EXAMPLE: DEMOCRACY AND GROWTH

# Read in data from GitHub
data.DEMOCRACY = load_data("AED_DEMOCRACY.DTA")
attach(data.DEMOCRACY)
summary(data.DEMOCRACY)

# Table 16.1
table161vars = c("democracy", "growth", "constraint", "indcent", "catholic", 
    "muslim", "protestant", "other")
summary(data.DEMOCRACY[table161vars])

cor(cbind(democracy, growth, constraint, indcent, catholic, muslim, protestant, other))

# Bivariate regression
ols.bivariate = lm(democracy ~ growth)
summ(ols.bivariate, digits=3, robust = "HC1")

# Figure 16.1
# Display in console
plot(growth, democracy, xlab="Change in Democracy",
    ylab="Change in Log GDP per capita",
     main="Democracy and Growth, 1500-2000", pch=19)
abline(ols.bivariate)

# Save to file
png(file.path(images_dir, "ch16_fig1_democracy_growth.png"),
    width=800, height=600)
plot(growth, democracy, xlab="Change in Democracy",
    ylab="Change in Log GDP per capita",
     main="Democracy and Growth, 1500-2000", pch=19)
abline(ols.bivariate)
dev.off()
cat("\nFigure saved to:", file.path(images_dir, "ch16_fig1_democracy_growth.png"), "\n")

# Multiple regression
ols.multiple = lm(democracy ~ growth+constraint+indcent+catholic+muslim+protestant)
summ(ols.multiple, digits=3, robust = "HC1")

#### 16.8 DIAGNOSTICS

yhat = predict(ols.multiple)
uhat = resid(ols.multiple)

# Figure 16.2 using olsrr package
# Actual versus fitted
ols_plot_obs_fit(ols.multiple)

# Save actual versus fitted
png(file.path(images_dir, "ch16_fig2a_actual_vs_fitted_olsrr.png"),
    width=800, height=600)
ols_plot_obs_fit(ols.multiple)
dev.off()

# Residual versus fitted
ols_plot_resid_fit(ols.multiple)

# Save residual versus fitted
png(file.path(images_dir, "ch16_fig2b_residual_vs_fitted_olsrr.png"),
    width=800, height=600)
ols_plot_resid_fit(ols.multiple)
dev.off() 

# Figure 16.2 - Manually
# Figure 16.2 - Panel A   Actual vs. Fitted
plot(yhat, democracy, xlab="Predicted value of y", ylab="Actual value of y",
    main="Actual vs. Fitted", pch=19)
ols.actvsfitted = lm(democracy ~ yhat)
abline(ols.actvsfitted)
lines(lowess(yhat, democracy), lty=3)

# Save Panel A
png(file.path(images_dir, "ch16_fig2a_actual_vs_fitted.png"),
    width=800, height=600)
plot(yhat, democracy, xlab="Predicted value of y", ylab="Actual value of y",
    main="Actual vs. Fitted", pch=19)
abline(ols.actvsfitted)
lines(lowess(yhat, democracy), lty=3)
dev.off()

# Figure 16.2 - Panel B  Residual vs. Fitted
plot(uhat, democracy, xlab="Predicted value of y", ylab="OLS Residual",
    main="Residual vs. Fitted", pch=19)
ols.residvsfitted = lm(democracy ~ uhat)
abline(ols.residvsfitted)
abline(ols.multiple)
lines(lowess(uhat, democracy), lty=3)

# Save Panel B
png(file.path(images_dir, "ch16_fig2b_residual_vs_fitted.png"),
    width=800, height=600)
plot(uhat, democracy, xlab="Predicted value of y", ylab="OLS Residual",
    main="Residual vs. Fitted", pch=19)
abline(ols.residvsfitted)
abline(ols.multiple)
lines(lowess(uhat, democracy), lty=3)
dev.off()

# Figure 16.3 using olsrr package for all regressors
# Residual versus Regressor
# Not available
# Figure 16.3 - Panel B  Component plus residual plot
ols_plot_comp_plus_resid(ols.multiple)

# Save component plus residual plots
png(file.path(images_dir, "ch16_fig3b_comp_plus_resid.png"),
    width=1200, height=800)
ols_plot_comp_plus_resid(ols.multiple)
dev.off()

# Figure 16.3 - Panel C  Added variable plot
ols_plot_added_variable(ols.multiple)

# Save added variable plots
png(file.path(images_dir, "ch16_fig3c_added_variable.png"),
    width=1200, height=800)
ols_plot_added_variable(ols.multiple)
dev.off()

# Figure 16.3 done manually for a single regressor growth
# Figure 16.3 - Panel A  Residual versus Regressor
plot(growth, uhat, xlab="Growth regressor", ylab="Democracy Residual",
    main="Residual versus Regressor", pch=19)
abline(h=0)
lines(lowess(growth, uhat), lty=3)

# Save Panel A
png(file.path(images_dir, "ch16_fig3a_residual_vs_regressor.png"),
    width=800, height=600)
plot(growth, uhat, xlab="Growth regressor", ylab="Democracy Residual",
    main="Residual versus Regressor", pch=19)
abline(h=0)
lines(lowess(growth, uhat), lty=3)
dev.off()

# Figure 16.3 - Panel B  Component plus residual plot
bgrowth=summary(ols.multiple)$coefficients["growth",1]
prgrowth = bgrowth*growth + uhat
ols.compplusres = lm(prgrowth ~ growth)
plot(growth, prgrowth, xlab="Growth regressor", ylab="Dem Res + .049*Growth",
    main="Component Plus Residual", pch=19)
abline(ols.compplusres)
lines(lowess(growth, prgrowth), lty=3)

# Save Panel B
png(file.path(images_dir, "ch16_fig3b_comp_plus_resid_manual.png"),
    width=800, height=600)
plot(growth, prgrowth, xlab="Growth regressor", ylab="Dem Res + .049*Growth",
    main="Component Plus Residual", pch=19)
abline(ols.compplusres)
lines(lowess(growth, prgrowth), lty=3)
dev.off()

# Figure 16.3 - Panel C  Added variable plot done manually
# Drop growth from regression model
ols.nogrowth = lm(democracy ~ constraint+indcent+catholic+muslim+protestant)
uhat1democ = resid(ols.nogrowth)
# Growth is dependent variable
ols.growth = lm(growth ~ constraint+indcent+catholic+muslim+protestant)
uhat1growth = resid(ols.growth)
ols.addedvar = lm(uhat1democ ~ uhat1growth)
plot(uhat1growth, uhat1democ, xlab="Growth regressor", ylab="Democracy Partial Residual",
    main="Added Variable", pch=19)
abline(ols.addedvar)
lines(lowess(uhat1growth, uhat1democ), lty=3)

# Save Panel C
png(file.path(images_dir, "ch16_fig3c_added_variable_manual.png"),
    width=800, height=600)
plot(uhat1growth, uhat1democ, xlab="Growth regressor", ylab="Democracy Partial Residual",
    main="Added Variable", pch=19)
abline(ols.addedvar)
lines(lowess(uhat1growth, uhat1democ), lty=3)
dev.off()

## Influential Observations
ols.multiple = lm(democracy ~ growth+constraint+indcent+catholic+muslim+protestant)

# DFITS
# Plot
ols_plot_dffits(ols.multiple)

# Save DFITS plot
png(file.path(images_dir, "ch16_dffits.png"),
    width=800, height=600)
ols_plot_dffits(ols.multiple)
dev.off()

# List the threshold and large DFITS
dfits = ols_plot_dffits(ols.multiple, print_plot= FALSE)
print(dfits$threshold)
print(dfits$outliers)
summary(dfits$outliers)

# DFBETAS - Separate plots for each regressor
ols_plot_dfbetas(ols.multiple)

# Save DFBETAS plots
png(file.path(images_dir, "ch16_dfbetas.png"),
    width=1200, height=800)
ols_plot_dfbetas(ols.multiple)
dev.off()

dfbetas = ols_plot_dfbetas(ols.multiple, print_plot= FALSE)

########## ANALYSIS COMPLETE ##########

cat("\n", rep("=", 70), "\n")
cat("ANALYSIS COMPLETE\n")
cat(rep("=", 70), "\n")
cat("\nFigures saved to:", images_dir, "\n")
cat("Tables saved to:", tables_dir, "\n")

# Detach databases
detach(data.EARNINGS_COMPLETE)
detach(data.DEMOCRACY)
