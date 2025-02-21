# shaclAPI

Web server for RDF data validation, wrapping the TopBraid Shacl API tool. 
Based on https://github.com/SDSC-ORD/shacl

## How to use it?


### With docker

We provide a helper make recipe to build two docker images, a small "headless" version with only the REST server, and a larger image that bundles the REST server and a streamlit web application. These two images are differentiated by their tag: `<version>` vs `<version>-webapp`.

```
make docker-build
```

The docker images can be run as follows:

```
# Only REST API
docker run -it --rm -p 8000:15400 sdsc-ordes/shacl-api:latest 
# REST API + web server
docker run -it --rm -p 8000:15400 -p 8501:8501 sdsc-ordes/shacl-api:latest-webapp
```


## With docker compose

For development, it may be more convenient to use our docker compose stack.

```
make docker-compose-up
```
