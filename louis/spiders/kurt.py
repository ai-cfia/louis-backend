"""Spider that fetches chunk tokens from the Kurt API and converts them to embedding items"""

import scrapy

from louis.items import EmbeddingItem
from louis.openai import fetch_embedding

import louis.db as db

def convert_to_embedding_items(response):
    chunk_token = response.json()
    embedding = fetch_embedding(chunk_token['tokens'])
    yield EmbeddingItem(
        {
            "token_id": chunk_token['token_id'],
            "embedding": embedding,
            "embedding_model": 'text-embedding-ada-002'
        }
    )


class KurtSpider(scrapy.Spider):
    """Spider that fetches chunk tokens from the Kurt API and converts them to embedding items"""
    name = "kurt"

    def __init__(self, category=None, *args, **kwargs):
        super(KurtSpider, self).__init__(*args, **kwargs)
        self.connection = db.connect_db()
        self.dbname = self.connection.info.dbname

    def start_requests(self):
        with db.cursor(self.connection) as cursor:
            chunk_ids = db.fetch_chunk_id_without_embedding(cursor)
        for chunk_id in chunk_ids:
            url = db.create_postgresql_url(self.dbname, 'chunk', chunk_id, {'encoding': 'cl100k_base'})
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        yield from convert_to_embedding_items(response)