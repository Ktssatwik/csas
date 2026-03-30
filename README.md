# CSAS — Customer Sales Analytics System

A retail analytics platform built with **FastAPI + MySQL + Streamlit**.

## Setup

### 0. create a venv and use it 

### 1. Install dependencies
```bash
pip install -r requirements.txt
```

### 2. Configure environment
Create a `.env` file in the project root:
```
DB_HOST=localhost
DB_PORT=3306
DB_USER=root
DB_PASSWORD=your_password
DB_NAME=csas
```

### 3. Load data into MySQL
```bash
python -m database.load_data
```
This will: create the `csas` database, run `schema.sql`, and import all CSVs.

### 4. Start the FastAPI backend
```bash
python -m uvicorn backend.main:app --reload
```
API docs available at: http://localhost:8000/docs

### 5. Start the Streamlit frontend
```bash
python -m streamlit run frontend/app.py
```
Dashboard at: http://localhost:8501

---

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/customers/` | Paginated customer list |
| GET | `/products/` | Paginated product list |
| GET | `/orders/` | Paginated order list |
| GET | `/analytics/repeat-customers` | Loyal customers (≥N orders) |
| GET | `/analytics/top-customers` | Highest spenders |
| GET | `/analytics/top-products` | Best-selling products |
| GET | `/analytics/sales-by-city` | Revenue by city |
| GET | `/analytics/sales-by-month` | Monthly revenue trend |
| GET | `/analytics/sales-by-category` | Revenue by category |

All analytics endpoints accept optional `date_from` and `date_to` query parameters (format: `YYYY-MM-DD`).

---

## Flow Pipeline

```
CSV Files → load_data.py → MySQL → FastAPI → API Endpoints → Streamlit → Dashboard
```

---

## New Updates: Dynamic Filter Module

The project now includes a dedicated filter module:

- `backend/filter_analysis.py`
- `backend/routes/filter_routes.py`

And the routes are registered in `backend/main.py` using:

```python
app.include_router(filter_routes.router)
```

### Filter API Base Path

All new filter APIs are under:

`/analytics/filters`

### 8 New Filter Endpoints (2 per data domain)

| Method | Endpoint | What it does |
|--------|----------|--------------|
| GET | `/analytics/filters/customers/list` | Customer list with filters like city, signup range, name search, min orders, top_n |
| GET | `/analytics/filters/customers/spend-summary` | Customer spend metrics (total spend, avg order value, total orders) with spend/date/city filters |
| GET | `/analytics/filters/orders/list` | Orders list with date range, status, customer, city, and top_n filters |
| GET | `/analytics/filters/orders/value-summary` | Per-order totals and item counts with date/status/customer/value-range filters |
| GET | `/analytics/filters/order-items/list` | Raw order-item rows with category/product/order/quantity filters |
| GET | `/analytics/filters/order-items/grouped` | Product-level rollup from order items (units, revenue, order_count) with date/category filters |
| GET | `/analytics/filters/products/list` | Product catalog filtering by category, price range, product id, name, and top_n |
| GET | `/analytics/filters/products/sales-summary` | Product sales summary with category/date/revenue-range filters |

### Common Filter Style

- Date filters: `date_from`, `date_to` (format: `YYYY-MM-DD`)
- Numeric range filters: `min_*`, `max_*`
- Entity filters: `customer_id`, `product_id`, `order_id`, `city`, `category`, `status`
- Result-size filter: `top_n`
