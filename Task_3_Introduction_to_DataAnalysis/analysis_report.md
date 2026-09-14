# Sales Data Analysis Report

## 1. Project Overview

This is the Week 3 internship project for The Developers Arena. It focuses on analyzing the provided real sales dataset using Python and Pandas.

## 2. Objectives

- Load a CSV dataset.
- Explore the dataset.
- Understand rows and columns.
- Inspect data types.
- Check data quality.
- Handle missing values.
- Handle duplicates.
- Calculate sales metrics.
- Identify useful business insights.

## 3. Dataset Description

The analysis uses the provided `sales_data.csv` file. It contains 100 sales records and 7 columns covering dates, products, quantities, prices, customer IDs, regions, and calculated sale amounts.

- **Number of rows:** 100
- **Number of columns:** 7
- **Columns:** `Date`, `Product`, `Quantity`, `Price`, `Customer_ID`, `Region`, `Total_Sales`
- **Date range:** 2024-01-01 to 2024-04-09
- **Products:** Phone, Headphones, Laptop, Tablet, and Monitor
- **Regions:** East, North, West, and South
- **Important fields:** `Quantity`, `Price`, and `Total_Sales` support the sales calculations; `Product` and `Region` support grouped analysis.

The source CSV was copied into this project folder without changing its contents.

## 4. Technologies Used

- Python 3.x
- Pandas
- Visual Studio Code
- Git
- GitHub

## 5. Setup Instructions

1. Install Python 3.x.
2. Open the project folder in VS Code.
3. Install the dependency:

```text
pip install -r requirements.txt
```

4. Run the analysis:

```text
python sales_analysis.py
```

## 6. Project Structure

```text
Task_3_Introduction_to_DataAnalysis/
├── sales_analysis.py
├── sales_data.csv
├── analysis_report.md
└── requirements.txt
```

## 7. Data Loading

The script imports Pandas and loads the provided file with:

```python
sales_data = pd.read_csv(DATA_FILE)
```

The path is resolved relative to the script, so the analysis can be run from the project folder or the repository root.

## 8. Data Exploration

### First 5 rows

| Date       | Product    | Quantity | Price | Customer_ID | Region | Total_Sales |
| ---------- | ---------- | -------: | ----: | ----------- | ------ | ----------: |
| 2024-01-01 | Phone      |        7 | 37300 | CUST001     | East   |      261100 |
| 2024-01-02 | Headphones |        4 | 15406 | CUST002     | North  |       61624 |
| 2024-01-03 | Phone      |        2 | 21746 | CUST003     | West   |       43492 |
| 2024-01-04 | Headphones |        1 | 30895 | CUST004     | East   |       30895 |
| 2024-01-05 | Laptop     |        8 | 39835 | CUST005     | North  |      318680 |

### Shape and columns

- **Shape:** `(100, 7)`
- **Columns:** `Date`, `Product`, `Quantity`, `Price`, `Customer_ID`, `Region`, `Total_Sales`

### Data types

| Column      | Data type |
| ----------- | --------- |
| Date        | object    |
| Product     | object    |
| Quantity    | int64     |
| Price       | int64     |
| Customer_ID | object    |
| Region      | object    |
| Total_Sales | int64     |

### Basic statistics

| Statistic | Quantity |     Price | Total_Sales |
| --------- | -------: | --------: | ----------: |
| Count     |      100 |       100 |         100 |
| Mean      |     4.78 | 25,808.51 |  123,650.48 |
| Minimum   |        1 |     1,308 |       6,540 |
| 25%       |     2.75 | 14,965.25 |   39,517.50 |
| Median    |     5.00 |    24,192 |   97,955.50 |
| 75%       |     7.00 | 38,682.25 |  175,792.50 |
| Maximum   |        9 |    49,930 |     373,932 |

## 9. Data Cleaning

