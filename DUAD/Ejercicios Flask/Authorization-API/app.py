import os
from datetime import date

from flask import Flask, request, jsonify, g

from user_repository import user_repository
from product_repository import product_repository
from invoice_repository import invoice_repository
from jwt_manager import jwt_manager
from auth_decorators import jwt_required, roles_required

app = Flask("fruit-store-service")


def serialize_product(product):
    return {
        "id": product.id,
        "name": product.name,
        "price": product.price,
        "entry_date": product.entry_date.isoformat(),
        "quantity": product.quantity,
    }


def serialize_invoice(invoice):
    return {
        "id": invoice.id,
        "product_id": invoice.product_id,
        "quantity": invoice.quantity,
        "unit_price": invoice.unit_price,
        "total": invoice.total,
        "created_at": invoice.created_at.isoformat(),
    }


@app.route("/liveness")
def liveness():
    return jsonify(message="Service is running")


# ---------------------------------------------------------------------------
# Auth endpoints
# ---------------------------------------------------------------------------

@app.route("/register", methods=["POST"])
def register():
    data = request.get_json(silent=True)
    if data is None:
        return jsonify(error="Request body must be valid JSON"), 400

    username = data.get("username")
    password = data.get("password")

    if username is None or password is None:
        return jsonify(error="Username and password are required"), 400

    if user_repository.get_by_username(username) is not None:
        return jsonify(error="Username is already taken"), 400

    # Public registration always creates a regular user; admins are seeded separately
    new_user = user_repository.create(username, password, role="user")
    access_token, refresh_token = jwt_manager.generate_tokens(new_user.id)
    return jsonify(access_token=access_token, refresh_token=refresh_token), 201


@app.route("/login", methods=["POST"])
def login():
    data = request.get_json(silent=True)
    if data is None:
        return jsonify(error="Request body must be valid JSON"), 400

    username = data.get("username")
    password = data.get("password")

    if username is None or password is None:
        return jsonify(error="Username and password are required"), 400

    user = user_repository.get_by_credentials(username, password)
    if user is None:
        return jsonify(error="Invalid username or password"), 401

    access_token, refresh_token = jwt_manager.generate_tokens(user.id)
    return jsonify(access_token=access_token, refresh_token=refresh_token)


@app.route("/me")
@jwt_required
def me():
    user = g.current_user
    return jsonify(id=user.id, username=user.username, role=user.role)


@app.route("/refresh", methods=["POST"])
def refresh():
    data = request.get_json(silent=True)
    if data is None:
        return jsonify(error="Request body must be valid JSON"), 400

    refresh_token = data.get("refresh_token")
    if refresh_token is None:
        return jsonify(error="Refresh token is required"), 400

    decoded = jwt_manager.decode_token(refresh_token, "refresh")
    if decoded is None:
        return jsonify(error="Invalid or expired refresh token"), 401

    user = user_repository.get_by_id(decoded["id"])
    if user is None:
        return jsonify(error="User not found"), 404

    access_token, new_refresh_token = jwt_manager.generate_tokens(user.id)
    return jsonify(access_token=access_token, refresh_token=new_refresh_token)


# ---------------------------------------------------------------------------
# Product endpoints (admin only)
# ---------------------------------------------------------------------------

@app.route("/products", methods=["POST"])
@roles_required("admin")
def create_product():
    data = request.get_json(silent=True)
    if data is None:
        return jsonify(error="Request body must be valid JSON"), 400

    name = data.get("name")
    price = data.get("price")
    entry_date = data.get("entry_date")
    quantity = data.get("quantity")

    if name is None or price is None or entry_date is None or quantity is None:
        return jsonify(error="name, price, entry_date and quantity are required"), 400

    try:
        price = float(price)
        quantity = int(quantity)
        parsed_entry_date = date.fromisoformat(entry_date)
    except (TypeError, ValueError):
        return jsonify(error="Invalid price, quantity or entry_date (expected YYYY-MM-DD)"), 400

    if price < 0 or quantity < 0:
        return jsonify(error="price and quantity must not be negative"), 400

    new_product = product_repository.create(name, price, parsed_entry_date, quantity)
    return jsonify(serialize_product(new_product)), 201


@app.route("/products", methods=["GET"])
@roles_required("admin")
def get_products():
    products = product_repository.get_all()
    return jsonify([serialize_product(product) for product in products])


@app.route("/products/<int:product_id>", methods=["GET"])
@roles_required("admin")
def get_product(product_id):
    product = product_repository.get_by_id(product_id)
    if product is None:
        return jsonify(error="Product not found"), 404

    return jsonify(serialize_product(product))


@app.route("/products/<int:product_id>", methods=["PUT"])
@roles_required("admin")
def update_product(product_id):
    product = product_repository.get_by_id(product_id)
    if product is None:
        return jsonify(error="Product not found"), 404

    data = request.get_json(silent=True)
    if data is None:
        return jsonify(error="Request body must be valid JSON"), 400

    fields = {}

    if "name" in data:
        fields["name"] = data["name"]

    if "price" in data:
        try:
            fields["price"] = float(data["price"])
        except (TypeError, ValueError):
            return jsonify(error="Invalid price"), 400
        if fields["price"] < 0:
            return jsonify(error="price must not be negative"), 400

    if "entry_date" in data:
        try:
            fields["entry_date"] = date.fromisoformat(data["entry_date"])
        except (TypeError, ValueError):
            return jsonify(error="Invalid entry_date (expected YYYY-MM-DD)"), 400

    if "quantity" in data:
        try:
            fields["quantity"] = int(data["quantity"])
        except (TypeError, ValueError):
            return jsonify(error="Invalid quantity"), 400
        if fields["quantity"] < 0:
            return jsonify(error="quantity must not be negative"), 400

    if not fields:
        return jsonify(error="No valid fields to update"), 400

    updated_product = product_repository.update(product_id, **fields)
    return jsonify(serialize_product(updated_product))


@app.route("/products/<int:product_id>", methods=["DELETE"])
@roles_required("admin")
def delete_product(product_id):
    product = product_repository.get_by_id(product_id)
    if product is None:
        return jsonify(error="Product not found"), 404

    product_repository.delete(product_id)
    return "", 204


# ---------------------------------------------------------------------------
# Purchases and invoices (any authenticated user)
# ---------------------------------------------------------------------------

@app.route("/products/<int:product_id>/purchase", methods=["POST"])
@jwt_required
def purchase_product(product_id):
    product = product_repository.get_by_id(product_id)
    if product is None:
        return jsonify(error="Product not found"), 404

    data = request.get_json(silent=True) or {}
    quantity = data.get("quantity", 1)

    try:
        quantity = int(quantity)
    except (TypeError, ValueError):
        return jsonify(error="Invalid quantity"), 400

    if quantity <= 0:
        return jsonify(error="Quantity must be greater than zero"), 400

    if product.quantity < quantity:
        return jsonify(error="Not enough stock available"), 400

    total = product.price * quantity
    product_repository.decrease_stock(product_id, quantity)
    new_invoice = invoice_repository.create(
        user_id=g.current_user.id,
        product_id=product.id,
        quantity=quantity,
        unit_price=product.price,
        total=total,
    )
    return jsonify(serialize_invoice(new_invoice)), 201


@app.route("/invoices", methods=["GET"])
@jwt_required
def get_invoices():
    # Always scoped to the authenticated user; never filterable by an external id
    invoices = invoice_repository.get_by_user_id(g.current_user.id)
    return jsonify([serialize_invoice(invoice) for invoice in invoices])


if __name__ == "__main__":
    app.run(debug=os.environ.get("FLASK_DEBUG") == "1")
