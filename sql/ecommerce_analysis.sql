
-- E-commerce Business Analytics SQL Analysis
-- Database dialect: SQLite
-- Tables expected:
--   olist_orders_dataset
--   olist_order_items_dataset
--   olist_order_payments_dataset
--   olist_order_reviews_dataset
--   olist_customers_dataset
--   olist_products_dataset
--   olist_sellers_dataset
--   product_category_name_translation

-- 1) Total revenue and delivered orders
SELECT
    ROUND(SUM(oi.price + oi.freight_value), 2) AS total_revenue,
    COUNT(DISTINCT o.order_id) AS delivered_orders,
    COUNT(DISTINCT o.customer_id) AS unique_customers,
    ROUND(SUM(oi.price + oi.freight_value) / COUNT(DISTINCT o.order_id), 2) AS average_order_value
FROM olist_orders_dataset o
JOIN olist_order_items_dataset oi
    ON o.order_id = oi.order_id
WHERE o.order_status = 'delivered';

-- 2) Monthly revenue trend
SELECT
    strftime('%Y-%m', o.order_purchase_timestamp) AS order_month,
    ROUND(SUM(oi.price + oi.freight_value), 2) AS revenue,
    COUNT(DISTINCT o.order_id) AS total_orders,
    COUNT(DISTINCT o.customer_id) AS unique_customers,
    ROUND(SUM(oi.price + oi.freight_value) / COUNT(DISTINCT o.order_id), 2) AS average_order_value
FROM olist_orders_dataset o
JOIN olist_order_items_dataset oi
    ON o.order_id = oi.order_id
WHERE o.order_status = 'delivered'
GROUP BY order_month
ORDER BY order_month;

-- 3) Top product categories by revenue
SELECT
    COALESCE(t.product_category_name_english, p.product_category_name) AS category,
    ROUND(SUM(oi.price + oi.freight_value), 2) AS revenue,
    COUNT(DISTINCT oi.order_id) AS total_orders,
    COUNT(*) AS total_items,
    ROUND(AVG(oi.price), 2) AS avg_price,
    ROUND(AVG(oi.freight_value), 2) AS avg_freight
FROM olist_order_items_dataset oi
JOIN olist_orders_dataset o
    ON oi.order_id = o.order_id
LEFT JOIN olist_products_dataset p
    ON oi.product_id = p.product_id
LEFT JOIN product_category_name_translation t
    ON p.product_category_name = t.product_category_name
WHERE o.order_status = 'delivered'
GROUP BY category
ORDER BY revenue DESC
LIMIT 10;

-- 4) Revenue by customer state
SELECT
    c.customer_state,
    ROUND(SUM(oi.price + oi.freight_value), 2) AS revenue,
    COUNT(DISTINCT o.order_id) AS total_orders,
    COUNT(DISTINCT o.customer_id) AS unique_customers,
    ROUND(SUM(oi.price + oi.freight_value) / COUNT(DISTINCT o.order_id), 2) AS average_order_value
FROM olist_orders_dataset o
JOIN olist_order_items_dataset oi
    ON o.order_id = oi.order_id
JOIN olist_customers_dataset c
    ON o.customer_id = c.customer_id
WHERE o.order_status = 'delivered'
GROUP BY c.customer_state
ORDER BY revenue DESC;

-- 5) Late delivery rate
SELECT
    COUNT(*) AS delivered_orders,
    SUM(CASE
        WHEN date(order_delivered_customer_date) > date(order_estimated_delivery_date)
        THEN 1 ELSE 0
    END) AS late_orders,
    ROUND(
        100.0 * SUM(CASE
            WHEN date(order_delivered_customer_date) > date(order_estimated_delivery_date)
            THEN 1 ELSE 0
        END) / COUNT(*),
        2
    ) AS late_delivery_rate_pct
FROM olist_orders_dataset
WHERE order_status = 'delivered';

-- 6) Review score vs delivery performance
SELECT
    r.review_score,
    COUNT(DISTINCT o.order_id) AS total_orders,
    ROUND(AVG(julianday(o.order_delivered_customer_date) - julianday(o.order_purchase_timestamp)), 2) AS avg_delivery_days,
    ROUND(AVG(julianday(o.order_delivered_customer_date) - julianday(o.order_estimated_delivery_date)), 2) AS avg_delay_days,
    ROUND(
        100.0 * SUM(CASE
            WHEN date(o.order_delivered_customer_date) > date(o.order_estimated_delivery_date)
            THEN 1 ELSE 0
        END) / COUNT(DISTINCT o.order_id),
        2
    ) AS late_delivery_rate_pct
FROM olist_orders_dataset o
JOIN olist_order_reviews_dataset r
    ON o.order_id = r.order_id
WHERE o.order_status = 'delivered'
GROUP BY r.review_score
ORDER BY r.review_score;

-- 7) Payment method mix
SELECT
    p.payment_type,
    COUNT(DISTINCT p.order_id) AS total_orders,
    ROUND(SUM(p.payment_value), 2) AS payment_value,
    ROUND(AVG(p.payment_value), 2) AS avg_payment_value
FROM olist_order_payments_dataset p
JOIN olist_orders_dataset o
    ON p.order_id = o.order_id
WHERE o.order_status = 'delivered'
GROUP BY p.payment_type
ORDER BY payment_value DESC;

-- 8) Seller performance: revenue, review, and late delivery
SELECT
    oi.seller_id,
    ROUND(SUM(oi.price + oi.freight_value), 2) AS revenue,
    COUNT(DISTINCT oi.order_id) AS total_orders,
    ROUND(AVG(r.review_score), 2) AS avg_review_score,
    ROUND(
        100.0 * SUM(CASE
            WHEN date(o.order_delivered_customer_date) > date(o.order_estimated_delivery_date)
            THEN 1 ELSE 0
        END) / COUNT(DISTINCT o.order_id),
        2
    ) AS late_delivery_rate_pct
FROM olist_order_items_dataset oi
JOIN olist_orders_dataset o
    ON oi.order_id = o.order_id
LEFT JOIN olist_order_reviews_dataset r
    ON oi.order_id = r.order_id
WHERE o.order_status = 'delivered'
GROUP BY oi.seller_id
HAVING total_orders >= 20
ORDER BY revenue DESC
LIMIT 20;

-- 9) Underperforming high-revenue categories
WITH category_metrics AS (
    SELECT
        COALESCE(t.product_category_name_english, p.product_category_name) AS category,
        ROUND(SUM(oi.price + oi.freight_value), 2) AS revenue,
        COUNT(DISTINCT oi.order_id) AS total_orders,
        ROUND(AVG(r.review_score), 2) AS avg_review_score,
        ROUND(
            100.0 * SUM(CASE
                WHEN date(o.order_delivered_customer_date) > date(o.order_estimated_delivery_date)
                THEN 1 ELSE 0
            END) / COUNT(DISTINCT o.order_id),
            2
        ) AS late_delivery_rate_pct
    FROM olist_order_items_dataset oi
    JOIN olist_orders_dataset o
        ON oi.order_id = o.order_id
    LEFT JOIN olist_order_reviews_dataset r
        ON oi.order_id = r.order_id
    LEFT JOIN olist_products_dataset p
        ON oi.product_id = p.product_id
    LEFT JOIN product_category_name_translation t
        ON p.product_category_name = t.product_category_name
    WHERE o.order_status = 'delivered'
    GROUP BY category
)
SELECT *
FROM category_metrics
WHERE revenue >= (SELECT AVG(revenue) FROM category_metrics)
ORDER BY avg_review_score ASC, late_delivery_rate_pct DESC;
