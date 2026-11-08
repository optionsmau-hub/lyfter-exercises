"""
REST API for a car rental service (users, cars and rentals) using Flask.
Data is persisted in PostgreSQL, under the lyfter_car_rental schema.

Routes only parse the request and shape the response; all SQL lives in
repositories/ (one module per entity).
"""

from datetime import datetime

from flask import Flask, jsonify, request
from werkzeug.security import generate_password_hash

from repositories import cars, rentals, users

app = Flask(__name__)

USER_STATUSES = ["active", "inactive", "suspended", "delinquent"]
CAR_STATUSES = ["available", "rented", "disabled", "maintenance"]
RENTAL_STATUSES = ["active", "completed", "cancelled"]


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def is_valid_date(value):
    try:
        datetime.strptime(value, "%Y-%m-%d")
        return True
    except (TypeError, ValueError):
        return False


def missing_fields(data, required):
    """Returns the required fields that are absent, null, or blank strings."""
    if not isinstance(data, dict):
        return list(required)

    missing = []
    for field in required:
        value = data.get(field)
        if value is None:
            missing.append(field)
        elif isinstance(value, str) and not value.strip():
            missing.append(field)
    return missing


def parse_int(data, field):
    """Returns the field as an int, or None if it's missing/not a valid integer."""
    try:
        return int(data.get(field))
    except (TypeError, ValueError):
        return None


# ---------------------------------------------------------------------------
# Users
# ---------------------------------------------------------------------------

@app.route("/users", methods=["GET"])
def list_users():
    try:
        return jsonify(users.list_users(request.args)), 200
    except ValueError as error:
        return jsonify({"error": str(error)}), 400


@app.route("/users", methods=["POST"])
def create_user():
    data = request.get_json(silent=True)
    errors = missing_fields(data, ["full_name", "email", "username", "password", "birth_date"])

    status = (data or {}).get("status", "active")
    if status not in USER_STATUSES:
        errors.append(f"'status' must be one of: {', '.join(USER_STATUSES)}.")
    if data and data.get("birth_date") and not is_valid_date(data["birth_date"]):
        errors.append("'birth_date' must be in YYYY-MM-DD format.")

    if errors:
        return jsonify({"errors": errors}), 400

    hashed_password = generate_password_hash(data["password"])

    try:
        user = users.create_user(
            data["full_name"], data["email"], data["username"], hashed_password, data["birth_date"], status
        )
    except ValueError as error:
        return jsonify({"error": str(error)}), 409

    return jsonify(user), 201


@app.route("/users/<int:user_id>/status", methods=["PATCH"])
def update_user_status(user_id):
    data = request.get_json(silent=True) or {}
    status = data.get("status")

    if status not in USER_STATUSES:
        return jsonify({"error": f"'status' must be one of: {', '.join(USER_STATUSES)}."}), 400

    user = users.update_status(user_id, status)
    if user is None:
        return jsonify({"error": f"No user found with id '{user_id}'."}), 404

    return jsonify(user), 200


@app.route("/users/<int:user_id>/flag-delinquent", methods=["PATCH"])
def flag_user_delinquent(user_id):
    user = users.flag_delinquent(user_id)
    if user is None:
        return jsonify({"error": f"No user found with id '{user_id}'."}), 404

    return jsonify(user), 200


# ---------------------------------------------------------------------------
# Cars
# ---------------------------------------------------------------------------

@app.route("/cars", methods=["GET"])
def list_cars():
    try:
        return jsonify(cars.list_cars(request.args)), 200
    except ValueError as error:
        return jsonify({"error": str(error)}), 400


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
        car = cars.create_car(data["brand"], data["model"], year, status)
    except ValueError as error:
        return jsonify({"error": str(error)}), 400

    return jsonify(car), 201


@app.route("/cars/<int:car_id>/status", methods=["PATCH"])
def update_car_status(car_id):
    data = request.get_json(silent=True) or {}
    status = data.get("status")

    if status not in CAR_STATUSES:
        return jsonify({"error": f"'status' must be one of: {', '.join(CAR_STATUSES)}."}), 400

    car = cars.update_status(car_id, status)
    if car is None:
        return jsonify({"error": f"No car found with id '{car_id}'."}), 404

    return jsonify(car), 200


@app.route("/cars/<int:car_id>/disable", methods=["PATCH"])
def disable_car(car_id):
    try:
        car = cars.disable(car_id)
    except ValueError as error:
        return jsonify({"error": str(error)}), 409

    if car is None:
        return jsonify({"error": f"No car found with id '{car_id}'."}), 404

    return jsonify(car), 200


# ---------------------------------------------------------------------------
# Rentals
# ---------------------------------------------------------------------------

@app.route("/rentals", methods=["GET"])
def list_rentals():
    try:
        return jsonify(rentals.list_rentals(request.args)), 200
    except ValueError as error:
        return jsonify({"error": str(error)}), 400


@app.route("/rentals", methods=["POST"])
def create_rental_route():
    data = request.get_json(silent=True)
    errors = missing_fields(data, ["user_id", "car_id"])

    user_id = car_id = None
    if not errors:
        user_id = parse_int(data, "user_id")
        car_id = parse_int(data, "car_id")
        if user_id is None:
            errors.append("'user_id' must be an integer.")
        if car_id is None:
            errors.append("'car_id' must be an integer.")

    if errors:
        return jsonify({"errors": errors}), 400

    try:
        rental = rentals.create(user_id, car_id)
    except LookupError as error:
        return jsonify({"error": str(error)}), 404
    except ValueError as error:
        return jsonify({"error": str(error)}), 409

    return jsonify(rental), 201


@app.route("/rentals/<int:rental_id>/complete", methods=["PATCH"])
def complete_rental_route(rental_id):
    try:
        rental = rentals.complete(rental_id)
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
        rental = rentals.change_status(rental_id, status)
    except LookupError as error:
        return jsonify({"error": str(error)}), 404
    except ValueError as error:
        return jsonify({"error": str(error)}), 409

    return jsonify(rental), 200


if __name__ == "__main__":
    app.run(debug=True)
