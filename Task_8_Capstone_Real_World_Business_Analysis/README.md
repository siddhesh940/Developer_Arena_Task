# Week 8 Capstone: Real World Business Analysis

This portfolio-ready capstone analyzes three actual business datasets for The Developers Arena internship: sales performance, customer churn, and property pricing.

## Business Problem

The project answers how a business can improve revenue performance, reduce customer churn, and make better property pricing decisions using evidence from real data.

## Objectives

- Prepare and validate raw business data.
- Perform EDA, descriptive statistics, group comparisons, correlation, regression, and trend analysis.
- Create five professional visualizations.
- Translate findings into recommendations and a 90-day implementation plan.

## Datasets

- `house_prices.csv`: 300 rows, 8 columns.
- `customer_churn.csv`: 500 rows, 9 columns.
- `sales_data.csv`: 100 rows, 7 columns.

All source datasets had zero missing values and zero duplicate records. The datasets are analyzed independently because they have no common business key.

## Technologies

Python, Pandas, NumPy, SciPy, Seaborn, Matplotlib, scikit-learn, ReportLab, python-pptx, and Jupyter.

## Setup and Run

```text
cd /d D:\Developer_Arena\Week1_Task\Task_8_Capstone_Real_World_Business_Analysis
py -m pip install -r requirements.txt
py capstone_analysis.py
```

The script generates cleaned CSVs, five charts, an executive PDF, a technical PDF, and a PowerPoint presentation.

## Main Findings

- Laptop leads sales products and North leads sales regions.
- Month-to-month churn is the highest observed contract segment.
- City Center has the highest mean property price.
- Property area has a strong positive correlation with price (`r=0.796`).
- April sales are partial because the sales data ends on April 9.

## Structure

```text
Task_8_Capstone_Real_World_Business_Analysis/
├── capstone_analysis.py
├── capstone_analysis.ipynb
├── data/
├── cleaned_data/
├── visualizations/
├── reports/
├── presentation/
└── screenshots/
```

Screenshots are not fabricated; capture them manually after running the project.
