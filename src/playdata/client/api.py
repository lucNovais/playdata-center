import logging
from abc import ABC, abstractmethod
from typing import Any

import requests
from httpx import HTTPError
from requests import Response

from playdata.utils.constants import VALID_APIS

logger = logging.getLogger(__name__)


class BaseAPIClient(ABC):
    """Base class that sets the standard for public API calls.

    Every API client implemented on playdata-center should inherit
    from this class.
    """

    def __init__(
        self,
        base_url: str,
        api_key: str | None = None,
        api_token: str | None = None,
    ) -> None:
        """Initialize the client and resolve which public API it targets.

        Args:
            base_url: Public API base url (without https).
            api_key: If needed, the API key for authentication.
            api_token: If needed, the API token for authentication.

        Raises:
            ValueError: If base_url does not match any valid API.
        """
        matched_name: str | None = next(
            (name for name, domain in VALID_APIS.items() if domain in base_url),
            None,
        )

        if matched_name is None:
            raise ValueError(
                f"The provided base URL {base_url} for the API does not match any valid URL!"
            )

        self.name: str = matched_name
        self.base_url: str = base_url

        self.api_key: str | None = api_key
        self.api_token: str | None = api_token

    @abstractmethod
    def build_headers(self) -> dict[str, str]:
        """Build the authentication headers expected by the target API.

        Returns:
            The headers to send on every request.

        Raises:
            ValueError: If the resolved API has no known header format.
        """
        logger.info(f"Building headers for {self.name}...")

        match self.name:
            case "API-Sports":
                return {"x-apisports-key": self.api_key}
            case _:
                raise ValueError(f"Name {self.name} not recognized by API Client!")

    @abstractmethod
    def build_request_url(self, endpoint: str) -> str:
        """Build the full request url for an API endpoint.

        Args:
            endpoint: Endpoint path, relative to the base url.

        Returns:
            The absolute url for the endpoint.
        """
        logger.info(f"Building request URL for the following endpoint: {endpoint}...")

        return f"https://{self.base_url}/{endpoint}"

    @abstractmethod
    def get_from_api(self, url: str, headers: dict[str, str]) -> Any:
        """Perform a GET request and decode the JSON response.

        Args:
            url: Absolute url to request.
            headers: Headers to send with the request, usually the
                output of build_headers.

        Returns:
            The decoded JSON payload.

        Raises:
            HTTPError: If the request fails with an HTTP error.
            Exception: If any other unexpected error occurs.
        """
        logger.info(f"Getting data from {url}...")

        try:
            response: Response = requests.get(url=url, headers=headers)
            data: Any = response.json()
        except HTTPError as err:
            raise HTTPError(
                f"HTTP error occurred while making GET on {url}: {err}"
            ) from err
        except Exception as err:
            raise Exception(
                f"An unexpected error occurred while making GET on {url}: {err}"
            ) from err

        logger.info("Retrieved data!")
        return data
