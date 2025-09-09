set positional-arguments
set dotenv-load
set shell := ["bash", "-cue"]

version := env("VERSION", `git describe --tags --abbrev=0`)
image := "ghcr.io/sdsc-ordes/shacl-api"
root_dir := justfile_dir()
export SHACLROOT := root_dir / "external/shacl/bin"
export PATH := SHACLROOT + x":${PATH}"

# Default recipe to list all recipes.
[private]
default:
  just --list --no-aliases

# Setup project for development
install:
  rm -f uv.lock && \
    uv pip install -e '.[webapp,test,dev]'

# Fetch external dependencies
fetch:
  vendir sync --locked -f vendir.yaml --chdir external
  chmod -R u+x external/shacl/bin

# Lint python code
lint: install
  uv run ruff check src

# Run unit tests
test *args: install
  uv run pytest {{args}}

# Run the API server
serve shapes_path opts="": install
  SHAPES_PATH="{{shapes_path}}" uv run python \
    -m uvicorn \
    src.shacl_api.server:app \
      --host 0.0.0.0 \
      --port 15400 \
      {{opts}}

# Serve and reload on file changes
watch shapes_path:
  just serve {{shapes_path}} "--reload"

alias dev := nix-develop
# Enter a Nix development shell.
nix-develop *args:
  @echo "Starting nix developer shell in './tools/nix/flake.nix'."
  @cd "{{root_dir}}" && \
  cmd=("$@") && \
  { [ -n "${cmd:-}" ] || cmd=("zsh"); } && \
  nix develop ./tools/nix#default --accept-flake-config --command "${cmd[@]}"

# Manage kubernetes manifests.
mod manifests 'tools/just/manifests.just'
# Manage container images.
mod image 'tools/just/image.just'
