#!/bin/sh
if [ -z "$LOUIS_DSN" ]; then
    echo "Specify environment variable LOUIS_DSN"
    exit 1
fi
if [ -z "$LOUIS_SCHEMA" ]; then
    echo "Specify environment variable LOUIS_SCHEMA"
    exit 1
fi
if [ -z "$LOAD_DATA_ONLY" ]; then
    psql "$LOUIS_DSN" -v ON_ERROR_STOP=1 --single-transaction -f /data/schema.sql
    if [ "$?" -ne 0 ]; then
        echo "error loading /data/schema.sql. already created? use environment variable LOAD_DATA_ONLY"
        exit 1
    fi
fi

TABLES="crawl link chunk token ada_002 score query"
SCRIPT=/data/copy-tables.sql
echo "" > $SCRIPT

for table in `echo $TABLES`; do
    csv="/data/$table.csv"
    if [ -f "$csv" ]; then
        if [ -n "$DISABLE_TRIGGER_ALL" ]; then
            echo "ALTER TABLE $LOUIS_SCHEMA.$table DISABLE TRIGGER ALL;" >> $SCRIPT
        fi
        COMMAND="\COPY $LOUIS_SCHEMA.$table FROM '$csv' WITH DELIMITER ';' CSV HEADER"
        echo "$COMMAND" >> $SCRIPT
        if [ -n "$DISABLE_TRIGGER_ALL" ]; then
            echo "ALTER TABLE $LOUIS_SCHEMA.$table ENABLE TRIGGER ALL;" >> $SCRIPT
        fi
    else
        echo "input file $csv for table $table does not exist"
    fi
done

for table in `echo $TABLES`; do
    if [ -f "$csv" ]; then
        echo "REINDEX TABLE $LOUIS_SCHEMA.$table;" >> $SCRIPT
    fi
done
echo "VACUUM ANALYZE;" >> $SCRIPT

echo "EXECUTING:"
echo "-----"
cat $SCRIPT
echo "-----"

psql "$LOUIS_DSN" -v ON_ERROR_STOP=1 --single-transaction -f $SCRIPT