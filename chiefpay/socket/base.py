from typing import Callable, Union
from chiefpay.base import BaseClient
from chiefpay.constants import *
from chiefpay.types import Rate
from chiefpay.types.notification import NotificationInvoice, NotificationTransaction


class BaseSocketClient(BaseClient):
    """
    Base class for interacting with the payment system via WebSockets.
    """
    PATH = Endpoints.socket.value

    def __init__(self, api_key: str, base_url: str = BASE_URL):
        """
        Initializes the socket client.

        Parameters:
            api_key (str): API key for authentication.
            base_url (str): Base URL for the API endpoints.
        """
        super().__init__(api_key, base_url)
        self.rates: list[Rate] = None
        self.on_rates = None
        self.on_notification = None

    def _init_session(self):
        return None

    def set_on_notification(self, callback: Callable[[Union[NotificationInvoice, NotificationTransaction]], None]):
        """
        Sets a callback function to handle incoming notifications.

        Parameters:
            callback (function): A function that takes one argument (the notification data)
                                 and handles it appropriately.
        """
        self.on_notification = callback

    def set_on_rates(self, callback: Callable[[Union[NotificationInvoice, NotificationTransaction]], None]):
        """
        Sets a callback function to handle incoming rates updates.

        Parameters:
            callback (function): A function that takes one argument (the rates data)
                                and handles it appropriately.
        """
        self.on_rates = callback

    def get_latest_rates(self) -> list[Rate] | None:
        """
        Retrieves the latest exchange rates.

        Returns:
            dict: The latest exchange rates.
        """
        return self.rates