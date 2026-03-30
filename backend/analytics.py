
"""
Analytics queries for the CSAS project.
Each function returns rows from MySQL for a specific analytics use case.
"""

from .crud import fetch_all, fetch_one


# ----------------------------
# Customer Analytics
# ----------------------------

def top_customers_by_spending(limit: int = 10):
    query = """
        SELECT
            c.customer_id,
            c.name,
            c.city,
            SUM(oi.quantity * p.price) AS total_spend,
            COUNT(DISTINCT o.order_id) AS total_orders
        FROM customers c
        JOIN orders o ON o.customer_id = c.customer_id
        JOIN order_items oi ON oi.order_id = o.order_id
        JOIN products p ON p.product_id = oi.product_id
        GROUP BY c.customer_id, c.name, c.city
        ORDER BY total_spend DESC
        LIMIT %s
    """
    return fetch_all(query, (limit,))


def top_customers_by_orders(limit: int = 10):
    query = """
        SELECT
            c.customer_id,
            c.name,
            c.city,
            COUNT(o.order_id) AS orders_count
        FROM customers c
        JOIN orders o ON o.customer_id = c.customer_id
        GROUP BY c.customer_id, c.name, c.city
        ORDER BY orders_count DESC
        LIMIT %s
    """
    return fetch_all(query, (limit,))


def customers_by_city():
    query = """
        SELECT city, COUNT(*) AS customer_count
        FROM customers
        GROUP BY city
        ORDER BY customer_count DESC
    """
    return fetch_all(query)


def customer_lifetime_value(limit: int = 20):
    """
    Customer Lifetime Value: total spend, avg order value, order frequency.
    """
    query = """
        SELECT
            c.customer_id,
            c.name,
            c.city,
            COUNT(DISTINCT o.order_id)                              AS total_orders,
            SUM(oi.quantity * p.price)                              AS total_spend,
            ROUND(SUM(oi.quantity * p.price) /
                  COUNT(DISTINCT o.order_id), 2)                    AS avg_order_value,
            DATEDIFF(MAX(o.order_date), MIN(o.order_date))          AS customer_lifespan_days
        FROM customers c
        JOIN orders o ON o.customer_id = c.customer_id
        JOIN order_items oi ON oi.order_id = o.order_id
        JOIN products p ON p.product_id = oi.product_id
        GROUP BY c.customer_id, c.name, c.city
        ORDER BY total_spend DESC
        LIMIT %s
    """
    return fetch_all(query, (limit,))


def repeat_vs_new_customers():
    """
    Ratio of repeat customers (>1 order) vs one-time buyers.
    """
    query = """
        SELECT
            CASE WHEN order_count > 1 THEN 'Repeat' ELSE 'New' END AS customer_type,
            COUNT(*) AS customer_count
        FROM (
            SELECT customer_id, COUNT(order_id) AS order_count
            FROM orders
            GROUP BY customer_id
        ) AS sub
        GROUP BY customer_type
    """
    return fetch_all(query)


def customer_order_frequency():
    """
    Distribution of how many orders customers place.
    """
    query = """
        SELECT
            order_count,
            COUNT(*) AS num_customers
        FROM (
            SELECT customer_id, COUNT(order_id) AS order_count
            FROM orders
            GROUP BY customer_id
        ) AS sub
        GROUP BY order_count
        ORDER BY order_count
    """
    return fetch_all(query)


# ----------------------------
# Product Analytics
# ----------------------------

def top_products_by_revenue(limit: int = 10):
    query = """
        SELECT
            p.product_id, p.product_name, p.category,
            SUM(oi.quantity * p.price) AS total_revenue
        FROM products p
        JOIN order_items oi ON oi.product_id = p.product_id
        GROUP BY p.product_id, p.product_name, p.category
        ORDER BY total_revenue DESC
        LIMIT %s
    """
    return fetch_all(query, (limit,))


