# We assume all encrypted secrets follow the naming pattern {{SECRET_DIR}}/*{{ENC_SUFFIX}}
set positional-arguments
set shell := ["bash", "-cue"]
root_dir := `git rev-parse --show-toplevel`
ctr := "docker"
version := `git describe --tags --abbrev=0`
image := "ghcr.io/sdsc-ordes/gimie-api:" + version
image_dir := root_dir + "/tools/image"

# Default recipe to list all recipes.
[private]
default:
  just --list image --no-aliases

_build *args:
  cd {{root_dir}} && \
    {{ctr}} build \
      -f "{{image_dir}}/Dockerfile" \
      --build-arg VERSION={{version}} \
      {{args}} \
      .


# Build Docker images
build *args:
  @echo "🐋 Building docker image"
  just image _build {{args}} --target=api -t {{image}}
  just image _build {{args}} --target=webapp -t {{image}}-webapp

# Run docker image
run *args: build
  cd {{root_dir}} && \
    {{ctr}} run \
      --env-file .env \
      -p 8000:15400 \
      -p 8501:8501 \
      {{args}} \
      {{image}}-webapp

# Push Docker images
push *args: build
  @echo "🐋 Pushing docker image"
  cd {{root_dir}} && \
    {{ctr}} push {{args}} {{image}} && \
    {{ctr}} push {{args}} {{image}}-webapp

# Start the Docker Compose stack
compose-up *args: 
  @echo "🐋 Running docker-compose"
  cd {{root_dir}} && \
    {{ctr}} compose \
      --env-file .env \
      --project-directory "{{root_dir}}" \
      -f "{{image_dir}}/compose.yml" \
      up --build {{args}}

