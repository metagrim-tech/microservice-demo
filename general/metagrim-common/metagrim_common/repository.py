import typing

import inject
from auth_service import constants
from metagrim_common.adapter.base import AbstractRepository
from metagrim_common.adapter.base import BaseBackend
from metagrim_common.adapter.base import SqlAlchemyRepository
from metagrim_common.base.settings import CoreSettings
from metagrim_common.enums import UserStatusEnum
from metagrim_common.model import UserActionModel
from metagrim_common.model import UserModel
from metagrim_common.model.base import CoreModel
from metagrim_common.model.types.uuid import UUID
from pydantic import UUID4
from sqlalchemy import func
from sqlalchemy import or_


class UserSqlAlchemyRepository(SqlAlchemyRepository):
    model: typing.Type[UserModel] = UserModel
    search_fields = [UserModel.first_name, UserModel.last_name, UserModel.email]

    async def find_by_email(self, email):
        return self.session.query(self.model).filter_by(email=email).first()

    async def check_user_exists(self, email: str = None, mobile: str = None, id_: UUID | None = None) -> bool:
        query = self.session.query(func.count(self.model.id))
        if mobile and email:
            query = query.filter(or_(self.model.mobile == mobile, self.model.email == email))
        else:
            if mobile:
                query = query.filter_by(mobile=mobile)
            if email:
                query = query.filter_by(email=email)
        if id_:
            query = query.filter(self.model.id != id_)
        rec = query.scalar()
        return bool(rec)

    async def filter_users_by_user_type(self, user_type: str = None) -> list:
        query = self.session.query(
            self.model.id, self.model.first_name, self.model.last_name, self.model.user_type, self.model.status
        )
        if user_type:
            rec = query.filter(self.model.user_type == user_type).all()

        else:
            rec = []

        return [
            {
                "key": user.id,
                "label": f"{user.first_name} {user.last_name} - Inactive"
                if user.status != UserStatusEnum.active
                else f"{user.first_name} {user.last_name}",
                "value": user.id,
            }
            for user in rec
        ]

    async def is_user_active(self, user_id: UUID4 = None) -> bool:
        user_status = False
        query = self.session.query(self.model.id, self.model.status)
        if user_id:
            ticket_agent_rec = query.filter(self.model.id == user_id).first()
            if ticket_agent_rec.status == UserStatusEnum.active:
                user_status = True
        return user_status

    async def get_user_info(self, user_id: UUID4 = None) -> dict:
        user = {}
        query = self.session.query(self.model.id, self.model.first_name, self.model.last_name)
        if user_id:
            rec = query.filter(self.model.id == user_id)
            user = rec.first()
        return user


class UserActionsSqlAlchemyRepository(SqlAlchemyRepository):
    model: typing.Type[UserActionModel] = UserActionModel
    search_fields = []

    async def add_user_action(self, user_id: UUID, actions: typing.List[str]):
        for action in actions:
            model = UserActionModel()
            model.user_id = user_id
            model.action = action
            await self.add(model)

    async def remove_user_action(self, user_id: UUID, actions: typing.List[str]):
        self.session.query(self.model).filter(self.model.user_id == user_id, self.model.action.in_(actions)).delete()


class RedisRepository(AbstractRepository):
    @inject.autoparams("backend")
    def __init__(self, backend: BaseBackend):
        self.backend: BaseBackend = backend

    def _add(self, key: str, data: typing.Union[dict, list, str], **kwargs):
        if type(data) == dict:
            self.backend.set_dict(key, data, **kwargs)
        elif type(data) == list:
            self.backend.set_list(key, data, **kwargs)
        elif type(data) == str:
            self.backend.set_str(key, data, **kwargs)
        else:
            raise NotImplemented(f"Unable to save the {type(data)!r}")

    def add(self, model: CoreModel):
        self._add(str(model.id), {c: getattr(self, c) for c in model.__table__.columns})

    def get(self, uuid: str) -> typing.Union[dict, str, list, None]:
        return self.backend.get_dict(uuid)

    def update(self, data: dict, where: dict):
        raise NotImplemented("Cannot implement update record for RedisRepository")


class TokenRedisRepository(RedisRepository):
    def __init__(self, *args, **kwargs):
        settings = inject.instance(CoreSettings)
        self.token_time_exp = settings.access_token_expire_minutes * 60
        super(TokenRedisRepository, self).__init__(*args, **kwargs)

    def add_token(self, uuid, token_data):
        self._add(uuid, token_data, ex=self.token_time_exp)

    def get_token(self, uuid) -> typing.Optional[dict]:
        return self.backend.get_dict(uuid)

    def delete(self, uuid):
        self.backend.delete(uuid)
