from typing import Optional

from sqlalchemy import select

from core.repositories import Repository
from core.users.entities import UserEntity
from core.users.models import UserModel


class UserRepository(Repository):

    async def create(self, email: str, hashed_password: str) -> UserEntity:
        db_user = UserModel(
            email=email,
            password=hashed_password,
        )
        self.db.add(db_user)
        await self.db.flush()
        user = self._map_obj_to_domain(db_user)
        return user

    async def get_by_email(self, email: str) -> Optional[UserEntity]:
        q = select(UserModel).where(UserModel.email == email)
        resp = await self.db.execute(q)
        db_user = resp.scalar_one_or_none()
        if db_user is None:
            return None
        user = self._map_obj_to_domain(db_user)
        return user

    async def get_by_id(self, user_id: int) -> Optional[UserEntity]:
        q = select(UserModel).where(UserModel.id == user_id)
        resp = await self.db.execute(q)
        db_user = resp.scalar_one_or_none()
        user = self._map_obj_to_domain(db_user)
        return user

    def _map_obj_to_domain(self, db_user: UserModel) -> UserEntity:
        return UserEntity(
            id=db_user.id,
            email=db_user.email,
            is_active=db_user.is_active,
            is_superuser=db_user.is_superuser,
        )
