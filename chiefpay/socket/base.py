from chiefpay.base import BaseClient
from chiefpay.constants import *


class BaseSocketClient(BaseClient):
    URL = BASE_URL
    PATH = API_VERSION + ENDPOINTS.get('socket')

    def __init__(self, api_key: str):
        super().__init__(api_key)
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