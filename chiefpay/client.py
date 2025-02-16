import requests
import urllib3
from typing import Dict, Optional

from chiefpay.base import BaseClient


urllib3.disable_warnings()


class Client(BaseClient):
    def _init_session(self):
        session = requests.session()
        session.headers.update(self.headers)
        return session

    def _get_request(self, path: str, params: Optional[Dict] = None):
        url = self._get_url(path)
        response = self.session.get(url, params=params, verify=False)
        return self._handle_response(response)

    def _post_request(self, path: str, json: Optional[Dict] = None):
        url = self._get_url(path)
        response = self.session.post(url, json=json)
        return self._handle_response(response)

    @staticmethod
    def _handle_response(response: requests.Response):
        if not (200 <= response.status_code < 300):
            print(f"{response.status_code=}") # raise self exception
        try:
            return response.json()
        except ValueError as e:
            raise e # raise self exception


    def get_rates(self):
        return self._get_request("rates")

    def get_invoice(self, id: str, order_id: str):
        params = {"id": id, "orderId": order_id}
        return self._get_request("invoice", params)

    def get_history(self, from_date: str, to_date: Optional[str] = None):
        params = {"fromDate": from_date, "toDate": to_date}
        return self._get_request("history", params)

    def get_wallet(self, id: str, order_id: str):
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
        data = {
            "orderId": order_id
        }
        return self._post_request('wallet', json=data)