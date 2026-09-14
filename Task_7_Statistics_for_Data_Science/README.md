# Statistical Business Analysis

Week 7 of The Developers Arena internship applies descriptive statistics, hypothesis testing, correlation, confidence intervals, and regression to the supplied sales and customer churn datasets.

## Objectives

- Calculate descriptive statistics.
- Test business hypotheses with SciPy.
- Measure correlation and covariance.
- Calculate a 95% confidence interval and margin of error.
- Fit a simple regression model.
- Create statistical visualizations and business recommendations.

## Technologies

Python, Pandas, NumPy, SciPy, Matplotlib, Seaborn, and VS Code.

## Datasets

- `sales_data.csv`: 100 rows and 7 columns.
- `customer_churn.csv`: 500 rows and 9 columns.

Both datasets were loaded from actual supplied files. No missing values or duplicate rows were found.

## Setup and Run

```text
cd /d D:\Developer_Arena\Week1_Task\Task_7_Statistics_for_Data_Science
py -m pip install -r requirements.txt
py statistical_analysis.py
```

## Statistical Methods

- Descriptive statistics for Total_Sales.
- One-sample t-test against a 100,000 benchmark.
- One-way ANOVA across regions.
- Pearson correlation significance test for Price and Total_Sales.
- Chi-square independence test for Contract and Churn.
- 95% confidence interval for mean Total_Sales.
- Linear regression of Total_Sales on Quantity.

## Main Findings

- Mean sale: `123,650.48`.
- 95% confidence interval: `103,776.35` to `143,524.61`.
- Laptop is the top product by sales.
- North is the top region by sales.
- Price and Total_Sales have a statistically significant positive correlation.
- Contract and Churn are statistically associated in this dataset.
- The sales and customer ID formats have zero overlap, so customer-level sales rankings are not claimed.

## Project Structure

```text
Task_7_Statistics_for_Data_Science/
├── statistical_analysis.py
├── statistical_analysis.ipynb
├── sales_data.csv
├── customer_churn.csv
├── requirements.txt
├── hypothesis_tests_results.txt
├── visualizations/
├── screenshots/
└── report/
```

Screenshots are not fabricated; capture them manually after running the analysis.
