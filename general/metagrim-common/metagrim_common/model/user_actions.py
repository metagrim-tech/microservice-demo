from metagrim_common.model import UserModel
from metagrim_common.model.base import Base
from metagrim_common.model.base import CoreModel
from sqlalchemy import Column
from sqlalchemy import ForeignKey
from sqlalchemy import String
from sqlalchemy.orm import relationship


class UserActionModel(CoreModel, Base):
    user_id = Column(ForeignKey(UserModel.id))
    action = Column(String(255))

    user = relationship(UserModel, backref="actions")
