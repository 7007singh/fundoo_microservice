import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import sessionmaker
from main import note_app
from Note.model import Base, get_db
from sqlalchemy import create_engine
from fastapi.encoders import jsonable_encoder
from .test_user import login_user

engine = create_engine('postgresql+psycopg2://postgres:Ssingh2023@localhost:5432/Test')

session = sessionmaker(autoflush=False, autocommit=False, bind=engine)


@pytest.fixture
def override_get_db():
    Base.metadata.create_all(bind=engine)
    db = session()
    try:
        yield db
    finally:
        Base.metadata.drop_all(bind=engine)
        db.close()


@pytest.fixture
def client(override_get_db):
    def override_db():
        try:
            yield override_get_db
        finally:
            override_get_db.close()

    note_app.dependency_overrides[get_db] = override_db
    yield TestClient(note_app)


@pytest.mark.abc
def test_create_note_successful(client, login_user):
    data = {
        "title": "string",
        "description": "string",
        "color": "string"
    }
    print(login_user)
    response = client.post('/note/create_note', json=data, headers={'Authorization': login_user})
    print(response.content)
    assert response.status_code == 201
