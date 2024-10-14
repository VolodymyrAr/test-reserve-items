from datetime import datetime, timedelta, timezone
from typing import Optional, Annotated

import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from core.services import Service
from core.settings import env
from core.store.utils import hash_password
from core.uow import UnitOfWork, get_uow
from core.users.entities import User

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/users/token")


class EmailAlreadyExists(Exception):
    pass


class InvalidTokenError(Exception):
    pass


class UserService(Service):
    ACCESS_TOKEN_EXPIRE_MINUTES = 30
    ALGORITHM = "HS256"

    async def register(self, email: str, password: str) -> User:
        user = await self.uow.users.get_by_email(email)
        if user:
            raise EmailAlreadyExists

        password = hash_password(password)
        user = await self.uow.users.create(email=email, hashed_password=password)
        return user

    async def authenticate(self, email: str, password: str) -> Optional[User]:
        user = await self.uow.users.get_by_creds(email, password)
        return user

    def create_access_token(self, user: User) -> str:
        data = {"sub": user.email}
        to_encode = data.copy()

        expire = datetime.now(timezone.utc) + timedelta(minutes=self.ACCESS_TOKEN_EXPIRE_MINUTES)

        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, env.SECRET_KEY, algorithm=self.ALGORITHM)
        return encoded_jwt


async def get_user(
    token: Annotated[str, Depends(oauth2_scheme)],
    uow: UnitOfWork = Depends(get_uow),
) -> User:
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
) -> User:
    user = await get_user(token, uow)
    if not user.is_superuser:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
    return user
