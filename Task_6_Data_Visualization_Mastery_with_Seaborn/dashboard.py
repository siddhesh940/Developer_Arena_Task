"""Week 6 Seaborn analysis and interactive Plotly sales dashboard."""

import pathlib
import typing

import matplotlib.pyplot as plt
import pandas as pd
import plotly.graph_objects as go
import seaborn as sns


PROJECT_DIR: pathlib.Path = pathlib.Path(__file__).parent
DATA_FILE: pathlib.Path = PROJECT_DIR / "sales_data.csv"
VISUALIZATIONS_DIR: pathlib.Path = PROJECT_DIR / "visualizations"
REQUIRED_COLUMNS: set[str] = {
    "Date", "Product", "Quantity", "Price", "Customer_ID", "Region", "Total_Sales",
}


def load_data() -> pd.DataFrame:
    """Load and validate the supplied sales CSV."""
    if not DATA_FILE.exists():
        raise FileNotFoundError(f"Sales dataset not found: {DATA_FILE}")

    try:
        data: pd.DataFrame = pd.read_csv(DATA_FILE)
    except Exception:
        raise ValueError("The sales dataset could not be read or parsed.")

    if data.empty:
        raise ValueError("The sales dataset contains no rows.")

    missing_columns: set[str] = REQUIRED_COLUMNS - set(data.columns)
    if missing_columns:
        raise ValueError(f"Missing required columns: {', '.join(sorted(missing_columns))}")

    data["Date"] = pd.to_datetime(data["Date"], errors="coerce")
    numeric_columns: list[str] = ["Quantity", "Price", "Total_Sales"]
    for column in numeric_columns:
        data[column] = pd.to_numeric(data[column], errors="coerce")

    if data.isna().any().any():
        raise ValueError("The dataset contains missing or invalid values after validation.")
    if (data[numeric_columns] < 0).any().any():
        raise ValueError("Numeric sales values cannot be negative.")

    data: pd.DataFrame = data.drop_duplicates().copy()
    data["Month"] = data["Date"].dt.to_period("M").astype(str)
    data["Month_Name"] = data["Date"].dt.strftime("%b %Y")
    return data


def save_seaborn_charts(data: pd.DataFrame) -> list[pathlib.Path]:
    """Create five meaningful static charts with Seaborn."""
    VISUALIZATIONS_DIR.mkdir(exist_ok=True)
    sns.set_theme(style="whitegrid", palette="deep")
    chart_paths = []

    product_sales = data.groupby("Product", as_index=False)["Total_Sales"].sum().sort_values("Total_Sales")
    fig, axis = plt.subplots(figsize=(9, 5))
    sns.barplot(data=product_sales, x="Product", y="Total_Sales", hue="Product", legend=False, ax=axis, palette="Blues_d")
    axis.set_title("Total Sales by Product")
    axis.set_xlabel("Product")
    axis.set_ylabel("Total Sales")
    axis.tick_params(axis="x", rotation=30)
    fig.tight_layout()
    path: pathlib.Path = VISUALIZATIONS_DIR / "sales_by_product.png"
    fig.savefig(path, dpi=150)
    plt.close(fig)
    chart_paths.append(path)

    monthly_sales: pd.Series = data.groupby("Month", as_index=False)["Total_Sales"].sum()
    fig, axis = plt.subplots(figsize=(10, 5))
    sns.lineplot(data=monthly_sales, x="Month", y="Total_Sales", marker="o", linewidth=2.5, color="#d1495b", ax=axis)
    axis.set_title("Monthly Sales Trend")
    axis.set_xlabel("Month")
    axis.set_ylabel("Total Sales")
    fig.tight_layout()
    path: pathlib.Path = VISUALIZATIONS_DIR / "sales_trend.png"
    fig.savefig(path, dpi=150)
    plt.close(fig)
    chart_paths.append(path)

    region_sales = data.groupby("Region", as_index=False)["Total_Sales"].sum().sort_values("Total_Sales")
    fig, axis = plt.subplots(figsize=(9, 5))
    sns.barplot(data=region_sales, x="Region", y="Total_Sales", hue="Region", legend=False, ax=axis, palette="Greens_d")
    axis.set_title("Total Sales by Region")
    axis.set_xlabel("Region")
    axis.set_ylabel("Total Sales")
    fig.tight_layout()
    path: pathlib.Path = VISUALIZATIONS_DIR / "sales_by_region.png"
    fig.savefig(path, dpi=150)
    plt.close(fig)
    chart_paths.append(path)

    fig, axis = plt.subplots(figsize=(9, 5))
    sns.histplot(data=data, x="Total_Sales", bins=12, kde=True, color="#7b2cbf", ax=axis)
    axis.set_title("Distribution of Individual Sales Values")
    axis.set_xlabel("Total Sales")
    axis.set_ylabel("Number of Transactions")
    fig.tight_layout()
    path: pathlib.Path = VISUALIZATIONS_DIR / "sales_distribution.png"
    fig.savefig(path, dpi=150)
    plt.close(fig)
    chart_paths.append(path)

    numeric_data: pd.DataFrame = data[["Quantity", "Price", "Total_Sales"]]
    fig, axis = plt.subplots(figsize=(7, 5))
    sns.heatmap(numeric_data.corr(), annot=True, cmap="YlOrRd", fmt=".2f", linewidths=0.5, ax=axis)
    axis.set_title("Correlation Between Numeric Sales Variables")
    fig.tight_layout()
    path: pathlib.Path = VISUALIZATIONS_DIR / "correlation_heatmap.png"
    fig.savefig(path, dpi=150)
    plt.close(fig)
    chart_paths.append(path)
    return chart_paths


