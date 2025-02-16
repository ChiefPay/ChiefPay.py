import requests
from typing import Dict, Optional

from chiefpay.base import BaseClient
from chiefpay.exceptions import HTTPError, APIError
from chiefpay.types import History, Wallet, Invoice, Rate
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
            data = response.json()
            return data.get('data')
        except ValueError:
            raise APIError("Invalid JSON response")


    def get_rates(self) -> list[Rate]:
        """
        Retrieves the current exchange rates.

        Returns:
             Rate DTO: The exchange rate data.
        """
        response_data = self._get_request("rates")
        return [Rate(**rate) for rate in response_data]

    def get_invoice(self, id: str, order_id: str) -> Invoice:
        """
        Retrieves information about a specific invoice.

        Parameters:
            id (str): The invoice ID.
            order_id (str): The order ID.

        Returns:
             Invoice DTO: The invoice data.
        """
        params = {"id": id, "orderId": order_id}
        response_data = self._get_request("invoice", params)
        return Invoice(**response_data)

    def get_history(self, from_date: str, to_date: Optional[str] = None) -> list[History]:
        """
        Retrieves transaction history within a given date range.

        Parameters:
            from_date (str): The start date.
            to_date (str, optional): The end date.
            Format: ISO 8601 (YYYY-MM-DDTHH:MM:SS.sssZ)

        Returns:
             History DTO: The transaction history.
        """
        Utils.validate_date(from_date)
        if to_date:
            Utils.validate_date(to_date)

        params = {"fromDate": from_date, "toDate": to_date}
        response_data = self._get_request("history", params)
        return [History(**history) for history in response_data]

    def get_wallet(self, id: str, order_id: str) -> Wallet:
        """
        Retrieves information about a wallet.

        Parameters:
            id (str): The wallet ID.
            order_id (str): The order ID.

        Returns:
             Wallet DTO: The created wallet data.
        """

        params = {"id": id, "orderId": order_id}
        response_data = self._get_request("wallet", params)
        return Wallet(**response_data)


    def create_invoice(
        self,
        order_id: str,
        description: str,
        amount: str,
        currency: str,
        fee_included: bool,
        accuracy: str,
        discount: str,
    ) -> Invoice:
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
             Invoice DTO: The created invoice data.
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

    def create_wallet(self, order_id: str) -> Wallet:
        """
        Creates a new wallet.

        Parameters:
            order_id (str): The order ID.

        Returns:
             Wallet DTO: The created wallet data.
        """

        data = {
            "orderId": order_id
        }
        return self._post_request('wallet', json=data)