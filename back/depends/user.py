from django.contrib.auth.models import User
from fastapi import Depends, HTTPException
from fastapi_jwt_auth import AuthJWT
from jose import JWTError

from back.schemas.token import TokenData
from back.utils.exceptions import Credentials


def get_current_user(auth: AuthJWT = Depends()):
    try:
        username = auth.get_jwt_subject()
        if username is None:
            raise Credentials
        token_data = TokenData(username=username)
    except JWTError:
        raise Credentials
    try:
        user = User.objects.get(username=token_data.username)
    except User.DoesNotExist:
        raise Credentials
    return user


def get_current_active_user(current_user: User = Depends(get_current_user)):
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user
