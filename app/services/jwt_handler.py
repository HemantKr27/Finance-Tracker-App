import jwt
import datetime

SECRET_KEY = "supersecretkey"
ALGORITHM = "HS256"
TOKEN_EXPIRY_HOURS = 24


def create_token(user_id):
    payload = {
        "user_id": user_id,
        "exp": datetime.datetime.now() + datetime.timedelta(hours=TOKEN_EXPIRY_HOURS)
    }

    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

    return token


def verify_token(token):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload["user_id"]

    except jwt.ExpiredSignatureError:
        return None

    except jwt.InvalidTokenError:
        return None