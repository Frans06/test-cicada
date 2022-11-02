import pytest
from unittest.mock import patch, AsyncMock, MagicMock
import json
from fastapi.testclient import TestClient
from api.server import create_app
from core.db.standalone_session import standalone_session
from db.models.user import User
from uuid import uuid4
from core.db.session import set_session_context, reset_session_context, session
from core.fastapi.dependencies import LimiterInit
from core.helpers.redis import redis
from core.utils.token_helper import TokenHelper
from db.models import User
from httpx import AsyncClient
from asgi_lifespan import LifespanManager

user = User(id=5)


@pytest.mark.anyio
async def test_verify_token(client, mocker):
    token = TokenHelper.encode(payload={"user_id": user.id})
    response = await client.post("/auth/verify", content=json.dumps({"token": token}))
    assert response.status_code == 200


@pytest.mark.anyio
async def test_refresh_token(client, mocker):
    token = TokenHelper.encode(payload={"user_id": user.id})
    refresh_token = TokenHelper.encode(payload={"sub": "refresh"})
    response = await client.post(
        "/auth/refresh",
        content=json.dumps({"token": token, "refresh_token": refresh_token}),
    )
    assert response.status_code == 200
    assert list(response.json().keys()) == ["token", "refresh_token"]
