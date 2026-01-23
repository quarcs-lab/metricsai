# Dataset Documentation

This directory contains the datasets used throughout the metricsAI course. All data files are in Stata (.DTA) format and are automatically loaded from GitHub when running the notebooks.

## Data Access

The notebooks are configured to stream data directly from the GitHub repository, so **no manual downloads are required**. The data is accessed via URLs like:

```python
github_url = "https://github.com/quarcs-lab/metricsai/raw/main/data/"
df = pd.read_stata(github_url + "AED_HOUSE.DTA")
```

## Main Datasets

| Dataset File | Description | Used In | Key Variables |
|--------------|-------------|---------|---------------|
| **AED_HOUSE.DTA** | Housing price data | Ch01, Ch05, Ch06 | House prices, square footage, location |
| **AED_EARNINGS.DTA** | Earnings and education data | Ch02, Ch03, Ch04 | Earnings, education, experience |
| **AED_EARNINGSMALE.DTA** | Male earnings subset | Ch02 | Male earnings, demographics |
| **AED_EARNINGS_COMPLETE.DTA** | Complete earnings dataset | Ch10-Ch13 | Comprehensive labor market variables |
| **AED_AUTOSMPG.DTA** | Automobile fuel efficiency | Ch08, Ch09 | MPG, weight, horsepower, price |
| **AED_HEALTH2009.DTA** | Health expenditure data | Ch07 | Health spending, insurance status |
| **AED_HEALTHINSEXP.DTA** | Health insurance expenditures | Ch13, Ch16 | Insurance, medical costs |
| **AED_HEALTHACCESS.DTA** | Healthcare access survey | Ch14 | Access indicators, demographics |
| **AED_REALGDPPC.DTA** | Real GDP per capita | Ch17 | GDP, country, year |
| **AED_DEMOCRACY.DTA** | Democracy and development | Ch08 | Democracy index, GDP, institutions |
| **AED_INSTITUTIONS.DTA** | Institutional quality data | Ch08 | Governance, economic indicators |
| **AED_RETURNSTOSCHOOLING.DTA** | Returns to education | Ch13 | Schooling, wages, demographics |
| **AED_NBA.DTA** | NBA player statistics | Ch14 | Player stats, positions, salaries |
| **AED_FISHING.DTA** | Recreational fishing data | Ch16 | Fishing trips, prices, income |
| **AED_GDPUNEMPLOY.DTA** | GDP and unemployment | Ch17 | GDP, unemployment rate, time |
| **AED_PHILLIPS.DTA** | Phillips curve data | Ch17 | Inflation, unemployment |
| **AED_INCUMBENCY.DTA** | Political incumbency effects | Ch14 | Election results, incumbency |
| **AED_CAPM.DTA** | Capital Asset Pricing Model | Ch05, Ch07 | Stock returns, market returns |
| **AED_INTERESTRATES.DTA** | Interest rate data | Ch17 | Interest rates, time series |
| **AED_SP500INDEX.DTA** | S&P 500 index data | Ch17 | Stock index, dates |
| **AED_COBBDOUGLAS.DTA** | Production function data | Ch09 | Output, capital, labor |
| **AED_GASPRICE.DTA** | Gasoline price data | Ch09 | Gas prices, time |

## Additional Files

- **AED_CENSUSAGEMEANS.DTA** - Census age group means for simulation exercises
- **AED_CENSUSREGRESSIONS.DTA** - Census regression results
- **AED_COINTOSSMEANS.DTA** - Coin toss simulation data for statistical concepts
- **AED_GENERATEDDATA.DTA** - Simulated data for teaching statistical concepts
- **AED_HEALTHCATEGORIES.DTA** - Health status categories
- **AED_MONTHLYHOMESALES.DTA** - Time series of home sales
- **AED_API99.DTA** - Academic Performance Index data
- **exercises/** - Subdirectory containing additional exercise datasets

## Data Source

All datasets are from Colin Cameron's textbook *Analysis of Economics Data: An Introduction to Econometrics* and are used with permission for educational purposes.

Original source: https://cameron.econ.ucdavis.edu/aed/

## Notes

- All data files are in Stata 13+ format (.DTA)
- Data is automatically converted to pandas DataFrames when loaded
- No local downloads required when using Google Colab notebooks
- Some datasets have duplicate files (marked with (1), (2)) - these can be ignored
