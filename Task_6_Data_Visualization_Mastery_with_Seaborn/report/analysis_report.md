# Week 6 - Data Visualization Mastery with Seaborn

## 1. Project Overview

This project creates an Interactive Sales Dashboard for The Developers Arena internship. It uses the provided sales data with Pandas, creates statistical charts with Seaborn, and builds an interactive HTML dashboard with Plotly.

## 2. Project Objectives

- Load and validate real sales data.
- Explore sales by product, region, and month.
- Create useful statistical visualizations.
- Compare numerical variables with correlation analysis.
- Build an interactive dashboard with KPI cards and filters.
- Document actual findings without fabricating data.

## 3. Dataset Description

The provided dataset contains 100 rows and 7 columns:

`Date`, `Product`, `Quantity`, `Price`, `Customer_ID`, `Region`, and `Total_Sales`.

The data covers 2024-01-01 through 2024-04-09, with 5 products, 4 regions, and 100 customer IDs. The dataset represents individual sales transactions.

## 4. Technologies Used

- Python
- Pandas
- Seaborn
- Matplotlib
- Plotly
- Visual Studio Code
- Git and GitHub

## 5. Project Structure

```text
Task_6_Data_Visualization_Mastery_with_Seaborn/
├── dashboard.py
├── dashboard.html
├── dashboard.ipynb
├── sales_data.csv
├── requirements.txt
├── visualizations/
│   ├── sales_by_product.png
│   ├── sales_trend.png
│   ├── sales_by_region.png
│   ├── sales_distribution.png
│   └── correlation_heatmap.png
├── screenshots/
└── report/
    └── analysis_report.md
```

No fake screenshots or GIF were created. The dashboard HTML is the runnable interactive artifact.

## 6. Setup Instructions

```text
cd /d D:\Developer_Arena\Week1_Task\Task_6_Data_Visualization_Mastery_with_Seaborn
python -m pip install -r requirements.txt
python dashboard.py
```

Open `dashboard.html` in a browser.

## 7. Data Loading and Cleaning

`dashboard.py` loads the provided CSV with `pd.read_csv()`. It validates the file, required columns, empty input, dates, numeric values, missing values, negative values, and duplicate rows. The `Date` column is converted to Pandas datetime, and `Month` and `Month_Name` derived columns are created.

Observed data quality results:

- Shape: `(100, 7)` before derived columns.
- Missing values: `0`.
- Duplicate rows: `0`.
- Numeric columns loaded and validated successfully.

## 8. Data Analysis

Actual results:

- Total sales: `12,365,048`.
- Total quantity: `478`.
- Average sale: `123,650.48`.
- Products: `5`.
- Regions: `4`.
- Best-selling product by total sales: `Laptop`.

Sales by product:

| Product    | Total Sales |
| ---------- | ----------: |
| Laptop     |   3,889,210 |
| Tablet     |   2,884,340 |
| Phone      |   2,859,394 |
| Headphones |   1,384,033 |
| Monitor    |   1,348,071 |

Sales by region:

| Region | Total Sales |
| ------ | ----------: |
| North  |   3,983,635 |
| South  |   3,737,852 |
| East   |   2,519,639 |
| West   |   2,123,922 |

Monthly sales:

| Month   | Total Sales |
| ------- | ----------: |
| 2024-01 |   4,120,524 |
| 2024-02 |   2,656,050 |
| 2024-03 |   4,485,006 |
| 2024-04 |   1,103,468 |

April is a partial month because the data ends on April 9.

## 9. Visualization Explanation

1. **Sales by Product:** Seaborn bar chart comparing total revenue by product. Laptop is the leading product.
2. **Monthly Sales Trend:** Seaborn line chart showing monthly sales movement. March is the highest complete month.
3. **Sales by Region:** Seaborn bar chart comparing regional performance. North has the highest total.
4. **Sales Distribution:** Seaborn histogram with KDE showing the distribution of individual transaction values.
5. **Correlation Heatmap:** Seaborn heatmap comparing correlations between Quantity, Price, and Total_Sales.

## 10. Interactive Dashboard Explanation

The Plotly HTML dashboard contains Total Sales and Total Quantity KPI cards, an interactive monthly trend chart, separate interactive product and region charts, hover values, browser zoom/pan controls, and a dropdown that switches the trend between all products and individual products.

## 11. Key Insights

- Laptop generated the highest product sales at `3,889,210`.
- North generated the highest regional sales at `3,983,635`.
- March generated the highest complete monthly sales at `4,485,006`.
- April should not be compared as a full month because only April 1-9 is present.
- The dataset contains one transaction per customer ID, so customer-level analysis is limited to transaction-level customer identifiers rather than repeat-purchase behavior.

## 12. Error Handling and Validation

The program handles missing files, empty files, parse errors, missing required columns, invalid dates, invalid numeric values, missing values, negative numeric values, and duplicate rows. Errors are reported with a clear message instead of producing a dashboard from invalid data.

## 13. Testing

The complete command was tested:

```text
python -m py_compile dashboard.py
python dashboard.py
```

Verified results:

- The real CSV loaded successfully.
- Dataset validation completed.
- Date conversion completed.
- Sales calculations completed.
- Five Seaborn PNG charts were generated.
- The Plotly dashboard HTML was generated.
- No runtime errors occurred during the successful run.

## 14. Conclusion

The project provides a complete beginner-friendly visualization workflow. Seaborn supplies five distinct statistical charts, while Plotly provides an interactive dashboard for exploring monthly, product, and regional sales based on the actual dataset.