def top_products_by_quantity(limit: int = 10):
    query = """
        SELECT
            p.product_id, p.product_name, p.category,
            SUM(oi.quantity) AS total_quantity
        FROM products p
        JOIN order_items oi ON oi.product_id = p.product_id
        GROUP BY p.product_id, p.product_name, p.category
        ORDER BY total_quantity DESC
        LIMIT %s
    """
    return fetch_all(query, (limit,))


def items_sold_per_category():
    query = """
        SELECT p.category, SUM(oi.quantity) AS total_quantity
        FROM products p
        JOIN order_items oi ON oi.product_id = p.product_id
        GROUP BY p.category
        ORDER BY total_quantity DESC
    """
    return fetch_all(query)


def revenue_by_category():
    query = """
        SELECT p.category, SUM(oi.quantity * p.price) AS total_revenue
        FROM products p
        JOIN order_items oi ON oi.product_id = p.product_id
        GROUP BY p.category
        ORDER BY total_revenue DESC
    """
    return fetch_all(query)


def underperforming_products(limit: int = 10):
    query = """
        SELECT
            p.product_id, p.product_name, p.category,
            SUM(oi.quantity * p.price) AS total_revenue
        FROM products p
        JOIN order_items oi ON oi.product_id = p.product_id
        GROUP BY p.product_id, p.product_name, p.category
        HAVING total_revenue > 0
        ORDER BY total_revenue ASC
        LIMIT %s
    """
    return fetch_all(query, (limit,))


def product_price_vs_revenue():
    """
    Price vs total revenue scatter — reveals pricing sweet spots.
    """
    query = """
        SELECT
            p.product_name,
            p.category,
            p.price,
            SUM(oi.quantity) AS total_units_sold,
            SUM(oi.quantity * p.price) AS total_revenue
        FROM products p
        JOIN order_items oi ON oi.product_id = p.product_id
        GROUP BY p.product_id, p.product_name, p.category, p.price
        ORDER BY total_revenue DESC
    """
    return fetch_all(query)


def category_avg_price():
    """
    Average product price per category.
    """
    query = """
        SELECT category, ROUND(AVG(price), 2) AS avg_price, COUNT(*) AS product_count
        FROM products
        GROUP BY category
        ORDER BY avg_price DESC
    """
    return fetch_all(query)


# ----------------------------
# Sales Analytics
# ----------------------------

def monthly_sales_trend():
    query = """
        SELECT
            DATE_FORMAT(o.order_date, '%Y-%m') AS month,
            SUM(oi.quantity * p.price) AS total_revenue
        FROM orders o
        JOIN order_items oi ON oi.order_id = o.order_id
        JOIN products p ON p.product_id = oi.product_id
        GROUP BY month
        ORDER BY month
    """
    return fetch_all(query)


def orders_per_month():
    query = """
        SELECT DATE_FORMAT(order_date, '%Y-%m') AS month, COUNT(*) AS orders_count
        FROM orders
        GROUP BY month
        ORDER BY month
    """
    return fetch_all(query)


def revenue_by_city():  
    query = """
        SELECT
            c.city,
            SUM(oi.quantity * p.price) AS total_revenue
        FROM customers c
        JOIN orders o ON o.customer_id = c.customer_id
        JOIN order_items oi ON oi.order_id = o.order_id
        JOIN products p ON p.product_id = oi.product_id
        GROUP BY c.city
        ORDER BY total_revenue DESC
    """
    return fetch_all(query)


def order_status_breakdown():
    query = """
        SELECT
            status,
            COUNT(*) AS orders_count,
            ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM orders), 2) AS percentage_of_total
        FROM orders
        GROUP BY status
        ORDER BY orders_count DESC
    """
    return fetch_all(query)


