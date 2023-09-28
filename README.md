# louis backend

## Overview

This project contains the code for the backend of the louis project, tying the database to both louis-frontend and louis-backend

For more information ou Louis, refer to: [https://github.com/ai-cfia/louis](Louis main documentation).

## Table of content:

* [API documentation](docs/API.md)
* [Deployment](docs/DEPLOYMENT.md)

## functionality overview

* search API: converting queries to embedding and searching vectorstore
* agent logic (based on langchain) to take user queries and obtain answers from searcg results, LLM and other search tools

## planned functionality

* switch to tool and have LLM decide which tool to use to answer user query

## Layers

Layers:

* louis.blueprints: API are defined here as blueprints for Flask
* louis.agents: agent logic
* louis.prompts: natural language configuration of agents
* louis.tools: tools that can be used by the LLM, described with natural language

## References


* [deploying flask container to Azure](http://blog.pamelafox.org/2022/09/deploying-containerized-flask-app-to.html)
