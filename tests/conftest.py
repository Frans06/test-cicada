import os
import alembic
import pytest
import pytest_asyncio
import asyncio
from fastapi.testclient import TestClient
from alembic.config import Config
from core.config import config
from sqlalchemy_utils import database_exists, drop_database, create_database
from sqlalchemy.orm import Query
from unittest.mock import AsyncMock
from core.fastapi.dependencies import LimiterInit
from core.helpers.redis import redis
from api.server import app, create_app
from httpx import AsyncClient
from asgi_lifespan import LifespanManager


@pytest.fixture(scope="session")
def anyio_backend():
    return "asyncio"


@pytest.fixture(scope="session", autouse=True)
def create_test_db():
    # Creating a new database url for the test database.
    # url = f"{str(DATABASE_URL)}_test"
    url = config.TEST_DB_URL
    if database_exists(url):
        drop_database(url)
    create_database(url)
    alembic_config = Config("alembic.ini")

    alembic.command.upgrade(alembic_config, "head")
    yield None
    alembic.command.downgrade(alembic_config, "base")
    drop_database(url)


@pytest.fixture(scope="session")
async def client():
    async with LifespanManager(app):
        async with AsyncClient(app=app, base_url="http://test") as client:
            yield client
