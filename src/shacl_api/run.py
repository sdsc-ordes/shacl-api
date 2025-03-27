from enum import Enum
from typing import IO
import subprocess
import tempfile


class ShaclCommand(str, Enum):
    """Supported SHACL commands."""

    validate = "shaclvalidate.sh"
    infer = "shaclinfer.sh"


def run_shacl(mode: ShaclCommand, data_path: str, shapes_path: str) -> IO[bytes]:
    """Run the shacl command line tool."""
    report_file = tempfile.NamedTemporaryFile(delete=False, delete_on_close=False)
    _ = subprocess.run(
        [mode.value, "-datafile", data_path, "-shapesfile", shapes_path],
        stdout=report_file,
    )
    report_file.seek(0)

    return report_file
