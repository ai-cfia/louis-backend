"""Database functions for the Louis project."""
import os
import urllib
import logging

LOGGER = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)

import psycopg
import psycopg.sql as sql

from pgvector.psycopg import register_vector

import numpy as np

from psycopg.rows import dict_row

LOUIS_DSN = os.environ.get("LOUIS_DSN")

def connect_db():
    """Connect to the postgresql database and return the connection."""
    connection = psycopg.connect(
        conninfo=LOUIS_DSN,
        row_factory=dict_row,
        autocommit=True)
    # psycopg.extras.register_uuid()
    register_vector(connection)
    return connection

def cursor(connection):
    """Return a cursor for the given connection."""
    return connection.cursor()

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
        data['crawl_id'] = cursor.fetchone()['id']
        cursor.execute(
            "INSERT INTO public.chunk (crawl_id, title, text_content)"
                " VALUES(%(crawl_id)s::UUID, %(title)s, %(text_content)s)"
            " RETURNING id",
            data
        )
        data['chunk_id'] = cursor.fetchone()['chunk_id']
        cursor.execute(
            "INSERT INTO public.token (chunk_id, tokens, encoding)"
                " VALUES (%(chunk_id)s::UUID, %(tokens)s::vector, %(encoding)s)"
            " RETURNING id",
            data
        )
        data['token_id'] = cursor.fetchone()['token_id']

        return item
    except psycopg.IntegrityError:
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
    except psycopg.IntegrityError:
        # ignore duplicates and keep processing
        return item

def store_embedding_item(cursor, item):
    """Process an EmbeddingItem and insert it into the database."""
    try:
        data = {
            'token_id': item["token_id"],
            # TODO: shouldn't python-pgvector support casting from smallint[] to vector?
            'embedding': np.array(item["embedding"]),
            'embedding_model': item["embedding_model"],
        }
        query = sql.SQL(
                'INSERT INTO public.{embedding_model} (token_id, embedding)'
                ' VALUES (%(token_id)s, %(embedding)s::vector)'
            ).format(embedding_model=sql.Identifier(data['embedding_model'])).as_string(cursor)
        cursor.execute(
           query,
            data
        )
        return item
    except psycopg.IntegrityError:
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
    except psycopg.IntegrityError:
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
    data['destination_urls'] = [r['url'] for r in cursor.fetchall()]
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
    return [chunk_id['chunk_id'] for chunk_id in cursor.fetchall()]

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

def fetch_chunk_token_row(cursor, url):
    """Fetch the most recent chunk token for a given chunk id."""

    # TODO: eventually we could generalize the use of these postgresql
    # url to data but for now keep it simple
    data = parse_postgresql_url(url)
    cursor.execute(
        "SELECT chunk.id as chunk_id, token.id as token_id, tokens FROM public.chunk"
        " JOIN public.token ON public.chunk.id = public.token.chunk_id"
        " JOIN public.crawl ON public.chunk.crawl_id = public.crawl.id"
        " WHERE public.chunk.id = %(entity_uuid)s LIMIT 1",
        data
    )
    # psycopg.extras.DictRow is not a real dict and will convert
    # to string as a list so we force convert to dict
    return dict(cursor.fetchone())

def create_postgresql_url(dbname, tablename, entity_uuid, parameters=None):
    if parameters is None:
        return f'postgresql://{dbname}/public/{tablename}/{entity_uuid}'
    return f'postgresql://{dbname}/public/{tablename}/{entity_uuid}?{urllib.parse.urlencode(parameters)}'


def parse_postgresql_url(url):
    """Parse a postgresql url and return a dictionary with the parameters."""
    parsed = urllib.parse.urlparse(url)
    return {
        'dbname': parsed.hostname,
        'tablename': parsed.path.split('/')[2],
        'entity_uuid': parsed.path.split('/')[3],
        'parameters': urllib.parse.parse_qs(parsed.query)
    }

def match_documents(cursor, query_embedding):
    """Match documents with a given query."""
    data = {
        # TODO: use of np.array to get it to recognize the vector type
        # is there a simpler way to do this? only reason we use this
        # dependency
        # 'query_embedding': np.array(query_embedding),
        'query_embedding': query_embedding,
        'match_threshold': 0.5,
        'match_count': 10
    }

    # cursor.callproc('match_documents', data)
    cursor.execute("SELECT * FROM match_documents(%(query_embedding)s::vector, %(match_threshold)s, %(match_count)s)", data)

    # turn into list of dict now to preserve dictionaries
    return [dict(r) for r in cursor.fetchall()]