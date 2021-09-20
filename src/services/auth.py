from http import HTTPStatus

from src import db
from src.models.tokens import Token
from src.services.users import UserServices
from src.utils.auth import check_password, encode_auth_token
from src.utils.handle_response import default_response


class AuthServices:
    def __init__(self):
        pass

    def register(self, **params):
        return UserServices(**params).create()

    def login(self, **params):
        username = params["username"]
        password = params["password"]

        user = UserServices._get_user({"username": username})
        if not user:
            return default_response(
                status=HTTPStatus.UNPROCESSABLE_ENTITY, message="Invalid user", data=[]
            )

        valid_password = check_password(password, user.password, user.salt)
        if not valid_password:
            return default_response(
                status=HTTPStatus.UNPROCESSABLE_ENTITY,
                message="Invalid password",
                data=[],
            )

        token_result = encode_auth_token(user.id)
        auth_token = token_result["token"]
        # save token after login success
        token_params = dict(
            user_id=user.id, token=auth_token, expires=token_result["token_expired"]
        )
        token = Token(**token_params)
        db.session.add(token)
        db.session.flush()

        # TODO handle with marshmallow dump
        return default_response(
            message="Login success",
            data=dict(authorization_token=auth_token, user_id=user.id, name=user.name),
        )
