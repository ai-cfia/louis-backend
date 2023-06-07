import unittest

import louis.openai as openai

class TestResponses(unittest.TestCase):
    def test_fetch_embedding(self):
        embedding = openai.fetch_embedding([1,2,3])
        self.assertEqual(len(embedding), 1536)