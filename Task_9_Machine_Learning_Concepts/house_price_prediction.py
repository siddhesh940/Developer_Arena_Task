"""Week 9 house price prediction with scratch and scikit-learn regression."""

import pathlib

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
import sklearn.linear_model
import sklearn.metrics
import sklearn.model_selection


PROJECT_DIR: pathlib.Path = pathlib.Path(__file__).parent
DATA_FILE: pathlib.Path = PROJECT_DIR / "data" / "house_prices.csv"
VISUALIZATIONS_DIR: pathlib.Path = PROJECT_DIR / "visualizations"
RANDOM_STATE = 42
FEATURE_COLUMNS: list[str] = ["Area", "Bedrooms", "Bathrooms", "Age", "Location", "Property_Type"]
NUMERIC_FEATURES: list[str] = ["Area", "Bedrooms", "Bathrooms", "Age"]
CATEGORICAL_FEATURES: list[str] = ["Location", "Property_Type"]


def load_and_validate_data() -> pd.DataFrame:
    """Load the real dataset and validate its required structure."""
    if not DATA_FILE.exists():
        raise FileNotFoundError(f"Dataset not found: {DATA_FILE}")
    try:
        data: pd.DataFrame = pd.read_csv(DATA_FILE)
    except Exception:
        raise ValueError("The house prices CSV could not be read or parsed.")

    required_columns: set[str] = set(FEATURE_COLUMNS + ["Property_ID", "Price"])
    missing_columns: set[str] = required_columns - set(data.columns)
    if missing_columns:
        raise ValueError(f"Missing required columns: {', '.join(sorted(missing_columns))}")
    if data.empty:
        raise ValueError("The house prices dataset has no rows.")
    if data.isna().any().any():
        raise ValueError("The dataset contains missing values.")
    if data.duplicated().any():
        raise ValueError("The dataset contains duplicate rows.")

    for column in NUMERIC_FEATURES + ["Price"]:
        data[column] = pd.to_numeric(data[column], errors="coerce")
    if data[NUMERIC_FEATURES + ["Price"]].isna().any().any():
        raise ValueError("The dataset contains invalid numeric values.")
    if (data[NUMERIC_FEATURES + ["Price"]] < 0).any().any():
        raise ValueError("Numeric values cannot be negative.")
    return data


def prepare_features(data: pd.DataFrame) -> tuple[pd.DataFrame, pd.Series]:
    """Encode categorical features and separate X from the Price target."""
    features: pd.DataFrame = pd.get_dummies(data[FEATURE_COLUMNS], columns=CATEGORICAL_FEATURES, dtype=float)
    target: pd.Series = data["Price"].astype(float)
    return features, target


def fit_scratch_linear_regression(x_train: np.ndarray, y_train: np.ndarray) -> np.ndarray:
    """Fit linear regression with the normal equation beta=(X'X)^-1 X'y."""
    x_with_intercept: np.ndarray[tuple[int, ...], np.dtype[np.float64]] = np.column_stack([np.ones(len(x_train)), x_train])
    # Pseudo-inverse is numerically safer than a direct matrix inverse.
    coefficients = np.linalg.pinv(x_with_intercept.T @ x_with_intercept) @ x_with_intercept.T @ y_train
    return coefficients


def predict_scratch(coefficients: np.ndarray, x_values: np.ndarray) -> np.ndarray:
    """Generate predictions from scratch-model coefficients."""
    x_with_intercept: np.ndarray[tuple[int, ...], np.dtype[np.float64]] = np.column_stack([np.ones(len(x_values)), x_values])
    return x_with_intercept @ coefficients


