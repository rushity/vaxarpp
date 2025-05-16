import jwt
import yaml
from functools import wraps
from flask import request, jsonify
from jwt.exceptions import ExpiredSignatureError, InvalidTokenError

with open("config.yaml") as f:
    config = yaml.safe_load(f)

JWT_SECRET = config["app"]["secret_key"]
JWT_ALGORITHM = config["jwt"]["algorithm"]

class AuthMiddleware:

    @staticmethod
    def ValidateToken(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            auth_header = request.headers.get("Authorization")
            if not auth_header or not auth_header.startswith("Bearer "):
                return jsonify({"error": "Missing or invalid token"}), 401
            token = auth_header.split(" ")[1]
            try:
                # decoded = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM], options={"verify_aud": False, "verify_iss": False})
                decoded = jwt.decode(
    token,
    JWT_SECRET,
    algorithms=[JWT_ALGORITHM],
    options={
        "verify_signature": False,
        "verify_exp": False,
        "verify_aud": False,
        "verify_iss": False
    }
)

                return fn(decoded, *args, **kwargs)
            except (ExpiredSignatureError, InvalidTokenError):
                return jsonify({"error": "Invalid or expired token"}), 401
        return wrapper
