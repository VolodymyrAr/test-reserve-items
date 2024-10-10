# pylint: disable=duplicate-code
from typing import AsyncGenerator

import pytest
import pytest_asyncio
from httpx import AsyncClient, ASGITransport
from sqlalchemy import NullPool
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

from core.db import Base
from core.settings import env
from core.uow import UnitOfWork
from run import app

engine = create_async_engine(
    f"postgresql+asyncpg://{env.DB_USER}:{env.DB_PASSWORD}@{env.DB_HOST}:5432/test_{env.DB_NAME}",
    poolclass=NullPool,
)

TestSession = async_sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
    expire_on_commit=False,
    class_=AsyncSession,
)


@pytest.fixture(scope="session")
async def setup_db():
    # Create the database tables
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    yield  # Tests run here

    # Drop the database tables after the test
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest_asyncio.fixture(scope="function")
async def uow(setup_db) -> AsyncGenerator:  # pylint: disable=redefined-outer-name,unused-argument
    async with UnitOfWork(db=TestSession()) as uow:  # pylint: disable=redefined-outer-name
        yield uow


@pytest_asyncio.fixture(scope="function")
async def db(setup_db) -> AsyncGenerator:  # pylint: disable=redefined-outer-name,unused-argument
    async with TestSession() as session:
        yield session
        await session.rollback()


@pytest_asyncio.fixture(scope="function")
async def client() -> AsyncGenerator:
    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test",
    ) as client:  # pylint: disable=redefined-outer-name
        yield client
