import os
import tempfile
from typing import Annotated, Union

from fastapi import FastAPI, File, Header, UploadFile
from fastapi.responses import FileResponse
from pydantic import BaseModel

from . import __version__
from .io import convert_rdf_file
from .mimetypes import RdfMimeType
from .run import ShaclCommand, run_shacl

description = """

## Context

REST API wrapping [TOPBraid's SHACL validation tool](http://github.com/topquadrant/shacl) to allow remote validation of instance data.

## Usage

The API allows SHACL validation and inference via dedicated endpoints.
If you do not provide your custom shapes, the server will use its configured default shapes.

You can control RDF serialization formats through appropriate http headers.

## Resources

* [Repository](https://github.com/sdsc-ordes/shacl-api)
* [Example requests](https://github.com/sdsc-ordes/shacl-api/tree/main/examples/requests)
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


class FormatHeaders(BaseModel):
    """Common headers for RDF formats."""
    accept: RdfMimeType = RdfMimeType.jsonld


def _wrap_shacl(mode: ShaclCommand, data: UploadFile, shapes: Union[UploadFile, str, None], headers: FormatHeaders):
    """Wrap SHACL command execution and RDF format conversion for use in endpoints."""

    # Fall back on server shapes if none are provided
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
        report_ttl = run_shacl(mode, data_ttl.name, shapes_ttl.name)

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
    return _wrap_shacl(ShaclCommand.validate, data, shapes, headers)


@app.post("/infer", )
def infer(
    data: Annotated[
        UploadFile,
        File(description="RDF file with instance data on which to run inference.")
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

    return _wrap_shacl(ShaclCommand.infer, data, shapes, headers)
