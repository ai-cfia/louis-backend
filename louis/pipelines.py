# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import psycopg2
import psycopg2.extras

def process_chunk_item(cursor, item):
    """Process a ChunkItem and insert it into the database."""
    try:
        data = {
                'url': item["url"],
                'title': item["title"],
                'text_content': item["text_content"],
                'tokens': item["tokens"]
        }
        cursor.execute(
            "SELECT id FROM public.crawl WHERE url = %(url)s ORDER BY last_updated DESC LIMIT 1",
            data
        )
        data['crawl_id'] = cursor.fetchone()[0]
        cursor.execute(
            "INSERT INTO public.chunk (crawl_id, title, text_content)"
                " VALUES(%(crawl_id)s::UUID, %(title)s, %(text_content)s)"
            " RETURNING id",
            data
        )
        data['chunk_id'] = cursor.fetchone()[0]
        cursor.execute(
            "INSERT INTO public.token (chunk_id, tokens)"
                " VALUES (%(chunk_id)s::UUID, %(tokens)s)"
            " RETURNING id",
            data
        )
        data['token_id'] = cursor.fetchone()[0]

        return item
    except psycopg2.IntegrityError as integrity_error:
        # ignore duplicates and keep processing
        return item

def process_crawl_item(cursor, item):
    try:
        cursor.execute(
            "INSERT INTO public.crawl (url, title, lang, html_content, last_crawled, last_updated) VALUES (%s, %s, %s, %s, %s, %s)",
            (
                item["url"],
                item["title"],
                item["lang"],
                item["html_content"],
                item["last_crawled"],
                item["last_updated"],
            )
        )
        return item
    except psycopg2.IntegrityError as e:
        # ignore duplicates and keep processing
        return item

def connect_db():
    connection = psycopg2.connect(database="inspection.canada.ca")
    psycopg2.extras.register_uuid()
    connection.set_isolation_level(psycopg2.extensions.ISOLATION_LEVEL_AUTOCOMMIT)
    return connection

class LouisPipeline:
    def open_spider(self, spider):
        # open connection to postgresql database using psycopg2
        self.connection = connect_db()

    def close_spider(self, spider):
        # close connection to postgresql database using psycopg2
        self.connection.close()

    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        if 'html_content' in adapter:
            with self.connection.cursor() as cursor:
                return process_crawl_item(cursor, item)
        elif 'text_content' in adapter:
            with self.connection.cursor() as cursor:
                return process_chunk_item(cursor, item)
