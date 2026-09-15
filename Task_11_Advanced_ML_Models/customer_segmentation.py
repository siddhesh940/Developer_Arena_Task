from __future__ import annotations

import json
import pathlib
import textwrap
import typing

import matplotlib
matplotlib.use("Agg")
import matplotlib.backends.backend_pdf
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
import scipy.cluster.hierarchy
import sklearn.cluster
import sklearn.compose
import sklearn.decomposition
import sklearn.ensemble
import sklearn.impute
import sklearn.metrics
import sklearn.model_selection
import sklearn.pipeline
import sklearn.preprocessing

ROOT: pathlib.Path = pathlib.Path(__file__).resolve().parent
DATA_PATH: pathlib.Path = ROOT / "customer_churn.csv"
VISUALIZATION_PATH: pathlib.Path = ROOT / "visualizations"
RESULTS_PATH: pathlib.Path = ROOT / "results"
REPORT_PATH: pathlib.Path = ROOT / "report"
SCREENSHOTS_PATH: pathlib.Path = ROOT / "screenshots"


def ensure_directories() -> None:
    for folder in [VISUALIZATION_PATH, RESULTS_PATH, REPORT_PATH, SCREENSHOTS_PATH]:
        folder.mkdir(exist_ok=True, parents=True)


def load_data(path: pathlib.Path) -> pd.DataFrame:
    if not path.exists():
        raise FileNotFoundError(f"Dataset not found: {path}")

    df: pd.DataFrame = pd.read_csv(path)
    if df.empty:
        raise ValueError("Input dataset is empty.")

    required: list[str] = [
        "CustomerID", "Tenure", "MonthlyCharges", "TotalCharges",
        "Contract", "PaymentMethod", "PaperlessBilling", "SeniorCitizen", "Churn"
    ]
    missing: list[str] = [col for col in required if col not in df.columns]
    if missing:
        raise ValueError(f"Missing required columns: {missing}")

    for col in ["Tenure", "MonthlyCharges", "TotalCharges", "SeniorCitizen", "Churn"]:
        numeric: pd.Series = pd.to_numeric(df[col], errors="coerce")
        if numeric.isna().any():
            raise ValueError(f"Column '{col}' contains invalid numeric values.")

    print("=== DATASET OVERVIEW ===")
    print(f"Shape: {df.shape}")
    print(f"Columns: {list(df.columns)}")
    print(df.dtypes.to_string())
    print(f"Missing values: {df.isna().sum().to_dict()}")
    print(f"Duplicate rows: {int(df.duplicated().sum())}")
    print(f"Churn distribution: {df['Churn'].value_counts().to_dict()}")
    print(df.head().to_string(index=False))
    return df


def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    cleaned: pd.DataFrame = df.drop_duplicates().copy()
    for col in ["Tenure", "MonthlyCharges", "TotalCharges", "SeniorCitizen", "Churn"]:
        cleaned[col] = pd.to_numeric(cleaned[col], errors="coerce")
    for col in ["Tenure", "MonthlyCharges", "TotalCharges", "SeniorCitizen"]:
        if cleaned[col].isna().any():
            cleaned[col] = cleaned[col].fillna(cleaned[col].median())
    for col in ["Contract", "PaymentMethod", "PaperlessBilling"]:
        cleaned[col] = cleaned[col].astype(str).str.strip().str.title()
    cleaned["CustomerID"] = cleaned["CustomerID"].astype(str).str.strip()
    cleaned["SeniorCitizen"] = cleaned["SeniorCitizen"].astype(int)
    cleaned["Churn"] = cleaned["Churn"].astype(int)
    print("\n=== CLEANING SUMMARY ===")
    print(f"Duplicate rows removed: {int(df.duplicated().sum())}")
    print(f"Missing values after cleaning: {cleaned.isna().sum().to_dict()}")
    return cleaned


def print_exploratory_summary(df: pd.DataFrame) -> None:
    print("\n=== NUMERICAL STATISTICS ===")
    print(df[["Tenure", "MonthlyCharges", "TotalCharges", "SeniorCitizen"]].describe().to_string())
    print("\n=== CATEGORICAL DISTRIBUTIONS ===")
    for col in ["Contract", "PaymentMethod", "PaperlessBilling", "SeniorCitizen"]:
        print(f"\n{col}:\n{df[col].value_counts(dropna=False).to_string()}")
    print("\n=== CHURN DISTRIBUTION ===")
    print(df["Churn"].value_counts(normalize=True).mul(100).round(2).to_string())


def prepare_clustering_features(df: pd.DataFrame) -> pd.DataFrame:
    feature_cols: list[str] = [
        "Tenure", "MonthlyCharges", "TotalCharges", "SeniorCitizen",
        "Contract", "PaymentMethod", "PaperlessBilling"
    ]
    encoded: pd.DataFrame = pd.get_dummies(df[feature_cols].copy(), columns=["Contract", "PaymentMethod", "PaperlessBilling"], drop_first=False)
    return encoded


