#!/bin/bash
DIRNAME=`dirname $0`
TODAY=`date +%Y-%m-%d`
SCHEMA=louis_v002
NAME=$DIRNAME/dumps/$SCHEMA/schema.sql
if [ ! -f "$NAME" ]; then
    pg_dump --no-owner --no-privileges --no-security-labels --no-table-access-method --no-tablespaces --schema-only -n $SCHEMA -d inspection.canada.ca | grep -v "^SET" > $NAME
else
    echo "File $NAME already exists"
fi
