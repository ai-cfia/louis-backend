import re
import time
import scrapy
from bs4 import BeautifulSoup, Comment

from louis.items import CrawlItem
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

def convert_to_chunk_items(url, soup):
    wrap_headers(soup)
    title = soup.h1.text
    for b in soup.select('.h2-block'):
        paragraphs = [p.get_text() for p in b.select('p')]
        urls = [(u.get_text(), u['href']) for u in b.select('a')]
        content = "\n".join(paragraphs)

        yield {
            'url': url,
            'title': title,
            'subtitle': b.h2.text,
            'content': content,
            'urls': urls
        }

def convert_to_crawl_item(response):
    title = " ".join([t.get() for t in response.xpath("//title/text()")])
    title = re.sub(r'\s+', ' ', title).strip()
    last_updated =  response.xpath("//time/text()").get()
    content = clean(response)
    url = response.url
    now = int(time.time())
    lang = 'en'
    if url.find('/fra/') != -1:
        lang = 'fr'
    
    yield CrawlItem({
        'url': url,
        'title': title,
        'lang': lang,
        'html_content': content,
        'last_crawled': now,
        'last_updated': last_updated
    })

def clean(response):
    main = response.css('main')
    main.css('aside').drop()
    main.css('.pagedetails').drop()
    main.css('script').drop()
    main.css('.nojs-hide').drop()
    soup = BeautifulSoup(main.get(), "lxml")
    # remove comments
    [c.extract() for c in soup.findAll(string=lambda text:isinstance(text, Comment))]
    content = str(soup)
    return re.sub(r'\s+', ' ', content).strip()

class GoldieSpider(scrapy.Spider):
    name = "goldie"
    allowed_domains = ["inspection.gc.ca", "inspection.canada.ca"]
    start_urls = ["https://inspection.canada.ca/splash"]

    def parse(self, response):
        yield from convert_to_crawl_item(response)
        yield from extract_urls(response, self.parse)
