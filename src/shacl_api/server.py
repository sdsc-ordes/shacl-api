import base64
from enum import Enum
import os
import subprocess
import tempfile
from typing import Annotated, BinaryIO, IO, Optional, Union

from fastapi import FastAPI, File, Header, Request, Response, UploadFile
from pydantic import BaseModel
from rdflib import Graph
from rdflib.namespace import Namespace


app = FastAPI()
SHAPES_PATH = os.getenv("SHAPES_PATH", "data/shapes.ttl")


@app.get("/")
def index():
    return {
        "title": "Hello, welcome to the SHACL API v0.0.5. Compatible with Ontology v0.8."
    }

class RdfMimeType(str, Enum):
    """MIME types for supported RDF serialization formats."""
    jsonld = "application/ld+json"
    json = "application/json"
    turtle = "text/turtle"
    ntriples = "application/n-triples"
    rdfxml = "application/rdf+xml"
    
    def to_rdflib(self):
        match self:
            case RdfMimeType.jsonld:
                return "json-ld"
            case RdfMimeType.json:
                return "json-ld"
            case RdfMimeType.turtle:
                return "turtle"
            case RdfMimeType.ntriples:
                return "ntriples"
            case RdfMimeType.rdfxml:
                return "xml"

class FormatHeaders(BaseModel):
    """Common headers for RDF formats."""
    accept: RdfMimeType = RdfMimeType.jsonld

def convert_rdf_file(file: IO[bytes], from_format: str, to_format="turtle") -> IO[bytes]:
    """Convert RDF data to Turtle format if not already in Turtle."""
    tmp = tempfile.NamedTemporaryFile(delete=False, delete_on_close=False)
    if from_format == to_format:
        tmp.write(file.read())
    else:
        g = Graph()
        g.parse(file, format=from_format)
        tmp.write(g.serialize(format=to_format).encode())
    tmp.close()
    return tmp

@app.post("/validate", )
def validate(
    data: Annotated[
        UploadFile,
        File(description="RDF file with instance data to validate.")
    ],
    shapes: Annotated[
        Union[UploadFile, str, None],
        File(description="SHACL shapes file, by default None.")
    ] = None,
    headers: Annotated[
        FormatHeaders,
        Header(description="Request headers for RDF format")] = FormatHeaders(),
):
    """Validate RDF instance data against SHACL shapes. If shapes are omitted, the default shapes file from the server is used. Supported file formats are rdf-xml, turtle, json-ld and ntriples."""

    if shapes is None or isinstance(shapes, str):
        shapes_file = open(SHAPES_PATH, 'rb')
    else:
        shapes_file = convert_rdf_file(
            shapes.file,
            from_format=RdfMimeType(shapes.content_type).to_rdflib()
        )
    data_file = convert_rdf_file(
        data.file,
        from_format=RdfMimeType(data.content_type).to_rdflib()
    )

    output = subprocess.run(
        [
            #"shaclvalidate.sh",
            #"-datafile",
            "cat",
            data_file.name,
            #"-shapesfile",
            #shapes_file.name,
        ],
        stdout=subprocess.PIPE,
    )

    if isinstance(shapes, UploadFile) and shapes_file.name != SHAPES_PATH:
        os.unlink(shapes_file.name)
    os.unlink(data_file.name)

    if headers.accept == RdfMimeType.turtle:
        report = output.stdout
    else:
        report = (
            Graph()
            .parse(data=output.stdout, format="turtle")
            .serialize(format=RdfMimeType(headers.accept).to_rdflib())
        )

    return Response(content=report, media_type=headers.accept)


@app.post("/inference")
def inference(
    data: Annotated[UploadFile, File()],
    shapes: Annotated[Optional[UploadFile], File()] = None,
    headers: Annotated[FormatHeaders, Header()] = FormatHeaders(),
):

    output = subprocess.run(
        ["shaclinfer.sh", "-datafile", "datafile.ttl", "-shapesfile", "shapesfile.ttl"],
        stdout=subprocess.PIPE,
    )

    os.remove("datafile.ttl")
    os.remove("shapesfile.ttl")
    with open("validationTest.ttl", "wb") as f:
        f.write(output.stdout)

    return {"output": output.stdout}
