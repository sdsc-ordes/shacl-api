import streamlit as st
import requests 
import base64
# This interface is for uploading the files and getting the files back 

st.set_page_config(layout="wide")
st.title("shaclAPI")
st.write("Validation and Inference")


option = st.radio("Which analysis would you like to do?",
         ("Validation", "Inference"))

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
            url = "http://127.0.0.1:8000/validate"
        elif option == "Inference":
            url = "http://127.0.0.1:8000/inference"

        r = requests.post(url, data=payload)
        output = r.json()["output"]
        with st.expander("See Output"):
            st.code(output, language="ttl") #line_numbers

        st.download_button('Download TTL', output, file_name='output.ttl')


st.markdown("""---""")

st.markdown("Developed with <3 by ORDES SDSC Team.")