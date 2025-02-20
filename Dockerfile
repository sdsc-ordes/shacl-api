FROM ghcr.io/ashleycaselli/shacl:1.4.3_89205df


ENV PYTHONUNBUFFERED=1

RUN apk update && apk add \
    bash \
    curl \
    python3 \
    py3-pip \
    py3-pyarrow \
    shadow \
    && rm -rf /var/lib/apt/lists/*

RUN groupadd --gid 1000 appuser \
    && useradd --uid 1000 --gid 1000 -m appuser

USER appuser
WORKDIR /shacl
COPY requirements.txt requirements.txt

RUN pip3 install --break-system-packages -r requirements.txt && \
  pip3 install --break-system-packages python-multipart streamlit rdflib

COPY ./app app
COPY ./tests tests

ENV PATH="${PATH}:/home/appuser/.local/bin"

ENTRYPOINT ["bash", "/shacl/app/entrypoint.sh"]
