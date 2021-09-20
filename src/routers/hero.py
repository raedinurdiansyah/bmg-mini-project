from http import HTTPStatus

from flask import Blueprint, request

from src.schemas.hero import GetHeroSchema
from src.services.hero import HeroServices
from src.utils.handle_response import handle_response

hero_blueprint = Blueprint("hero", __name__, url_prefix="/v1/hero")


@hero_blueprint.route("", methods=("GET",))
def get_hero():
    try:
        parameters = GetHeroSchema(only=["id"]).load(data=request.args)

        result = HeroServices(**parameters).get_hero_detail()

        return handle_response(
            status=result.status,
            message=result.message,
            data=GetHeroSchema(many=True).dump(result.data),
        )
    except Exception as e:
        return handle_response(
            error=[{"code": 500, "message": str(e)}],
            status=HTTPStatus.INTERNAL_SERVER_ERROR,
        )
