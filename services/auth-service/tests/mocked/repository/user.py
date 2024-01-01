import uuid

from faker import Faker
from faker_sqlalchemy import SqlAlchemyProvider
from metagrim_common.model.user import UserModel
from metagrim_common.repository import UserSqlAlchemyRepository


def get_fake_action(action: str):
    # use this funtion to create fake action object of given action
    pass


def get_actions(user_type: str):
    # Use this funtion to list all the actions of given use type
    pass


class MockedUserSqlAlchemyRepository(UserSqlAlchemyRepository):
    """Mocked User Repository."""

    async def find_by_email(self, email: str):
        """Mocked Method
        Original implementation can be seen `src.repository.user.UserSqlAlchemyRepository.find_by_email`

        :param email: Email to find the user
            If email starts with  "no_user" it wil simulate the case when user does not exists
            If email contains "inactive" it will simulate if the user status is inactive
            if email contains the 'admin', 'cashier' or 'manager', it will simulate the respective user type
                if email do not contain any role info then ticket agent user type will be simulated
        :return:
        """
        if email.lower().startswith("no_user") or email.lower().startswith("no.user"):
            return None

        fake = Faker()
        fake.add_provider(SqlAlchemyProvider)
        instance = fake.sqlalchemy_model(UserModel)
        instance.email = email
        instance.password_hash = "$2b$12$iXS8TFkM4Yn8AJK/.WtyfeBmVEVEbGyglaFbR01E3DCe3I/xeT5DC"
        instance.status = "INACTIVE" if email.lower().find("inactive") >= 0 else "ACTIVE"
        if email.find("admin") > -1:
            instance.user_type = "ADMIN"
            instance.actions = []
        elif email.find("cashier") > -1:
            instance.user_type = "CASHIER"
            instance.actions = []
        elif email.find("manager"):
            instance.user_type = "MANAGER"
            instance.actions = []
        instance.id = uuid.uuid4()
        return instance
