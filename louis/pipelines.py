# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter

import louis.db as db

class LouisPipeline:
    def open_spider(self, spider):
        # open connection to postgresql database using psycopg2
        self.connection = db.connect_db()

    def close_spider(self, spider):
        # close connection to postgresql database using psycopg2
        self.connection.close()

    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        if 'html_content' in adapter:
            with self.connection.cursor() as cursor:
                return db.store_crawl_item(cursor, item)
        elif 'text_content' in adapter:
            with self.connection.cursor() as cursor:
                return db.store_chunk_item(cursor, item)
        elif 'embedding' in adapter:
            with self.connection.cursor() as cursor:
                return db.store_embedding_item(cursor, item)
