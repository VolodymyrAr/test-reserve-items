from pydantic.alias_generators import to_snake
from sqlalchemy import Column, Integer
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.orm import declarative_base

from .settings import env

db_url = f"postgresql+asyncpg://{env.DB_USER}:{env.DB_PASSWORD}@{env.DB_HOST}:5432/{env.DB_NAME}"
engine = create_async_engine(db_url)

LocalSession = async_sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
    expire_on_commit=False,
    class_=AsyncSession,
)


class Base:
    id = Column(Integer, primary_key=True, index=True)

    @declared_attr
    def __tablename__(cls):  # pylint: disable=no-self-argument
        return to_snake(cls.__name__)  # pylint: disable=no-member


Base = declarative_base(cls=Base)
