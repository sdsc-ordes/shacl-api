from fastapi import FastAPI, Request, Form
import subprocess
import os
import base64

from rdflib import Graph
from rdflib.namespace import Namespace

import json

app = FastAPI()
SHAPES_PATH = os.getenv("SHAPES_PATH", "data/shapes.ttl")


@app.get("/")
def index():
    return {
        "title": "Hello, welcome to the SHACL API v0.0.5. Compatible with Ontology v0.8."
    }


@app.post("/validate-jsonld")
async def validateJsonLD(
    item: Request,
    jsonInput: bool | None = None,
    jsonOutput: bool | None = None,
    verbose: bool | None = None,
):
    data = await item.json()
    data = data["data"]
    if verbose:
        print(data)

    if jsonInput:
        if verbose:
            print("Assuming json")
            print(f"Type: {type(data)}")
            print("Cleaning newlines")
        data = json.dumps(data)
    else:
        if verbose:
            print("Assuming string")
            print(f"Type: {type(data)}")
            print("Cleaning newlines")
        data = data.splitlines()
        data = " ".join(data)

    # This is generating the datafile necesary to run inference.
    graph = Graph()
    graph.parse(data=data, format="json-ld")

    SCHEMA = Namespace("http://schema.org/")
    graph.namespace_manager.bind("schema", SCHEMA, override=True, replace=True)
    ttl_input = str(graph.serialize(destination="datafile.ttl", format="turtle"))

    output = subprocess.run(
        ["shaclvalidate.sh", "-datafile", "datafile.ttl", "-shapesfile", SHAPES_PATH],
        stdout=subprocess.PIPE,
    )

    os.remove("datafile.ttl")

    ### Read and provide JSON-LD
    graph = Graph()
    graph.parse(data=output.stdout, format="turtle")
    SCHEMA = Namespace("http://schema.org/")
    graph.namespace_manager.bind("schema", SCHEMA, override=True, replace=True)
    jsonld = str(graph.serialize(format="json-ld"))

    if jsonOutput:
        jsonld = json.loads(jsonld)

    return {
        "jsonldOutput": jsonld,
        "ttlOutput": output.stdout,
        "jsonldInput": data,
        "ttlInput": ttl_input,
    }


@app.post("/inference-jsonld")
async def inferenceJsonLD(
    item: Request,
    jsonInput: bool | None = None,
    jsonOutput: bool | None = None,
    verbose: bool | None = None,
):
    data = await item.json()
    data = data["data"]
    if verbose:
        print(data)

    if jsonInput:
        if verbose:
            print("Assuming json")
            print(f"Type: {type(data)}")
            print("Cleaning newlines")
        data = json.dumps(data)
    else:
        if verbose:
            print("Assuming string")
            print(f"Type: {type(data)}")
            print("Cleaning newlines")
        data = data.splitlines()
        data = " ".join(data)

    # This is generating the datafile necesary to run inference.
    graph = Graph()
    graph.parse(data=data, format="json-ld")

    SCHEMA = Namespace("http://schema.org/")
    graph.namespace_manager.bind("schema", SCHEMA, override=True, replace=True)
    ttl_input = str(graph.serialize(destination="datafile.ttl", format="turtle"))

    output = subprocess.run(
        ["shaclinfer.sh", "-datafile", "datafile.ttl", "-shapesfile", "SHAPES_PATH"],
        stdout=subprocess.PIPE,
    )

    os.remove("datafile.ttl")

    ### Read and provide JSON-LD
    graph = Graph()
    graph.parse(data=output.stdout, format="turtle")
    SCHEMA = Namespace("http://schema.org/")
    graph.namespace_manager.bind("schema", SCHEMA, override=True, replace=True)
    jsonld = str(graph.serialize(format="json-ld"))

    if jsonOutput:
        jsonld = json.loads(jsonld)

    return {
        "jsonldOutput": jsonld,
        "ttlOutput": output.stdout,
        "jsonldInput": data,
        "ttlInput": ttl_input,
    }


@app.post("/validate")
def validate(datafile: str = Form(...), shapesfile: str = Form(...)):
    datafile = base64.b64decode(str.encode(datafile))
    shapesfile = base64.b64decode(str.encode(shapesfile))

    # TODO: use tempfile package
    with open("datafile.ttl", "wb") as f:
        f.write(datafile)

    with open("shapesfile.ttl", "wb") as f:
        f.write(shapesfile)

    output = subprocess.run(
        [
            "shaclvalidate.sh",
            "-datafile",
            "datafile.ttl",
            "-shapesfile",
            "shapesfile.ttl",
        ],
        stdout=subprocess.PIPE,
    )

    os.remove("datafile.ttl")
    os.remove("shapesfile.ttl")
    with open("validationTest.ttl", "wb") as f:
        f.write(output.stdout)

    return {"output": output.stdout}


@app.post("/inference")
def inference(datafile: str = Form(...), shapesfile: str = Form(...)):
    datafile = base64.b64decode(str.encode(datafile))
    shapesfile = base64.b64decode(str.encode(shapesfile))
    print(datafile)

    # TODO: use tempfile package
    with open("datafile.ttl", "wb") as f:
        f.write(datafile)

    with open("shapesfile.ttl", "wb") as f:
        f.write(shapesfile)

    output = subprocess.run(
        ["shaclinfer.sh", "-datafile", "datafile.ttl", "-shapesfile", "shapesfile.ttl"],
        stdout=subprocess.PIPE,
    )

    os.remove("datafile.ttl")
    os.remove("shapesfile.ttl")
    with open("validationTest.ttl", "wb") as f:
        f.write(output.stdout)

    return {"output": output.stdout}
