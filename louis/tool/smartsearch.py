from langchain.tools import tool

from louis import actions

@tool
def smartsearch(query: str) -> str:
    """Returns list of documents from inspection.canada.ca based on semantic similarity to query"""
    documents = actions.smartsearch(query)
    return "\n".join([f"{doc['title']} from {doc['url']}: {doc['content']}" for doc in documents])