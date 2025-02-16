# ChiefPay SDK

This is the official Python SDK for interacting with the ChiefPay payment system.

## Installation

```bash
pip install chiefpay-sdk
```

## Usage

```python
from chiefpay import Client

client = Client(api_key="your_api_key")
rates = client.get_rates()
print(rates)
```