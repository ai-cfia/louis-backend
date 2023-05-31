# inspection.gc.ca crawler

## planned functionality

* crawl extract content (main tag) from main website and store in postgres
* separate content into chunks
* get embeddings from chunks
* index documents using embeddings and vectorstore
* build search API (converting queries to embedding and searching vectorstore)
* plugin search functionality in conversational agent

stretch

* build indexing-on-request API (can accept, queue and process external links)

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

## database client

Suggested: https://dbeaver.io/download/

## References

* [text-embedding-ada-002](https://platform.openai.com/docs/guides/embeddings)
* [pgvector](https://github.com/pgvector/pgvector)
* [Chunking Strategies for LLM Applications](https://www.pinecone.io/learn/chunking-strategies/)
* [Scrapy](https://docs.scrapy.org/en/latest/index.html)
* [Scrapy: saving to postgres](https://scrapeops.io/python-scrapy-playbook/scrapy-save-data-postgres/)
* [Switch postgresql to utf-8](https://tutorials.technology/tutorials/How-to-change-postgresql-database-encoding-to-UTF8-from-SQL_ASCII.html?utm_content=cmp-true)
* [pgvector](https://github.com/pgvector/pgvector)
* [Tutorial: Explore Azure OpenAI Service embeddings and document search](https://learn.microsoft.com/en-us/azure/cognitive-services/openai/tutorials/embeddings)