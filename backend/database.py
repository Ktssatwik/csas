
"""
Database connection utilities for the CSAS FastAPI backend.
Uses shared DB config from db_config.py.
"""

import mysql.connector

from .db_config import get_db_config

def get_connection():
    """
    Open and return a new MySQL connection.
    """
    # A new connection is created each time this function is called.
    return mysql.connector.connect(**get_db_config())
