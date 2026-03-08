# ChiefPay SDK

Official Python SDK for interacting with the ChiefPay payment system.

## Requirements

- Python 3.9+

## Installation

```bash
pip install chiefpay
```

## Quick Start

### Synchronous Client

```python
from chiefpay import Client

client = Client(api_key="your_api_key")

# Get exchange rates
rates = client.get_rates()

# Get available payment methods
payment_methods = client.get_payment_methods()

# Create an invoice
invoice = client.create_invoice(
    order_id="unique-order-id",
    amount="15.4",  # String format, USD
    fee_included=False,
    accuracy="0.01"
)
print(f"Payment URL: {invoice.url}")
```

### Asynchronous Client

```python
import asyncio
from chiefpay import AsyncClient

async def main():
    async with AsyncClient(api_key="your_api_key") as client:
        rates = await client.get_rates()

        invoice = await client.create_invoice(
            order_id="unique-order-id",
            amount="100.50"
        )
        print(f"Invoice ID: {invoice.id}")

asyncio.run(main())
```

### WebSocket Client

```python
from chiefpay import SocketClient

def on_notification(data):
    if data.type == "invoice":
        print(f"Invoice updated: {data.invoice.status}")
    elif data.type == "transaction":
        print(f"Transaction: {data.transaction.txid}")

with SocketClient(api_key="your_api_key") as client:
    client.set_on_notification(on_notification)
    input("Press Enter to exit...")
```

### Asynchronous WebSocket Client

```python
import asyncio
from chiefpay import AsyncSocketClient

async def on_notification(data):
    print(f"Notification type: {data.type}")

async def on_rates(rates):
    print(f"Rates updated: {len(rates)} rates")

async def main():
    async with AsyncSocketClient(api_key="your_api_key") as client:
        client.set_on_notification(on_notification)
        client.set_on_rates(on_rates)
        await asyncio.sleep(60)

asyncio.run(main())
```

## Error Handling

```python
from chiefpay import Client
from chiefpay.exceptions import (
    APIError,
    TransportError,
    InvalidJSONError,
    ManyRequestsError,
    ChiefPayErrorCode,
)

client = Client(api_key="your_api_key")

try:
    invoice = client.create_invoice(order_id="", amount="10")
except APIError as e:
    print(f"API Error: {e.code} - {e.errors}")
    if e.code == ChiefPayErrorCode.INVALID_ARGUMENT:
        print("Invalid parameters")
except ManyRequestsError:
    print("Rate limit exceeded")
except TransportError as e:
    print(f"Network error: {e.status_code}")
except InvalidJSONError:
    print("Invalid JSON response")
```

## Examples

For comprehensive examples, including advanced use cases, check out the [examples](./examples) directory:

- [`sync.py`](./examples/sync.py) - Synchronous REST API usage
- [`async.py`](./examples/async.py) - Asynchronous REST API usage
- [`socket.py`](./examples/socket.py) - WebSocket real-time notifications