- **Missing values:** 0 missing values were found in every column. No missing-value cleaning was needed.
- **Duplicate rows:** 0 duplicate rows were found. No duplicate records were removed.
- **Numeric values:** `Quantity`, `Price`, and `Total_Sales` loaded as `int64`. The script checks these columns with numeric conversion and would remove rows that contained invalid numeric values.
- **Cleaning approach:** The script works on an in-memory copy and never overwrites the provided CSV. Because this dataset is complete and has no duplicates or invalid numeric values, the analyzed data remains unchanged.

## 10. Sales Analysis

### Overall metrics

| Metric                |        Result |
| --------------------- | ------------: |
| Total Sales / Revenue | 12,365,048.00 |
| Average Sales         |    123,650.48 |
| Maximum Sale          |    373,932.00 |
| Minimum Sale          |      6,540.00 |
| Total Quantity Sold   |           478 |
| Unique Products       |             5 |
| Unique Customers      |           100 |

### Best-selling product

**Laptop** was the best-selling product by total sales, generating **3,889,210**.

### Sales by product

| Product    | Total Sales |
| ---------- | ----------: |
| Laptop     |   3,889,210 |
| Tablet     |   2,884,340 |
| Phone      |   2,859,394 |
| Headphones |   1,384,033 |
| Monitor    |   1,348,071 |

### Sales by region

| Region | Total Sales |
| ------ | ----------: |
| North  |   3,983,635 |
| South  |   3,737,852 |
| East   |   2,519,639 |
| West   |   2,123,922 |

## 11. Key Findings / Insights

- Total revenue across the 100 records was **12,365,048.00**.
- **Laptop** generated the highest product sales at **3,889,210**.
- **North** generated the highest regional sales at **3,983,635**.
- The average sale was **123,650.48**, while individual sales ranged from **6,540.00** to **373,932.00**.
- Monitor and Headphones had the lowest product totals, so their performance may need attention compared with the other products.

## 12. Technical Requirements Fulfilled

- Pandas loads and analyzes the provided CSV using `pd.read_csv()`.
- The script displays the first five rows, dataset information, shape, columns, data types, and descriptive statistics.
- Missing values and duplicate rows are checked and reported.
- Conditional in-memory cleaning handles invalid numeric values, missing values, and duplicates if they occur.
- More than three meaningful metrics are calculated, including total, average, minimum, maximum, and quantity.
- Best-selling product, sales by product, and sales by region are calculated.
- Comments explain the loading and cleaning steps.
- A clean Markdown analysis report documents the actual results.

## 13. Testing

The command below was executed successfully on 2026-09-14:

```text
python Task_3_Introduction_to_DataAnalysis\sales_analysis.py
```

Observed results:

- The first five rows printed successfully.
- Dataset shape printed as `(100, 7)`.
- All seven column names and their data types printed successfully.
- Total missing values printed as `0`.
- Duplicate rows printed as `0`.
- The script reported that no missing values or duplicate rows required cleaning.
- Total sales printed as `12,365,048.00`.
- Best-selling product printed as `Laptop`.
- Product and regional sales summaries printed successfully.
- The script exited without errors.

## 14. Visual Documentation

Screenshots are not included yet. Add them manually in the project documentation or repository as needed.

Recommended screenshots:

1. CSV dataset opened in VS Code.
2. Terminal showing successful script execution.
3. Dataset exploration output.
4. Missing-value and duplicate check.
5. Final sales analysis results.

[INSERT SCREENSHOT HERE]

[INSERT SCREENSHOT HERE]

[INSERT SCREENSHOT HERE]

## 15. What I Learned

This project demonstrated how to use Pandas with CSV files, explore rows and columns, inspect data types, check missing values and duplicates, perform basic cleaning, calculate descriptive statistics, group data for comparisons, and turn data into business insights.

## 16. Conclusion

The Sales Data Analysis project successfully analyzed the provided 100-row sales dataset with Python and Pandas. It produced verified revenue, product, regional, quantity, customer, and data-quality results without modifying the original CSV.
