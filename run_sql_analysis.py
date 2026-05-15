import pandas as pd
import sqlite3
import warnings
warnings.filterwarnings('ignore')

# ── Load CSV ──────────────────────────────────────────────
print("Loading Amazon Sale Report...")
df = pd.read_csv('data/raw/Amazon Sale Report.csv', encoding='latin-1', low_memory=False)

# Clean column names (strip spaces)
df.columns = df.columns.str.strip()

# Convert Amount and Qty to numeric
df['Amount'] = pd.to_numeric(df['Amount'], errors='coerce')
df['Qty'] = pd.to_numeric(df['Qty'], errors='coerce')

print(f"Loaded {len(df):,} rows and {len(df.columns)} columns")

# ── Load into SQLite ──────────────────────────────────────
conn = sqlite3.connect('data/cleaned/ecommerce.db')
df.to_sql('amazon_sales', conn, if_exists='replace', index=False)
print("Data loaded into SQLite: data/cleaned/ecommerce.db\n")

# ── Run all 10 queries ────────────────────────────────────
queries = {
    "Q1 - Revenue by Order Status": """
        SELECT Status, COUNT(*) AS total_orders,
            ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM amazon_sales), 2) AS pct_of_orders,
            ROUND(SUM(Amount), 2) AS total_revenue
        FROM amazon_sales WHERE Amount IS NOT NULL
        GROUP BY Status ORDER BY total_orders DESC
    """,
    "Q2 - Revenue vs Volume by Category": """
        SELECT Category, COUNT(*) AS total_orders,
            ROUND(SUM(Amount), 2) AS total_revenue,
            ROUND(AVG(Amount), 2) AS avg_order_value,
            ROUND(SUM(Qty), 0) AS total_units_sold
        FROM amazon_sales
        WHERE Status NOT LIKE '%Cancelled%' AND Amount IS NOT NULL
        GROUP BY Category ORDER BY total_revenue DESC
    """,
    "Q3 - Top 10 States by Revenue": """
        SELECT "ship-state" AS state, COUNT(*) AS total_orders,
            ROUND(SUM(Amount), 2) AS total_revenue,
            ROUND(AVG(Amount), 2) AS avg_order_value
        FROM amazon_sales
        WHERE Status NOT LIKE '%Cancelled%' AND Amount IS NOT NULL AND "ship-state" IS NOT NULL
        GROUP BY "ship-state" ORDER BY total_revenue DESC LIMIT 10
    """,
    "Q4 - Opportunity Markets (High AOV, Low Volume)": """
        SELECT "ship-state" AS state, COUNT(*) AS total_orders,
            ROUND(AVG(Amount), 2) AS avg_order_value
        FROM amazon_sales
        WHERE Status NOT LIKE '%Cancelled%' AND Amount IS NOT NULL AND "ship-state" IS NOT NULL
        GROUP BY "ship-state"
        HAVING avg_order_value > (SELECT AVG(Amount) FROM amazon_sales WHERE Amount IS NOT NULL)
        AND total_orders < (SELECT AVG(order_count) FROM (SELECT COUNT(*) AS order_count FROM amazon_sales GROUP BY "ship-state"))
        ORDER BY avg_order_value DESC LIMIT 10
    """,
    "Q5 - Cancellation Rate by Category": """
        SELECT Category, COUNT(*) AS total_orders,
            SUM(CASE WHEN Status LIKE '%Cancelled%' THEN 1 ELSE 0 END) AS cancelled_orders,
            ROUND(SUM(CASE WHEN Status LIKE '%Cancelled%' THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) AS cancellation_rate_pct
        FROM amazon_sales WHERE Category IS NOT NULL
        GROUP BY Category ORDER BY cancellation_rate_pct DESC
    """,
    "Q6 - B2B vs B2C Segment Comparison": """
        SELECT CASE WHEN B2B = 'True' THEN 'B2B' ELSE 'B2C' END AS customer_segment,
            COUNT(*) AS total_orders,
            ROUND(SUM(Amount), 2) AS total_revenue,
            ROUND(AVG(Amount), 2) AS avg_order_value,
            ROUND(AVG(Qty), 2) AS avg_units_per_order
        FROM amazon_sales
        WHERE Status NOT LIKE '%Cancelled%' AND Amount IS NOT NULL
        GROUP BY B2B
    """,
    "Q7 - Fulfilment Method Performance": """
        SELECT "fulfilled-by" AS fulfilment_method,
            COUNT(*) AS total_orders,
            ROUND(SUM(Amount), 2) AS total_revenue,
            ROUND(AVG(Amount), 2) AS avg_order_value,
            SUM(CASE WHEN Status LIKE '%Delivered%' THEN 1 ELSE 0 END) AS delivered,
            SUM(CASE WHEN Status LIKE '%Cancelled%' THEN 1 ELSE 0 END) AS cancelled,
            ROUND(SUM(CASE WHEN Status LIKE '%Delivered%' THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) AS delivery_rate_pct
        FROM amazon_sales WHERE "fulfilled-by" IS NOT NULL
        GROUP BY "fulfilled-by" ORDER BY total_revenue DESC
    """,
    "Q8 - Monthly Revenue Trend": """
        SELECT SUBSTR(Date, 1, 2) AS month, COUNT(*) AS total_orders,
            ROUND(SUM(Amount), 2) AS total_revenue,
            ROUND(AVG(Amount), 2) AS avg_order_value
        FROM amazon_sales
        WHERE Status NOT LIKE '%Cancelled%' AND Amount IS NOT NULL AND Date IS NOT NULL
        GROUP BY month ORDER BY month
    """,
    "Q9 - Top Sizes by Units Sold": """
        SELECT Size, COUNT(*) AS total_orders,
            ROUND(SUM(Amount), 2) AS total_revenue,
            ROUND(SUM(Qty), 0) AS total_units
        FROM amazon_sales
        WHERE Status NOT LIKE '%Cancelled%' AND Amount IS NOT NULL AND Size IS NOT NULL
        GROUP BY Size ORDER BY total_units DESC LIMIT 15
    """,
    "Q10 - Top 10 Cities by Revenue": """
        SELECT "ship-city" AS city, "ship-state" AS state,
            COUNT(*) AS total_orders,
            ROUND(SUM(Amount), 2) AS total_revenue,
            ROUND(AVG(Amount), 2) AS avg_order_value
        FROM amazon_sales
        WHERE Status NOT LIKE '%Cancelled%' AND Amount IS NOT NULL AND "ship-city" IS NOT NULL
        GROUP BY "ship-city" ORDER BY total_revenue DESC LIMIT 10
    """
}

# Run and print each query
for title, query in queries.items():
    print(f"\n{'='*60}")
    print(f"  {title}")
    print('='*60)
    result = pd.read_sql_query(query, conn)
    print(result.to_string(index=False))

conn.close()
print("\n\nAll 10 queries complete. SQLite DB saved at data/cleaned/ecommerce.db")
