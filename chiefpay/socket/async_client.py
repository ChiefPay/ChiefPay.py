import socketio

from chiefpay.constants import BASE_URL
from chiefpay.exceptions import SocketError
from chiefpay.socket.base import BaseSocketClient

class AsyncSocketClient(BaseSocketClient):
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

        @self.sio.event
        async def notification(data):
            self.notifications.append(data)

    async def connect(self):
        try:
            await self.sio.connect(
                self.base_url,
                headers={"X-Api-Key": self.api_key},
                socketio_path=self.PATH,
            )
        except Exception as e:
            raise SocketError(f"Failed to connect to Socket.IO server: {e}")

    async def disconnect(self):
        await self.sio.disconnect()