"""Week 10 customer churn preprocessing and feature engineering pipeline."""

import pathlib
import typing
import typing_extensions

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
import sklearn.compose
import sklearn.impute
import sklearn.preprocessing
import sklearn.model_selection
import sklearn.pipeline


PROJECT_DIR: pathlib.Path = pathlib.Path(__file__).parent
DATA_FILE: pathlib.Path = PROJECT_DIR / "data" / "churn_data.csv"
CLEANED_FILE: pathlib.Path = PROJECT_DIR / "cleaned_data" / "cleaned_churn_data.csv"
VISUALIZATIONS_DIR: pathlib.Path = PROJECT_DIR / "visualizations"
RANDOM_STATE = 42
TARGET = "Churn"
BASE_NUMERIC: list[str] = ["Tenure", "MonthlyCharges", "TotalCharges", "SeniorCitizen"]
BASE_CATEGORICAL: list[str] = ["Contract", "PaymentMethod", "PaperlessBilling"]
REQUIRED_COLUMNS: set[str] = set(BASE_NUMERIC + BASE_CATEGORICAL + ["CustomerID", TARGET])


def load_data() -> pd.DataFrame:
    """Load and validate the supplied churn dataset."""
    if not DATA_FILE.exists():
        raise FileNotFoundError(f"Dataset not found: {DATA_FILE}")
    try:
        data: pd.DataFrame = pd.read_csv(DATA_FILE)
    except Exception:
        raise ValueError("The churn dataset could not be read or parsed.")
    missing: set[str] = REQUIRED_COLUMNS - set(data.columns)
    if missing:
        raise ValueError(f"Missing required columns: {', '.join(sorted(missing))}")
    if data.empty:
        raise ValueError("The churn dataset has no rows.")
    return data


def clean_data(data: pd.DataFrame) -> tuple[pd.DataFrame, dict[str, int]]:
    """Clean valid records and report quality findings without fabricating data."""
    quality: dict[str, int] = {
        "missing_before": int(data.isna().sum().sum()),
        "duplicates_before": int(data.duplicated().sum()),
    }
    cleaned: pd.DataFrame = data.copy()
    for column in BASE_NUMERIC + [TARGET]:
        cleaned[column] = pd.to_numeric(cleaned[column], errors="coerce")
    for column in BASE_CATEGORICAL + ["CustomerID"]:
        cleaned[column] = cleaned[column].astype("string").str.strip()
    if cleaned.isna().any().any():
        raise ValueError("Missing or invalid values remain after type conversion.")
    if not cleaned[TARGET].isin([0, 1]).all():
        raise ValueError("Churn must contain only 0 and 1.")
    cleaned: pd.DataFrame = cleaned.drop_duplicates().copy()
    quality["rows_removed"] = len(data) - len(cleaned)
    return cleaned, quality


def engineer_features(data: pd.DataFrame) -> tuple[pd.DataFrame, list[str]]:
    """Create business-supported features from customer columns only."""
    features: pd.DataFrame = data.copy()
    features["AverageMonthlySpending"] = features["TotalCharges"] / features["Tenure"].replace(0, np.nan)
    features["TotalChargesPerTenure"] = features["TotalCharges"] / features["Tenure"].replace(0, np.nan)
    features["MonthlyChargeCategory"] = pd.cut(
        features["MonthlyCharges"], bins=[-np.inf, 75, 150, np.inf], labels=["Low", "Medium", "High"]
    ).astype("string")
    features["TenureGroup"] = pd.cut(
        features["Tenure"], bins=[-np.inf, 12, 24, 48, np.inf], labels=["New", "Developing", "Established", "Loyal"]
    ).astype("string")
    features["IsLongTermContract"] = features["Contract"].isin(["One year", "Two year"]).astype(int)
    features["IsElectronicPayment"] = features["PaymentMethod"].eq("Electronic Check").astype(int)
    engineered: list[str] = [
        "AverageMonthlySpending", "TotalChargesPerTenure", "MonthlyChargeCategory",
        "TenureGroup", "IsLongTermContract", "IsElectronicPayment",
    ]
    features["AverageMonthlySpending"] = features["AverageMonthlySpending"].fillna(features["MonthlyCharges"])
    return features, engineered


