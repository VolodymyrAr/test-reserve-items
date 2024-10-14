# pylint: disable=duplicate-code
from typing import AsyncGenerator

import pytest_asyncio
from httpx import AsyncClient, ASGITransport
from sqlalchemy import NullPool, text
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

from core.db import Base, get_db, db_url
from core.settings import env
from run import app as fastapi_app

test_db_url = "/".join(db_url.split("/")[:-1]) + f"/test_{env.DB_NAME}"
test_engine = create_async_engine(test_db_url, poolclass=NullPool)

TestSession = async_sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=test_engine,
    expire_on_commit=False,
    class_=AsyncSession,
)


@pytest_asyncio.fixture(scope="session", autouse=True)
async def setup_db():
    # Drop the database tables before the test session
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

    # Create the database tables before the test session (each run)
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    yield

    # Drop the database tables after the test session
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest_asyncio.fixture(scope="function")
async def truncate_db(setup_db):  # pylint: disable=redefined-outer-name,unused-argument
    # clean db after each test

    yield  # Tests run here

    async with test_engine.begin() as conn:
        for table in reversed(Base.metadata.sorted_tables):
            await conn.execute(text(f"""TRUNCATE TABLE "{table.name}" RESTART IDENTITY CASCADE"""))


@pytest_asyncio.fixture(scope="function")
async def db(truncate_db):  # pylint: disable=redefined-outer-name,unused-argument
    """
    ones called, same session obj will use as test fixture in tests and as db dependency in fastapi
    """
    async with TestSession() as session:
        yield session
        await session.rollback()


@pytest_asyncio.fixture(scope="function")
async def client(db: AsyncSession) -> AsyncGenerator:  # pylint: disable=redefined-outer-name
    fastapi_app.dependency_overrides[get_db] = lambda: db

    async with AsyncClient(
        transport=ASGITransport(app=fastapi_app),
        base_url="http://test",
    ) as client:  # pylint: disable=redefined-outer-name
        yield client
