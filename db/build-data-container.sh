#!/bin/bash

DIRNAME=`dirname $0`

if [ -z "$1" ]; then
    echo "usage: $0 LOUIS_SCHEMA"
    exit 1
fi

if [ ! -d "$DIRNAME/dumps/$1" ]; then
    echo "No such schema $1, setting nocopy"
    BUILD_ENV=nocopy
else
    BUILD_ENV=copy
fi

LOUIS_SCHEMA=$1
echo "building $LOUIS_SCHEMA"
podman build --format docker \
    --build-arg LOUIS_SCHEMA=$LOUIS_SCHEMA,BUILD_ENV=$BUILD_ENV \
    -t louis-data:$LOUIS_SCHEMA \
    .