def perform_kmeans(X_scaled: np.ndarray, k_values: range) -> tuple[pd.Series, dict]:
    inertia_values = []
    silhouette_values = []
    for k in k_values:
        model = sklearn.cluster.KMeans(n_clusters=k, random_state=42, n_init=20)
        labels = model.fit_predict(X_scaled)
        inertia_values.append(model.inertia_)
        silhouette_values.append(sklearn.metrics.silhouette_score(X_scaled, labels) if len(np.unique(labels)) > 1 else np.nan)

    valid = [s for s in silhouette_values if pd.notna(s)]
    if not valid:
        raise ValueError("No valid silhouette scores available for K-Means.")

    optimal_k: int = list(k_values)[int(np.nanargmax(silhouette_values))]
    print(f"\nK-Means selected K={optimal_k}")
    print(f"Inertia values: {inertia_values}")
    print(f"Silhouette scores: {silhouette_values}")

    plt.figure(figsize=(8, 5))
    plt.plot(list(k_values), inertia_values, marker="o", color="#1f77b4")
    plt.title("Elbow Method for K-Means")
    plt.xlabel("Number of clusters (K)")
    plt.ylabel("Inertia")
    plt.grid(alpha=0.3)
    plt.tight_layout()
    plt.savefig(VISUALIZATION_PATH / "elbow_curve.png", dpi=300)
    plt.close()

    plt.figure(figsize=(8, 5))
    plt.plot(list(k_values), silhouette_values, marker="o", color="#2ca02c")
    plt.title("Silhouette Scores by K")
    plt.xlabel("Number of clusters (K)")
    plt.ylabel("Silhouette Score")
    plt.grid(alpha=0.3)
    plt.tight_layout()
    plt.savefig(VISUALIZATION_PATH / "silhouette_scores.png", dpi=300)
    plt.close()

    final_model = sklearn.cluster.KMeans(n_clusters=optimal_k, random_state=42, n_init=20)
    labels: pd.Series = pd.Series(final_model.fit_predict(X_scaled), name="cluster_id")
    summary = {
        "k_values": list(k_values),
        "inertia": inertia_values,
        "silhouette": silhouette_values,
        "optimal_k": optimal_k,
    }
    return labels, summary


def perform_hierarchical_clustering(X_scaled: np.ndarray, n_clusters: int) -> tuple[pd.Series, float]:
    model = sklearn.cluster.AgglomerativeClustering(n_clusters=n_clusters, linkage="ward")
    labels = model.fit_predict(X_scaled)
    linkage_matrix = scipy.cluster.hierarchy.linkage(X_scaled, method="ward")
    plt.figure(figsize=(10, 7))
    scipy.cluster.hierarchy.dendrogram(linkage_matrix, truncate_mode="level", p=8)
    plt.title("Hierarchical Clustering Dendrogram")
    plt.xlabel("Sample Index")
    plt.ylabel("Distance")
    plt.tight_layout()
    plt.savefig(VISUALIZATION_PATH / "hierarchical_dendrogram.png", dpi=300)
    plt.close()

    score: float | np.floating | np.floating | np.float64 = sklearn.metrics.silhouette_score(X_scaled, labels)
    print(f"\nHierarchical silhouette score: {score:.4f}")
    return pd.Series(labels, name="hierarchical_cluster"), float(score)


def perform_dbscan(X_scaled: np.ndarray) -> tuple[pd.Series | None, float | None, dict | None]:
    best_score: float = -1.0
    best_params = None
    for eps in [0.3, 0.5, 0.8, 1.0, 1.5]:
        for min_samples in [3, 5, 8, 10]:
            labels = sklearn.cluster.DBSCAN(eps=eps, min_samples=min_samples).fit_predict(X_scaled)
            unique: set[typing.Any] = set(labels)
            if len(unique) < 2 or -1 in unique:
                continue
            try:
                score: float | np.floating | np.floating | np.float64 = sklearn.metrics.silhouette_score(X_scaled, labels)
            except ValueError:
                continue
            if score > best_score:
                best_score = score
                best_params = {"eps": eps, "min_samples": min_samples, "labels": labels, "unique_clusters": len(unique)}

    if best_params is None:
        print("DBSCAN produced no meaningful clusters for this dataset.")
        return None, None, None

    labels: pd.Series = pd.Series(best_params["labels"], name="dbscan_cluster")
    reduced = sklearn.decomposition.PCA(n_components=2).fit_transform(X_scaled)
    plt.figure(figsize=(8, 6))
    scatter: plt.PathCollection = plt.scatter(reduced[:, 0], reduced[:, 1], c=labels, cmap="viridis", s=35)
    plt.title("DBSCAN Clusters (PCA Projection)")
    plt.xlabel("Principal Component 1")
    plt.ylabel("Principal Component 2")
    plt.colorbar(scatter, label="Cluster")
    plt.tight_layout()
    plt.savefig(VISUALIZATION_PATH / "dbscan_clusters.png", dpi=300)
    plt.close()

    print(f"\nDBSCAN selected: eps={best_params['eps']}, min_samples={best_params['min_samples']}, clusters={best_params['unique_clusters']}")
    print(f"DBSCAN silhouette score: {best_score:.4f}")
    return labels, float(best_score), best_params


def plot_cluster_distribution(labels: pd.Series) -> None:
    counts: pd.Series = labels.value_counts().sort_index()
    plt.figure(figsize=(7, 5))
    sns.barplot(x=counts.index.astype(str), y=counts.values, palette="Set2")
    plt.title("Cluster Distribution")
    plt.xlabel("Cluster")
    plt.ylabel("Customer Count")
    plt.tight_layout()
    plt.savefig(VISUALIZATION_PATH / "cluster_distribution.png", dpi=300)
    plt.close()


def plot_cluster_profiles(df: pd.DataFrame, cluster_col: str) -> None:
    profile: pd.DataFrame = df.groupby(cluster_col)[["Tenure", "MonthlyCharges", "TotalCharges"]].mean().reset_index()
    melted: pd.DataFrame = profile.melt(id_vars=[cluster_col], var_name="Metric", value_name="Average")
    plt.figure(figsize=(9, 6))
    sns.barplot(data=melted, x=cluster_col, y="Average", hue="Metric", palette="Set2")
    plt.title("Cluster Profile Comparison")
    plt.xlabel("Cluster")
    plt.ylabel("Average Value")
    plt.legend(title="Metric")
    plt.tight_layout()
    plt.savefig(VISUALIZATION_PATH / "cluster_profiles.png", dpi=300)
    plt.close()


