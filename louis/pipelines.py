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

        self.connection = psycopg2.connect(database="inspection.gc.ca")
                                           
    def close_spider(self, spider):
        # close connection to postgresql database using psycopg2

        self.connection.close()

    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        cursor = self.connection.cursor()
        cursor.execute("INSERT INTO public.crawl (url, title, lang, html_content, last_crawled, last_updated) VALUES (%s, %s, %s, %s, %s, %s)",
                       (adapter['url'], adapter['title'], adapter['lang'], adapter['html_content'], adapter['last_crawled'], adapter['last_updated']))
        self.connection.commit()
        return item
