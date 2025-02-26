from aiohttp import ClientSession
from requests import Session
from chiefpay.constants import BASE_URL, Endpoints
from typing import Union


class BaseClient:
    """
    Base class for interacting with the payment system.
    """
    def __init__(self, api_key: str, base_url: str = BASE_URL):
        """
        Initialize the client.

        Parameters:
            api_key (str): API key for authentication.
            base_url (str): Base URL for the API endpoints.
        """
        self.api_key = api_key
        self.base_url = base_url
        self.headers = {
            "Accept": "application/json",
            "X-Api-Key": self.api_key
        }
        self.session: Union[Session, ClientSession] = self._init_session()


    def _init_session(self):
        raise NotImplementedError

    def _get_url(self, endpoint: Endpoints):
        url = self.base_url + endpoint.value
        return url