def detect_outliers(data: pd.DataFrame) -> pd.DataFrame:
    """Flag IQR outliers and retain them because they may be valid customers."""
    result: pd.DataFrame = data.copy()
    for column in ["Tenure", "MonthlyCharges", "TotalCharges"]:
        q1, q3 = result[column].quantile([0.25, 0.75])
        iqr = q3 - q1
        result[f"{column}_IQR_Outlier"] = (result[column] < q1 - 1.5 * iqr) | (result[column] > q3 + 1.5 * iqr)
    result["Any_IQR_Outlier"] = result.filter(like="_IQR_Outlier").any(axis=1)
    return result


def build_pipeline(feature_data: pd.DataFrame) -> tuple[sklearn.compose.ColumnTransformer, list[str], list[str]]:
    """Build a leakage-safe ColumnTransformer for machine learning."""
    numeric: list[str] = BASE_NUMERIC + ["AverageMonthlySpending", "TotalChargesPerTenure", "IsLongTermContract", "IsElectronicPayment"]
    ordinal: list[str] = ["Contract"]
    categorical: list[str] = ["PaymentMethod", "PaperlessBilling", "MonthlyChargeCategory", "TenureGroup"]
    transformer = sklearn.compose.ColumnTransformer(
        transformers=[
            ("numeric", sklearn.pipeline.Pipeline([("imputer", sklearn.impute.SimpleImputer(strategy="median")), ("scaler", sklearn.preprocessing.StandardScaler())]), numeric),
            ("ordinal_contract", sklearn.pipeline.Pipeline([("imputer", sklearn.impute.SimpleImputer(strategy="most_frequent")), ("ordinal", sklearn.preprocessing.OrdinalEncoder(categories=[["Month-to-month", "One year", "Two year"]], handle_unknown="use_encoded_value", unknown_value=-1))]), ordinal),
            ("categorical", sklearn.pipeline.Pipeline([("imputer", sklearn.impute.SimpleImputer(strategy="most_frequent")), ("onehot", sklearn.preprocessing.OneHotEncoder(handle_unknown="ignore", sparse_output=False))]), categorical),
        ],
        remainder="drop",
    )
    return transformer, numeric, categorical


def compare_scalers(data: pd.DataFrame) -> dict[str, float]:
    """Compare StandardScaler and MinMaxScaler on the same numeric columns."""
    numeric: pd.DataFrame = data[["Tenure", "MonthlyCharges", "TotalCharges"]]
    standard = sklearn.preprocessing.StandardScaler().fit_transform(numeric)
    minimum = sklearn.preprocessing.MinMaxScaler().fit_transform(numeric)
    return {
        "standard_mean": float(standard[:, 0].mean()),
        "standard_std": float(standard[:, 0].std()),
        "minmax_min": float(minimum[:, 0].min()),
        "minmax_max": float(minimum[:, 0].max()),
    }


def create_visualizations(data: pd.DataFrame, outliers: pd.DataFrame) -> list[pathlib.Path]:
    """Generate required preprocessing and churn visualizations."""
    VISUALIZATIONS_DIR.mkdir(exist_ok=True)
    sns.set_theme(style="whitegrid")
    paths = []
    fig, axis = plt.subplots(figsize=(7, 5))
    sns.countplot(data=data, x="Churn", hue="Churn", legend=False, palette="Set2", ax=axis)
    axis.set_title("Churn Distribution")
    axis.set_xlabel("Churn (0 = No, 1 = Yes)")
    axis.set_ylabel("Customers")
    fig.tight_layout(); path: pathlib.Path = VISUALIZATIONS_DIR / "churn_distribution.png"; fig.savefig(path, dpi=150); plt.close(fig); paths.append(path)

    fig, axes = plt.subplots(1, 2, figsize=(13, 5))
    sns.histplot(data=data, x="Tenure", bins=12, kde=True, color="#2f6690", ax=axes[0])
    axes[0].set_title("Tenure Distribution")
    axes[0].set_xlabel("Tenure")
    sns.histplot(data=data, x="MonthlyCharges", bins=12, kde=True, color="#55a630", ax=axes[1])
    axes[1].set_title("Monthly Charges Distribution")
    axes[1].set_xlabel("Monthly Charges")
    fig.tight_layout(); path: pathlib.Path = VISUALIZATIONS_DIR / "feature_distribution.png"; fig.savefig(path, dpi=150); plt.close(fig); paths.append(path)

    numeric: pd.DataFrame = data[BASE_NUMERIC + ["Churn"]].corr()
    fig, axis = plt.subplots(figsize=(8, 6))
    sns.heatmap(numeric, annot=True, fmt=".2f", cmap="YlOrRd", ax=axis)
    axis.set_title("Correlation Heatmap")
    fig.tight_layout(); path: pathlib.Path = VISUALIZATIONS_DIR / "correlation_heatmap.png"; fig.savefig(path, dpi=150); plt.close(fig); paths.append(path)

    fig, axes = plt.subplots(1, 2, figsize=(13, 5))
    sns.boxplot(data=data, x="Churn", y="MonthlyCharges", hue="Churn", legend=False, palette="Set2", ax=axes[0])
    axes[0].set_title("Monthly Charges by Churn")
    sns.boxplot(data=data, x="Churn", y="TotalCharges", hue="Churn", legend=False, palette="Set3", ax=axes[1])
    axes[1].set_title("Total Charges by Churn")
    fig.tight_layout(); path: pathlib.Path = VISUALIZATIONS_DIR / "outlier_analysis.png"; fig.savefig(path, dpi=150); plt.close(fig); paths.append(path)
    return paths


