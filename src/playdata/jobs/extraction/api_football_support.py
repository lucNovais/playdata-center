import logging

from playdata.client.sports import APISports

logger = logging.getLogger(__name__)


class APIFootballSupport:
    def __init__(
        self, api_key: str, api_version: str, base_url: str, endpoints: list[str]
    ) -> None:
        self.api_key = api_key
        self.api_version = api_version
        self.base_url = base_url
        self.endpoints = endpoints

    def get_available_timezones(
        self, client: APISports, headers: dict[str, str], request_url: str
    ) -> list[str]:
        raw_response = client.get_from_api(url=request_url, headers=headers)

        return raw_response["response"]

    def run(self) -> None:
        client = APISports(
            base_url=self.base_url,
            api_key=self.api_key,
        )

        headers: dict[str, str] = client.build_headers()

        timezone_endpoint: str = self.endpoints[0]
        timezone_request_url: str = client.build_request_url(timezone_endpoint)

        timezones: list[str] = self.get_available_timezones(
            client, headers, timezone_request_url
        )

        # data = client.get_from_api(url=request_url, headers=headers)
        # logger.info("API-Sports status: %s", json.dumps(data, indent=4))

        print(timezones)
