#FROM python:3.9
FROM ghcr.io/sdsc-ord/shacl:latest

RUN apt-get update

RUN apt-get install -y python3 pip

RUN pip install fastapi uvicorn python-multipart

RUN pip install streamlit

COPY ./app /app
COPY ./tests /tests
#WORKDIR /app
ENTRYPOINT ["bash", "/app/entrypoint.sh"]
#ENTRYPOINT ["bash"]
#ENTRYPOINT ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "15400"]