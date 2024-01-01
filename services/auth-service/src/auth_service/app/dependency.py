import logging
from functools import lru_cache

import inject
from auth_service.error_conf import ErrorConfig
from auth_service.service.unit_of_work import UnitOfWork
from auth_service.settings import Settings
from metagrim_common.adapter.base import BaseBackend
from metagrim_common.adapter.redis_backend import RedisBackend
from metagrim_common.base.settings import CoreSettings
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session

logger = logging.getLogger(__name__)


@lru_cache
def get_settings():
    return Settings()


def sql_alchemy_session_factory() -> sessionmaker:
    """ "
    SQLAlchemy Session Maker
    """
    settings = get_settings()
    engine = create_engine(settings.sqlalchemy_uri)
    logger.info("Initializing SQLAlchemy Session Maker")
    return sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_backend() -> BaseBackend:
    """
    Gets the object store Backend
    :return:
    """
    logger.info("Initializing Redis Backend")
    settings = get_settings()
    try:
        backend = RedisBackend(
            host=settings.redis_host,
            port=settings.redis_port,
            password=settings.redis_pass,
            username=settings.redis_user,
        )
    except Exception as ex:
        logger.fatal(f"Unable to instantiate RedisBackend with Exception {ex}", exc_info=True)
        backend = BaseBackend()

    return backend


def configure_dependency(binder: inject.Binder):
    # bind instances
    binder.bind(CoreSettings, get_settings())
    binder.bind(BaseBackend, get_backend())

    # Singleton Error configuration
    binder.bind_to_constructor(ErrorConfig, ErrorConfig)

    # Always return the new SQLAlchemy Session
    binder.bind_to_provider(Session, sql_alchemy_session_factory())
    binder.bind_to_provider(UnitOfWork, UnitOfWork)
