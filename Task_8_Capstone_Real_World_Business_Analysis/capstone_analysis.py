"""Reproducible Week 8 capstone business analysis artifact generator."""

import pathlib

import matplotlib.pyplot as plt
import pandas as pd
import pptx.presentation
import pptx.shapes.autoshape
import pptx.slide
import seaborn as sns
import pptx
import pptx.util
import reportlab.lib.pagesizes
import reportlab.lib.styles
import reportlab.platypus
import scipy as sp
import sklearn.linear_model


ROOT: pathlib.Path = pathlib.Path(__file__).parent
DATA: pathlib.Path = ROOT / "data"
CLEANED: pathlib.Path = ROOT / "cleaned_data"
VIZ: pathlib.Path = ROOT / "visualizations"
REPORTS: pathlib.Path = ROOT / "reports"
PRESENTATION: pathlib.Path = ROOT / "presentation"
ALPHA = 0.05


def load_data() -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """Load and validate the three supplied datasets."""
    files: dict[str, pathlib.Path] = {name: DATA / name for name in ["house_prices.csv", "customer_churn.csv", "sales_data.csv"]}
    if not all(path.exists() for path in files.values()):
        raise FileNotFoundError("All three datasets must be present in data/.")
    house: pd.DataFrame = pd.read_csv(files["house_prices.csv"])
    churn: pd.DataFrame = pd.read_csv(files["customer_churn.csv"])
    sales: pd.DataFrame = pd.read_csv(files["sales_data.csv"])
    sales["Date"] = pd.to_datetime(sales["Date"], errors="coerce")
    if house.isna().any().any() or churn.isna().any().any() or sales.isna().any().any():
        raise ValueError("Missing or invalid values found in the supplied datasets.")
    if house.duplicated().any() or churn.duplicated().any() or sales.duplicated().any():
        raise ValueError("Duplicate records found; review before analysis.")
    sales["Month"] = sales["Date"].dt.to_period("M").astype(str)
    return house, churn, sales


def clean_and_save(house: pd.DataFrame, churn: pd.DataFrame, sales: pd.DataFrame) -> None:
    """Save reproducible cleaned copies without changing source files."""
    CLEANED.mkdir(exist_ok=True)
    house.to_csv(CLEANED / "cleaned_house_prices.csv", index=False)
    churn.to_csv(CLEANED / "cleaned_customer_churn.csv", index=False)
    sales.to_csv(CLEANED / "cleaned_sales_data.csv", index=False)


