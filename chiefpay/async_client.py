import aiohttp
from typing import Dict, Optional
from chiefpay.base import BaseClient
from chiefpay.constants import Endpoints
from chiefpay.exceptions import APIError, InvalidJSONError, ManyRequestsError, TransportError
from chiefpay.types import Rate, Wallet, Invoice, InvoicesHistory, TransactionsHistory, Transaction
from chiefpay.utils import Utils

from asyncio import sleep


class AsyncClient(BaseClient):
    """
    Client for making asynchronous requests to the payment system API.
    """

    def _init_session(self):
        return aiohttp.ClientSession(headers=self.headers)

    async def _request(self, method: str, path: str, max_retries: int = 3, **kwargs):
        url = self._get_url(path)
        for attempt in range(max_retries):
            try:
                async with self.session.request(method, url, **kwargs) as response:
                    return await self._handle_response(response)
            except ManyRequestsError:
                if attempt == max_retries - 1:
                    raise ManyRequestsError() from None
                continue

    async def _get_request(self, path: str, params: Optional[Dict] = {}, max_retries: int = 3):
        params = self._get_json(params)

        return await self._request("GET", path, max_retries, params=params)

    async def _post_request(self, path: str, json: Optional[Dict] = {}, max_retries: int = 3):
        json = self._get_json(json)

        return await self._request("POST", path, max_retries, json=json)

    async def _patch_request(self, path: str, json: Optional[Dict] = {}, max_retries: int = 3):
        json = self._get_json(json)

        return await self._request("PATCH", path, max_retries, json=json)

    async def _delete_request(self, path: str, json: Optional[Dict] = {}, max_retries: int = 3):
        json = self._get_json(json)

        return await self._request("DELETE", path, max_retries, json=json)


    def _get_json(self, data: Dict = {}):
        return {k: v for k, v in data.items() if v is not None}

    @staticmethod
    async def _handle_response(response: aiohttp.ClientResponse):
        if response.status == 429:
            headers = response.headers
            retry = int(headers.get('Retry-After-ms', '3000')) / 1000
            await sleep(retry)
            raise ManyRequestsError()

        if not (200 <= response.status < 300):
            text = await response.text()
            try:
                content_type = response.headers.get('Content-Type', '')
                error_data = await response.json(content_type=content_type)
                if error_data.get("status") == "error" and "message" in error_data:
                    message_data = error_data["message"]
                    raise APIError(
                        status_code=response.status,
                        message=message_data.get("message", "Unknown error"),
                        code=message_data.get("code"),
                        fields=message_data.get("fields")
                    )
                raise TransportError(response.status, text)
            except ValueError:
                raise InvalidJSONError()

        try:
            data = await response.json()
            return data.get('data')
        except ValueError:
            raise InvalidJSONError()


    async def get_rates(self) -> list[Rate]:
        """
        Asynchronously retrieves the current exchange rates.

        Returns:
             Rate DTO: The exchange rate data.
        """
        rates = await self._get_request(Endpoints.rates)
        return [Rate(**rate) for rate in rates]

    async def get_invoice(self, id: Optional[str] = None, order_id: Optional[str] = None) -> Invoice:
        """
        Asynchronously retrieves information about a specific invoice.

        Parameters:
            id (str): The invoice ID.
            order_id (str): The order ID.

        Returns:
             Invoice DTO: The invoice data.
        """
        params = {
            "id": id,
            "orderId": order_id
        }

        response_data = await self._get_request(Endpoints.invoice, params)
        return Invoice(**response_data)


    async def get_invoices(self, from_date: str, to_date: Optional[str] = None, limit: int = 100) -> InvoicesHistory:
        """
        Asynchronously retrieves a list of invoices within a specified date range.
        Args:
            from_date (str): The start date for the invoice history in 'YYYY-MM-DD' format.
            to_date (Optional[str], optional): The end date for the invoice history in 'YYYY-MM-DD' format. Defaults to None.
            limit (int, optional): The maximum number of invoices to retrieve. Defaults to 100.
        Returns:
            InvoicesHistory: An object containing the list of invoices and the total count of invoices.
        Raises:
            ValueError: If the date format for `from_date` or `to_date` is invalid.
        """
        Utils.validate_date(from_date)
        if to_date:
            Utils.validate_date(to_date)

        params = {
            "fromDate": from_date,
            "limit": limit,
            "toDate": to_date
        }

        response_data = await self._get_request(Endpoints.invoices_history, params)
        invoices = [Invoice(**data) for data in response_data.get('invoices')]
        return InvoicesHistory(
            invoices=invoices,
            totalCount=response_data.get('totalCount')
        )

    async def get_transactions(self, from_date: str, to_date: Optional[str] = None, limit: int = 100) -> TransactionsHistory:
        """
        Asynchronously retrieves transaction history within a specified date range.
        Args:
            from_date (str): The start date for the transaction history in 'YYYY-MM-DD' format.
            to_date (Optional[str], optional): The end date for the transaction history in 'YYYY-MM-DD' format. Defaults to None.
            limit (int, optional): The maximum number of transactions to retrieve. Defaults to 100.
        Returns:
            TransactionsHistory: An object containing the list of transactions and the total count.
        Raises:
            ValueError: If the date format for `from_date` or `to_date` is invalid.
        """
        Utils.validate_date(from_date)
        if to_date:
            Utils.validate_date(to_date)

        params = {
            "fromDate": from_date,
            "limit": limit,
            "toDate": to_date
        }

        response_data = await self._get_request(Endpoints.transactions_history, params)
        transactions = [Transaction(**data) for data in response_data.get('transactions')]
        return TransactionsHistory(
            transactions=transactions,
            totalCount=response_data.get('totalCount')
        )

    async def get_wallet(self, id: Optional[str] = None, order_id: Optional[str] = None) -> Wallet:
        """
        Retrieve wallet information based on wallet ID or order ID.
        Args:
            id (Optional[str]): The ID of the wallet to retrieve.
            order_id (Optional[str]): The order ID associated with the wallet to retrieve.
        Returns:
            Wallet: An instance of the Wallet class containing the retrieved wallet information.
        Raises:
            ValueError: If neither `id` nor `order_id` is provided.
        """
        params = {
            "id": id,
            "orderId": order_id
        }

        response_data = await self._get_request(Endpoints.wallet, params)
        return Wallet(**response_data)


    async def create_invoice(
        self,
        order_id: str,
        description: Optional[str] = None,
        amount: Optional[float] = None,
        currency: Optional[str] = "USD",
        fee_included: Optional[bool] = False,
        accuracy: Optional[float] = None,
        url_return: Optional[str] = None,
        url_success: Optional[str] = None
    ) -> Invoice:
        """
        Asynchronously creates a new invoice.

        Parameters:
            order_id (str): The order ID.
            description (str): The invoice description.
            amount (float): The amount.
            currency (str): The currency.
            fee_included (bool): Whether the fee is included in the amount.
            accuracy (float): The accuracy level.

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
            "urlReturn": url_return,
            "urlSuccess": url_success
        }

        response_data = await self._post_request(Endpoints.invoice, json=data)
        return Invoice(**response_data)

    async def create_wallet(self, order_id: str) -> Wallet:
        """
        Asynchronously creates a new wallet.

        Parameters:
            order_id (str): The order ID.

        Returns:
             Wallet DTO: The created wallet data.
        """
        data = {
            "orderId": order_id
        }

        response_data = await self._post_request(Endpoints.wallet, json=data)
        return Wallet(**response_data)


    async def cancel_invoice(self, id: Optional[str] = None, order_id: Optional[str] = None) -> Invoice:
        """
        Asynchronously cancels a specific invoice.

        Parameters:
            id (str): The invoice ID.
            order_id (str): The order ID.

        Returns:
                Invoice DTO: The invoice data.
        """
        data = {
            "id": id,
            "orderId": order_id
        }

        response_data = await self._delete_request(Endpoints.invoice, json=data)
        return Invoice(**response_data)


    async def prolongate_invoice(self, id: Optional[str] = None, order_id: Optional[str] = None) -> Invoice:
        """
        Asynchronously prolongates a specific invoice.

        Parameters:
            id (str): The invoice ID.
            order_id (str): The order ID.

        Returns:
             Invoice DTO: The invoice data.
        """
        data = {
            "id": id,
            "orderId": order_id
        }

        response_data = await self._patch_request(Endpoints.invoice, json=data)
        return Invoice(**response_data)


    async def close(self):
        """
        Closes the asynchronous session.

        This should be called after all asynchronous requests are complete.
        """
        await self.session.close()


    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc, tb):
        await self.close()
