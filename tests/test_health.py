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
async def test_health_check(client, mocker):
    response = await client.get("/health")
    assert response.status_code == 200
