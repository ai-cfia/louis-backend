# database

## database setup

We've added the devcontainer postgres feature. Config files are in

```
/home/vscode/.asdf/installs/postgres/15.3/data/*.conf
```

In the devcontainer you can start the database:

```
pg_ctl start
```

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

see extensions available: https://pgxn.org/

## database client

Suggested: https://dbeaver.io/download/

