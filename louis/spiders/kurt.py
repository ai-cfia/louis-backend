import scrapy
import json

from louis.items import EmbeddingItem
from louis.embedding import fetch_embedding

from louis.db import fetch_links, connect_db

def convert_to_embedding_items(response):
    chunk_tokens = json.loads(response.body)
    embedding = fetch_embedding(chunk_tokens.tokens)
    yield EmbeddingItem(
        {
            "chunk_id": chunk_tokens['id'],
            "embedding": embedding,
            "embedding_model": 'text-embedding-ada-002'
        }
    )


class KurtSpider(scrapy.Spider):
    name = "kurt"
    allowed_domains = ["inspection.gc.ca", "inspection.canada.ca"]
    start_urls = ["https://inspection.canada.ca/splash"]

    def __init__(self, category=None, *args, **kwargs):
        super(KurtSpider, self).__init__(*args, **kwargs)
        self.connection = connect_db()

    def parse(self, response):
        yield from convert_to_embedding_items(response)
        with self.connection.cursor() as cursor:
            destination_urls = fetch_links(cursor, response.url)
        for url in destination_urls:
            yield Request(url, callback=self.parse, headers={'Referer': response.url})