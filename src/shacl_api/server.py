from enum import Enum
import os
import shutil
import subprocess
import tempfile
from typing import Annotated, IO, Optional, Union

from fastapi import FastAPI, File, Header, UploadFile
from fastapi.responses import FileResponse
from pydantic import BaseModel
from rdflib import Graph

from . import __version__

description = """

## Context

REST API wrapping [TOPBraid's SHACL validation tool](http://github.com/topquadrant/shacl) to allow remote validation of instance data.

## Usage

The API allows SHACL validation and inference via dedicated endpoints.
If you do not provide your custom shapes, the server will use its configured default shapes.

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

def convert_rdf_file(
    in_file: IO[bytes],
    to_file: IO[bytes],
    in_format: str="turtle",
    to_format: str="turtle",
):
    """Convert RDF data to Turtle format if not already in Turtle."""
    if in_format == to_format:
        # NOTE: may want to symlink instead to remove overhead
        shutil.copyfileobj(in_file, to_file)
    else:
        # WARN: This loads the file in memory
        g = Graph()
        g.parse(in_file, format=in_format)
        to_file.write(g.serialize(format=to_format).encode())
    to_file.seek(0)

class ShaclCommand(str, Enum):
    """Supported SHACL commands."""
    validate = "shaclvalidate.sh"
    infer = "shaclinfer.sh"

def run_shacl(mode: ShaclCommand, data_path: str, shapes_path: str) -> IO[bytes]:
    report_file = tempfile.NamedTemporaryFile(delete=False, delete_on_close=False)
    _ = subprocess.run(
        [mode.value, "-datafile", data_path, "-shapesfile", shapes_path],
        stdout=report_file,
    )
    report_file.seek(0)
    
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
    """Validate RDF instance data against SHACL shapes.
    If shapes are omitted, the default shapes file from the server is used.
    Supported file formats are rdf-xml, turtle, json-ld and ntriples.
    """

    if shapes is None or isinstance(shapes, str):
        shapes_source = open(SHAPES_PATH, 'rb')
        shapes_format = "turtle"
    else:
        shapes_source = shapes.file
        shapes_format = RdfMimeType(shapes.content_type).to_rdflib()

    # Convert inputs to turtle format
    with (
        tempfile.NamedTemporaryFile() as data_ttl,
        tempfile.NamedTemporaryFile() as shapes_ttl,
    ):
        convert_rdf_file(
            in_file=shapes_source,
            to_file=shapes_ttl,
            in_format=shapes_format,
        )
        convert_rdf_file(
            in_file=data.file,
            in_format=RdfMimeType(data.content_type).to_rdflib(),
            to_file=data_ttl,
        )

        # Run validation
        report_ttl = run_shacl(ShaclCommand.validate, data_ttl.name, shapes_ttl.name)

    # Convert report to requested format
    report_file = tempfile.NamedTemporaryFile(delete=False, delete_on_close=False)
    convert_rdf_file(
        in_file=report_ttl,
        to_file=report_file,
        to_format=RdfMimeType(headers.accept).to_rdflib()
    )
    os.remove(report_ttl.name)

    # NOTE: FastAPI automatically deletes the response file
    return FileResponse(report_file.name, media_type=headers.accept)

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
