import socketio
from typing import Callable, Any
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
        async def connect_error(data):
            if data and "Too many connections!" in str(data):
                self._too_many_connections = True
            elif data and "Wrong api key" in str(data):
                self._invalid_api_key = True

        @self.sio.event
        async def rates(data: dict):
            self.rates = data
            if self.on_rates:
                await self.on_rates(data)

        @self.sio.event
        async def notification(data: dict):
            try:
                if self.on_notification:
                    data = self._convert_to_dto(data)
                    await self.on_notification(data)
                    return {"status": "success"}
            except Exception as e:
                print(f"Error processing notification: {e}")
                return {"status": "error"}

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
            if self._too_many_connections:
                raise SocketError("Too many connections!")
            if self._invalid_api_key:
                raise SocketError("Invalid API key provided.")
            raise SocketError(f"Failed to connect to Socket.IO server: {e}")

    async def disconnect(self):
        """
        Asynchronously disconnects from the Socket.IO server.
        """
        await self.sio.disconnect()

    async def emit(
        self, event: str, data: Any = None, callback: Callable[[Any], None] = None
    ):
        """
        Asynchronously sends an event to the server with optional data and an acknowledgment callback.

        Args:
            event (str): The name of the event to emit.
            data (Any, optional): The data to send with the event.
            callback (Callable[[Any], None], optional): A function to handle the server's acknowledgment.
        """
        try:
            await self.sio.emit(event, data, callback=callback)
        except Exception as e:
            raise SocketError(f"Failed to emit event '{event}': {e}")

    async def __aenter__(self):
        await self.connect()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.disconnect()
