"""
Simple filter analysis queries for CSAS.
2 endpoints per table: customers, orders, order_items, products.
"""

from datetime import date
from typing import Optional

from .crud import fetch_all, fetch_one


# ----------------------------
# Customers (2)
# ----------------------------

def customers_list(
    city: Optional[str] = None,
    signup_from: Optional[date] = None,
    signup_to: Optional[date] = None,
    name_like: Optional[str] = None,
    min_orders: Optional[int] = None,
    top_n: int = 20,
):
    query = """
        SELECT
            c.customer_id,
            c.name,
            c.city,
            c.signup_date,
            COUNT(DISTINCT o.order_id) AS total_orders
        FROM customers c
        LEFT JOIN orders o ON o.customer_id = c.customer_id
        WHERE 1=1
    """
    params = []
    if city:
        query += " AND c.city = %s"
        params.append(city)
    if signup_from is not None:
        query += " AND c.signup_date >= %s"
        params.append(signup_from)
    if signup_to is not None:
        query += " AND c.signup_date <= %s"
        params.append(signup_to)
    if name_like:
        query += " AND c.name LIKE %s"
        params.append(f"%{name_like}%")

    query += """
        GROUP BY c.customer_id, c.name, c.city, c.signup_date
    """
    if min_orders is not None:
        query += " HAVING COUNT(DISTINCT o.order_id) >= %s"
        params.append(min_orders)

    query += " ORDER BY total_orders DESC, c.customer_id ASC LIMIT %s"
    params.append(top_n)
    return fetch_all(query, tuple(params))


def customers_spend_summary(
    city: Optional[str] = None,
    signup_from: Optional[date] = None,
    signup_to: Optional[date] = None,
    min_total_spend: Optional[float] = None,
    max_total_spend: Optional[float] = None,
    top_n: int = 20,
):
    query = """
        SELECT
            x.customer_id,
            x.name,
            x.city,
            x.total_orders,
            x.total_spend,
            x.avg_order_value
        FROM (
            SELECT
                c.customer_id,
                c.name,
                c.city,
                COUNT(DISTINCT o.order_id) AS total_orders,
                ROUND(COALESCE(SUM(oi.quantity * p.price), 0), 2) AS total_spend,
                ROUND(
                    COALESCE(SUM(oi.quantity * p.price), 0) / NULLIF(COUNT(DISTINCT o.order_id), 0),
                    2
                ) AS avg_order_value,
                c.signup_date
            FROM customers c
            LEFT JOIN orders o ON o.customer_id = c.customer_id
            LEFT JOIN order_items oi ON oi.order_id = o.order_id
            LEFT JOIN products p ON p.product_id = oi.product_id
            GROUP BY c.customer_id, c.name, c.city, c.signup_date
        ) AS x
        WHERE 1=1
    """
    params = []
    if city:
        query += " AND x.city = %s"
        params.append(city)
    if signup_from is not None:
        query += " AND x.signup_date >= %s"
        params.append(signup_from)
    if signup_to is not None:
        query += " AND x.signup_date <= %s"
        params.append(signup_to)
    if min_total_spend is not None:
        query += " AND x.total_spend >= %s"
        params.append(min_total_spend)
    if max_total_spend is not None:
        query += " AND x.total_spend <= %s"
        params.append(max_total_spend)

    query += " ORDER BY x.total_spend DESC LIMIT %s"
    params.append(top_n)
    return fetch_all(query, tuple(params))


# ----------------------------
# Orders (2)
# ----------------------------

