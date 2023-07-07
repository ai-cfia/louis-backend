#!/bin/bash

if [ -z "$LOUIS_DSN" ]; then
    echo "please set LOUIS_DSN to psql connection string before running"
    echo "export LOUIS_DSN=..."
    exit 1
fi

if [ -z "$1" ]; then
    echo "usage: $0 LOUIS_SCHEMA"
    exit 2
fi

LOUIS_SCHEMA=$1
echo "loading $LOUIS_SCHEMA"
podman run -it --rm \
    -e LOUIS_DSN="$LOUIS_DSN" \
    -e LOUIS_SCHEMA=$LOUIS_SCHEMA \
    -e LOAD_DATA_ONLY=$LOAD_DATA_ONLY \
    -e DISABLE_TRIGGER_ALL=YES \
    -v ./dumps/$LOUIS_SCHEMA:/data \
    localhost/louis-data:nodata