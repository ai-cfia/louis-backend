DIRNAME=`dirname $0`
. $DIRNAME/lib.sh
if [ -z "$1" ]; then
    echo "usage: $0 output_schema"
    exit 1
fi
NEW_SCHEMA=$1
RELPATH=dumps/$NEW_SCHEMA
OUTPUT_DIR=`realpath $RELPATH`

if [ -d "$OUTPUT_DIR" ]; then
    echo "Error: Directory exist: $OUTPUT_DIR"
    exit 2
fi

$PSQL_ADMIN < $DIRNAME/sql/schema_to_csv.sql

mkdir -p "$OUTPUT_DIR"
echo "Outputting all tables as csv to $OUTPUT_DIR"
$PSQL_ADMIN -c "select * from schema_to_csv('$TARGET_SCHEMA', '$OUTPUT_DIR')"