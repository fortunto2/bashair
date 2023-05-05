from django.contrib.auth.models import User
from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi_jwt_auth import AuthJWT
from fastapi_jwt_auth.exceptions import AuthJWTException

from back.utils.exceptions import Credentials, BaseHTTPException, NotFound


def get_current_user(auth: AuthJWT = Depends(), credentials: HTTPAuthorizationCredentials = Depends(HTTPBearer())):
    try:
        auth.jwt_required()
        username = auth.get_jwt_subject()
        if username is None:
            raise Credentials
    except AuthJWTException as e:
        print(e)
        raise HTTPException(status_code=e.status_code, detail=e.message)

    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        raise NotFound
    return user


def get_current_active_user(current_user: User = Depends(get_current_user)):
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user
