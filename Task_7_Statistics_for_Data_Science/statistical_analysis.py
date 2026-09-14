"""Week 7 statistical business analysis using the supplied datasets."""

import pathlib
import typing

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import pandas.core.arrays.base
import seaborn as sns
import scipy as sp


PROJECT_DIR: pathlib.Path = pathlib.Path(__file__).parent
SALES_FILE: pathlib.Path = PROJECT_DIR / "sales_data.csv"
CUSTOMER_FILE: pathlib.Path = PROJECT_DIR / "customer_churn.csv"
VISUALIZATIONS_DIR: pathlib.Path = PROJECT_DIR / "visualizations"
ALPHA = 0.05


def load_and_clean_data() -> tuple[pd.DataFrame, pd.DataFrame, dict[str, int]]:
    """Load, validate, and prepare both real datasets."""
    if not SALES_FILE.exists() or not CUSTOMER_FILE.exists():
        raise FileNotFoundError("Both sales_data.csv and customer_churn.csv are required.")

    sales: pd.DataFrame = pd.read_csv(SALES_FILE)
    customers: pd.DataFrame = pd.read_csv(CUSTOMER_FILE)
    required_sales: set[str] = {"Date", "Product", "Quantity", "Price", "Customer_ID", "Region", "Total_Sales"}
    required_customers: set[str] = {"CustomerID", "Tenure", "MonthlyCharges", "TotalCharges", "Contract", "PaymentMethod", "PaperlessBilling", "SeniorCitizen", "Churn"}
    if not required_sales.issubset(sales.columns):
        raise ValueError("sales_data.csv is missing required columns.")
    if not required_customers.issubset(customers.columns):
        raise ValueError("customer_churn.csv is missing required columns.")
    if sales.empty or customers.empty:
        raise ValueError("One of the datasets is empty.")

    quality: dict[str, int] = {
        "sales_missing": int(sales.isna().sum().sum()),
        "customer_missing": int(customers.isna().sum().sum()),
        "sales_duplicates": int(sales.duplicated().sum()),
        "customer_duplicates": int(customers.duplicated().sum()),
    }
    sales["Date"] = pd.to_datetime(sales["Date"], errors="coerce")
    for column in ["Quantity", "Price", "Total_Sales"]:
        sales[column] = pd.to_numeric(sales[column], errors="coerce")
    for column in ["Tenure", "MonthlyCharges", "TotalCharges", "SeniorCitizen", "Churn"]:
        customers[column] = pd.to_numeric(customers[column], errors="coerce")
    if sales.isna().any().any() or customers.isna().any().any():
        raise ValueError("Invalid or missing values remain after type conversion.")
    if not customers["Churn"].isin([0, 1]).all():
        raise ValueError("Churn must contain only 0 and 1.")

    sales: pd.DataFrame = sales.drop_duplicates().copy()
    customers: pd.DataFrame = customers.drop_duplicates().copy()
    sales["Month"] = sales["Date"].dt.to_period("M").astype(str)
    sales["Year"] = sales["Date"].dt.year
    sales["Month_Name"] = sales["Date"].dt.strftime("%b %Y")
    return sales, customers, quality


def run_statistics(sales: pd.DataFrame, customers: pd.DataFrame) -> tuple[str, dict[str, float]]:
    """Calculate descriptive statistics, tests, confidence intervals, and regression."""
    sales_values: pd.Series = sales["Total_Sales"]
    mean_sales: float = sales_values.mean()
    sem = sp.stats.sem(sales_values)
    mean_ci = sp.stats.t.interval(0.95, len(sales_values) - 1, loc=mean_sales, scale=sem)
    margin_error = mean_ci[1] - mean_sales

    one_sample = sp.stats.ttest_1samp(sales_values, popmean=100000)
    region_groups: list[np.ndarray[tuple[int], np.dtype[typing.Any]] | pandas.core.arrays.base.ExtensionArray | pd.Categorical] = [group["Total_Sales"].values for _, group in sales.groupby("Region")]
    anova = sp.stats.f_oneway(*region_groups)
    pearson = sp.stats.pearsonr(sales["Price"], sales["Total_Sales"])
    contingency: pd.DataFrame = pd.crosstab(customers["Contract"], customers["Churn"])
    chi_square = sp.stats.chi2_contingency(contingency)
    regression = sp.stats.linregress(sales["Quantity"], sales["Total_Sales"])
    covariance: pd.DataFrame = sales[["Quantity", "Price", "Total_Sales"]].cov()

    def decision(p_value: float) -> str:
        return "Reject H0" if p_value < ALPHA else "Fail to reject H0"

    tests: list[tuple[str, str, str, str, typing.Any, typing.Any, str]] = [
        ("One-sample t-test: mean sale vs 100,000", "H0: Mean Total_Sales = 100,000", "H1: Mean Total_Sales != 100,000", "one-sample t-test", one_sample.statistic, one_sample.pvalue, "The average transaction differs statistically from the 100,000 benchmark."),
        ("One-way ANOVA: sales across regions", "H0: All regional mean sales are equal", "H1: At least one regional mean differs", "one-way ANOVA", anova.statistic, anova.pvalue, "Regional average sales show whether location is associated with different transaction values."),
        ("Pearson correlation: Price and Total_Sales", "H0: Population correlation is 0", "H1: Population correlation is not 0", "Pearson correlation significance test", pearson.statistic, pearson.pvalue, "Price and Total_Sales have a statistically testable linear relationship."),
        ("Chi-square: Contract and Churn", "H0: Contract and Churn are independent", "H1: Contract and Churn are associated", "chi-square test of independence", chi_square[0], chi_square[1], "Contract type can be compared with churn patterns, without claiming causation."),
    ]
    lines: list[str] = ["Week 7 Hypothesis Test Results", "Significance level: 0.05", ""]
    for name, h0, h1, method, statistic, p_value, interpretation in tests:
        lines.extend([f"Test Name: {name}", h0, h1, f"Test Used: {method}", f"Test Statistic: {statistic:.6f}", f"P-value: {p_value:.6g}", f"Decision: {decision(p_value)}", f"Business Interpretation: {interpretation}", ""])
    (PROJECT_DIR / "hypothesis_tests_results.txt").write_text("\n".join(lines), encoding="utf-8")

    descriptive: pd.Series = sales_values.describe()
    mode_value: typing.Any | float = sales_values.mode().iloc[0] if not sales_values.mode().empty else np.nan
    metrics = {
        "mean": mean_sales, "median": sales_values.median(), "mode": mode_value,
        "std": sales_values.std(), "min": sales_values.min(), "max": sales_values.max(),
        "q1": descriptive["25%"], "q3": descriptive["75%"], "ci_low": mean_ci[0], "ci_high": mean_ci[1],
        "margin_error": margin_error, "correlation": pearson.statistic, "correlation_p": pearson.pvalue,
        "reg_slope": regression.slope, "reg_intercept": regression.intercept, "reg_r2": regression.rvalue ** 2, "reg_p": regression.pvalue,
        "anova_p": anova.pvalue, "chi_p": chi_square[1], "one_sample_p": one_sample.pvalue,
        "quantity_sales_covariance": covariance.loc["Quantity", "Total_Sales"],
    }
    return "\n".join(lines), metrics


