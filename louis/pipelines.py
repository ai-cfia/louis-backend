# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter

import louis.db as db

class LouisPipeline:
    def open_spider(self, _spider):
        """open connection to the database"""
        self.connection = db.connect_db()

    def close_spider(self, _spider):
        """close connection to database"""
        self.connection.close()

    def process_item(self, item, spider):
        """process item and store in database"""
        if spider.name == 'goldie':
            with self.connection.cursor() as cursor:
                return db.store_crawl_item(cursor, item)
        elif spider.name == 'hawn':
            with self.connection.cursor() as cursor:
                return db.store_chunk_item(cursor, item)
        elif spider.name == 'kurt':
            with self.connection.cursor() as cursor:
                return db.store_embedding_item(cursor, item)
