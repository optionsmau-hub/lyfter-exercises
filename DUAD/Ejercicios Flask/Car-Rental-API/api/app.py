"""
REST API for a car rental service (users, cars and rentals) using Flask.
Data is persisted in PostgreSQL, under the lyfter_car_rental schema.
"""

from datetime import datetime

import psycopg2
import psycopg2.errors
import psycopg2.extras
from flask import Flask, jsonify, request
from werkzeug.security import generate_password_hash

from db import _serialize_row, fetch_all, fetch_one, get_connection

app = Flask(__name__)

USER_STATUSES = ["active", "inactive", "suspended", "delinquent"]
CAR_STATUSES = ["available", "rented", "disabled", "maintenance"]
RENTAL_STATUSES = ["active", "completed", "cancelled"]

# Columns each listing endpoint is allowed to filter by. Keeping an
# allow-list (instead of trusting whatever query param name arrives)
# is what makes "filter by any column" safe to build with string
# formatting: only known, fixed column names ever reach the query.
USER_FILTER_COLUMNS = {"id", "full_name", "email", "username", "birth_date", "status"}
CAR_FILTER_COLUMNS = {"id", "brand", "model", "year", "status"}
RENTAL_FILTER_COLUMNS = {"id", "user_id", "car_id", "rental_date", "return_date", "status"}

# password is intentionally left out of every SELECT.
USER_PUBLIC_COLUMNS = "id, full_name, email, username, birth_date, status"
CAR_PUBLIC_COLUMNS = "id, brand, model, year, status"
RENTAL_PUBLIC_COLUMNS = "id, user_id, car_id, rental_date, return_date, status"


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def build_filters(args, allowed_columns):
    """
    Builds a parameterized WHERE clause from query-string filters.
    Raises ValueError if a filter name isn't an allowed column.
    """
    clauses = []
    params = []
    for key, value in args.items():
        if key not in allowed_columns:
            raise ValueError(f"'{key}' is not a filterable column.")
        clauses.append(f"{key} = %s")
        params.append(value)
    where_sql = f" WHERE {' AND '.join(clauses)}" if clauses else ""
    return where_sql, params


def is_valid_date(value):
    try:
        datetime.strptime(value, "%Y-%m-%d")
        return True
    except (TypeError, ValueError):
        return False


def missing_fields(data, required):
    if not isinstance(data, dict):
        return list(required)
    return [field for field in required if not str(data.get(field, "")).strip()]


# ---------------------------------------------------------------------------
# Transactional operations (span more than one statement/table)
# ---------------------------------------------------------------------------

