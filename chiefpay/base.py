from aiohttp import ClientSession
from requests import Session
from chiefpay.constants import BASE_URL, ENDPOINTS


class BaseClient:
    def __init__(self, api_key: str, base_url: str = BASE_URL):
        self.api_key = api_key
        self.base_url = base_url
        self.headers = {
            "Accept": "application/json",
            "X-Api-Key": self.api_key
        }
        self.session: Session | ClientSession = self._init_session()


    def _init_session(self):
        raise NotImplementedError

    def _get_url(self, path: str):
        url = self.base_url + ENDPOINTS.get(path)
        return url