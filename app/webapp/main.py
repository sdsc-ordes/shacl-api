import streamlit as st
import requests 
import base64
# This interface is for uploading the files and getting the files back 

st.set_page_config(layout="wide")

st.image("https://datascience.ch/wp-content/uploads/2020/09/logo-SDSC-transparent.png", width=200)
st.title("shaclAPI")

cola, colb, colc, _,_,_,_ = st.columns(7)

with cola:
    st.write("Validation and Inference")

with colb:
    option = st.radio("Which analysis would you like to do?",
        ("Validation", "Inference"))
    
with colc:
    port = st.radio("Which port is the API using?",
            ("15400", "8000"))


st.markdown("""---""")
col1, col2, col3 = st.columns(3)
with col1:
    st.markdown("## Datafile")
    datafile = st.file_uploader("datafile")
    if datafile:
        datafile = datafile.read()
        with st.expander("See datafile"):
            st.code(datafile.decode())

        datafile64 = base64.b64encode(datafile)

with col2:
    st.markdown("## ShapesFile")
    shapesfile = st.file_uploader("shapesfile")
    if shapesfile:
        shapesfile = shapesfile.read()
        with st.expander("See shapesfile"):
            st.code(shapesfile.decode())

        shapesfile64 = base64.b64encode(shapesfile)

with col3:
    st.markdown("## SHACL Output")
    calculate = st.button("Calculate")

    if calculate:     
        payload = {"datafile": datafile64,
                "shapesfile": shapesfile64}

        if option == "Validation":
            url = f"http://127.0.0.1:{port}/validate"
        elif option == "Inference":
            url = f"http://127.0.0.1:{port}/inference"

        r = requests.post(url, data=payload)
        output = r.json()["output"]
        with st.expander("See Output"):
            st.code(output, language="ttl") #line_numbers

        st.download_button('Download TTL', output, file_name='output.ttl')


st.markdown("""---""")


col4, col5 = st.columns(2)
with col4:
    st.markdown("## How to use the API in python?")
    with st.expander("See Code"):
        st.code("""
        import requests 
        import base64
        with open('../tests/tests-files/val_imagingID.ttl', 'rb') as file:
            datafile = file.read()

        with open('../tests/tests-files/val_ImagingOntologyShapes.ttl', 'rb') as file:
            shapesfile = file.read()

        datafile64 = base64.b64encode(datafile) 
        shapesfile64 = base64.b64encode(shapesfile)

        payload = {"datafile": datafile64,
                "shapesfile": shapesfile64}

        url = "http://127.0.0.1:8000/validate"
        r = requests.post(url, data=payload)

        output = r.json()["output"]
            
        """, language="python")

with col5:
    st.markdown("## How to use the API in javascript?")
    with st.expander("See Code"):
        st.code("""
        SOON
            
        """, language="python")

st.markdown("""---""")
st.markdown("Developed with <3 by ORDES SDSC Team.")
