from pydantic import EmailStr

from core.entities import Entity


class UserEntity(Entity):
    id: int
    email: EmailStr
    is_active: bool
    is_superuser: bool
