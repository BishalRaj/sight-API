import time

import jwt
from decouple import config
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer

JWT_SECRET = config("secret")
JWT_ALGORITHM = config("algorithm")

# Returns generated token


def token_response(token: str):
    return {
        "access_token": token
    }

# to sign in jwt string


def signJWT(userID: str):
    payload = {
        "userID": userID,
        "expiry": time.time()+600
    }
    token = jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)
    return token_response(token)


def decodeJWT(token: str):
    try:
        decode_token = jwt.decode(token, JWT_SECRET, algorithms=JWT_ALGORITHM)
        # print(decode_token)
        return decode_token if decode_token['expiry'] >= time.time() else None
    except:
        return {}


async def authenticate(token: str = Depends(OAuth2PasswordBearer(tokenUrl=JWT_SECRET))):
    print(token)
    return {"token": token}
