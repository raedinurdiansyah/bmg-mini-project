from http import HTTPStatus
from urllib.parse import urlencode

import requests


class BaseApiResource:
    def __init__(
        self,
        base_url: str,
        *args,
        **kwargs,
    ):
        self.base_url = base_url
        self.available_request_method = ["get", "post", "put", "delete"]
        self.http_status_mapping = {status.value: status for status in HTTPStatus}

    def make_request(self, request_method: str, path: str = "", params: dict = {}):
        if request_method not in self.available_request_method:
            return HTTPStatus.METHOD_NOT_ALLOWED, {"message": "Method not allowed"}

        request_object = getattr(requests, request_method)

        if isinstance(params, dict):
            params = urlencode(params)  # type: ignore

        url = f"{self.base_url}{path}?{params}"

        resp = request_object(url=url)

        try:
            response_data = resp.json()
        except Exception:
            response_data = resp.text

        return self.http_status_mapping.get(resp.status_code), response_data
