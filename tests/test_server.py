from fastapi.testclient import TestClient
from rdflib import Graph
from rdflib.namespace import SH
from rdflib.term import Literal

from shacl_api.server import app

client = TestClient(app)


def test_validate_bad_data():
    """Test that the server successfully returns a failed validation report."""

    data_path = "tests/data/val_fail_data.ttl"
    shapes_path = "tests/data/val_fail_shapes.ttl"

    response = client.post(
        "/validate/",
        files={
            "shapes": ("shapes.ttl", open(shapes_path, "rb"), "text/turtle"),
            "data": ("data.ttl", open(data_path, "rb"), "text/turtle"),
        },
        headers={"Accept": "text/turtle"},
    )
    report = Graph().parse(data=response.text, format="turtle")

    assert response.status_code == 200
    assert (None, SH.conforms, Literal(False)) in report

def test_validate_good_data():
    ...

def test_validate_good_data_shapes():
    ...

def test_validate_bad_data_shapes():
    ...
