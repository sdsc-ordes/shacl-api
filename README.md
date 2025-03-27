# shaclAPI

Web server for RDF data validation, wrapping the TopBraid Shacl API tool. 
Based on https://github.com/SDSC-ORD/shacl

## How to use it?

### Setup

This repository contains a [justfile](./justfile), and we use [`just`](https://github.com/casey/just) as a command runner.

We provide all the tools you need to work on this project in a nix development shell.
See here to install nix: https://determinate.systems/nix-installer/

To enter the dev-shell, run:

```shell
just dev
```

> [!NOTE]
> Alternatively, you may enter the devshell directly with :
> `nix develop ./tools/nix#default --accept-flake-config --command "zsh"`

The server and containers use the `.env` file in the repository, before running them, you should copy `.env.dist` to `.env` and set desired values for the variables inside.

### With nix

The nix dev-shell contains all dependencies to run the project. Once you're inside, you can run `just serve` to start the server, or `just watch` to automatically reload it when the source files changes.

This is recommended for development.

> [!TIP]
> If the variables in your `.env` are set up for the docker image, you may want to override the variable directly, e.g. `SHAPES_PATH=./tests/data/val_ok_shapes.ttl just serve`

### With docker

We build two docker images, a small "headless" version with only the REST server, and a larger image that bundles the REST server and a streamlit web application. These two images are differentiated by their tag: `<version>` vs `<version>-webapp`.

```shell
just docker build
```

The docker images can be run as follows:

```
# Only REST API
docker run -it --rm -p 8000:15400 --env-file .env ghcr.io/sdsc-ordes/shacl-api:latest 

# REST API + web server
docker run -it --rm -p 8000:15400 -p 8501:8501 --env-file .env ghcr.io/sdsc-ordes/shacl-api:latest-webapp
# or
just docker run
```

### With docker compose

For development, it may be more convenient to use our docker compose stack.

```
just docker compose-up
```

## Deployment

We provide manifests to deploy the service on kubernetes.
The manifest templates in [tools/deploy](tools/deploy) are managed with ytt and can be rendered using:

```shell
just manifests render
```

Or deployed directly with:

```shell
just manifests deploy
```
