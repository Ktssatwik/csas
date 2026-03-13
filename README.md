# CSAS — Customer Sales Analytics System

A retail analytics platform built with **FastAPI + MySQL + Streamlit**.

---

## Project Structure

```
csas/
├── data/                        # Raw CSV files
│   ├── customers.csv
│   ├── orders.csv
│   ├── order_items.csv
│   └── products.csv
│
├── backend/                     # FastAPI application
│   ├── main.py                  # App entry point + CORS
│   ├── config.py                # DB config via .env
│   ├── database.py              # SQLAlchemy engine + session
│   ├── models.py                # ORM table definitions
│   ├── schemas.py               # Pydantic response models
│   ├── crud.py                  # Basic list queries
│   ├── analytics.py             # Analytics logic
│   ├── utils.py                 # Helpers (future use)
│   └── routes/
│       ├── customers.py         # GET /customers/
│       ├── orders.py            # GET /orders/
│       ├── products.py          # GET /products/
│       └── analytics.py        # GET /analytics/*
│
├── frontend/                    # Streamlit dashboard
│   ├── app.py                   # Home page + quick stats
│   └── pages/
│       ├── sales_dashboard.py   # Revenue trends & geo breakdown
│       ├── customer_analysis.py # Top spenders & repeat buyers
│       └── product_analysis.py  # Best sellers & categories
│
├── database/
│   ├── schema.sql               # CREATE TABLE statements
│   └── load_data.py             # CSV → MySQL loader
│
├── docs/
│   └── sql_queries.md           # SQL query documentation
│
├── requirements.txt
└── README.md
```

---

## Setup

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
uvicorn backend.main:app --reload
```
API docs available at: http://localhost:8000/docs

### 5. Start the Streamlit frontend
```bash
streamlit run frontend/app.py
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
