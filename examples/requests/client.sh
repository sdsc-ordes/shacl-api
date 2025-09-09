#!/usr/bin/env bash

set -euo pipefail

URL='http://localhost:8001/validate'
HEADERS=( \
  -H "Content-Type: multipart/form-data" \
  -H "Accept: application/n-triples" \
)

# Providing both data and shapes:
curl \
  -X POST \
  -F "data=@tests/data/val_ok_shapes.ttl;type=text/turtle" \
  -F "shapes=@tests/data/val_ok_data.ttl;type=text/turtle" \
  "${HEADERS[@]}" \
  "${URL}"

# Validate input data with default server shapes:

curl \
  -X POST \
  -F "data=@tests/data/val_ok_data.ttl;type=text/turtle" \
  "${HEADERS[@]}" \
  "${URL}"
