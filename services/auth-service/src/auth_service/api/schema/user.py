import typing

from metagrim_common.enums import UserStatusEnum
from metagrim_common.enums import UserTypeEnum
from metagrim_common.schema import BaseRequestSchema
from metagrim_common.schema import PaginationResponseSchema
from metagrim_common.schema import SearchPaginatedRequestSchema
from pydantic import BaseModel
from pydantic import Field
from pydantic import UUID4


class UserBase(BaseModel):
    """Base User with common fields."""

    email: str = None
    user_type: typing.Optional[UserTypeEnum] = Field(default=UserTypeEnum.ticket_agent)
    first_name: str
    last_name: str | None = None


class UserCreateSchema(BaseRequestSchema, UserBase):
    """Used to Create new User."""

    password: str


class UserUpdateSchema(BaseRequestSchema, UserBase):
    """Used to update user details."""

    status: str = Field(default=UserStatusEnum.inactive)


class UserReadSchema(UserBase):
    """Used to show the user details."""

    id: UUID4
    status: str = Field(default=UserStatusEnum.inactive)


class UserBriefSchema(UserReadSchema):
    """Used to list the user details."""

    pass


class UserTypeOptionsRequestSchema(BaseModel):
    user_type: str = Field(default=None)


class UserPaginationResponseSchema(PaginationResponseSchema):
    data: typing.List[UserBriefSchema] = Field(default_factory=list, title="User records")


class UserSearchPaginatedRequestSchema(SearchPaginatedRequestSchema):
    user_type: typing.Optional[UserTypeEnum] = Field(default=None, title="User type")
    status: typing.Optional[UserStatusEnum] = Field(default=None, title="User status")
