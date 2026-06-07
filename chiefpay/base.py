from aiohttp import ClientSession
from requests import Session
from chiefpay.constants import BASE_URL, Endpoints
from typing import Dict, Optional, Union


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
            "X-Api-Key": self.api_key,
        }
        self.session: Union[Session, ClientSession] = None

    def _init_session(self):
        raise NotImplementedError

    def _get_url(self, endpoint: Union[Endpoints, str]):
        if not self.session:
            self.session = self._init_session()

        path = endpoint.value if isinstance(endpoint, Endpoints) else endpoint
        url = self.base_url + path
        return url

    @staticmethod
    def _prepare_params(params: Optional[Dict]) -> Optional[Dict]:
        """
        Prepare query params for the wire: drop unset values and serialize
        booleans to the canonical lowercase "true"/"false".

        Callers pass natural Python values (bool, None); serialization concerns
        live here only. requests would send Python-style "True"/"False" (the API
        only accepts that case-insensitively), and aiohttp rejects bool/None
        param values outright.
        """
        if params is None:
            return None
        prepared = {}
        for key, value in params.items():
            if value is None:
                continue
            if isinstance(value, bool):
                value = "true" if value else "false"
            prepared[key] = value
        return prepared
