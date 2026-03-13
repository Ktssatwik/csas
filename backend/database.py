
"""
Database connection utilities for the CSAS FastAPI backend.
Reads DB credentials from .env and returns a MySQL connection.
"""

import os

import mysql.connector
from dotenv import load_dotenv

# Load environment variables from .env in the project root.
load_dotenv()


def get_db_config() -> dict:

    # Build DB config from environment variables.

    return {
        "host": os.getenv("DB_HOST", "localhost"),
        "user": os.getenv("DB_USER", "root"),
        "password": os.getenv("DB_PASSWORD", ""),
        "database": os.getenv("DB_NAME", "csas"),
        "port": int(os.getenv("DB_PORT", "3306")),
    }


def get_connection():
    """
    Open and return a new MySQL connection.
    """
    # A new connection is created each time this function is called.
    return mysql.connector.connect(**get_db_config())
