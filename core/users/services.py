from datetime import datetime, timedelta, timezone
from typing import Optional, Annotated

import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext

from core.services import Service
from core.settings import env
from core.uow import UnitOfWork, get_uow
from core.users.entities import UserEntity


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/users/token")


def verify_password(plain_password, hashed_password) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def hash_password(password) -> str:
    return pwd_context.hash(password)


class EmailAlreadyExists(Exception):
    pass


class InvalidTokenError(Exception):
    pass


class UserService(Service):
    ACCESS_TOKEN_EXPIRE_MINUTES = 30
    ALGORITHM = "HS256"

    async def register(self, email: str, password: str) -> UserEntity:
        user = await self.uow.users.get_by_email(email)
        if user:
            raise EmailAlreadyExists

        password = hash_password(password)
        user = await self.uow.users.create(email=email, hashed_password=password)
        return user

    async def authenticate(self, email: str, password: str) -> Optional[UserEntity]:
        user = await self.uow.users.get_by_email(email)
        if not user:
            return
        if not verify_password(password, user.password):
            return
        return user

    def create_access_token(self, user: UserEntity) -> str:
        data = {"sub": user.email}
        to_encode = data.copy()

        expire = datetime.now(timezone.utc) + timedelta(minutes=self.ACCESS_TOKEN_EXPIRE_MINUTES)

        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, env.SECRET_KEY, algorithm=self.ALGORITHM)
        return encoded_jwt


async def get_user(
    token: Annotated[str, Depends(oauth2_scheme)],
    uow: UnitOfWork = Depends(get_uow),
) -> UserEntity:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, env.SECRET_KEY, algorithms=[UserService.ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
    except InvalidTokenError as e:
        raise credentials_exception from e

    user = await uow.users.get_by_email(email)

    if user is None:
        raise credentials_exception

    if not user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")

    return user


async def get_superuser(
    token: Annotated[str, Depends(oauth2_scheme)],
    uow: UnitOfWork = Depends(get_uow),
) -> UserEntity:
    user = await get_user(token, uow)
    if not user.is_superuser:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
    return user
