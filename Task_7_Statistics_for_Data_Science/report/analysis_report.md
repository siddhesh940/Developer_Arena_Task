# Week 7 – Introduction to Statistics for Data Science

## 1. Project Overview

This Statistical Business Analysis project uses the actual sales and customer churn datasets supplied for The Developers Arena internship. It demonstrates descriptive statistics, hypothesis testing, correlation, covariance, confidence intervals, regression, visualization, and business interpretation.

## 2. Objectives

- Inspect and clean both datasets.
- Describe sales distributions.
- Perform at least three appropriate hypothesis tests.
- Analyze relationships between numerical variables.
- Estimate the mean sale with a confidence interval.
- Model sales using quantity with linear regression.
- Turn statistical evidence into cautious business recommendations.

## 3. Dataset Description

### sales_data.csv

- Shape: `100 rows × 7 columns`
- Columns: `Date`, `Product`, `Quantity`, `Price`, `Customer_ID`, `Region`, `Total_Sales`
- Date range: 2024-01-01 to 2024-04-09

### customer_churn.csv

- Shape: `500 rows × 9 columns`
- Columns: `CustomerID`, `Tenure`, `MonthlyCharges`, `TotalCharges`, `Contract`, `PaymentMethod`, `PaperlessBilling`, `SeniorCitizen`, `Churn`

No missing values or duplicate rows were found in either dataset. Customer IDs and sales IDs have different formats and zero overlap, so customer sales rankings cannot be calculated reliably.

## 4. Technologies Used

Python, Pandas, NumPy, SciPy, Matplotlib, Seaborn, and VS Code.

## 5. Setup Instructions

```text
cd /d D:\Developer_Arena\Week1_Task\Task_7_Statistics_for_Data_Science
py -m pip install -r requirements.txt
py statistical_analysis.py
```

## 6. Data Cleaning

Dates were converted with `pd.to_datetime`. Numeric columns were validated with `pd.to_numeric`. The script checks required columns, missing values, duplicates, non-negative sales values, and valid binary churn values. Since both actual datasets had zero missing values and zero duplicates, no important records were removed.

Derived sales fields include year, month, and month name for time analysis.

## 7. Descriptive Statistics

For `Total_Sales` across 100 transactions:

| Measure            |                                           Value |
| ------------------ | ----------------------------------------------: |
| Mean               |                                      123,650.48 |
| Median             |                                       97,955.50 |
| Mode               | No unique mode; all 100 sales values occur once |
| Standard deviation |                                      100,161.09 |
| Minimum            |                                           6,540 |
| First quartile     |                                       39,517.50 |
| Third quartile     |                                      175,792.50 |
| Maximum            |                                         373,932 |

Total sales were `12,365,048` and total quantity was `478`. Laptop was the top product; North was the top region.

## 8. Hypothesis Testing

All tests use significance level `alpha = 0.05`. Full generated evidence is in `hypothesis_tests_results.txt`.

### Test 1: One-sample t-test

- H0: Mean Total_Sales equals 100,000.
- H1: Mean Total_Sales differs from 100,000.
- Statistic: `2.361244`
- p-value: `0.0201722`
- Decision: Reject H0.
- Interpretation: The observed average transaction differs statistically from the selected 100,000 benchmark.

### Test 2: One-way ANOVA by region

- H0: All regional mean sales are equal.
- H1: At least one regional mean differs.
- Statistic: `2.164363`
- p-value: `0.0972368`
- Decision: Fail to reject H0.
- Interpretation: At the 0.05 level, this sample does not provide sufficient evidence that average transaction values differ by region.

### Test 3: Pearson correlation

- H0: Population correlation between Price and Total_Sales is zero.
- H1: The correlation is not zero.
- Correlation/statistic: `0.646131`
- p-value: `3.88216e-13`
- Decision: Reject H0.
- Interpretation: Price and Total_Sales have a statistically significant positive linear relationship in this dataset. This is association, not proof of causation.

### Test 4: Chi-square test

- H0: Contract and Churn are independent.
- H1: Contract and Churn are associated.
- Statistic: `27.715301`
- p-value: `9.58735e-07`
- Decision: Reject H0.
- Interpretation: Churn proportions differ across contract groups in this sample; this does not prove contract type causes churn.

## 9. Correlation Analysis

The Pearson correlation between Price and Total_Sales was `0.646131` with p-value `3.88216e-13`, indicating a statistically significant positive association. The heatmap includes the correlation matrix for Quantity, Price, and Total_Sales. The analysis uses correlation to describe linear association, not causation.

The sample covariance between Quantity and Total_Sales was `178,380.29`, a positive value consistent with the positive quantity-sales relationship. Covariance depends on measurement units, so the standardized Pearson correlation is easier to compare across variable pairs.

## 10. Confidence Intervals

The 95% confidence interval for mean Total_Sales is:

- Lower bound: `103,776.35`
- Upper bound: `143,524.61`
- Margin of error: `19,874.13`

In simple business terms, this interval estimates a plausible range for the population's average transaction value under the sampling assumptions of the t interval.

## 11. Regression Analysis

A simple linear regression predicts Total_Sales from Quantity:

- Slope: `26,629.54`
- Intercept: `-3,638.74`
- R-squared: `0.4735`
- Slope p-value: `2.58051e-15`

The positive slope means higher quantity is associated with higher total sales in this sample. Quantity explains approximately 47.35% of the variation in Total_Sales under this simple linear model. The intercept is a mathematical model parameter and is not interpreted as a realistic zero-quantity sale.

## 12. Key Business Insights

- Laptop leads total product revenue and North leads regional revenue.
- March was the strongest complete month; April is partial because data ends on April 9.
- Price and Total_Sales show a significant positive association.
- Contract and Churn show a significant association, with month-to-month customers having the highest observed churn rate in the customer dataset.
- The two datasets cannot identify most valuable customers together because their ID formats have zero overlap. It would be inappropriate to fabricate customer sales rankings.

## 13. Visualization Explanation

- `distribution.png`: histogram and KDE showing the distribution of transaction values.
- `sales_by_region_boxplot.png`: box plots comparing regional sales spread and possible outliers.
- `regression.png`: scatter plot with fitted regression line for Quantity and Total_Sales.
- `correlation_heatmap.png`: correlation matrix for Quantity, Price, and Total_Sales.
- `monthly_sales.png`: monthly sales trend using the converted Date column.

## 14. Testing

The complete script was run successfully with:

```text
py statistical_analysis.py
```

Verified:

- Both datasets loaded.
- Data quality checks completed.
- Dates and numeric columns converted.
- Four hypothesis tests executed.
- Confidence interval and margin of error calculated.
- Correlation and regression calculated.
- Five visualizations generated.
- `hypothesis_tests_results.txt` generated.
- No runtime errors remained.

## 15. Conclusion

The analysis provides evidence about transaction values, regional variation, price-sales association, quantity-sales modeling, and churn-contract patterns. The results support targeted retention attention for contract groups with higher observed churn and continued product/region monitoring, while respecting the limitation that customer and sales IDs cannot be joined.
