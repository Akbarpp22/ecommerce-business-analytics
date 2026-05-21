# Executive Summary - E-commerce Business Analytics

## Business Problem

Marketplace/e-commerce companies need to monitor revenue growth, customer demand, product performance, delivery quality, and customer satisfaction in one integrated view. This project builds an end-to-end analytics workflow to identify revenue drivers, operational bottlenecks, and practical actions to improve customer experience.

## Dataset

This package uses synthetic Olist-style marketplace data with the same structure as the public Olist Brazilian E-commerce dataset so the project can be run immediately. The recommended real dataset source is the Olist Brazilian E-commerce public dataset from Kaggle.

## Method

1. Load raw relational CSV files.
2. Clean datetime fields and create delivery performance features.
3. Join order, item, payment, product, seller, customer, and review tables.
4. Calculate business KPIs using Python and SQL.
5. Create dashboard-ready summary tables and charts.
6. Translate findings into business recommendations.

## Key Metrics

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

1. The highest-revenue category is **computers_accessories**, generating **1,685,925.43** in revenue.
2. The top customer state is **SP**, generating **7,350,781.42** in revenue.
3. Late delivery is associated with lower review scores, meaning logistics quality directly affects customer satisfaction.
4. Product category, seller performance, and region should be monitored together, not separately.

## Business Recommendations

1. Prioritize high-revenue categories for campaign planning, inventory planning, and seller quality monitoring.
2. Monitor late delivery rate weekly, especially for categories and regions with high revenue.
3. Build seller performance tiers based on revenue, review score, late delivery rate, and total orders.
4. Focus marketing and logistics investment on top revenue states while testing lower-penetration states.
5. Use the dashboard as a weekly business review tool for executives and operations teams.

## Portfolio Positioning

This project demonstrates skills in SQL, Python, data cleaning, business KPI analysis, dashboarding, and insight communication. It is suitable for Data Analyst, Business Intelligence Analyst, Junior Data Analyst, and Business Analyst applications.
