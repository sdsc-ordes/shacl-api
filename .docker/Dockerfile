FROM ghcr.io/ashleycaselli/shacl:1.4.3_89205df AS base

### API-only build-stage ###
FROM base AS api

ENV SHAPES_FILE_URL=https://github.com/sdsc-ordes/imaging-plaza-ontology/releases/download/v0.8/ImagingOntologyCombined.ttl.gz
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
COPY . .

RUN pip3 install --break-system-packages -e . 

EXPOSE 15400

ENTRYPOINT ["bash", "/shacl/src/entrypoint.sh", "api"]

### API + Webapp build-stage ###
FROM api AS webapp

USER root
RUN apk update && apk add \
    py3-pyarrow \
    && rm -rf /var/lib/apt/lists/*
USER appuser

RUN pip3 install --break-system-packages -e '.[webapp]'

ENV PATH="${PATH}:/home/appuser/.local/bin"
EXPOSE 8501

ENTRYPOINT ["bash", "/shacl/app/entrypoint.sh", "webapp"]

