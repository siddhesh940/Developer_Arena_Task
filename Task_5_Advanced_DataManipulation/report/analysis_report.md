# Week 5 – Advanced Data Manipulation with Pandas

## 1. Project Overview

Customer Sales Analysis is the Week 5 internship project for The Developers Arena. It uses the actual customer churn and sales datasets to demonstrate advanced Pandas manipulation, independent customer and sales analysis, validation, aggregation, filtering, date operations, pivot tables, and a Matplotlib dashboard.

## 2. Project Objectives

- Load and inspect two real CSV datasets.
- Clean and validate customer and sales data.
- Analyze customer tenure, charges, contracts, payment methods, and churn.
- Analyze sales by month, product, region, and quantity.
- Test whether customer and sales IDs can be joined.
- Demonstrate groupby aggregations, filtering, string cleaning, datetime columns, and pivot tables.
- Create a professional five-chart dashboard.
- Produce evidence-based insights and recommendations.

## 3. Dataset Description

### customer_churn.csv

- Rows: 500
- Columns: 9
- Columns: `CustomerID`, `Tenure`, `MonthlyCharges`, `TotalCharges`, `Contract`, `PaymentMethod`, `PaperlessBilling`, `SeniorCitizen`, `Churn`
- Customer identifiers use the `C00001` format.

### sales_data.csv

- Rows: 100
- Columns: 7
- Columns: `Date`, `Product`, `Quantity`, `Price`, `Customer_ID`, `Region`, `Total_Sales`
- Dates range from 2024-01-01 to 2024-04-09.
- Customer identifiers use the `CUST001` format.

## 4. Technologies Used

- Python
- Pandas
- Matplotlib
- VS Code
- Git
- GitHub

## 5. Project Structure

```text
Task_5_Advanced_DataManipulation/
├── main.py
├── customer_churn.csv
├── sales_data.csv
├── requirements.txt
├── data/
├── visualizations/
│   ├── sales_by_product.png
│   ├── sales_by_region.png
│   ├── monthly_sales_trend.png
│   ├── churn_by_contract.png
│   └── sales_distribution.png
├── report/
│   └── analysis_report.md
└── screenshots/
```

## 6. Setup Instructions

From this project folder, install dependencies:

```text
python -m pip install -r requirements.txt
```

Run the analysis:

```text
python main.py
```

## 7. Data Loading

`main.py` loads both supplied files with `pd.read_csv()`. It checks each file exists, is not empty, can be parsed, and contains the required columns.

## 8. Data Exploration

Both datasets were inspected before analysis.

- Customer shape: `(500, 9)`
- Sales shape: `(100, 7)`
- Customer missing values: `0`
- Sales missing values: `0`
- Customer duplicate rows: `0`
- Sales duplicate rows: `0`

The customer file loaded numeric fields as integers and categorical fields as objects. The sales file loaded `Date` as text initially and numeric sales fields as integers. The script displays the first five rows, columns, data types, and statistics during execution.

## 9. Data Cleaning

- Numeric customer fields and sales fields are validated with `pd.to_numeric(..., errors="coerce")`.
- `Date` is converted with `pd.to_datetime(..., errors="coerce")`.
- Churn is validated to contain only `0` and `1`.
- Category and identifier text is stripped with Pandas string operations.
- Cleaning uses in-memory copies and removes missing or duplicate rows only if present.
- Actual data required no removals because both datasets had zero missing values and zero duplicate rows.
- Derived sales columns are `Year`, `Month`, `Month_Name`, `Day`, and `Day_of_Week`.

## 10. Advanced Pandas Operations

The project demonstrates:

- `groupby()` for product, region, month, contract, and payment summaries.
- Aggregations using `sum()`, `mean()`, and counts.
- Multiple-condition filtering with `&` and `isin()`.
- String cleanup with `.str.strip()`.
- Datetime conversion and date component extraction.
- Set-based ID overlap checking before a potential merge.
- Two `pd.pivot_table()` summaries.
- Calculated date columns and churn-rate percentages.

## 11. Aggregations

Three required sales aggregations and their actual results are:

### Total sales by product

| Product    | Total sales |
| ---------- | ----------: |
| Laptop     |   3,889,210 |
| Tablet     |   2,884,340 |
| Phone      |   2,859,394 |
| Headphones |   1,384,033 |
| Monitor    |   1,348,071 |

### Total sales by region

| Region | Total sales |
| ------ | ----------: |
| North  |   3,983,635 |
| South  |   3,737,852 |
| East   |   2,519,639 |
| West   |   2,123,922 |

### Monthly total sales

| Month   | Total sales |
| ------- | ----------: |
| 2024-01 |   4,120,524 |
| 2024-02 |   2,656,050 |
| 2024-03 |   4,485,006 |
| 2024-04 |   1,103,468 |

Additional actual metrics: total sales `12,365,048`, total quantity `478`, and average sale `123,650.48`.

## 12. Merge / Join Analysis

The potential join was checked between `customer_churn.CustomerID` and `sales_data.Customer_ID`. There were **0 overlapping IDs**: the customer file uses IDs such as `C00001`, while the sales file uses IDs such as `CUST001`.

Because there are no matches, the program does not perform a misleading customer-sales merge and does not fabricate top customer sales rankings. Customer churn and sales performance are analyzed independently.

## 13. Pivot Tables

### Sales by product and region

