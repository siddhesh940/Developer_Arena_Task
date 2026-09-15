# Week 11 - Advanced Machine Learning Models

## 1. Project Overview
This project segments the actual customer churn dataset and trains separate churn prediction models for each final segment.

## 2. Objectives
- Inspect and validate the source data.
- Compare K-Means, agglomerative hierarchical clustering, and DBSCAN.
- Profile the selected customer segments.
- Tune and evaluate a separate Random Forest model for each segment.
- Translate observed segment and model results into cautious business recommendations.

## 3. Dataset Description
- Rows: 500
- Columns: 9
- Columns: CustomerID, Tenure, MonthlyCharges, TotalCharges, Contract, PaymentMethod, PaperlessBilling, SeniorCitizen, Churn
- Data types: {'CustomerID': 'object', 'Tenure': 'int64', 'MonthlyCharges': 'int64', 'TotalCharges': 'int64', 'Contract': 'object', 'PaymentMethod': 'object', 'PaperlessBilling': 'object', 'SeniorCitizen': 'int64', 'Churn': 'int64'}
- Target: Churn (0 = retained, 1 = churned)

## 4. Data Exploration
- Missing values: {'CustomerID': 0, 'Tenure': 0, 'MonthlyCharges': 0, 'TotalCharges': 0, 'Contract': 0, 'PaymentMethod': 0, 'PaperlessBilling': 0, 'SeniorCitizen': 0, 'Churn': 0}
- Duplicate rows: 0
- Churn distribution: {0: 447, 1: 53} (10.60% churn)
- Contract distribution: {'One Year': 186, 'Month-To-Month': 170, 'Two Year': 144}
- Payment method distribution: {'Credit Card': 178, 'Electronic Check': 163, 'Bank Transfer': 159}
- Paperless billing distribution: {'No': 257, 'Yes': 243}
- Numerical statistics: {'Tenure': {'count': 500.0, 'mean': 36.53, 'std': 20.67, 'min': 1.0, '25%': 19.0, '50%': 37.0, '75%': 54.0, 'max': 71.0}, 'MonthlyCharges': {'count': 500.0, 'mean': 113.64, 'std': 51.8, 'min': 20.0, '25%': 67.0, '50%': 115.0, '75%': 158.0, 'max': 199.0}, 'TotalCharges': {'count': 500.0, 'mean': 4237.88, 'std': 2260.62, 'min': 159.0, '25%': 2237.25, '50%': 4182.5, '75%': 6266.75, 'max': 7992.0}, 'SeniorCitizen': {'count': 500.0, 'mean': 0.5, 'std': 0.5, 'min': 0.0, '25%': 0.0, '50%': 0.0, '75%': 1.0, 'max': 1.0}}

## 5. Data Preprocessing
Numeric columns were converted with pandas numeric coercion and median imputation is available in the modeling pipeline for any future missing values. Duplicate rows were removed if present. Categorical values were trimmed and title-cased. CustomerID was retained only for traceability and excluded from every feature matrix.

## 6. Feature Engineering
Clustering and prediction use Tenure, MonthlyCharges, TotalCharges, SeniorCitizen, Contract, PaymentMethod, and PaperlessBilling. Numeric features are standardized for distance-based clustering. Categorical features are one-hot encoded in the prediction pipeline with unknown-category handling.

## 7. Clustering Methodology
K-Means was evaluated for K=2 through K=8 using inertia and silhouette score. Agglomerative clustering with Ward linkage was compared at the selected K. DBSCAN tested a small grid of eps and min_samples values; configurations with noise or fewer than two meaningful clusters were excluded from silhouette comparison.

## 8. Optimal Cluster Selection
- Tested K values: [2, 3, 4, 5, 6, 7, 8]
- Inertia: [4989.708, 4486.758, 4134.152, 3762.74, 3467.209, 3300.333, 3151.239]
- Silhouette scores: [0.1653, 0.1913, 0.1604, 0.1916, 0.2174, 0.2077, 0.1997]
- Selected K-Means K: 6
- Hierarchical silhouette: 0.1664
- DBSCAN result: No configuration produced a meaningful non-noise solution.
K-Means was selected for the final labels because it had the strongest tested silhouette result and produced six interpretable, sufficiently sized groups for segment-specific modeling.

