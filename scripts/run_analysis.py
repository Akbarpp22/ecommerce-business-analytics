"""
Run E-commerce Business Analytics pipeline.

Usage:
    python scripts/run_analysis.py

Expected raw CSV files in data/raw:
    olist_customers_dataset.csv
    olist_order_items_dataset.csv
    olist_order_payments_dataset.csv
    olist_order_reviews_dataset.csv
    olist_orders_dataset.csv
    olist_products_dataset.csv
    olist_sellers_dataset.csv
    product_category_name_translation.csv
"""

from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

BASE_DIR = Path(__file__).resolve().parents[1]
RAW_DIR = BASE_DIR / "data" / "raw"
CLEAN_DIR = BASE_DIR / "data" / "cleaned"
IMG_DIR = BASE_DIR / "images"

CLEAN_DIR.mkdir(parents=True, exist_ok=True)
IMG_DIR.mkdir(parents=True, exist_ok=True)

def load_csv(name):
    return pd.read_csv(RAW_DIR / name)

def save_fig(path):
    plt.tight_layout()
    plt.savefig(path, bbox_inches="tight")
    plt.close()

def main():
    orders = load_csv("olist_orders_dataset.csv")
    items = load_csv("olist_order_items_dataset.csv")
    customers = load_csv("olist_customers_dataset.csv")
    payments = load_csv("olist_order_payments_dataset.csv")
    reviews = load_csv("olist_order_reviews_dataset.csv")
    products = load_csv("olist_products_dataset.csv")
    sellers = load_csv("olist_sellers_dataset.csv")
    translation = load_csv("product_category_name_translation.csv")

    date_cols = [
        "order_purchase_timestamp",
        "order_approved_at",
        "order_delivered_carrier_date",
        "order_delivered_customer_date",
        "order_estimated_delivery_date",
    ]
    for col in date_cols:
        orders[col] = pd.to_datetime(orders[col], errors="coerce")

    orders["delivery_days"] = (
        orders["order_delivered_customer_date"] - orders["order_purchase_timestamp"]
    ).dt.days
    orders["estimated_delivery_days"] = (
        orders["order_estimated_delivery_date"] - orders["order_purchase_timestamp"]
    ).dt.days
    orders["delivery_delay_days"] = (
        orders["order_delivered_customer_date"] - orders["order_estimated_delivery_date"]
    ).dt.days
    orders["is_late"] = orders["delivery_delay_days"] > 0
    orders["order_month"] = orders["order_purchase_timestamp"].dt.to_period("M").astype(str)

    df = orders.merge(customers, on="customer_id", how="left")
    df = df.merge(items, on="order_id", how="left")
    df = df.merge(payments, on="order_id", how="left")
    df = df.merge(reviews[["order_id", "review_score", "review_comment_title", "review_comment_message"]], on="order_id", how="left")
    df = df.merge(products, on="product_id", how="left")
    df = df.merge(sellers, on="seller_id", how="left")
    df = df.merge(translation, on="product_category_name", how="left")

    df["revenue"] = df["price"].fillna(0) + df["freight_value"].fillna(0)

    delivered_items = df[df["order_status"] == "delivered"].copy()
    delivered_orders = orders[orders["order_status"] == "delivered"].copy()

    kpi = pd.DataFrame({
        "metric": [
            "Total Revenue",
            "Delivered Orders",
            "Unique Customers",
            "Average Order Value",
            "Average Review Score",
            "Late Delivery Rate",
            "Average Delivery Days",
        ],
        "value": [
            delivered_items["revenue"].sum(),
            delivered_orders["order_id"].nunique(),
            delivered_orders["customer_id"].nunique(),
            delivered_items["revenue"].sum() / delivered_orders["order_id"].nunique(),
            delivered_items.drop_duplicates("order_id")["review_score"].mean(),
            delivered_orders["is_late"].mean(),
            delivered_orders["delivery_days"].mean(),
        ],
    })

    monthly = delivered_items.groupby("order_month", as_index=False).agg(
        revenue=("revenue", "sum"),
        total_orders=("order_id", "nunique"),
        total_customers=("customer_id", "nunique"),
        avg_review_score=("review_score", "mean"),
        late_delivery_rate=("is_late", "mean"),
    )
    monthly["aov"] = monthly["revenue"] / monthly["total_orders"]

    category = delivered_items.groupby("product_category_name_english", as_index=False).agg(
        revenue=("revenue", "sum"),
        total_orders=("order_id", "nunique"),
        total_items=("order_item_id", "count"),
        avg_price=("price", "mean"),
        avg_freight=("freight_value", "mean"),
        avg_review_score=("review_score", "mean"),
        late_delivery_rate=("is_late", "mean"),
    ).sort_values("revenue", ascending=False)

    state = delivered_items.groupby("customer_state", as_index=False).agg(
        revenue=("revenue", "sum"),
        total_orders=("order_id", "nunique"),
        total_customers=("customer_id", "nunique"),
        avg_delivery_days=("delivery_days", "mean"),
        late_delivery_rate=("is_late", "mean"),
        avg_review_score=("review_score", "mean"),
    ).sort_values("revenue", ascending=False)
    state["aov"] = state["revenue"] / state["total_orders"]

    review_delivery = delivered_items.drop_duplicates("order_id").groupby("review_score", as_index=False).agg(
        total_orders=("order_id", "nunique"),
        avg_delivery_days=("delivery_days", "mean"),
        avg_delay_days=("delivery_delay_days", "mean"),
        late_delivery_rate=("is_late", "mean"),
    )

    payment = delivered_items.drop_duplicates("order_id").groupby("payment_type", as_index=False).agg(
        total_orders=("order_id", "nunique"),
        payment_value=("payment_value", "sum"),
        avg_payment=("payment_value", "mean"),
    ).sort_values("payment_value", ascending=False)

    orders.to_csv(CLEAN_DIR / "orders_cleaned.csv", index=False)
    df.to_csv(CLEAN_DIR / "ecommerce_final_dataset.csv", index=False)
    kpi.to_csv(CLEAN_DIR / "kpi_summary.csv", index=False)
    monthly.to_csv(CLEAN_DIR / "monthly_revenue.csv", index=False)
    category.to_csv(CLEAN_DIR / "category_analysis.csv", index=False)
    state.to_csv(CLEAN_DIR / "state_analysis.csv", index=False)
    review_delivery.to_csv(CLEAN_DIR / "review_delivery_analysis.csv", index=False)
    payment.to_csv(CLEAN_DIR / "payment_summary.csv", index=False)

    plt.figure(figsize=(11, 5))
    plt.plot(monthly["order_month"], monthly["revenue"] / 1_000_000, marker="o")
    plt.title("Monthly Revenue Trend")
    plt.xlabel("Order Month")
    plt.ylabel("Revenue (Millions)")
    plt.xticks(rotation=45, ha="right")
    plt.grid(True, alpha=0.3)
    save_fig(IMG_DIR / "monthly_revenue_trend.png")

    top_categories = category.head(10).sort_values("revenue")
    plt.figure(figsize=(10, 6))
    plt.barh(top_categories["product_category_name_english"], top_categories["revenue"] / 1_000_000)
    plt.title("Top 10 Categories by Revenue")
    plt.xlabel("Revenue (Millions)")
    plt.ylabel("Product Category")
    plt.grid(True, axis="x", alpha=0.3)
    save_fig(IMG_DIR / "top_categories_by_revenue.png")

    plt.figure(figsize=(8, 5))
    plt.bar(review_delivery["review_score"].astype(str), review_delivery["late_delivery_rate"] * 100)
    plt.title("Late Delivery Rate by Review Score")
    plt.xlabel("Review Score")
    plt.ylabel("Late Delivery Rate (%)")
    plt.grid(True, axis="y", alpha=0.3)
    save_fig(IMG_DIR / "late_delivery_by_review_score.png")

    top_states = state.head(10).sort_values("revenue")
    plt.figure(figsize=(9, 5))
    plt.barh(top_states["customer_state"], top_states["revenue"] / 1_000_000)
    plt.title("Top 10 Customer States by Revenue")
    plt.xlabel("Revenue (Millions)")
    plt.ylabel("Customer State")
    plt.grid(True, axis="x", alpha=0.3)
    save_fig(IMG_DIR / "top_states_by_revenue.png")

    print("Analysis completed. Outputs saved to data/cleaned and images/.")

if __name__ == "__main__":
    main()
