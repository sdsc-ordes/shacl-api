FROM ghcr.io/ashleycaselli/shacl:1.4.3_89205df AS base
ARG VERSION=latest

### API-only build-stage ###
FROM base AS api

# Metadata
LABEL org.opencontainers.image.source="https://github.com/sdsc-ordes/shacl-api"
LABEL org.opencontainers.image.licenses="AGPL-3.0"
LABEL org.opencontainers.image.title="SHACL API"
LABEL org.opencontainers.image.description="API for validating RDF data against SHACL shapes."
LABEL org.opencontainers.image.version=${VERSION}

# unset or set to "" to disable shapes download
ENV SHAPES_URL="https://github.com/sdsc-ordes/imaging-plaza-ontology/releases/download/v0.8/ImagingOntologyCombined.ttl.gz"
ENV SHAPES_PATH="/data/shapes.ttl"
ENV PATH="${PATH}:/home/appuser/.local/bin"

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

RUN mkdir -p $(dirname ${SHAPES_PATH}) && chown -R appuser:appuser $(dirname ${SHAPES_PATH})
USER appuser
WORKDIR /shacl-api
ADD LICENSE README.md CHANGELOG pyproject.toml uv.lock .
ADD src ./src
# give permissions on /shacl-api/data to appuser
COPY ./tools/image/entrypoint.sh /entrypoint.sh

ENV PYTHONUNBUFFERED=1
RUN pip3 install --break-system-packages -e . 

EXPOSE 15400

ENTRYPOINT ["bash", "/entrypoint.sh", "api"]

### API + Webapp build-stage ###
FROM api AS webapp

LABEL org.opencontainers.image.version=${VERSION}-webapp

USER root
RUN apk update && apk add \
    py3-pyarrow \
    && rm -rf /var/lib/apt/lists/*
USER appuser

RUN pip3 install --break-system-packages -e '.[webapp]'


EXPOSE 8501

ENTRYPOINT ["bash", "/entrypoint.sh", "webapp"]