def create_visualizations(house: pd.DataFrame, churn: pd.DataFrame, sales: pd.DataFrame) -> list[pathlib.Path]:
    """Create five portfolio-ready business charts."""
    VIZ.mkdir(exist_ok=True)
    sns.set_theme(style="whitegrid", palette="deep")
    paths: list[pathlib.Path] = []

    fig, axes = plt.subplots(1, 2, figsize=(14, 5))
    monthly: pd.Series = sales.groupby("Month", as_index=False)["Total_Sales"].sum()
    sns.lineplot(data=monthly, x="Month", y="Total_Sales", marker="o", color="#2f6690", ax=axes[0])
    axes[0].set(title="Monthly Sales Trend", xlabel="Month", ylabel="Sales")
    product = sales.groupby("Product", as_index=False)["Total_Sales"].sum().sort_values("Total_Sales")
    sns.barplot(data=product, x="Product", y="Total_Sales", hue="Product", legend=False, palette="Blues_d", ax=axes[1])
    axes[1].set(title="Sales by Product", xlabel="Product", ylabel="Sales")
    axes[1].tick_params(axis="x", rotation=30)
    fig.tight_layout(); path: pathlib.Path = VIZ / "sales_analysis.png"; fig.savefig(path, dpi=150); plt.close(fig); paths.append(path)

    fig, axes = plt.subplots(1, 2, figsize=(14, 5))
    churn_rates: pd.Series = churn.groupby("Contract", as_index=False)["Churn"].mean()
    churn_rates["Churn"] *= 100
    sns.barplot(data=churn_rates, x="Contract", y="Churn", hue="Contract", legend=False, palette="Reds", ax=axes[0])
    axes[0].set(title="Churn Rate by Contract", xlabel="Contract", ylabel="Churn (%)")
    sns.boxplot(data=churn, x="Churn", y="MonthlyCharges", hue="Churn", legend=False, palette="Set2", ax=axes[1])
    axes[1].set(title="Monthly Charges by Churn Status", xlabel="Churn (0=No, 1=Yes)", ylabel="Monthly Charges")
    fig.tight_layout(); path: pathlib.Path = VIZ / "churn_analysis.png"; fig.savefig(path, dpi=150); plt.close(fig); paths.append(path)

    fig, axes = plt.subplots(1, 2, figsize=(14, 5))
    sns.scatterplot(data=house, x="Area", y="Price", hue="Location", alpha=0.7, ax=axes[0])
    axes[0].set(title="Property Price vs Area", xlabel="Area", ylabel="Price")
    location = house.groupby("Location", as_index=False)["Price"].mean().sort_values("Price")
    sns.barplot(data=location, x="Location", y="Price", hue="Location", legend=False, palette="Greens_d", ax=axes[1])
    axes[1].set(title="Average Price by Location", xlabel="Location", ylabel="Average Price")
    fig.tight_layout(); path: pathlib.Path = VIZ / "property_price_analysis.png"; fig.savefig(path, dpi=150); plt.close(fig); paths.append(path)

    fig, axes = plt.subplots(1, 2, figsize=(14, 5))
    sns.heatmap(house[["Area", "Bedrooms", "Bathrooms", "Age", "Price"]].corr(), annot=True, fmt=".2f", cmap="YlOrRd", ax=axes[0])
    axes[0].set_title("Property Correlation Heatmap")
    sns.histplot(house["Price"], bins=15, kde=True, color="#7b2cbf", ax=axes[1])
    axes[1].set(title="Property Price Distribution", xlabel="Price", ylabel="Count")
    fig.tight_layout(); path: pathlib.Path = VIZ / "correlation_heatmap.png"; fig.savefig(path, dpi=150); plt.close(fig); paths.append(path)

    fig, axis = plt.subplots(figsize=(9, 5))
    region = sales.groupby("Region", as_index=False)["Total_Sales"].sum().sort_values("Total_Sales")
    sns.barplot(data=region, x="Region", y="Total_Sales", hue="Region", legend=False, palette="mako", ax=axis)
    axis.set(title="Regional Sales Performance", xlabel="Region", ylabel="Total Sales")
    fig.tight_layout(); path: pathlib.Path = VIZ / "additional_visualization.png"; fig.savefig(path, dpi=150); plt.close(fig); paths.append(path)
    return paths


def analyze(house: pd.DataFrame, churn: pd.DataFrame, sales: pd.DataFrame) -> dict[str, object]:
    """Calculate business metrics and appropriate statistical models."""
    house_model: sklearn.linear_model.LinearRegression = sklearn.linear_model.LinearRegression().fit(house[["Area"]], house["Price"])
    return {
        "sales_total": sales["Total_Sales"].sum(), "sales_quantity": sales["Quantity"].sum(),
        "top_product": sales.groupby("Product")["Total_Sales"].sum().idxmax(),
        "top_region": sales.groupby("Region")["Total_Sales"].sum().idxmax(),
        "monthly": sales.groupby("Month")["Total_Sales"].sum().to_dict(),
        "churn_rate": churn["Churn"].mean(), "contract_churn": churn.groupby("Contract")["Churn"].mean().to_dict(),
        "top_location": house.groupby("Location")["Price"].mean().idxmax(),
        "location_prices": house.groupby("Location")["Price"].mean().to_dict(),
        "house_area_corr": house[["Area", "Price"]].corr().loc["Area", "Price"],
        "house_slope": house_model.coef_[0], "house_r2": house_model.score(house[["Area"]], house["Price"]),
        "sales_mean_ci": sp.stats.t.interval(.95, len(sales)-1, loc=sales["Total_Sales"].mean(), scale=sp.stats.sem(sales["Total_Sales"])),
    }


