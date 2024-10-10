from typing import Optional

from sqlalchemy import select

from core.base import Repository
from core.users.models import User


class UserRepository(Repository[User]):
    model = User

    async def get_by_email(self, email: str) -> Optional[User]:
        q = select(User).where(User.email == email)
        res = await self.db.execute(q)
        return res.scalar_one_or_none()
