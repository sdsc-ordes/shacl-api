from fastapi.testclient import TestClient

from shacl_api.server import app

client = TestClient(app)


def test_validate_bad_data():
    response = client.post(
        "/validate/",
        files={"shapes": "shapes.ttl", "data": "data.ttl"},
    )
    assert response.status_code == 200

def test_validate_good_data():
    ...

def test_validate_good_data_shapes():
    ...

def test_validate_bad_data_shapes():
    ...
