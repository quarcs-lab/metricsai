# ch01_Analysis_of_Economics_Data.R - January 2026 For R
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
library(haven)

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

########## DATA DESCRIPTION ##########

# House sale price for 29 houses in Central Davis in 1999
#     29 observations on 9 variables

########## 1.3 REGRESSION ANALYSIS ##########

# Read in the Stata data set from GitHub
data.HOUSE <- load_data("AED_HOUSE.DTA")

# Allow variables in database to be accessed simply by giving names
attach(data.HOUSE)

# Summarize the data set
cat("\n", strrep("=", 70), "\n")
cat("Data Summary\n")
cat(strrep("=", 70), "\n")
summary_stats <- summary(data.HOUSE)
print(summary_stats)

# Save summary statistics to table
write.csv(as.data.frame(do.call(cbind, lapply(data.HOUSE, summary))),
          file.path(tables_dir, "ch01_descriptive_stats.csv"))
cat("\nTable saved to:", file.path(tables_dir, "ch01_descriptive_stats.csv"), "\n")

# Fit the regression line
ols <- lm(price ~ size)

# Display regression results
cat("\n", strrep("=", 70), "\n")
cat("OLS Regression Results: price ~ size\n")
cat(strrep("=", 70), "\n")
print(summary(ols))

# Save regression results
sink(file.path(tables_dir, "ch01_regression_summary.txt"))
print(summary(ols))
sink()
cat("\nRegression summary saved to:", file.path(tables_dir, "ch01_regression_summary.txt"), "\n")

# Save regression coefficients
coef_table <- data.frame(
  coefficient = coef(ols),
  std_error = summary(ols)$coefficients[, "Std. Error"],
  t_value = summary(ols)$coefficients[, "t value"],
  p_value = summary(ols)$coefficients[, "Pr(>|t|)"]
)
write.csv(coef_table, file.path(tables_dir, "ch01_regression_coefficients.csv"))
cat("Coefficients saved to:", file.path(tables_dir, "ch01_regression_coefficients.csv"), "\n")

########## FIGURE 1.1: SCATTER PLOT WITH FITTED LINE ##########

# Display plot in R console
plot(size, price,
     xlab="House size (in square feet)",
     ylab="House sale price (in dollars)",
     pch=19, col="black",
     main="Figure 1.1: House Price vs Size")
abline(ols, col="blue", lwd=2)
legend("topleft",
       c("Actual", "Fitted"),
       lty=c(0, 1),
       pch=c(19, NA),
       col=c("black", "blue"),
       bty="o")

# Save Figure 1.1 to file
png(file.path(images_dir, "ch01_fig1_house_price_vs_size.png"),
    width=800, height=600)
plot(size, price,
     xlab="House size (in square feet)",
     ylab="House sale price (in dollars)",
     pch=19, col="black",
     main="Figure 1.1: House Price vs Size")
abline(ols, col="blue", lwd=2)
legend("topleft",
       c("Actual", "Fitted"),
       lty=c(0, 1),
       pch=c(19, NA),
       col=c("black", "blue"),
       bty="o")
dev.off()
cat("\nFigure saved to:", file.path(images_dir, "ch01_fig1_house_price_vs_size.png"), "\n")

########## ANALYSIS COMPLETE ##########

cat("\n", strrep("=", 70), "\n")
cat("ANALYSIS COMPLETE\n")
cat(strrep("=", 70), "\n")
cat("\nFigures saved to:", images_dir, "\n")
cat("Tables saved to:", tables_dir, "\n")

# Detach database
detach(data.HOUSE)
