from typing import Any, Dict, Optional
from fastapi import HTTPException, status


class DuplicatedError(HTTPException):
    def __init__(self, detail: Any = None, headers: Optional[Dict[str, Any]] = None):
        super().__init__(status.HTTP_400_BAD_REQUEST, detail, headers)


class NotFoundError(HTTPException):
    def __init__(self, detail: Any = None, headers: Optional[dict[str, Any]] = None):
        super().__init__(status.HTTP_404_NOT_FOUND, detail, headers)


class ServerError(HTTPException):
    def __init__(self, detail: Any = None, headers: Optional[dict[str, Any]] = None):
        super().__init__(status.HTTP_500_INTERNAL_SERVER_ERROR, detail, headers)


class AuthError(HTTPException):
    def __init__(self, detail: Any = None, headers: Optional[dict[str, Any]] = None):
        super().__init__(status.HTTP_401_UNAUTHORIZED, detail, headers)

