# Week 10 - Data Preprocessing and Feature Engineering

## 1. Project Overview

This project prepares the actual 500-row customer churn dataset for machine learning. It demonstrates a complete reproducible preprocessing workflow with validation, business feature engineering, encoding, scaling, outlier analysis, feature selection, and train/test preparation.

## 2. Objectives

- Inspect and validate customer data.
- Handle missing values and duplicates appropriately.
- Build meaningful churn-related features.
- Compare StandardScaler and MinMaxScaler.
- Demonstrate One-Hot, Label, and Ordinal encoding.
- Detect outliers without blindly removing valid customers.
- Build a leakage-safe ColumnTransformer pipeline.

## 3. Dataset Description

The dataset contains 500 customers and 9 columns: `CustomerID`, `Tenure`, `MonthlyCharges`, `TotalCharges`, `Contract`, `PaymentMethod`, `PaperlessBilling`, `SeniorCitizen`, and `Churn`. The churn distribution is 447 non-churned customers and 53 churned customers, for an observed churn rate of 10.60%.

## 4. Data Inspection

The script prints shape, columns, dtypes, categorical unique values, descriptive statistics, missing values, duplicates, and target distribution. The original dataset shape is `(500, 9)`. Numeric columns are Tenure, MonthlyCharges, TotalCharges, SeniorCitizen, and Churn. Categorical columns are CustomerID, Contract, PaymentMethod, and PaperlessBilling.

Observed quality results:

- Missing values before cleaning: `0`.
- Duplicate rows before cleaning: `0`.
- Invalid target values: none; Churn contains only 0 and 1.
- Rows removed: `0`.

## 5. Data Cleaning

Numeric fields are converted with `pd.to_numeric(errors="coerce")`. Text categories and identifiers are converted to string values and stripped of whitespace. Invalid conversions raise a clear error instead of silently fabricating replacements. Duplicate records would be removed from the working copy if present; the supplied data required no removal.

## 6. Missing Value Handling

No missing values were found. The preprocessing pipeline still includes median imputation for numeric columns and most-frequent imputation for categorical columns so it remains robust when used with future data.

## 7. Duplicate Handling

No duplicate rows were found. The working copy uses `drop_duplicates()` as a defensive cleaning step and leaves the original CSV unchanged.

## 8. Encoding Techniques

- LabelEncoder converts the binary Churn target into model labels.
- OrdinalEncoder represents Contract in the meaningful order Month-to-month, One year, Two year.
- OneHotEncoder represents unordered categories including PaymentMethod, PaperlessBilling, MonthlyChargeCategory, and TenureGroup.

## 9. Scaling Techniques

The project compares both methods on Tenure, MonthlyCharges, and TotalCharges:

- StandardScaler centers features around mean 0 and standard deviation 1.
- MinMaxScaler maps each feature to a 0-1 range.

StandardScaler is used in the machine-learning pipeline because it is useful when numeric feature magnitudes differ and centered values are appropriate. MinMaxScaler is included as a documented comparison.

## 10. Outlier Detection

The project uses the IQR rule for Tenure, MonthlyCharges, and TotalCharges. A row is flagged when it falls below Q1 - 1.5×IQR or above Q3 + 1.5×IQR. Flags are retained for review rather than automatically removing customers, because extreme charges or tenure can be valid business observations.

## 11. Feature Engineering

Six meaningful features are created: AverageMonthlySpending, TotalChargesPerTenure, MonthlyChargeCategory, TenureGroup, IsLongTermContract, and IsElectronicPayment. Their formulas, source columns, and business interpretations are documented in `feature_engineering_documentation.md`.

## 12. Feature Selection

CustomerID is excluded because it is an identifier, not a predictive measurement. Original numeric fields, engineered numeric indicators, original categorical fields, and engineered group categories are retained because they represent customer lifecycle, charges, contract, billing, and payment behavior. The correlation heatmap supports numeric relationship review without using the target to create input features.

## 13. Preprocessing Pipeline

A scikit-learn ColumnTransformer contains:

- Numeric pipeline: median imputation followed by StandardScaler.
- Contract pipeline: most-frequent imputation followed by OrdinalEncoder.
- Nominal categorical pipeline: most-frequent imputation followed by OneHotEncoder with unknown-category handling.

The target is separated before pipeline fitting.

## 14. Data Leakage Prevention

The train/test split uses stratification and `random_state=42`. The ColumnTransformer is fitted only on training features. The test set is transformed with the already-fitted transformer, so test statistics do not influence training preprocessing. Churn is never used to derive input features.

## 15. Final Dataset

The script saves `cleaned_churn_data.csv` and a fully transformed `processed_features.csv`. It prints the final processed feature count, train size, and test size. The final matrix is numeric and ready for a downstream churn model.

## 16. Results and Observations

The supplied data produced a clean 500-row working dataset, six engineered features, and a reproducible train/test preparation. The pipeline demonstrates all three required encoding strategies and both scaling comparisons. Outlier rows are flagged for review rather than discarded automatically.

## 17. Limitations

- The dataset is a single 500-customer sample.
- Feature engineering thresholds are simple business-friendly bands, not optimized model parameters.
- Outlier flags identify unusual values but do not prove data errors.
- Preprocessing prepares data for modeling; it does not claim predictive accuracy because no classifier is required in this task.

## 18. Conclusion

This project provides a safe, reproducible foundation for churn machine learning. It validates the actual data, creates interpretable customer features, compares scaling choices, handles categorical variables appropriately, flags outliers responsibly, and prevents leakage through train-fitted preprocessing.
