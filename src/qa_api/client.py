import logging
from typing import Any
from urllib.parse import urlsplit

import requests

LOGGER = logging.getLogger(__name__)
DEFAULT_BASE_URL = "https://qa-internship.avito.com"
REGISTER = "/api/1/register"
AUTHORIZE = "/api/1/autorize"
ITEMS = "/api/1/item"


class ApiTransportError(RuntimeError):
    pass


class ApiTimeoutError(ApiTransportError):
    pass


def https_base_url(value: str) -> str:
    url = value.strip().rstrip("/")
    error = "QA_API_BASE_URL must be an HTTPS URL without credentials, query or fragment"
    try:
        parsed = urlsplit(url)
        port = parsed.port
    except ValueError:
        raise ValueError(error) from None
    if (
        parsed.scheme != "https"
        or not parsed.hostname
        or parsed.username is not None
        or port == 0
        or "?" in url
        or "#" in url
    ):
        raise ValueError(error)
    return url


class ApiClient:
    def __init__(self, session: requests.Session, base_url: str, timeout: float) -> None:
        self.session = session
        self.base_url = https_base_url(base_url)
        self.timeout = timeout

    def request(
        self,
        method: str,
        path: str,
        *,
        token: str | None = None,
        json: dict[str, Any] | None = None,
    ) -> requests.Response:
        headers = {"Accept": "application/json"}
        if token is not None:
            headers["Authorization"] = f"Bearer {token}"

        try:
            response = self.session.request(
                method,
                self.base_url + path,
                headers=headers,
                json=json,
                timeout=self.timeout,
                allow_redirects=False,
            )
        except requests.RequestException as exc:
            error_type = ApiTimeoutError if isinstance(exc, requests.Timeout) else ApiTransportError
            raise error_type(
                f"{method} {path}: HTTP request failed ({type(exc).__name__})"
            ) from None

        LOGGER.info(
            "%s %s -> HTTP %s (%.0f ms)",
            method,
            path,
            response.status_code,
            response.elapsed.total_seconds() * 1000,
        )
        return response
