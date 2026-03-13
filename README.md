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
