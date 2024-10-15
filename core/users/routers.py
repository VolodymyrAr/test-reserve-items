from datetime import datetime, timezone, timedelta
from typing import Annotated

import jwt
from fastapi import APIRouter, Depends, status, HTTPException
from fastapi.security import OAuth2PasswordRequestForm

from core.settings import env
from core.users.models import User
from core.users.services import UserService, EmailAlreadyExists, get_user
from core.uow import UnitOfWork, get_uow
from core.users.schemas import UserCreate, Token, UserResponse

users = APIRouter()


@users.post("/register", response_model=UserResponse)
async def register(req: UserCreate, uow: UnitOfWork = Depends(get_uow)):
    srv = UserService(uow)
    try:
        user = await srv.register(req.email, req.password)
        return user
    except EmailAlreadyExists as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered") from e


@users.post("/token", response_model=Token)
async def token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    uow: UnitOfWork = Depends(get_uow),
) -> Token:
    srv = UserService(uow)
    user = await srv.authenticate(form_data.username, form_data.password)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    data = {"sub": user.email}
    to_encode = data.copy()

    expire = datetime.now(timezone.utc) + timedelta(minutes=env.ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, env.SECRET_KEY, algorithm="HS256")

    return Token(access_token=encoded_jwt, token_type="bearer")  # nosec


@users.get("/me", response_model=UserResponse)
async def me(
    user: Annotated[User, Depends(get_user)],
):
    return user
