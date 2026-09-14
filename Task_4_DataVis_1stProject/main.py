"""Complete sales analysis and visualization project for Week 4."""

import pathlib

import matplotlib.pyplot as plt
import pandas as pd


PROJECT_DIR: pathlib.Path = pathlib.Path(__file__).parent
DATA_FILE: pathlib.Path = PROJECT_DIR / "data" / "sales_data.csv"
VISUALIZATIONS_DIR: pathlib.Path = PROJECT_DIR / "visualizations"
REQUIRED_COLUMNS: set[str] = {"Product", "Quantity", "Price", "Total_Sales"}


def load_and_validate_data(file_path: pathlib.Path) -> pd.DataFrame:
    """Load the CSV and validate the fields needed by the analysis."""
    if not file_path.exists():
        raise FileNotFoundError(f"CSV file was not found: {file_path}")

    try:
        data: pd.DataFrame = pd.read_csv(file_path)
    except Exception:
        raise ValueError("The CSV file could not be read or parsed.")

    if data.empty:
        raise ValueError("The dataset contains no rows.")

    missing_columns: set[str] = REQUIRED_COLUMNS - set(data.columns)
    if missing_columns:
        missing: str = ", ".join(sorted(missing_columns))
        raise ValueError(f"Missing required columns: {missing}")

    numeric_columns: list[str] = ["Quantity", "Price", "Total_Sales"]
    for column in numeric_columns:
        data[column] = pd.to_numeric(data[column], errors="coerce")

    if data[numeric_columns].isna().any().any():
        raise ValueError("The dataset contains invalid numeric values.")

    if "Date" in data.columns:
        data["Date"] = pd.to_datetime(data["Date"], errors="coerce")
        if data["Date"].isna().any():
            raise ValueError("The dataset contains invalid dates.")

    return data


def clean_data(data: pd.DataFrame) -> tuple[pd.DataFrame, int, int]:
    """Remove missing and duplicate records from an in-memory copy."""
    cleaned_data: pd.DataFrame = data.copy()
    missing_before = int(cleaned_data.isna().sum().sum())
    duplicate_count = int(cleaned_data.duplicated().sum())

    # Cleaning happens in memory so the provided source CSV is never overwritten.
    cleaned_data: pd.DataFrame = cleaned_data.dropna().drop_duplicates().copy()
    return cleaned_data, missing_before, duplicate_count


