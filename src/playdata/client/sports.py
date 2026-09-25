import logging
from typing import Any

from playdata.client.api import BaseAPIClient

logger = logging.getLogger(__name__)


class APISports(BaseAPIClient):
    """Class responsible for handling API-Sports (api-sports.io) calls."""

    def __init__(
        self,
        base_url: str,
        api_key: str | None = None,
        api_token: str | None = None,
    ) -> None:
        logger.info("Initializing API Sports client...")
        super().__init__(base_url, api_key, api_token)

    def build_headers(self) -> dict[str, str]:
        return super().build_headers()

    def build_request_url(self, endpoint: str) -> str:
        return super().build_request_url(endpoint)

    def get_from_api(self, url: str, headers: dict[str, str]) -> Any:
        return super().get_from_api(url, headers)
