from auth_service import constants
from auth_service.api.schema import login
from auth_service.service.authenticator import AuthenticatorService
from auth_service.service.user import UserService
from fastapi import Depends
from fastapi import Form
from fastapi.responses import JSONResponse
from metagrim_common.base.deps import get_authorised_user
from metagrim_common.base.router import APIRouter
from metagrim_common.base.utils import respond
from metagrim_common.schema import ResponseSchema
from starlette.requests import Request

from .schema import user

router = APIRouter(tags=["Authentication"])


@router.post("/auth", response_model=login.AuthResponse)
async def login_request(user_login: login.AuthRequest) -> login.AuthResponse:
    service = AuthenticatorService()
    return await service.verify_password(user_login.email, password=user_login.password)


@router.delete("/auth", response_model=ResponseSchema)
async def logout_request(current_user_id: str = Depends(get_authorised_user)) -> JSONResponse:
    service = AuthenticatorService(current_user_id=current_user_id)
    await service.logout()
    return respond(constants.RESPONSE_OK, message="Logged out successfully")


@router.post("/token", response_model=login.AuthResponse, include_in_schema=True)
async def get_token(username: str = Form(), password: str = Form()) -> login.AuthResponse:
    """
    This API is used by OpenAPI specification only, not meant to be used by the other users
    :param username:
    :param password:
    :return:
    """
    service = AuthenticatorService()
    return await service.verify_password(username, password)


@router.get("/me", response_model=user.UserReadSchema)
async def me_service(current_user_id: str = Depends(get_authorised_user)):
    service = UserService(current_user_id=current_user_id)
    user = await service.get_user(current_user_id)
    return user


@router.get("/sso/login")
async def sso_login(request: Request):
    """Generate login url and redirect"""
    service = AuthenticatorService()
    return await service.sso_login(redirect_url=request.url_for("sso_callback"))


@router.get("/sso/callback")
async def sso_callback(request: Request):
    """Process login response from Google and return user info"""
    service = AuthenticatorService()
    return await service.sso_callback(request=request)
