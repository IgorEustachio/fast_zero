from contextlib import contextmanager
from datetime import datetime

import pytest
import pytest_asyncio
from fastapi.testclient import TestClient
from sqlalchemy import event
from sqlalchemy.ext.asyncio import (  # ext de extension
    AsyncSession,
    create_async_engine,
)
from sqlalchemy.pool import StaticPool

from fast_zero.app import app
from fast_zero.database import get_session
from fast_zero.models import User, table_registry
from fast_zero.security import get_password_hash


@pytest.fixture
def client(session):  # ← recebe a session de teste (banco em memória)

    # 1. Define a função substituta
    #    que retorna a session de teste
    def get_session_override():
        return session  # ← session isolada do conftest

    # 2. Abre o TestClient
    with TestClient(app) as client:
        # 3. Registra a substituição
        app.dependency_overrides[get_session] = get_session_override
        #   ↑ agora toda rota que pedir get_session
        #     receberá get_session_override no lugar

        # 4. Entrega o client para o teste rodar
        yield client

    # 5. Após o teste, limpa todas as substituições
    app.dependency_overrides.clear()


@pytest_asyncio.fixture
async def session():
    engine = create_async_engine(
        'sqlite+aiosqlite:///:memory:',
        connect_args={'check_same_thread': False},
        poolclass=StaticPool,
    )
    async with engine.begin() as conn:
        await conn.run_sync(table_registry.metadata.create_all)

    async with AsyncSession(engine) as session:
        yield session

    async with engine.begin() as conn:
        await conn.run_sync(table_registry.metadata.drop_all)


@contextmanager
def _mock_db_time(*, model, time=datetime(2024, 1, 1)):

    def fake_time_hook(mapper, connection, target):
        if hasattr(target, 'created_at'):
            target.created_at = time
        if hasattr(target, 'updated_at'):
            target.updated_at = time

    event.listen(model, 'before_insert', fake_time_hook)

    yield time

    event.remove(model, 'before_insert', fake_time_hook)


@pytest.fixture
def mock_db_time():
    return _mock_db_time


@pytest_asyncio.fixture
async def user(session):
    password = 'testtest'
    user = User(
        username='Teste',
        email='teste@test.com',
        password=get_password_hash('testtest'),
    )
    session.add(user)
    await session.commit()
    await session.refresh(user)

    user.clean_password = password

    return user


@pytest.fixture
def token(client, user):
    response = client.post(
        '/auth/token',
        data={'username': user.email, 'password': user.clean_password},
    )
    return response.json()['access_token']
