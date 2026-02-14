import asyncio
from chiefpay import SocketClient, AsyncSocketClient
from chiefpay.types import NotificationInvoice, NotificationTransaction


# Synchronous WebSocket Client


def on_notification(data: NotificationInvoice | NotificationTransaction):
    """Handler for invoice and transaction notifications"""
    if data.type == "invoice":
        print(f"Invoice {data.invoice.id}: {data.invoice.status}")
    elif data.type == "transaction":
        print(f"Transaction {data.transaction.txid}: {data.transaction.usd} USD")


def on_rates(rates):
    """Handler for rate updates"""
    print(f"Rates updated: {len(rates)} rates")


# Using context manager ensures proper cleanup
with SocketClient(api_key="your_api_key") as client:
    client.set_on_notification(on_notification)
    client.set_on_rates(on_rates)
    input("Press Enter to exit...")


# Asynchronous WebSocket Client


async def async_on_notification(data: NotificationInvoice | NotificationTransaction):
    """Async handler for notifications"""
    if data.type == "invoice":
        print(f"Invoice {data.invoice.id}: {data.invoice.status}")
        # You can perform async operations here
        # await some_async_processing(data.invoice)
    elif data.type == "transaction":
        print(f"Transaction {data.transaction.txid}: {data.transaction.usd} USD")
        # await store_transaction(data.transaction)


async def async_on_rates(rates):
    """Async handler for rate updates"""
    print(f"Rates updated: {len(rates)} rates")


async def main():
    async with AsyncSocketClient(api_key="your_api_key") as client:
        client.set_on_notification(async_on_notification)
        client.set_on_rates(async_on_rates)
        await asyncio.sleep(60)  # Keep alive for 60 seconds


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Asynchronous WebSocket client stopped.")
