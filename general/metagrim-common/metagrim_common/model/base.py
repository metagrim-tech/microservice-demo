import re
from functools import lru_cache
from uuid import uuid4

from metagrim_common.model.types import UUID
from sqlalchemy import Boolean
from sqlalchemy import Column
from sqlalchemy import DateTime
from sqlalchemy import func
from sqlalchemy import String
from sqlalchemy import TIMESTAMP
from sqlalchemy.orm import as_declarative
from sqlalchemy.orm import declared_attr


class CoreModel:
    id = Column(UUID, primary_key=True, default=uuid4)
    created_at = Column(DateTime, server_default=func.now())
    modified_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.current_timestamp())
    is_deleted = Column(Boolean(), default=False)
    created_by = Column(String(36))
    modified_by = Column(String(36))

    @classmethod
    @lru_cache(maxsize=1)
    def get_columns(cls):
        columns = []
        for column in cls.__table__.columns:
            name = f"{column}".split(".")[-1]
            columns.append(name)
        return columns


@as_declarative()
class Base:
    __name__: str

    # Generate __tablename__ automatically
    @declared_attr
    def __tablename__(cls) -> str:
        table_name = "_".join(["demo", re.sub(r"(?<!^)(?=[A-Z])", "_", cls.__name__).lower()])
        return table_name.replace("_model", "")
