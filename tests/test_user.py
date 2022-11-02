import pytest
from unittest.mock import patch, AsyncMock, MagicMock
import json
from fastapi.testclient import TestClient
from api.server import app
from core.db.standalone_session import standalone_session
from db.models.user import User
from uuid import uuid4
from core.db.session import set_session_context, reset_session_context, session
from core.fastapi.dependencies import LimiterInit
from core.helpers.redis import redis


@pytest.mark.anyio
async def test_sign_up(client, mocker):
    response = await client.post(
        "/api/v1/users",
        content=json.dumps(
            {"email": "test@email.com", "password": "pass", "nickname": "test"}
        ),
    )
    assert response.status_code == 200
    assert response.json() == {"email": "test@email.com", "nickname": "test"}


@pytest.mark.anyio
async def test_sign_in(client, mocker):
    session_id = str(uuid4())
    context = set_session_context(session_id=session_id)
    try:
        async_mock = AsyncMock()
        mocker.patch.object(session, "execute", side_effect=async_mock)
        query_mock = MagicMock()
        query_mock.scalars.return_value.first.return_value = User(id=1)
        async_mock.return_value = query_mock
        response = await client.post(
            "/api/v1/users/login",
            content=json.dumps({"email": "test@email.com", "password": "pass"}),
        )
    except Exception as e:
        await session.rollback()
        raise e
    finally:
        await session.remove()
        reset_session_context(context=context)
    assert response.status_code == 200
    assert list(response.json().keys()) == ["token", "refresh_token"]
