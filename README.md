# E-commerce Business Analytics Portfolio Project

## Project Overview

This project analyzes end-to-end marketplace performance across sales, customer location, product categories, payment methods, delivery performance, seller performance, and customer review scores.

The project is designed to look like a real Data Analyst workflow:
- define business questions,
- clean and join relational data,
- calculate KPIs with SQL/Python,
- build a dashboard,
- generate insights,
- translate findings into business recommendations.

> **Important transparency note**  
> The raw files included in this package are **synthetic Olist-style data** generated with the same table structure as the public Olist e-commerce dataset. I used synthetic data because the execution environment could not directly download the large Kaggle/GitHub CSV files.  
> To make this a real-data portfolio project, replace the CSV files in `data/raw/` with the original Olist dataset files from Kaggle, then rerun the notebook/script. The pipeline, SQL, dashboard structure, and portfolio story are already prepared.

Recommended real dataset:
- Kaggle: https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce
- GitHub mirror inspected: https://github.com/spdrio/Brazilian-E-Commerce-Public-Dataset-by-Olist

## Business Questions

1. What is the monthly revenue trend?
2. Which product categories contribute the most revenue?
3. Which customer states generate the highest revenue?
4. How does late delivery relate to review score?
5. Which payment methods are most used?
6. Which sellers should be monitored based on revenue, review score, and delivery performance?
7. What business actions can improve revenue and customer satisfaction?

## Tools Used

- **Python**: data cleaning, feature engineering, EDA, visualization
- **Pandas / NumPy**: data transformation
- **Matplotlib**: charts
- **SQL**: business KPI queries
- **Excel Dashboard**: interactive-style dashboard and summary tables
- **GitHub-ready README**: documentation for portfolio

## Repository Structure

```text
ecommerce_business_analytics_portfolio/
│
├── data/
│   ├── raw/                         # Olist-style raw CSV files
│   └── cleaned/                     # Cleaned analytical datasets and summary tables
│
├── notebooks/
│   └── 01_ecommerce_data_cleaning_eda.ipynb
│
├── sql/
│   └── ecommerce_analysis.sql
│
├── dashboard/
│   └── ecommerce_dashboard.xlsx
│
├── images/
│   ├── dashboard_screenshot.png
│   ├── monthly_revenue_trend.png
│   ├── top_categories_by_revenue.png
│   ├── late_delivery_by_review_score.png
│   ├── top_states_by_revenue.png
│   └── orders_by_payment_type.png
│
├── reports/
│   ├── executive_summary.md
│   └── executive_summary.pdf
│
├── cv/
│   └── cv_project_bullets_id_en.md
│
├── scripts/
│   └── run_analysis.py
│
└── README.md
```

## Key Metrics from Current Portfolio Dataset

| Metric | Value |
|---|---:|
| Total Revenue | 17,900,525.67 |
| Delivered Orders | 96,551 |
| Unique Customers | 96,551 |
| Average Order Value | 185.40 |
| Average Review Score | 3.83 |
| Late Delivery Rate | 24.18% |
| Average Delivery Days | 9.15 |

## Key Findings

### 1. Revenue is concentrated in a few categories

The highest-revenue category is **computers_accessories**, generating **1,685,925.43** in revenue. This means category-level monitoring is important for campaign planning, stock prioritization, and seller performance control.

### 2. Late delivery is linked to lower customer satisfaction

Orders with lower review scores show higher late delivery rates. This suggests that logistics performance is one of the strongest operational drivers of customer satisfaction.

### 3. Revenue is concentrated in major customer states

The highest-revenue customer state is **SP**, generating **7,350,781.42** in revenue. This indicates that regional marketing and logistics optimization should prioritize high-demand states first.

### 4. Seller monitoring can protect customer experience

Some sellers can generate high revenue while still having delivery or review issues. A seller scorecard can help identify which sellers need operational improvement.

## Business Recommendations

1. **Prioritize high-revenue product categories** for campaigns, stock planning, and seller quality monitoring.
2. **Reduce late delivery** by monitoring seller SLA and high-delay routes weekly.
3. **Focus marketing investment** on top revenue states while testing growth opportunities in lower-penetration states.
4. **Create seller performance tiers** using revenue, late delivery rate, average review score, and order volume.
5. **Use the dashboard as a weekly business review tool** for revenue, orders, review score, and delivery KPIs.

## Dashboard Preview

![Dashboard Preview](images/dashboard_screenshot.png)

## Main Charts

### Monthly Revenue Trend
![Monthly Revenue Trend](images/monthly_revenue_trend.png)

### Top Categories by Revenue
![Top Categories by Revenue](images/top_categories_by_revenue.png)

### Late Delivery by Review Score
![Late Delivery by Review Score](images/late_delivery_by_review_score.png)

## How to Reproduce

1. Clone or download this project.
2. Install dependencies:

```bash
pip install pandas numpy matplotlib
```

3. Run the notebook:

```bash
jupyter notebook notebooks/01_ecommerce_data_cleaning_eda.ipynb
```

Or run the script:

```bash
python scripts/run_analysis.py
```

4. Open the dashboard:

```text
dashboard/ecommerce_dashboard.xlsx
```

## How to Use Real Olist Data

1. Download the original Olist dataset from Kaggle.
2. Replace the CSV files inside `data/raw/` with the original files:
   - `olist_customers_dataset.csv`
   - `olist_order_items_dataset.csv`
   - `olist_order_payments_dataset.csv`
   - `olist_order_reviews_dataset.csv`
   - `olist_orders_dataset.csv`
   - `olist_products_dataset.csv`
   - `olist_sellers_dataset.csv`
   - `product_category_name_translation.csv`
3. Rerun the notebook or `scripts/run_analysis.py`.
4. Refresh the dashboard tables/charts or rebuild the Excel dashboard.

## Suggested Portfolio Title

**E-commerce Business Analytics: Sales, Delivery, Review & Customer Insights**

## Suggested CV Summary

Built an end-to-end e-commerce analytics project using SQL, Python, and Excel Dashboard to analyze 100K+ marketplace orders, identify revenue drivers, evaluate delivery performance, and develop business recommendations to improve customer satisfaction.