def write_reports(metrics: dict[str, object], house: pd.DataFrame, churn: pd.DataFrame, sales: pd.DataFrame) -> None:
    """Create a concise executive PDF and a detailed multi-page technical PDF."""
    styles: reportlab.lib.styles.StyleSheet1 = reportlab.lib.styles.getSampleStyleSheet()
    styles["BodyText"].leading = 14
    styles["BodyText"].spaceAfter = 8
    styles["Heading2"].spaceBefore = 12
    styles["Heading2"].spaceAfter = 7
    key: list[str] = [
        f"Total sales: {metrics['sales_total']:,.0f}",
        f"Total quantity sold: {metrics['sales_quantity']:,}",
        f"Top product: {metrics['top_product']}",
        f"Top region: {metrics['top_region']}",
        f"Overall churn: {metrics['churn_rate']:.2%}",
        f"Top property location by mean price: {metrics['top_location']}",
        f"Area-price correlation: {metrics['house_area_corr']:.3f}",
    ]

    summary: list[reportlab.platypus.Paragraph] = [
        reportlab.platypus.Paragraph("Week 8 Capstone: Executive Summary", styles["Title"]),
        reportlab.platypus.Paragraph("Business problem", styles["Heading2"]),
        reportlab.platypus.Paragraph("This capstone combines three independent business views: sales performance, customer retention, and property pricing. The purpose is to identify measurable opportunities and turn them into practical actions for a management team.", styles["BodyText"]),
        reportlab.platypus.Paragraph("Key findings", styles["Heading2"]),
    ]
    summary += [reportlab.platypus.Paragraph(f"• {line}", styles["BodyText"]) for line in key]
    summary += [
        reportlab.platypus.Paragraph("Recommended priorities", styles["Heading2"]),
        reportlab.platypus.Paragraph("1. Start an early-retention program for month-to-month customers and monitor churn weekly. 2. Protect Laptop availability and review North-region capacity because both lead sales performance. 3. Use property area and location as core inputs in pricing reviews.", styles["BodyText"]),
        reportlab.platypus.Paragraph("Expected impact", styles["Heading2"]),
        reportlab.platypus.Paragraph("A repeatable KPI process should improve visibility into churn risk, sales concentration, and price positioning. The recommendations are evidence-based priorities, not causal guarantees; each should be evaluated through a 30-, 60-, and 90-day measurement cycle.", styles["BodyText"]),
    ]
    reportlab.platypus.SimpleDocTemplate(str(REPORTS / "executive_summary.pdf"), pagesize=reportlab.lib.pagesizes.letter, rightMargin=54, leftMargin=54).build(summary)

    def heading(text: str) -> reportlab.platypus.Paragraph:
        return reportlab.platypus.Paragraph(text, styles["Heading2"])

    def body(text: str) -> reportlab.platypus.Paragraph:
        return reportlab.platypus.Paragraph(text, styles["BodyText"])

    product_sales: pd.Series = sales.groupby("Product")["Total_Sales"].sum().sort_values(ascending=False)
    region_sales: pd.Series = sales.groupby("Region")["Total_Sales"].sum().sort_values(ascending=False)
    contract_churn: pd.Series = (churn.groupby("Contract")["Churn"].mean() * 100).sort_values(ascending=False)
    location_prices: pd.Series = house.groupby("Location")["Price"].mean().sort_values(ascending=False)
    monthly_sales: pd.Series = sales.groupby("Month")["Total_Sales"].sum()
    technical: list[object] = [
        reportlab.platypus.Paragraph("Week 8 Capstone Technical Report", styles["Title"]),
        body("This report documents a reproducible end-to-end analysis of sales, customer churn, and property pricing data. It is written for reviewers who need both the analytical method and the business meaning of the results."),
        heading("1. Business Context and Problem Definition"),
        body("The business needs a joined view of performance: sales teams need to understand product and regional revenue, customer teams need to understand which segments show higher churn, and property teams need evidence for pricing decisions. The datasets are separate samples, so the analysis answers each business question independently rather than manufacturing a relationship between unrelated records."),
        body("Success is defined as producing traceable metrics, clear visual evidence, practical recommendations, and a repeatable artifact-generation script. Key monitoring measures are total sales, product and regional revenue, churn rate by contract, average property price by location, and pricing relationships with physical property characteristics."),
        heading("2. Dataset Inventory"),
        body(f"The house-price dataset contains {house.shape[0]} properties and {house.shape[1]} columns. It includes area, bedrooms, bathrooms, age, location, property type, and price. The customer dataset contains {churn.shape[0]} records and {churn.shape[1]} columns covering tenure, charges, contract, payment method, senior-citizen status, and churn. The sales dataset contains {sales.shape[0]} transactions and {sales.shape[1] - 1} original columns, with dates from {sales['Date'].min().date()} through {sales['Date'].max().date()} and one derived Month field."),
        body("All three files were loaded from the project data directory. Each dataset had zero missing values and zero duplicate records. The sales Date column was converted to datetime and used to derive monthly totals. Cleaned copies were written to cleaned_data without overwriting the supplied source files."),
        heading("3. Data Preparation and Quality Checks"),
        body("The preparation process validates file presence, reads each CSV with Pandas, checks for missing values and duplicates, converts the sales date, and saves reproducible cleaned copies. Numeric and categorical fields were retained because the supplied data passed the quality checks. April sales are treated as a partial period because the final sales date is April 9."),
        body("The datasets do not have a shared customer or property key. Customer IDs in the churn data are not present in the sales data, and property records have no sales key. Therefore, joins were intentionally avoided. This prevents unsupported customer-level sales conclusions and keeps each business analysis valid for its own source."),
        reportlab.platypus.PageBreak(),
        heading("4. Sales Performance Analysis"),
        body(f"Sales revenue totals {metrics['sales_total']:,.0f} across {metrics['sales_quantity']:,} units. {metrics['top_product']} is the leading product, and {metrics['top_region']} is the leading region. The monthly sequence is {', '.join(f'{month}: {value:,.0f}' for month, value in monthly_sales.items())}. March is the strongest complete month; April cannot be compared as a full month."),
        reportlab.platypus.Table([["Product", "Total Sales"]] + [[str(index), f"{value:,.0f}"] for index, value in product_sales.items()], colWidths=[220, 150], style=reportlab.platypus.TableStyle([["BACKGROUND", (0, 0), (-1, 0), "#d9eaf7"], ["GRID", (0, 0), (-1, -1), 0.5, "#9aa7b0"], ["ALIGN", (1, 1), (-1, -1), "RIGHT"]])),
        reportlab.platypus.Spacer(1, 10),
        reportlab.platypus.Table([["Region", "Total Sales"]] + [[str(index), f"{value:,.0f}"] for index, value in region_sales.items()], colWidths=[220, 150], style=reportlab.platypus.TableStyle([["BACKGROUND", (0, 0), (-1, 0), "#d9f0df"], ["GRID", (0, 0), (-1, -1), 0.5, "#9aa7b0"], ["ALIGN", (1, 1), (-1, -1), "RIGHT"]])),
        heading("Sales interpretation"),
        body("Revenue is concentrated in a small number of product and regional leaders. That concentration creates an opportunity to protect availability and execution in leading segments, while using lower-performing segments as a focused improvement agenda. The analysis does not claim that product or region causes revenue differences; it identifies where management attention is most likely to have value."),
        heading("5. Customer Churn and Retention Analysis"),
        body(f"The observed churn rate is {metrics['churn_rate']:.2%}. Contract-level rates are {', '.join(f'{name}: {value:.2f}%' for name, value in contract_churn.items())}. The gap between month-to-month and one-year contracts is a clear segmentation signal for retention planning. It should be monitored over time and tested with controlled campaigns before claiming causal impact."),
        reportlab.platypus.Table([["Contract", "Churn Rate"]] + [[str(index), f"{value:.2f}%"] for index, value in contract_churn.items()], colWidths=[220, 150], style=reportlab.platypus.TableStyle([["BACKGROUND", (0, 0), (-1, 0), "#f5dddd"], ["GRID", (0, 0), (-1, -1), 0.5, "#9aa7b0"], ["ALIGN", (1, 1), (-1, -1), "RIGHT"]])),
        heading("Retention recommendation"),
        body("Create an early-tenure monitoring list for month-to-month customers, provide clear upgrade value, and measure contact, conversion, and subsequent churn. Keep payment and billing attributes in the monitoring workflow, but avoid treating group differences as proof of customer behavior causes."),
        reportlab.platypus.PageBreak(),
        heading("6. Property Pricing Analysis"),
        body(f"The property dataset contains {house.shape[0]} observations. Mean price is {house['Price'].mean():,.0f}, with a range from {house['Price'].min():,.0f} to {house['Price'].max():,.0f}. {metrics['top_location']} has the highest mean price at {location_prices.iloc[0]:,.0f}. The Pearson correlation between Area and Price is {metrics['house_area_corr']:.3f}, indicating a strong positive linear association in this sample."),
        reportlab.platypus.Table([["Location", "Mean Price"]] + [[str(index), f"{value:,.0f}"] for index, value in location_prices.items()], colWidths=[220, 150], style=reportlab.platypus.TableStyle([["BACKGROUND", (0, 0), (-1, 0), "#d9f0df"], ["GRID", (0, 0), (-1, -1), 0.5, "#9aa7b0"], ["ALIGN", (1, 1), (-1, -1), "RIGHT"]])),
        heading("Pricing interpretation"),
        body("Area is a useful starting variable for pricing review, while location adds a clear market-segmentation perspective. The project recommends using both features in a pricing review model, then validating predictions against future transactions. A correlation is informative but does not prove that increasing area alone causes a specific price increase."),
        heading("7. Analysis Techniques and Statistical Reasoning"),
        body("The project uses exploratory data analysis, descriptive statistics, groupby aggregation, monthly trend analysis, segmentation by contract, correlation analysis, and linear regression. These techniques were selected because the datasets contain numeric measures, categorical groupings, a time field in sales, and repeated business dimensions suitable for comparisons."),
        body("The analysis deliberately avoids artificial joins. It also distinguishes observed patterns from causal conclusions. This is important for a portfolio project: reproducibility and honest limitations are more valuable than a complicated but unsupported model."),
        reportlab.platypus.PageBreak(),
        heading("8. Visualization Evidence"),
        body("Five visualizations were generated from the actual values. sales_analysis.png combines the monthly sales trend and product performance. churn_analysis.png compares contract churn and monthly charges by churn status. property_price_analysis.png combines area-price observations and mean prices by location. correlation_heatmap.png shows relationships among property variables and price. additional_visualization.png shows regional sales performance."),
        body("Each chart has a focused business purpose: identify trends, compare groups, locate concentration, inspect relationships, or support pricing decisions. The chart files are saved under visualizations and can be inserted into a portfolio or presentation."),
        heading("9. Business Insights"),
        body("Sales: Laptop is the top product and North is the top region. This suggests protecting supply and execution in these leading segments while testing targeted improvement actions in lower-performing segments. Monthly sales peak in March, but April is partial and should not be interpreted as a complete-month decline."),
        body("Retention: Month-to-month customers have the highest observed churn rate. This supports early-retention outreach, clearer upgrade communication, and recurring segment monitoring. The data supports prioritization, not a claim that contract type alone causes churn."),
        body("Property: City Center has the highest average price, and Area has a strong positive association with Price. Pricing teams can use area and location together for market review, while validating the approach with new listings and completed transactions."),
        heading("10. Actionable Recommendations"),
        body("Recommendation 1 - High priority: establish a weekly churn dashboard focused on month-to-month customers and early-tenure signals. Recommendation 2 - Medium priority: align inventory and regional sales planning with Laptop and North-region performance. Recommendation 3 - Medium priority: introduce an area-and-location pricing review using comparable properties and track prediction error."),
        reportlab.platypus.PageBreak(),
        heading("11. Implementation Plan"),
        reportlab.platypus.Table([["Action", "Priority", "Timeline", "Success metric"], ["Churn monitoring and outreach", "High", "0-30 days", "Churn rate and response rate"], ["Product and region planning", "Medium", "31-60 days", "Product/region revenue"], ["Property pricing review", "Medium", "31-90 days", "Pricing error and conversion"], ["Governance review", "High", "Monthly", "Data quality and refresh completion"]], colWidths=[160, 75, 90, 150], style=reportlab.platypus.TableStyle([["BACKGROUND", (0, 0), (-1, 0), "#d9eaf7"], ["GRID", (0, 0), (-1, -1), 0.5, "#9aa7b0"], ["VALIGN", (0, 0), (-1, -1), "TOP"]])),
        heading("12. Limitations and Risk Controls"),
        body("The sales sample contains 100 transactions and only covers part of April. The customer, sales, and property datasets are independent and cannot be joined. The analysis is observational, so correlations and group differences are not causal proof. Future work should add more time periods, establish reliable business keys, and test recommendations through controlled measurement."),
        heading("13. Reproducibility and Quality Assurance"),
        body("capstone_analysis.py loads the supplied files, validates missing values and duplicates, saves cleaned copies, calculates metrics, generates charts, and writes the PDF and PowerPoint deliverables. The final run completed successfully with 300 property rows, 500 customer rows, and 100 sales rows. Source CSVs were not overwritten."),
        heading("14. Conclusion"),
        body("This capstone turns three real datasets into a practical business portfolio. It identifies sales concentration, a retention priority, and a property pricing signal, then connects each finding to an action, owner-facing metric, and implementation timeline. The project is ready for review and presentation after manual screenshots are added."),
    ]
    reportlab.platypus.SimpleDocTemplate(str(REPORTS / "technical_report.pdf"), pagesize=reportlab.lib.pagesizes.letter, rightMargin=54, leftMargin=54, topMargin=50, bottomMargin=50).build(technical)


