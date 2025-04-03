import json
import os
import streamlit as st
from pathlib import Path
import requests

from shacl_api.mimetypes import RdfMimeType


def get_mimetype(filename: str) -> str:
    ext = Path(filename).suffix.removeprefix(".")

    return RdfMimeType.from_extension(ext).value


# This interface is for uploading the files and getting the files back

DEFAULT_API_PORT = os.environ.get("UVICORN_PORT", "15400")
HOST = "http://localhost"

st.set_page_config(layout="wide")

st.image(
    "https://datascience.ch/wp-content/uploads/2020/09/logo-SDSC-transparent.png",
    width=200,
)
st.title("shaclAPI")

cola, colb, colc, _, _, _, _ = st.columns(7)

with cola:
    st.write("Validation and Inference")

with colb:
    option = st.radio(
        "Which analysis would you like to do?", ("Validation", "Inference")
    )

with colc:
    PORT = st.radio("Which port is the API using?", (f"{DEFAULT_API_PORT}", "8000"))


st.markdown("""---""")
col1, col2, col3 = st.columns(3)
with col1:
    st.markdown("## Data File")
    datafile = st.file_uploader("data")
    if datafile:
        with st.expander("See data file"):
            st.code(datafile.read().decode())
            datafile.seek(0)

with col2:
    st.markdown("## Shapes File")
    shapesfile = st.file_uploader("shapes")
    if shapesfile:
        with st.expander("See shapes file"):
            st.code(shapesfile.read().decode())
            shapesfile.seek(0)

with col3:
    st.markdown("## Validation report")
    calculate = st.button("Calculate")

    if calculate and datafile:
        payload = {
            "data": ("data", datafile, get_mimetype(datafile.name)),
        }

        if shapesfile:
            payload["shapes"] = ("shapes", shapesfile, get_mimetype(shapesfile.name))

        match option:
            case "Validation":
                path = "/validate"
            case "Inference":
                path = "/infer"
            case _:
                raise ValueError("Invalid option")

        url = f"{HOST}:{PORT}{path}"

        r = requests.post(url, files=payload, headers={"Accept": "text/turtle"})
        output = r.text
        with st.expander("See SHACL output"):
            st.code(output)  # line_numbers

        st.download_button("Download report", output, file_name="output.ttl")


st.markdown("""---""")


col4, col5 = st.columns(2)
with col4:
    st.markdown("## How to use the API in python?")
    with st.expander("See Code"):
        st.code(
            f"""
        import requests 
        data_file = open('../tests/data/val_ok_data.ttl', 'rb')
        shapes_file = open('../tests/data/val_ok_shapes.ttl', 'rb')

        payload = {{
            "data": ("data.ttl", data_file, "text/turtle"),
            "shapes": ("shapes.ttl", shapes_file, "text/turtle")
        }}

        url = "{HOST}:{PORT}/validate"
        r = requests.post(url, files=payload, headers={{'Accept': 'application/json'}})

        output = r.json()["output"]
        """,
            language="python",
        )

with col5:
    st.markdown("## How to use the API in javascript?")
    with st.expander("See Code"):
        st.code(
            """
        SOON
            
        """,
            language="javascript",
        )

st.markdown("""---""")
st.markdown("Developed with <3 by ORDES SDSC Team.")
