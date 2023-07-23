import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import sessionmaker

from main import user_app
from User.model import Base, get_db
from sqlalchemy import create_engine
from fastapi.encoders import jsonable_encoder


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
    user_app.dependency_overrides[get_db] = override_db
    yield TestClient(user_app)


@pytest.fixture
def login_user(client):
    data = {
        "username": "abc",
        "first_name": "xyz",
        "last_name": "ab",
        "password": "password",
        "email": "abc@gmail.com"
    }
    client.post('/user/register', json=jsonable_encoder(data))
    login_response = client.post('/user/login', json=jsonable_encoder({'username': 'abc', 'password': 'password'}))
    return ""


def test_user_register_successful(client):
    data = {
        "username": "abc",
        "first_name": "xyz",
        "last_name": "ab",
        "password": "password",
        "email": "abc@gmail.com"
    }
    response = client.post('/user/register', json=jsonable_encoder(data))
    assert response.status_code == 201


def test_user_register_fail(client):
    data = {
        "username": "abc",
        "first_name": "xyz",
        "last_name": "ab",
        "password": "password",
        "email": "abc@gmail.com"
    }
    response = client.post('/user/register', json=jsonable_encoder(data))
    response = client.post('/user/register', json=jsonable_encoder(data))
    assert response.status_code == 400


def test_login_user_successful(client):
    data = {
        "username": "abc",
        "first_name": "xyz",
        "last_name": "ab",
        "password": "password",
        "email": "abc@gmail.com"
    }
    response = client.post('/user/register', json=jsonable_encoder(data))
    assert response.status_code == 201

    login_response = client.post('/user/login', json=jsonable_encoder({'username': 'abc', 'password': 'password'}))
    assert login_response.status_code == 200


def test_login_user_fail(client):
    data = {
        "username": "abc",
        "first_name": "xyz",
        "last_name": "ab",
        "password": "password",
        "email": "abc@gmail.com"
    }
    response = client.post('/user/register', json=jsonable_encoder(data))
    assert response.status_code == 201

    login_response = client.post('/user/login', json=jsonable_encoder({'username': 'abc', 'password': ''}))
    assert login_response.status_code == 401
