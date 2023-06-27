"""test database functions"""
import json
import unittest
import os

import louis.db as db


CWD = os.path.dirname(os.path.realpath(__file__))

embedding_table = """
create table if not exists public."{embedding_model}" (
	id uuid default uuid_generate_v4 (),
	token_id uuid references public.token(id),
	embedding vector(1536),
	primary key(id),
	unique(token_id)
);
"""

class TestMatchDocuments(unittest.TestCase):
    """Test the database functions"""
    def setUp(self):
        self.connection = db.connect_db()

    def tearDown(self):
        self.connection.close()

    def test_match_documents(self):
        # query_embedding = louis.openai.fetch_embedding('what are the cooking temperatures for e.coli?')
        with open(os.path.join(CWD, "embeddings/what are the cooking temperatures for e.coli?.json"), encoding='utf-8') as embeddings_file:
            query_embedding = json.loads(embeddings_file.read())
        with db.cursor(self.connection) as cursor:
            documents = db.match_documents(cursor, query_embedding)
        self.assertEqual(len(documents), 10)
        self.assertEqual(str(documents[0]['title']), 'Control measures for Listeria monocytogenes in ready-to-eat foods - Canadian Food Inspection Agency')
        self.assertEqual(str(documents[0]['id']), 'cfa971b6-48f5-4ad4-992c-a1b4b2fb1b4d')