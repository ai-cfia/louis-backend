import psycopg2
import psycopg2.extras

def connect_db():
    connection = psycopg2.connect(database="inspection.canada.ca")
    psycopg2.extras.register_uuid()
    connection.set_isolation_level(psycopg2.extensions.ISOLATION_LEVEL_AUTOCOMMIT)
    return connection

def process_chunk_item(cursor, item):
    """Process a ChunkItem and insert it into the database."""
    try:
        data = {
                'url': item["url"],
                'title': item["title"],
                'text_content': item["text_content"],
                'tokens': item["tokens"],
                'encoding': 'cl100k_base'
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
            "INSERT INTO public.token (chunk_id, tokens, encoding)"
                " VALUES (%(chunk_id)s::UUID, %(tokens)s, %(encoding)s)"
            " RETURNING id",
            data
        )
        data['token_id'] = cursor.fetchone()[0]

        return item
    except psycopg2.IntegrityError as integrity_error:
        # ignore duplicates and keep processing
        return item

def process_crawl_item(cursor, item):
    """Process a CrawlItem and insert it into the database."""
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

def process_embedding_item(cursor, item):
    """Process an EmbeddingItem and insert it into the database."""
    try:
        cursor.execute(
            "INSERT INTO public.embedding (chunk_id, embedding, embedding_model) VALUES (%s, %s, %s)",
            (
                item["chunk_id"],
                item["embedding"],
                item["embedding_model"],
            )
        )
        return item
    except psycopg2.IntegrityError as e:
        # ignore duplicates and keep processing
        return item


def link_pages(cursor, source_url, destination_url):
    """Link two pages together in the database."""
    data = {
        'source_url': source_url,
        'destination_url': destination_url,
    }
    try:
        cursor.execute(
            "SELECT id FROM public.crawl WHERE url = %(source_url)s ORDER BY last_updated DESC LIMIT 1",
            data
        )
        data['source_crawl_id'] = cursor.fetchone()[0]
        cursor.execute(
            "SELECT id FROM public.crawl WHERE url = %(destination_url)s ORDER BY last_updated DESC LIMIT 1",
            data
        )
        data['destination_crawl_id'] = cursor.fetchone()[0]
        cursor.execute(
            "INSERT INTO public.link (source_crawl_id, destination_crawl_id) VALUES (%(source_crawl_id)s, %(destination_crawl_id)s)",
            data
        )
    except psycopg2.IntegrityError as e:
        # ignore duplicates and keep processing
        return


def fetch_links(cursor, url):
    data = {
        'source_url': url
    }
    cursor.execute(
        "SELECT url FROM public.link WHERE source_crawl_id = (SELECT id FROM public.crawl WHERE url = %(url)s ORDER BY last_updated DESC LIMIT 1)",
        data
    )
    data['destination_urls'] = cursor.fetchall()
    return data['destination_urls']