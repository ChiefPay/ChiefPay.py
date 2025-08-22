import socketio
from typing import Callable, Any
from chiefpay.constants import BASE_URL
from chiefpay.exceptions import SocketError
from chiefpay.socket.base import BaseSocketClient


class SocketClient(BaseSocketClient):
    """
    Client for interacting with the payment system via WebSockets (synchronous).
    """

    def __init__(self, api_key: str, base_url: str = BASE_URL):
        super().__init__(api_key, base_url)
        self.sio = socketio.Client()
        self._setup_event_handlers()

    def _setup_event_handlers(self):
        @self.sio.event
        def connect():
            print("Connected to Socket.IO server")

        @self.sio.event
        def disconnect():
            print("Disconnected from Socket.IO server")

        @self.sio.event
        def connect_error(data):
            if data and "Too many connections!" in str(data):
                self._too_many_connections = True
            elif data and "Wrong api key" in str(data):
                self._invalid_api_key = True

        @self.sio.event
        def rates(data: dict):
            self.rates = data
            if self.on_rates:
                self.on_rates(data)

        @self.sio.event
        def notification(data: dict):
            try:
                if self.on_notification:
                    data = self._convert_to_dto(data)
                    self.on_notification(data)
                    return {"status": "success"}
            except Exception as e:
                print(f"Error processing notification: {e}")
                return {"status": "error"}

    def connect(self):
        """
        Connects to the Socket.IO server.

        Raises:
            SocketError: If the connection fails.
        """
        try:
            self.sio.connect(
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

    def disconnect(self):
        """
        Disconnects from the Socket.IO server.
        """
        self.sio.disconnect()

    def emit(
        self, event: str, data: Any = None, callback: Callable[[Any], None] = None
    ):
        """
        Sends an event to the server with optional data and an acknowledgment callback.

        Args:
            event (str): The name of the event to emit.
            data (Any, optional): The data to send with the event.
            callback (Callable[[Any], None], optional): A function to handle the server's acknowledgment.
        """
        try:
            self.sio.emit(event, data, callback=callback)
        except Exception as e:
            raise SocketError(f"Failed to emit event '{event}': {e}")

    def __enter__(self):
        self.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.disconnect()
