#!/bin/bash

set -e

extract_file() {
    ARCHIVE="$1"
    OUTPUT="$2"

    case "$ARCHIVE" in
        *.gz)
            gzip -dc "$ARCHIVE" > "$OUTPUT"
            ;;
        *.zip)
            unzip -p "$ARCHIVE" > "$OUTPUT"
            ;;
        *.tar.gz|*.tgz)
            tar -xzOf "$ARCHIVE" > "$OUTPUT"
            ;;
        *)
            mv "$ARCHIVE" "$OUTPUT"
            ;;
    esac
}

# Download and extract shapes
if [ -z "$SHAPES_URL" ]; then
  mkdir -p "$(dirname "$SHAPES_PATH")"
  TMP_FILE=$(mktemp)
  curl -fsSL "$SHAPES_URL" -o "$TMP_FILE"
  extract_file "$TMP_FILE" "$SHAPES_PATH"
fi

# Start webapp if enabled
if [ "$1" == "webapp" ]; then
    nohup streamlit run /shacl/src/shacl-api/webapp.py --server.port "${WEBAPP_PORT:-8501}" &
fi

# Start API server
python3 -m uvicorn src.shacl-api.server:app --host 0.0.0.0 --port "${API_PORT:-15400}"

