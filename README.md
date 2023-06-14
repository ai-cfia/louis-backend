# inspection.canada.ca crawler

## Table of content:


* [Crawler documentation](CRAWL.md)
* [DB documentation](DB.md)
* [API documentation](API.md)

## Deployment

Edit configurations

* .env.prod: your .env for your container
* gunicorn_config.py: production WSGI server

Build (do this from your WSL Ubuntu where Docker is already installed):

```
docker build -t louis-demo .
```

test locally:

```
docker run -p 5000:5000 louis-demo
```

output:

```
ngadamr@QCMONTC701988P:~/src/louis-crawler$ docker run -p 5000:5000 louis-demo
[2023-06-14 19:12:56 +0000] [1] [INFO] Starting gunicorn 20.1.0
[2023-06-14 19:12:56 +0000] [1] [INFO] Listening at: http://0.0.0.0:5000 (1)
[2023-06-14 19:12:56 +0000] [1] [INFO] Using worker: gthread
[2023-06-14 19:12:56 +0000] [7] [INFO] Booting worker with pid: 7
[2023-06-14 19:12:57 +0000] [8] [INFO] Booting worker with pid: 8
[2023-06-14 19:12:57 +0000] [23] [INFO] Booting worker with pid: 23
[2023-06-14 19:12:57 +0000] [24] [INFO] Booting worker with pid: 24
INFO:numexpr.utils:NumExpr defaulting to 8 threads.
INFO:numexpr.utils:NumExpr defaulting to 8 threads.
INFO:numexpr.utils:NumExpr defaulting to 8 threads.
INFO:numexpr.utils:NumExpr defaulting to 8 threads.
```

## pushing to azure

You first need to push the container to the private registry:

```
docker tag louis-demo $CONTAINER_REGISTRY.azurecr.io/louis-demo
docker login -u $CONTAINER_REGISTRY_ADMIN --pasword-stdin $CONTAINER_REGISTRY
docker push $CONTAINER_REGISTRY.azurecr.io/louis-demo
```

The password and username $CONTAINER_REGISTRY_ADMIN is from from Portal Azure Access Keys page of the container registry view.

## Layers

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


## References

* [text-embedding-ada-002](https://platform.openai.com/docs/guides/embeddings)
* [pgvector](https://github.com/pgvector/pgvector)
* [Chunking Strategies for LLM Applications](https://www.pinecone.io/learn/chunking-strategies/)
* [Scrapy](https://docs.scrapy.org/en/latest/index.html)
* [Scrapy: saving to postgres](https://scrapeops.io/python-scrapy-playbook/scrapy-save-data-postgres/)
* [Switch postgresql to utf-8](https://tutorials.technology/tutorials/How-to-change-postgresql-database-encoding-to-UTF8-from-SQL_ASCII.html?utm_content=cmp-true)
* [pgvector](https://github.com/pgvector/pgvector)
* [Tutorial: Explore Azure OpenAI Service embeddings and document search](https://learn.microsoft.com/en-us/azure/cognitive-services/openai/tutorials/embeddings)
* [How to optimize performance when using pgvector on Azure Cosmos DB for PostgreSQL](https://learn.microsoft.com/en-us/azure/cosmos-db/postgresql/howto-optimize-performance-pgvector)
* [Building a custom connector](https://docs.elastic.co/search-ui/guides/building-a-custom-connector)
* [How to change PostgreSQL database encoding to UTF-8](https://www.shubhamdipt.com/blog/how-to-change-postgresql-database-encoding-to-utf8/)
* [deploying flask container to Azure](http://blog.pamelafox.org/2022/09/deploying-containerized-flask-app-to.html)
