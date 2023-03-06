from typing import Any

import requests.exceptions

from app.core.exceptions import NetworkConnectionError
from app.core.models import HTTPResponse


def make_request(method: str, url: str, params: Any = None, data: Any = None) -> HTTPResponse:
    try:
        response = requests.request(method, url, params=params, data=data)
        return HTTPResponse(status_code=response.status_code)
    except requests.exceptions.ConnectionError as e:
        raise NetworkConnectionError(str(e))
