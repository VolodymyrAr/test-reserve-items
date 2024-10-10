from typing import TypeVar

from sqlalchemy.orm import DeclarativeMeta

from core.uow import UnitOfWorkBase

T = TypeVar("T", bound=DeclarativeMeta)


class Service:

    def __init__(self, uow: UnitOfWorkBase):
        self.uow = uow
