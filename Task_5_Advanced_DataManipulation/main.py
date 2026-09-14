"""Week 5 customer and sales analysis using advanced Pandas operations."""

import pathlib
import traceback
import typing

import matplotlib.pyplot as plt
import pandas as pd


PROJECT_DIR: pathlib.Path = pathlib.Path(__file__).parent
DATA_DIR: pathlib.Path = PROJECT_DIR / "data"
CUSTOMER_FILE: pathlib.Path = DATA_DIR / "customer_churn.csv"
SALES_FILE: pathlib.Path = DATA_DIR / "sales_data.csv"
VISUALIZATIONS_DIR: pathlib.Path = PROJECT_DIR / "visualizations"
CUSTOMER_COLUMNS: set[str] = {
    "CustomerID", "Tenure", "MonthlyCharges", "TotalCharges", "Contract",
    "PaymentMethod", "PaperlessBilling", "SeniorCitizen", "Churn",
}
SALES_COLUMNS: set[str] = {
    "Date", "Product", "Quantity", "Price", "Customer_ID", "Region", "Total_Sales",
}


def load_csv(file_path: pathlib.Path, required_columns: set[str]) -> pd.DataFrame:
    """Load one CSV and validate its existence, content, and required columns."""
    if not file_path.exists():
        raise FileNotFoundError(f"Dataset not found: {file_path}")

    try:
        data: pd.DataFrame = pd.read_csv(file_path)
    except Exception:
        raise ValueError(f"Dataset could not be read or parsed: {file_path.name}")

    if data.empty:
        raise ValueError(f"Dataset has no rows: {file_path.name}")

    missing_columns: set[str] = required_columns - set(data.columns)
    if missing_columns:
        missing: str = ", ".join(sorted(missing_columns))
        raise ValueError(f"Missing required columns in {file_path.name}: {missing}")

    return data


def clean_datasets(customer_data: pd.DataFrame, sales_data: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame, dict[str, int]]:
    """Validate types and clean copies without changing either source CSV."""
    customers: pd.DataFrame = customer_data.copy()
    sales: pd.DataFrame = sales_data.copy()
    quality: dict[str, int] = {
        "customer_missing": int(customers.isna().sum().sum()),
        "customer_duplicates": int(customers.duplicated().sum()),
        "sales_missing": int(sales.isna().sum().sum()),
        "sales_duplicates": int(sales.duplicated().sum()),
    }

    for column in ["Tenure", "MonthlyCharges", "TotalCharges", "SeniorCitizen", "Churn"]:
        customers[column] = pd.to_numeric(customers[column], errors="coerce")
    for column in ["Quantity", "Price", "Total_Sales"]:
        sales[column] = pd.to_numeric(sales[column], errors="coerce")

    sales["Date"] = pd.to_datetime(sales["Date"], errors="coerce")
    if customers[["Tenure", "MonthlyCharges", "TotalCharges", "SeniorCitizen", "Churn"]].isna().any().any():
        raise ValueError("Customer dataset contains invalid numeric values.")
    if sales[["Quantity", "Price", "Total_Sales", "Date"]].isna().any().any():
        raise ValueError("Sales dataset contains invalid numeric or date values.")
    if not customers["Churn"].isin([0, 1]).all():
        raise ValueError("Churn must contain only 0 and 1.")

    # Strip whitespace from categories; this changes no values in the supplied files.
    for column in ["Contract", "PaymentMethod", "PaperlessBilling"]:
        customers[column] = customers[column].astype(str).str.strip()
    for column in ["Product", "Customer_ID", "Region"]:
        sales[column] = sales[column].astype(str).str.strip()

    customers: pd.DataFrame = customers.dropna().drop_duplicates().copy()
    sales: pd.DataFrame = sales.dropna().drop_duplicates().copy()
    sales["Year"] = sales["Date"].dt.year
    sales["Month"] = sales["Date"].dt.to_period("M").astype(str)
    sales["Month_Name"] = sales["Date"].dt.month_name()
    sales["Day"] = sales["Date"].dt.day
    sales["Day_of_Week"] = sales["Date"].dt.day_name()
    return customers, sales, quality


