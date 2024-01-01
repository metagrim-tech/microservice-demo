import typing

from metagrim_common.enums import UserTypeEnum
from metagrim_common.schema import BaseRequestSchema
from pydantic import UUID4


class AuthRequest(BaseRequestSchema):
    email: str
    password: str


class AuthResponse(BaseRequestSchema):
    id: UUID4
    email: typing.Optional[str] = None
    mobile: typing.Optional[str] = None
    access_token: str
    user_type: UserTypeEnum
    first_name: str | None = None
    last_name: str | None = None
