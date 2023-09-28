# database

## layers

* louis.db: any interaction with the postgresql database is done here
* louis.models: interactions with LLM
  * openai.py: openai API interactions

## database setup

We've added the devcontainer postgres feature. Config files are in

```
/home/vscode/.asdf/installs/postgres/15.3/data/*.conf
```

In the devcontainer you can start the database:

```
pg_ctl start
```

## changing default template to utf-8

if the default database is set to SQL_ASCII, it will cause problems:

```
UPDATE pg_database SET datistemplate = FALSE WHERE datname = 'template1';
DROP DATABASE template1;
CREATE DATABASE template1 WITH TEMPLATE = template0 ENCODING = 'UTF8';
UPDATE pg_database SET datistemplate = TRUE WHERE datname = 'template1';
\c template1
VACUUM FREEZE;
```

## creating the database

```
psql -U postgres
CREATE USER vscode;
ALTER USER vscode WITH SUPERUSER;
```

and then

```
createdb -E utf-8 inspection.canada.ca
```

and then

```
psql -d inspection.canada.ca
```


## postgresql extensions

```
pip install pgxnclient
pgxn install vector
```

## loading dump

```
./load-db.sh dumps/inspection.canada.ca.2023-06-09.pg_dump
```

## workaround for psycopg2 not finding the socket file

either build from source:

```
pip install --no-binary psycopg2
```

or symlink:

```
sudo mkdir -p /var/run/postgresql
sudo ln -s /tmp/.s.PGSQL.5432 /var/run/postgresql/.s.PGSQL.5432
```



see extensions available: https://pgxn.org/


## configuration

postgresql.conf

```
log_min_duration_statement = 40
```

## testing impact of indexes by flushing cache first

stop database:

```
pg_ctl stop
```

in your OS (not the container):

```
echo 3 > /proc/sys/vm/drop_caches
```

start database:

```
pg_ctl start
```

test query:

```
time curl -X POST http://localhost:5000/search --data '{"query": "is e.coli a virus or bacteria?"}' -H "Content-Type: application/json"
```

result:

```
real    0m4.791s
user    0m0.003s
sys     0m0.016s
```

create index.

Repeat operations to clear cache.

## database client

Suggested: https://dbeaver.io/download/

## References

* [text-embedding-ada-002](https://platform.openai.com/docs/guides/embeddings)
* [pgvector](https://github.com/pgvector/pgvector)
* [Switch postgresql to utf-8](https://tutorials.technology/tutorials/How-to-change-postgresql-database-encoding-to-UTF8-from-SQL_ASCII.html?utm_content=cmp-true)
* [pgvector](https://github.com/pgvector/pgvector)
* [Tutorial: Explore Azure OpenAI Service embeddings and document search](https://learn.microsoft.com/en-us/azure/cognitive-services/openai/tutorials/embeddings)
* [How to optimize performance when using pgvector on Azure Cosmos DB for PostgreSQL](https://learn.microsoft.com/en-us/azure/cosmos-db/postgresql/howto-optimize-performance-pgvector)
* [Building a custom connector](https://docs.elastic.co/search-ui/guides/building-a-custom-connector)
* [How to change PostgreSQL database encoding to UTF-8](https://www.shubhamdipt.com/blog/how-to-change-postgresql-database-encoding-to-utf8/)