def create_rental(user_id, car_id):
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
                RETURNING {RENTAL_PUBLIC_COLUMNS}
                """,
                (user_id, car_id),
            )
            rental = _serialize_row(cur.fetchone())
            cur.execute("UPDATE cars SET status = 'rented' WHERE id = %s", (car_id,))
            return rental


def complete_rental(rental_id):
    with get_connection() as conn:
        with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
            cur.execute("SELECT car_id, status FROM rentals WHERE id = %s", (rental_id,))
            rental = cur.fetchone()
            if rental is None:
                raise LookupError(f"Rental {rental_id} does not exist.")
            if rental["status"] != "active":
                raise ValueError(f"Rental {rental_id} is not active (current status: {rental['status']}).")

            cur.execute(
                f"""
                UPDATE rentals
                SET status = 'completed', return_date = NOW()
                WHERE id = %s
                RETURNING {RENTAL_PUBLIC_COLUMNS}
                """,
                (rental_id,),
            )
            updated_rental = _serialize_row(cur.fetchone())
            cur.execute("UPDATE cars SET status = 'available' WHERE id = %s", (rental["car_id"],))
            return updated_rental


def update_rental_status(rental_id, new_status):
    with get_connection() as conn:
        with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
            cur.execute("SELECT car_id, status FROM rentals WHERE id = %s", (rental_id,))
            rental = cur.fetchone()
            if rental is None:
                raise LookupError(f"Rental {rental_id} does not exist.")

            cur.execute(
                f"""
                UPDATE rentals
                SET status = %s
                WHERE id = %s
                RETURNING {RENTAL_PUBLIC_COLUMNS}
                """,
                (new_status, rental_id),
            )
            updated_rental = _serialize_row(cur.fetchone())

            # Cancelling an active rental frees up the car again.
            if new_status == "cancelled" and rental["status"] == "active":
                cur.execute("UPDATE cars SET status = 'available' WHERE id = %s", (rental["car_id"],))

            return updated_rental


# ---------------------------------------------------------------------------
# Users
# ---------------------------------------------------------------------------

@app.route("/users", methods=["GET"])
def list_users():
    try:
        where_sql, params = build_filters(request.args, USER_FILTER_COLUMNS)
    except ValueError as error:
        return jsonify({"error": str(error)}), 400

    users = fetch_all(f"SELECT {USER_PUBLIC_COLUMNS} FROM users{where_sql} ORDER BY id", params)
    return jsonify(users), 200


@app.route("/users", methods=["POST"])
def create_user():
    data = request.get_json(silent=True)
    errors = missing_fields(data, ["full_name", "email", "username", "password", "birth_date"])

    status = (data or {}).get("status", "active")
    if status not in USER_STATUSES:
        errors.append(f"'status' must be one of: {', '.join(USER_STATUSES)}.")
    if data and "birth_date" in data and data["birth_date"] and not is_valid_date(data["birth_date"]):
        errors.append("'birth_date' must be in YYYY-MM-DD format.")

    if errors:
        return jsonify({"errors": errors}), 400

    hashed_password = generate_password_hash(data["password"])

    try:
        user = fetch_one(
            f"""
            INSERT INTO users (full_name, email, username, password, birth_date, status)
            VALUES (%s, %s, %s, %s, %s, %s)
            RETURNING {USER_PUBLIC_COLUMNS}
            """,
            (data["full_name"], data["email"], data["username"], hashed_password, data["birth_date"], status),
        )
    except psycopg2.errors.UniqueViolation:
        return jsonify({"error": "A user with that email or username already exists."}), 409

    return jsonify(user), 201


@app.route("/users/<int:user_id>/status", methods=["PATCH"])
def update_user_status(user_id):
    data = request.get_json(silent=True) or {}
    status = data.get("status")

    if status not in USER_STATUSES:
        return jsonify({"error": f"'status' must be one of: {', '.join(USER_STATUSES)}."}), 400

    user = fetch_one(
        f"UPDATE users SET status = %s WHERE id = %s RETURNING {USER_PUBLIC_COLUMNS}",
        (status, user_id),
    )
    if user is None:
        return jsonify({"error": f"No user found with id '{user_id}'."}), 404

    return jsonify(user), 200


@app.route("/users/<int:user_id>/flag-delinquent", methods=["PATCH"])
def flag_user_delinquent(user_id):
    user = fetch_one(
        f"UPDATE users SET status = 'delinquent' WHERE id = %s RETURNING {USER_PUBLIC_COLUMNS}",
        (user_id,),
    )
    if user is None:
        return jsonify({"error": f"No user found with id '{user_id}'."}), 404

    return jsonify(user), 200


# ---------------------------------------------------------------------------
# Cars
# ---------------------------------------------------------------------------

@app.route("/cars", methods=["GET"])
def list_cars():
    try:
        where_sql, params = build_filters(request.args, CAR_FILTER_COLUMNS)
    except ValueError as error:
        return jsonify({"error": str(error)}), 400

    cars = fetch_all(f"SELECT {CAR_PUBLIC_COLUMNS} FROM cars{where_sql} ORDER BY id", params)
    return jsonify(cars), 200


@app.route("/cars", methods=["POST"])
def create_car():
    data = request.get_json(silent=True)
    errors = missing_fields(data, ["brand", "model", "year"])

    status = (data or {}).get("status", "available")
    if status not in CAR_STATUSES:
        errors.append(f"'status' must be one of: {', '.join(CAR_STATUSES)}.")

    year = (data or {}).get("year")
    if year is not None and not isinstance(year, int):
        errors.append("'year' must be an integer.")

    if errors:
        return jsonify({"errors": errors}), 400

    try:
        car = fetch_one(
            f"""
            INSERT INTO cars (brand, model, year, status)
            VALUES (%s, %s, %s, %s)
            RETURNING {CAR_PUBLIC_COLUMNS}
            """,
            (data["brand"], data["model"], year, status),
        )
    except psycopg2.errors.CheckViolation:
        return jsonify({"error": "'year' is outside the allowed range."}), 400

    return jsonify(car), 201


@app.route("/cars/<int:car_id>/status", methods=["PATCH"])
def update_car_status(car_id):
    data = request.get_json(silent=True) or {}
    status = data.get("status")

    if status not in CAR_STATUSES:
        return jsonify({"error": f"'status' must be one of: {', '.join(CAR_STATUSES)}."}), 400

    car = fetch_one(
        f"UPDATE cars SET status = %s WHERE id = %s RETURNING {CAR_PUBLIC_COLUMNS}",
        (status, car_id),
    )
    if car is None:
        return jsonify({"error": f"No car found with id '{car_id}'."}), 404

    return jsonify(car), 200


@app.route("/cars/<int:car_id>/disable", methods=["PATCH"])
def disable_car(car_id):
    car = fetch_one(
        f"UPDATE cars SET status = 'disabled' WHERE id = %s RETURNING {CAR_PUBLIC_COLUMNS}",
        (car_id,),
    )
    if car is None:
        return jsonify({"error": f"No car found with id '{car_id}'."}), 404

    return jsonify(car), 200


# ---------------------------------------------------------------------------
# Rentals
# ---------------------------------------------------------------------------

@app.route("/rentals", methods=["GET"])
def list_rentals():
    try:
        where_sql, params = build_filters(request.args, RENTAL_FILTER_COLUMNS)
    except ValueError as error:
        return jsonify({"error": str(error)}), 400

    rentals = fetch_all(f"SELECT {RENTAL_PUBLIC_COLUMNS} FROM rentals{where_sql} ORDER BY id", params)
    return jsonify(rentals), 200


@app.route("/rentals", methods=["POST"])
def create_rental_route():
    data = request.get_json(silent=True)
    errors = missing_fields(data, ["user_id", "car_id"])
    if errors:
        return jsonify({"errors": errors}), 400

    try:
        rental = create_rental(data["user_id"], data["car_id"])
    except LookupError as error:
        return jsonify({"error": str(error)}), 404
    except ValueError as error:
        return jsonify({"error": str(error)}), 409

    return jsonify(rental), 201


@app.route("/rentals/<int:rental_id>/complete", methods=["PATCH"])
def complete_rental_route(rental_id):
    try:
        rental = complete_rental(rental_id)
    except LookupError as error:
        return jsonify({"error": str(error)}), 404
    except ValueError as error:
        return jsonify({"error": str(error)}), 409

    return jsonify(rental), 200


@app.route("/rentals/<int:rental_id>/status", methods=["PATCH"])
def update_rental_status_route(rental_id):
    data = request.get_json(silent=True) or {}
    status = data.get("status")

    if status not in RENTAL_STATUSES:
        return jsonify({"error": f"'status' must be one of: {', '.join(RENTAL_STATUSES)}."}), 400

    try:
        rental = update_rental_status(rental_id, status)
    except LookupError as error:
        return jsonify({"error": str(error)}), 404

    return jsonify(rental), 200


if __name__ == "__main__":
    app.run(debug=True)