def create_visualizations(data: pd.DataFrame) -> list[pathlib.Path]:
    """Create and save charts based on the cleaned data."""
    VISUALIZATIONS_DIR.mkdir(exist_ok=True)
    chart_paths: list[pathlib.Path] = []

    product_sales: pd.Series = data.groupby("Product")["Total_Sales"].sum().sort_values()
    fig, axis = plt.subplots(figsize=(9, 5))
    product_sales.plot(kind="bar", ax=axis, color="#2f6690", label="Total sales")
    axis.set_title("Total Sales by Product")
    axis.set_xlabel("Product")
    axis.set_ylabel("Sales")
    axis.legend()
    axis.tick_params(axis="x", rotation=30)
    fig.tight_layout()
    product_path: pathlib.Path = VISUALIZATIONS_DIR / "sales_by_product.png"
    fig.savefig(product_path, dpi=150)
    plt.close(fig)
    chart_paths.append(product_path)

    if "Date" in data.columns:
        daily_sales: pd.Series = data.groupby("Date")["Total_Sales"].sum().sort_index()
        fig, axis = plt.subplots(figsize=(10, 5))
        daily_sales.plot(ax=axis, color="#d1495b", linewidth=2, label="Daily sales")
        axis.set_title("Sales Trend Over Time")
        axis.set_xlabel("Date")
        axis.set_ylabel("Sales")
        axis.legend()
        fig.autofmt_xdate()
        fig.tight_layout()
        trend_path: pathlib.Path = VISUALIZATIONS_DIR / "sales_trend.png"
        fig.savefig(trend_path, dpi=150)
        plt.close(fig)
        chart_paths.append(trend_path)

    if "Region" in data.columns:
        region_sales: pd.Series = data.groupby("Region")["Total_Sales"].sum().sort_values()
        fig, axis = plt.subplots(figsize=(9, 5))
        region_sales.plot(kind="bar", ax=axis, color="#55a630", label="Total sales")
        axis.set_title("Total Sales by Region")
        axis.set_xlabel("Region")
        axis.set_ylabel("Sales")
        axis.legend()
        axis.tick_params(axis="x", rotation=0)
        fig.tight_layout()
        region_path: pathlib.Path = VISUALIZATIONS_DIR / "sales_by_region.png"
        fig.savefig(region_path, dpi=150)
        plt.close(fig)
        chart_paths.append(region_path)

    # Show each product's share of total sales as a percentage.
    product_distribution: pd.Series = data.groupby("Product")["Total_Sales"].sum()
    fig, axis = plt.subplots(figsize=(8, 8))
    product_distribution.plot(
        kind="pie",
        ax=axis,
        autopct="%1.1f%%",
        startangle=90,
        ylabel="",
        labeldistance=None,
    )
    axis.set_title("Sales Distribution by Product")
    axis.legend(product_distribution.index, title="Product", loc="center left", bbox_to_anchor=(1, 0.5))
    fig.tight_layout()
    distribution_path: pathlib.Path = VISUALIZATIONS_DIR / "sales_distribution_by_product.png"
    fig.savefig(distribution_path, dpi=150)
    plt.close(fig)
    chart_paths.append(distribution_path)

    return chart_paths


def print_report(data: pd.DataFrame, missing_count: int, duplicate_count: int) -> None:
    """Print the main findings in a readable format."""
    product_sales: pd.Series = data.groupby("Product")["Total_Sales"].sum().sort_values(ascending=False)
    print("\n" + "=" * 60)
    print("WEEK 4 - COMPLETE SALES ANALYSIS PROJECT")
    print("=" * 60)
    print(f"Rows: {len(data)} | Columns: {len(data.columns)}")
    print(f"Missing values found: {missing_count}")
    print(f"Duplicate rows found: {duplicate_count}")
    print(f"Total sales: {data['Total_Sales'].sum():,.2f}")
    print(f"Average sale: {data['Total_Sales'].mean():,.2f}")
    print(f"Maximum sale: {data['Total_Sales'].max():,.2f}")
    print(f"Minimum sale: {data['Total_Sales'].min():,.2f}")
    print(f"Total quantity sold: {data['Quantity'].sum():,}")
    print(f"Best-selling product: {product_sales.index[0]}")
    print("\nSales by product:")
    print(product_sales.to_string())

    if "Region" in data.columns:
        print("\nSales by region:")
        print(data.groupby("Region")["Total_Sales"].sum().sort_values(ascending=False).to_string())


def main() -> None:
    """Run the complete load, clean, analyze, and visualize workflow."""
    try:
        raw_data: pd.DataFrame = load_and_validate_data(DATA_FILE)
        print("First 5 rows:")
        print(raw_data.head())
        print(f"\nDataset shape: {raw_data.shape}")
        print(f"Columns: {list(raw_data.columns)}")
        print("\nData types:")
        print(raw_data.dtypes)
        print("\nBasic statistics:")
        print(raw_data.describe())

        cleaned_data, missing_count, duplicate_count = clean_data(raw_data)
        if cleaned_data.empty:
            raise ValueError("No rows remain after cleaning.")

        chart_paths: list[pathlib.Path] = create_visualizations(cleaned_data)
        print_report(cleaned_data, missing_count, duplicate_count)
        print("\nCharts saved:")
        for chart_path in chart_paths:
            print(f"- {chart_path.relative_to(PROJECT_DIR)}")
    except Exception:
        print("Analysis could not be completed.")


if __name__ == "__main__":
    main()
