import enum


class ResponseTypeEnum(str, enum.Enum):
    success: str = "SUCCESS"
    error: str = "ERROR"
    warning: str = "WARNING"
    info: str = "INFO"


class UserTypeEnum(str, enum.Enum):
    cashier: str = "CASHIER"
    admin: str = "ADMIN"
    ticket_agent: str = "TICKET_AGENT"
    manager: str = "MANAGER"


class UserStatusEnum(str, enum.Enum):
    active: str = "ACTIVE"
    inactive: str = "INACTIVE"


class OrderEnum(str, enum.Enum):
    desc: str = "DESC"
    asc: str = "ASC"


class SearchFieldOperatorEnum(str, enum.Enum):
    between: str = "BETWEEN"
    gt: str = ">"
    lt: str = "<"
    eq: str = "="
    ne: str = "!="
    gteq: str = ">="
    lteq: str = "<="