def orders_list(
    date_from: Optional[date] = None,
    date_to: Optional[date] = None,
    status: Optional[str] = None,
    customer_id: Optional[int] = None,
    city: Optional[str] = None,
    top_n: int = 20,
):
    query = """
        SELECT
            o.order_id,
            o.customer_id,
            c.name AS customer_name,
            c.city,
            o.order_date,
            o.status
        FROM orders o
        JOIN customers c ON c.customer_id = o.customer_id
        WHERE 1=1
    """
    params = []
    if date_from is not None:
        query += " AND o.order_date >= %s"
        params.append(date_from)
    if date_to is not None:
        query += " AND o.order_date <= %s"
        params.append(date_to)
    if status:
        query += " AND o.status = %s"
        params.append(status)
    if customer_id is not None:
        query += " AND o.customer_id = %s"
        params.append(customer_id)
    if city:
        query += " AND c.city = %s"
        params.append(city)

    query += " ORDER BY o.order_date DESC, o.order_id DESC LIMIT %s"
    params.append(top_n)
    return fetch_all(query, tuple(params))


def orders_value_summary(
    date_from: Optional[date] = None,
    date_to: Optional[date] = None,
    status: Optional[str] = None,
    customer_id: Optional[int] = None,
    min_order_total: Optional[float] = None,
    max_order_total: Optional[float] = None,
):
    query = """
        SELECT
            x.order_id,
            x.customer_id,
            x.order_date,
            x.status,
            x.order_total,
            x.total_items
        FROM (
            SELECT
                o.order_id,
                o.customer_id,
                o.order_date,
                o.status,
                ROUND(SUM(oi.quantity * p.price), 2) AS order_total,
                SUM(oi.quantity) AS total_items
            FROM orders o
            JOIN order_items oi ON oi.order_id = o.order_id
            JOIN products p ON p.product_id = oi.product_id
            GROUP BY o.order_id, o.customer_id, o.order_date, o.status
        ) AS x
        WHERE 1=1
    """
    params = []
    if date_from is not None:
        query += " AND x.order_date >= %s"
        params.append(date_from)
    if date_to is not None:
        query += " AND x.order_date <= %s"
        params.append(date_to)
    if status:
        query += " AND x.status = %s"
        params.append(status)
    if customer_id is not None:
        query += " AND x.customer_id = %s"
        params.append(customer_id)
    if min_order_total is not None:
        query += " AND x.order_total >= %s"
        params.append(min_order_total)
    if max_order_total is not None:
        query += " AND x.order_total <= %s"
        params.append(max_order_total)

    query += " ORDER BY x.order_total DESC, x.order_id DESC"
    return fetch_all(query, tuple(params))


# ----------------------------
# Order items (2)
# ----------------------------

def order_items_list(
    order_id: Optional[int] = None,
    product_id: Optional[int] = None,
    category: Optional[str] = None,
    min_quantity: Optional[int] = None,
    max_quantity: Optional[int] = None,
    top_n: int = 30,
):
    query = """
        SELECT
            oi.order_item_id,
            oi.order_id,
            oi.product_id,
            p.product_name,
            p.category,
            oi.quantity,
            p.price,
            ROUND(oi.quantity * p.price, 2) AS line_total
        FROM order_items oi
        JOIN products p ON p.product_id = oi.product_id
        WHERE 1=1
    """
    params = []
    if order_id is not None:
        query += " AND oi.order_id = %s"
        params.append(order_id)
    if product_id is not None:
        query += " AND oi.product_id = %s"
        params.append(product_id)
    if category:
        query += " AND p.category = %s"
        params.append(category)
    if min_quantity is not None:
        query += " AND oi.quantity >= %s"
        params.append(min_quantity)
    if max_quantity is not None:
        query += " AND oi.quantity <= %s"
        params.append(max_quantity)

    query += " ORDER BY line_total DESC, oi.order_item_id DESC LIMIT %s"
    params.append(top_n)
    return fetch_all(query, tuple(params))


