-- ============================================================
-- India E-Commerce Pulse — SQL Business Analysis
-- Author: Juvana Dsouza
-- Dataset: Amazon Sale Report (128,975 rows)
-- Tool: SQLite (via Python)
-- ============================================================


-- ============================================================
-- Q1. What is the overall revenue and order breakdown by Status?
--     (Understanding how much revenue is lost to cancellations)
-- ============================================================
SELECT 
    Status,
    COUNT(*) AS total_orders,
    ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM amazon_sales), 2) AS pct_of_orders,
    ROUND(SUM(Amount), 2) AS total_revenue
FROM amazon_sales
WHERE Amount IS NOT NULL
GROUP BY Status
ORDER BY total_orders DESC;


-- ============================================================
-- Q2. Which product Category drives the most revenue vs volume?
--     (High revenue categories may not be high margin — spot the gap)
-- ============================================================
SELECT
    Category,
    COUNT(*) AS total_orders,
    ROUND(SUM(Amount), 2) AS total_revenue,
    ROUND(AVG(Amount), 2) AS avg_order_value,
    ROUND(SUM(Qty), 0) AS total_units_sold
FROM amazon_sales
WHERE Status NOT LIKE '%Cancelled%'
  AND Amount IS NOT NULL
GROUP BY Category
ORDER BY total_revenue DESC;


-- ============================================================
-- Q3. Which States generate the highest revenue?
--     (Top 10 performing states — where to focus operations)
-- ============================================================
SELECT
    "ship-state" AS state,
    COUNT(*) AS total_orders,
    ROUND(SUM(Amount), 2) AS total_revenue,
    ROUND(AVG(Amount), 2) AS avg_order_value
FROM amazon_sales
WHERE Status NOT LIKE '%Cancelled%'
  AND Amount IS NOT NULL
  AND "ship-state" IS NOT NULL
GROUP BY "ship-state"
ORDER BY total_revenue DESC
LIMIT 10;


-- ============================================================
-- Q4. Which States have HIGH average order value but LOW volume?
--     (Opportunity markets — high potential, underserved)
-- ============================================================
SELECT
    "ship-state" AS state,
    COUNT(*) AS total_orders,
    ROUND(AVG(Amount), 2) AS avg_order_value
FROM amazon_sales
WHERE Status NOT LIKE '%Cancelled%'
  AND Amount IS NOT NULL
  AND "ship-state" IS NOT NULL
GROUP BY "ship-state"
HAVING avg_order_value > (
    SELECT AVG(Amount) FROM amazon_sales WHERE Amount IS NOT NULL
)
AND total_orders < (
    SELECT AVG(order_count) FROM (
        SELECT COUNT(*) AS order_count 
        FROM amazon_sales 
        GROUP BY "ship-state"
    )
)
ORDER BY avg_order_value DESC
LIMIT 10;


-- ============================================================
-- Q5. What is the cancellation rate by Category?
--     (Which categories are customers most likely to cancel — why?)
-- ============================================================
SELECT
    Category,
    COUNT(*) AS total_orders,
    SUM(CASE WHEN Status LIKE '%Cancelled%' THEN 1 ELSE 0 END) AS cancelled_orders,
    ROUND(SUM(CASE WHEN Status LIKE '%Cancelled%' THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) AS cancellation_rate_pct
FROM amazon_sales
WHERE Category IS NOT NULL
GROUP BY Category
ORDER BY cancellation_rate_pct DESC;


-- ============================================================
-- Q6. B2B vs B2C — which segment is more valuable?
--     (Average order value, volume, and revenue comparison)
-- ============================================================
SELECT
    CASE WHEN B2B = 'True' THEN 'B2B' ELSE 'B2C' END AS customer_segment,
    COUNT(*) AS total_orders,
    ROUND(SUM(Amount), 2) AS total_revenue,
    ROUND(AVG(Amount), 2) AS avg_order_value,
    ROUND(AVG(Qty), 2) AS avg_units_per_order
FROM amazon_sales
WHERE Status NOT LIKE '%Cancelled%'
  AND Amount IS NOT NULL
GROUP BY B2B;


-- ============================================================
-- Q7. Which fulfilment method (Easy Ship vs Amazon) performs better?
--     (Delivery reliability and revenue by fulfilment type)
-- ============================================================
SELECT
    "fulfilled-by" AS fulfilment_method,
    COUNT(*) AS total_orders,
    ROUND(SUM(Amount), 2) AS total_revenue,
    ROUND(AVG(Amount), 2) AS avg_order_value,
    SUM(CASE WHEN Status LIKE '%Delivered%' THEN 1 ELSE 0 END) AS delivered,
    SUM(CASE WHEN Status LIKE '%Cancelled%' THEN 1 ELSE 0 END) AS cancelled,
    ROUND(SUM(CASE WHEN Status LIKE '%Delivered%' THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) AS delivery_rate_pct
FROM amazon_sales
WHERE "fulfilled-by" IS NOT NULL
GROUP BY "fulfilled-by"
ORDER BY total_revenue DESC;


-- ============================================================
-- Q8. What is the monthly revenue trend?
--     (Is the business growing month over month?)
-- ============================================================
SELECT
    SUBSTR(Date, 1, 2) AS month,
    COUNT(*) AS total_orders,
    ROUND(SUM(Amount), 2) AS total_revenue,
    ROUND(AVG(Amount), 2) AS avg_order_value
FROM amazon_sales
WHERE Status NOT LIKE '%Cancelled%'
  AND Amount IS NOT NULL
  AND Date IS NOT NULL
GROUP BY month
ORDER BY month;


-- ============================================================
-- Q9. Which Size sells the most and generates most revenue?
--     (Inventory planning — which sizes to stock more of)
-- ============================================================
SELECT
    Size,
    COUNT(*) AS total_orders,
    ROUND(SUM(Amount), 2) AS total_revenue,
    ROUND(SUM(Qty), 0) AS total_units
FROM amazon_sales
WHERE Status NOT LIKE '%Cancelled%'
  AND Amount IS NOT NULL
  AND Size IS NOT NULL
GROUP BY Size
ORDER BY total_units DESC
LIMIT 15;


-- ============================================================
-- Q10. Which cities are the top 10 revenue drivers?
--      (City-level performance for hyperlocal targeting)
-- ============================================================
SELECT
    "ship-city" AS city,
    "ship-state" AS state,
    COUNT(*) AS total_orders,
    ROUND(SUM(Amount), 2) AS total_revenue,
    ROUND(AVG(Amount), 2) AS avg_order_value
FROM amazon_sales
WHERE Status NOT LIKE '%Cancelled%'
  AND Amount IS NOT NULL
  AND "ship-city" IS NOT NULL
GROUP BY "ship-city"
ORDER BY total_revenue DESC
LIMIT 10;
