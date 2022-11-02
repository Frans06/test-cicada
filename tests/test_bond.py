import pytest
from unittest.mock import patch, AsyncMock, MagicMock, ANY
import json
from fastapi.testclient import TestClient
from api.server import app
from core.db.standalone_session import standalone_session
from db.models.user import User
from uuid import uuid4
from core.db.session import set_session_context, reset_session_context, session
from core.fastapi.dependencies import LimiterInit
from core.helpers.redis import redis
from core.fastapi.dependencies.permission import (
    PermissionDependency,
    IsAuthenticated,
    get_current_user_id,
)
from api.server import app


@pytest.mark.anyio
async def test_bond_create_error_unauthenticate(client):
    session_id = str(uuid4())
    context = set_session_context(session_id=session_id)
    try:
        user = User(email="email", password="pass", nickname="nick")
        session.add(user)
        await session.commit()
        response = await client.post(
            "/api/v1/bonds",
            content=json.dumps(
                {"name": "string", "quantity": 10000, "price": "100000000"}
            ),
        )
    except Exception as e:
        await session.rollback()
        raise e
    finally:
        await session.remove()
        reset_session_context(context=context)
    assert response.status_code == 401
    assert response.json() == {
        "error_code": 401,
        "message": "No permission -- see authorization schemes",
    }


@pytest.mark.anyio
async def test_bond_create_successfully(client):
    session_id = str(uuid4())
    context = set_session_context(session_id=session_id)
    try:
        user = User(email="email2", password="pass", nickname="nick2")
        session.add(user)
        await session.commit()
        app.dependency_overrides[PermissionDependency([IsAuthenticated])] = lambda: True
        app.dependency_overrides[get_current_user_id] = lambda: 1
        response = await client.post(
            "/api/v1/bonds",
            content=json.dumps(
                {"name": "string", "quantity": 10000, "price": "100000000"}
            ),
        )
    except Exception as e:
        await session.rollback()
        raise e
    finally:
        await session.remove()
        reset_session_context(context=context)
    app.dependency_overrides = {}
    assert response.status_code == 200
    assert response.json() == {
        "id": ANY,
        "quantity": 10000,
        "owner_id": 1,
        "price": 100000000,
        "name": "string",
    }


@pytest.mark.anyio
async def test_bond_create_error_many_decimals(client):
    session_id = str(uuid4())
    context = set_session_context(session_id=session_id)
    try:
        user = User(email="email3", password="pass", nickname="nick3")
        session.add(user)
        await session.commit()
        app.dependency_overrides[PermissionDependency([IsAuthenticated])] = lambda: True
        app.dependency_overrides[get_current_user_id] = lambda: 1
        response = await client.post(
            "/api/v1/bonds",
            content=json.dumps(
                {"name": "string", "quantity": 10000, "price": "10000000.00001"}
            ),
        )
    except Exception as e:
        await session.rollback()
        raise e
    finally:
        await session.remove()
        reset_session_context(context=context)
    app.dependency_overrides = {}

    assert response.status_code == 422
    assert response.json() == {
        "detail": [
            {
                "loc": ["body", "price"],
                "msg": "ensure that there are no more than 4 decimal places",
                "type": "value_error.decimal.max_places",
                "ctx": {"decimal_places": 4},
            }
        ]
    }


@pytest.mark.anyio
async def test_bond_create_greater_than_max(client):
    session_id = str(uuid4())
    context = set_session_context(session_id=session_id)
    try:
        user = User(email="email5", password="pass", nickname="nick5")
        session.add(user)
        await session.commit()
        app.dependency_overrides[PermissionDependency([IsAuthenticated])] = lambda: True
        app.dependency_overrides[get_current_user_id] = lambda: 1
        response = await client.post(
            "/api/v1/bonds",
            content=json.dumps(
                {"name": "string", "quantity": 10000, "price": "200000000.0000"}
            ),
        )
    except Exception as e:
        await session.rollback()
        raise e
    finally:
        await session.remove()
        reset_session_context(context=context)
    app.dependency_overrides = {}

    assert response.status_code == 422
    to_assert = [
        {
            "loc": ["body", "price"],
            "msg": "ensure this value is less than or equal to 100000000",
            "type": "value_error.number.not_le",
            "ctx": {"limit_value": 100000000},
        },
        {
            "loc": ["body", "quantity"],
            "msg": "ensure this value is less than or equal to 10000",
            "type": "value_error.number.not_le",
            "ctx": {"limit_value": 10000},
        },
    ]
    for i in response.json()["detail"]:
        assert i in to_assert


