import shutil
from typing import IO

from rdflib import Graph


def convert_rdf_file(
    in_file: IO[bytes],
    to_file: IO[bytes],
    in_format: str = "turtle",
    to_format: str = "turtle",
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
