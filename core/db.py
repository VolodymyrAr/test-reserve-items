from pydantic.alias_generators import to_snake
from sqlalchemy import Column, Integer
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.ext.declarative import declarative_base, declared_attr

from .settings import env

db_url = f"postgresql+asyncpg://{env.DB_USER}:{env.DB_PASSWORD}@{env.DB_HOST}:5432/{env.DB_NAME}"
async_engine = create_async_engine(db_url)

AsyncLocalSession = async_sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=async_engine,
    expire_on_commit=False,
    class_=AsyncSession,
)


class Base:
    id = Column(Integer, primary_key=True, index=True)

    @declared_attr
    def __tablename__(cls):  # pylint: disable=no-self-argument
        return to_snake(cls.__name__)  # pylint: disable=no-member


Base = declarative_base(cls=Base)
