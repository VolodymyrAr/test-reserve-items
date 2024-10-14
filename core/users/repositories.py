from typing import Optional

from sqlalchemy import select

from core.repositories import Repository
from core.store.utils import verify_password
from core.users.entities import User
from core.users.models import UserModel


class UserRepository(Repository):

    async def create(self, email: str, hashed_password: str) -> User:
        db_user = UserModel(
            email=email,
            password=hashed_password,
        )
        self.db.add(db_user)
        await self.db.flush()
        user = self._map_obj_to_domain(db_user)
        return user

    async def get_by_email(self, email: str) -> Optional[User]:
        q = select(UserModel).where(UserModel.email == email)
        resp = await self.db.execute(q)
        db_user = resp.scalar_one_or_none()
        if db_user is None:
            return None
        user = self._map_obj_to_domain(db_user)
        return user

    async def get_by_creds(self, email: str, password: str) -> Optional[User]:
        q = select(UserModel).where(UserModel.email == email)
        resp = await self.db.execute(q)
        db_user = resp.scalar_one_or_none()
        if db_user is None:
            return None
        if not verify_password(password, db_user.password):
            return None
        return self._map_obj_to_domain(db_user)

    async def get_by_id(self, user_id: int) -> Optional[User]:
        q = select(UserModel).where(UserModel.id == user_id)
        resp = await self.db.execute(q)
        db_user = resp.scalar_one_or_none()
        user = self._map_obj_to_domain(db_user)
        return user

    def _map_obj_to_domain(self, db_user: UserModel) -> User:
        return User(
            id=db_user.id,
            email=db_user.email,
            is_active=db_user.is_active,
            is_superuser=db_user.is_superuser,
        )
