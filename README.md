# louis backend

## Overview

This project contains the Python code and SQL schema for the Louis project

For more information ou Louis, refer to: [https://github.com/ai-cfia/louis](Louis main documentation).

## Table of content:

* [Deployment](docs/DEPLOYMENT.md)
* [Crawler documentation](docs/CRAWL.md)
* [DB documentation](docs/DB.md)
* [API documentation](docs/API.md)

## functionality overview

* crawl extract content (main tag) from main website and store in postgres
* separate content into chunks
* get embeddings from chunks
* index documents using embeddings and vectorstore
* search API: converting queries to embedding and searching vectorstore
* agent logic (based on langchain) to take user queries and obtain answers from searcg results, LLM and other search tools

## planned functionality

* improve search performance
* index more knowledge based related to the CFIA regulatory work
* build continuous indexing of new pages
* build indexing-on-request API (can accept, queue and process external links)
* switch to tool and have LLM decide which tool to use to answer user query

## Layers

Layers:

* louis.db: any interaction with the postgresql database is done here
* louis.blueprints: API are defined here as blueprints for Flask
* louis.agents: agent logic
* louis.crawler:
  * .requests: creation of requests here
  * .responses: creation of responses here
  * .settings: configuration of the crawler. reads from .env
  * .chunking.py: chunking logic (splitting docs into logical blocks)
* louis.models: interactions with LLM
  * openai.py: openai API interactions
* louis.prompts: natural language configuration of agents
* louis.tools: tools that can be used by the LLM, described with natural language

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