| Product    |    East |     North |     South |    West |
| ---------- | ------: | --------: | --------: | ------: |
| Headphones | 288,361 |   107,091 |   512,168 | 476,413 |
| Laptop     | 221,946 | 1,798,206 | 1,373,120 | 495,938 |
| Monitor    | 642,870 |   397,100 |    39,924 | 268,177 |
| Phone      | 506,828 |   489,284 | 1,471,428 | 391,854 |
| Tablet     | 859,634 | 1,191,954 |   341,212 | 491,540 |

### Monthly sales by product

The program creates a second pivot with months as rows and products as columns. It shows January through April 2024 product totals and is printed during execution.

## 14. Customer Analysis

- The customer dataset contains 500 customers.
- Overall churn was `10.60%`.
- Contract counts were Month-to-month `170`, One year `186`, and Two year `144`.
- Average tenure for retained customers was `40.15` months; average tenure for churned customers was `6.00` months.
- Average monthly charges were `111.72` for retained customers and `129.77` for churned customers.
- Average total charges were `4,234.58` for retained customers and `4,265.75` for churned customers.
- Customer-sales top rankings are unavailable because no IDs matched the sales data.

## 15. Sales Analysis

Sales totalled `12,365,048` across 100 transactions and 478 units. Laptop was the strongest product at `3,889,210`, and North was the strongest region at `3,983,635`. March was the strongest complete month at `4,485,006`; April is partial because the data ends on April 9.

## 16. Churn Analysis

- Month-to-month churn: `20.59%` (35 of 170).
- One-year contract churn: `4.30%` (8 of 186).
- Two-year contract churn: `6.94%` (10 of 144).
- Credit Card churn: `13.48%`.
- Electronic Check churn: `11.04%`.
- Bank Transfer churn: `6.92%`.
- Paperless Billing Yes churn: `11.11%`; No churn: `10.12%`.
- Senior Citizen churn: `10.04%`; non-senior churn: `11.16%`.
- Tenure analysis showed all 53 churned customers were in the first 12-month band, while the 12+ month bands had zero churn in this dataset.

These are grouped comparisons only and do not establish causation.

## 17. Visualizations

1. [Sales by Product](../visualizations/sales_by_product.png) - bar chart comparing product revenue; Laptop leads.
2. [Sales by Region](../visualizations/sales_by_region.png) - bar chart comparing regional revenue; North leads.
3. [Monthly Sales Trend](../visualizations/monthly_sales_trend.png) - line chart showing monthly movement; March is highest and April is partial.
4. [Churn by Contract](../visualizations/churn_by_contract.png) - bar chart showing the highest churn rate for month-to-month contracts.
5. [Sales Distribution](../visualizations/sales_distribution.png) - pie chart showing each product's share of sales.

## 18. Dashboard

Together, the five charts form a compact performance dashboard: product and region charts compare sales, the line chart shows timing, the contract chart highlights churn differences, and the pie chart shows product revenue mix.

## 19. Key Insights

- Most valuable sales product: Laptop, by total product revenue.
- Individual most valuable customers cannot be identified because the two customer ID systems have zero overlap.
- North generated the most sales.
- March was the strongest complete month; April is incomplete.
- Churn is highest in the month-to-month contract group and concentrated in the first 12 months.
- Churned customers had higher average monthly charges than retained customers in this dataset.

## 20. Business Recommendations

- Prioritize early-tenure onboarding and retention outreach because every observed churned customer was in the first 12 months.
- Review month-to-month customer offers and provide clear value for longer contracts, while monitoring whether incentives are appropriate.
- Investigate Laptop inventory and promotion opportunities because it leads product revenue.
- Review North-region demand and capacity because North leads regional sales.
- Repair or formally map the two customer ID systems before attempting customer-level sales value targeting.
- Treat April sales as partial-period data when comparing months.

## 21. Technical Requirements Fulfilled

- Pandas performs all major loading, cleaning, aggregation, filtering, date, and pivot operations.
- More than three aggregations are implemented: product, region, month, quantity, contract, payment, and churn summaries.
- Join feasibility is tested using the actual ID columns; no invalid merge is forced.
- Two pivot tables are created with `pd.pivot_table()`.
- Missing values, duplicates, numeric fields, dates, and churn values are validated.
- Multiple-condition filters use Pandas boolean expressions.
- Five professional Matplotlib visualizations are saved as PNG files.
- Error handling covers missing, empty, malformed, and schema-invalid files.
- Comments explain key cleaning and analysis steps.

## 22. Testing

The following command was executed successfully:

```text
python main.py
```

Verified results:

- Both datasets loaded successfully.
- Shapes, columns, first rows, and data-quality counts printed.
- Date conversion completed successfully.
- Product, region, and monthly aggregations printed.
- Multi-condition filters returned 14 high-value North/South sales and 194 long-tenure, high-charge customers.
- ID overlap returned 0 and the limitation was reported.
- Both pivot tables printed.
- Churn groupings printed.
- Five visualization files were generated successfully.
- Python compilation completed without errors.

## 23. Visual Documentation

No screenshots are fabricated. Capture these manually after execution:

1. Dataset loading and first rows.
2. Data cleaning and validation output.
3. Aggregation output.
4. Pivot table output.
5. Merge/join overlap output.
6. Final analysis output.
7. Dashboard charts.

## 24. What I Learned

This project practices advanced Pandas groupby operations, multiple aggregations, filtering, string operations, datetime operations, merge feasibility checks, pivot tables, Matplotlib visualization, churn analysis, and evidence-based business recommendations.

## 25. Conclusion

The Week 5 project successfully analyzes the actual customer and sales datasets. It finds strong product and regional sales performance, documents the zero-overlap limitation between the ID systems, identifies early-tenure and month-to-month churn patterns, and presents the results in a five-chart dashboard without fabricating customer matches.
