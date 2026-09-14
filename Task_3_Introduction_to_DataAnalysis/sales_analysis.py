"""Beginner-friendly sales data analysis using Pandas."""

import pathlib

import pandas as pd
from pandas import DataFrame, Series


DATA_FILE: pathlib.Path = pathlib.Path(__file__).with_name("sales_data.csv")


def main() -> None:
    """Load, inspect, clean, and summarize the sales dataset."""
    # Load the provided CSV file without changing the source file.
    sales_data: DataFrame = pd.read_csv(DATA_FILE)

    print("=" * 60)
    print("SALES DATA ANALYSIS")
    print("=" * 60)
    print("\nFirst 5 rows:")
    print(sales_data.head())

    print("\nDataset information:")
    sales_data.info()
    print(f"\nShape: {sales_data.shape}")
    print(f"Columns: {list(sales_data.columns)}")
    print("\nData types:")
    print(sales_data.dtypes)
    print("\nBasic statistics:")
    print(sales_data.describe())

    print("\nMissing values by column:")
    missing_values: Series = sales_data.isna().sum()
    print(missing_values)
    print(f"Total missing values: {int(missing_values.sum())}")

    duplicate_count = int(sales_data.duplicated().sum())
    print(f"\nDuplicate rows: {duplicate_count}")

    # Work on an in-memory copy so the provided CSV remains unchanged.
    cleaned_data: DataFrame = sales_data.copy()
    numeric_columns: list[str] = ["Quantity", "Price", "Total_Sales"]
    available_numeric_columns: list[str] = [
        column for column in numeric_columns if column in cleaned_data.columns
    ]
    for column in available_numeric_columns:
        cleaned_data[column] = pd.to_numeric(cleaned_data[column], errors="coerce")

    invalid_numeric_rows: Series = cleaned_data[available_numeric_columns].isna().any(axis=1)
    if invalid_numeric_rows.any():
        cleaned_data: DataFrame = cleaned_data.loc[~invalid_numeric_rows].copy()
        print(f"Removed {int(invalid_numeric_rows.sum())} rows with invalid numeric values.")

    if cleaned_data.isna().any().any():
        rows_before_cleaning: int = len(cleaned_data)
        cleaned_data: DataFrame = cleaned_data.dropna().copy()
        print(f"Removed {rows_before_cleaning - len(cleaned_data)} rows with missing values.")
    else:
        print("No missing values required cleaning.")

    if duplicate_count:
        cleaned_data: DataFrame = cleaned_data.drop_duplicates().copy()
        print(f"Removed {duplicate_count} duplicate rows.")
    else:
        print("No duplicate rows required cleaning.")

    total_sales = cleaned_data["Total_Sales"].sum()
    average_sales: float = cleaned_data["Total_Sales"].mean()
    maximum_sale = cleaned_data["Total_Sales"].max()
    minimum_sale = cleaned_data["Total_Sales"].min()
    total_quantity = cleaned_data["Quantity"].sum()
    sales_by_product: Series = cleaned_data.groupby("Product")["Total_Sales"].sum().sort_values(ascending=False)
    best_product: int | str = sales_by_product.idxmax()

    print("\n" + "=" * 60)
    print("SALES ANALYSIS REPORT")
    print("=" * 60)
    print(f"Total sales: {total_sales:,.2f}")
    print(f"Average sale: {average_sales:,.2f}")
    print(f"Maximum sale: {maximum_sale:,.2f}")
    print(f"Minimum sale: {minimum_sale:,.2f}")
    print(f"Total quantity sold: {total_quantity:,}")
    print(f"Unique products: {cleaned_data['Product'].nunique():,}")

    if "Customer_ID" in cleaned_data.columns:
        print(f"Unique customers: {cleaned_data['Customer_ID'].nunique():,}")

    print(f"Best-selling product by total sales: {best_product}")
    print("\nSales by product:")
    print(sales_by_product.to_string())

    if "Region" in cleaned_data.columns:
        print("\nSales by region:")
        print(cleaned_data.groupby("Region")["Total_Sales"].sum().sort_values(ascending=False).to_string())


if __name__ == "__main__":
    main()
