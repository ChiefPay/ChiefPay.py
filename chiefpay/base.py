from requests import Session
from chiefpay.constants import BASE_URL, ENDPOINTS


class BaseClient:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.headers = {
            "Accept": "application/json",
            "X-Api-Key": self.api_key
        }
        self.session: Session = self._init_session()


    def _init_session(self):
        raise NotImplementedError

    def _get_url(self, path: str):
        url = BASE_URL + ENDPOINTS.get(path)
        return url