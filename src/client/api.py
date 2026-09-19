import requests

from utils.constants import VALID_APIS

from attr.converters import optional


from abc import ABC, abstractmethod


class BaseAPIClient(ABC):
    """
    Class responsible for managing public API calls.
    """
    def __init__(
        self,
        base_url: str,
        api_key: optional[str] = None,
        api_token: optional[str] = None,
    ) -> None:
        matched_name: str | None = next(
            (
                name
                for name, domain in VALID_APIS.items()
                if domain in base_url
            ),
            None,
        )

        if matched_name is None:
            raise ValueError(
                f"The provided base URL {base_url} for the API does not match any valid URL!"
            )
    
        self.name: str = matched_name
        self.base_url: str = base_url

    @abstractmethod
    def build_headers(self) -> dict[str, str]:
        match self.name:
            case "API-Sports":
                return {
                    "x-apisports-key": self.api_key
                }
            case _:
                raise ValueError(
                    f"Name {self.name} not recognized by API Client!"
                )

    @abstractmethod
    def build_request_url(self) -> str:
        pass        
