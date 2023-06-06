import scrapy
import json

from louis.items import EmbeddingItem
from louis.openai import fetch_embedding

from louis.db import fetch_links, connect_db, fetch_chunk_id_without_embedding

def convert_to_embedding_items(response):
    chunk_token = response.json()
    embedding = fetch_embedding(chunk_token.tokens)
    yield EmbeddingItem(
        {
            "chunk_id": chunk_token['id'],
            "embedding": embedding,
            "embedding_model": 'text-embedding-ada-002'
        }
    )


class KurtSpider(scrapy.Spider):
    """Spider that fetches chunk tokens from the Kurt API and converts them to embedding items"""
    name = "kurt"

    def __init__(self, category=None, *args, **kwargs):
        super(KurtSpider, self).__init__(*args, **kwargs)
        self.connection = connect_db()
        self.dbname = self.connection.info.dbname

    def start_requests(self):
        with self.connection.cursor() as cursor:
            chunk_ids = fetch_chunk_id_without_embedding(cursor)
        for chunk_id in chunk_ids:
            url = f'postgresql://{self.dbname}/public/chunk_token_cl100k_base/{chunk_id}'
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        yield from convert_to_embedding_items(response)