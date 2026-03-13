# CSAS SQL Queries

This document lists all analytics SQL queries used by the backend.

## Customer Analytics

### Top Customers by Spending
```sql
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
LIMIT ?;
```

### Top Customers by Orders
```sql
SELECT
    c.customer_id,
    c.name,
    c.city,
    COUNT(o.order_id) AS orders_count
FROM customers c
JOIN orders o ON o.customer_id = c.customer_id
GROUP BY c.customer_id, c.name, c.city
ORDER BY orders_count DESC
LIMIT ?;
```

### Customers by City
```sql
SELECT city, COUNT(*) AS customer_count
FROM customers
GROUP BY city
ORDER BY customer_count DESC;
```

### Customer Lifetime Value (Top N)
```sql
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
LIMIT ?;
```

### Repeat vs New Customers
```sql
SELECT
    CASE WHEN order_count > 1 THEN 'Repeat' ELSE 'New' END AS customer_type,
    COUNT(*) AS customer_count
FROM (
    SELECT customer_id, COUNT(order_id) AS order_count
    FROM orders
    GROUP BY customer_id
) AS sub
GROUP BY customer_type;
```

### Customer Order Frequency
```sql
SELECT
    order_count,
    COUNT(*) AS num_customers
FROM (
    SELECT customer_id, COUNT(order_id) AS order_count
    FROM orders
    GROUP BY customer_id
) AS sub
GROUP BY order_count
ORDER BY order_count;
```

## Product Analytics

### Top Products by Revenue
```sql
SELECT
    p.product_id, p.product_name, p.category,
    SUM(oi.quantity * p.price) AS total_revenue
FROM products p
JOIN order_items oi ON oi.product_id = p.product_id
GROUP BY p.product_id, p.product_name, p.category
ORDER BY total_revenue DESC
LIMIT ?;
```

### Top Products by Quantity
```sql
SELECT
    p.product_id, p.product_name, p.category,
    SUM(oi.quantity) AS total_quantity
FROM products p
JOIN order_items oi ON oi.product_id = p.product_id
GROUP BY p.product_id, p.product_name, p.category
ORDER BY total_quantity DESC
LIMIT ?;
```

### Items Sold per Category
```sql
SELECT p.category, SUM(oi.quantity) AS total_quantity
FROM products p
JOIN order_items oi ON oi.product_id = p.product_id
GROUP BY p.category
ORDER BY total_quantity DESC;
```

### Revenue by Category
```sql
SELECT p.category, SUM(oi.quantity * p.price) AS total_revenue
FROM products p
JOIN order_items oi ON oi.product_id = p.product_id
GROUP BY p.category
ORDER BY total_revenue DESC;
```

### Underperforming Products (Lowest Revenue)
```sql
SELECT
    p.product_id, p.product_name, p.category,
    SUM(oi.quantity * p.price) AS total_revenue
FROM products p
JOIN order_items oi ON oi.product_id = p.product_id
GROUP BY p.product_id, p.product_name, p.category
HAVING total_revenue > 0
ORDER BY total_revenue ASC
LIMIT ?;
```

### Price vs Revenue (Scatter)
```sql
SELECT
    p.product_name,
    p.category,
    p.price,
    SUM(oi.quantity) AS total_units_sold,
    SUM(oi.quantity * p.price) AS total_revenue
FROM products p
JOIN order_items oi ON oi.product_id = p.product_id
GROUP BY p.product_id, p.product_name, p.category, p.price
ORDER BY total_revenue DESC;
```

### Average Price by Category
```sql
SELECT category, ROUND(AVG(price), 2) AS avg_price, COUNT(*) AS product_count
FROM products
GROUP BY category
ORDER BY avg_price DESC;
```

## Sales Analytics

### Monthly Sales Trend
```sql
SELECT
    DATE_FORMAT(o.order_date, '%Y-%m') AS month,
    SUM(oi.quantity * p.price) AS total_revenue
FROM orders o
JOIN order_items oi ON oi.order_id = o.order_id
JOIN products p ON p.product_id = oi.product_id
GROUP BY month
ORDER BY month;
```

### Orders per Month
```sql
SELECT DATE_FORMAT(order_date, '%Y-%m') AS month, COUNT(*) AS orders_count
FROM orders
GROUP BY month
ORDER BY month;
```

### Revenue by City
```sql
SELECT
    c.city,
    SUM(oi.quantity * p.price) AS total_revenue
FROM customers c
JOIN orders o ON o.customer_id = c.customer_id
JOIN order_items oi ON oi.order_id = o.order_id
JOIN products p ON p.product_id = oi.product_id
GROUP BY c.city
ORDER BY total_revenue DESC;
```

### Order Status Breakdown
```sql
SELECT
    status,
    COUNT(*) AS orders_count,
    ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM orders), 2) AS percentage_of_total
FROM orders
GROUP BY status
ORDER BY orders_count DESC;
```

### Monthly Revenue Growth (MoM %)
```sql
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
ORDER BY month;
```

### Revenue by Weekday
```sql
SELECT
    DAYNAME(o.order_date) AS weekday,
    DAYOFWEEK(o.order_date) AS day_num,
    SUM(oi.quantity * p.price) AS total_revenue,
    COUNT(DISTINCT o.order_id) AS orders_count
FROM orders o
JOIN order_items oi ON oi.order_id = o.order_id
JOIN products p ON p.product_id = oi.product_id
GROUP BY weekday, day_num
ORDER BY day_num;
```

### City × Category Revenue Heatmap
```sql
SELECT
    c.city,
    p.category,
    SUM(oi.quantity * p.price) AS total_revenue
FROM customers c
JOIN orders o ON o.customer_id = c.customer_id
JOIN order_items oi ON oi.order_id = o.order_id
JOIN products p ON p.product_id = oi.product_id
GROUP BY c.city, p.category
ORDER BY c.city, total_revenue DESC;
```

## Order Analytics

### Average Order Value
```sql
SELECT ROUND(SUM(oi.quantity * p.price) / COUNT(DISTINCT o.order_id), 2) AS avg_order_value
FROM orders o
JOIN order_items oi ON oi.order_id = o.order_id
JOIN products p ON p.product_id = oi.product_id;
```

### Average Items per Order
```sql
SELECT ROUND(SUM(oi.quantity) / COUNT(DISTINCT o.order_id), 2) AS avg_items_per_order
FROM orders o
JOIN order_items oi ON oi.order_id = o.order_id;
```

### Order Value Distribution
```sql
SELECT
    CASE
        WHEN order_total < 50    THEN 'Under $50'
        WHEN order_total < 100   THEN '$50-$100'
        WHEN order_total < 200   THEN '$100-$200'
        WHEN order_total < 500   THEN '$200-$500'
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
ORDER BY MIN(order_total);
```

### High Value Orders (Top N)
```sql
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
LIMIT ?;
```