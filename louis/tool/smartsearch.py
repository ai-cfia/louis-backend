from langchain.tools import tool

from louis import actions

@tool
def SmartSearch(query: str) -> str:
    """
    Returns list of documents from inspection.canada.ca,
    the official website of the CFIA
    (Canadian Food Inspection Agency or Agence Canadienne d'Inspection des Aliments in french) based on
    semantic similarity to query"""
    documents = actions.smartsearch(query)
    paragraphs = []
    for doc in documents:
        tokens_count = doc['tokens_count']
        if tokens_count > 256:
            proportional_length = int(256/tokens_count*len(doc['content']))
            doc['content'] = doc['content'][0:proportional_length] + "..."
        paragraph = f"{doc['title']} from {doc['url']}: {doc['content']}"
        paragraphs.append(paragraph)
    return "\n".join(paragraphs)