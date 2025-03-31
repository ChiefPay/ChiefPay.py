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
### Asynchronous WebSocket Client

```python
import asyncio
from chiefpay import AsyncSocketClient

async def on_notification(data):
    print("New notification:", data)

async def main():
    async with AsyncSocketClient(api_key="your_api_key") as client:
        client.set_on_notification(on_notification)
        print("Asynchronous WebSocket client started. Waiting for events...")
        await asyncio.sleep(60)

asyncio.run(main())
```
### Error Handling

```python
from chiefpay import Client
from chiefpay.exceptions import APIError, TransportError, InvalidJSONError, ManyRequestsError, ChiefPayErrorCode

def handle_errors():
    client = Client(api_key="wrong_api_key")

    try:
        rates = client.get_rates()
        print("Exchange rates:", rates)
    except APIError as e:
        if e.code == ChiefPayErrorCode.PERMISSION_DENIED:
            print(f"Permission denied. Check your API key in: {e.fields}")
        else:
            print(f"API Error: {e.message} (HTTP Status: {e.status_code})")
    except ManyRequestsError:
        print("Too many requests. Please try again later.")
    except TransportError as e:
        print(f"Transport error occurred: {e}")
    except InvalidJSONError as e:
        print(f"Invalid JSON response: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    handle_errors()
```
## Examples

For comprehensive examples, including advanced use cases, check out the examples directory