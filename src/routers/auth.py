from http import HTTPStatus

from flask import Blueprint, request
from marshmallow import ValidationError

from src.schemas.auth import LoginSchema, RegisterSchema
from src.services.auth import AuthServices
from src.utils.commit_context_manager import commit_session
from src.utils.handle_response import handle_response

auth_blueprint = Blueprint("auth", __name__, url_prefix="/v1/auth")


@auth_blueprint.route("/register", methods=("POST",))
def register():
    try:
        params = RegisterSchema().load(data=request.json)
    except ValidationError as e:
        return handle_response(data=e.messages, status=HTTPStatus.UNPROCESSABLE_ENTITY)

    try:
        with commit_session():
            resp = AuthServices().register(**params)
        return handle_response(status=resp.status, data=resp.data, message=resp.message)
    except Exception as e:
        return handle_response(data=str(e), status=HTTPStatus.INTERNAL_SERVER_ERROR)


@auth_blueprint.route("/login", methods=("POST",))
def login():
    try:
        params = LoginSchema().load(data=request.json)
    except ValidationError as e:
        return handle_response(data=e.messages, status=HTTPStatus.UNPROCESSABLE_ENTITY)

    try:
        with commit_session():
            resp = AuthServices().login(**params)
        return handle_response(status=resp.status, data=resp.data, message=resp.message)
    except Exception as e:
        return handle_response(data=str(e), status=HTTPStatus.INTERNAL_SERVER_ERROR)
