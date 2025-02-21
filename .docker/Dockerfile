ARG VERSION=latest

FROM ghcr.io/ashleycaselli/shacl:1.4.3_89205df AS base

### API-only build-stage ###
FROM base AS api

# Metadata
LABEL org.opencontainers.image.source https://github.com/sdsc-ordes/shacl-api
LABEL org.opencontainers.image.licenses AGPL-3.0
LABEL org.opencontainers.image.title "SHACL API"
LABEL org.opencontainers.image.description "API for validating RDF data against SHACL shapes."
LABEL org.opencontainers.image.version ${VERSION}

# Environment
ENV API_PORT=15400
ENV WEBAPP_PORT=8501
ENV SHAPES_PATH=/data/shapes.ttl
ENV SHAPES_URL='https://github.com/sdsc-ordes/imaging-plaza-ontology/releases/download/v0.8/ImagingOntologyCombined.ttl.gz'

RUN apk update && apk add \
    bash \
    curl \
    gzip \
    python3 \
    py3-pip \
    shadow \
    tar \
    zip \
    && rm -rf /var/lib/apt/lists/*

RUN groupadd --gid 1000 appuser \
    && useradd --uid 1000 --gid 1000 -m appuser

USER appuser
WORKDIR /shacl
COPY . .

ENV PYTHONUNBUFFERED=1
RUN pip3 install --break-system-packages -e . 

EXPOSE ${API_PORT}

ENTRYPOINT ["bash", "/shacl/.docker/entrypoint.sh", "api"]

### API + Webapp build-stage ###
FROM api AS webapp

LABEL org.opencontainers.image.version ${VERSION}-webapp

USER root
RUN apk update && apk add \
    py3-pyarrow \
    && rm -rf /var/lib/apt/lists/*
USER appuser

RUN pip3 install --break-system-packages -e '.[webapp]'

ENV PATH="${PATH}:/home/appuser/.local/bin"

EXPOSE ${WEBAPP_PORT}

ENTRYPOINT ["bash", "/shacl/.docker/entrypoint.sh", "webapp"]

