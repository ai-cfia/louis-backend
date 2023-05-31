from urllib.parse import urlparse
import scrapy

def extract_urls(response, parse):
    for href in response.xpath("//a/@href").getall():
        if href.endswith('pdf'):
            continue
        # remove anchors and query params urls
        href = href.split('#')[0]
        href = href.split('?')[0]
        if href.startswith('http'):
            yield scrapy.Request(href, parse)
        if href.startswith('/'):
            # add relative url to full domain
            parsed = urlparse(response.url)
            href = parsed.scheme + "://" + parsed.netloc + href
            yield scrapy.Request(href, parse)