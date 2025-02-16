import requests
from typing import Dict, Optional

from chiefpay.base import BaseClient
from chiefpay.exceptions import HTTPError, APIError
from chiefpay.utils import Utils


class Client(BaseClient):
    """
    Client for making synchronous requests to the payment system API.
    """
    def _init_session(self):
        session = requests.session()
        session.headers.update(self.headers)
        return session

    def _get_request(self, path: str, params: Optional[Dict] = None):
        url = self._get_url(path)
        response = self.session.get(url, params=params)
        return self._handle_response(response)

    def _post_request(self, path: str, json: Optional[Dict] = None):
        url = self._get_url(path)
        response = self.session.post(url, json=json)
        return self._handle_response(response)

    @staticmethod
    def _handle_response(response: requests.Response):
        if not (200 <= response.status_code < 300):
            raise HTTPError(response.status_code, response.text)
        try:
            return response.json()
        except ValueError:
            raise APIError("Invalid JSON response")


    def get_rates(self):
        """
        Retrieves the current exchange rates.

        Returns:
            dict: The exchange rate data.
        """
        return self._get_request("rates")

    def get_invoice(self, id: str, order_id: str):
        """
        Retrieves information about a specific invoice.

        Parameters:
            id (str): The invoice ID.
            order_id (str): The order ID.

        Returns:
            dict: The invoice data.
        """

        params = {"id": id, "orderId": order_id}
        return self._get_request("invoice", params)

    def get_history(self, from_date: str, to_date: Optional[str] = None):
        """
        Retrieves transaction history within a given date range.

        Parameters:
            from_date (str): The start date.
            to_date (str, optional): The end date.
            Format: ISO 8601 (YYYY-MM-DDTHH:MM:SS.sssZ)

        Returns:
            dict: The transaction history.
        """
        Utils.validate_date(from_date)
        if to_date:
            Utils.validate_date(to_date)

        params = {"fromDate": from_date, "toDate": to_date}
        return self._get_request("history", params)

    def get_wallet(self, id: str, order_id: str):
        """
        Retrieves information about a wallet.

        Parameters:
            id (str): The wallet ID.
            order_id (str): The order ID.

        Returns:
            dict: The wallet data.
        """

        params = {"id": id, "orderId": order_id}
        return self._get_request("wallet", params)


    def create_invoice(
        self,
        order_id: str,
        description: str,
        amount: str,
        currency: str,
        fee_included: bool,
        accuracy: str,
        discount: str,
    ):
        """
        Creates a new invoice.

        Parameters:
            order_id (str): The order ID.
            description (str): The invoice description.
            amount (str): The amount.
            currency (str): The currency.
            fee_included (bool): Whether the fee is included in the amount.
            accuracy (str): The accuracy level.
            discount (str): The discount.

        Returns:
            dict: The created invoice data.
        """

        data = {
            "orderId": order_id,
            "description": description,
            "amount": amount,
            "currency": currency,
            "feeIncluded": fee_included,
            "accuracy": accuracy,
            "discount": discount,
        }
        return self._post_request('invoice', json=data)

    def create_wallet(self, order_id: str):
        """
        Creates a new wallet.

        Parameters:
            order_id (str): The order ID.

        Returns:
            dict: The created wallet data.
        """

        data = {
            "orderId": order_id
        }
        return self._post_request('wallet', json=data)