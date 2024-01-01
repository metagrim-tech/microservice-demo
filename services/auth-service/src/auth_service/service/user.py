import typing
from typing import Any
from typing import Dict

import inject
from auth_service import constants
from auth_service.service.unit_of_work import UnitOfWork
from metagrim_common.base.error import ApplicationError
from metagrim_common.domains import SearchPaginatedParameters
from metagrim_common.domains import User
from metagrim_common.enums import UserStatusEnum
from metagrim_common.service.base import BaseService
from pydantic import UUID4


class UserService(BaseService):
    @inject.autoparams("uow")
    def __init__(self, uow: UnitOfWork, current_user_id: str = None):
        """
        Initialise the User Service
        :param uow:
        :param current_user_id:
        """
        super(UserService, self).__init__(current_user_id=current_user_id)
        self.uow: UnitOfWork = uow
        self.uow.current_user_id = current_user_id

    async def list_users(self, paginate: SearchPaginatedParameters) -> Dict[str, Any]:
        """
        List Users
        :param paginate:
        :return:
        """
        result = []
        async with self.uow:
            paginated = await self.uow.users.get_paginated_result(
                **paginate.model_dump(exclude_none=True),
                excluded_ids=[self.uow.current_user_id],  # Excluding logged in user from the listing & search
            )
            for item in paginated.get("data", []) or []:
                result.append(User.model_validate(item).model_dump())
            paginated["data"] = result
        return paginated

    async def create_user(self, user: User, requested_actions: typing.List[str]):
        """
        Create new User
        :param user:
        :param requested_actions:
        :return:
        """
        async with self.uow:
            if await self.uow.users.check_user_exists(email=user.email):
                raise ApplicationError(
                    response_code=constants.HTTP_409_CONFLICT, message="User already exists with Email"
                )
            new_user = await self.uow.users.add(user.model_dump(exclude_none=True, exclude_related=True))
            user = User.model_validate(new_user)

            self.uow.commit()
            return user

    async def update_user(self, user: User, requested_actions: typing.List[str] | None) -> User:
        """
        Update User details
        :param user:
        :param requested_actions:
        :return:
        """
        async with self.uow:
            record = await self.uow.users.get(user.id)
            if await self.uow.users.check_user_exists(email=user.email, mobile=user.mobile, id_=user.id):
                raise ApplicationError(
                    response_code=constants.HTTP_409_CONFLICT, message="User already exists with Email or Mobile."
                )
            user_rec = User.model_validate(record)
            user_rec = user_rec + user.model_dump(exclude_unset=True, exclude_related=True)
            data = user_rec.model_dump(exclude_unset=True, exclude_related=True)
            await self.uow.users.update_by(values=data, where={"id": user.id})

            if requested_actions:
                allowed_actions = user_rec.user_actions
                user_actions_to_add = list(set(requested_actions) - set(allowed_actions))
                user_actions_to_remove = list(set(allowed_actions) - set(requested_actions))
                if user_actions_to_add:
                    # Add the user action
                    await self.uow.user_actions.add_user_action(user_id=user.id, actions=user_actions_to_add)
                if user_actions_to_remove:
                    # Add the user remove
                    await self.uow.user_actions.remove_user_action(user_id=user.id, actions=user_actions_to_remove)

            self.uow.commit()
            # Get Updated values
            self.uow.users.refresh(record)
            user_rec = User.model_validate(record)
            return user_rec

    async def get_user(self, user_id: UUID4) -> User:
        """
        Retrive user details with given User ID
        :param user_id:
        :return:
        """
        async with self.uow:
            record = await self.uow.users.get(user_id)
            if record:
                return User.model_validate(record)
            else:
                raise ApplicationError(response_code=constants.HTTP_404_NOT_FOUND, message="User not found")

    async def delete_user(self, user_id: UUID4) -> None:
        """
        Delete the user
        :param user_id:
        :return:
        """
        async with self.uow:
            record = await self.uow.users.get(user_id)
            if not record:
                raise ApplicationError(response_code=constants.HTTP_404_NOT_FOUND, message="User not found")
            else:
                await self.uow.users.delete(user_id)
                self.uow.commit()

    async def change_user_status(self, user_id: UUID4) -> User:
        """
        Toggle User Status
        from Active to Inactive or Inactive to Active
        :param user_id:
        :return:
        """
        async with self.uow:
            record = await self.uow.users.get(user_id)
            if not record:
                raise ApplicationError(response_code=constants.HTTP_404_NOT_FOUND, message="User not found")
            record = User.model_validate(record)
            if record.status == UserStatusEnum.active:
                await self.uow.users.update_by(values={"status": UserStatusEnum.inactive}, where={"id": user_id})
            else:
                await self.uow.users.update_by(values={"status": UserStatusEnum.active}, where={"id": user_id})
            self.uow.commit()
            return record
