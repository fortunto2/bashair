from fastapi import FastAPI
from fastapi_jwt_auth import AuthJWT
from fastapi_jwt_auth.exceptions import AuthJWTException
from pydantic import BaseModel
from starlette.responses import JSONResponse

from back.models.deny_list import DenyList
from config import settings
from config.envs import envs

auth_handler = FastAPI()


class AuthJWTSettings(BaseModel):
    authjwt_secret_key: str = settings.SECRET_KEY
    authjwt_access_token_expires: int = envs.ACCESS_TOKEN_EXPIRE_MINUTES * 60
    authjwt_refresh_token_expires: int = envs.REFRESH_TOKEN_EXPIRE_MINUTES * 60
    authjwt_denylist_enabled: bool = False
    authjwt_denylist_token_checks: set = {"access", "refresh"}


@AuthJWT.load_config
def get_config():
    return AuthJWTSettings()


@auth_handler.exception_handler(AuthJWTException)
def authjwt_exception_handler(exc: AuthJWTException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.message}
    )


@AuthJWT.token_in_denylist_loader
def check_if_token_in_denylist(decrypted_token):
    jti = decrypted_token['jti']
    exists = DenyList.objects.filter(jti=jti).exists()
    return exists