def monthly_revenue_growth():
    """
    Month-over-month revenue growth percentage.
    """
    query = """
        SELECT
            month,
            total_revenue,
            LAG(total_revenue) OVER (ORDER BY month) AS prev_revenue,
            ROUND(
                (total_revenue - LAG(total_revenue) OVER (ORDER BY month))
                / LAG(total_revenue) OVER (ORDER BY month) * 100, 2
            ) AS growth_pct
        FROM (
            SELECT
                DATE_FORMAT(o.order_date, '%Y-%m') AS month,
                SUM(oi.quantity * p.price) AS total_revenue
            FROM orders o
            JOIN order_items oi ON oi.order_id = o.order_id
            JOIN products p ON p.product_id = oi.product_id
            GROUP BY month
        ) AS monthly
        ORDER BY month
    """
    return fetch_all(query)


def revenue_by_weekday():
    """
    Which days of the week generate the most revenue.
    """
    query = """
        SELECT
            DAYNAME(o.order_date) AS weekday,
            DAYOFWEEK(o.order_date) AS day_num,
            SUM(oi.quantity * p.price) AS total_revenue,
            COUNT(DISTINCT o.order_id) AS orders_count
        FROM orders o
        JOIN order_items oi ON oi.order_id = o.order_id
        JOIN products p ON p.product_id = oi.product_id
        GROUP BY weekday, day_num
        ORDER BY day_num
    """
    return fetch_all(query)


def top_city_category_combos():
    """
    Which city buys which categories the most — heatmap data.
    """
    query = """
        SELECT
            c.city,
            p.category,
            SUM(oi.quantity * p.price) AS total_revenue
        FROM customers c
        JOIN orders o ON o.customer_id = c.customer_id
        JOIN order_items oi ON oi.order_id = o.order_id
        JOIN products p ON p.product_id = oi.product_id
        GROUP BY c.city, p.category
        ORDER BY c.city, total_revenue DESC
    """
    return fetch_all(query)


# ----------------------------
# Order Analytics
# ----------------------------

def average_order_value():
    query = """
        SELECT ROUND(SUM(oi.quantity * p.price) / COUNT(DISTINCT o.order_id), 2) AS avg_order_value
        FROM orders o
        JOIN order_items oi ON oi.order_id = o.order_id
        JOIN products p ON p.product_id = oi.product_id
    """
    return fetch_one(query)


def average_items_per_order():
    query = """
        SELECT ROUND(SUM(oi.quantity) / COUNT(DISTINCT o.order_id), 2) AS avg_items_per_order
        FROM orders o
        JOIN order_items oi ON oi.order_id = o.order_id
    """
    return fetch_one(query)


def order_value_distribution():
    """
    Bucket orders into value ranges to show spend distribution.
    """
    query = """
        SELECT
            CASE
                WHEN order_total < 50    THEN 'Under $50'
                WHEN order_total < 100   THEN '$50–$100'
                WHEN order_total < 200   THEN '$100–$200'
                WHEN order_total < 500   THEN '$200–$500'
                ELSE 'Over $500'
            END AS value_bucket,
            COUNT(*) AS orders_count
        FROM (
            SELECT o.order_id, SUM(oi.quantity * p.price) AS order_total
            FROM orders o
            JOIN order_items oi ON oi.order_id = o.order_id
            JOIN products p ON p.product_id = oi.product_id
            GROUP BY o.order_id
        ) AS order_totals
        GROUP BY value_bucket
        ORDER BY MIN(order_total)
    """
    return fetch_all(query)


def high_value_orders(limit: int = 10):
    """
    Top N highest-value individual orders.
    """
    query = """
        SELECT
            o.order_id,
            c.name AS customer_name,
            c.city,
            o.order_date,
            o.status,
            SUM(oi.quantity * p.price) AS order_total,
            COUNT(oi.product_id) AS distinct_products
        FROM orders o
        JOIN customers c ON c.customer_id = o.customer_id
        JOIN order_items oi ON oi.order_id = o.order_id
        JOIN products p ON p.product_id = oi.product_id
        GROUP BY o.order_id, c.name, c.city, o.order_date, o.status
        ORDER BY order_total DESC
        LIMIT %s
    """
    return fetch_all(query, (limit,))

