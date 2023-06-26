DIRNAME=`dirname $0`
. $DIRNAME/lib.sh

$PSQL_ADMIN -f $DIRNAME/sql/fix-utf8-template.sql
$PSQL_ADMIN -c "CREATE USER $USER; ALTER USER $USER WITH SUPERUSER;"
createdb -E utf-8 inspection.canada.ca
pip install pgxnclient
pgxn install vector
$DIRNAME/load-db.sh dumps/inspection.canada.ca.2023-06-09.pg_dump