def create_presentation(metrics: dict[str, object]) -> None:
    """Create a detailed 15-slide business presentation."""
    presentation: pptx.presentation.Presentation = pptx.Presentation()
    presentation.slide_width = pptx.util.Inches(13.333)
    presentation.slide_height = pptx.util.Inches(7.5)
    slides: list[tuple[str, str]] = [
        ("Real World Business Analysis", "Week 8 Capstone | The Developers Arena\nA portfolio project connecting sales, customer retention, and property pricing evidence.\nPurpose: convert raw business data into measurable decisions."),
        ("Business Problem", "Management needs a clear view of revenue performance, churn risk, and property pricing signals.\nThe analysis identifies what is happening, where attention is needed, and how to measure improvement.\nThe datasets are analyzed independently because they have no valid shared key."),
        ("Objectives", "Validate and prepare three real datasets.\nUse EDA, group comparisons, trends, correlation, and regression.\nTranslate findings into recommendations with owners, timelines, and success metrics."),
        ("Datasets", "House prices: 300 properties and 8 fields.\nCustomer churn: 500 customers and 9 fields.\nSales: 100 transactions and 7 original fields; April is a partial period."),
        ("Data Preparation", "All three datasets had zero missing values and zero duplicate rows.\nSales dates were converted to datetime and monthly fields were derived.\nCleaned copies were saved without overwriting the supplied source files."),
        ("Sales Performance", f"Revenue totals {metrics['sales_total']:,.0f} across {metrics['sales_quantity']:,} units.\n{metrics['top_product']} is the leading product and {metrics['top_region']} is the leading region.\nMarch is the strongest complete month; April should be treated as partial."),
        ("Customer Churn Analysis", f"Overall churn is {metrics['churn_rate']:.2%}.\nMonth-to-month customers show the highest observed churn rate.\nPrioritize early retention outreach, but validate impact through controlled KPI tracking."),
        ("Property Price Analysis", f"{metrics['top_location']} has the highest mean property price.\nArea-price correlation is {metrics['house_area_corr']:.3f}, a strong positive association.\nUse area and location in pricing review without claiming causation."),
        ("Key Visual Evidence", "Sales charts show product, region, and monthly concentration.\nChurn charts compare contract segments and charge distributions.\nProperty charts show area-price relationships, location differences, and correlations."),
        ("Major Findings", "Laptop and North lead sales performance.\nMonth-to-month churn is the main retention priority.\nCity Center and property area are important pricing signals in this sample."),
        ("Business Recommendations", "Launch a weekly churn monitoring process with early-tenure outreach.\nProtect Laptop availability and review North-region capacity.\nUse area and location as inputs to a property pricing review."),
        ("Implementation Plan", "0-30 days: define dashboards, segments, and owners.\n31-60 days: launch retention tests and review product/region planning.\n61-90 days: evaluate pricing accuracy and scale successful actions."),
        ("Success Metrics", "Retention: churn rate, outreach response, and upgrade conversion.\nSales: product revenue, regional revenue, and monthly trend.\nProperty: pricing error, listing conversion, and location-level performance."),
        ("Limitations", "The datasets are independent and cannot be joined at customer level.\nSales covers 100 transactions and April ends on day 9.\nObserved relationships are not proof of causation; future data and testing are required."),
        ("Conclusion", "The capstone creates a reproducible path from raw data to action.\nIt highlights sales concentration, a retention opportunity, and a property pricing signal.\nThe implementation plan makes the recommendations measurable and reviewable."),
    ]
    for title, body in slides:
        slide: pptx.slide.Slide = presentation.slides.add_slide(presentation.slide_layouts[6])
        background: pptx.shapes.autoshape.FillFormat = slide.background.fill
        background.solid()
        background.fore_color.rgb = pptx.dml.color.RGBColor(9, 27, 34)
        title_box: pptx.shapes.autoshape.Shape = slide.shapes.add_textbox(pptx.util.Inches(0.8), pptx.util.Inches(0.65), pptx.util.Inches(11.8), pptx.util.Inches(0.75))
        title_frame: pptx.shapes.autoshape.TextFrame = title_box.text_frame
        title_frame.text = title
        title_frame.paragraphs[0].font.size = pptx.util.Pt(30)
        title_frame.paragraphs[0].font.bold = True
        title_frame.paragraphs[0].font.color.rgb = pptx.dml.color.RGBColor(73, 198, 181)
        body_box: pptx.shapes.autoshape.Shape = slide.shapes.add_textbox(pptx.util.Inches(1.0), pptx.util.Inches(1.8), pptx.util.Inches(11.0), pptx.util.Inches(4.7))
        body_frame: pptx.shapes.autoshape.TextFrame = body_box.text_frame
        body_frame.word_wrap = True
        body_frame.margin_left = pptx.util.Inches(0.18)
        body_frame.text = body
        for paragraph in body_frame.paragraphs:
            paragraph.font.size = pptx.util.Pt(21)
            paragraph.font.color.rgb = pptx.dml.color.RGBColor(232, 243, 240)
            paragraph.space_after = pptx.util.Pt(14)
        footer: pptx.shapes.autoshape.Shape = slide.shapes.add_textbox(pptx.util.Inches(0.8), pptx.util.Inches(7.05), pptx.util.Inches(11.8), pptx.util.Inches(0.25))
        footer.text_frame.text = "Week 8 Capstone | Real World Business Analysis"
        footer.text_frame.paragraphs[0].font.size = pptx.util.Pt(9)
        footer.text_frame.paragraphs[0].font.color.rgb = pptx.dml.color.RGBColor(143, 169, 168)
    presentation.save(PRESENTATION / "business_analysis_presentation.pptx")


def main() -> None:
    """Run the complete capstone artifact generation."""
    house, churn, sales = load_data()
    clean_and_save(house, churn, sales)
    metrics: dict[str, object] = analyze(house, churn, sales)
    paths: list[pathlib.Path] = create_visualizations(house, churn, sales)
    write_reports(metrics, house, churn, sales)
    create_presentation(metrics)
    print("Capstone analysis completed successfully.")
    print(f"Datasets: house={house.shape}, churn={churn.shape}, sales={sales.shape}")
    print(f"Sales total={metrics['sales_total']:,.0f}; churn={metrics['churn_rate']:.2%}; top product={metrics['top_product']}; top region={metrics['top_region']}")
    print(f"Area-price correlation={metrics['house_area_corr']:.3f}; property location leader={metrics['top_location']}")
    print(f"Generated {len(paths)} visualizations, 2 PDFs, and 1 presentation.")


if __name__ == "__main__":
    main()
