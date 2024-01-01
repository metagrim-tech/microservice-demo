from auth_service.service.unit_of_work import UnitOfWork
from tests.mocked.repository.user import MockedUserSqlAlchemyRepository


class MockedUnitOfWork(UnitOfWork):
    """Mocked Unit of work, will hold the all mocked repositories."""

    users: MockedUserSqlAlchemyRepository

    async def __aenter__(self):
        # Ass the mocked repositories, don't call the parent here, as we want to instantiate the mocked repos
        self.users = MockedUserSqlAlchemyRepository(self.session)

    def rollback(self):
        """Mocked function."""
        pass

    def commit(self):
        """Mocked function."""
        pass
