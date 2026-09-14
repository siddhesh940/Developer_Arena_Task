# Week 9: House Price Prediction

This project introduces machine learning concepts by predicting house prices from the supplied real estate dataset.

## Objectives

- Inspect and validate real housing data.
- Encode categorical features.
- Split data into training and testing sets.
- Implement linear regression from scratch.
- Compare it with scikit-learn Linear Regression.
- Evaluate predictions with MAE, MSE, and R2 Score.
- Interpret coefficients and visualize model behavior.

## Dataset

`data/house_prices.csv` contains 300 rows and 8 columns:

`Property_ID`, `Area`, `Bedrooms`, `Bathrooms`, `Age`, `Location`, `Property_Type`, and `Price`.

The dataset has no missing values and no duplicate rows. `Price` is the target variable.

## Technologies

- Python
- Pandas
- NumPy
- Matplotlib
- Seaborn
- scikit-learn
- Jupyter

## Setup

```text
cd /d D:\Developer_Arena\Week1_Task\Task_9_Machine_Learning_Concepts
py -m pip install -r requirements.txt
```

## Run

```text
py house_price_prediction.py
```

## Method

Numeric features are kept as numeric values. `Location` and `Property_Type` are one-hot encoded with Pandas. An 80/20 train-test split uses `random_state=42`. The scratch model uses the normal equation with a pseudo-inverse; the second model uses scikit-learn's `LinearRegression`.

## Evaluation

The script prints:

- MAE
- MSE
- R2 Score
- Training and testing sample counts
- Actual versus predicted examples
- Encoded feature coefficients

## Visualizations

- `area_vs_price.png`
- `predictions_vs_actual.png`
- `feature_analysis.png`

Screenshots are not fabricated. Capture actual execution and chart screenshots manually in `screenshots/`.
