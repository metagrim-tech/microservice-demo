import typing

import inject
from auth_service.settings import Settings
from metagrim_common.base.settings import CoreSettings

from .dependency import configure_dependency

# Configure the Dependencies for the Application
inject.configure(configure_dependency)


def init_app():
    # Loading apps
    from auth_service.api.login import router as auth_ends
    from auth_service.api.user import router as user_ends
    from metagrim_common.base.bootstrap import create_app

    api_ = create_app(typing.cast(Settings, inject.instance(CoreSettings)))
    return api_


# Create the FAST API app
api = init_app()
