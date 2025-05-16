from flask.views import MethodView
from flask import request, jsonify
import jwt, datetime, yaml
from jwt.exceptions import ExpiredSignatureError, InvalidTokenError
from src.constants import infoConstant as constant
from src.utils.loggerUtils import CustomJSONFormatter as logger

with open("config.yaml") as f:
    config = yaml.safe_load(f)

JWT_SECRET = config["app"]["secret_key"]
JWT_ALGORITHM = config["jwt"]["algorithm"]

class AuthController(MethodView):

    def signIn(self):
        try:
            data = request.get_json()
            username = data.get("username")
            password = data.get("password")

            if username == "admin" and password == "password":
                payload = {
                    "username": username,
                    "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=config["app"]["token_expiry_hours"])
                }
                token = jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)
                return jsonify({"token": token})

            return jsonify({"error": "Invalid credentials"}), 401
        except Exception as e:
            logger.CreateLog("ERROR", "LOGIN_FAILED", 500, 123, str(e))
            return jsonify({"error": "Server error"}), 500