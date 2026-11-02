import pytest
from testcontainers.community.postgres import PostgresContainer


@pytest.fixture
def test_db_url():
    with PostgresContainer("postgres:latest", driver="asyncpg") as postgres:
        yield postgres.get_connection_url()
