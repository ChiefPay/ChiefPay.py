import aiohttp
from typing import Dict, Optional
from chiefpay.base import BaseClient
from chiefpay.exceptions import APIError, HTTPError


class AsyncClient(BaseClient):
    def _init_session(self):
        connector = aiohttp.TCPConnector(   # Del
            verify_ssl=False
        )
        session = aiohttp.ClientSession(headers=self.headers,
                                        connector=connector)
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
            return await response.json()
        except ValueError:
            raise APIError("Invalid JSON response")


    async def get_rates(self):
        return await self._get_request("rates")

    async def get_invoice(self, id: str, order_id: str):
        params = {"id": id, "orderId": order_id}
        return await self._get_request("invoice", params)

    async def get_history(self, from_date: str, to_date: Optional[str] = None):
        params = {"fromDate": from_date, "toDate": to_date}
        return await self._get_request("history", params)

    async def get_wallet(self, id: str, order_id: str):
        params = {"id": id, "orderId": order_id}
        return await self._get_request("wallet", params)

    async def create_invoice(
        self,
        order_id: str,
        description: str,
        amount: str,
        currency: str,
        fee_included: bool,
        accuracy: str,
        discount: str,
    ):
        data = {
            "orderId": order_id,
            "description": description,
            "amount": amount,
            "currency": currency,
            "feeIncluded": fee_included,
            "accuracy": accuracy,
            "discount": discount,
        }
        return await self._post_request('invoice', json=data)

    async def create_wallet(self, order_id: str):
        data = {
            "orderId": order_id
        }
        return await self._post_request('wallet', json=data)

    async def close(self):
        await self.session.close()