def create_plotly_dashboard(data: pd.DataFrame) -> pathlib.Path:
    """Create one interactive HTML dashboard with hover, zoom, and a product dropdown."""
    product_names: list[typing.Any] = sorted(data["Product"].unique())
    product_sales: pd.Series = data.groupby("Product")["Total_Sales"].sum().reindex(product_names)
    region_sales: pd.Series = data.groupby("Region")["Total_Sales"].sum().sort_values(ascending=False)
    monthly_sales: pd.Series = data.groupby("Month")["Total_Sales"].sum()
    product_monthly: pd.DataFrame = data.pivot_table(index="Month", columns="Product", values="Total_Sales", aggfunc="sum", fill_value=0)

    monthly_chart = go.Figure(go.Scatter(
        x=monthly_sales.index,
        y=monthly_sales.values,
        mode="lines+markers",
        name="All Products",
        line={"color": "#49c6b5", "width": 3},
        marker={"size": 9},
        hovertemplate="Month: %{x}<br>Sales: %{y:,.0f}<extra></extra>",
    ))
    buttons = [{"label": "All Products", "method": "update", "args": [{"y": [monthly_sales.values], "name": ["All Products"]}]}]
    for product in product_names:
        buttons.append({"label": product, "method": "update", "args": [{"y": [product_monthly[product].values], "name": [product]}, {"title": {"text": f"Monthly Sales Trend - {product}"}}]})
    monthly_chart.update_layout(
        title="Monthly Sales Trend",
        template="plotly_dark",
        height=390,
        margin={"l": 55, "r": 25, "t": 70, "b": 55},
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font={"color": "#dbe7e5"},
        xaxis={"title": "Month", "gridcolor": "#294047"},
        yaxis={"title": "Total Sales", "gridcolor": "#294047"},
        updatemenus=[{"buttons": buttons, "direction": "down", "showactive": True, "x": 0.78, "y": 1.22, "bgcolor": "#18343a", "font": {"color": "#e9f4f1"}}],
    )

    product_chart = go.Figure(go.Bar(x=product_sales.index, y=product_sales.values, name="Product Sales", marker_color="#49c6b5", hovertemplate="%{x}<br>Sales: %{y:,.0f}<extra></extra>"))
    product_chart.update_layout(title="Sales by Product", template="plotly_dark", height=350, margin={"l": 55, "r": 25, "t": 65, "b": 55}, paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", font={"color": "#dbe7e5"}, xaxis={"title": "Product", "gridcolor": "#294047"}, yaxis={"title": "Total Sales", "gridcolor": "#294047"})
    region_chart = go.Figure(go.Bar(x=region_sales.index, y=region_sales.values, name="Regional Sales", marker_color="#efb366", hovertemplate="%{x}<br>Sales: %{y:,.0f}<extra></extra>"))
    region_chart.update_layout(title="Sales by Region", template="plotly_dark", height=350, margin={"l": 55, "r": 25, "t": 65, "b": 55}, paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", font={"color": "#dbe7e5"}, xaxis={"title": "Region", "gridcolor": "#294047"}, yaxis={"title": "Total Sales", "gridcolor": "#294047"})

    chart_options = {"responsive": True, "displaylogo": False, "modeBarButtonsToRemove": ["lasso2d", "select2d"]}
    monthly_html: str = monthly_chart.to_html(full_html=False, include_plotlyjs="cdn", config=chart_options)
    product_html: str = product_chart.to_html(full_html=False, include_plotlyjs=False, config=chart_options)
    region_html: str = region_chart.to_html(full_html=False, include_plotlyjs=False, config=chart_options)
    total_sales = data["Total_Sales"].sum()
    total_quantity = data["Quantity"].sum()
    best_product: int | str = product_sales.idxmax()
    best_region: int | str = region_sales.idxmax()
    output_path: pathlib.Path = PROJECT_DIR / "dashboard.html"
    html: str = f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>Interactive Sales Dashboard</title>
<style>
:root {{ --ink:#e9f4f1; --muted:#8fa9a8; --panel:#12252b; --panel2:#173139; --line:#294047; --accent:#49c6b5; --gold:#efb366; }}
* {{ box-sizing:border-box; }} body {{ margin:0; min-height:100vh; background:#0a151a; color:var(--ink); font-family:Segoe UI,Arial,sans-serif; }}
.shell {{ width:min(1320px, calc(100% - 40px)); margin:0 auto; padding:42px 0 55px; }}
.hero {{ display:flex; justify-content:space-between; align-items:flex-end; gap:25px; padding-bottom:30px; border-bottom:1px solid var(--line); }}
.eyebrow {{ color:var(--accent); font-size:12px; font-weight:700; letter-spacing:2px; text-transform:uppercase; }} h1 {{ margin:8px 0 8px; font-size:clamp(30px, 4vw, 54px); letter-spacing:-1px; }} .subtitle {{ margin:0; color:var(--muted); font-size:15px; }}
.stamp {{ color:var(--muted); font-size:13px; text-align:right; }}
.kpis {{ display:grid; grid-template-columns:repeat(4,1fr); gap:14px; margin:24px 0; }} .kpi {{ padding:20px; background:var(--panel); border:1px solid var(--line); border-radius:12px; box-shadow:0 12px 30px #00000020; }} .kpi-label {{ color:var(--muted); font-size:12px; text-transform:uppercase; letter-spacing:1px; }} .kpi-value {{ margin-top:8px; font-size:28px; font-weight:700; }} .kpi-accent {{ color:var(--accent); }}
.panel {{ background:var(--panel); border:1px solid var(--line); border-radius:12px; padding:16px; margin-bottom:16px; box-shadow:0 12px 30px #00000020; }} .panel-title {{ margin:0 0 4px 4px; font-size:16px; }} .panel-note {{ margin:0 0 8px 4px; color:var(--muted); font-size:13px; }} .grid {{ display:grid; grid-template-columns:1fr 1fr; gap:16px; }}
.footer {{ color:var(--muted); font-size:12px; padding-top:18px; }}
@media (max-width:800px) {{ .shell {{ width:min(100% - 24px, 650px); padding-top:24px; }} .hero {{ display:block; }} .stamp {{ text-align:left; margin-top:15px; }} .kpis {{ grid-template-columns:1fr 1fr; }} .grid {{ grid-template-columns:1fr; }} }}
@media (max-width:440px) {{ .kpis {{ grid-template-columns:1fr; }} }}
</style></head><body><main class="shell">
<header class="hero"><div><div class="eyebrow">Sales intelligence / 2024</div><h1>Interactive Sales Dashboard</h1><p class="subtitle">A clear view of product momentum, regional performance, and monthly revenue.</p></div><div class="stamp">100 transactions<br>Jan 01 - Apr 09, 2024</div></header>
<section class="kpis"><div class="kpi"><div class="kpi-label">Total Sales</div><div class="kpi-value kpi-accent">{total_sales:,.0f}</div></div><div class="kpi"><div class="kpi-label">Total Quantity</div><div class="kpi-value">{total_quantity:,}</div></div><div class="kpi"><div class="kpi-label">Best Product</div><div class="kpi-value">{best_product}</div></div><div class="kpi"><div class="kpi-label">Top Region</div><div class="kpi-value">{best_region}</div></div></section>
<section class="panel"><h2 class="panel-title">Revenue pulse</h2><p class="panel-note">Use the dropdown to isolate a product. Hover points for exact values.</p>{monthly_html}</section>
<section class="grid"><div class="panel"><h2 class="panel-title">Product performance</h2>{product_html}</div><div class="panel"><h2 class="panel-title">Regional performance</h2>{region_html}</div></section>
<footer class="footer">Built with Pandas and Plotly. Charts support hover, zoom, pan, and responsive resizing.</footer>
</main></body></html>"""
    output_path.write_text(html, encoding="utf-8")
    return output_path


def main() -> None:
    """Run validation, analysis, static charts, and interactive dashboard creation."""
    try:
        data: pd.DataFrame = load_data()
        print(f"Dataset shape: {data.shape}")
        print(f"Missing values: {int(data.isna().sum().sum())}")
        print(f"Duplicate rows after cleaning: {int(data.duplicated().sum())}")
        print(f"Total sales: {data['Total_Sales'].sum():,.2f}")
        print(f"Total quantity: {data['Quantity'].sum():,}")
        print(f"Products: {data['Product'].nunique()}")
        print(f"Regions: {data['Region'].nunique()}")
        print(f"Best-selling product: {data.groupby('Product')['Total_Sales'].sum().idxmax()}")
        chart_paths: list[pathlib.Path] = save_seaborn_charts(data)
        dashboard_path: pathlib.Path = create_plotly_dashboard(data)
        print("Static charts saved:")
        for path in chart_paths:
            print(f"- {path.relative_to(PROJECT_DIR)}")
        print(f"Interactive dashboard saved: {dashboard_path.name}")
    except Exception:
        print("Dashboard could not be created.")


if __name__ == "__main__":
    main()
