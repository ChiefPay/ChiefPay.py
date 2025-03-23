import requests
from typing import Dict, Optional
from time import sleep

from chiefpay.base import BaseClient
from chiefpay.constants import Endpoints
from chiefpay.exceptions import HTTPError, APIError, ManyRequestsError
from chiefpay.types import Rate, Wallet, Invoice, InvoicesHistory, TransactionsHistory, Transaction
from chiefpay.utils import Utils


class Client(BaseClient):
    """
    Client for making synchronous requests to the payment system API.
    """
    def _init_session(self):
        session = requests.session()
        session.headers.update(self.headers)
        return session

    def _request(self, method: str, path: str, max_retries: int = 3, **kwargs):
        url = self._get_url(path)
        for attempt in range(max_retries):
            response = self.session.request(method, url, **kwargs)
            try:
                return self._handle_response(response)
            except ManyRequestsError:
                if attempt == max_retries - 1:
                    raise HTTPError(429, f"Too Many Requests after {max_retries} attempts")
                continue

    def _get_request(self, path: str, params: Optional[Dict] = None, max_retries: int = 3):
        return self._request("GET", path, max_retries, params=params)

    def _post_request(self, path: str, json: Optional[Dict] = None, max_retries: int = 3):
        return self._request("POST", path, max_retries, json=json)

    @staticmethod
    def _handle_response(response: requests.Response):
        if response.status_code == 429:
            headers = response.headers
            retry = int(headers.get('Retry-After-ms', '3000')) / 1000
            sleep(retry)
            raise ManyRequestsError()

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
        response_data = self._get_request(Endpoints.rates)
        return [Rate(**rate) for rate in response_data]

    def get_invoice(self, id: Optional[str] = None, order_id: Optional[str] = None) -> Invoice:
        """
        Retrieves information about a specific invoice.

        Parameters:
            id (str): The invoice ID.
            order_id (str): The order ID.

        Returns:
             Invoice DTO: The invoice data.
        """
        if id:
            params = {"id": id}
        elif order_id:
            params = {"orderId": order_id}
        response_data = self._get_request(Endpoints.invoice, params)
        return Invoice(**response_data)

    def get_invoices(self, from_date: str, to_date: Optional[str] = None, limit: int = 100) -> InvoicesHistory:
        """
        Retrieves invoices history within a given date range.

        Parameters:
            from_date (str): The start date.
            to_date (str, optional): The end date.
            Format: ISO 8601 (YYYY-MM-DDTHH:MM:SS.sssZ)

        Returns:
             Invoice DTO: The transaction history.
        """
        Utils.validate_date(from_date)
        if to_date:
            Utils.validate_date(to_date)

        params = {"fromDate": from_date, "toDate": to_date, "limit": limit}
        response_data = self._get_request(Endpoints.invoices_history, params)
        invoices = [Invoice(**data) for data in response_data.get('invoices')]
        return InvoicesHistory(
            invoices=invoices,
            totalCount=response_data.get('totalCount')
        )

    def get_transactions(self, from_date: str, to_date: Optional[str] = None, limit: int = 100) -> TransactionsHistory:
        """
        Retrieves transaction history within a given date range.

        Parameters:
            from_date (str): The start date.
            to_date (str, optional): The end date.
            Format: ISO 8601 (YYYY-MM-DDTHH:MM:SS.sssZ)

        Returns:
             Transaction DTO: The transaction history.
        """
        Utils.validate_date(from_date)
        if to_date:
            Utils.validate_date(to_date)

        params = {"fromDate": from_date, "toDate": to_date, "limit": limit}
        response_data = self._get_request(Endpoints.transactions_history, params)
        transactions = [Transaction(**data) for data in response_data.get('transactions')]
        return TransactionsHistory(
            transactions=transactions,
            totalCount=response_data.get('totalCount')
        )


    def get_wallet(self, id: Optional[str] = None, order_id: Optional[str] = None) -> Wallet:
        """
        Retrieve wallet information based on wallet ID or order ID.

        Args:
            id (Optional[str]): The ID of the wallet to retrieve.
            order_id (Optional[str]): The order ID associated with the wallet to retrieve.

        Returns:
            Wallet: An instance of the Wallet class containing the wallet information.

        Raises:
            ValueError: If neither `id` nor `order_id` is provided.
        """
        if id:
            params = {"id": id}
        elif order_id:
            params = {"orderId": order_id}
        response_data = self._get_request(Endpoints.wallet, params)
        return Wallet(**response_data)


    def create_invoice(
        self,
        order_id: str,
        description: Optional[str] = None,
        amount: Optional[float] = None,
        currency: Optional[str] = "USD",
        fee_included: Optional[bool] = False,
        accuracy: Optional[float] = None,
        discount: Optional[float] = None,
        url_return: Optional[str] = None,
        url_success: Optional[str] = None
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
            "urlReturn": url_return,
            "urlSuccess": url_success
        }

        response_data = self._post_request(Endpoints.invoice, json=data)
        return Invoice(**response_data)

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

        response_data = self._post_request(Endpoints.wallet, json=data)
        return Wallet(**response_data)