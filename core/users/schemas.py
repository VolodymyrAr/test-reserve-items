from pydantic import BaseModel, EmailStr


class UserCreate(BaseModel):
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    id: int
    email: EmailStr
    is_active: bool
    is_superuser: bool


class Token(BaseModel):
    access_token: str
    token_type: str
