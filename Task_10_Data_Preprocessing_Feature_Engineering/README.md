# Week 10: Data Preprocessing and Feature Engineering

This project prepares the actual customer churn dataset for machine learning. It demonstrates inspection, cleaning, feature engineering, encoding, scaling, outlier analysis, feature selection, and a leakage-safe scikit-learn preprocessing pipeline.

## Dataset

`data/churn_data.csv` contains 500 rows and 9 columns: customer ID, tenure, charges, contract, payment method, billing preference, senior-citizen status, and churn target. The supplied dataset has no missing values and no duplicate rows.

## Technologies

Python, Pandas, NumPy, Matplotlib, Seaborn, scikit-learn, and Jupyter.

## Setup

```text
cd /d D:\Developer_Arena\Week1_Task\Task_10_Data_Preprocessing_Feature_Engineering
py -m pip install -r requirements.txt
```

## Run

```text
py churn_prediction_pipeline.py
```

## Workflow

1. Inspect dataset shape, types, categories, statistics, missing values, duplicates, and churn distribution.
2. Validate numeric and target values and remove duplicate records only if present.
3. Engineer six features: AverageMonthlySpending, TotalChargesPerTenure, MonthlyChargeCategory, TenureGroup, IsLongTermContract, and IsElectronicPayment.
4. Apply LabelEncoder to the binary Churn target, OrdinalEncoder to ordered Contract categories, and OneHotEncoder to unordered categorical fields.
5. Compare StandardScaler and MinMaxScaler.
6. Flag IQR outliers without deleting potentially valid customers.
7. Fit the preprocessing pipeline only on training features, then transform test and full data.

## Outputs

- `cleaned_data/cleaned_churn_data.csv`
- `cleaned_data/processed_features.csv`
- `visualizations/churn_distribution.png`
- `visualizations/feature_distribution.png`
- `visualizations/correlation_heatmap.png`
- `visualizations/outlier_analysis.png`
- Detailed reports under `report/`

Screenshots are not fabricated; capture successful execution and charts manually in `screenshots/`.
