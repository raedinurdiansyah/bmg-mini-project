import base64
import functools
import hashlib
import os
import re
from datetime import datetime, timedelta
from http import HTTPStatus
from typing import Union

import jwt
from flask import current_app, request

from src.models.tokens import Token
from src.utils.handle_response import handle_response


def validate_email(email: str) -> bool:
    try:
        regex = re.compile(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)")
        match = regex.match(email)
        return True if match else False

    except Exception:
        return False


def encode_auth_token(user_id: int) -> dict:
    expired = datetime.utcnow() + timedelta(hours=6)
    payload = dict(exp=expired, iat=datetime.utcnow(), sub=user_id)

    token = jwt.encode(payload, current_app.config.get("SECRET_KEY"), algorithm="HS256")

    return dict(token=token, token_expired=expired)


def decode_auth_token(token: str) -> Union[dict, str]:
    try:
        return jwt.decode(
            token, current_app.config.get("SECRET_KEY"), algorithms=["HS256"]
        )
    except jwt.ExpiredSignatureError:
        return "Signature expired. Please log in again."
    except jwt.InvalidTokenError:
        return "Invalid token. Please log in again."


def validate_token(token: str) -> dict:

    auth_token = Token.query.filter_by(token=token, is_active=True).first()
    if not auth_token:
        raise Exception("Token blacklisted or revoked")

    decoded_token = decode_auth_token(token)
    if isinstance(decoded_token, str):
        raise Exception(decoded_token)

    user_id = auth_token.user_id

    return dict(
        sub=decoded_token.get("sub"), exp=decoded_token.get("exp"), user_id=user_id
    )


def get_digest(password: str):
    salt = base64.b64encode(os.urandom(32))
    digest = create_digest(password, salt)
    return salt, digest


def create_digest(password: str, salt: bytes):
    return hashlib.sha256(salt + password.encode("UTF-8")).hexdigest()


def check_digest(password: str, salt: str):
    return hashlib.sha256(salt.encode("UTF-8") + password.encode("UTF-8")).hexdigest()


def check_password(password: str, saved_password: str, salt: str) -> bool:
    salted_password = check_digest(password, salt)
    return True if saved_password == salted_password else False


def login_required(_func=None, return_validation_data=False):
    def decorator_login_required(func):
        @functools.wraps(func)
        def wrap(*args, **kwargs):
            try:
                auth_header = request.headers.get("Authorization")
                if not auth_header:
                    raise Exception("Unauthorized")

                auth_data = auth_header.split(" ")
                if len(auth_data) != 2:
                    raise Exception("Unauthorized")

                if auth_data[0] != "Bearer":
                    raise Exception("Unauthorized")

                auth_token = auth_data[1]

                try:
                    token_validation = validate_token(auth_token)
                except Exception:
                    raise Exception

                if return_validation_data:
                    kwargs.update({"validation_data": token_validation})

                if (
                    request.json
                    and isinstance(request.json, dict)
                    and request.data.decode
                ):
                    kwargs.update({"request": request.json})

                return func(*args, **kwargs)

            except Exception as e:
                return handle_response(
                    data=[], message=str(e), status=HTTPStatus.UNAUTHORIZED
                )

        return wrap

    if _func is None:
        return decorator_login_required
    else:
        return decorator_login_required(_func)