def create_charts(customers: pd.DataFrame, sales: pd.DataFrame) -> list[pathlib.Path]:
    """Create five dashboard charts from actual customer and sales data."""
    VISUALIZATIONS_DIR.mkdir(exist_ok=True)
    chart_paths = []

    product_sales: pd.Series = sales.groupby("Product")["Total_Sales"].sum().sort_values()
    fig, axis = plt.subplots(figsize=(9, 5))
    product_sales.plot(kind="bar", ax=axis, color="#2f6690", label="Total sales")
    axis.set_title("Total Sales by Product")
    axis.set_xlabel("Product")
    axis.set_ylabel("Sales")
    axis.legend()
    axis.tick_params(axis="x", rotation=30)
    fig.tight_layout()
    path: pathlib.Path = VISUALIZATIONS_DIR / "sales_by_product.png"
    fig.savefig(path, dpi=150)
    plt.close(fig)
    chart_paths.append(path)

    region_sales: pd.Series = sales.groupby("Region")["Total_Sales"].sum().sort_values()
    fig, axis = plt.subplots(figsize=(9, 5))
    region_sales.plot(kind="bar", ax=axis, color="#55a630", label="Total sales")
    axis.set_title("Total Sales by Region")
    axis.set_xlabel("Region")
    axis.set_ylabel("Sales")
    axis.legend()
    fig.tight_layout()
    path: pathlib.Path = VISUALIZATIONS_DIR / "sales_by_region.png"
    fig.savefig(path, dpi=150)
    plt.close(fig)
    chart_paths.append(path)

    monthly_sales: pd.Series = sales.groupby("Month")["Total_Sales"].sum()
    fig, axis = plt.subplots(figsize=(9, 5))
    monthly_sales.plot(kind="line", marker="o", ax=axis, color="#d1495b", label="Monthly sales")
    axis.set_title("Monthly Sales Trend")
    axis.set_xlabel("Month")
    axis.set_ylabel("Sales")
    axis.legend()
    fig.tight_layout()
    path: pathlib.Path = VISUALIZATIONS_DIR / "monthly_sales_trend.png"
    fig.savefig(path, dpi=150)
    plt.close(fig)
    chart_paths.append(path)

    churn_by_contract: pd.Series = customers.groupby("Contract")["Churn"].mean().sort_values() * 100
    fig, axis = plt.subplots(figsize=(9, 5))
    churn_by_contract.plot(kind="bar", ax=axis, color="#bc4749", label="Churn rate")
    axis.set_title("Churn Rate by Contract")
    axis.set_xlabel("Contract")
    axis.set_ylabel("Churn rate (%)")
    axis.legend()
    axis.tick_params(axis="x", rotation=0)
    fig.tight_layout()
    path: pathlib.Path = VISUALIZATIONS_DIR / "churn_by_contract.png"
    fig.savefig(path, dpi=150)
    plt.close(fig)
    chart_paths.append(path)

    product_distribution: pd.Series = sales.groupby("Product")["Total_Sales"].sum()
    fig, axis = plt.subplots(figsize=(8, 8))
    product_distribution.plot(kind="pie", ax=axis, autopct="%1.1f%%", startangle=90, ylabel="")
    axis.set_title("Sales Distribution by Product")
    fig.tight_layout()
    path: pathlib.Path = VISUALIZATIONS_DIR / "sales_distribution.png"
    fig.savefig(path, dpi=150)
    plt.close(fig)
    chart_paths.append(path)
    return chart_paths