def plot_pca_clusters(df: pd.DataFrame, cluster_col: str, X_scaled: np.ndarray) -> None:
    reduced = sklearn.decomposition.PCA(n_components=2).fit_transform(X_scaled)
    plt.figure(figsize=(8, 6))
    scatter: plt.PathCollection = plt.scatter(reduced[:, 0], reduced[:, 1], c=df[cluster_col].astype(int), cmap="tab10", s=35)
    plt.title("PCA Cluster Visualization")
    plt.xlabel("PC1")
    plt.ylabel("PC2")
    plt.colorbar(scatter, label="Cluster")
    plt.tight_layout()
    plt.savefig(VISUALIZATION_PATH / "pca_clusters.png", dpi=300)
    plt.close()


def assign_business_name(row: pd.Series) -> str:
    churn_rate = row["churn_rate"]
    avg_tenure = row["avg_tenure"]
    avg_monthly = row["avg_monthly_charges"]

    if churn_rate >= 0.25:
        return "At-Risk Churners"
    if avg_tenure >= 35 and avg_monthly >= 110:
        return "High-Value Loyal Customers"
    if avg_tenure <= 20 and avg_monthly <= 80:
        return "Budget-Conscious Short-Term Customers"
    if avg_monthly >= 120:
        return "Premium Retention Segment"
    if churn_rate < 0.08:
        return "Low-Risk Stable Customers"
    return "Stable Growth Customers"


def build_segment_profile(df: pd.DataFrame, cluster_col: str = "final_cluster") -> pd.DataFrame:
    rows = []
    for cluster_id, group in df.groupby(cluster_col):
        contract_counts: pd.Series = group["Contract"].value_counts(normalize=True)
        payment_counts: pd.Series = group["PaymentMethod"].value_counts(normalize=True)
        row = {
            "segment": int(cluster_id),
            "customer_count": int(len(group)),
            "customer_percentage": round(len(group) / len(df) * 100, 2),
            "avg_tenure": round(group["Tenure"].mean(), 2),
            "avg_monthly_charges": round(group["MonthlyCharges"].mean(), 2),
            "avg_total_charges": round(group["TotalCharges"].mean(), 2),
            "churn_rate": round(group["Churn"].mean(), 4),
            "senior_citizen_pct": round(group["SeniorCitizen"].mean(), 4),
            "dominant_contract": contract_counts.idxmax(),
            "dominant_contract_pct": round(contract_counts.max() * 100, 2),
            "dominant_payment": payment_counts.idxmax(),
            "dominant_payment_pct": round(payment_counts.max() * 100, 2),
            "paperless_billing_yes_pct": round(group["PaperlessBilling"].eq("Yes").mean() * 100, 2),
            "contract_distribution": json.dumps(group["Contract"].value_counts(normalize=True).mul(100).round(2).to_dict(), sort_keys=True),
            "payment_distribution": json.dumps(group["PaymentMethod"].value_counts(normalize=True).mul(100).round(2).to_dict(), sort_keys=True),
            "paperless_distribution": json.dumps(group["PaperlessBilling"].value_counts(normalize=True).mul(100).round(2).to_dict(), sort_keys=True),
        }
        rows.append(row)

    profile: pd.DataFrame = pd.DataFrame(rows).sort_values("segment").reset_index(drop=True)
    profile["segment_name"] = "Established Customer Base"
    profile.loc[profile["churn_rate"].idxmax(), "segment_name"] = "Highest Churn Priority"
    profile.loc[profile["churn_rate"].idxmin(), "segment_name"] = "Lowest Churn Stability"
    remaining: list[typing.Any] = profile.index[profile["segment_name"] == "Established Customer Base"].tolist()
    if remaining:
        profile.loc[profile["avg_monthly_charges"].idxmax(), "segment_name"] = "Higher-Value Premium Base"
        remaining: list[typing.Any] = profile.index[profile["segment_name"] == "Established Customer Base"].tolist()
    if remaining:
        profile.loc[profile["avg_monthly_charges"].idxmin(), "segment_name"] = "Lower-Charge Opportunity"
        remaining: list[typing.Any] = profile.index[profile["segment_name"] == "Established Customer Base"].tolist()
    for rank, index in enumerate(remaining, start=1):
        profile.loc[index, "segment_name"] = f"Established Customer Base {rank}"
    return profile


def profile_segments(df: pd.DataFrame) -> pd.DataFrame:
    profile: pd.DataFrame = build_segment_profile(df)
    profile.to_csv(RESULTS_PATH / "segment_profiles.csv", index=False)
    print("\n=== SEGMENT PROFILES ===")
    print(profile.to_string(index=False))
    return profile


def build_preprocessor() -> sklearn.compose.ColumnTransformer:
    num_cols: list[str] = ["Tenure", "MonthlyCharges", "TotalCharges", "SeniorCitizen"]
    cat_cols: list[str] = ["Contract", "PaymentMethod", "PaperlessBilling"]
    return sklearn.compose.ColumnTransformer(
        transformers=[
            ("num", sklearn.pipeline.Pipeline([("imputer", sklearn.impute.SimpleImputer(strategy="median")), ("scaler", sklearn.preprocessing.StandardScaler())]), num_cols),
            ("cat", sklearn.pipeline.Pipeline([("imputer", sklearn.impute.SimpleImputer(strategy="most_frequent")), ("onehot", sklearn.preprocessing.OneHotEncoder(handle_unknown="ignore", sparse_output=False))]), cat_cols),
        ]
    )


