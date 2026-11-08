"""
Database connection helper for the car rental API.

Reads connection settings from environment variables (see .env.example)
and exposes a context manager that commits on success and rolls back
on any error, so every route only has to worry about its own query.
"""

import os
from contextlib import contextmanager
from datetime import date, datetime

import psycopg2
import psycopg2.extras
from dotenv import load_dotenv

load_dotenv()

DB_CONFIG = {
    "host": os.environ.get("DB_HOST", "localhost"),
    "port": os.environ.get("DB_PORT", "5432"),
    "dbname": os.environ.get("DB_NAME", "postgres"),
    "user": os.environ.get("DB_USER", "postgres"),
    "password": os.environ.get("DB_PASSWORD", ""),
    # Every table lives in this schema, so queries don't need to qualify it.
    "options": "-c search_path=lyfter_car_rental",
}


@contextmanager
def get_connection():
    conn = psycopg2.connect(**DB_CONFIG)
    try:
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()


def _serialize_row(row):
    """Converts date/datetime values to ISO 8601 strings for clean JSON output."""
    return {
        key: value.isoformat() if isinstance(value, (date, datetime)) else value
        for key, value in row.items()
    }


def _is_valid_date(value):
    try:
        datetime.strptime(value, "%Y-%m-%d")
        return True
    except (TypeError, ValueError):
        return False


def _is_valid_datetime(value):
    if _is_valid_date(value):
        return True
    try:
        datetime.fromisoformat(value)
        return True
    except (TypeError, ValueError):
        return False


def _coerce_filter_value(column, value, column_type):
    """Validates/converts a raw query-string value against a column's type."""
    if column_type == "int":
        try:
            return int(value)
        except (TypeError, ValueError):
            raise ValueError(f"'{column}' must be an integer.")
    if column_type == "date":
        if not _is_valid_date(value):
            raise ValueError(f"'{column}' must be a date in YYYY-MM-DD format.")
        return value
    if column_type == "datetime":
        if not _is_valid_datetime(value):
            raise ValueError(f"'{column}' must be a date (YYYY-MM-DD) or an ISO 8601 timestamp.")
        return value
    return value


def build_where(args, allowed_columns, column_types=None):
    """
    Builds a parameterized WHERE clause from query-string filters.
    Raises ValueError if a filter name isn't an allowed column, or if its
    value doesn't match the column's expected type (column_types maps a
    column name to "int", "date", "datetime", defaulting to plain text).
    """
    column_types = column_types or {}
    clauses = []
    params = []
    for key, value in args.items():
        if key not in allowed_columns:
            raise ValueError(f"'{key}' is not a filterable column.")
        clauses.append(f"{key} = %s")
        params.append(_coerce_filter_value(key, value, column_types.get(key, "text")))
    where_sql = f" WHERE {' AND '.join(clauses)}" if clauses else ""
    return where_sql, params


def fetch_all(query, params=None):
    with get_connection() as conn:
        with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
            cur.execute(query, params or [])
            return [_serialize_row(row) for row in cur.fetchall()]


def fetch_one(query, params=None):
    with get_connection() as conn:
        with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
            cur.execute(query, params or [])
            row = cur.fetchone()
            return _serialize_row(row) if row else None
