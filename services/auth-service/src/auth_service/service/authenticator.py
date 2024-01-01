import logging

import inject
from auth_service import constants
from auth_service.api.schema.login import AuthResponse
from auth_service.service.unit_of_work import UnitOfWork
from metagrim_common.base.error import ApplicationError
from metagrim_common.base.settings import CoreSettings
from metagrim_common.base.utils import create_access_token
from metagrim_common.base.utils import verify_password
from metagrim_common.domains import User
from metagrim_common.enums import UserStatusEnum
from metagrim_common.schema import JWTUser
from metagrim_common.service.base import BaseService

logger = logging.getLogger(__name__)


class AuthenticatorService(BaseService):
    @inject.autoparams("uow")
    def __init__(self, uow: UnitOfWork, current_user_id: str | None = None):
        super(AuthenticatorService, self).__init__(current_user_id=current_user_id)
        self.uow: UnitOfWork = uow
        self.uow.current_user_id = current_user_id
        self.settings: CoreSettings = inject.get_injector().get_instance(CoreSettings)

    async def verify_password(self, email: str, password: str) -> AuthResponse:
        async with self.uow:
            user = await self.uow.users.find_by_email(email)
            if not user:
                raise ApplicationError(response_code=constants.USER_NOT_REGISTERED, message="User does not exists")
            elif user.status == UserStatusEnum.inactive:
                raise ApplicationError(
                    response_code=constants.USER_IS_NOT_AUTHORIZED, message="User account is currently deactivated"
                )

            if user and verify_password(password, user.password_hash):
                access = {}
                # Update this code to pull actions from user_actions table
                user_domain = User.model_validate(user)
                scopes = user_domain.user_actions
                data = JWTUser(
                    id=str(user.id),
                    email=user.email,
                    user_type=user.user_type,
                    name=user.name,
                    scopes=scopes,
                    sub=str(user.id),
                ).model_dump()

                access["token"] = create_access_token(data)
                access["t_type"] = "access"
                access["user_id"] = str(user.id)
                access["is_revoked"] = False
                self.uow.tokens.add_token(str(user.id), access)
                return AuthResponse(
                    email=user.email,
                    mobile=user.mobile,
                    access_token=access.get("token"),
                    id=user.id,
                    user_type=user.user_type,
                    first_name=user.first_name,
                    last_name=user.last_name,
                )

            raise ApplicationError(response_code=constants.HTTP_401_UNAUTHORIZED, message="User password is wrong")

    async def logout(self) -> None:
        """
        :return:
        """
        async with self.uow:
            self.uow.tokens.delete(self.current_user_id)
