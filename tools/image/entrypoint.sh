#!/bin/bash

set -e

extract_file() {
    EXT="$1"
    ARCHIVE="$2"
    OUTPUT="$3"

    case "$EXT" in
        gz)
            gzip -dc "$ARCHIVE" > "$OUTPUT"
            ;;
        zip)
            unzip -p "$ARCHIVE" > "$OUTPUT"
            ;;
        tgz)
            tar -xzOf "$ARCHIVE" > "$OUTPUT"
            ;;
        *)
            mv "$ARCHIVE" "$OUTPUT"
            ;;
    esac
}

# Download and extract shapes
if ! [ -z "$SHAPES_URL" ]; then
  TMP_FILE=$(mktemp)
  curl -fsSL "$SHAPES_URL" -o "$TMP_FILE"
  extract_file "${SHAPES_URL##*.}" "$TMP_FILE" "${SHAPES_PATH}"
fi

# Start webapp if enabled
if [ "$1" == "webapp" ]; then
    nohup streamlit run /shacl-api/src/shacl_api/webapp.py &
fi

# Start API server
python3 -m uvicorn src.shacl_api.server:app --host 0.0.0.0

