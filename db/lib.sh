PGBASE="inspectioncanadaca"
PSQL_ADMIN="psql $LOUIS_DSN -v ON_ERROR_STOP=1 -U postgres --single-transaction"
TARGET_SCHEMA=louis_v003
TODAY=`date +%Y-%m-%d`
