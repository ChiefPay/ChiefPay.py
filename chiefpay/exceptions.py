from enum import Enum
from typing import List, Optional


class ChiefPayErrorCode(Enum):
    INVALID_ARGUMENT = "INVALID_ARGUMENT"
    ALREADY_EXISTS = "ALREADY_EXISTS"
    NOT_FOUND = "NOT_FOUND"
    INTERNAL = "INTERNAL"
    OUT_OF_RANGE = "OUT_OF_RANGE"
    UNAUTHENTICATED = "UNAUTHENTICATED"
    PERMISSION_DENIED = "PERMISSION_DENIED"


class ChiefPayError(Exception):
    def __init__(self, message: str):
        self.message = message
        super().__init__(message)


class APIError(ChiefPayError):
    def __init__(
        self,
        message: Optional[str] = None,
        code: Optional[str] = None,
        errors: Optional[List[str]] = None,
        status_code: Optional[int] = None,
    ):
        self.code = (
            ChiefPayErrorCode(code) if code in ChiefPayErrorCode.__members__ else None
        )
        self.errors = errors or []
        self.status_code = status_code
        detail = f"Code: {self.code.value if self.code else 'Unknown'}, Errors: {self.errors}"
        super().__init__(detail)


class ManyRequestsError(ChiefPayError):
    def __init__(self):
        super().__init__("Too Many Requests", code="OUT_OF_RANGE")


class InvalidJSONError(ChiefPayError):
    def __init__(self, message: str = "Invalid JSON response"):
        super().__init__(message)


class TransportError(ChiefPayError):
    def __init__(self, status_code: int, message: str):
        self.status_code = status_code
        super().__init__(f"Transport Error: {status_code}: {message}")


class SocketError(ChiefPayError):
    def __init__(self, message: str):
        super().__init__(message)
