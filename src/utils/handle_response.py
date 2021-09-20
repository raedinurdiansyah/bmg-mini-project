import json
from collections import namedtuple
from http import HTTPStatus
from typing import Any, Union

from flask import Response

from src.schemas.commons import DefaultResponseSchema


def handle_response(
    data=[], error=[], message="", status=HTTPStatus.OK, mimetype="application/json"
):
    code = status.value
    if any(error) and any(data) is False:
        data = DefaultResponseSchema().dump(dict(code=code, errors=error))
    else:
        data = DefaultResponseSchema().dump(dict(code=code, data=data, message=message))

    response = Response(json.dumps(data), status=status, mimetype=mimetype)
    return response


def default_response(
    status: Union[HTTPStatus, int] = HTTPStatus.OK, message: str = "", data: Any = None
):
    Response = namedtuple("Response", ["status", "message", "data"])
    return Response(status, message, data)
