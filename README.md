# inspection.canada.ca crawler

## Table of content:


* [Crawler documentation](CRAWL.md)
* [DB documentation](DB.md)
* [API documentation](API.md)

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