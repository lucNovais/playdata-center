import json
import logging

from playdata.client.sports import APISports

logger = logging.getLogger(__name__)


class FootballAPIToRaw:
    def __init__(self, api_key: str, base_url: str, endpoint: str) -> None:
        self.api_key = api_key
        self.base_url = base_url
        self.endpoint = endpoint

    def run(self) -> None:
        client = APISports(
            base_url=self.base_url,
            api_key=self.api_key,
        )

        headers: dict[str, str] = client.build_headers()
        request_url: str = client.build_request_url(self.endpoint)

        data = client.get_from_api(url=request_url, headers=headers)
        logger.info("API-Sports status: %s", json.dumps(data, indent=4))
