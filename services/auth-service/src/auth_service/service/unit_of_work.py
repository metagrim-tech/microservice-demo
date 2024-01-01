from metagrim_common.domains import User
from metagrim_common.repository import UserSqlAlchemyRepository
from metagrim_common.service.unit_of_work import SqlAlchemyUnitOfWork


class UnitOfWork(SqlAlchemyUnitOfWork):
    def __init__(self, *args, **kwargs):
        """
        Initialise the Unit of Work object
        :param args:
        :param kwargs:
        """
        super(UnitOfWork, self).__init__(*args, **kwargs)

    async def __aenter__(self):
        """Start Asynchronous context manager"""
        await super(UnitOfWork, self).__aenter__()

        # initialize repositories after connecting to DB
        self.users = UserSqlAlchemyRepository(self.session)

        if self.current_user_id and (not self.current_user or self.current_user.id != self.current_user_id):
            # Load current user
            user = await self.users.get(self.current_user_id)
            self.current_user: User = User.model_validate(user)
