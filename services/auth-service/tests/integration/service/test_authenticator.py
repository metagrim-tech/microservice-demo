from typing import Any
from typing import Type

import pytest
from auth_service.api.schema.login import AuthResponse
from auth_service.service.authenticator import AuthenticatorService
from metagrim_common.base.error import ApplicationError


@pytest.mark.integration
@pytest.mark.parametrize(
    ("email", "password", "expected_result"),
    [
        ("first.user@gc.com", "admin@123", AuthResponse),  # Valid user with valid password
        ("first.user@gc.com", "wrong_pass", ApplicationError),  # Valid user with wrong password
        ("no.user@gc.com", "admin@123", ApplicationError),  # No user
        ("inactive.user@gc.com", "admin@123", ApplicationError),  # Inactive user with correct password
    ],
)
async def test_verify_password(email, password, expected_result: Type[Exception] | Any):
    service = AuthenticatorService()
    expected_class_ = expected_result if isinstance(expected_result, type) else type(expected_result)
    if issubclass(expected_class_, Exception):
        with pytest.raises(expected_result):
            await service.verify_password(email, password)
    else:
        result = await service.verify_password(email, password)
        assert type(result) == expected_class_