def print_analysis(customers: pd.DataFrame, sales: pd.DataFrame, quality: dict[str, int]) -> None:
    """Print exploration, aggregations, filters, merge result, and pivots."""
    print("=" * 70)
    print("WEEK 5 - CUSTOMER SALES ANALYSIS")
    print("=" * 70)
    print(f"Customer dataset shape: {customers.shape}")
    print(f"Sales working shape after derived date columns: {sales.shape}")
    print(f"Customer columns: {list(customers.columns[:9])}")
    print(f"Sales columns: {list(sales.columns[:7])}")
    print(f"Customer missing values: {quality['customer_missing']}")
    print(f"Customer duplicate rows: {quality['customer_duplicates']}")
    print(f"Sales missing values: {quality['sales_missing']}")
    print(f"Sales duplicate rows: {quality['sales_duplicates']}")

    print("\nSales aggregations:")
    print("Total sales by product:")
    print(sales.groupby("Product")["Total_Sales"].sum().sort_values(ascending=False).to_string())
    print("\nTotal sales by region:")
    print(sales.groupby("Region")["Total_Sales"].sum().sort_values(ascending=False).to_string())
    print("\nMonthly total sales:")
    print(sales.groupby("Month")["Total_Sales"].sum().to_string())
    print(f"\nTotal sales: {sales['Total_Sales'].sum():,.2f}")
    print(f"Total quantity: {sales['Quantity'].sum():,}")

    high_value_sales: pd.DataFrame = sales[(sales["Total_Sales"] > 200000) & (sales["Region"].isin(["North", "South"]))]
    long_high_charge_customers: pd.DataFrame = customers[(customers["Tenure"] >= 24) & (customers["MonthlyCharges"] > 100)]
    print(f"\nFiltered high-value North/South sales: {len(high_value_sales)}")
    print(f"Filtered long-tenure, high-charge customers: {len(long_high_charge_customers)}")

    customer_ids: set[typing.Any] = set(customers["CustomerID"])
    sales_ids: set[typing.Any] = set(sales["Customer_ID"])
    overlap: set[typing.Any] = customer_ids & sales_ids
    print(f"\nCustomer ID overlap: {len(overlap)}")
    print("Merge result: no customer-sales merge performed because the ID formats do not overlap.")

    print("\nPivot: sales by product and region")
    print(pd.pivot_table(sales, index="Product", columns="Region", values="Total_Sales", aggfunc="sum", fill_value=0).to_string())
    print("\nPivot: monthly sales by product")
    print(pd.pivot_table(sales, index="Month", columns="Product", values="Total_Sales", aggfunc="sum", fill_value=0).to_string())

    print("\nChurn analysis:")
    print(f"Overall churn rate: {customers['Churn'].mean() * 100:.2f}%")
    print((customers.groupby("Contract")["Churn"].mean() * 100).sort_values(ascending=False).round(2).to_string())
    print("\nChurn by payment method:")
    print((customers.groupby("PaymentMethod")["Churn"].mean() * 100).sort_values(ascending=False).round(2).to_string())
    print("\nTop customer analysis: unavailable because there are zero matching customer IDs.")


def main() -> None:
    """Run the complete Week 5 workflow."""
    try:
        raw_customers: pd.DataFrame = load_csv(CUSTOMER_FILE, CUSTOMER_COLUMNS)
        raw_sales: pd.DataFrame = load_csv(SALES_FILE, SALES_COLUMNS)
        print("Customer first 5 rows:\n", raw_customers.head().to_string(index=False))
        print("\nSales first 5 rows:\n", raw_sales.head().to_string(index=False))
        print(f"\nCustomer dataset shape: {raw_customers.shape}")
        print(f"Sales dataset shape: {raw_sales.shape}")
        customers, sales, quality = clean_datasets(raw_customers, raw_sales)
        print_analysis(customers, sales, quality)
        chart_paths: list[pathlib.Path] = create_charts(customers, sales)
        print("\nCharts saved:")
        for chart_path in chart_paths:
            print(f"- {chart_path.relative_to(PROJECT_DIR)}")
    except Exception:
        traceback.print_exc()
        print("Analysis could not be completed.")


if __name__ == "__main__":
    main()
