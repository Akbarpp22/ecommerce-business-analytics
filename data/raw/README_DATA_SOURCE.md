# Data Source Notes

This project package includes synthetic Olist-style CSV files so the full portfolio project can be opened and studied immediately.

Why synthetic data is included:
- The execution environment could not directly download the large public CSV files from Kaggle/GitHub.
- The synthetic files follow the same relational structure and filenames as the public Olist Brazilian E-commerce dataset.
- This lets the notebook, SQL queries, dashboard, and report run immediately.

Recommended real dataset:
- Brazilian E-Commerce Public Dataset by Olist
- Kaggle: https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce
- GitHub mirror inspected: https://github.com/spdrio/Brazilian-E-Commerce-Public-Dataset-by-Olist

To use real data:
1. Download the original Olist dataset from Kaggle.
2. Replace every CSV in this folder with the original CSV files.
3. Rerun `notebooks/01_ecommerce_data_cleaning_eda.ipynb` or `scripts/run_analysis.py`.
4. Refresh or rebuild the dashboard.
