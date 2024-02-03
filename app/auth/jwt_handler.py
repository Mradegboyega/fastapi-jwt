import time
import jwt
from decouple import config

JWT_SECRET = config("secret")
JWT_ALGORITHM = config("algorithm")

# this function returns generated tokens (JWT)
def token_response(token: str):
    return {
        "token_type": "Bearer",
        "access_token": token
    }

# function for signing the JWT str
def signJWT(userID: str):
    payload = {
        "userID": userID,
        "expiry": time.time() + 600
    }

    token = jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)
    return token_response(token)

# function to decode jwt token
def decodeJWT(token: str):
    try:
        decoded_token = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        return decoded_token if decoded_token['expiry'] >= time.time() else None
    except jwt.ExpiredSignatureError:
        return None  # Token has expired
    except jwt.InvalidTokenError:
        return None  # Invalid token
