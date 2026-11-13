from functools import wraps

from flask import request, jsonify, g

from jwt_manager import jwt_manager
from user_repository import user_repository


def jwt_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        token = request.headers.get("Authorization")
        if token is None:
            return jsonify(error="Missing Authorization header"), 401

        token = token.replace("Bearer ", "")
        decoded = jwt_manager.decode_token(token, "access")
        if decoded is None:
            return jsonify(error="Invalid or expired access token"), 401

        user = user_repository.get_by_id(decoded["id"])
        if user is None:
            return jsonify(error="User not found"), 404

        g.current_user = user
        return f(*args, **kwargs)

    return wrapper


def roles_required(*allowed_roles):
    def decorator(view_func):
        @jwt_required
        @wraps(view_func)
        def wrapper(*args, **kwargs):
            if g.current_user.role not in allowed_roles:
                return jsonify(error="You don't have permission to access this resource"), 403
            return view_func(*args, **kwargs)

        return wrapper

    return decorator
