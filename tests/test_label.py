import json
import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import sessionmaker
from main import label_app
from Label.model import Base, get_db
from sqlalchemy import create_engine

engine = create_engine('postgresql+psycopg2://postgres:Ssingh2023@localhost:5432/Test')

session = sessionmaker(autoflush=False, autocommit=False, bind=engine)


class CustomDelete(TestClient):
    def delete_with_payload(self, **kwargs):
        return self.request(method='DELETE', **kwargs)


delete_client = CustomDelete(label_app)


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

    label_app.dependency_overrides[get_db] = override_db
    yield TestClient(label_app)


@pytest.fixture
def login_token():
    return "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyIjoxfQ.0KckvP31ZipVNqq0hSD2rAz2HnpbzQNHpBb-GrlZ-Gw"


def test_create_label_success(client, login_token):
    data = {
        "name": 'Study'
    }
    response = client.post('/label/add_label', json=data, headers={'Authorization': login_token})
    assert response.status_code == 201


def test_create_label_fail(client, login_token):
    data = {
        "name": 'Study'
    }
    response = client.post('/label/add_label', json=data)
    assert response.status_code == 401


def test_update_label_success(client, login_token):
    data = {
        "name": 'Study'
    }
    response = client.post('/label/add_label', json=data, headers={'Authorization': login_token})
    data = json.loads(response.content)
    label_id = data['data']['id']
    data = {
        'name': 'Updated Label'
    }
    response = client.put(f'/label/update_label/{label_id}', json=data, headers={'Authorization': login_token})
    assert response.status_code == 200


def test_update_label_fail(client, login_token):
    data = {
        "name": 'Study'
    }
    response = client.post('/label/add_label', json=data, headers={'Authorization': login_token})
    data = json.loads(response.content)
    label_id = data['data']['id']
    data = {

    }
    response = client.put(f'/label/update_label/{label_id}', json=data, headers={'Authorization': login_token})
    assert response.status_code == 422


def test_delete_label(client, login_token):
    data = {
        "name": 'Study'
    }
    response = client.post('/label/add_label', json=data, headers={'Authorization': login_token})
    data = json.loads(response.content)
    label_id = data['data']['id']
    data = {
        "id": label_id
    }
    response = delete_client.delete_with_payload(url=f'/label/delete_label/{label_id}', json=data, headers={'Authorization': login_token})
    assert response.status_code == 200


def test_delete_label_fail(client, login_token):
    data = {
        "name": 'Study'
    }
    response = client.post('/label/add_label', json=data, headers={'Authorization': login_token})
    data = json.loads(response.content)
    label_id = data['data']['id']
    data = {
        "id": label_id
    }
    response = delete_client.delete_with_payload(url=f'/label/delete_label/{label_id}', json=data)
    assert response.status_code == 401


def test_associate_label_success(client, login_token):
    data = {
        "name": 'Study'
    }
    response = client.post('/label/add_label', json=data, headers={'Authorization': login_token})
    data = json.loads(response.content)
    label_id = data['data']['id']
    data = {
        'note_id': 6,
        'label_id': [label_id]
    }
    response = client.post('/label/associate_label', json=data, headers={'Authorization': login_token})
    assert response.status_code == 200


def test_associate_label_fail(client, login_token):
    data = {
        "name": 'Study'
    }
    client.post('/label/add_label', json=data, headers={'Authorization': login_token})
    data = {
        'note_id': 6,
        'label_id': [7, 6]
    }
    response = client.post('/label/associate_label', json=data)
    assert response.status_code == 401


def test_delete_label_association_success(client, login_token):
    data = {
        "name": 'Study'
    }
    response = client.post('/label/add_label', json=data, headers={'Authorization': login_token})
    data = json.loads(response.content)
    label_id = data['data']['id']
    data = {
        "note_id": 7,
        "label_id": [label_id],
    }
    delete_response = delete_client.delete_with_payload(url='/label/delete_label_association', json=data, headers={'Authorization': login_token})
    assert delete_response.status_code == 200
