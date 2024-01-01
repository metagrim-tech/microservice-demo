from metagrim_common.base.constants import *

USER_IS_NOT_AUTHORIZED = HTTP_403_FORBIDDEN  # type: ignore [name-defined]
RECORD_NOT_FOUND = HTTP_404_NOT_FOUND  # type: ignore [name-defined]
MISSING_DATA = HTTP_422_UNPROCESSABLE_ENTITY  # type: ignore [name-defined]
USER_TOKEN_ERROR = 452
USER_TOKEN_EXPIRED = 453
USER_TOKEN_INVALID = 454
USER_NOT_REGISTERED = 456
RESPONSE_OK = HTTP_200_OK  # type: ignore [name-defined]
AUTHORIZATION_REQUIRED = 457
USER_AUTHENTICATION_FAILED = 458