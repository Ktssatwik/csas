
"""
Low-level database helpers for running SQL queries.
These functions open a connection, execute SQL, and return results.
"""

from typing import Any, Iterable, Optional

from .database import get_connection


def fetch_all(query: str, params: Optional[Iterable[Any]] = None):
    """
    Run a SELECT query and return all rows as a list of dicts.
    """
    # Create a connection and dictionary cursor (rows as dicts).
    connection = get_connection()
    cursor = connection.cursor(dictionary=True)
    try:
        cursor.execute(query, params or ())
        return cursor.fetchall()
    finally:
        cursor.close()
        connection.close()


def fetch_one(query: str, params: Optional[Iterable[Any]] = None):
    """
    Run a SELECT query and return a single row as a dict (or None).
    """
    connection = get_connection()
    cursor = connection.cursor(dictionary=True)
    try:
        cursor.execute(query, params or ())
        return cursor.fetchone()
    finally:
        cursor.close()
        connection.close()


# def execute(query: str, params: Optional[Iterable[Any]] = None) -> int:
#     """
#     Run an INSERT/UPDATE/DELETE query and return affected row count.
#     """
#     connection = get_connection()
#     cursor = connection.cursor()
#     try:
#         cursor.execute(query, params or ())
#         connection.commit()
#         return cursor.rowcount
#     finally:
#         cursor.close()
#         connection.close()