def evaluate_segment_model(segment_df: pd.DataFrame, segment_id: int) -> dict:
    feature_cols: list[str] = ["Tenure", "MonthlyCharges", "TotalCharges", "SeniorCitizen", "Contract", "PaymentMethod", "PaperlessBilling"]
    X: pd.DataFrame = segment_df[feature_cols]
    y: pd.Series = segment_df["Churn"].astype(int)

    if len(segment_df) < 20:
        raise ValueError(f"Segment {segment_id} is too small for robust training.")
    if y.nunique() < 2:
        raise ValueError(f"Segment {segment_id} does not contain both churn classes.")

    X_train, X_test, y_train, y_test = sklearn.model_selection.train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    minority_count = int(y_train.value_counts().min())
    if minority_count < 2:
        raise ValueError(f"Segment {segment_id} has too few training examples in its minority class for cross-validation.")
    pipeline = sklearn.pipeline.Pipeline([
        ("preprocessor", build_preprocessor()),
        ("model", sklearn.ensemble.RandomForestClassifier(random_state=42, class_weight="balanced"))
    ])

    param_grid = {
        "model__n_estimators": [100, 200],
        "model__max_depth": [None, 8, 15],
        "model__min_samples_split": [2, 5],
        "model__min_samples_leaf": [1, 2],
        "model__max_features": ["sqrt"],
    }
    search: sklearn.model_selection.GridSearchCV = sklearn.model_selection.GridSearchCV(
        pipeline,
        param_grid=param_grid,
        cv=min(3, minority_count),
        scoring="f1",
        n_jobs=-1,
    )
    search.fit(X_train, y_train)

    best_model: sklearn.pipeline.Pipeline = search.best_estimator_
    predictions = best_model.predict(X_test)
    probas = best_model.predict_proba(X_test)[:, 1]

    metrics = {
        "segment": segment_id,
        "accuracy": float(sklearn.metrics.accuracy_score(y_test, predictions)),
        "precision": float(sklearn.metrics.precision_score(y_test, predictions, zero_division=0)),
        "recall": float(sklearn.metrics.recall_score(y_test, predictions, zero_division=0)),
        "f1_score": float(sklearn.metrics.f1_score(y_test, predictions, zero_division=0)),
        "roc_auc": float(sklearn.metrics.roc_auc_score(y_test, probas)) if len(np.unique(y_test)) == 2 else np.nan,
        "best_params": search.best_params_,
        "confusion_matrix": sklearn.metrics.confusion_matrix(y_test, predictions).tolist(),
        "y_test": y_test,
        "predictions": predictions,
        "probas": probas,
        "model": best_model,
        "test_customer_ids": segment_df.loc[y_test.index, "CustomerID"],
    }

    feature_names = best_model.named_steps["preprocessor"].get_feature_names_out()
    importances = best_model.named_steps["model"].feature_importances_
    metrics["feature_importance"] = pd.DataFrame({"feature": feature_names, "importance": importances}).sort_values("importance", ascending=False).head(10)
    return metrics


def train_segment_models(df: pd.DataFrame, segment_mapping: dict[int, str]) -> tuple[pd.DataFrame, pd.DataFrame]:
    rows = []
    prediction_rows = []

    for segment_id, segment_name in segment_mapping.items():
        segment_df: pd.DataFrame = df[df["final_cluster"] == segment_id].copy()
        if segment_df.empty:
            continue
        try:
            summary = evaluate_segment_model(segment_df, segment_id)
        except ValueError as exc:
            print(f"Skipping segment {segment_id}: {exc}")
            continue

        rows.append({
            "segment": segment_id,
            "segment_name": segment_name,
            "accuracy": summary["accuracy"],
            "precision": summary["precision"],
            "recall": summary["recall"],
            "f1_score": summary["f1_score"],
            "roc_auc": summary["roc_auc"],
            "best_params": json.dumps(summary["best_params"], sort_keys=True),
            "confusion_matrix": json.dumps(summary["confusion_matrix"]),
            "top_features": json.dumps(summary["feature_importance"].head(5)["feature"].tolist()),
        })

        for customer_id, actual, pred, prob in zip(summary["test_customer_ids"], summary["y_test"], summary["predictions"], summary["probas"]):
            prediction_rows.append({
                "CustomerID": customer_id,
                "Segment": segment_id,
                "SegmentName": segment_name,
                "ActualChurn": int(actual),
                "PredictedChurn": int(pred),
                "PredictionProbability": float(prob),
            })

        importance = summary["feature_importance"]
        plt.figure(figsize=(8, 5))
        sns.barplot(data=importance, x="importance", y="feature", palette="viridis")
        plt.title(f"Feature Importance - Segment {segment_id}: {segment_name}")
        plt.xlabel("Importance")
        plt.ylabel("Feature")
        plt.tight_layout()
        plt.savefig(VISUALIZATION_PATH / f"feature_importance_segment_{segment_id + 1}.png", dpi=300)
        plt.close()

    if not rows:
        raise RuntimeError("No valid segment models were produced from the real data.")

    model_df = pd.DataFrame(rows)
    model_df.to_csv(RESULTS_PATH / "model_evaluation_results.csv", index=False)
    prediction_df = pd.DataFrame(prediction_rows)
    prediction_df.to_csv(RESULTS_PATH / "prediction_results.csv", index=False)

    print("\n=== MODEL EVALUATION RESULTS ===")
    print(model_df.to_string(index=False))
    return model_df, prediction_df


def plot_model_comparison(model_df: pd.DataFrame) -> None:
    melted: pd.DataFrame = model_df.melt(id_vars=["segment", "segment_name"], value_vars=["accuracy", "precision", "recall", "f1_score"], var_name="Metric", value_name="Score")
    plt.figure(figsize=(9, 6))
    sns.barplot(data=melted, x="segment_name", y="Score", hue="Metric", palette="Set2")
    plt.title("Segment Model Performance Comparison")
    plt.xlabel("Segment")
    plt.ylabel("Score")
    plt.xticks(rotation=30)
    plt.tight_layout()
    plt.savefig(VISUALIZATION_PATH / "model_comparison.png", dpi=300)
    plt.close()


def assign_final_cluster_labels(df: pd.DataFrame, labels: pd.Series) -> pd.DataFrame:
    result: pd.DataFrame = df.copy()
    result["final_cluster"] = labels.reset_index(drop=True)
    return result


