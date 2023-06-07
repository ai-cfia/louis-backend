# inspection.canada.ca crawler

## Overview

We use scrapy as a generic job queue processing facility from crawling pages (from a live connection of a cached disk version) to processing rows of data in the database. The architecture and multiprocessing facilities let us organize the code and scrapy offer a number of builtin services to monitor and manage long job queues.

Flows as follow:

* spider (such as louis/spiders/kurt.py) is instantiated and start_requests is called
  * start_request generates a series of requests (possibly from rows in the db) bound for a method of spider (parse)
* requests are handled by louis/middleware.py
  * the content for each request is fetched from a web server, filesystem or database
  * the content is turned into a response
* responses are sent back to the spider. The spider generates Item from the responses
* items are received by the louis/pipeline.py
  * items are store in the database

Layers:

* louis/db.py: any interaction with the postgresql database is done here
* louis/requests.py: creation of requests here
* louis/responses.py: creation of responses here
* louis/settings.py: configuration of the crawler. reads from .env
* louis/chunking.py: chunking logic
* louis/openai.py: openai API interactions

## planned functionality

* crawl extract content (main tag) from main website and store in postgres
* separate content into chunks
* get embeddings from chunks
* index documents using embeddings and vectorstore
* build search API (converting queries to embedding and searching vectorstore)
* plugin search functionality in conversational agent

stretch

* build indexing-on-request API (can accept, queue and process external links)

## running the crawlers

We use the crawlers in a little bit of a non-standard way.

Instead of hitting a website, we pick up the URL from disk

As a second step, we pick up rows from the database

As a third step, we pick up rows from the database to pass to the embedding API

goldie crawler: HTML from disk dump in Cache/:

```
scrapy crawl goldie --logfile goldie.log
```

hawn crawler: crawl table to chunk and token:

```
scrapy crawl hawn --logfile hawn.log
```

kurt crawler: crawl tokens to embedding

```
scrapy crawl kurt --logfile kurt.log
```


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

## References

* [text-embedding-ada-002](https://platform.openai.com/docs/guides/embeddings)
* [pgvector](https://github.com/pgvector/pgvector)
* [Chunking Strategies for LLM Applications](https://www.pinecone.io/learn/chunking-strategies/)
* [Scrapy](https://docs.scrapy.org/en/latest/index.html)
* [Scrapy: saving to postgres](https://scrapeops.io/python-scrapy-playbook/scrapy-save-data-postgres/)
* [Switch postgresql to utf-8](https://tutorials.technology/tutorials/How-to-change-postgresql-database-encoding-to-UTF8-from-SQL_ASCII.html?utm_content=cmp-true)
* [pgvector](https://github.com/pgvector/pgvector)
* [Tutorial: Explore Azure OpenAI Service embeddings and document search](https://learn.microsoft.com/en-us/azure/cognitive-services/openai/tutorials/embeddings)