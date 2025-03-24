import base64
from enum import Enum
import os
import subprocess
import tempfile
from typing import Annotated, BinaryIO, IO, Optional, Union

from fastapi import FastAPI, File, Header, Request, Response, UploadFile
from fastapi.responses import FileResponse
from pydantic import BaseModel
from rdflib import Graph
from rdflib.namespace import Namespace

from . import __version__

description = """

## Context

REST API wrapping [TOPBraid's SHACL validation tool](http://github.com/topquadrant/shacl) to allow remote validation of instance data.

## Usage

The API allows SHACL validation and inference via dedicated endpoints. If you do not provide your custom shapes, the server will use its configured default shapes.

You can control RDF serialization formats through appropriate http headers.

"""

app = FastAPI(
    title="shacl-api",
    description=description,
    summary="Validate RDF files against SHACL shapes.",
    version=__version__,
    contact={
        "name": "Swiss Data Science Center",
        "url": "https://datascience.ch",
        "email": "contact@datascience.ch",
    },
    license_info={
        "name": "AGPL-3.0",
        "identifier": "AGPL-3.0-or-later",
    },
)
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
        """Translates mimetypes to rdflib format names."""
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

class ShaclCommand(str, Enum):
    """Supported SHACL commands."""
    validate = "shaclvalidate.sh"
    infer = "shaclinfer.sh"

def run_shacl(mode: ShaclCommand, data: IO[bytes], shapes: IO[bytes]) -> IO[bytes]:
    report_file = tempfile.NamedTemporaryFile(delete=False, delete_on_close=False)
    _ = subprocess.run(
        [mode.value, "-datafile", data.name, "-shapesfile", shapes.name],
        stdout=report_file,
    )
    
    return report_file


    

@app.post("/validate", )
def validate(
    data: Annotated[
        UploadFile,
        File(description="RDF file with instance data to validate.")
    ],
    shapes: Annotated[
        Union[UploadFile, str, None],
        File(description="SHACL shapes file. Default: None.")
    ] = None,
    headers: Annotated[
        FormatHeaders,
        Header(description="Request headers for RDF format")] = FormatHeaders(),
):
    """Validate RDF instance data against SHACL shapes. If shapes are omitted, the default shapes file from the server is used. Supported file formats are rdf-xml, turtle, json-ld and ntriples."""

    # Convert input data to turtle format
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

    # Run validation
    report_file = run_shacl(ShaclCommand.validate, data_file, shapes_file)

    # Convert report to requested format
    output_file = convert_rdf_file(
        report_file,
        from_format="turtle",
        to_format=RdfMimeType(headers.accept).to_rdflib()
    )

    try:
        return FileResponse(output_file.name, media_type=headers.accept)
    finally:
        # Cleanup temporary files
        if isinstance(shapes, UploadFile) and shapes_file.name != SHAPES_PATH:
            os.unlink(shapes_file.name)
        for tmp in (data_file, report_file, output_file):
            os.unlink(tmp.name)

@app.post("/infer", )
def infer(
    data: Annotated[
        UploadFile,
        File(description="RDF file with instance data to validate.")
    ],
    shapes: Annotated[
        Union[UploadFile, str, None],
        File(description="SHACL shapes file. Default: None.")
    ] = None,
    headers: Annotated[
        FormatHeaders,
        Header(description="Request headers for RDF format")] = FormatHeaders(),
):
    """Runs SHACL inference on RDF instance data using provided shapes. If shapes are omitted, the default shapes file from the server is used. Supported file formats are rdf-xml, turtle, json-ld and ntriples."""

    output = subprocess.run(
        ["shaclinfer.sh", "-datafile", "datafile.ttl", "-shapesfile", "shapesfile.ttl"],
        stdout=subprocess.PIPE,
    )

    os.remove("datafile.ttl")
    os.remove("shapesfile.ttl")
    with open("validationTest.ttl", "wb") as f:
        f.write(output.stdout)

    return {"output": output.stdout}