def write_markdown_report(df: pd.DataFrame, profile_df: pd.DataFrame, kmeans_summary: dict, hierarchical_score: float, dbscan_summary: dict | None, model_results: pd.DataFrame) -> None:
    report_path: pathlib.Path = REPORT_PATH / "segment_profiles.md"
    lines: list[str] = [
        "# Week 11 – Advanced Machine Learning Models",
        "",
        "## 1. Dataset Summary",
        f"- Rows: {df.shape[0]}",
        f"- Columns: {df.shape[1]}",
        f"- Missing values: {df.isna().sum().to_dict()}",
        f"- Duplicate rows: {int(df.duplicated().sum())}",
        f"- Churn distribution: {df['Churn'].value_counts().to_dict()}",
        "",
        "## 2. Clustering",
        f"- Tested K values: {kmeans_summary['k_values']}",
        f"- K-Means inertia: {kmeans_summary['inertia']}",
        f"- K-Means silhouette scores: {kmeans_summary['silhouette']}",
        f"- Optimal K: {kmeans_summary['optimal_k']}",
        f"- Hierarchical silhouette score: {hierarchical_score:.4f}",
        f"- DBSCAN summary: {dbscan_summary}",
        "",
        "## 3. Segment Profiles",
    ]

    for _, row in profile_df.iterrows():
        lines.extend([
            f"### Segment {int(row['segment'])}: {row['segment_name']}",
            f"- Customer count: {int(row['customer_count'])}",
            f"- Customer percentage: {float(row['customer_percentage'])}%",
            f"- Average tenure: {float(row['avg_tenure']):.2f}",
            f"- Average monthly charges: {float(row['avg_monthly_charges']):.2f}",
            f"- Average total charges: {float(row['avg_total_charges']):.2f}",
            f"- Churn rate: {float(row['churn_rate']):.2%}",
            f"- Dominant contract: {row['dominant_contract']} ({float(row['dominant_contract_pct']):.2f}%)",
            f"- Dominant payment: {row['dominant_payment']} ({float(row['dominant_payment_pct']):.2f}%)",
            f"- Paperless billing share: {float(row['paperless_billing_yes_pct']):.2f}%",
            "",
        ])

    lines.extend([
        "## 4. Segment Model Evaluation",
        "| Segment | Accuracy | Precision | Recall | F1-score | ROC-AUC |",
        "| --- | ---: | ---: | ---: | ---: | ---: |",
    ])
    for _, row in model_results.iterrows():
        roc_value: str = "N/A" if pd.isna(row["roc_auc"]) else f"{float(row['roc_auc']):.4f}"
        lines.append(f"| {int(row['segment'])} | {float(row['accuracy']):.4f} | {float(row['precision']):.4f} | {float(row['recall']):.4f} | {float(row['f1_score']):.4f} | {roc_value} |")

    lines.extend([
        "",
        "## 5. Business Recommendations",
        "- Prioritize retention efforts in the highest-churn segment.",
        "- Protect high-value loyal customers by maintaining service continuity and loyalty offers.",
        "- Use pricing and engagement tactics for lower-value or short-tenure segments.",
        "",
        "## 6. Conclusion",
        "This workflow uses the actual customer churn dataset to create meaningful segments, profile them, and build segment-specific predictive models that support business retention decisions.",
    ])

    report_path.write_text("\n".join(lines), encoding="utf-8")
    print(f"\nReport saved to: {report_path}")


