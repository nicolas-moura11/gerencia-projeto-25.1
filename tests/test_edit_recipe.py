from fastapi.testclient import TestClient
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database import Base
from models import Recipe, Ingredient
from app import app, get_db 
from security import get_current_user


TEST_DATABASE_URL = "sqlite:///:memory:"
test_engine = create_engine(TEST_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)

client = TestClient(app)

def override_user_role(role: str):
    def fake_user():
        class UserFake:
            def __init__(self):
                self.role = role
                self.username = "fakeuser"
                self.email = "fake@example.com"
                self.disabled = False
        return UserFake()
    app.dependency_overrides[get_current_user] = fake_user

def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
app.dependency_overrides[get_db] = override_get_db


@pytest.fixture(scope="function")
def db_session():
    Base.metadata.create_all(bind=test_engine)
    session = TestingSessionLocal()
    yield session
    session.close()
    Base.metadata.drop_all(bind=test_engine)


def criar_receita_com_ingredientes(db_session):
    ingrediente1 = Ingredient(name="tomate")
    ingrediente2 = Ingredient(name="queijo")
    db_session.add_all([ingrediente1, ingrediente2])
    db_session.commit()

    receita = Recipe(title="pizza", description="pizza teste", image_url=None)
    receita.ingredients = [ingrediente1, ingrediente2]
    db_session.add(receita)
    db_session.commit()
    db_session.refresh(receita)
    return receita

def test_editar_receita_nao_encontrada(db_session):
    override_user_role("creator")
    payload = {
        "title": "receita Inexistente",
        "description": "não existe",
        "ingredients": ["ingrediente"],
        "image_url": None
    }
    response = client.put("/receitas/999999", json=payload)
    assert response.status_code == 404
    assert response.json()["detail"] == "Receita não encontrada"


def test_editar_receita_client(db_session):
    override_user_role("creator")
    receita = criar_receita_com_ingredientes(db_session)

    override_user_role("client")
    payload = {
        "title": "pizza margherita",
        "description": "pizza atualizada",
        "ingredients": ["tomate", "manjericão"],
        "image_url": None
    }

    response = client.put(f"/receitas/{receita.id}", json=payload)
    assert response.status_code == 403
    assert response.json()["detail"] == "Acesso não autorizado"
