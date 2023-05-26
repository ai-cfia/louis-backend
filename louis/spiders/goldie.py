import scrapy
from bs4 import BeautifulSoup, Comment

def wrap_headers(soup):
    last_div = None
    for tag in soup.select("h2, p"):   # or soup.find_all(["h1", "p"], recursive=False) if there are inner tags
        if tag.name == "h2":
            last_div = tag.wrap(soup.new_tag("div", **{"class": "h2-block"}))
            last_div.insert(0, "\n")
            last_div.append("\n")
            continue

        if last_div is not None:
            last_div.append(tag)
            last_div.append("\n")

def convert_to_dict(url, soup):
    wrap_headers(soup)
    title = soup.h1.text
    for b in soup.select('.h2-block'):
        paragraphs = [p.get_text() for p in b.select('p')]
        urls = [(u.get_text(), u['href']) for u in b.select('a')]
        content = "\n".join(paragraphs)
        print(urls)
        yield {
            'url': url,
            'title': title,
            'subtitle': b.h2.text,
            'content': content,
            'urls': urls
        }

def clean(response):
    main = response.css('main')
    main.css('aside').drop()
    main.css('.pagedetails').drop()
    main.css('script').drop()
    main.css('.nojs-hide').drop()
    soup = BeautifulSoup(main.get(), "lxml")
    # remove comments
    [c.extract() for c in soup.findAll(string=lambda text:isinstance(text, Comment))]
    return soup

class GoldieSpider(scrapy.Spider):
    name = "goldie"
    allowed_domains = ["inspection.gc.ca"]
    start_urls = ["https://inspection.canada.ca/inspection-and-enforcement/enforcement-of-the-sfcr/eng/1546989322632/1547741756885"]

    def parse(self, response):
        soup = clean(response)
        yield from convert_to_dict(response.url, soup)
