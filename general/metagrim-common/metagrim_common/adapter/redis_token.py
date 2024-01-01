import typing

import inject
from metagrim_common.base.settings import CoreSettings
from metagrim_common.repository import RedisRepository


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
