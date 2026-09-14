# Interactive Sales Dashboard

Week 6 of The Developers Arena internship demonstrates sales analysis with Pandas, five Seaborn visualizations, and an interactive Plotly HTML dashboard.

## Features

- Loads and validates the provided `sales_data.csv`.
- Converts dates and calculates monthly sales.
- Reports sales, quantity, product, region, and correlation metrics.
- Creates five distinct Seaborn charts.
- Creates an interactive Plotly dashboard with KPI cards, hover details, zoom/pan, and a product dropdown.

## Technologies

- Python 3.x
- Pandas
- Seaborn
- Matplotlib
- Plotly

## Setup

```text
cd /d D:\Developer_Arena\Week1_Task\Task_6_Data_Visualization_Mastery_with_Seaborn
python -m pip install -r requirements.txt
```

## Run

```text
python dashboard.py
```

Open `dashboard.html` in a browser after the script completes.

## Visualizations

- `visualizations/sales_by_product.png` - Seaborn bar chart.
- `visualizations/sales_trend.png` - Seaborn line chart.
- `visualizations/sales_by_region.png` - Seaborn regional bar chart.
- `visualizations/sales_distribution.png` - Seaborn histogram with KDE.
- `visualizations/correlation_heatmap.png` - Seaborn correlation heatmap.

## Structure

```text
Task_6_Data_Visualization_Mastery_with_Seaborn/
├── dashboard.py
├── dashboard.html
├── dashboard.ipynb
├── sales_data.csv
├── requirements.txt
├── visualizations/
├── screenshots/
└── report/
```

Screenshots and GIFs are not fabricated; capture them manually after opening the dashboard.
