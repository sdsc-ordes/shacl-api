FROM ghcr.io/ashleycaselli/shacl:1.4.3_89205df

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
#  pip3 install --break-system-packages python-multipart streamlit rdflib


EXPOSE 15400

ENTRYPOINT ["bash", "/shacl/src/entrypoint.sh"]
