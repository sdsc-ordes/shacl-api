# shaclAPI

Web server for RDF data validation, wrapping the TopBraid Shacl API tool. 
Based on https://github.com/SDSC-ORD/shacl

## Setup

### Requirements

* just: This repository contains a [justfile](./justfile), and we use [`just`](https://github.com/casey/just) as a command runner.
* nix: We provide all the tools you need to work on this project in a nix development shell. See here to install nix: https://determinate.systems/nix-installer/
* docker: Only required to build and run the containerized api.

## Usage

### Get started

First, enter the dev-shell:

```bash
just dev
```

Then fetch the third party [shacl](https://github.com/topquadrant/shacl) tool:

```bash
just fetch
```

Finally, start the server:

```bash
just serve ./tests/data/val_ok_shapes.ttl
```

> [!NOTE]
> Alternatively, if just is not installed, you may enter the devshell directly with:
> `nix develop ./tools/nix#default --accept-flake-config --command "zsh"`

Containers use the `.env` file in the repository, before running them, you should copy `.env.dist` to `.env` and set desired values for your shapes.

### With nix

The nix dev-shell contains all dependencies to run the project. Once you're inside, you can run `just serve` to start the server, or `just watch` to automatically reload it on file changes.

This is recommended for development.


### With docker

We build two docker images, a small "headless" version with only the REST server, and a larger image that bundles the REST server and a streamlit web application. These two images are differentiated by their tag: `<version>` vs `<version>-webapp`.

```bash
just image build
```

The docker images can be run as follows:

```
# Only REST API
docker run -it --rm -p 8000:15400 --env-file .env ghcr.io/sdsc-ordes/shacl-api:latest 

# REST API + web server
docker run -it --rm -p 8000:15400 -p 8501:8501 --env-file .env ghcr.io/sdsc-ordes/shacl-api:latest-webapp
# or
just image run
```

### With docker compose

For development, it may be more convenient to use our docker compose stack.

```
just image compose-up
```

## Deployment

We provide manifests to deploy the service on kubernetes.
The manifest templates in [tools/deploy](tools/deploy) are managed with ytt and can be rendered using:

```bash
just manifests render
```

Or deployed directly with:

```bash
just manifests deploy
```
