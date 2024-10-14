import pytest
from fastapi import status
from httpx import AsyncClient
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from core.users.models import UserModel

base_api_path = "/api/users"


@pytest.mark.asyncio
async def test_create_user_success(db: AsyncSession, client: AsyncClient):
    test_mail = "test@gmail.com"
    resp = await client.post(
        f"{base_api_path}/register",
        json={"email": test_mail, "password": "testpass"},
    )
    assert resp.status_code == status.HTTP_200_OK
    data = resp.json()
    assert data.get("email") == test_mail
    assert not data.get("is_active")
    assert not data.get("is_superuser")

    query = select(func.count()).select_from(UserModel)
    resp = await db.execute(query)
    user_counts = resp.scalar()
    assert user_counts == 1

    query = select(UserModel).where(UserModel.email == test_mail)
    resp = await db.execute(query)
    db_user = resp.scalar_one_or_none()
    assert db_user is not None
    assert db_user.id == data.get("id")