def main() -> None:
    """Run inspection, cleaning, feature engineering, and pipeline preparation."""
    try:
        raw: pd.DataFrame = load_data()
        cleaned, quality = clean_data(raw)
        engineered, engineered_names = engineer_features(cleaned)
        outliers: pd.DataFrame = detect_outliers(engineered)
        features: pd.DataFrame = engineered.drop(columns=["CustomerID", TARGET])
        target_encoder = sklearn.preprocessing.LabelEncoder()
        y: typing_extensions.Buffer | np._SupportsArray[np.dtype[typing.Any]] | np._NestedSequence[np._SupportsArray[np.dtype[typing.Any]]] | bool | int | float | complex | str | bytes | np._NestedSequence[bool | int | float | complex | str | bytes] = target_encoder.fit_transform(engineered[TARGET])
        transformer, numeric, categorical = build_pipeline(features)
        x_train, x_test, y_train, y_test = sklearn.model_selection.train_test_split(features, y, test_size=0.2, random_state=RANDOM_STATE, stratify=y)
        pipeline = sklearn.pipeline.Pipeline([("preprocessor", transformer)])
        train_processed = pipeline.fit_transform(x_train)
        test_processed = pipeline.transform(x_test)
        full_processed = pipeline.transform(features)
        processed_columns = pipeline.named_steps["preprocessor"].get_feature_names_out()
        pd.DataFrame(full_processed, columns=processed_columns).assign(Churn=y).to_csv(PROJECT_DIR / "cleaned_data" / "processed_features.csv", index=False)
        engineered.drop(columns=["_unused"], errors="ignore").to_csv(CLEANED_FILE, index=False)
        chart_paths: list[pathlib.Path] = create_visualizations(cleaned, outliers)
        scaler_results: dict[str, float] = compare_scalers(cleaned)
        print("Customer churn preprocessing completed successfully.")
        print(f"Original dataset shape: {raw.shape}")
        print(f"Missing values before cleaning: {quality['missing_before']}")
        print(f"Duplicate count: {quality['duplicates_before']}")
        print(f"Cleaned dataset shape: {cleaned.shape}")
        print(f"Categorical feature count: {len(categorical)}")
        print(f"Numerical feature count: {len(numeric)}")
        print(f"Engineered feature count: {len(engineered_names)}")
        print(f"Final processed feature count: {train_processed.shape[1]}")
        print(f"Train/test sizes: {len(x_train)}/{len(x_test)}")
        print(f"IQR outlier rows flagged: {int(outliers['Any_IQR_Outlier'].sum())}; retained for analysis")
        print(f"StandardScaler Tenure mean/std: {scaler_results['standard_mean']:.2f}/{scaler_results['standard_std']:.2f}")
        print(f"MinMaxScaler Tenure min/max: {scaler_results['minmax_min']:.2f}/{scaler_results['minmax_max']:.2f}")
        print("LabelEncoder target classes:", target_encoder.classes_.tolist())
        print("OrdinalEncoder contract order: Month-to-month < One year < Two year")
        print("Generated visualizations:")
        for path in chart_paths:
            print(f"- {path.relative_to(PROJECT_DIR)}")
    except Exception:
        print("Preprocessing failed.")


if __name__ == "__main__":
    main()