## 9. Cluster Profiles
The following profiles are generated directly from results/segment_profiles.csv.

### Segment 0: Higher-Value Premium Base
- Customers: 75 (15.00%)
- Average tenure: 37.13
- Average monthly charges: 122.71
- Average total charges: 4264.80
- Churn rate: 12.00%
- Senior citizen share: 44.00%
- Contract distribution: {"Month-To-Month": 29.33, "One Year": 45.33, "Two Year": 25.33}
- Payment distribution: {"Electronic Check": 100.0}
- Paperless billing distribution: {"Yes": 100.0}

### Segment 1: Established Customer Base 1
- Customers: 86 (17.20%)
- Average tenure: 36.71
- Average monthly charges: 112.20
- Average total charges: 4190.29
- Churn rate: 4.65%
- Senior citizen share: 50.00%
- Contract distribution: {"Month-To-Month": 26.74, "One Year": 44.19, "Two Year": 29.07}
- Payment distribution: {"Bank Transfer": 100.0}
- Paperless billing distribution: {"Yes": 100.0}

### Segment 2: Highest Churn Priority
- Customers: 97 (19.40%)
- Average tenure: 37.40
- Average monthly charges: 112.58
- Average total charges: 4490.11
- Churn rate: 19.59%
- Senior citizen share: 56.70%
- Contract distribution: {"Month-To-Month": 100.0}
- Payment distribution: {"Bank Transfer": 28.87, "Credit Card": 38.14, "Electronic Check": 32.99}
- Paperless billing distribution: {"No": 100.0}

### Segment 3: Lower-Charge Opportunity
- Customers: 82 (16.40%)
- Average tenure: 37.29
- Average monthly charges: 108.83
- Average total charges: 4357.30
- Churn rate: 17.07%
- Senior citizen share: 50.00%
- Contract distribution: {"Month-To-Month": 34.15, "One Year": 30.49, "Two Year": 35.37}
- Payment distribution: {"Credit Card": 100.0}
- Paperless billing distribution: {"Yes": 100.0}

### Segment 4: Lowest Churn Stability
- Customers: 89 (17.80%)
- Average tenure: 37.47
- Average monthly charges: 110.46
- Average total charges: 3761.88
- Churn rate: 2.25%
- Senior citizen share: 47.19%
- Contract distribution: {"One Year": 100.0}
- Payment distribution: {"Bank Transfer": 30.34, "Credit Card": 38.2, "Electronic Check": 31.46}
- Paperless billing distribution: {"No": 100.0}

### Segment 5: Established Customer Base 2
- Customers: 71 (14.20%)
- Average tenure: 32.44
- Average monthly charges: 116.77
- Average total charges: 4381.25
- Churn rate: 7.04%
- Senior citizen share: 49.30%
- Contract distribution: {"Two Year": 100.0}
- Payment distribution: {"Bank Transfer": 25.35, "Credit Card": 35.21, "Electronic Check": 39.44}
- Paperless billing distribution: {"No": 100.0}

## 10. Prediction Methodology
Churn is the binary target. Each segment is filtered independently, split 80/20 with random_state=42 and stratification, then modeled with a separate Random Forest pipeline. The preprocessor is fitted inside the training pipeline to prevent test-set transformation leakage.

## 11. Model Evaluation
| Segment | Accuracy | Precision | Recall | F1-score | ROC-AUC |
| --- | ---: | ---: | ---: | ---: | ---: |
| 0: Higher-Value Premium Base | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 |
| 1: Established Customer Base 1 | 0.9444 | 0.0000 | 0.0000 | 0.0000 | 1.0000 |
| 2: Highest Churn Priority | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 |
| 3: Lower-Charge Opportunity | 0.9412 | 1.0000 | 0.6667 | 0.8000 | 1.0000 |
| 4: Lowest Churn Stability | 0.9444 | 0.0000 | 0.0000 | 0.0000 | N/A |
| 5: Established Customer Base 2 | 0.9333 | 0.0000 | 0.0000 | 0.0000 | 0.7857 |

