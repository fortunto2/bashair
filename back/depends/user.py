from django.contrib.auth.models import User
from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi_jwt_auth import AuthJWT
from jose import JWTError

from back.utils.exceptions import Credentials


def get_current_user(auth: AuthJWT = Depends(), credentials: HTTPAuthorizationCredentials = Depends(HTTPBearer())):
    try:
        username = auth.get_jwt_subject()
        if username is None:
            raise Credentials
    except JWTError:
        raise Credentials
    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        raise Credentials
    return user


def get_current_active_user(current_user: User = Depends(get_current_user)):
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user
