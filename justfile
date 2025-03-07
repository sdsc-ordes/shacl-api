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
  pip install -e '.[webapp,test,dev]'

# Lint python code
lint: install
	ruff check src

# Run unit tests
test: install 
	pytest

alias dev := nix-develop
# Enter a Nix development shell.
nix-develop *args:
  @echo "Starting nix developer shell in './tools/nix/flake.nix'."
  @cd "{{root_dir}}" && \
  cmd=("$@") && \
  { [ -n "${cmd:-}" ] || cmd=("zsh"); } && \
  nix develop ./tools/nix#default --accept-flake-config --command "${cmd[@]}"

# Manage manifests.
mod manifests 'tools/just/manifests.just'
# Manage containers.
mod docker 'tools/just/docker.just'
