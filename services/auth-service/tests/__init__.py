import sys
from os.path import abspath
from os.path import join

# Adjust the paths
sys.path.insert(0, abspath(join(__file__, "../", "../", "src/")))

from unittest.mock import create_autospec  # noqa:

import inject  # noqa

from sqlalchemy.orm import Session  # noqa

from auth_service.app.dependency import get_settings  # noqa
from metagrim_common.adapter.base import BaseBackend  # noqa
from metagrim_common.base.error_conf import ErrorConfig  # noqa
from metagrim_common.base.settings import CoreSettings  # noqa
from auth_service.service.unit_of_work import UnitOfWork  # noqa
from tests.mocked.redis_backend import MockedRedisBackend  # noqa
from tests.mocked.unit_of_work import MockedUnitOfWork  # noqa


def get_mocked_session():
    # get the Mocked SQLAlchemy session
    return create_autospec(Session)


def configure_injector(binder: inject.Binder):
    # bind instances
    settings = get_settings()
    settings.app_env = "PYTEST"
    binder.bind(CoreSettings, settings)
    binder.bind(BaseBackend, MockedRedisBackend())

    # Singleton Error configuration
    binder.bind_to_constructor(ErrorConfig, ErrorConfig)

    # Always return the new SQLAlchemy Session
    binder.bind_to_provider(UnitOfWork, MockedUnitOfWork)
    binder.bind_to_provider(Session, get_mocked_session)


# Configure the container for testing
inject.configure(configure_injector)
