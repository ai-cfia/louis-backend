# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import psycopg2


class LouisPipeline:

    def open_spider(self, spider):
        # open connection to postgresql database using psycopg2
        self.connection = psycopg2.connect(database="inspection.canada.ca")
        self.connection.set_isolation_level(psycopg2.extensions.ISOLATION_LEVEL_AUTOCOMMIT)

    def close_spider(self, spider):
        # close connection to postgresql database using psycopg2
        self.connection.close()

    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        if adapter['html_content']:
            try:
                with self.connection.cursor() as cursor:
                    cursor.execute("INSERT INTO public.crawl (url, title, lang, html_content, last_crawled, last_updated) VALUES (%s, %s, %s, %s, %s, %s)",
                                (adapter['url'], adapter['title'], adapter['lang'], adapter['html_content'], adapter['last_crawled'], adapter['last_updated']))
                    return item
            except psycopg2.IntegrityError as e:
                # ignore duplicates and keep processing
                return item
        if adapter['text_content']:
            try:
                with self.connection.cursor() as cursor:
                    cursor.execute("INSERT INTO public.chunk (url, title, subtitle, text_content) VALUES (%s, %s, %s, %s, %s, %s)",
                                (adapter['url'], adapter['title'], adapter['subtitle'], adapter['text_content']))
                    return item
            except psycopg2.IntegrityError as e:
                # ignore duplicates and keep processing
                return item            