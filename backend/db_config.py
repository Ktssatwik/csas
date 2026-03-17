"""
Shared DB configuration loader for the CSAS project.
Reads DB credentials from .env.
"""

import os

from dotenv import load_dotenv


# Load environment variables from .env in the project root.
load_dotenv()


def get_db_config() -> dict:
    """
    Build DB config from environment variables.
    Expected keys: DB_HOST, DB_USER, DB_PASSWORD, DB_NAME, optional DB_PORT.
    """
    return {
        "host": os.getenv("DB_HOST", "localhost"),
        "user": os.getenv("DB_USER", "root"),
        "password": os.getenv("DB_PASSWORD", "Bablu@1103"),
        "database": os.getenv("DB_NAME", "csas"),
        "port": int(os.getenv("DB_PORT", "3306")),
    }
