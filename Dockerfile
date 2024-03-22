FROM ghcr.io/sdsc-ordes/shacl:1.4.2_b8973a6

RUN apt-get update

RUN apt-get install -y python3 pip

RUN pip install fastapi uvicorn python-multipart

RUN pip install streamlit rdflib

COPY ./app /app
COPY ./tests /tests

ENTRYPOINT ["bash", "/app/entrypoint.sh"]