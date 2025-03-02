import asyncio
from chiefpay import SocketClient, AsyncSocketClient

# Notification handler
def on_notification(data):
    print("New notification received:", data)

# Rates update handler
def on_rates(data):
    print("Rates updated:", data)

# Synchronous WebSocket client
with SocketClient(api_key="your_api_key") as socket_client:
    socket_client.set_on_notification(on_notification)
    socket_client.set_on_rates(on_rates)
    print("Synchronous WebSocket client started. Waiting for events...")

# Asynchronous WebSocket client
async def main():
    async with AsyncSocketClient(api_key="your_api_key") as socket_client:
        socket_client.set_on_notification(on_notification)
        socket_client.set_on_rates(on_rates)
        print("Asynchronous WebSocket client started. Waiting for events...")
        await asyncio.sleep(60)  # Wait for 60 seconds

# Run the async WebSocket client
if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Asynchronous WebSocket client stopped.")