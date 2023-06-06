"""Database functions for the Louis project."""

import psycopg2
import psycopg2.extras
import psycopg2.sql as sql

def connect_db():
    """Connect to the postgresql database and return the connection."""
    connection = psycopg2.connect(database="inspection.canada.ca")
    psycopg2.extras.register_uuid()
    connection.set_isolation_level(psycopg2.extensions.ISOLATION_LEVEL_AUTOCOMMIT)
    return connection

def store_chunk_item(cursor, item):
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
    except psycopg2.IntegrityError:
        # ignore duplicates and keep processing
        return item

def store_crawl_item(cursor, item):
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
    except psycopg2.IntegrityError:
        # ignore duplicates and keep processing
        return item

def store_embedding_item(cursor, item):
    """Process an EmbeddingItem and insert it into the database."""
    try:
        data = {
            'token_id': item["token_id"],
            'embedding': item["embedding"],
            'embedding_model': item["embedding_model"],
        }
        query = sql.SQL(
                'INSERT INTO public.{embedding_model} (token_id, embedding)'
                ' VALUES (%(token_id)s, %(embedding)s)'
            ).format(embedding_model=sql.Identifier(data['embedding_model'])).as_string(cursor)
        cursor.execute(
           query,
            data
        )
        return item
    except psycopg2.IntegrityError:
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
        data['source_crawl_id'] = cursor.fetchone()['id']
        cursor.execute(
            "SELECT id FROM public.crawl WHERE url = %(destination_url)s ORDER BY last_updated DESC LIMIT 1",
            data
        )
        data['destination_crawl_id'] = cursor.fetchone()['id']
        cursor.execute(
            "INSERT INTO public.link (source_crawl_id, destination_crawl_id)"
            " VALUES (%(source_crawl_id)s, %(destination_crawl_id)s)",
            data
        )
    except psycopg2.IntegrityError:
        # ignore duplicates and keep processing
        return


def fetch_links(cursor, url):
    """Fetch all links from a given url."""
    data = {
        'source_url': url
    }
    cursor.execute(
        "SELECT url FROM public.link"
        " JOIN public.crawl ON public.link.destination_crawl_id = public.crawl.id"
        " WHERE source_crawl_id = ("
            " SELECT id FROM public.crawl WHERE url = %(source_url)s"
            " ORDER BY last_updated DESC LIMIT 1)",
        data
    )
    data['destination_urls'] = [r[0] for r in cursor.fetchall()]
    return data['destination_urls']

def fetch_chunk_id_without_embedding(cursor, embedding_model='text-embedding-ada-002'):
    """Fetch all chunk ids without an embedding."""
    query = sql.SQL(
        "SELECT chunk_id FROM public.chunk"
        " JOIN public.token ON public.chunk.id = public.token.chunk_id"
        " LEFT JOIN public.{embedding_model} ON public.token.id = public.{embedding_model}.token_id"
        " WHERE public.{embedding_model}.embedding IS NULL"
    ).format(embedding_model=sql.Identifier(embedding_model)).as_string(cursor)
    cursor.execute(query)
    return cursor.fetchall()

def fetch_crawl_row(cursor, url):
    """Fetch the most recent crawl row for a given url."""
    data = {
        'url': url
    }
    cursor.execute(
        "SELECT * FROM public.crawl WHERE url = %(url)s ORDER BY last_updated DESC LIMIT 1",
        data
    )
    return cursor.fetchone()

def fetch_chunk_token_row(cursor, chunk_id):
    """Fetch the most recent chunk token for a given chunk id."""
    data = {
        'chunk_id': chunk_id
    }
    cursor.execute(
        "SELECT * FROM public.chunk"
        " JOIN public.token ON public.chunk.id = public.token.chunk_id"
        " JOIN public.crawl ON public.chunk.crawl_id = public.crawl.id"
        " WHERE public.chunk.id = %(chunk_id)s LIMIT 1",
        data
    )
    return cursor.fetchone()

def cursor(connection):
    """Return a cursor for the given connection."""
    return connection.cursor(cursor_factory=psycopg2.extras.DictCursor)