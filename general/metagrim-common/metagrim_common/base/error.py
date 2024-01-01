import inject
from metagrim_common.base import constants
from metagrim_common.base.error_conf import ErrorConfig
from metagrim_common.enums import ResponseTypeEnum

# Define the Error Codes For the Exceptions


class BaseError(Exception):

    include_trace: bool = False

    def __init__(
        self,
        message: str,
        response_code: int,
        headers: dict = None,
        response_type: ResponseTypeEnum = ResponseTypeEnum.error,
        http_code: int = constants.HTTP_500_INTERNAL_SERVER_ERROR,
    ) -> None:
        self.response_code = response_code
        self.response_type = response_type
        self.http_code = http_code
        self.message = message
        self.headers = headers
        args = (response_code, message)
        super(BaseError, self).__init__(*args)

    def __str__(self) -> str:
        return f"{self.message}"

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.message!r}, {self.response_code})"


class ApplicationError(BaseError):
    @inject.autoparams("msg_conf")
    def __init__(
        self,
        response_code: int,
        msg_conf: ErrorConfig,
        headers: dict = None,
        message: str = None,
        include_trace: bool = False,
    ):
        msg = msg_conf.get(response_code)
        self.include_trace = include_trace
        if not msg:
            msg = {
                "response_code": response_code,
                "response_type": ResponseTypeEnum.error,
                "message": message or f"Undefined error code {response_code!r}",
                "http_code": response_code,
            }

        if headers:
            msg["headers"] = headers
        if message:
            msg["message"] = message
        super(ApplicationError, self).__init__(**msg)


class InternalServerError(BaseError):
    include_trace = True

    def __init__(self, response_code=constants.HTTP_500_INTERNAL_SERVER_ERROR, message="", headers=None):
        super(InternalServerError, self).__init__(message=message, response_code=response_code, headers=headers)


class JWTTokenError(BaseError):
    """JWT Token Signature invalid."""

    def __init__(self, response_code=constants.JWT_TOKEN_SIGNATURE_INVALID, message="", headers=None):
        super(JWTTokenError, self).__init__(message=message, response_code=response_code, headers=headers)


class JWTTokenExpiredError(BaseError):
    """JWT Token Expired."""

    def __init__(self, response_code=constants.JWT_TOKEN_SIGNATURE_EXPIRED, message="", headers=None):
        super(JWTTokenExpiredError, self).__init__(message=message, response_code=response_code, headers=headers)


class JWTTokenMissingError(BaseError):
    """JWT Token Not present."""

    def __init__(self, response_code=constants.JWT_TOKEN_MISSING, message="", headers=None):
        super(JWTTokenMissingError, self).__init__(message=message, response_code=response_code, headers=headers)
