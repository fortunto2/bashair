from typing import Union

from django.contrib.auth.hashers import check_password, make_password
from django.contrib.auth.models import User
from fastapi import HTTPException, Depends, APIRouter, Body
from fastapi.security import OAuth2PasswordRequestForm
from fastapi_jwt_auth import AuthJWT
from starlette import status
from starlette.responses import Response

from back.depends.user import get_current_active_user
from back.models.deny_list import DenyList
from back.schemas.token import TokenGet
from back.schemas.user import UserCreate

router = APIRouter(tags=["auth"], prefix="/auth")


def denylist_add(decrypted_token):
    if decrypted_token is not None:
        jti = decrypted_token['jti']
        DenyList.objects.create({'jti': jti})


def verify_password(plain_password, hashed_password):
    return check_password(plain_password, hashed_password)


def authenticate_user(username: str, password: str) -> Union[User, bool]:
    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        return False
    if not verify_password(password, user.password):
        return False
    return user


@router.post("/token/", response_model=TokenGet)
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), auth: AuthJWT = Depends()):
    denylist_add(auth.get_raw_jwt())
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = auth.create_access_token(subject=user.username)
    refresh_token = auth.create_refresh_token(subject=user.username)
    return {"access_token": access_token, "refresh_token": refresh_token, "token_type": "Bearer", "ttl": auth._access_token_expires * 1000}


@router.post("/token/refresh/", response_model=TokenGet)
def refresh_access_token(auth: AuthJWT = Depends()):
    auth.jwt_refresh_token_required()
    denylist_add(auth.get_raw_jwt())
    current_user = auth.get_jwt_subject()
    access_token = auth.create_access_token(subject=current_user)
    refresh_token = auth.create_refresh_token(subject=current_user)
    return {"access_token": access_token, "refresh_token": refresh_token, "token_type": "Bearer", "ttl": auth._access_token_expires * 1000}


@router.post("/register/", response_model=TokenGet)
def create_user(user: UserCreate, auth: AuthJWT = Depends()):
    exists = User.objects.filter(username=user.username).exists()
    if exists:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already exists",
        )
    if not user.username or not user.password or not user.email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username, password and email required",
        )
    password = user.password
    user = User(**user.dict())
    user.set_password(password)
    user.save()
    access_token = auth.create_access_token(subject=user.username)
    refresh_token = auth.create_refresh_token(subject=user.username)
    return {"access_token": access_token, "refresh_token": refresh_token, "token_type": "Bearer", "ttl": auth._access_token_expires * 1000}


@router.post("/change_password/")
def change_password(new_password: str = Body(...), current_password: str = Body(...), current_user: User = Depends(get_current_active_user)):
    if not verify_password(current_password, current_user.password):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Wrong current password",
        )
    current_user.set_password(new_password)
    current_user.save()
    return Response()
