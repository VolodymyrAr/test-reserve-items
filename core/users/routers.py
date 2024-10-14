from typing import Annotated

from fastapi import APIRouter, Depends, status, HTTPException
from fastapi.security import OAuth2PasswordRequestForm

from core.users.entities import UserEntity
from core.users.services import UserService, EmailAlreadyExists, get_user
from core.uow import UnitOfWork, get_uow
from core.users.schemas import UserCreate, Token

users = APIRouter()


@users.post("/register", response_model=UserEntity)
async def register_user(req: UserCreate, uow: UnitOfWork = Depends(get_uow)):
    srv = UserService(uow)
    try:
        user = await srv.register(req.email, req.password)
        return user
    except EmailAlreadyExists as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered") from e


@users.post("/token", response_model=Token)
async def login_for_access_token(
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
    access_token = srv.create_access_token(user)
    return Token(access_token=access_token, token_type="bearer")  # nosec


@users.get("/me", response_model=UserEntity)
async def read_users_me(
    user: Annotated[UserEntity, Depends(get_user)],
):
    return user
