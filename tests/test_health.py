import pytest
import sqlalchemy
from fastapi import status
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from core.health.routers import Status


@pytest.mark.asyncio
async def test_health_db_web(db: AsyncSession, client: AsyncClient):
    result = await db.execute(sqlalchemy.text("SELECT 1"))
    assert result.fetchall() == [(1,)]

    resp = await client.get("/api/health/web")
    assert resp.status_code == status.HTTP_200_OK
    assert resp.json() == {"status": Status.SUCCESS.value}


@pytest.mark.asyncio
async def test_health_web(client: AsyncClient):
    resp = await client.get("/api/health/web")
    assert resp.status_code == status.HTTP_200_OK
    assert resp.json() == {"status": Status.SUCCESS.value}


@pytest.mark.asyncio
async def test_health_db(client: AsyncClient):
    response = await client.get("/api/health/db")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"status": Status.SUCCESS.value}
