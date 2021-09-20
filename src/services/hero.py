from http import HTTPStatus

from flask import current_app

from src.utils.handle_response import default_response
from src.utils.requests import BaseApiResource


class HeroServices:
    def __init__(self, **kwargs):
        self.id: str = kwargs.get("id")
        self.url_hero: str = current_app.config.get("HERO_URL")
        self.api_request: BaseApiResource = (
            BaseApiResource(base_url=self.url_hero) or None
        )

    def heroes_data(self) -> dict:
        try:
            status, resp = self.api_request.make_request(request_method="get")
            if status != 200 or not resp.get("data"):
                raise Exception
            return resp.get("data")
        except Exception:
            return []

    def get_hero_detail(self) -> default_response:
        heroes_data = self.heroes_data()
        if not heroes_data:
            return default_response(
                status=HTTPStatus.INTERNAL_SERVER_ERROR,
                message="Failed to get heroes data",
                data=[],
            )
        datum = heroes_data.values()
        data = list(datum)
        if self.id:
            data = list(filter(lambda x: self.id in x["id"].lower(), datum))

        return default_response(data=data)
