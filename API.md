## Running and testing the API

Running:

```
flask run
```

Query from the command-line:

```
curl -X POST http://localhost:5000/search --data '{"query": "is e.coli a virus or bacteria?"}' -H "Content-Type: application/json"
```

Example output available in [tests/api/is e.coli a virus or a bacteria?.json](tests/api/is e.coli a virus or a bacteria?.json).

JSON structure explanation:

* id: crawl record
* content:
* similarity: how similar this document is to the query
* title: the title of the page
* subtitle: the title or titles from the snippet
* url: the URL to the page (should be to inspection.canada.ca)