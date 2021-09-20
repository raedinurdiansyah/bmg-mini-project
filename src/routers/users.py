from http import HTTPStatus

from flask import Blueprint, request
from marshmallow import EXCLUDE, ValidationError

from src.schemas.auth import GetUserSchema, InsertReferralSchema, UserAuthSchema
from src.services.users import UserServices
from src.utils.auth import login_required
from src.utils.commit_context_manager import commit_session
from src.utils.handle_response import handle_response

user_blueprint = Blueprint("user", __name__, url_prefix="/v1/users")


@user_blueprint.route("", methods=("GET",))
@login_required
def get_user_data():
    try:
        params = GetUserSchema(unknown=EXCLUDE).load(request.args)
    except ValidationError as e:
        return handle_response(data=e.messages, status=HTTPStatus.UNPROCESSABLE_ENTITY)

    try:
        resp = UserServices().get_users(**params)
        return handle_response(status=resp.status, data=resp.data, message=resp.message)
    except Exception as e:
        return handle_response(data=str(e), status=HTTPStatus.INTERNAL_SERVER_ERROR)


@user_blueprint.route("/<int:id>", methods=("PATCH",))
@login_required(return_validation_data=True)
def edit_user_data(id: int, **kwargs):
    if id != kwargs.get("validation_data")["user_id"]:
        return handle_response(
            status=HTTPStatus.FORBIDDEN, message="Forbidden", data=[]
        )
    try:
        params = UserAuthSchema(
            only=["username", "email", "name"], unknown=EXCLUDE
        ).load(data=kwargs.get("request"))
    except ValidationError as e:
        return handle_response(data=e.messages, status=HTTPStatus.UNPROCESSABLE_ENTITY)

    try:
        with commit_session():
            resp = UserServices(id=id).update_user(**params)

        return handle_response(status=resp.status, data=resp.data, message=resp.message)
    except Exception as e:
        return handle_response(data=str(e), status=HTTPStatus.INTERNAL_SERVER_ERROR)


@user_blueprint.route("/<int:id>/referral", methods=("PATCH",))
@login_required(return_validation_data=True)
def insert_user_referral(id: int, **kwargs):
    if id != kwargs.get("validation_data")["user_id"]:
        return handle_response(
            status=HTTPStatus.FORBIDDEN, message="Forbidden", data=[]
        )
    try:
        params = InsertReferralSchema(unknown=EXCLUDE).load(
            {"id": id, **kwargs.get("request")}
        )
    except ValidationError as e:
        return handle_response(data=e.messages, status=HTTPStatus.UNPROCESSABLE_ENTITY)

    try:
        with commit_session():
            resp = UserServices(**params).insert_referral()

        return handle_response(status=resp.status, data=resp.data, message=resp.message)
    except Exception as e:
        return handle_response(data=str(e), status=HTTPStatus.INTERNAL_SERVER_ERROR)
