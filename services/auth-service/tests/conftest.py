"""UNIT TESTS CONFIGURATION FILE

This file contains all the fixtures and repeated mocks that are used in
the unit tests.

Useful documentation:
- https://stackoverflow.com/questions/43358802/pytest-mock-mocker-in-pytest-fixture
- https://openbase.com/python/pytest-mock/documentation#usage
- https://www.youtube.com/watch?v=lidTnXTFssM
"""
import pytest
from auth_service.service.unit_of_work import UnitOfWork
from metagrim_common.model.base import Base


@pytest.fixture(scope="function")
def sqlalchemy_declarative_base():
    return Base


@pytest.fixture(scope="function")
def sqlalchemy_mock_config():
    # Configure here the database records for testing
    return [
        (
            "gc_user",  # Table name to add the records
            [
                {
                    "id": "39b31cae-433d-47bb-9172-c305ef873530",
                    # "created_at": "2023-10-30 22:32:00.564655",
                    # "updated_at": "2023-09-01 00:00:00",
                    "is_deleted": False,
                    "created_by": "aaa125e6-fec5-43ce-88eb-891739c3ca7e",
                    # "updated_by": "2",
                    "email": "first.user@gc.com",
                    "mobile": "9999999999",
                    "password_hash": "$2b$12$iXS8TFkM4Yn8AJK/.WtyfeBmVEVEbGyglaFbR01E3DCe3I/xeT5DC",
                    "user_type": "TICKET_AGENT",
                    "first_name": "First",
                    "last_name": "User",
                    "status": "ACTIVE",
                },
                {
                    "id": "aaa125e6-fec5-43ce-88eb-891739c3ca7e",
                    # "created_at": "2023-09-01 00:00:00",
                    # "updated_at": "2023-09-01 00:00:00",
                    "is_deleted": False,
                    "created_by": "aaa125e6-fec5-43ce-88eb-891739c3ca7e",
                    # "updated_by": "2",
                    "email": "second.user@gc.com",
                    "mobile": "9999999988",
                    "password_hash": "$2b$12$iXS8TFkM4Yn8AJK/.WtyfeBmVEVEbGyglaFbR01E3DCe3I/xeT5DC",
                    "user_type": "TICKET_AGENT",
                    "first_name": "First",
                    "last_name": "User",
                    "status": "ACTIVE",
                },
                {
                    "id": "bbb125e6-fec5-43ce-88eb-891739c3ca7e",
                    # "created_at": "2023-09-01 00:00:00",
                    # "updated_at": "2023-09-01 00:00:00",
                    "is_deleted": False,
                    "created_by": "aaa125e6-fec5-43ce-88eb-891739c3ca7e",
                    # "updated_by": "2",
                    "email": "inactive.user@gc.com",
                    "mobile": "9999997788",
                    "password_hash": "$2b$12$iXS8TFkM4Yn8AJK/.WtyfeBmVEVEbGyglaFbR01E3DCe3I/xeT5DC",
                    "user_type": "TICKET_AGENT",
                    "first_name": "Inactive",
                    "last_name": "User",
                    "status": "INACTIVE",
                },
            ],
        )
    ]


@pytest.fixture(scope="function")
def mocked_uow(mocked_session):
    # Use the Mocked Unit of work with the SQLAlchemy session configured with above data
    return UnitOfWork(session=mocked_session)
