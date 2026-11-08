"""Data access layer for the cars table. Routes never touch SQL directly."""

import psycopg2.errors

from db import build_where, fetch_all, fetch_one

FILTER_COLUMNS = {"id", "brand", "model", "year", "status"}
COLUMN_TYPES = {"id": "int", "year": "int"}

PUBLIC_COLUMNS = "id, brand, model, year, status"


def list_cars(filters):
    where_sql, params = build_where(filters, FILTER_COLUMNS, COLUMN_TYPES)
    return fetch_all(f"SELECT {PUBLIC_COLUMNS} FROM cars{where_sql} ORDER BY id", params)


def create_car(brand, model, year, status):
    try:
        return fetch_one(
            f"""
            INSERT INTO cars (brand, model, year, status)
            VALUES (%s, %s, %s, %s)
            RETURNING {PUBLIC_COLUMNS}
            """,
            (brand, model, year, status),
        )
    except psycopg2.errors.CheckViolation:
        raise ValueError("'year' is outside the allowed range.")


def update_status(car_id, status):
    return fetch_one(
        f"UPDATE cars SET status = %s WHERE id = %s RETURNING {PUBLIC_COLUMNS}",
        (status, car_id),
    )


def disable(car_id):
    """
    Disables a car, unless it's currently rented -- a car with an active
    rental has to be returned (or the rental cancelled) first, otherwise
    the renter would be left with a car the system thinks doesn't exist.
    """
    car = fetch_one(f"SELECT {PUBLIC_COLUMNS} FROM cars WHERE id = %s", (car_id,))
    if car is None:
        return None
    if car["status"] == "rented":
        raise ValueError(f"Car {car_id} is currently rented and cannot be disabled.")

    return fetch_one(
        f"UPDATE cars SET status = 'disabled' WHERE id = %s RETURNING {PUBLIC_COLUMNS}",
        (car_id,),
    )
