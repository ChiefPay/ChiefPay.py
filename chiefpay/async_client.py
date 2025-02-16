import aiohttp
from typing import Dict, Optional
from chiefpay.base import BaseClient
from chiefpay.constants import Endpoints
from chiefpay.exceptions import APIError, HTTPError
from chiefpay.types import Rate, History, Wallet, Invoice
from chiefpay.utils import Utils


class AsyncClient(BaseClient):
    """
    Client for making asynchronous requests to the payment system API.
    """

    def _init_session(self):
        session = aiohttp.ClientSession(headers=self.headers)
        return session

    async def _get_request(self, path: str, params: Optional[Dict] = None):
        url = self._get_url(path)
        async with self.session.get(url, params=params) as response:
            return await self._handle_response(response)

    async def _post_request(self, path: str, json: Optional[Dict] = None):
        url = self._get_url(path)
        async with self.session.post(url, json=json) as response:
            return await self._handle_response(response)

    @staticmethod
    async def _handle_response(response: aiohttp.ClientResponse):
        if not (200 <= response.status < 300):
            text = await response.text()
            raise HTTPError(response.status, text)
        try:
            data = await response.json()
            return data
        except ValueError:
            raise APIError("Invalid JSON response")


    async def get_rates(self) -> list[Rate]:
        """
        Asynchronously retrieves the current exchange rates.

        Returns:
             Rate DTO: The exchange rate data.
        """
        rates = await self._get_request(Endpoints.rates)
        return [Rate(**rate) for rate in rates]

    async def get_invoice(self, id: str, order_id: str) -> Invoice:
        """
        Asynchronously retrieves information about a specific invoice.

        Parameters:
            id (str): The invoice ID.
            order_id (str): The order ID.

        Returns:
             Invoice DTO: The invoice data.
        """
        params = {"id": id, "orderId": order_id}
        response_data = await self._get_request(Endpoints.invoice, params)
        return Invoice(**response_data)

    async def get_history(self, from_date: str, to_date: Optional[str] = None) -> list[History]:
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
        response_data = await self._get_request(Endpoints.history, params)
        return [History(**history) for history in response_data]

    async def get_wallet(self, id: str, order_id: str) -> Wallet:
        """
        Asynchronously retrieves information about a wallet.

        Parameters:
            id (str): The wallet ID.
            order_id (str): The order ID.

        Returns:
             Wallet DTO: The wallet data.
        """
        params = {"id": id, "orderId": order_id}
        response_data = await self._get_request(Endpoints.wallet, params)
        return Wallet(**response_data)


    async def create_invoice(
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
        Asynchronously creates a new invoice.

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


    async def close(self):
        """
        Closes the asynchronous session.

        This should be called after all asynchronous requests are complete.
        """
        await self.session.close()