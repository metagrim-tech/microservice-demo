from typing import Any
from typing import Dict

from metagrim_common.adapter.redis_backend import RedisBackend


class MockedRedisConnection:
    """Mocked Redis Connection Class"""

    store: Dict[str, Any]

    def __init__(self):
        self.store = {}

    def set(self, key, value, **kwargs):
        self.store[key] = value

    def get(self, key, **kwargs):
        self.store.get(key)


class MockedRedisBackend(RedisBackend):
    """Mocked RedisBackend class.

    Note:
        This has to be overriden as we are not injecting the dependency of the Redis connection separately.
        @todo: Find the better way to mock this backend
    """

    def __init__(self):
        # Instantiate the mocked Redis connection here
        self.conn = MockedRedisConnection()
