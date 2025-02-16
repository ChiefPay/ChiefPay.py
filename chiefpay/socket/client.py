import requests
import socketio

from chiefpay.socket.base import BaseSocketClient


class SocketClient(BaseSocketClient):
    def __init__(self, api_key: str):
        super().__init__(api_key)

        http_session = requests.Session()  # Del
        http_session.verify = False  # Del

        self.sio = socketio.Client(http_session=http_session)
        self._setup_event_handlers()

    def _setup_event_handlers(self):
        @self.sio.event
        def connect():
            print("Connected to Socket.IO server")

        @self.sio.event
        def disconnect():
            print("Disconnected from Socket.IO server")

        @self.sio.event
        def rates(data):
            self.rates = data

        @self.sio.event
        def notification(data):
            self.notifications.append(data)

    def connect(self):
        try:
            self.sio.connect(
                self.URL, headers={"X-Api-Key": self.api_key}, socketio_path=self.PATH
            )
        except Exception as e:
            raise e

    def disconnect(self):
        self.sio.disconnect()
