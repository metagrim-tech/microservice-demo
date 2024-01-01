import typing

from fastapi import APIRouter as _APIRouter


class APIRouter(_APIRouter):
    """Wraper class over fastapi.APIRouer
    to track the routers instantiated in whole application
    """

    # Track all instantiated routes
    _routes: typing.List[_APIRouter] = []

    def __init__(self, *args, **kwargs) -> None:
        super(APIRouter, self).__init__(*args, **kwargs)
        self.append(self)

    @classmethod
    def append(cls, route: _APIRouter) -> None:
        cls._routes.append(route)

    @classmethod
    def get_routes(cls) -> typing.List[_APIRouter]:
        return cls._routes

    def __len__(self) -> int:
        return len(self._routes)
