from contextlib import contextmanager
from datetime import datetime

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, event
from sqlalchemy.orm import Session
from sqlalchemy.pool import StaticPool

from fast_zero.app import app
from fast_zero.database import get_session
from fast_zero.models import User, table_registry


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


@pytest.fixture
def session():
    engine = create_engine(
        'sqlite:///:memory:',
        connect_args={'check_same_thread': False},
        poolclass=StaticPool,
    )
    table_registry.metadata.create_all(engine)

    with Session(engine) as session:
        yield session

    table_registry.metadata.drop_all(engine)
    engine.dispose()  # fecha as conexões


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


@pytest.fixture
def user(session):
    user = User(username='Teste', email='teste@test.com', password='testtest')
    session.add(user)
    session.commit()
    session.refresh(user)

    return user
