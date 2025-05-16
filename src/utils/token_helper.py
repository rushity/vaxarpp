import jwt
from jwt.exceptions import ExpiredSignatureError, InvalidTokenError
import yaml

with open("config.yaml") as f:
    config = yaml.safe_load(f)

JWT_SECRET = config["app"]["secret_key"]
JWT_ALGORITHM = config["jwt"]["algorithm"]

def verify_token(token):
    try:
        decoded = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM], options={"verify_aud": False, "verify_iss": False})
        return decoded
    except (ExpiredSignatureError, InvalidTokenError):
        return None