## 12. Hyperparameter Tuning
GridSearchCV optimized n_estimators, max_depth, min_samples_split, min_samples_leaf, and max_features using up to three stratified folds. Best parameters and confusion matrices are stored in results/model_evaluation_results.csv.

## 13. Feature Importance
- Segment 0 (Higher-Value Premium Base): ["num__Tenure", "num__TotalCharges", "num__MonthlyCharges", "cat__Contract_Two Year", "num__SeniorCitizen"]. These are predictive associations, not causal effects.
- Segment 1 (Established Customer Base 1): ["num__Tenure", "num__TotalCharges", "num__MonthlyCharges", "num__SeniorCitizen", "cat__Contract_One Year"]. These are predictive associations, not causal effects.
- Segment 2 (Highest Churn Priority): ["num__Tenure", "num__MonthlyCharges", "num__TotalCharges", "num__SeniorCitizen", "cat__PaymentMethod_Electronic Check"]. These are predictive associations, not causal effects.
- Segment 3 (Lower-Charge Opportunity): ["num__Tenure", "num__MonthlyCharges", "num__TotalCharges", "cat__Contract_Month-To-Month", "cat__Contract_One Year"]. These are predictive associations, not causal effects.
- Segment 4 (Lowest Churn Stability): ["num__Tenure", "num__TotalCharges", "num__MonthlyCharges", "num__SeniorCitizen", "cat__PaymentMethod_Credit Card"]. These are predictive associations, not causal effects.
- Segment 5 (Established Customer Base 2): ["num__Tenure", "num__MonthlyCharges", "num__TotalCharges", "cat__PaymentMethod_Bank Transfer", "num__SeniorCitizen"]. These are predictive associations, not causal effects.

## 14. Business Insights
- Highest observed churn: Segment 2 (Highest Churn Priority) at 19.59%.
- Highest average total charges: Segment 2 (Highest Churn Priority) at 4490.11; this is a value proxy, not customer lifetime value.
- Segment sizes and categorical distributions should be read together with churn rate; a small high-rate segment can still be operationally important.

## 15. Business Recommendations
- **Higher-Value Premium Base**: Use tailored engagement and monitor churn signals; preserve the segment's existing service experience.
- **Established Customer Base 1**: Use tailored engagement and monitor churn signals; preserve the segment's existing service experience.
- **Highest Churn Priority**: Prioritize targeted retention outreach and investigate contract, payment, and billing friction.
- **Lower-Charge Opportunity**: Use tailored engagement and monitor churn signals; preserve the segment's existing service experience.
- **Lowest Churn Stability**: Use tailored engagement and monitor churn signals; preserve the segment's existing service experience.
- **Established Customer Base 2**: Use tailored engagement and monitor churn signals; preserve the segment's existing service experience.

## 16. Model Limitations
The dataset has 500 rows and only 53 churn cases, so segment-level test metrics can be unstable. Some segments have few positive examples and ROC-AUC is reported only when both test classes are present. Clustering is sensitive to preprocessing and distance choices. Feature importance indicates model use, not causation, and performance on this sample may not generalize to future customers.

## 17. Testing
The executed script validated CSV loading, required columns, numeric conversion, missing values, duplicates, encoded/scaled features, K-Means inertia and silhouette scoring, hierarchical clustering, DBSCAN parameter search, cluster assignments, profiles, stratified splits, tuned segment models, predictions, classification metrics, feature importance, charts, CSV outputs, and report generation.

## 18. Visual Documentation
Charts in visualizations/ document the elbow curve, silhouette comparison, cluster distribution, profiles, PCA projection, hierarchical dendrogram, model comparison, and feature importance. The screenshots/ directory is intentionally left for manually captured evidence.

## 19. What I Learned
The workflow demonstrates how scaling affects distance-based clustering, how silhouette and inertia support K selection, how hierarchical clustering and DBSCAN provide alternative views, how PCA can visualize high-dimensional assignments, and why segment-specific model metrics and feature importance need careful interpretation under class imbalance.

## 20. Conclusion
The actual customer_churn.csv was inspected, transformed without using CustomerID as a feature, segmented with reproducible clustering, and used to train independent tuned Random Forest models for each final segment. Results and recommendations are evidence-based and preserved in the generated CSV files and charts.