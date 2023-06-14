from langchain.tools import tool

from louis import actions

@tool
def SmartSearch(query: str, max_tokens=3000) -> str:
    """
    Returns list of documents from inspection.canada.ca,
    the official website of the CFIA
    (Canadian Food Inspection Agency or Agence Canadienne d'Inspection des Aliments in french) based on
    semantic similarity to query"""
    documents = actions.smartsearch(query)
    paragraphs = []
    total_tokens = 0
    for doc in documents:
        total_tokens += doc['tokens_count']
        if total_tokens > max_tokens:
            break
        paragraph = f"{doc['title']} : {doc['url']} : {doc['content']}"
        paragraphs.append(paragraph)
    return "\n".join(paragraphs)