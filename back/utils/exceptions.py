from fastapi import HTTPException
from starlette import status


class BaseHTTPException(HTTPException):
    headers = None

    def __init__(self):
        super().__init__(status_code=self.status_code, detail=self.detail, headers=self.headers)


class NotFound(BaseHTTPException):
    status_code = status.HTTP_404_NOT_FOUND
    detail = 'Not found'


class Credentials(BaseHTTPException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Could not validate credentials"
    headers = {"WWW-Authenticate": "Bearer"}
