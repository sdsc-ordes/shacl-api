#FROM python:3.9
FROM ghcr.io/sdsc-ord/shacl:latest

RUN apt-get update

RUN apt-get install -y python3 pip

RUN pip install fastapi uvicorn

COPY ./app /app
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "15400"]