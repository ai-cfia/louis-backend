#!/bin/bash
TODAY=`date +%Y-%m-%d`
NAME=dumps/inspection.canada.ca.$TODAY.pg_dump
if [ ! -f "$NAME" ]; then
    pg_dump -d inspection.canada.ca > $NAME
fi

if [ ! -f "$NAME.zip" ]; then
    zip $NAME.zip $NAME
fi
