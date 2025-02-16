import aiohttp
import socketio

from .base import BaseSocketClient

class AsyncSocketClient(BaseSocketClient):
    def __init__(self, api_key: str):
        super().__init__(api_key)

        session = aiohttp.ClientSession(connector=aiohttp.TCPConnector(verify_ssl=False)) # Del

        self.sio = socketio.AsyncClient(http_session=session)
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
                self.URL,
                headers={"X-Api-Key": self.api_key},
                socketio_path=self.PATH,
            )
        except Exception as e:
            raise e

    async def disconnect(self):

        await self.sio.disconnect()