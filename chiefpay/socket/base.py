from chiefpay.base import BaseClient
from chiefpay.constants import *


class BaseSocketClient(BaseClient):
    PATH = API_VERSION + ENDPOINTS.get('socket')

    def __init__(self, api_key: str, base_url: str = BASE_URL):
        super().__init__(api_key, base_url)
        self.rates = None
        self.notifications = []

    def _init_session(self):
        return None

    def get_latest_rates(self):
        return self.rates

    def get_notifications(self):
        return self.notifications

    def clear_notifications(self):
        self.notifications = []