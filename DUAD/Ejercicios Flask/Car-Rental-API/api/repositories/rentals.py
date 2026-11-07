"""
Data access layer for the rentals table.

A rental isn't just its own row: its status has to stay in sync with the
car it points to (a car can't be 'available' while an 'active' rental
still has it out, and vice versa). That sync lives here, next to the SQL
that touches both tables, so every route that changes a rental's status
goes through the same rules.
"""

import psycopg2.extras

from db import _serialize_row, build_where, fetch_all, get_connection

FILTER_COLUMNS = {"id", "user_id", "car_id", "rental_date", "return_date", "status"}
COLUMN_TYPES = {"id": "int", "user_id": "int", "car_id": "int", "rental_date": "datetime", "return_date": "datetime"}

PUBLIC_COLUMNS = "id, user_id, car_id, rental_date, return_date, status"


def list_rentals(filters):
    where_sql, params = build_where(filters, FILTER_COLUMNS, COLUMN_TYPES)
    return fetch_all(f"SELECT {PUBLIC_COLUMNS} FROM rentals{where_sql} ORDER BY id", params)


def create(user_id, car_id):
    with get_connection() as conn:
        with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
            cur.execute("SELECT 1 FROM users WHERE id = %s", (user_id,))
            if cur.fetchone() is None:
                raise LookupError(f"User {user_id} does not exist.")

            cur.execute("SELECT status FROM cars WHERE id = %s", (car_id,))
            car = cur.fetchone()
            if car is None:
                raise LookupError(f"Car {car_id} does not exist.")
            if car["status"] != "available":
                raise ValueError(f"Car {car_id} is not available (current status: {car['status']}).")

            cur.execute(
                f"""
                INSERT INTO rentals (user_id, car_id, status)
                VALUES (%s, %s, 'active')
                RETURNING {PUBLIC_COLUMNS}
                """,
                (user_id, car_id),
            )
            rental = _serialize_row(cur.fetchone())
            cur.execute("UPDATE cars SET status = 'rented' WHERE id = %s", (car_id,))
            return rental


def change_status(rental_id, new_status, require_status=None):
    """
    Updates a rental's status and keeps the related car in sync:
      - moving INTO 'active' requires the car to be available, then marks
        it 'rented' (this covers reactivating a cancelled rental, which
        previously left the car 'available' for anyone else to take).
      - moving OUT of 'active' frees the car back to 'available', but only
        if the car is still 'rented' -- if it was disabled or sent to
        maintenance while the rental was active, returning the car must
        not silently undo that.
      - reaching 'completed' stamps return_date; leaving 'active' clears it.

    require_status, when given, rejects the change unless the rental is
    currently in that status (used by complete(), which only makes sense
    for an active rental).
    """
    with get_connection() as conn:
        with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
            cur.execute("SELECT car_id, status FROM rentals WHERE id = %s", (rental_id,))
            rental = cur.fetchone()
            if rental is None:
                raise LookupError(f"Rental {rental_id} does not exist.")

            car_id = rental["car_id"]
            old_status = rental["status"]

            if require_status is not None and old_status != require_status:
                raise ValueError(
                    f"Rental {rental_id} is not {require_status} (current status: {old_status})."
                )

            if new_status == "active" and old_status != "active":
                cur.execute("SELECT status FROM cars WHERE id = %s", (car_id,))
                car = cur.fetchone()
                if car["status"] != "available":
                    raise ValueError(f"Car {car_id} is not available (current status: {car['status']}).")
                cur.execute("UPDATE cars SET status = 'rented' WHERE id = %s", (car_id,))

            if new_status != "active" and old_status == "active":
                cur.execute(
                    "UPDATE cars SET status = 'available' WHERE id = %s AND status = 'rented'",
                    (car_id,),
                )

            if new_status == "completed":
                cur.execute(
                    f"""
                    UPDATE rentals SET status = %s, return_date = NOW()
                    WHERE id = %s RETURNING {PUBLIC_COLUMNS}
                    """,
                    (new_status, rental_id),
                )
            elif new_status == "active":
                cur.execute(
                    f"""
                    UPDATE rentals SET status = %s, return_date = NULL
                    WHERE id = %s RETURNING {PUBLIC_COLUMNS}
                    """,
                    (new_status, rental_id),
                )
            else:
                cur.execute(
                    f"""
                    UPDATE rentals SET status = %s
                    WHERE id = %s RETURNING {PUBLIC_COLUMNS}
                    """,
                    (new_status, rental_id),
                )

            return _serialize_row(cur.fetchone())


def complete(rental_id):
    return change_status(rental_id, "completed", require_status="active")
