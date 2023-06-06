import unittest
import time

import louis.items as items
import louis.db as db

import uuid

class TestDB(unittest.TestCase):
    """Test the database functions"""
    def setUp(self):
        self.connection = db.connect_db()

    def tearDown(self):
        self.connection.close()

    def test_schema(self):
        """sample test to check if the schema is correct and idempotent"""
        with open("schema.sql", encoding='utf-8') as schema_file:
            schema = schema_file.read()

        with db.cursor(self.connection) as cursor:
            cursor.execute(schema)
            self.connection.rollback()

    def test_store_chunk_item(self):
        """sample test to check if store_chunk_item works"""""
        with self.connection.cursor() as cursor:
            db.store_chunk_item(cursor, items.ChunkItem({
                "url": "https://inspection.canada.ca/splash",
                "title": "Test Title",
                "text_content": "Test Text Content",
                "token_count": 3,
                "tokens": [1,2,3],
            }))
            self.connection.rollback()

    def test_store_crawl_item(self):
        """sample test to check if store_crawl_item work"""
        with db.cursor(self.connection) as cursor:
            db.store_crawl_item(cursor, items.CrawlItem({
                "url": "https://inspection.canada.ca/splash",
                "title": "Test Title",
                "lang": "fr",
                "html_content": "<html><body><p>Test Text Content</p></body></html>",
                "last_updated": "2023-06-01",
                "last_crawled": time.time()
            }))
            self.connection.rollback()

    def test_store_embedding_item(self):
        """sample test to check if store_embedding_item works"""
        with db.cursor(self.connection) as cursor:
            db.store_embedding_item(cursor, items.EmbeddingItem({
                "token_id": "00000000-0000-0000-0000-000000000000",
                "embedding": list(range(0, 1536)),
                "embedding_model": "text-embedding-ada-002"
            }))
            self.connection.rollback()

    def test_link_pages_and_fetch_links(self):
        """sample test to check if link_pages works"""
        with db.cursor(self.connection) as cursor:
            source_url = "https://inspection.canada.ca/splash"
            destination_url = "https://inspection.canada.ca/animal-health/terrestrial-animals/exports/pets/australia/eng/1321292836314/1321292933011"
            db.link_pages(cursor, source_url, destination_url)
            links = db.fetch_links(cursor, "https://inspection.canada.ca/splash")
            self.connection.rollback()
        self.assertEqual(links, [destination_url])

    def test_fetch_crawl_row(self):
        """sample test to check if fetch_crawl_row works"""
        with db.cursor(self.connection) as cursor:
            row = db.fetch_crawl_row(cursor, "https://inspection.canada.ca/splash")
            self.connection.rollback()
        self.assertEqual(row['url'], "https://inspection.canada.ca/splash")
        self.assertEqual(row['id'], uuid.UUID("37ea48dc-f082-44fe-b48d-b4e6b92582ed"))

    def test_fetch_chunk_row(self):
        """sample test to check if fetch_chunk_row works"""
        with db.cursor(self.connection) as cursor:
            # select id from chunk join crawl ON public.chunk.crawl_id = public.crawl.id where url = 'https://inspection.canada.ca/splash'
            row = db.fetch_chunk_token_row(cursor, "5f3f01f1-0772-43a0-94b8-8547651a3562")
            self.connection.rollback()
        self.assertEqual(row['url'], "https://inspection.canada.ca/splash")
