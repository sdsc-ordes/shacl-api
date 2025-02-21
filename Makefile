VERSION = latest
IMAGE = ghcr.io/sdsc-ordes/shacl-api
CONTAINER_RUNTIME ?= docker

.PHONY: docker-build
docker-build: ## Build Docker images
	@echo "🐋 Building docker image"

	$(CONTAINER_RUNTIME) build \
		-f .docker/Dockerfile \
		-t $(IMAGE):$(VERSION) \
		--build-arg VERSION=$(VERSION) \
		--target api .

	$(CONTAINER_RUNTIME) build \
		-f .docker/Dockerfile \
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
		-f .docker/compose.yml \
		up --build

.PHONY: help
help:
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

.DEFAULT_GOAL := help