def order_items_grouped(
    category: Optional[str] = None,
    product_id: Optional[int] = None,
    date_from: Optional[date] = None,
    date_to: Optional[date] = None,
    min_units: Optional[int] = None,
    top_n: int = 20,
):
    query = """
        SELECT
            p.product_id,
            p.product_name,
            p.category,
            SUM(oi.quantity) AS units_sold,
            ROUND(SUM(oi.quantity * p.price), 2) AS total_revenue,
            COUNT(DISTINCT oi.order_id) AS order_count
        FROM order_items oi
        JOIN products p ON p.product_id = oi.product_id
        JOIN orders o ON o.order_id = oi.order_id
        WHERE 1=1
    """
    params = []
    if category:
        query += " AND p.category = %s"
        params.append(category)
    if product_id is not None:
        query += " AND p.product_id = %s"
        params.append(product_id)
    if date_from is not None:
        query += " AND o.order_date >= %s"
        params.append(date_from)
    if date_to is not None:
        query += " AND o.order_date <= %s"
        params.append(date_to)

    query += " GROUP BY p.product_id, p.product_name, p.category"
    if min_units is not None:
        query += " HAVING SUM(oi.quantity) >= %s"
        params.append(min_units)

    query += " ORDER BY total_revenue DESC, units_sold DESC LIMIT %s"
    params.append(top_n)
    return fetch_all(query, tuple(params))


# ----------------------------
# Products (2)
# ----------------------------

def products_list(
    category: Optional[str] = None,
    min_price: Optional[float] = None,
    max_price: Optional[float] = None,
    name_like: Optional[str] = None,
    product_id: Optional[int] = None,
    top_n: int = 30,
):
    query = """
        SELECT
            p.product_id,
            p.product_name,
            p.category,
            p.price
        FROM products p
        WHERE 1=1
    """
    params = []
    if category:
        query += " AND p.category = %s"
        params.append(category)
    if min_price is not None:
        query += " AND p.price >= %s"
        params.append(min_price)
    if max_price is not None:
        query += " AND p.price <= %s"
        params.append(max_price)
    if name_like:
        query += " AND p.product_name LIKE %s"
        params.append(f"%{name_like}%")
    if product_id is not None:
        query += " AND p.product_id = %s"
        params.append(product_id)

    query += " ORDER BY p.price DESC, p.product_id ASC LIMIT %s"
    params.append(top_n)
    return fetch_all(query, tuple(params))


def products_sales_summary(
    category: Optional[str] = None,
    date_from: Optional[date] = None,
    date_to: Optional[date] = None,
    min_revenue: Optional[float] = None,
    max_revenue: Optional[float] = None,
    top_n: int = 20,
):
    query = """
        SELECT
            x.product_id,
            x.product_name,
            x.category,
            x.price,
            x.units_sold,
            x.total_revenue,
            x.order_count
        FROM (
            SELECT
                p.product_id,
                p.product_name,
                p.category,
                p.price,
                SUM(oi.quantity) AS units_sold,
                ROUND(SUM(oi.quantity * p.price), 2) AS total_revenue,
                COUNT(DISTINCT o.order_id) AS order_count,
                MIN(o.order_date) AS first_order_date,
                MAX(o.order_date) AS last_order_date
            FROM products p
            JOIN order_items oi ON oi.product_id = p.product_id
            JOIN orders o ON o.order_id = oi.order_id
            GROUP BY p.product_id, p.product_name, p.category, p.price
        ) AS x
        WHERE 1=1
    """
    params = []
    if category:
        query += " AND x.category = %s"
        params.append(category)
    if date_from is not None:
        query += " AND x.last_order_date >= %s"
        params.append(date_from)
    if date_to is not None:
        query += " AND x.first_order_date <= %s"
        params.append(date_to)
    if min_revenue is not None:
        query += " AND x.total_revenue >= %s"
        params.append(min_revenue)
    if max_revenue is not None:
        query += " AND x.total_revenue <= %s"
        params.append(max_revenue)

    query += " ORDER BY x.total_revenue DESC, x.units_sold DESC LIMIT %s"
    params.append(top_n)
    return fetch_all(query, tuple(params))

