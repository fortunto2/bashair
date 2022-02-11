from fastapi import HTTPException


class NotFound(HTTPException):
    status_code = 404
    detail = 'Not found'
