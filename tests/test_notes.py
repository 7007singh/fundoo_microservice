import json
import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import sessionmaker
from main import note_app
from Note.model import Base, get_db
from sqlalchemy import create_engine

engine = create_engine('postgresql+psycopg2://postgres:Ssingh2023@localhost:5432/Test')

session = sessionmaker(autoflush=False, autocommit=False, bind=engine)


class CustomDelete(TestClient):
    def delete_with_payload(self, **kwargs):
        return self.request(method='DELETE', **kwargs)


delete_client = CustomDelete(note_app)


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


@pytest.fixture
def login_token():
    return "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyIjoxfQ.0KckvP31ZipVNqq0hSD2rAz2HnpbzQNHpBb-GrlZ-Gw"


def test_create_note_successful(client, login_token):
    data = {
        "title": "Sub",
        "description": "all",
        "color": "white"
    }
    response = client.post('/note/create_note', json=data, headers={'Authorization': login_token})
    assert response.status_code == 201


def test_create_note_fail(client, login_token):
    data = {

        "description": 'all',
        "color": "white"
    }
    response = client.post('/note/create_note', json=data, headers={'Authorization': login_token})
    assert response.status_code == 422


def test_update_note_successful(client, login_token):
    data = {
        "title": "Sub",
        "description": "all",
        "color": "white"
    }
    response = client.post('/note/create_note', json=data, headers={'Authorization': login_token})
    data = json.loads(response.content)
    note_id = data['data']['id']
    data = {
        "title": "HOF",
        "description": "lamda",
        "color": "grey"
    }
    update_response = client.put(f'/note/update_note/{note_id}', json=data, headers={'Authorization': login_token})
    assert update_response.status_code == 200


def test_update_note_fail(client, login_token):
    data = {
        "title": "Sub",
        "description": "all",
        "color": "white"
    }
    response = client.post('/note/create_note', json=data, headers={'Authorization': login_token})
    data = json.loads(response.content)
    note_id = data['data']['id']
    data = {
        "title": "HOF",
        "description": "lamda",
        "color": "grey"
    }
    update_response = client.put(f'/note/update_note/{note_id}', json=data, headers={'Authorization': ''})
    assert update_response.status_code == 401


def test_delete_note_successful(client, login_token):
    data = {
        "title": "Sub",
        "description": "all",
        "color": "white"
    }
    response = client.post('/note/create_note', json=data, headers={'Authorization': login_token})
    data = json.loads(response.content)
    note_id = data['data']['id']
    data = {
        "id": note_id
    }
    delete_response = delete_client.delete_with_payload(url=f'/note/delete_note/{note_id}', json=data,
                                                        headers={'Authorization': login_token})
    assert delete_response.status_code == 200


def test_delete_note_fail(client, login_token):
    data = {
        "title": "Sub",
        "description": "all",
        "color": "white"
    }
    response = client.post('/note/create_note', json=data, headers={'Authorization': login_token})
    data = json.loads(response.content)
    note_id = data['data']['id']
    data = {
        "id": note_id
    }
    delete_response = delete_client.delete_with_payload(url=f'/note/delete_note/{note_id}', json=data,
                                                        )
    assert delete_response.status_code == 401


def test_add_collaborator(client, login_token):
    data = {
        "title": "Sub",
        "description": "all",
        "color": "white"
    }
    response = client.post('/note/create_note', json=data, headers={'Authorization': login_token})
    data = json.loads(response.content)
    note_id = data['data']['id']
    data = {
        "note_id": note_id,
        "user_id": [
            2, 4
        ]
    }
    collab_response = client.post('/note/collaborate', json=data, headers={'Authorization': login_token})
    assert collab_response.status_code == 200


def test_add_collaborator_fail(client, login_token):
    data = {
        "title": "Sub",
        "description": "all",
        "color": "white"
    }
    response = client.post('/note/create_note', json=data, headers={'Authorization': login_token})
    data = json.loads(response.content)
    note_id = data['data']['id']
    data = {
        "note_id": 100,
        "user_id": [
            2, 4
        ]
    }
    collab_response = client.post('/note/collaborate', json=data, headers={'Authorization': login_token})
    assert collab_response.status_code == 400


def test_delete_collab(client, login_token):
    data = {
        "title": "Sub",
        "description": "all",
        "color": "white"
    }
    response = client.post('/note/create_note', json=data, headers={'Authorization': login_token})
    data = json.loads(response.content)
    note_id = data['data']['id']
    data = {
        "note_id": note_id,
        "user_id": [
            2, 4
        ]
    }
    client.post('/note/collaborate', json=data, headers={'Authorization': login_token})
    custom_del = CustomDelete(note_app)
    data = {
        "note_id": note_id,
        "user_id": [
            2
        ]
    }
    collab_response = custom_del.delete_with_payload(url='/note/delete_collaborator', json=data,
                                                     headers={'Authorization': login_token})
    assert collab_response.status_code == 200


def test_delete_collab_fail(client, login_token):
    data = {
        "title": "Sub",
        "description": "all",
        "color": "white"
    }
    response = client.post('/note/create_note', json=data, headers={'Authorization': login_token})
    data = json.loads(response.content)
    note_id = data['data']['id']
    data = {
        "note_id": note_id,
        "user_id": [
            2, 4
        ]
    }
    client.post('/note/collaborate', json=data, headers={'Authorization': login_token})
    custom_del = CustomDelete(note_app)
    data = {
        "note_id": 32,
        "user_id": [
            2
        ]
    }
    collab_response = custom_del.delete_with_payload(url='/note/delete_collaborator', json=data,
                                                     headers={'Authorization': login_token})
    assert collab_response.status_code == 400
