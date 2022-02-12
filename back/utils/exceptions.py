from fastapi import HTTPException


class BaseHTTPException(HTTPException):
    def __init__(self):
        super().__init__(status_code=self.status_code, detail=self.detail)


class NotFound(BaseHTTPException):
    status_code = 404
    detail = 'Not found'
