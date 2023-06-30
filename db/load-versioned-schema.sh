DIRNAME=`dirname $0`
. $DIRNAME/lib.sh
SOURCE_DIR=$1
if [ ! -d "$SOURCE_DIR" ]; then
    echo "Directory does not exist: $SOURCE_DIR"
    exit 1
fi

SCHEMA_FILE=$SOURCE_DIR/schema.sql
if [ ! -f "$SCHEMA_FILE" ]; then
    echo "File does not exist: $SCHEMA_FILE"
    exit 2
fi
$PSQL_ADMIN -d $PGBASE < $SCHEMA_FILE
