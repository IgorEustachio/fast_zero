import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from fast_zero.app import app
from fast_zero.models import table_registry


@pytest.fixture
def client():
    return TestClient(app)


@pytest.fixture
def session():
    # 1. Cria um banco de dados SQLite na MEMÓRIA RAM
    #    (não cria nenhum arquivo no disco)
    engine = create_engine('sqlite:///:memory:')

    # 2. Cria todas as tabelas definidas nos models
    #    (equivale a rodar CREATE TABLE no SQL)
    table_registry.metadata.create_all(engine)

    # 3. Abre uma sessão e ENTREGA para o teste
    with Session(engine) as session:
        yield session  # ← teste roda aqui

    # 4. Após o teste terminar, DESTRÓI tudo
    table_registry.metadata.drop_all(engine)  # apaga as tabelas
    engine.dispose()                         # fecha as conexões
