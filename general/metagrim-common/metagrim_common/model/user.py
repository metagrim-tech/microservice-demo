from metagrim_common.base.utils import get_password_hash
from metagrim_common.base.utils import verify_password
from metagrim_common.model.base import Base
from metagrim_common.model.base import CoreModel
from sqlalchemy import Column
from sqlalchemy import String


class UserModel(CoreModel, Base):

    email = Column(String(255), unique=True, nullable=True)
    mobile = Column(String(15), unique=True, nullable=True)
    password_hash = Column(String(255), nullable=True)
    user_type = Column(String, nullable=False, default="CASHIER")
    first_name = Column(String(255), nullable=True)
    last_name = Column(String(255), nullable=True)
    status = Column(String(15), nullable=False, server_default="INACTIVE")

    def __repr__(self):
        return f"<User email={self.email}, mobile={self.mobile}, id={self.id}, user_type={self.user_type}>"

    @property
    def password(self):
        raise AttributeError("password: write-only field")

    @password.setter
    def password(self, password):
        self.password_hash = get_password_hash(password)

    def check_password(self, password):
        return verify_password(password, self.password_hash)

    @property
    def name(self):
        data = []
        for key in ["first_name", "middle_name", "last_name"]:
            value = getattr(self, key, None)
            if value:
                data.append(value)
        return " ".join(data) if data else None
