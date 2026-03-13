"""
Load CSV files into MySQL tables for the CSAS project.
This script reads DB credentials from .env and inserts data into the 4 tables.
"""

import os

import pandas as pd
import mysql.connector
from dotenv import load_dotenv


# Load environment variables from .env in the project root.
load_dotenv()


def get_db_config() -> dict:
    """
    Read DB config from environment variables.
    Expected keys: DB_HOST, DB_USER, DB_PASSWORD, DB_NAME, optional DB_PORT.
    """
    return {
        "host": os.getenv("DB_HOST", "localhost"),
        "user": os.getenv("DB_USER", "root"),
        "password": os.getenv("DB_PASSWORD", ""),
        "database": os.getenv("DB_NAME", "csas"),
        "port": int(os.getenv("DB_PORT", "3306")),
    }


def truncate_tables(cursor) -> None:
    """
    Truncate tables in safe order to avoid FK errors.
    """
    cursor.execute("SET FOREIGN_KEY_CHECKS = 0;")
    cursor.execute("TRUNCATE TABLE order_items;")
    cursor.execute("TRUNCATE TABLE orders;")
    cursor.execute("TRUNCATE TABLE products;")
    cursor.execute("TRUNCATE TABLE customers;")
    cursor.execute("SET FOREIGN_KEY_CHECKS = 1;")


def insert_customers(cursor, df: pd.DataFrame) -> None:
    """
    Insert rows into customers table.
    """
    query = """
        INSERT INTO customers (customer_id, name, city, signup_date)
        VALUES (%s, %s, %s, %s)
    """
    rows = df[["customer_id", "name", "city", "signup_date"]].values.tolist()
    cursor.executemany(query, rows)


def insert_orders(cursor, df: pd.DataFrame) -> None:
    """
    Insert rows into orders table.
    """
    query = """
        INSERT INTO orders (order_id, customer_id, order_date, status)
        VALUES (%s, %s, %s, %s)
    """
    rows = df[["order_id", "customer_id", "order_date", "status"]].values.tolist()
    cursor.executemany(query, rows)


def insert_order_items(cursor, df: pd.DataFrame) -> None:
    """
    Insert rows into order_items table.
    """
    query = """
        INSERT INTO order_items (order_item_id, order_id, product_id, quantity)
        VALUES (%s, %s, %s, %s)
    """
    rows = df[["order_item_id", "order_id", "product_id", "quantity"]].values.tolist()
    cursor.executemany(query, rows)


def insert_products(cursor, df: pd.DataFrame) -> None:
    """
    Insert rows into products table.
    """
    query = """
        INSERT INTO products (product_id, product_name, category, price)
        VALUES (%s, %s, %s, %s)
    """
    rows = df[["product_id", "product_name", "category", "price"]].values.tolist()
    cursor.executemany(query, rows)


def main() -> None:
    """
    Read CSVs, truncate tables, insert data, and print row counts.
    """
    config = get_db_config()
    connection = mysql.connector.connect(**config)
    cursor = connection.cursor()

    try:
        truncate_tables(cursor)
        connection.commit()

        # Load CSV files
        customers_df = pd.read_csv("data/customers.csv")
        orders_df = pd.read_csv("data/orders.csv")
        order_items_df = pd.read_csv("data/order_items.csv")
        products_df = pd.read_csv("data/products.csv")

        # Insert data table by table and commit after each one
        insert_customers(cursor, customers_df)
        connection.commit()

        insert_products(cursor, products_df)
        connection.commit()

        insert_orders(cursor, orders_df)
        connection.commit()

        insert_order_items(cursor, order_items_df)
        connection.commit()

        # Validate row counts
        for table in ["customers", "products", "orders", "order_items"]:
            cursor.execute(f"SELECT COUNT(*) FROM {table};")
            count = cursor.fetchone()[0]
            print(f"{table}: {count} rows")
    finally:
        cursor.close()
        connection.close()


if __name__ == "__main__":
    main()
