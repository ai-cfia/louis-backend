# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class CrawlItem(scrapy.Item):
    id = scrapy.Field()
    url = scrapy.Field()
    title = scrapy.Field()
    lang = scrapy.Field()
    html_content = scrapy.Field()
    last_crawled = scrapy.Field()
    last_updated = scrapy.Field()

class ChunkItem(scrapy.Item):
    id = scrapy.Field()
    crawl_uuid = scrapy.Field()
    chunk = scrapy.Field()
    chunk_hash = scrapy.Field()

class EmbeddingItem(scrapy.Item):
    chunk_id = scrapy.Field()
    embedding = scrapy.Field()
    embedding_model = scrapy.Field()