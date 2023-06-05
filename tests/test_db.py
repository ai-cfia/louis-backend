import unittest
import time

from louis.items import ChunkItem, CrawlItem
from louis.pipelines import process_chunk_item, connect_db, process_crawl_item

class TestDB(unittest.TestCase):
    def setUp(self):
        self.connection = connect_db()

    def tearDown(self):
        self.connection.close()

    def test_process_chunk_item(self):
        """sample test to check if process_chunk_item works"""""
        with self.connection.cursor() as cursor:
            process_chunk_item(cursor, ChunkItem({
                "url": "https://inspection.canada.ca/splash",
                "title": "Test Title",
                "text_content": "Test Text Content",
                "token_count": 3,
                "tokens": [1,2,3],
            }))
            self.connection.rollback()

    def test_process_crawl_item(self):
        """sample test to check if process_crawl_item work"""
        with self.connection.cursor() as cursor:
            process_crawl_item(cursor, CrawlItem({
                "url": "https://inspection.canada.ca/splash",
                "title": "Test Title",
                "lang": "fr",
                "html_content": "<html><body><p>Test Text Content</p></body></html>",
                "last_updated": "2023-06-01",
                "last_crawled": time.time()
            }))
            self.connection.rollback()
