# grep version from __init__.py
VERSION := $(shell grep __version__ src/shacl-api/__init__.py | cut -d '"' -f 2)
IMAGE = ghcr.io/sdsc-ordes/shacl-api
CONTAINER_RUNTIME ?= docker

.PHONY: docker-build
docker-build: ## Build Docker images
	@echo "🐋 Building docker image"

	$(CONTAINER_RUNTIME) build \
		-f tools/docker/Dockerfile \
		-t $(IMAGE):$(VERSION) \
		--build-arg VERSION=$(VERSION) \
		--target api .

	$(CONTAINER_RUNTIME) build \
		-f tools/docker/Dockerfile \
		-t $(IMAGE):$(VERSION)-webapp \
		--build-arg VERSION=$(VERSION) \
		--target webapp .

.PHONY: docker-push
docker-push: docker-build ## Push Docker images
	@echo "🐋 Pushing docker image"
	$(CONTAINER_RUNTIME) push $(IMAGE):$(VERSION)
	$(CONTAINER_RUNTIME) push $(IMAGE):$(VERSION)-webapp

docker-compose-up: ## Run the Docker Compose stack
	@echo "🐋 Running docker-compose"
	$(CONTAINER_RUNTIME) compose \
		-f tools/docker/compose.yml \
		up --build

.PHONY: format
format: install ## Format python code
	ruff format src

.PHONY: lint
lint: install ## Lint python code
	ruff check src

.PHONY: install
install: ## Setup project for development
	pip install -e '.[webapp,test,dev]'


.PHONY: test
test: install ## Run unit tests
	pytest

.PHONY: help
help:
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

.DEFAULT_GOAL := help
