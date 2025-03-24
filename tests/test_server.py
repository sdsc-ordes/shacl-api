from fastapi.testclient import TestClient

from shacl_api.server import app

client = TestClient(app)


def test_validate_bad_data():
    response = client.post(
        "/items/",
        headers={"X-Token": "coneofsilence"},
        json={"id": "foobar", "title": "Foo Bar", "description": "The Foo Barters"},
    )
    assert response.status_code == 200
    assert response.json() == {
        "id": "foobar",
        "title": "Foo Bar",
        "description": "The Foo Barters",
    }

def test_validate_good_data():
    ...

def test_validate_good_data_shapes():
    ...

def test_validate_bad_data_shapes():
    ...
