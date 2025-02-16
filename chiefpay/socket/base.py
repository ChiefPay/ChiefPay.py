from chiefpay.base import BaseClient
from chiefpay.constants import *
from chiefpay.types import Rate


class BaseSocketClient(BaseClient):
    """
    Base class for interacting with the payment system via WebSockets.
    """
    PATH = API_VERSION + ENDPOINTS.get('socket')

    def __init__(self, api_key: str, base_url: str = BASE_URL):
        """
        Initializes the socket client.

        Parameters:
            api_key (str): API key for authentication.
            base_url (str): Base URL for the API endpoints.
        """
        super().__init__(api_key, base_url)
        self.rates: list[Rate] = None
        self.notifications = []

    def _init_session(self):
        return None

    def get_latest_rates(self) -> list[Rate] | None:
        """
        Retrieves the latest exchange rates.

        Returns:
            dict: The latest exchange rates.
        """
        return self.rates

    def get_notifications(self) -> list:
        """
        Retrieves a list of notifications.

        Returns:
            list: The list of notifications.
        """
        return self.notifications

    def clear_notifications(self):
        """
        Clears the list of notifications.
        """
        self.notifications = []
