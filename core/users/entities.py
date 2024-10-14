from pydantic import EmailStr

from core.entities import Entity


class User(Entity):
    id: int
    email: EmailStr
    is_active: bool
    is_superuser: bool