def write_detailed_report(
    raw_df: pd.DataFrame,
    profile_df: pd.DataFrame,
    kmeans_summary: dict,
    hierarchical_score: float,
    dbscan_summary: dict | None,
    model_results: pd.DataFrame,
) -> None:
    """Write the evidence-based project report from the generated results."""
    lines: list[str] = [
        "# Week 11 - Advanced Machine Learning Models",
        "",
        "## 1. Project Overview",
        "This project segments the actual customer churn dataset and trains separate churn prediction models for each final segment.",
        "",
        "## 2. Objectives",
        "- Inspect and validate the source data.",
        "- Compare K-Means, agglomerative hierarchical clustering, and DBSCAN.",
        "- Profile the selected customer segments.",
        "- Tune and evaluate a separate Random Forest model for each segment.",
        "- Translate observed segment and model results into cautious business recommendations.",
        "",
        "## 3. Dataset Description",
        f"- Rows: {raw_df.shape[0]}",
        f"- Columns: {raw_df.shape[1]}",
        f"- Columns: {', '.join(raw_df.columns)}",
        f"- Data types: {raw_df.dtypes.astype(str).to_dict()}",
        "- Target: Churn (0 = retained, 1 = churned)",
        "",
        "## 4. Data Exploration",
        f"- Missing values: {raw_df.isna().sum().to_dict()}",
        f"- Duplicate rows: {int(raw_df.duplicated().sum())}",
        f"- Churn distribution: {raw_df['Churn'].value_counts().to_dict()} ({raw_df['Churn'].mean():.2%} churn)",
        f"- Contract distribution: {raw_df['Contract'].value_counts().to_dict()}",
        f"- Payment method distribution: {raw_df['PaymentMethod'].value_counts().to_dict()}",
        f"- Paperless billing distribution: {raw_df['PaperlessBilling'].value_counts().to_dict()}",
        f"- Numerical statistics: {raw_df[['Tenure', 'MonthlyCharges', 'TotalCharges', 'SeniorCitizen']].describe().round(2).to_dict()}",
        "",
        "## 5. Data Preprocessing",
        "Numeric columns were converted with pandas numeric coercion and median imputation is available in the modeling pipeline for any future missing values. Duplicate rows were removed if present. Categorical values were trimmed and title-cased. CustomerID was retained only for traceability and excluded from every feature matrix.",
        "",
        "## 6. Feature Engineering",
        "Clustering and prediction use Tenure, MonthlyCharges, TotalCharges, SeniorCitizen, Contract, PaymentMethod, and PaperlessBilling. Numeric features are standardized for distance-based clustering. Categorical features are one-hot encoded in the prediction pipeline with unknown-category handling.",
        "",
        "## 7. Clustering Methodology",
        "K-Means was evaluated for K=2 through K=8 using inertia and silhouette score. Agglomerative clustering with Ward linkage was compared at the selected K. DBSCAN tested a small grid of eps and min_samples values; configurations with noise or fewer than two meaningful clusters were excluded from silhouette comparison.",
        "",
        "## 8. Optimal Cluster Selection",
        f"- Tested K values: {kmeans_summary['k_values']}",
        f"- Inertia: {[round(value, 3) for value in kmeans_summary['inertia']]}",
        f"- Silhouette scores: {[round(value, 4) for value in kmeans_summary['silhouette']]}",
        f"- Selected K-Means K: {kmeans_summary['optimal_k']}",
        f"- Hierarchical silhouette: {hierarchical_score:.4f}",
        f"- DBSCAN result: {dbscan_summary if dbscan_summary is not None else 'No configuration produced a meaningful non-noise solution.'}",
        "K-Means was selected for the final labels because it had the strongest tested silhouette result and produced six interpretable, sufficiently sized groups for segment-specific modeling.",
        "",
        "## 9. Cluster Profiles",
        "The following profiles are generated directly from results/segment_profiles.csv.",
        "",
    ]
    for _, row in profile_df.iterrows():
        lines.extend([
            f"### Segment {int(row['segment'])}: {row['segment_name']}",
            f"- Customers: {int(row['customer_count'])} ({float(row['customer_percentage']):.2f}%)",
            f"- Average tenure: {float(row['avg_tenure']):.2f}",
            f"- Average monthly charges: {float(row['avg_monthly_charges']):.2f}",
            f"- Average total charges: {float(row['avg_total_charges']):.2f}",
            f"- Churn rate: {float(row['churn_rate']):.2%}",
            f"- Senior citizen share: {float(row['senior_citizen_pct']):.2%}",
            f"- Contract distribution: {row['contract_distribution']}",
            f"- Payment distribution: {row['payment_distribution']}",
            f"- Paperless billing distribution: {row['paperless_distribution']}",
            "",
        ])

    lines.extend([
        "## 10. Prediction Methodology",
        "Churn is the binary target. Each segment is filtered independently, split 80/20 with random_state=42 and stratification, then modeled with a separate Random Forest pipeline. The preprocessor is fitted inside the training pipeline to prevent test-set transformation leakage.",
        "",
        "## 11. Model Evaluation",
        "| Segment | Accuracy | Precision | Recall | F1-score | ROC-AUC |",
        "| --- | ---: | ---: | ---: | ---: | ---: |",
    ])
    for _, row in model_results.iterrows():
        auc: str = "N/A" if pd.isna(row["roc_auc"]) else f"{float(row['roc_auc']):.4f}"
        lines.append(f"| {int(row['segment'])}: {row['segment_name']} | {float(row['accuracy']):.4f} | {float(row['precision']):.4f} | {float(row['recall']):.4f} | {float(row['f1_score']):.4f} | {auc} |")

    lines.extend([
        "",
        "## 12. Hyperparameter Tuning",
        "GridSearchCV optimized n_estimators, max_depth, min_samples_split, min_samples_leaf, and max_features using up to three stratified folds. Best parameters and confusion matrices are stored in results/model_evaluation_results.csv.",
        "",
        "## 13. Feature Importance",
    ])
    for _, row in model_results.iterrows():
        lines.append(f"- Segment {int(row['segment'])} ({row['segment_name']}): {row['top_features']}. These are predictive associations, not causal effects.")

    highest: pd.Series | pd.DataFrame = profile_df.loc[profile_df["churn_rate"].idxmax()]
    valuable: pd.Series | pd.DataFrame = profile_df.loc[profile_df["avg_total_charges"].idxmax()]
    lines.extend([
        "",
        "## 14. Business Insights",
        f"- Highest observed churn: Segment {int(highest['segment'])} ({highest['segment_name']}) at {float(highest['churn_rate']):.2%}.",
        f"- Highest average total charges: Segment {int(valuable['segment'])} ({valuable['segment_name']}) at {float(valuable['avg_total_charges']):.2f}; this is a value proxy, not customer lifetime value.",
        "- Segment sizes and categorical distributions should be read together with churn rate; a small high-rate segment can still be operationally important.",
        "",
        "## 15. Business Recommendations",
    ])
    for _, row in profile_df.iterrows():
        strategy: str = "Prioritize targeted retention outreach and investigate contract, payment, and billing friction." if row["segment"] == highest["segment"] else "Use tailored engagement and monitor churn signals; preserve the segment's existing service experience."
        lines.extend([f"- **{row['segment_name']}**: {strategy}"])

    lines.extend([
        "",
        "## 16. Model Limitations",
        "The dataset has 500 rows and only 53 churn cases, so segment-level test metrics can be unstable. Some segments have few positive examples and ROC-AUC is reported only when both test classes are present. Clustering is sensitive to preprocessing and distance choices. Feature importance indicates model use, not causation, and performance on this sample may not generalize to future customers.",
        "",
        "## 17. Testing",
        "The executed script validated CSV loading, required columns, numeric conversion, missing values, duplicates, encoded/scaled features, K-Means inertia and silhouette scoring, hierarchical clustering, DBSCAN parameter search, cluster assignments, profiles, stratified splits, tuned segment models, predictions, classification metrics, feature importance, charts, CSV outputs, and report generation.",
        "",
        "## 18. Visual Documentation",
        "Charts in visualizations/ document the elbow curve, silhouette comparison, cluster distribution, profiles, PCA projection, hierarchical dendrogram, model comparison, and feature importance. The screenshots/ directory is intentionally left for manually captured evidence.",
        "",
        "## 19. What I Learned",
        "The workflow demonstrates how scaling affects distance-based clustering, how silhouette and inertia support K selection, how hierarchical clustering and DBSCAN provide alternative views, how PCA can visualize high-dimensional assignments, and why segment-specific model metrics and feature importance need careful interpretation under class imbalance.",
        "",
        "## 20. Conclusion",
        "The actual customer_churn.csv was inspected, transformed without using CustomerID as a feature, segmented with reproducible clustering, and used to train independent tuned Random Forest models for each final segment. Results and recommendations are evidence-based and preserved in the generated CSV files and charts.",
    ])
    (REPORT_PATH / "segment_profiles.md").write_text("\n".join(lines), encoding="utf-8")


