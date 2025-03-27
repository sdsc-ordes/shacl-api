from __future__ import annotations
from enum import Enum


class RdfMimeType(str, Enum):
    """MIME types for supported RDF serialization formats."""

    jsonld = "application/ld+json"
    json = "application/json"
    turtle = "text/turtle"
    ntriples = "application/n-triples"
    rdfxml = "application/rdf+xml"

    def to_extension(self) -> str:
        """Translates mimetypes to file extensions."""
        match self:
            case RdfMimeType.jsonld:
                return "json"
            case RdfMimeType.json:
                return "json"
            case RdfMimeType.turtle:
                return "ttl"
            case RdfMimeType.ntriples:
                return "nt"
            case RdfMimeType.rdfxml:
                return "rdf"

    @classmethod
    def from_extension(cls, extension: str) -> RdfMimeType:
        """Translates file extensions to mimetypes."""
        match extension:
            case "json" | "jsonld":
                return cls.jsonld
            case "ttl" | "turtle":
                return cls.turtle
            case "nt" | "ntriples":
                return cls.ntriples
            case "rdf" | "xml":
                return cls.rdfxml
            case _:  # default
                raise ValueError(f"Unsupported file extension: {extension}")

    def to_rdflib(self) -> str:
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
