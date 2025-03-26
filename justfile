set positional-arguments
set dotenv-load
set shell := ["bash", "-cue"]

version := `git describe --tags --abbrev=0`
image := "ghcr.io/sdsc-ordes/shacl-api"
root_dir := `git rev-parse --show-toplevel`


# Default recipe to list all recipes.
[private]
default:
  just --list --no-aliases

# Setup project for development
install: 
  uv pip install -e '.[webapp,test,dev]'

# Lint python code
lint: install
  uv run ruff check src

# Run unit tests
test: install 
  uv run pytest

# Fetch external dependencies
fetch:
  vendir sync -f vendir.yaml --chdir external

# Run the API server
serve *args: install
  uv run python -m uvicorn src.shacl_api.server:app --host 0.0.0.0 --port 15400 {{args}}

# Serve and reload on file changes
watch: 
  just serve --reload

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
