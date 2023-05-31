import re
import time
import scrapy
from bs4 import BeautifulSoup, Comment

from louis.items import ChunkItem
from louis.requests import extract_urls

def wrap_headers(soup):
    last_div = None
    for tag in soup.select("h2, p"):
        if tag.name == "h2":
            last_div = tag.wrap(soup.new_tag("div", **{"class": "h2-block"}))
            last_div.insert(0, "\n")
            last_div.append("\n")
            continue

        if last_div is not None:
            last_div.append(tag)
            last_div.append("\n")

def convert_to_chunk_items(response):
    soup = BeautifulSoup(response.body, "lxml")
    wrap_headers(soup)
    title = soup.h1.text
    for b in soup.select('.h2-block'):
        paragraphs = [p.get_text() for p in b.select('p')]
        urls = [(u.get_text(), u['href']) for u in b.select('a')]
        content = "\n".join(paragraphs)

        yield ChunkItem({
            'url': url,
            'title': title,
            'subtitle': b.h2.text,
            'text_content': content,
            'urls': urls
        })

class HawnSpider(scrapy.Spider):
    name = "hawn"
    allowed_domains = ["inspection.gc.ca", "inspection.canada.ca"]
    start_urls = ["https://inspection.canada.ca/splash"]

    def parse(self, response):
        yield from convert_to_chunk_items(response)
        yield from extract_urls(response, self.parse)
