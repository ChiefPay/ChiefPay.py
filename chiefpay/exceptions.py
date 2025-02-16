class ChiefPayError(Exception):
    pass


class HTTPError(ChiefPayError):
    def __init__(self, status_code: int, message: str):
        self.status_code = status_code
        self.message = message
        super().__init__(f"HTTP Error: {status_code}: {message}")


class APIError(ChiefPayError):
    pass


class SocketError(ChiefPayError):
    pass