def create_visualizations(data: pd.DataFrame, y_test: pd.Series, predictions: np.ndarray) -> list[pathlib.Path]:
    """Save the required actual-vs-predicted and feature relationship charts."""
    VISUALIZATIONS_DIR.mkdir(exist_ok=True)
    sns.set_theme(style="whitegrid")
    paths = []

    fig, axis = plt.subplots(figsize=(9, 5))
    sns.scatterplot(data=data, x="Area", y="Price", hue="Location", alpha=0.75, ax=axis)
    axis.set_title("Area vs House Price")
    axis.set_xlabel("Area")
    axis.set_ylabel("Price")
    fig.tight_layout()
    path: pathlib.Path = VISUALIZATIONS_DIR / "area_vs_price.png"
    fig.savefig(path, dpi=150)
    plt.close(fig)
    paths.append(path)

    fig, axis = plt.subplots(figsize=(8, 6))
    sns.scatterplot(x=y_test, y=predictions, color="#2f6690", ax=axis)
    minimum: float = min(float(y_test.min()), float(predictions.min()))
    maximum: float = max(float(y_test.max()), float(predictions.max()))
    axis.plot([minimum, maximum], [minimum, maximum], "--", color="#c0392b", label="Perfect prediction")
    axis.set_title("Actual vs Predicted House Prices")
    axis.set_xlabel("Actual Price")
    axis.set_ylabel("Predicted Price")
    axis.legend()
    fig.tight_layout()
    path: pathlib.Path = VISUALIZATIONS_DIR / "predictions_vs_actual.png"
    fig.savefig(path, dpi=150)
    plt.close(fig)
    paths.append(path)

    numeric: pd.Series = data[NUMERIC_FEATURES + ["Price"]].corr()["Price"].drop("Price").sort_values()
    fig, axis = plt.subplots(figsize=(8, 5))
    sns.barplot(x=numeric.values, y=numeric.index, hue=numeric.index, legend=False, palette="viridis", ax=axis)
    axis.set_title("Numeric Feature Correlation with Price")
    axis.set_xlabel("Correlation with Price")
    axis.set_ylabel("Feature")
    fig.tight_layout()
    path: pathlib.Path = VISUALIZATIONS_DIR / "feature_analysis.png"
    fig.savefig(path, dpi=150)
    plt.close(fig)
    paths.append(path)
    return paths


def evaluate_model(y_true: pd.Series, predictions: np.ndarray) -> dict[str, float]:
    """Calculate the required regression evaluation metrics."""
    return {
        "mae": sklearn.metrics.mean_absolute_error(y_true, predictions),
        "mse": sklearn.metrics.mean_squared_error(y_true, predictions),
        "r2": sklearn.metrics.r2_score(y_true, predictions),
    }


def main() -> None:
    """Run the complete reproducible prediction workflow."""
    try:
        data: pd.DataFrame = load_and_validate_data()
        features, target = prepare_features(data)
        x_train, x_test, y_train, y_test = sklearn.model_selection.train_test_split(
            features, target, test_size=0.2, random_state=RANDOM_STATE
        )

        scratch_coefficients = fit_scratch_linear_regression(x_train.to_numpy(), y_train.to_numpy())
        scratch_predictions = predict_scratch(scratch_coefficients, x_test.to_numpy())
        sklearn_model: sklearn.linear_model.LinearRegression = sklearn.linear_model.LinearRegression().fit(x_train, y_train)
        sklearn_predictions = sklearn_model.predict(x_test)
        metrics: dict[str, float] = evaluate_model(y_test, sklearn_predictions)
        scratch_metrics: dict[str, float] = evaluate_model(y_test, scratch_predictions)
        chart_paths: list[pathlib.Path] = create_visualizations(data, y_test, sklearn_predictions)

        coefficient_table = pd.DataFrame({"Feature": features.columns, "Coefficient": sklearn_model.coef_})
        coefficient_table["Absolute_Impact"] = coefficient_table["Coefficient"].abs()
        coefficient_table: pd.DataFrame = coefficient_table.sort_values("Absolute_Impact", ascending=False)

        print("House price prediction completed successfully.")
        print(f"Dataset shape: {data.shape}")
        print(f"Training samples: {len(x_train)}")
        print(f"Testing samples: {len(x_test)}")
        print("\nScikit-learn Linear Regression metrics:")
        print(f"MAE: {metrics['mae']:,.2f}")
        print(f"MSE: {metrics['mse']:,.2f}")
        print(f"R2 Score: {metrics['r2']:.4f}")
        print("\nScratch Linear Regression metrics:")
        print(f"MAE: {scratch_metrics['mae']:,.2f}")
        print(f"MSE: {scratch_metrics['mse']:,.2f}")
        print(f"R2 Score: {scratch_metrics['r2']:.4f}")
        print("\nActual vs predicted examples:")
        print(pd.DataFrame({"Actual": y_test.values[:5], "Predicted": sklearn_predictions[:5]}).to_string(index=False))
        print("\nMost influential encoded features:")
        print(coefficient_table.head(8)[["Feature", "Coefficient"]].to_string(index=False))
        print("\nGenerated visualizations:")
        for path in chart_paths:
            print(f"- {path.relative_to(PROJECT_DIR)}")
    except Exception:
        print("Analysis failed.")


if __name__ == "__main__":
    main()