@pytest.mark.anyio
async def test_bond_list(client):
    session_id = str(uuid4())
    context = set_session_context(session_id=session_id)
    try:
        user = User(email="email4", password="pass", nickname="nick4")
        session.add(user)
        await session.commit()
        app.dependency_overrides[PermissionDependency([IsAuthenticated])] = lambda: True
        app.dependency_overrides[get_current_user_id] = lambda: 1
        response = await client.get(
            "/api/v1/bonds?limit=1",
        )
    except Exception as e:
        await session.rollback()
        raise e
    finally:
        await session.remove()
        reset_session_context(context=context)
    app.dependency_overrides = {}

    assert response.status_code == 200
    assert response.json() == [
        {
            "id": 1,
            "quantity": 10000,
            "owner_id": 1,
            "price": 100000000,
            "status": "posted",
            "name": "string",
        }
    ]


@pytest.mark.anyio
async def test_bond_list_usd(client):
    session_id = str(uuid4())
    context = set_session_context(session_id=session_id)
    try:
        user = User(email="email6", password="pass", nickname="nick6")
        session.add(user)
        await session.commit()
        app.dependency_overrides[PermissionDependency([IsAuthenticated])] = lambda: True
        app.dependency_overrides[get_current_user_id] = lambda: 1
        response = await client.get(
            "/api/v1/bonds?currency=USD&limit=1",
        )
    except Exception as e:
        await session.rollback()
        raise e
    finally:
        await session.remove()
        reset_session_context(context=context)
    app.dependency_overrides = {}

    assert response.status_code == 200
    assert response.json() == [
        {
            "id": 1,
            "quantity": 10000,
            "owner_id": 1,
            "price": 5064000,
            "status": "posted",
            "name": "string",
        }
    ]


@pytest.mark.anyio
async def test_buy_bond_error_diff_user(client):
    session_id = str(uuid4())
    context = set_session_context(session_id=session_id)
    try:
        user = User(email="email7", password="pass", nickname="nick7")
        session.add(user)
        await session.commit()
        app.dependency_overrides[PermissionDependency([IsAuthenticated])] = lambda: True
        app.dependency_overrides[get_current_user_id] = lambda: 1
        response = await client.patch(
            "/api/v1/bonds/1/buy",
        )
    except Exception as e:
        await session.rollback()
        raise e
    finally:
        await session.remove()
        reset_session_context(context=context)
    app.dependency_overrides = {}

    assert response.status_code == 400
    assert response.json() == {
        "error_code": "SAME_USER_BUY",
        "message": "You can not buy your bond",
    }


@pytest.mark.anyio
async def test_buy_bond_error_diff_user(client):
    session_id = str(uuid4())
    context = set_session_context(session_id=session_id)
    try:
        user = User(email="email8", password="pass", nickname="nick8")
        session.add(user)
        await session.commit()
        app.dependency_overrides[PermissionDependency([IsAuthenticated])] = lambda: True
        app.dependency_overrides[get_current_user_id] = lambda: 2
        response = await client.patch(
            "/api/v1/bonds/1/buy",
        )
    except Exception as e:
        await session.rollback()
        raise e
    finally:
        await session.remove()
        reset_session_context(context=context)
    app.dependency_overrides = {}

    assert response.status_code == 200
    assert response.json() == {
        "id": 1,
        "owner_id": 2,
        "name": "string",
        "status": "sold",
        "success": True,
    }


@pytest.mark.anyio
async def test_buy_bond_error_bond_sold(client):
    session_id = str(uuid4())
    context = set_session_context(session_id=session_id)
    try:
        user = User(email="email9", password="pass", nickname="nick9")
        session.add(user)
        await session.commit()
        app.dependency_overrides[PermissionDependency([IsAuthenticated])] = lambda: True
        app.dependency_overrides[get_current_user_id] = lambda: 2
        response = await client.patch(
            "/api/v1/bonds/1/buy",
        )
    except Exception as e:
        await session.rollback()
        raise e
    finally:
        await session.remove()
        reset_session_context(context=context)
    app.dependency_overrides = {}

    assert response.status_code == 400
    assert response.json() == {
        "error_code": "BOND_ALREADY_SOLD",
        "message": "bond has been sold",
    }
