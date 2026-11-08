"""Data access layer for the users table. Routes never touch SQL directly."""

import psycopg2.errors

from db import build_where, fetch_all, fetch_one

FILTER_COLUMNS = {"id", "full_name", "email", "username", "birth_date", "status"}
COLUMN_TYPES = {"id": "int", "birth_date": "date"}

# password is intentionally left out of every SELECT.
PUBLIC_COLUMNS = "id, full_name, email, username, birth_date, status"


def list_users(filters):
    where_sql, params = build_where(filters, FILTER_COLUMNS, COLUMN_TYPES)
    return fetch_all(f"SELECT {PUBLIC_COLUMNS} FROM users{where_sql} ORDER BY id", params)


def create_user(full_name, email, username, hashed_password, birth_date, status):
    try:
        return fetch_one(
            f"""
            INSERT INTO users (full_name, email, username, password, birth_date, status)
            VALUES (%s, %s, %s, %s, %s, %s)
            RETURNING {PUBLIC_COLUMNS}
            """,
            (full_name, email, username, hashed_password, birth_date, status),
        )
    except psycopg2.errors.UniqueViolation:
        raise ValueError("A user with that email or username already exists.")


def update_status(user_id, status):
    return fetch_one(
        f"UPDATE users SET status = %s WHERE id = %s RETURNING {PUBLIC_COLUMNS}",
        (status, user_id),
    )


def flag_delinquent(user_id):
    return fetch_one(
        f"UPDATE users SET status = 'delinquent' WHERE id = %s RETURNING {PUBLIC_COLUMNS}",
        (user_id,),
    )