def create_visualizations(sales: pd.DataFrame) -> list[pathlib.Path]:
    """Create statistical visualizations from actual values."""
    VISUALIZATIONS_DIR.mkdir(exist_ok=True)
    sns.set_theme(style="whitegrid")
    paths = []

    fig, axis = plt.subplots(figsize=(9, 5))
    sns.histplot(sales["Total_Sales"], bins=12, kde=True, color="#2f6690", ax=axis)
    axis.set(title="Distribution of Total Sales", xlabel="Total Sales", ylabel="Frequency")
    fig.tight_layout(); path: pathlib.Path = VISUALIZATIONS_DIR / "distribution.png"; fig.savefig(path, dpi=150); plt.close(fig); paths.append(path)

    fig, axis = plt.subplots(figsize=(9, 5))
    sns.boxplot(data=sales, x="Region", y="Total_Sales", hue="Region", legend=False, palette="Set2", ax=axis)
    axis.set(title="Sales Spread by Region", xlabel="Region", ylabel="Total Sales")
    fig.tight_layout(); path: pathlib.Path = VISUALIZATIONS_DIR / "sales_by_region_boxplot.png"; fig.savefig(path, dpi=150); plt.close(fig); paths.append(path)

    fig, axis = plt.subplots(figsize=(9, 5))
    sns.regplot(data=sales, x="Quantity", y="Total_Sales", scatter_kws={"alpha": 0.7}, line_kws={"color": "#c0392b"}, ax=axis)
    axis.set(title="Regression: Quantity and Total Sales", xlabel="Quantity", ylabel="Total Sales")
    fig.tight_layout(); path: pathlib.Path = VISUALIZATIONS_DIR / "regression.png"; fig.savefig(path, dpi=150); plt.close(fig); paths.append(path)

    correlation: pd.DataFrame = sales[["Quantity", "Price", "Total_Sales"]].corr()
    fig, axis = plt.subplots(figsize=(7, 5))
    sns.heatmap(correlation, annot=True, fmt=".2f", cmap="YlOrRd", linewidths=0.5, ax=axis)
    axis.set_title("Correlation Heatmap")
    fig.tight_layout(); path: pathlib.Path = VISUALIZATIONS_DIR / "correlation_heatmap.png"; fig.savefig(path, dpi=150); plt.close(fig); paths.append(path)

    monthly: pd.Series = sales.groupby("Month", as_index=False)["Total_Sales"].sum()
    fig, axis = plt.subplots(figsize=(9, 5))
    sns.lineplot(data=monthly, x="Month", y="Total_Sales", marker="o", color="#7b2cbf", ax=axis)
    axis.set(title="Monthly Sales Trend", xlabel="Month", ylabel="Total Sales")
    fig.tight_layout(); path: pathlib.Path = VISUALIZATIONS_DIR / "monthly_sales.png"; fig.savefig(path, dpi=150); plt.close(fig); paths.append(path)
    return paths


def main() -> None:
    """Run the complete statistical business analysis."""
    try:
        sales, customers, quality = load_and_clean_data()
        _, metrics = run_statistics(sales, customers)
        chart_paths: list[pathlib.Path] = create_visualizations(sales)
        print("Week 7 statistical analysis completed successfully.")
        print(f"Sales shape: {sales.shape}; Customer shape: {customers.shape}")
        print(f"Missing values - sales: {quality['sales_missing']}, customers: {quality['customer_missing']}")
        print(f"Duplicates - sales: {quality['sales_duplicates']}, customers: {quality['customer_duplicates']}")
        print(f"Mean sale: {metrics['mean']:,.2f}; 95% CI: ({metrics['ci_low']:,.2f}, {metrics['ci_high']:,.2f})")
        print(f"Price/sales correlation: {metrics['correlation']:.4f}, p-value: {metrics['correlation_p']:.6g}")
        print(f"Quantity/sales covariance: {metrics['quantity_sales_covariance']:,.2f}")
        print(f"Regression R-squared: {metrics['reg_r2']:.4f}, p-value: {metrics['reg_p']:.6g}")
        print("Generated charts:")
        for path in chart_paths:
            print(f"- {path.relative_to(PROJECT_DIR)}")
    except Exception:
        print("Analysis failed.")


if __name__ == "__main__":
    main()