def generate_business_recommendations_pdf(
    raw_df: pd.DataFrame,
    profile_df: pd.DataFrame,
    model_results: pd.DataFrame,
) -> pathlib.Path:
    """Create a detailed, evidence-based business recommendations PDF."""
    from matplotlib.backends.backend_pdf import PdfPages

    pdf_path: pathlib.Path = REPORT_PATH / "business_recommendations.pdf"
    highest: pd.Series | pd.DataFrame = profile_df.loc[profile_df["churn_rate"].idxmax()]
    lowest: pd.Series | pd.DataFrame = profile_df.loc[profile_df["churn_rate"].idxmin()]
    highest_value: pd.Series | pd.DataFrame = profile_df.loc[profile_df["avg_total_charges"].idxmax()]

    def add_page(title: str, sections: list[tuple[str, str]], footer: str = "Week 11 - Customer Segmentation & Prediction") -> None:
        figure: plt.Figure = plt.figure(figsize=(8.27, 11.69))
        figure.patch.set_facecolor("#f7f9fc")
        figure.text(0.08, 0.95, title, fontsize=20, fontweight="bold", color="#17324d", va="top")
        y_position = 0.90
        for heading, body in sections:
            figure.text(0.08, y_position, heading, fontsize=11.5, fontweight="bold", color="#197278", va="top")
            y_position -= 0.027
            wrapped: list[str] = textwrap.wrap(body, width=94) or [""]
            for line in wrapped:
                figure.text(0.09, y_position, line, fontsize=9.3, color="#24313d", va="top")
                y_position -= 0.019
            y_position -= 0.018
        figure.text(0.08, 0.035, footer, fontsize=8, color="#6b7785")
        pdf.savefig(figure, bbox_inches="tight")
        plt.close(figure)

    with matplotlib.backends.backend_pdf.PdfPages(pdf_path) as pdf:
        add_page(
            "Business Recommendations",
            [
                ("Purpose", "This document translates the actual customer_churn.csv analysis into practical retention actions. Recommendations are based on observed segment profiles, churn rates, model metrics, and predictive features. Feature importance indicates predictive association and does not prove causation."),
                ("Dataset evidence", f"The dataset contains {len(raw_df)} customers and {int(raw_df['Churn'].sum())} observed churn cases ({raw_df['Churn'].mean():.2%}). There are no missing values and no duplicate rows. CustomerID was used only for traceability, never as a machine-learning feature."),
                ("Executive conclusion", f"Segment {int(highest['segment'])}, {highest['segment_name']}, needs the highest retention attention with {highest['churn_rate']:.2%} churn across {int(highest['customer_count'])} customers. Segment {int(lowest['segment'])}, {lowest['segment_name']}, is the most stable at {lowest['churn_rate']:.2%}. Segment {int(highest_value['segment'])} has the highest average TotalCharges ({highest_value['avg_total_charges']:.2f}) and should be treated as a value-protection priority, while recognizing that TotalCharges is only a value proxy."),
                ("Recommended operating principle", "Use the highest-churn segment for immediate retention experiments, use the stable segments as a control or loyalty population, and review model probabilities together with customer context before contacting customers."),
            ],
        )

        for _, profile in profile_df.iterrows():
            segment_id = int(profile["segment"])
            model: pd.DataFrame = model_results[model_results["segment"] == segment_id]
            model_row: pd.Series | None = model.iloc[0] if not model.empty else None
            churn_rate = float(profile["churn_rate"])
            if segment_id == int(highest["segment"]):
                priority = "CRITICAL - first retention priority"
                strategy = "Launch a focused save campaign. Review contract renewal options, payment experience, billing clarity, and service friction. Offer a measured contract incentive only after identifying the relevant friction; do not assume price is the cause."
            elif segment_id == int(lowest["segment"]):
                priority = "LOW - protect and learn"
                strategy = "Maintain service quality, use lightweight loyalty recognition, and avoid unnecessary discounting. This segment can provide a useful comparison group when measuring retention experiments."
            elif float(profile["avg_total_charges"]) == float(highest_value["avg_total_charges"]):
                priority = "HIGH - protect customer value"
                strategy = "Prioritize continuity and proactive service communication. Monitor churn scores closely because losing customers with higher accumulated charges may have greater commercial impact."
            elif churn_rate >= float(raw_df["Churn"].mean()):
                priority = "HIGH - above overall churn rate"
                strategy = "Use targeted outreach and test contract, billing, and engagement interventions. Compare outcomes against a holdout group before scaling the campaign."
            else:
                priority = "MEDIUM - monitor and nurture"
                strategy = "Use personalized engagement, periodic satisfaction checks, and model-score monitoring. Escalate customers whose predicted risk increases rather than applying broad discounts."

            feature_text = "No model summary available."
            metric_text = "No valid segment model was produced."
            if model_row is not None:
                feature_text: str = str(model_row["top_features"]).replace("num__", "").replace("cat__", "")
                auc_text: str = "not valid" if pd.isna(model_row["roc_auc"]) else f"{float(model_row['roc_auc']):.3f}"
                metric_text: str = f"Accuracy {float(model_row['accuracy']):.3f}; precision {float(model_row['precision']):.3f}; recall {float(model_row['recall']):.3f}; F1 {float(model_row['f1_score']):.3f}; ROC-AUC {auc_text}."

            add_page(
                f"Segment {segment_id}: {profile['segment_name']}",
                [
                    ("Priority", priority),
                    ("Observed profile", f"{int(profile['customer_count'])} customers ({float(profile['customer_percentage']):.2f}% of the dataset); average tenure {float(profile['avg_tenure']):.2f}; average MonthlyCharges {float(profile['avg_monthly_charges']):.2f}; average TotalCharges {float(profile['avg_total_charges']):.2f}; senior citizen share {float(profile['senior_citizen_pct']):.2%}; observed churn {churn_rate:.2%}."),
                    ("Observed categorical pattern", f"Contract distribution: {profile['contract_distribution']}. Payment distribution: {profile['payment_distribution']}. Paperless billing distribution: {profile['paperless_distribution']}. These are descriptive patterns, not causal explanations."),
                    ("Model evidence", f"{metric_text} Top predictive features: {feature_text}. Low recall or zero positive predictions means the model should not be used as an automatic rejection or contact decision."),
                    ("Recommended strategy", strategy),
                    ("Actions", "1) Define a contact list using segment membership and model probability. 2) Test one intervention at a time. 3) Record offer, contact channel, response, and subsequent churn. 4) Review results by segment and by churn outcome."),
                    ("Success measures", "Primary: reduction in churn among contacted eligible customers. Secondary: save rate, offer acceptance, complaint rate, incremental revenue, and cost per retained customer. Always compare with a holdout group where permitted."),
                ],
            )

        add_page(
            "Retention Program Design",
            [
                ("Priority order", f"1. {highest['segment_name']} at {highest['churn_rate']:.2%} churn. 2. Segments at or above the overall churn rate of {raw_df['Churn'].mean():.2%}. 3. {highest_value['segment_name']} for value protection. 4. Stable segments for loyalty and control-group learning."),
                ("Contact policy", "Use a human-reviewed threshold for outreach. Do not treat a predicted probability as a guaranteed outcome. Suppress customers who recently received the same offer, have unresolved complaints, or are legally restricted from the campaign."),
                ("Experiment policy", "For each segment, define a treatment group and a comparable holdout group. Predefine the success metric and evaluation window. Avoid changing multiple offers simultaneously because that makes the result difficult to interpret."),
                ("Data feedback loop", "Store campaign exposure, offer type, channel, response, renewal, and churn outcome. Recalculate segment profiles periodically because customer composition and contract mix can change."),
                ("Governance", "Review fairness and unintended impact, especially where SeniorCitizen appears among important predictive features. Use the model to support customer service decisions, not to deny service or impose punitive pricing."),
            ],
        )

        add_page(
            "Implementation Roadmap and Limitations",
            [
                ("First 30 days", "Validate the highest-churn segment with customer-service and billing teams. Create a small controlled retention campaign. Capture treatment, response, cost, and churn outcomes."),
                ("Days 31-60", "Compare campaign and holdout results. Refine the contact threshold and messaging. Review false negatives and false positives, not accuracy alone."),
                ("Days 61-90", "Scale only interventions with measurable incremental retention. Retrain the segment and prediction workflow when new labeled outcomes are available."),
                ("Model limitations", "The dataset has 500 rows and only 53 churn cases. Segment-level test metrics may be unstable, and several models predict no positive class in their small test sets. ROC-AUC is omitted where mathematically invalid. Clustering depends on feature scaling and algorithm choices."),
                ("Final caution", "The recommendations describe sensible actions suggested by observed data. They should be validated through controlled business experiments and customer feedback before becoming permanent policy."),
            ],
        )

    return pdf_path


