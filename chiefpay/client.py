import requests
from typing import Dict, Optional
from time import sleep

from chiefpay.base import BaseClient
from chiefpay.constants import Endpoints
from chiefpay.exceptions import (
    APIError,
    InvalidJSONError,
    ManyRequestsError,
    TransportError,
)
from chiefpay.types import (
    Rate,
    Wallet,
    Invoice,
    InvoicesHistory,
    TransactionsHistory,
    Transaction,
    ChainToken,
)
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
            response = self.session.request(method, url, **kwargs, verify=False)
            try:
                return self._handle_response(response)
            except ManyRequestsError:
                if attempt == max_retries - 1:
                    raise ManyRequestsError() from None
                continue

    def _get_request(
        self, path: str, params: Optional[Dict] = None, max_retries: int = 3
    ):
        return self._request("GET", path, max_retries, params=params)

    def _post_request(
        self, path: str, json: Optional[Dict] = None, max_retries: int = 3
    ):
        return self._request("POST", path, max_retries, json=json)

    def _patch_request(
        self, path: str, json: Optional[Dict] = None, max_retries: int = 3
    ):
        return self._request("PATCH", path, max_retries, json=json)

    def _delete_request(
        self, path: str, json: Optional[Dict] = None, max_retries: int = 3
    ):
        return self._request("DELETE", path, max_retries, json=json)

    @staticmethod
    def _handle_response(response: requests.Response):
        if response.status_code == 429:
            headers = response.headers
            retry = int(headers.get("Retry-After-ms", "3000")) / 1000
            sleep(retry)
            raise ManyRequestsError()

        if not (200 <= response.status_code < 300):
            try:
                error_data = response.json()
                if error_data.get("status") == "error" and "message" in error_data:
                    message_data = error_data["message"]
                    raise APIError(
                        status_code=response.status_code,
                        message=message_data.get("message", "Unknown error"),
                        code=message_data.get("code"),
                        fields=message_data.get("fields"),
                        errors=message_data.get("errors"),
                    )
                raise TransportError(response.status_code, response.text)
            except ValueError:
                raise InvalidJSONError()

        try:
            data = response.json()
            return data.get("data")
        except ValueError:
            raise InvalidJSONError()

    def get_rates(self) -> list[Rate]:
        """
        Retrieves the current exchange rates.

        Returns:
             Rate DTO: The exchange rate data.
        """
        response_data = self._get_request(Endpoints.rates)
        return [Rate(**rate) for rate in response_data]

    def get_invoice(self, id: str) -> Invoice:
        """
        Retrieves information about a specific invoice by ID.

        Parameters:
            id (str): The invoice ID (UUID).

        Returns:
             Invoice DTO: The invoice data.
        """
        endpoint = Endpoints.invoice_by_id.value.format(id=id)
        response_data = self._get_request(endpoint)
        return Invoice(**response_data)

    def get_invoices(
        self,
        from_date: str,
        to_date: Optional[str] = None,
        limit: int = 100,
        not_notified: Optional[bool] = None,
    ) -> InvoicesHistory:
        """
        Retrieves invoices history within a given date range.

        Parameters:
            from_date (str): The start date.
            to_date (str, optional): The end date.
            limit (int): Maximum number of items (max 1000).
            not_notified (bool, optional): Return only notifications not yet acknowledged.
            Format: ISO 8601 (YYYY-MM-DDTHH:MM:SS.sssZ)

        Returns:
             InvoicesHistory: The invoices history with pagination.
        """
        Utils.validate_date(from_date)
        if to_date:
            Utils.validate_date(to_date)

        params = {"fromDate": from_date, "toDate": to_date, "limit": limit}
        if not_notified is not None:
            params["notNotified"] = not_notified
        response_data = self._get_request(Endpoints.invoices_history, params)
        invoices = [Invoice(**data) for data in response_data.get("invoices")]
        return InvoicesHistory(
            invoices=invoices, totalCount=response_data.get("totalCount")
        )

    def get_transactions(
        self,
        from_date: str,
        to_date: Optional[str] = None,
        limit: int = 100,
        not_notified: Optional[bool] = None,
    ) -> TransactionsHistory:
        """
        Retrieves transaction history within a given date range.

        Parameters:
            from_date (str): The start date.
            to_date (str, optional): The end date.
            limit (int): Maximum number of items (max 1000).
            not_notified (bool, optional): Return only notifications not yet acknowledged.
            Format: ISO 8601 (YYYY-MM-DDTHH:MM:SS.sssZ)

        Returns:
             TransactionsHistory: The transaction history with pagination.
        """
        Utils.validate_date(from_date)
        if to_date:
            Utils.validate_date(to_date)

        params = {"fromDate": from_date, "toDate": to_date, "limit": limit}

        if not_notified is not None:
            params["notNotified"] = not_notified
        response_data = self._get_request(Endpoints.transactions_history, params)
        transactions = [
            Transaction(**data) for data in response_data.get("transactions")
        ]
        return TransactionsHistory(
            transactions=transactions, totalCount=response_data.get("totalCount")
        )

    def get_wallet(self, id: str) -> Wallet:
        """
        Retrieve wallet information by wallet ID.

        Args:
            id (str): The ID of the wallet to retrieve (UUID).

        Returns:
            Wallet: An instance of the Wallet class containing the wallet information.
        """
        endpoint = Endpoints.wallet_by_id.value.format(id=id)
        response_data = self._get_request(endpoint)
        return Wallet(**response_data)

    def create_invoice(
        self,
        order_id: str,
        description: Optional[str] = None,
        amount: Optional[str] = None,
        fee_included: Optional[bool] = False,
        accuracy: Optional[str] = None,
        url_return: Optional[str] = None,
        url_success: Optional[str] = None,
        chain_token: Optional[ChainToken] = None,
    ) -> Invoice:
        """
        Creates a new invoice.

        Parameters:
            order_id (str): The order ID in your system.
            description (str, optional): The invoice description.
            amount (str, optional): The amount in USD (decimal string, e.g., "15.4").
            fee_included (bool, optional): Whether the fee is included in the amount.
            accuracy (str, optional): Payment tolerance ("0" to "0.05", e.g., "0.01" = 99% minimum).
            url_return (str, optional): Redirect URL after failure.
            url_success (str, optional): Redirect URL after success.
            chain_token (ChainToken, optional): Pre-selected chain and token.

        Returns:
             Invoice: The created invoice data.
        """
        data = {
            "orderId": order_id,
            "description": description,
            "amount": amount,
            "feeIncluded": fee_included,
            "accuracy": accuracy,
            "urlReturn": url_return,
            "urlSuccess": url_success,
        }

        if chain_token:
            data["chainToken"] = {
                "chain": chain_token.chain,
                "token": chain_token.token,
            }

        data = {k: v for k, v in data.items() if v is not None}

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

        data = {"orderId": order_id}

        response_data = self._post_request(Endpoints.wallet, json=data)
        return Wallet(**response_data)

    def cancel_invoice(self, id: str) -> Invoice:
        """
        Cancels an invoice by its ID.

        Args:
            id (str): The unique identifier of the invoice to be canceled (UUID).

        Returns:
            Invoice: The canceled invoice details.
        """
        endpoint = Endpoints.invoice_cancel.value.format(id=id)
        response_data = self._post_request(endpoint)
        return Invoice(**response_data)

    def prolongate_invoice(self, id: str) -> Invoice:
        """
        Prolongs an existing invoice expiration time.

        Args:
            id (str): The unique identifier of the invoice to be prolonged (UUID).

        Returns:
            Invoice: The prolonged invoice details.
        """
        endpoint = Endpoints.invoice_prolong.value.format(id=id)
        response_data = self._post_request(endpoint)
        return Invoice(**response_data)

    def patch_invoice(
        self,
        id: str,
        amount: Optional[str] = None,
        chain_token: Optional[ChainToken] = None,
    ) -> Invoice:
        """
        Updates invoice amount and/or chain_token if they were not set during creation.

        Args:
            id (str): The invoice ID (UUID).
            amount (str, optional): Invoice amount (can only be set if not specified during creation).
            chain_token (ChainToken, optional): Chain and token (can only be set if not specified during creation).

        Returns:
            Invoice: The updated invoice details.
        """
        data = {}
        if amount is not None:
            data["amount"] = amount
        if chain_token is not None:
            data["chainToken"] = {
                "chain": chain_token.chain,
                "token": chain_token.token,
            }

        endpoint = Endpoints.invoice_by_id.value.format(id=id)
        response_data = self._patch_request(endpoint, json=data)
        return Invoice(**response_data)
