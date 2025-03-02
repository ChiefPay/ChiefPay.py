# ChiefPay SDK

This is the official Python SDK for interacting with the ChiefPay payment system.

## Installation

```bash
pip install chiefpay
```

## Usage

### Synchronous Client

```python
from chiefpay import Client

client = Client(api_key="your_api_key")
rates = client.get_rates()
print("Exchange rates:", rates)
```
### Asynchronous Client

```python
import asyncio
from chiefpay import AsyncClient

async def main():
    client = AsyncClient(api_key="your_api_key")
    rates = await client.get_rates()
    print("Exchange rates:", rates)

asyncio.run(main())
```

### WebSocket Client

```python
from chiefpay import SocketClient

def on_notification(data):
    print("New notification:", data)

with SocketClient(api_key="your_api_key") as client:
    client.set_on_notification(on_notification)
    input("Press Enter to exit...")
```

## Examples

For comprehensive examples, including advanced use cases, check out the examples directory