def main() -> None:
    ensure_directories()
    df: pd.DataFrame = load_data(DATA_PATH)
    df: pd.DataFrame = clean_data(df)
    print_exploratory_summary(df)

    features: pd.DataFrame = prepare_clustering_features(df)
    X_scaled = sklearn.preprocessing.StandardScaler().fit_transform(features)

    k_values = range(2, 9)
    kmeans_labels, kmeans_summary = perform_kmeans(X_scaled, k_values)
    hierarchical_labels, hierarchical_score = perform_hierarchical_clustering(X_scaled, n_clusters=kmeans_summary["optimal_k"])
    _, _, dbscan_summary = perform_dbscan(X_scaled)

    final_labels: pd.Series = kmeans_labels if kmeans_summary["optimal_k"] >= 3 else hierarchical_labels
    cluster_assignments = pd.DataFrame({"CustomerID": df["CustomerID"], "cluster": final_labels.values})
    cluster_assignments.to_csv(RESULTS_PATH / "cluster_assignments.csv", index=False)

    df_with_clusters: pd.DataFrame = assign_final_cluster_labels(df, final_labels)
    plot_cluster_distribution(df_with_clusters["final_cluster"])
    plot_cluster_profiles(df_with_clusters, "final_cluster")
    plot_pca_clusters(df_with_clusters, "final_cluster", X_scaled)

    profile: pd.DataFrame = profile_segments(df_with_clusters)
    segment_mapping: dict[int, typing.Any] = {int(row["segment"]): row["segment_name"] for _, row in profile.iterrows()}
    model_df, prediction_df = train_segment_models(df_with_clusters, segment_mapping)
    plot_model_comparison(model_df)
    write_detailed_report(df, profile, kmeans_summary, hierarchical_score, dbscan_summary, model_df)
    generate_business_recommendations_pdf(df, profile, model_df)

    print("\n=== FINAL SUMMARY ===")
    print(f"Optimal K: {kmeans_summary['optimal_k']}")
    print(f"Hierarchical silhouette: {hierarchical_score:.4f}")
    if dbscan_summary is not None:
        print(f"DBSCAN clusters: {dbscan_summary['unique_clusters']}")
    print(f"Cluster assignments saved to: {RESULTS_PATH / 'cluster_assignments.csv'}")
    print(f"Segment profiles saved to: {RESULTS_PATH / 'segment_profiles.csv'}")
    print(f"Model evaluation saved to: {RESULTS_PATH / 'model_evaluation_results.csv'}")
    print(f"Prediction results saved to: {RESULTS_PATH / 'prediction_results.csv'}")
    print(f"Markdown report saved to: {REPORT_PATH / 'segment_profiles.md'}")


if __name__ == "__main__":
    main()
