import socketio

from chiefpay.constants import BASE_URL
from chiefpay.exceptions import SocketError
from chiefpay.socket.base import BaseSocketClient


class AsyncSocketClient(BaseSocketClient):
    """
    Client for interacting with the payment system via WebSockets (asynchronous).
    """
    def __init__(self, api_key: str, base_url: str = BASE_URL):
        super().__init__(api_key, base_url)
        self.sio = socketio.AsyncClient()
        self._setup_event_handlers()

    def _setup_event_handlers(self):
        @self.sio.event
        async def connect():
            print("Connected to Socket.IO server")

        @self.sio.event
        async def disconnect():
            print("Disconnected from Socket.IO server")

        @self.sio.event
        async def rates(data):
            self.rates = data
            if self.on_rates:
                await self.on_rates(data)

        @self.sio.event
        async def notification(data):
            if self.on_notification:
                await self.on_notification(data)

    async def connect(self):
        """
        Asynchronously connects to the Socket.IO server.

        Raises:
            SocketError: If the connection fails.
        """
        try:
            await self.sio.connect(
                self.base_url,
                headers={"X-Api-Key": self.api_key},
                socketio_path=self.PATH,
            )
        except Exception as e:
            raise SocketError(f"Failed to connect to Socket.IO server: {e}")

    async def disconnect(self):
        """
        Asynchronously disconnects from the Socket.IO server.
        """
        await self.sio.disconnect()


    async def __aenter__(self):
        await self.connect()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.disconnect()